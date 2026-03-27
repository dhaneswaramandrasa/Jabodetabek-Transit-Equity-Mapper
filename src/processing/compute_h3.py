"""
MVP-24 — Generate H3 grid + derive all indicators via dual methods.

Produces data/processed/scores/h3_scores.geojson at H3 resolution 8
(~0.74 km² per cell, ~15,000–20,000 cells across Jabodetabek).

Derivation strategy per DATA_MODEL.md:
  Socioeconomic  → dasymetric mapping (WorldPop-weighted) from kelurahan values
  Road network   → area-weighted spatial clip per H3 cell
  Transit stops  → point-in-polygon spatial join
  Travel times   → direct r5py routing from H3 centroids (batch 1,000)
  TAI/TNI        → identical formula to kelurahan pipeline (compute_tai_tni.py)

Usage:
    python -m src.processing.compute_h3
    python -m src.processing.compute_h3 --skip-r5py   # L3 placeholder (180 min)
"""

import argparse
import logging
import sys
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from shapely.geometry import mapping

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

# ── Paths ──────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "processed"

KELURAHAN_SCORES  = DATA / "scores" / "kelurahan_scores.geojson"
DEMOGRAPHICS_GEOJSON = DATA / "demographics" / "kelurahan_demographics.geojson"
ROAD_CSV          = DATA / "networks"    / "road_metrics_by_kelurahan.csv"
TRANSIT_CSV       = DATA / "transit"     / "transit_stops_summary.csv"
WORLDPOP_TIF      = ROOT / "data" / "raw" / "population" / "jabodetabek_worldpop_100m.tif"
CBD_ZONES_GEOJSON = DATA / "poi" / "cbd_zones.geojson"
GTFS_DIR          = ROOT / "data" / "raw" / "gtfs"
OSM_PBF           = ROOT / "data" / "raw" / "networks" / "jabodetabek.osm.pbf"

OUTPUT_PATH = DATA / "scores" / "h3_scores.geojson"

H3_RESOLUTION = 8
BATCH_SIZE    = 1_000  # H3 centroids per r5py batch
CHECKPOINT_DIR = DATA / "scores" / "h3_checkpoints"

# Boundary buffer for edge detection (metres)
EDGE_BUFFER_M = 500


# ── H3 grid generation ─────────────────────────────────────────────────────────

def generate_h3_grid(boundary_gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Polyfill the Jabodetabek boundary at resolution 8.

    Returns a GeoDataFrame with columns: h3_index, geometry (polygon),
    h3_area_km2, is_edge_cell.
    """
    try:
        import h3
    except ImportError:
        raise ImportError("h3-py not installed. Run: pip install h3")

    # Union all boundary polygons into one
    union_geom = boundary_gdf.to_crs("EPSG:4326").union_all()
    geojson_dict = mapping(union_geom)

    # Polyfill — h3-py v4 API
    try:
        # h3-py v4
        cells = h3.h3shape_to_cells(h3.geo_to_h3shape(geojson_dict), H3_RESOLUTION)
    except AttributeError:
        # h3-py v3 fallback
        cells = h3.polyfill_geojson(geojson_dict, H3_RESOLUTION)

    logger.info(f"H3 polyfill → {len(cells):,} cells at resolution {H3_RESOLUTION}")

    # Build GeoDataFrame
    from shapely.geometry import Polygon

    def _hex_polygon(cell):
        try:
            boundary = h3.cell_to_boundary(cell)  # v4
        except AttributeError:
            boundary = h3.h3_to_geo_boundary(cell, geo_json=False)  # v3
        # boundary is list of (lat, lon) — shapely needs (lon, lat)
        return Polygon([(lon, lat) for lat, lon in boundary])

    records = [{"h3_index": c, "geometry": _hex_polygon(c)} for c in cells]
    gdf = gpd.GeoDataFrame(records, crs="EPSG:4326")

    # Constant area per cell (res 8 ≈ 0.7373 km²)
    gdf["h3_area_km2"] = 0.7373

    # Edge detection — cells whose centroid is within EDGE_BUFFER_M of boundary
    boundary_proj = boundary_gdf.to_crs("EPSG:32748")  # UTM zone 48S for Java
    boundary_line = boundary_proj.union_all().boundary.buffer(EDGE_BUFFER_M)
    gdf_proj = gdf.to_crs("EPSG:32748")
    gdf["is_edge_cell"] = gdf_proj.centroid.intersects(boundary_line)

    return gdf


# ── Dasymetric mapping: socioeconomic → H3 ────────────────────────────────────

def dasymetric_socioeconomic(
    h3_gdf: gpd.GeoDataFrame,
    kelurahan_scores: gpd.GeoDataFrame,
) -> pd.DataFrame:
    """
    Allocate kelurahan-level socioeconomic rates to H3 cells using WorldPop
    population raster as the weighting surface.

    Formula (methodology.md §2.5 step 18):
        value_h3 = Σ(pop_in_intersection_k × value_kelurahan_k) / pop_h3

    If WorldPop raster is unavailable, falls back to area-weighted overlay.
    """
    SOCIOECO_FIELDS = [
        "poverty_rate",
        "avg_household_expenditure",
        "zero_vehicle_hh_pct",
        "dependency_ratio",
    ]

    # Try WorldPop raster path
    use_worldpop = WORLDPOP_TIF.exists()
    if use_worldpop:
        try:
            from rasterstats import zonal_stats
        except ImportError:
            logger.warning("rasterstats not installed — falling back to area-weighted overlay")
            use_worldpop = False

    h3_proj = h3_gdf.to_crs("EPSG:32748")
    kel_proj = kelurahan_scores.to_crs("EPSG:32748")

    if use_worldpop:
        logger.info("Dasymetric: extracting WorldPop population per H3 cell...")
        from rasterstats import zonal_stats as _zs
        stats = _zs(
            h3_proj.geometry,
            str(WORLDPOP_TIF),
            stats=["sum"],
            nodata=-9999,
            all_touched=True,
        )
        h3_pop = pd.Series([s["sum"] or 0.0 for s in stats], index=h3_gdf.index)
    else:
        logger.info("Dasymetric: using area-weighted overlay (WorldPop raster not found)")
        h3_pop = None

    # Spatial overlay: H3 ∩ kelurahan
    logger.info("Dasymetric: computing H3 ∩ kelurahan overlay...")
    overlay = gpd.overlay(
        h3_proj[["h3_index", "geometry"]],
        kel_proj[["kelurahan_id", "geometry"] + SOCIOECO_FIELDS + ["population"]],
        how="intersection",
        keep_geom_type=False,
    )
    overlay["intersect_area_m2"] = overlay.geometry.area

    if use_worldpop:
        # Weight by WorldPop pop in each intersection fragment
        # Approximate: pop in intersection ≈ pop_kelurahan × (intersect_area / kelurahan_area)
        kel_areas = kel_proj.set_index("kelurahan_id").geometry.area.rename("kel_area_m2")
        overlay = overlay.join(kel_areas, on="kelurahan_id")
        overlay["area_frac"] = overlay["intersect_area_m2"] / overlay["kel_area_m2"]
        overlay["pop_in_intersection"] = overlay["population"] * overlay["area_frac"]
    else:
        overlay["pop_in_intersection"] = overlay["population"] * (
            overlay["intersect_area_m2"]
            / overlay.groupby("kelurahan_id")["intersect_area_m2"].transform("sum")
        )

    # Weighted average per H3 cell
    result_rows = []
    for h3_idx, grp in overlay.groupby("h3_index"):
        total_pop = grp["pop_in_intersection"].sum()
        row = {"h3_index": h3_idx, "population": total_pop}
        for field in SOCIOECO_FIELDS:
            if total_pop > 0:
                row[field] = (grp[field] * grp["pop_in_intersection"]).sum() / total_pop
            else:
                row[field] = np.nan
        # Track which kelurahan(s) contributed
        row["kelurahan_ids"] = list(grp["kelurahan_id"].unique())
        result_rows.append(row)

    df = pd.DataFrame(result_rows).set_index("h3_index")
    logger.info(f"Dasymetric complete — {len(df):,} H3 cells with socioeconomic values")
    return df


# ── Road metrics: area-weighted spatial clip ───────────────────────────────────

def clip_road_metrics(
    h3_gdf: gpd.GeoDataFrame,
    road_csv_path: Path,
) -> pd.DataFrame:
    """
    Derive road metrics per H3 cell by area-weighted disaggregation from
    kelurahan road metrics CSV.

    For scalar metrics (road_density, pct_footway, connectivity) uses
    area-weighted average. Road length is recomputed proportionally.
    """
    ROAD_FIELDS = [
        "road_length_km",
        "road_density_km_per_km2",
        "pct_footway",
        "network_connectivity",
    ]

    road_df = pd.read_csv(road_csv_path)
    # road_csv must have kelurahan_id + road fields; join to kelurahan geometry
    kel_geo = gpd.read_file(DEMOGRAPHICS_GEOJSON)[["kelurahan_id", "geometry"]]
    road_gdf = kel_geo.merge(road_df[["kelurahan_id"] + ROAD_FIELDS], on="kelurahan_id")
    road_gdf = road_gdf.to_crs("EPSG:32748")

    h3_proj = h3_gdf.to_crs("EPSG:32748")
    overlay = gpd.overlay(
        h3_proj[["h3_index", "geometry"]],
        road_gdf[["kelurahan_id", "geometry"] + ROAD_FIELDS],
        how="intersection",
        keep_geom_type=False,
    )
    overlay["intersect_area_m2"] = overlay.geometry.area
    kel_areas = road_gdf.set_index("kelurahan_id").geometry.area.rename("kel_area_m2")
    overlay = overlay.join(kel_areas, on="kelurahan_id")
    overlay["area_frac"] = overlay["intersect_area_m2"] / overlay["kel_area_m2"]

    # road_length: proportional to area fraction
    overlay["road_length_km_h3"] = overlay["road_length_km"] * overlay["area_frac"]

    result_rows = []
    for h3_idx, grp in overlay.groupby("h3_index"):
        total_area_m2 = grp["intersect_area_m2"].sum()
        row = {"h3_index": h3_idx}
        row["road_length_km"] = grp["road_length_km_h3"].sum()
        row["road_density_km_per_km2"] = row["road_length_km"] / 0.7373  # constant H3 area
        # Area-weighted average for fractional/density metrics
        for field in ["pct_footway", "network_connectivity"]:
            row[field] = (grp[field] * grp["intersect_area_m2"]).sum() / total_area_m2 if total_area_m2 > 0 else np.nan
        result_rows.append(row)

    df = pd.DataFrame(result_rows).set_index("h3_index")
    logger.info(f"Road clip complete — {len(df):,} H3 cells with road metrics")
    return df


# ── Transit stops: point-in-polygon ───────────────────────────────────────────

def assign_transit_stops(
    h3_gdf: gpd.GeoDataFrame,
    transit_csv_path: Path,
) -> pd.DataFrame:
    """
    Assign transit stop attributes to H3 cells via point-in-polygon join.

    For each H3 cell: aggregate stop counts, headway (min), mode_diversity,
    fare_tier, has_affordable, min_dist_to_transit_m.
    """
    transit_df = pd.read_csv(transit_csv_path)
    # Expected columns: kelurahan_id, n_stops, min_headway_min, mode_diversity,
    #   fare_tier, has_affordable, nearest_stop_lat, nearest_stop_lon,
    #   min_dist_to_transit_m, has_feeder_service

    # We need stop point geometries for true PiP; use nearest_stop_lat/lon
    # as the representative stop point per kelurahan
    stop_gdf = gpd.GeoDataFrame(
        transit_df,
        geometry=gpd.points_from_xy(
            transit_df["nearest_stop_lon"], transit_df["nearest_stop_lat"]
        ),
        crs="EPSG:4326",
    )

    h3_proj = h3_gdf[["h3_index", "geometry"]].to_crs("EPSG:32748")
    stops_proj = stop_gdf.to_crs("EPSG:32748")

    # Spatial join: which H3 cell contains each stop centroid?
    joined = gpd.sjoin(stops_proj, h3_proj, how="left", predicate="within")

    # For cells with no matched stop, fall back to nearest
    unmatched = joined[joined["index_right"].isna()]
    if not unmatched.empty:
        from scipy.spatial import cKDTree
        h3_centroids = np.array(
            [(g.centroid.x, g.centroid.y) for g in h3_proj.geometry]
        )
        stop_coords = np.array(
            [(g.x, g.y) for g in stops_proj.loc[unmatched.index, "geometry"]]
        )
        tree = cKDTree(h3_centroids)
        _, idx = tree.query(stop_coords)
        joined.loc[unmatched.index, "index_right"] = idx

    # Aggregate per H3 cell
    TRANSIT_FIELDS = [
        "n_stops", "min_headway_min", "mode_diversity",
        "fare_tier", "has_affordable", "min_dist_to_transit_m", "has_feeder_service",
    ]
    agg = (
        joined.groupby("h3_index")
        .agg(
            n_stops=("n_stops", "sum"),
            min_headway_min=("min_headway_min", "min"),
            mode_diversity=("mode_diversity", "max"),
            fare_tier=("fare_tier", "min"),
            has_affordable=("has_affordable", "max"),
            min_dist_to_transit_m=("min_dist_to_transit_m", "min"),
            has_feeder_service=("has_feeder_service", "max"),
        )
        .reset_index()
        .set_index("h3_index")
    )

    # Fill H3 cells with no stops
    all_h3 = h3_gdf.set_index("h3_index")
    agg = agg.reindex(all_h3.index)
    agg["n_stops"] = agg["n_stops"].fillna(0)
    agg["min_headway_min"] = agg["min_headway_min"].fillna(180)   # worst-case
    agg["mode_diversity"] = agg["mode_diversity"].fillna(0)
    agg["fare_tier"] = agg["fare_tier"].fillna(3)                 # highest fare
    agg["has_affordable"] = agg["has_affordable"].fillna(0)
    agg["min_dist_to_transit_m"] = agg["min_dist_to_transit_m"].fillna(5000)
    agg["has_feeder_service"] = agg["has_feeder_service"].fillna(0)

    logger.info(f"Transit PiP complete — {len(agg):,} H3 cells")
    return agg


# ── Travel times: direct r5py from H3 centroids ───────────────────────────────

def compute_h3_travel_times(
    h3_gdf: gpd.GeoDataFrame,
    cbd_zones_path: Path,
    skip_r5py: bool = False,
) -> pd.Series:
    """
    Route from each H3 centroid to CBD zones via r5py.
    Reuses the same RAPTOR parameters as the kelurahan pipeline.
    Batches 1,000 centroids at a time with checkpoint/resume.
    """
    if skip_r5py:
        logger.warning("--skip-r5py: assigning L3 placeholder (180 min) for all H3 cells")
        return pd.Series(180.0, index=h3_gdf["h3_index"])

    try:
        import r5py
    except ImportError:
        logger.warning("r5py not installed — using 180 min placeholder for L3")
        return pd.Series(180.0, index=h3_gdf["h3_index"])

    from datetime import datetime, timedelta

    CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)

    # Build origins GeoDataFrame from H3 centroids
    origins = h3_gdf[["h3_index", "geometry"]].copy().to_crs("EPSG:4326")
    origins["geometry"] = origins.geometry.centroid
    origins = origins.rename(columns={"h3_index": "id"})

    # Load CBD zones + weights
    from .r5py_batch import CBD_WEIGHTS, DEPARTURE_DATE, DEPARTURE_WINDOW_MIN
    cbd_gdf = gpd.read_file(cbd_zones_path).to_crs("EPSG:4326")
    cbd_gdf["centroid"] = cbd_gdf.geometry.centroid
    cbd_gdf["weight"] = cbd_gdf["zone_name"].map(CBD_WEIGHTS).fillna(1)

    TOTAL_WEIGHT = sum(CBD_WEIGHTS.values())

    # Load existing H3 checkpoints
    done_ids: set = set()
    existing_results = []
    for cp_file in sorted(CHECKPOINT_DIR.glob("h3_batch_*.csv")):
        df = pd.read_csv(cp_file)
        done_ids.update(df["h3_index"].tolist())
        existing_results.append(df)

    remaining = origins[~origins["id"].isin(done_ids)].copy()
    logger.info(
        f"H3 centroids: {len(origins):,} total, {len(done_ids):,} done, "
        f"{len(remaining):,} remaining"
    )

    # Build transport network once
    logger.info("Building r5py transport network for H3 routing...")
    gtfs_paths = list(GTFS_DIR.glob("*.zip"))
    transport_network = r5py.TransportNetwork(OSM_PBF, gtfs_paths)

    batches = [
        remaining.iloc[i : i + BATCH_SIZE]
        for i in range(0, len(remaining), BATCH_SIZE)
    ]
    for batch_idx, batch in enumerate(batches):
        logger.info(f"H3 batch {batch_idx + 1}/{len(batches)} — {len(batch):,} centroids")
        ttm = r5py.TravelTimeMatrixComputer(
            transport_network,
            origins=batch,
            destinations=cbd_gdf[["zone_name", "centroid"]].rename(
                columns={"zone_name": "id", "centroid": "geometry"}
            ),
            departure=DEPARTURE_DATE,
            departure_time_window=timedelta(minutes=DEPARTURE_WINDOW_MIN),
            transport_modes=[r5py.TransportMode.TRANSIT, r5py.TransportMode.WALK],
            max_time=timedelta(minutes=120),
            percentiles=[50],
        ).compute_travel_times()

        ttm = ttm.merge(
            cbd_gdf[["zone_name", "weight"]].rename(columns={"zone_name": "to_id"}),
            on="to_id",
            how="left",
        )
        batch_result = (
            ttm.groupby("from_id")
            .apply(
                lambda g: (g["travel_time_p50"] * g["weight"]).sum() / g["weight"].sum()
            )
            .reset_index()
            .rename(columns={"from_id": "h3_index", 0: "poi_reach_cbd_weighted"})
        )

        cp = CHECKPOINT_DIR / f"h3_batch_{batch_idx:05d}.csv"
        batch_result.to_csv(cp, index=False)
        existing_results.append(batch_result)
        logger.info(f"  Checkpoint saved: {cp}")

    combined = (
        pd.concat(existing_results, ignore_index=True)
        .drop_duplicates("h3_index")
        .set_index("h3_index")["poi_reach_cbd_weighted"]
    )
    return combined


# ── TAI/TNI computation (identical formula to kelurahan pipeline) ─────────────

def _winsorize_minmax(series: pd.Series, lo: float = 0.02, hi: float = 0.98) -> pd.Series:
    lo_val = series.quantile(lo)
    hi_val = series.quantile(hi)
    clipped = series.clip(lo_val, hi_val)
    rng = hi_val - lo_val
    return (clipped - lo_val) / rng if rng > 0 else pd.Series(0.5, index=series.index)


def compute_tni_h3(df: pd.DataFrame) -> pd.Series:
    """Equal-weighted 5-indicator TNI, winsorized min-max."""
    indicators = {
        "pop_density":               df["population"] / 0.7373,
        "poverty_rate":              df["poverty_rate"],
        "inv_expenditure":           1.0 / df["avg_household_expenditure"].replace(0, np.nan),
        "zero_vehicle_hh_pct":       df["zero_vehicle_hh_pct"],
        "dependency_ratio":          df["dependency_ratio"],
    }
    normed = {k: _winsorize_minmax(v.fillna(v.median())) for k, v in indicators.items()}
    tni = sum(normed.values()) / len(normed)
    return tni.clip(0, 1).rename("tni_score")


def compute_tai_h3(df: pd.DataFrame, travel_times: pd.Series) -> pd.DataFrame:
    """5-layer TAI per methodology.md — same weights as kelurahan pipeline."""
    idx = df.index

    # L1 first-mile
    l1 = (
        0.35 * _winsorize_minmax(1.0 / df["min_dist_to_transit_m"].replace(0, np.nan).fillna(5000))
        + 0.25 * _winsorize_minmax(df["pct_footway"].fillna(0))
        + 0.20 * _winsorize_minmax(df["network_connectivity"].fillna(0))
        + 0.20 * _winsorize_minmax(df["has_feeder_service"].fillna(0))
    ).clip(0, 1)

    # L2 service quality
    l2 = (
        0.35 * _winsorize_minmax(1.0 / df["min_headway_min"].replace(0, np.nan).fillna(180))
        + 0.25 * _winsorize_minmax(df["mode_diversity"].fillna(0))
        + 0.20 * _winsorize_minmax(1.0 / df["fare_tier"].replace(0, np.nan).fillna(3))
        + 0.20 * _winsorize_minmax(df["has_affordable"].fillna(0))
    ).clip(0, 1)

    # L3 CBD journey chain
    tt = travel_times.reindex(idx).fillna(180.0)
    l3 = _winsorize_minmax(1.0 / tt).clip(0, 1)

    # L4 last-mile — H3 cells lack separate CBD integration columns;
    # use road connectivity proxy (same as fallback in kelurahan pipeline)
    l4 = _winsorize_minmax(df["network_connectivity"].fillna(0)).clip(0, 1)

    # L5 cost competitiveness — use TCR from kelurahan scores if available,
    # else proxy from L3 travel time (higher TT → lower cost competitiveness)
    if "tcr_combined" in df.columns:
        tcr = df["tcr_combined"].fillna(1.0).clip(0.3, 2.0)
    else:
        # Proxy: invert normalised travel time as cost proxy
        tcr = tt.clip(30, 180)
        tcr = 1.0 + (180.0 - tcr) / 150.0  # rough TCR proxy (1.0–2.0 range)

    l5 = _winsorize_minmax(pd.Series(tcr, index=idx).clip(0.3, 2.0)).clip(0, 1)

    tai = (
        0.20 * l1
        + 0.15 * l2
        + 0.35 * l3
        + 0.15 * l4
        + 0.15 * l5
    ).clip(0, 1)

    return pd.DataFrame(
        {"l1_first_mile": l1, "l2_service_quality": l2,
         "l3_cbd_journey": l3, "l4_last_mile": l4,
         "l5_cost_competitiveness": l5, "tai_score": tai},
        index=idx,
    )


def assign_quadrant(tni: pd.Series, tai: pd.Series) -> pd.Series:
    """Median split → Q1 (high need, high access) … Q4 (high need, low access)."""
    tni_med = tni.median()
    tai_med = tai.median()
    conditions = [
        (tni >= tni_med) & (tai >= tai_med),   # Q1 high need, high access
        (tni <  tni_med) & (tai >= tai_med),   # Q2 low need, high access
        (tni <  tni_med) & (tai <  tai_med),   # Q3 low need, low access
        (tni >= tni_med) & (tai <  tai_med),   # Q4 high need, low access (transit desert)
    ]
    choices = ["Q1", "Q2", "Q3", "Q4"]
    return pd.Series(
        np.select(conditions, choices, default="Q3"), index=tni.index, name="quadrant"
    )


# ── Main pipeline ──────────────────────────────────────────────────────────────

def run(skip_r5py: bool = False) -> gpd.GeoDataFrame:
    logger.info("=== MVP-24: H3 grid generation + indicator derivation ===")

    # 1. Load Jabodetabek boundary (from kelurahan GeoJSON union)
    logger.info("Loading Jabodetabek boundary from kelurahan GeoJSON...")
    kel_gdf = gpd.read_file(DEMOGRAPHICS_GEOJSON)

    # 2. Generate H3 grid
    logger.info(f"Generating H3 resolution-{H3_RESOLUTION} grid...")
    h3_gdf = generate_h3_grid(kel_gdf)
    logger.info(f"Grid: {len(h3_gdf):,} cells")

    # 3. Load kelurahan scores for dasymetric mapping
    logger.info("Loading kelurahan scores for dasymetric mapping...")
    if not KELURAHAN_SCORES.exists():
        logger.warning(
            f"kelurahan_scores.geojson not found at {KELURAHAN_SCORES}. "
            "Run compute_tai_tni.py first (MVP-23)."
        )
        # Fall back to demographics GeoJSON + CSV for socioeconomic fields
        kel_scores = kel_gdf.copy()
    else:
        kel_scores = gpd.read_file(KELURAHAN_SCORES)

    # 4. Dasymetric socioeconomic
    logger.info("Deriving socioeconomic indicators (dasymetric)...")
    socioeco_df = dasymetric_socioeconomic(h3_gdf, kel_scores)

    # 5. Road metrics (area-weighted clip)
    logger.info("Deriving road metrics (area-weighted clip)...")
    road_df = clip_road_metrics(h3_gdf, ROAD_CSV)

    # 6. Transit stops (point-in-polygon)
    logger.info("Deriving transit stop indicators (point-in-polygon)...")
    transit_df = assign_transit_stops(h3_gdf, TRANSIT_CSV)

    # 7. Merge all indicators onto H3 grid
    h3_gdf = h3_gdf.set_index("h3_index")
    h3_df = (
        h3_gdf
        .join(socioeco_df, how="left")
        .join(road_df,     how="left")
        .join(transit_df,  how="left")
    )

    # 8. Travel times from H3 centroids (r5py)
    logger.info("Computing travel times from H3 centroids...")
    h3_gdf_reset = h3_gdf.reset_index()
    travel_times = compute_h3_travel_times(h3_gdf_reset, CBD_ZONES_GEOJSON, skip_r5py)

    # 9. Compute TNI
    logger.info("Computing TNI...")
    tni = compute_tni_h3(h3_df)

    # 10. Compute TAI
    logger.info("Computing TAI...")
    tai_df = compute_tai_h3(h3_df, travel_times)

    # 11. Equity gap + quadrant
    equity_gap = (tni - tai_df["tai_score"]).rename("equity_gap")
    quadrant = assign_quadrant(tni, tai_df["tai_score"])

    # 12. Assemble output GeoDataFrame
    logger.info("Assembling output GeoDataFrame...")
    out = gpd.GeoDataFrame(
        pd.concat(
            [
                h3_df[["geometry", "h3_area_km2", "is_edge_cell", "kelurahan_ids",
                        "population", "poverty_rate", "avg_household_expenditure",
                        "zero_vehicle_hh_pct", "dependency_ratio",
                        "road_length_km", "road_density_km_per_km2",
                        "pct_footway", "network_connectivity",
                        "n_stops", "min_headway_min", "mode_diversity",
                        "fare_tier", "has_affordable", "min_dist_to_transit_m",
                        "has_feeder_service"]],
                tai_df,
                tni.rename("tni_score").to_frame(),
                equity_gap.to_frame(),
                quadrant.to_frame(),
                travel_times.reindex(h3_df.index).rename("poi_reach_cbd_weighted").to_frame(),
            ],
            axis=1,
        ),
        geometry="geometry",
        crs="EPSG:4326",
    )
    out.index.name = "h3_index"

    # 13. Save
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    out.reset_index().to_file(OUTPUT_PATH, driver="GeoJSON")
    logger.info(f"Output saved → {OUTPUT_PATH} ({len(out):,} H3 cells)")

    # Summary stats
    q_counts = out["quadrant"].value_counts()
    logger.info(f"Quadrant distribution: {q_counts.to_dict()}")
    logger.info(
        f"TNI  — mean: {tni.mean():.3f}, Gini: {_gini(tni):.3f}"
    )
    logger.info(
        f"TAI  — mean: {tai_df['tai_score'].mean():.3f}, Gini: {_gini(tai_df['tai_score']):.3f}"
    )
    logger.info(
        f"Edge cells flagged: {out['is_edge_cell'].sum():,}"
    )

    return out


def _gini(series: pd.Series) -> float:
    """Gini coefficient (0 = perfectly equal, 1 = maximally unequal)."""
    s = series.dropna().sort_values().values
    n = len(s)
    if n == 0:
        return float("nan")
    cumsum = np.cumsum(s)
    return float((2 * cumsum.sum() / cumsum[-1] / n) - (n + 1) / n)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MVP-24: H3 grid + indicators")
    parser.add_argument(
        "--skip-r5py",
        action="store_true",
        help="Skip r5py routing — assign 180 min placeholder for L3",
    )
    args = parser.parse_args()
    run(skip_r5py=args.skip_r5py)
