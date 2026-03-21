#!/usr/bin/env python3
"""
13_extract_road_network.py — Extract OSM road network and compute road metrics per kelurahan.

Uses direct Overpass API queries (not osmnx) for reliability with large bounding boxes.
Downloads road ways in 9 tiles, converts to GeoDataFrame, clips to kelurahan, computes metrics.

Pipeline steps (methodology §2.5 steps 3–4):
  1. Query Overpass API for road ways in 9 tiles across Jabodetabek
  2. Parse ways into GeoDataFrame with highway class tags
  3. Load kelurahan boundaries
  4. Compute road metrics per kelurahan by spatial overlay
  5. Export road edges GeoDataFrame and road metrics CSV

Output:
  - data/processed/networks/jabodetabek_roads.geojson
  - data/processed/networks/road_metrics_by_kelurahan.csv

Usage:
  python src/ingestion/13_extract_road_network.py
"""

import json
import logging
import sys
import time
import warnings
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import requests
from shapely.geometry import LineString

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_BOUNDARIES = PROJECT_ROOT / "data" / "raw" / "boundaries" / "jabodetabek_kelurahan.geojson"
RAW_OSM_DIR = PROJECT_ROOT / "data" / "raw" / "osm"
OUT_DIR = PROJECT_ROOT / "data" / "processed" / "networks"

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

# Jabodetabek bounding box
BBOX = {"south": -6.80, "north": -6.00, "west": 106.40, "east": 107.20}
UTM_48S = "EPSG:32748"

# Highway tags to extract per methodology §2.5
HIGHWAY_TAGS = "motorway|trunk|primary|secondary|tertiary|residential|living_street|footway|pedestrian|path|cycleway"

# Road classification
PRIMARY_SECONDARY = {"primary", "secondary", "motorway", "trunk"}
RESIDENTIAL_TERTIARY = {"residential", "tertiary", "living_street"}
FOOTWAY_PEDESTRIAN = {"footway", "pedestrian", "path", "cycleway"}

ROAD_CLASS_SCORE = {
    "motorway": 5, "trunk": 5, "primary": 5,
    "secondary": 4, "tertiary": 3,
    "residential": 2, "living_street": 2,
    "footway": 1, "pedestrian": 1, "path": 1, "cycleway": 1,
}

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", datefmt="%H:%M:%S")
log = logging.getLogger(__name__)


def make_tiles(n_rows=3, n_cols=3):
    """Split bbox into tiles for reliable Overpass queries."""
    lats = np.linspace(BBOX["south"], BBOX["north"], n_rows + 1)
    lons = np.linspace(BBOX["west"], BBOX["east"], n_cols + 1)
    tiles = []
    for i in range(n_rows):
        for j in range(n_cols):
            tiles.append((lats[i], lons[j], lats[i + 1], lons[j + 1]))
    return tiles


def query_overpass_roads(south, west, north, east, tile_idx, n_tiles):
    """Query Overpass API for road ways with geometry in a bbox."""
    cache_path = RAW_OSM_DIR / f"roads_tile_{tile_idx}.json"

    if cache_path.exists():
        log.info(f"  Tile {tile_idx}/{n_tiles}: cached")
        with open(cache_path) as f:
            return json.load(f)

    query = f"""
[out:json][timeout:180];
way["highway"~"{HIGHWAY_TAGS}"]({south},{west},{north},{east});
out geom;
"""
    log.info(f"  Tile {tile_idx}/{n_tiles}: querying ({south:.2f},{west:.2f},{north:.2f},{east:.2f})...")
    try:
        r = requests.get(OVERPASS_URL, params={"data": query}, timeout=300)
        r.raise_for_status()
        data = r.json()
    except (requests.exceptions.HTTPError, requests.exceptions.Timeout) as e:
        log.warning(f"  Tile {tile_idx} failed: {e}. Splitting into 4 sub-tiles...")
        time.sleep(15)
        data = {"elements": []}
        mid_lat = (south + north) / 2
        mid_lon = (west + east) / 2
        for si, (s2, w2, n2, e2) in enumerate([
            (south, west, mid_lat, mid_lon), (south, mid_lon, mid_lat, east),
            (mid_lat, west, north, mid_lon), (mid_lat, mid_lon, north, east),
        ], 1):
            sub_query = f'[out:json][timeout:180];way["highway"~"{HIGHWAY_TAGS}"]({s2},{w2},{n2},{e2});out geom;'
            log.info(f"    Sub-tile {si}/4...")
            try:
                r2 = requests.get(OVERPASS_URL, params={"data": sub_query}, timeout=300)
                r2.raise_for_status()
                sub = r2.json()
                data["elements"].extend(sub.get("elements", []))
                log.info(f"    Sub-tile {si}: {len(sub.get('elements', []))} ways")
                time.sleep(10)
            except Exception as e2:
                log.warning(f"    Sub-tile {si} also failed: {e2} — skipping")

    # Cache raw response
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    with open(cache_path, "w") as f:
        json.dump(data, f)

    n_ways = len(data.get("elements", []))
    log.info(f"  Tile {tile_idx}/{n_tiles}: {n_ways:,} ways")
    return data


def overpass_to_gdf(all_elements):
    """Convert Overpass way elements to a roads GeoDataFrame."""
    rows = []
    seen_ids = set()

    for el in all_elements:
        if el["type"] != "way":
            continue
        way_id = el["id"]
        if way_id in seen_ids:
            continue
        seen_ids.add(way_id)

        geom_coords = el.get("geometry", [])
        if len(geom_coords) < 2:
            continue

        coords = [(pt["lon"], pt["lat"]) for pt in geom_coords]
        highway = el.get("tags", {}).get("highway", "unclassified")

        # Normalize: if highway is somehow a list-like string
        if isinstance(highway, list):
            highway = highway[0]

        if highway not in ROAD_CLASS_SCORE:
            continue

        rows.append({
            "osm_id": way_id,
            "highway_class": highway,
            "name": el.get("tags", {}).get("name", ""),
            "geometry": LineString(coords),
        })

    gdf = gpd.GeoDataFrame(rows, crs="EPSG:4326")
    log.info(f"Roads GeoDataFrame: {len(gdf):,} unique ways")
    return gdf


def compute_road_metrics(kelurahan, roads_gdf):
    """Compute road metrics per kelurahan."""
    log.info("Projecting to UTM 48S...")
    kel_proj = kelurahan.to_crs(UTM_48S)
    roads_proj = roads_gdf.to_crs(UTM_48S)

    # Build spatial index
    log.info("Building spatial index...")
    roads_sindex = roads_proj.sindex

    # For intersection density, extract road nodes with degree >= 3
    log.info("Computing node degrees for intersection density...")
    node_counts = {}
    for _, road in roads_proj.iterrows():
        coords = list(road.geometry.coords)
        for c in coords:
            key = (round(c[0], 1), round(c[1], 1))  # ~0.1m precision
            node_counts[key] = node_counts.get(key, 0) + 1

    # Intersection nodes: degree >= 3 (connected to 3+ road segments)
    intersection_points = [
        {"geometry": __import__("shapely.geometry", fromlist=["Point"]).Point(k[0], k[1])}
        for k, v in node_counts.items() if v >= 3
    ]
    from shapely.geometry import Point as SPoint
    intersection_points = [{"geometry": SPoint(k[0], k[1])} for k, v in node_counts.items() if v >= 3]
    ints_gdf = gpd.GeoDataFrame(intersection_points, crs=UTM_48S)
    log.info(f"Intersection nodes (degree >= 3): {len(ints_gdf):,}")

    if len(ints_gdf) > 0:
        ints_sindex = ints_gdf.sindex
    else:
        ints_sindex = None

    results = []
    n_kel = len(kel_proj)
    log.info(f"Computing metrics for {n_kel:,} kelurahan...")

    for i, (idx, kel_row) in enumerate(kel_proj.iterrows()):
        if (i + 1) % 200 == 0 or i == 0:
            log.info(f"  {i + 1:,}/{n_kel:,}...")

        kel_id = kel_row["kelurahan_id"]
        kel_geom = kel_row.geometry
        area_km2 = kel_geom.area / 1e6

        # Find candidate roads
        candidate_idxs = list(roads_sindex.intersection(kel_geom.bounds))
        if not candidate_idxs:
            results.append(_zero_metrics(kel_id, area_km2))
            continue

        candidates = roads_proj.iloc[candidate_idxs]
        clipped = candidates[candidates.geometry.intersects(kel_geom)].copy()
        if len(clipped) == 0:
            results.append(_zero_metrics(kel_id, area_km2))
            continue

        clipped = clipped.copy()
        clipped["geometry"] = clipped.geometry.intersection(kel_geom)
        clipped = clipped[~clipped.geometry.is_empty].copy()
        if len(clipped) == 0:
            results.append(_zero_metrics(kel_id, area_km2))
            continue

        clipped["seg_length_m"] = clipped.geometry.length
        total_m = clipped["seg_length_m"].sum()
        total_km = total_m / 1000.0

        if total_km == 0:
            results.append(_zero_metrics(kel_id, area_km2))
            continue

        def pct_group(tags):
            mask = clipped["highway_class"].isin(tags)
            return (clipped.loc[mask, "seg_length_m"].sum() / total_m) * 100.0

        clipped["score"] = clipped["highway_class"].map(ROAD_CLASS_SCORE).fillna(1)
        avg_score = float(np.average(clipped["score"], weights=clipped["seg_length_m"]))

        # Intersection count
        n_ints = 0
        if ints_sindex is not None:
            cand = list(ints_sindex.intersection(kel_geom.bounds))
            if cand:
                n_ints = ints_gdf.iloc[cand].geometry.within(kel_geom).sum()

        results.append({
            "kelurahan_id": kel_id,
            "area_km2": round(area_km2, 4),
            "road_length_km": round(total_km, 4),
            "road_density_km_per_km2": round(total_km / area_km2, 4) if area_km2 > 0 else 0.0,
            "pct_primary_secondary": round(pct_group(PRIMARY_SECONDARY), 2),
            "pct_residential_tertiary": round(pct_group(RESIDENTIAL_TERTIARY), 2),
            "pct_footway_pedestrian": round(pct_group(FOOTWAY_PEDESTRIAN), 2),
            "avg_road_class_score": round(avg_score, 4),
            "network_connectivity": round(n_ints / area_km2, 2) if area_km2 > 0 else 0.0,
            "n_road_segments": len(clipped),
            "n_intersections": int(n_ints),
        })

    return pd.DataFrame(results)


def _zero_metrics(kel_id, area_km2):
    return {
        "kelurahan_id": kel_id, "area_km2": round(area_km2, 4),
        "road_length_km": 0.0, "road_density_km_per_km2": 0.0,
        "pct_primary_secondary": 0.0, "pct_residential_tertiary": 0.0,
        "pct_footway_pedestrian": 0.0, "avg_road_class_score": 0.0,
        "network_connectivity": 0.0, "n_road_segments": 0, "n_intersections": 0,
    }


def main():
    print("=" * 70)
    print("Road Network Extractor — Jabodetabek Transit Equity Mapper (MVP-20)")
    print("=" * 70)

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Step 1: Download roads via Overpass (9 tiles)
    print("\n--- Step 1: Download roads via Overpass API (9 tiles) ---")
    tiles = make_tiles(3, 3)
    all_elements = []
    for i, (s, w, n, e) in enumerate(tiles, 1):
        data = query_overpass_roads(s, w, n, e, i, len(tiles))
        all_elements.extend(data.get("elements", []))
        if i < len(tiles):
            time.sleep(5)  # Rate limit

    # Step 2: Convert to GeoDataFrame
    print("\n--- Step 2: Convert to GeoDataFrame ---")
    roads_gdf = overpass_to_gdf(all_elements)

    # Step 3: Load kelurahan
    print("\n--- Step 3: Load kelurahan boundaries ---")
    kel = gpd.read_file(RAW_BOUNDARIES)
    log.info(f"Loaded {len(kel)} kelurahan")

    # Step 4: Compute metrics
    print("\n--- Step 4: Compute road metrics per kelurahan ---")
    metrics = compute_road_metrics(kel, roads_gdf)

    # Step 5: Export
    print("\n--- Step 5: Export ---")
    roads_path = OUT_DIR / "jabodetabek_roads.geojson"
    roads_gdf.to_file(roads_path, driver="GeoJSON")
    roads_mb = roads_path.stat().st_size / (1024 * 1024)
    log.info(f"Roads: {roads_path} ({roads_mb:.1f} MB)")

    metrics_path = OUT_DIR / "road_metrics_by_kelurahan.csv"
    metrics.to_csv(metrics_path, index=False)
    log.info(f"Metrics: {metrics_path}")

    # Summary
    print("\n--- Summary ---")
    print(f"  Road segments: {len(roads_gdf):,}")
    print(f"  Kelurahan processed: {len(metrics):,}")
    print(f"\n  Highway class distribution:")
    for cls, cnt in roads_gdf["highway_class"].value_counts().items():
        print(f"    {cls:<20} {cnt:>7,} ({100*cnt/len(roads_gdf):.1f}%)")

    print(f"\n  Road metrics (non-zero kelurahan):")
    for col in ["road_length_km", "road_density_km_per_km2", "pct_footway_pedestrian",
                "avg_road_class_score", "network_connectivity"]:
        vals = metrics[metrics[col] > 0][col]
        print(f"    {col:<30} mean={vals.mean():.2f}  min={vals.min():.2f}  max={vals.max():.2f}")

    n_zero = (metrics["road_length_km"] == 0).sum()
    if n_zero:
        print(f"\n  {n_zero} kelurahan with zero roads (islands, airports, etc.)")

    print("\n" + "=" * 70)
    print("Done.")
    print("=" * 70)


if __name__ == "__main__":
    main()
