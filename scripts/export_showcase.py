#!/usr/bin/env python3
"""Export compact data for the 3D showcase page (showcase/index.html).

Reads the processed GeoJSON/JSON the Next.js app already uses and writes
showcase/data/showcase.json (< 3 MB). Nothing is recomputed except the step-7
mock-up station location (largest Bodetabek Q4 HH component; population-weighted centroid snapped to a member hex).

Routes/stops: web/public/data/jakarta_transit_{routes,stops}.geojson is the only
route-geometry source in the repo (data/processed/transit/ holds stops only, no
route lines), so that one is used. It covers the 74 routes / 407 stops listed
in the pipeline output.

Run from the repo root:  python scripts/export_showcase.py
"""
import json
import math
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import h3
from shapely.geometry import shape, Point, mapping
from shapely.strtree import STRtree

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "web" / "public" / "data"
OUT = ROOT / "showcase" / "data" / "showcase.json"
MAX_BYTES = 3 * 1024 * 1024
LISA = {"NS": 0, "HH": 1, "LL": 2, "HL": 3, "LH": 4}


def load(name):
    with open(DATA / name, encoding="utf-8") as f:
        return json.load(f)


def rnd_coords(c, nd):
    if isinstance(c[0], (int, float)):
        return [round(c[0], nd), round(c[1], nd)]
    return [rnd_coords(x, nd) for x in c]


def haversine_m(lon1, lat1, lon2, lat2):
    p = math.pi / 180
    a = math.sin((lat2 - lat1) * p / 2) ** 2 + math.cos(lat1 * p) * math.cos(lat2 * p) * math.sin((lon2 - lon1) * p / 2) ** 2
    return 12742000 * math.asin(math.sqrt(a))


def main():
    summary = load("equity_summary.json")
    h3_feats = load("h3_scores.geojson")["features"]
    lisa_h3 = {f["properties"]["h3_index"]: f["properties"]["lisa_cluster"] for f in load("lisa_h3.geojson")["features"]}
    kel_feats = load("kelurahan_scores.geojson")["features"]
    lisa_kel = {f["properties"]["kelurahan_id"]: f["properties"]["lisa_cluster"] for f in load("lisa_kelurahan.geojson")["features"]}
    routes = load("jakarta_transit_routes.geojson")["features"]
    stops = load("jakarta_transit_stops.geojson")["features"]
    with open(ROOT / "data/processed/poi/cbd_zones.geojson", encoding="utf-8") as f:
        cbd_feat = next(x for x in json.load(f)["features"] if x["properties"]["name"] == "Sudirman-Thamrin")
    cbd = [round(cbd_feat["properties"]["center_lon"], 5), round(cbd_feat["properties"]["center_lat"], 5)]

    assert len(h3_feats) == 9083, len(h3_feats)
    assert len(kel_feats) == 1502, len(kel_feats)
    assert len(routes) == 74, len(routes)
    assert len(stops) == 407, len(stops)

    # ---- hexes (column-oriented) ----
    hx = {k: [] for k in ["id", "lon", "lat", "pop", "tni", "tai", "gap", "q", "lisa", "cbd_min"]}
    for f in h3_feats:
        p = f["properties"]
        lat, lon = h3.cell_to_latlng(p["h3_index"])
        hx["id"].append(p["h3_index"])
        hx["lon"].append(round(lon, 5))
        hx["lat"].append(round(lat, 5))
        hx["pop"].append(int(round(p["population"] or 0)))
        hx["tni"].append(round(p["tni_score"], 3))
        hx["tai"].append(round(p["tai_score"], 3))
        hx["gap"].append(round(p["equity_gap"], 3))
        hx["q"].append(int(p["quadrant"][1]))
        hx["lisa"].append(LISA[lisa_h3[p["h3_index"]]])
        m = p["poi_reach_cbd_min"]
        hx["cbd_min"].append(-1 if m is None else int(round(m)))
    n = len(hx["q"])
    q4 = sum(1 for q in hx["q"] if q == 4)
    assert abs(100 * q4 / n - summary["h3"]["q4_pct"]) < 0.01, (q4, n)
    routed = sum(1 for m in hx["cbd_min"] if m >= 0)
    assert routed == 1021, routed

    # ---- kelurahan (simplified) ----
    kel_out, kel_geoms = [], []
    for f in kel_feats:
        p = f["properties"]
        g = shape(f["geometry"]).simplify(0.0005, preserve_topology=True)
        kel_geoms.append(g)
        kel_out.append({"type": "Feature", "geometry": {"type": g.geom_type, "coordinates": rnd_coords(mapping(g)["coordinates"], 4)},
                        "properties": {"name": p["kelurahan_name"], "kota": p["kota_kab_name"], "pop": int(p["population"] or 0),
                                       "tni": round(p["tni_score"], 3), "tai": round(p["tai_score"], 3), "q": int(p["quadrant"][1]),
                                       "lisa": LISA[lisa_kel[p["kelurahan_id"]]]}})
    kq4 = sum(1 for f in kel_out if f["properties"]["q"] == 4)
    assert abs(100 * kq4 / len(kel_out) - summary["kelurahan"]["q4_pct"]) < 0.01

    # ---- step 7: mock-up station ----
    # Bodetabek = hex centroid not inside a DKI (Jakarta*/KepulauanSeribu) kelurahan.
    tree = STRtree(kel_geoms)
    dki = [i for i, f in enumerate(kel_out) if f["properties"]["kota"].startswith(("Jakarta", "Kepulauan"))]
    dki_set = set(dki)
    is_bode = []
    for lon, lat in zip(hx["lon"], hx["lat"]):
        hit = tree.query(Point(lon, lat), predicate="within")
        is_bode.append(not any(int(i) in dki_set for i in hit))
    idx_of = {c: i for i, c in enumerate(hx["id"])}
    cand = {i for i in range(n) if hx["q"][i] == 4 and hx["lisa"][i] == 1 and is_bode[i]}  # Q4 + LISA High-High
    seen, best, best_pop = set(), None, -1
    for s in cand:
        if s in seen:
            continue
        comp, stack = [], [s]
        seen.add(s)
        while stack:
            c = stack.pop()
            comp.append(c)
            for nb in h3.grid_disk(hx["id"][c], 1):
                j = idx_of.get(nb)
                if j in cand and j not in seen:
                    seen.add(j)
                    stack.append(j)
        pop = sum(hx["pop"][c] for c in comp)
        if pop > best_pop:
            best, best_pop = comp, pop
    w = sum(hx["pop"][c] for c in best) or 1
    slon = sum(hx["lon"][c] * hx["pop"][c] for c in best) / w
    slat = sum(hx["lat"][c] * hx["pop"][c] for c in best) / w
    # The population-weighted centroid of a ragged cluster can land in its sparse part (5 Q4 hexes within
    # 1.5 km). Pin instead at the member hex whose 1.5 km catchment holds the most Q4 population.
    def catch(c):
        return sum(hx["pop"][j] for j in best_set if haversine_m(hx["lon"][c], hx["lat"][c], hx["lon"][j], hx["lat"][j]) <= 1500)
    best_set = set(best)
    snap = max(best, key=catch)
    clon, clat = slon, slat  # population-weighted centroid, kept for reference
    slon, slat = hx["lon"][snap], hx["lat"][snap]
    d = [haversine_m(slon, slat, hx["lon"][i], hx["lat"][i]) for i in range(n)]
    ring_800 = [i for i in range(n) if d[i] <= 800 and hx["q"][i] == 4]
    ring_1500 = [i for i in range(n) if d[i] <= 1500 and hx["q"][i] == 4]
    station = {"lonlat": [round(slon, 5), round(slat, 5)], "cluster_centroid": [round(clon, 5), round(clat, 5)], "component_hexes": len(best), "component_pop": best_pop,
               "q4_hexes_in_800m": len(ring_800), "q4_hexes_in_ring": len(ring_1500), "pop_in_ring": sum(hx["pop"][i] for i in ring_1500)}

    # ---- transit ----
    r_out = [{"type": "Feature", "geometry": {"type": "LineString", "coordinates": rnd_coords(f["geometry"]["coordinates"], 4)},
              "properties": {"type": f["properties"]["type"], "line": f["properties"]["line"]}} for f in routes]
    s_out = [{"type": "Feature", "geometry": {"type": "Point", "coordinates": rnd_coords(f["geometry"]["coordinates"], 4)},
              "properties": {"type": f["properties"]["type"], "name": f["properties"]["name"]}} for f in stops]
    counts = {}
    for f in r_out:
        counts[f["properties"]["type"]] = counts.get(f["properties"]["type"], 0) + 1

    try:
        commit = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, text=True).strip()
    except Exception:
        commit = "unknown"
    out = {
        "meta": {"generated": datetime.now(timezone.utc).strftime("%Y-%m-%d"), "source_commit": commit, "stats": summary, "cbd": cbd,
                 "route_counts": counts, "n_routed": routed, "total_pop": sum(hx["pop"]), "mockup_station": station},
        "hex": hx,
        "kel": {"type": "FeatureCollection", "features": kel_out},
        "routes": {"type": "FeatureCollection", "features": r_out},
        "stops": {"type": "FeatureCollection", "features": s_out},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, separators=(",", ":"), ensure_ascii=False), encoding="utf-8")
    size = OUT.stat().st_size
    print(f"wrote {OUT.relative_to(ROOT)}: {size/1e6:.2f} MB; hexes {n}, kel {len(kel_out)}, routes {counts}, stops {len(s_out)}")
    print("mockup_station", station)
    assert size < MAX_BYTES, f"{size} bytes over 3 MB"


if __name__ == "__main__":
    main()
