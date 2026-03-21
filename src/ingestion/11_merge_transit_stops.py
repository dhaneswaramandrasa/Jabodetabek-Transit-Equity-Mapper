#!/usr/bin/env python3
"""
11_merge_transit_stops.py — Parse GTFS feeds + LRT stations → unified transit_stops.geojson

Pipeline steps (methodology §2.5 steps 1–2):
  1. Parse 3 GTFS ZIPs (TransJakarta, KRL, MRT) via gtfs_kit
  2. Extract unique stops with mode tags
  3. Compute average headway per stop from stop_times (median of consecutive departure diffs)
  4. Append LRT Jabodebek stations (no schedule data → headway = NaN)
  5. Deduplicate by proximity (stops within 50m → keep one, merge mode tags)
  6. Export unified transit_stops.geojson to data/processed/transit/

Output schema per DATA_MODEL.md:
  - stop_id, stop_name, stop_lat, stop_lon
  - mode (BRT/KRL/MRT/LRT)
  - route_ids (list of route_ids serving this stop)
  - avg_headway_min (median headway in minutes, NaN for LRT)
  - schedule_available (bool)

Usage:
  python src/ingestion/11_merge_transit_stops.py
"""

import json
import warnings
from pathlib import Path

import geopandas as gpd
import gtfs_kit as gk
import numpy as np
import pandas as pd
from shapely.geometry import Point

warnings.filterwarnings("ignore", category=FutureWarning)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_GTFS = PROJECT_ROOT / "data" / "raw" / "gtfs"
RAW_LRT = PROJECT_ROOT / "data" / "raw" / "lrt"
OUT_DIR = PROJECT_ROOT / "data" / "processed" / "transit"

# GTFS feeds with their mode tags
GTFS_FEEDS = {
    "transjakarta": {
        "path": RAW_GTFS / "transjakarta" / "transjakarta_gtfs.zip",
        "mode": "BRT",
        "fare_tier": 1,  # Rp 3,500 flat — most affordable
    },
    "krl": {
        "path": RAW_GTFS / "krl" / "krl_gtfs.zip",
        "mode": "KRL",
        "fare_tier": 1,  # Rp 3,000–13,000
    },
    "mrt": {
        "path": RAW_GTFS / "mrt" / "mrt_gtfs.zip",
        "mode": "MRT",
        "fare_tier": 2,  # Rp 3,000–14,000
    },
}

# Default headway estimates for feeds without schedule data (minutes)
# Source: TransJakarta operational reports — corridor routes ~7 min peak,
# feeder/cross-city routes ~15 min. We use 10 min as a conservative median.
DEFAULT_HEADWAY_MIN = {
    "transjakarta": 10.0,
    "lrt_jabodebek": np.nan,  # Explicitly no schedule data per methodology
}

# Jabodetabek bounding box for validation
BBOX = {
    "lat_min": -6.80,
    "lat_max": -6.00,
    "lon_min": 106.40,
    "lon_max": 107.20,
}


def parse_gtfs_feed(name: str, config: dict) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Parse a GTFS feed, return (stops_df, stop_times_df)."""
    path = config["path"]
    if not path.exists():
        raise FileNotFoundError(f"GTFS feed not found: {path}")

    feed = gk.read_feed(str(path), dist_units="km")

    stops = feed.stops[["stop_id", "stop_name", "stop_lat", "stop_lon"]].copy()
    stops["mode"] = config["mode"]
    stops["fare_tier"] = config["fare_tier"]
    stops["source_feed"] = name
    # Check if departure_time data actually exists
    has_times = not feed.stop_times["departure_time"].isna().all()
    stops["schedule_available"] = has_times

    # Get route_ids per stop via stop_times → trips → routes
    st = feed.stop_times[["trip_id", "stop_id", "departure_time"]].copy()
    trips = feed.trips[["trip_id", "route_id"]].copy()
    st = st.merge(trips, on="trip_id", how="left")

    # Route IDs per stop
    route_map = (
        st.groupby("stop_id")["route_id"]
        .apply(lambda x: sorted(x.unique().tolist()))
        .to_dict()
    )
    stops["route_ids"] = stops["stop_id"].map(route_map).fillna("").apply(
        lambda x: x if isinstance(x, list) else []
    )
    stops["n_routes"] = stops["route_ids"].apply(len)

    # Prefix stop_id to avoid collisions across feeds
    stops["stop_id"] = name + "_" + stops["stop_id"].astype(str)

    print(f"  [{name}] {len(stops)} stops, {len(st)} stop_times")
    return stops, st


def compute_headways(stop_times: pd.DataFrame, feed_name: str) -> dict[str, float]:
    """Compute median headway per stop from stop_times departure diffs.

    Headway = median of consecutive departure time differences for trips
    serving the same stop, filtered to weekday service.
    Returns dict: original_stop_id → avg_headway_min.
    """
    st = stop_times.copy()

    # Parse departure_time to seconds since midnight
    def time_to_seconds(t):
        if pd.isna(t):
            return np.nan
        parts = str(t).split(":")
        if len(parts) != 3:
            return np.nan
        h, m, s = int(parts[0]), int(parts[1]), int(parts[2])
        return h * 3600 + m * 60 + s

    st["dep_sec"] = st["departure_time"].apply(time_to_seconds)
    st = st.dropna(subset=["dep_sec"])

    # Sort by stop and departure time, compute diffs
    st = st.sort_values(["stop_id", "dep_sec"])
    st["dep_diff_sec"] = st.groupby("stop_id")["dep_sec"].diff()

    # Filter out unreasonable gaps (> 120 min or < 1 min)
    st = st[(st["dep_diff_sec"] >= 60) & (st["dep_diff_sec"] <= 7200)]

    # Median headway per stop
    headways = (
        st.groupby("stop_id")["dep_diff_sec"]
        .median()
        .div(60)  # convert to minutes
        .to_dict()
    )

    valid = sum(1 for v in headways.values() if not np.isnan(v))
    print(f"  [{feed_name}] Headways computed for {valid}/{len(headways)} stops")
    return headways


def load_lrt_stations() -> pd.DataFrame:
    """Load LRT Jabodebek stations from GeoJSON."""
    path = RAW_LRT / "lrt_jabodebek_stations.geojson"
    if not path.exists():
        raise FileNotFoundError(f"LRT GeoJSON not found: {path}")

    with open(path) as f:
        data = json.load(f)

    rows = []
    for feat in data["features"]:
        props = feat["properties"]
        coords = feat["geometry"]["coordinates"]
        rows.append({
            "stop_id": props["station_id"],
            "stop_name": props["name"],
            "stop_lat": coords[1],
            "stop_lon": coords[0],
            "mode": "LRT",
            "fare_tier": props.get("fare_tier", 2),
            "source_feed": "lrt_jabodebek",
            "schedule_available": False,
            "route_ids": props.get("lines", []),
            "n_routes": len(props.get("lines", [])),
            "avg_headway_min": np.nan,  # No schedule data
        })

    df = pd.DataFrame(rows)
    print(f"  [lrt] {len(df)} stations (no schedule data)")
    return df


def validate_bbox(df: pd.DataFrame) -> pd.DataFrame:
    """Filter stops to Jabodetabek bounding box."""
    mask = (
        (df["stop_lat"] >= BBOX["lat_min"])
        & (df["stop_lat"] <= BBOX["lat_max"])
        & (df["stop_lon"] >= BBOX["lon_min"])
        & (df["stop_lon"] <= BBOX["lon_max"])
    )
    n_outside = (~mask).sum()
    if n_outside > 0:
        print(f"  [bbox] Filtered out {n_outside} stops outside Jabodetabek bbox")
    return df[mask].copy()


def deduplicate_nearby(gdf: gpd.GeoDataFrame, threshold_m: float = 50) -> gpd.GeoDataFrame:
    """Merge stops within threshold_m meters, combining mode tags.

    When stops from different modes are within 50m, keep the first and
    append the other's mode to transit_mode_diversity tracking.
    """
    # Project to UTM zone 48S for meter-based distance
    gdf_proj = gdf.to_crs(epsg=32748)

    # Build spatial index for efficient neighbor lookup
    from shapely.strtree import STRtree

    tree = STRtree(gdf_proj.geometry.values)
    to_drop = set()
    mode_merge = {}  # index → set of modes

    for idx in gdf_proj.index:
        if idx in to_drop:
            continue
        point = gdf_proj.loc[idx, "geometry"]
        buffer = point.buffer(threshold_m)
        candidates = tree.query(buffer)

        for cidx_pos in candidates:
            cidx = gdf_proj.index[cidx_pos]
            if cidx == idx or cidx in to_drop:
                continue
            dist = point.distance(gdf_proj.loc[cidx, "geometry"])
            if dist <= threshold_m:
                # Merge: keep idx, drop cidx, combine modes
                if idx not in mode_merge:
                    mode_merge[idx] = {gdf.loc[idx, "mode"]}
                mode_merge[idx].add(gdf.loc[cidx, "mode"])

                # Also merge route_ids
                existing = gdf.loc[idx, "route_ids"]
                other = gdf.loc[cidx, "route_ids"]
                if isinstance(existing, list) and isinstance(other, list):
                    merged = sorted(set(existing + other))
                    gdf.at[idx, "route_ids"] = merged
                    gdf.at[idx, "n_routes"] = len(merged)

                to_drop.add(cidx)

    # Apply mode merges
    for idx, modes in mode_merge.items():
        gdf.at[idx, "modes_available"] = sorted(modes)

    n_before = len(gdf)
    gdf = gdf.drop(index=to_drop)
    n_after = len(gdf)

    if n_before != n_after:
        print(f"  [dedup] Merged {n_before - n_after} nearby stops (within {threshold_m}m)")
        print(f"  [dedup] {n_before} → {n_after} stops")

    return gdf


def main():
    print("=" * 70)
    print("Transit Stop Merger — Jabodetabek Transit Equity Mapper (MVP-19)")
    print("=" * 70)

    # Step 1: Parse GTFS feeds
    print("\n--- Step 1: Parse GTFS feeds ---")
    all_stops = []
    all_headways = {}

    for name, config in GTFS_FEEDS.items():
        stops, stop_times = parse_gtfs_feed(name, config)
        headways = compute_headways(stop_times, name)
        # Map headways back using original stop_id (before prefix)
        prefixed_headways = {
            f"{name}_{sid}": hw for sid, hw in headways.items()
        }
        all_headways.update(prefixed_headways)
        all_stops.append(stops)

    # Step 2: Load LRT stations
    print("\n--- Step 2: Load LRT stations ---")
    lrt = load_lrt_stations()
    all_stops.append(lrt)

    # Combine all stops
    stops_df = pd.concat(all_stops, ignore_index=True)
    stops_df["avg_headway_min"] = stops_df["stop_id"].map(all_headways)

    # Apply default headways for feeds without schedule data
    for feed_name, default_hw in DEFAULT_HEADWAY_MIN.items():
        mask = (stops_df["source_feed"] == feed_name) & stops_df["avg_headway_min"].isna()
        if mask.any():
            stops_df.loc[mask, "avg_headway_min"] = default_hw
            tag = f"{default_hw:.0f} min default" if not np.isnan(default_hw) else "NaN (no schedule)"
            print(f"  [{feed_name}] Applied {tag} to {mask.sum()} stops without schedule data")

    # LRT already has NaN headway set
    lrt_mask = stops_df["source_feed"] == "lrt_jabodebek"
    stops_df.loc[lrt_mask, "avg_headway_min"] = np.nan

    print(f"\n  Total stops before filtering: {len(stops_df)}")

    # Step 3: Validate bounding box
    print("\n--- Step 3: Validate bounding box ---")
    stops_df = validate_bbox(stops_df)
    print(f"  Stops after bbox filter: {len(stops_df)}")

    # Step 4: Create GeoDataFrame
    print("\n--- Step 4: Create GeoDataFrame ---")
    geometry = [Point(lon, lat) for lon, lat in zip(stops_df["stop_lon"], stops_df["stop_lat"])]
    gdf = gpd.GeoDataFrame(stops_df, geometry=geometry, crs="EPSG:4326")

    # Initialize modes_available from single mode
    gdf["modes_available"] = gdf["mode"].apply(lambda m: [m])

    # Step 5: Deduplicate nearby stops
    print("\n--- Step 5: Deduplicate nearby stops ---")
    gdf = deduplicate_nearby(gdf, threshold_m=50)

    # Step 6: Compute transit_mode_diversity
    gdf["transit_mode_diversity"] = gdf["modes_available"].apply(len)

    # Step 7: Export
    print("\n--- Step 6: Export ---")
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Prepare export columns
    export_cols = [
        "stop_id", "stop_name", "stop_lat", "stop_lon",
        "mode", "modes_available", "fare_tier",
        "route_ids", "n_routes", "avg_headway_min",
        "transit_mode_diversity", "schedule_available",
        "source_feed", "geometry",
    ]
    gdf_out = gdf[export_cols].copy()

    # Convert list/array columns to JSON strings for GeoJSON compatibility
    gdf_out["modes_available"] = gdf_out["modes_available"].apply(
        lambda x: json.dumps(list(x) if hasattr(x, 'tolist') else x)
    )
    gdf_out["route_ids"] = gdf_out["route_ids"].apply(
        lambda x: json.dumps(list(x) if hasattr(x, 'tolist') else x)
    )

    out_path = OUT_DIR / "transit_stops.geojson"
    gdf_out.to_file(out_path, driver="GeoJSON")
    size_kb = out_path.stat().st_size / 1024

    print(f"\n  Output: {out_path}")
    print(f"  Size: {size_kb:.1f} KB")

    # Summary stats
    print("\n--- Summary ---")
    print(f"  Total unique stops: {len(gdf_out)}")
    for mode in ["BRT", "KRL", "MRT", "LRT"]:
        count = (gdf_out["mode"] == mode).sum()
        headway_valid = gdf_out.loc[gdf_out["mode"] == mode, "avg_headway_min"].notna().sum()
        mean_hw = gdf_out.loc[gdf_out["mode"] == mode, "avg_headway_min"].mean()
        hw_str = f"{mean_hw:.1f} min" if not np.isnan(mean_hw) else "N/A (no schedule)"
        print(f"  {mode:>4}: {count:>5} stops | headway data: {headway_valid:>5} | avg headway: {hw_str}")

    multimodal = (gdf_out["transit_mode_diversity"].astype(int) > 1).sum()
    print(f"\n  Multimodal stops (2+ modes within 50m): {multimodal}")

    # Also export a summary CSV for quick inspection
    summary_path = OUT_DIR / "transit_stops_summary.csv"
    gdf_out.drop(columns=["geometry"]).to_csv(summary_path, index=False)
    print(f"  Summary CSV: {summary_path}")

    print("\n" + "=" * 70)
    print("Done. transit_stops.geojson ready for downstream pipeline.")
    print("=" * 70)


if __name__ == "__main__":
    main()
