#!/usr/bin/env python3
"""Export data for the commute-policy 3D page (showcase/commute/index.html).

Source: the Transportation Engineering final project (notebooks/trans-eng-final):
zones, OD skim and the Nested Logit policy results (scenarios A-H), plus the
real rail/BRT route lines in web/public/data. Writes showcase/commute/data/commute.json.

RoyalTrans and the scenario lines (new KRL/MRT/TJ links) have no GTFS shapes, so
they are drawn as straight schematic links from zone centroid to the CBD and
flagged "schematic" in the output.

Usage (repo root):  python scripts/export_commute_showcase.py [--src REPO_ROOT]
--src lets you read the inputs from another checkout (e.g. one with newer
notebook outputs) while writing into this one.
"""
import argparse
import csv
import json
from pathlib import Path

from shapely.geometry import shape, mapping

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "showcase" / "commute" / "data" / "commute.json"
MODES = ["car", "moto", "krl", "tj", "royal", "mrt"]
GTFS_MODE = {"transjakarta": "tj"}  # route/stop type -> model mode key
# scenario -> new schematic links (zone, mode, in-vehicle time min), times as in policy_results "desc"
NEW_LINKS = {"A": [("J3b", "krl", 70)], "D": [("J1b", "tj", 90)], "E": [("J3a", "mrt", 60)], "F": [("J3b", "tj", 80), ("J3a", "tj", 80)]}
# scenario -> modes whose service level improves (more vehicles on the map)
BOOST = {"C": "krl", "G": "royal", "H": "royal"}


def rnd(c, nd=4):
    if isinstance(c[0], (int, float)):
        return [round(c[0], nd), round(c[1], nd)]
    return [rnd(x, nd) for x in c]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=str(ROOT))
    src = Path(ap.parse_args().src)
    te = src / "notebooks" / "trans-eng-final"
    zones_geo = json.load(open(te / "app/public/data/zones.geojson", encoding="utf-8"))["features"]
    policy = json.load(open(te / "app/public/data/policy_results.json", encoding="utf-8"))
    with open(te / "data/jabodetabek_zones.csv", encoding="utf-8") as f:
        zcsv = {r["zone_id"]: r for r in csv.DictReader(f)}
    with open(te / "data/od_skim_jkt.csv", encoding="utf-8") as f:
        skim = list(csv.DictReader(f))
    routes = json.load(open(src / "web/public/data/jakarta_transit_routes.geojson", encoding="utf-8"))["features"]
    stops = json.load(open(src / "web/public/data/jakarta_transit_stops.geojson", encoding="utf-8"))["features"]

    zones, cbd = [], None
    for f in zones_geo:
        p = f["properties"]
        g = shape(f["geometry"]).simplify(0.001, preserve_topology=True)
        c = g.representative_point()
        z = {"id": p["zone_id"], "name": p["zone_name"], "centroid": [round(c.x, 4), round(c.y, 4)],
             "geometry": {"type": g.geom_type, "coordinates": rnd(mapping(g)["coordinates"])}}
        if p["is_cbd"] == "True":
            cbd = z
            continue
        r = zcsv[p["zone_id"]]
        z.update({"pop": int(float(r["population"])), "income_k": float(r["avg_income_k"]), "poverty_pct": float(r["poverty_pct"]),
                  "dist_km": float(r["distance_cbd_km"]), "character": r["character"],
                  "avail": [m for m in MODES if r["avail_" + m] == "1"],
                  "skim": {s["mode"]: {"t": float(s["time_min"]), "c": float(s["cost_idr_thousand"])} for s in skim if s["origin"] == p["zone_id"]}})
        zones.append(z)
    assert cbd and len(zones) == 7, len(zones)

    scen = {}
    for k, v in policy["scenarios"].items():
        scen[k] = {kk: v[kk] for kk in ["label", "desc", "equity_dir", "mean_dCS_th_idr", "annual_aggregate_bn_idr", "n_winners", "n_losers",
                                         "dCS_by_income", "dCS_by_zone", "mode_share_base", "mode_share_policy", "mode_share_delta"]}
        scen[k]["new_links"] = [{"zone": z, "mode": m, "t": t} for z, m, t in NEW_LINKS.get(k, [])]
        scen[k]["boost"] = BOOST.get(k)
        scen[k]["toll"] = k == "B"

    out = {
        "meta": {"model": policy["model"], "lambda": round(policy["lambda_hat"], 4), "beta_cost": round(policy["beta_cost"], 4),
                 "working_days": policy["working_days"], "baseline": policy["baseline"], "n_persons": 5000},
        "cbd": cbd, "zones": zones, "scenarios": scen,
        "routes": [{"mode": GTFS_MODE.get(f["properties"]["type"], f["properties"]["type"]), "line": f["properties"]["line"], "path": rnd(f["geometry"]["coordinates"])} for f in routes],
        "stops": [{"mode": GTFS_MODE.get(f["properties"]["type"], f["properties"]["type"]), "name": f["properties"]["name"], "p": rnd(f["geometry"]["coordinates"])} for f in stops],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, separators=(",", ":"), ensure_ascii=False), encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}: {OUT.stat().st_size/1e3:.0f} kB; zones {len(zones)}, scenarios {list(scen)}, routes {len(routes)}, stops {len(stops)}")


if __name__ == "__main__":
    main()
