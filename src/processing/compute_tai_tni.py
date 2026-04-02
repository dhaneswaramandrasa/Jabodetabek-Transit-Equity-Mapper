"""
MVP-23 — Compute 5-layer TAI and TNI per kelurahan.

Reads all four processed datasets from data/processed/ and outputs:
  data/processed/scores/kelurahan_scores.geojson

Field names exactly match docs/DATA_MODEL.md schema.

Usage:
    python -m src.processing.compute_tai_tni
    python -m src.processing.compute_tai_tni --skip-r5py   # skip L3, set null
"""

import argparse
import logging
import sys
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

from .gc_model import compute_gc
from .r5py_batch import compute_cbd_travel_times

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

# ── Paths ──────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "processed"

DEMOGRAPHICS_GEOJSON = DATA / "demographics" / "kelurahan_demographics.geojson"
DEMOGRAPHICS_CSV = DATA / "demographics" / "bps_kelurahan_demographics.csv"
ROAD_CSV = DATA / "networks" / "road_metrics_by_kelurahan.csv"
TRANSIT_CSV = DATA / "transit" / "transit_stops_summary.csv"
POI_GEOJSON = DATA / "poi" / "jabodetabek_pois.geojson"
CBD_ZONES_GEOJSON = DATA / "poi" / "cbd_zones.geojson"
OUTPUT_PATH = DATA / "scores" / "kelurahan_scores.geojson"

# GTFS + OSM paths — set to your actual files from MVP-19/20
GTFS_DIR = ROOT / "data" / "raw" / "gtfs"
OSM_PBF = ROOT / "data" / "raw" / "networks" / "jabodetabek.osm.pbf"


# ── Normalization helpers ──────────────────────────────────────────────────────

def _winsorize(s: pd.Series, lo: float = 0.02, hi: float = 0.98) -> pd.Series:
    """Clip to 2nd/98th percentile before min-max normalization."""
    lo_val, hi_val = s.quantile(lo), s.quantile(hi)
    return s.clip(lo_val, hi_val)


def _norm(s: pd.Series) -> pd.Series:
    """Min-max normalize to [0, 1] after winsorization."""
    s = _winsorize(s)
    rng = s.max() - s.min()
    if rng == 0:
        return pd.Series(0.5, index=s.index)
    return (s - s.min()) / rng


def _norm_inv(s: pd.Series) -> pd.Series:
    """Inverted min-max: higher raw value → lower normalized score."""
    return 1.0 - _norm(s)


# ── TNI ────────────────────────────────────────────────────────────────────────

def compute_tni(df: pd.DataFrame) -> pd.Series:
    """
    Transit Need Index (5 equal-weighted indicators).
    Formula: TNI = 0.20 × each of pop_density, poverty_rate,
                   norm_inv(avg_household_expenditure), zero_vehicle_hh_pct,
                   dependency_ratio
    Edge cases: zero-population kelurahan → NaN (excluded from TNI, retained in spatial dataset).
    """
    mask_valid = df["population"] >= 100
    tni = pd.Series(np.nan, index=df.index)

    sub = df[mask_valid].copy()
    if sub.empty:
        return tni

    tni[mask_valid] = (
        0.20 * _norm(sub["pop_density"])
        + 0.20 * _norm(sub["poverty_rate"])
        + 0.20 * _norm_inv(sub["avg_household_expenditure"])
        + 0.20 * _norm(sub["zero_vehicle_hh_pct"])
        + 0.20 * _norm(sub["dependency_ratio"])
    )
    return tni.round(4)


# ── TAI layers ─────────────────────────────────────────────────────────────────

def compute_l1_first_mile(df: pd.DataFrame) -> pd.Series:
    """
    Layer 1 — First-mile quality (weight 0.20 in TAI).
    L1 = 0.35×norm(1/walk_dist) + 0.25×norm(pct_footway) + 0.20×norm(connectivity)
         + 0.20×norm(has_feeder)
    """
    # walk_dist: use min_dist_to_transit_m from transit join; cap at 2000m
    walk_dist = df["min_dist_to_transit_m"].clip(upper=2000)
    inv_walk = 1.0 / (walk_dist + 1)       # +1 to avoid div/0

    has_feeder = df.get("has_feeder_service", pd.Series(0, index=df.index)).fillna(0)

    return (
        0.35 * _norm(inv_walk)
        + 0.25 * _norm(df["pct_footway_pedestrian"])
        + 0.20 * _norm(df["network_connectivity"])
        + 0.20 * _norm(has_feeder)
    ).round(4)


def compute_l2_service_quality(df: pd.DataFrame) -> pd.Series:
    """
    Layer 2 — Transit service quality (weight 0.15 in TAI).
    L2 = 0.35×norm(1/headway) + 0.25×norm(mode_diversity)
         + 0.20×norm(1/fare_tier) + 0.20×norm(has_affordable)
    """
    headway = df["avg_headway_min"].fillna(120)   # no service → 2hr headway
    inv_headway = 1.0 / (headway + 1)

    fare_tier = df["best_mode_fare_tier"].fillna(4)
    inv_fare_tier = 1.0 / fare_tier

    has_affordable = df["has_affordable_mode"].fillna(0).astype(float)
    mode_diversity = df["transit_mode_diversity"].fillna(0)

    return (
        0.35 * _norm(inv_headway)
        + 0.25 * _norm(mode_diversity)
        + 0.20 * _norm(inv_fare_tier)
        + 0.20 * _norm(has_affordable)
    ).round(4)


def compute_l3_cbd_journey(cbd_times: pd.Series, df: pd.DataFrame) -> pd.Series:
    """
    Layer 3 — CBD journey chain (weight 0.35 in TAI).
    L3 = norm(1 / poi_reach_cbd_weighted)
    Null when r5py skipped.
    """
    cbd = cbd_times.reindex(df["kelurahan_id"]).values
    cbd_series = pd.Series(cbd, index=df.index)
    # Areas with no transit get a very high travel time
    cbd_series = cbd_series.fillna(180.0)
    inv_cbd = 1.0 / (cbd_series + 1)
    return _norm(inv_cbd).round(4)


def compute_l4_last_mile(df: pd.DataFrame) -> pd.Series:
    """
    Layer 4 — Last-mile quality (weight 0.15 in TAI).
    Simplified: uses two boolean indicators since egress is already in L3 r5py.
    L4 = 0.50×norm(cbd_station_integration) + 0.50×norm(cbd_mode_transfer)
    Falls back to 0.5 if fields not present.
    """
    cbd_int = df.get("cbd_station_integration", pd.Series(0.5, index=df.index)).fillna(0.5)
    cbd_trans = df.get("cbd_mode_transfer_available", pd.Series(0.5, index=df.index)).fillna(0.5)
    return (0.50 * _norm(cbd_int) + 0.50 * _norm(cbd_trans)).round(4)


def compute_l5_cost_competitiveness(df: pd.DataFrame) -> pd.Series:
    """
    Layer 5 — Cost competitiveness vs. private transport (weight 0.15 in TAI).
    L5 = norm(tcr_combined), where tcr_combined = min(GC_car, GC_moto) / GC_transit.
    Higher TCR = transit is more competitive.
    transit_not_available → L5 = 0.
    """
    tcr = df.get("tcr_combined", pd.Series(np.nan, index=df.index))
    tcr = tcr.fillna(0.0)
    return _norm(tcr).round(4)


def compute_tai(df: pd.DataFrame) -> pd.Series:
    """
    TAI = 0.20×L1 + 0.15×L2 + 0.35×L3 + 0.15×L4 + 0.15×L5
    """
    return (
        0.20 * df["tai_l1_first_mile"]
        + 0.15 * df["tai_l2_service_quality"]
        + 0.35 * df["tai_l3_cbd_journey"]
        + 0.15 * df["tai_l4_last_mile"]
        + 0.15 * df["tai_l5_cost_competitiveness"]
    ).round(4)


def assign_quadrant(tni: pd.Series, tai: pd.Series) -> pd.Series:
    """
    Quadrant classification using median split on TNI and TAI.
    Q1: Low Need, High Access  (TNI < median, TAI >= median)
    Q2: Low Need, High Access  — actually: Low Need, High Access
    Q3: Low Need, Low Access
    Q4: High Need, Low Access  ← Transit Desert

    Standard matrix:
      High TNI + High TAI → Q1 (well-served)
      Low  TNI + High TAI → Q2 (potential overinvestment)
      Low  TNI + Low  TAI → Q3 (low priority)
      High TNI + Low  TAI → Q4 (transit desert)
    """
    tni_med = tni.median()
    tai_med = tai.median()
    high_need = tni >= tni_med
    high_access = tai >= tai_med

    quadrant = pd.Series("Q3", index=tni.index)
    quadrant[high_need & high_access] = "Q1"
    quadrant[~high_need & high_access] = "Q2"
    quadrant[high_need & ~high_access] = "Q4"
    # Q3 already set as default
    return quadrant


# ── Main pipeline ──────────────────────────────────────────────────────────────

def run(skip_r5py: bool = False) -> gpd.GeoDataFrame:
    logger.info("=== MVP-23: TAI/TNI Pipeline ===")

    # 1. Load base geometry + demographics
    logger.info("Loading kelurahan geometry + demographics...")
    gdf = gpd.read_file(DEMOGRAPHICS_GEOJSON).to_crs("EPSG:4326")

    demo_csv = pd.read_csv(DEMOGRAPHICS_CSV)
    gdf = gdf.merge(demo_csv, on="kelurahan_id", how="left", suffixes=("", "_csv"))
    # Prefer CSV values where geometry file may have stale fields
    for col in ["poverty_rate", "avg_household_expenditure", "zero_vehicle_hh_pct",
                "dependency_ratio", "population", "pop_density"]:
        if f"{col}_csv" in gdf.columns:
            gdf[col] = gdf[f"{col}_csv"].combine_first(gdf[col])
            gdf.drop(columns=[f"{col}_csv"], inplace=True)

    # 2. Road metrics
    logger.info("Joining road metrics...")
    road = pd.read_csv(ROAD_CSV)
    # Drop area_km2 from road CSV — already present in gdf from demographics join
    road = road.drop(columns=[c for c in ["area_km2"] if c in road.columns])
    gdf = gdf.merge(road, on="kelurahan_id", how="left")

    # 3. Transit stops summary
    logger.info("Joining transit stops...")
    transit = pd.read_csv(TRANSIT_CSV)
    # Aggregate to kelurahan level (stops CSV is per stop)
    # transit_stops_summary.csv has one row per stop; spatially join to kelurahan
    transit_stops_gdf = gpd.GeoDataFrame(
        transit,
        geometry=gpd.points_from_xy(transit["stop_lon"], transit["stop_lat"]),
        crs="EPSG:4326",
    )
    joined = gpd.sjoin(transit_stops_gdf, gdf[["kelurahan_id", "geometry"]], how="left", predicate="within")
    transit_by_kel = joined.groupby("kelurahan_id").agg(
        n_transit_stops=("stop_id", "count"),
        n_transit_routes=("n_routes", "sum"),
        avg_headway_min=("avg_headway_min", "mean"),
        transit_mode_diversity=("transit_mode_diversity", "max"),
        best_mode_fare_tier=("fare_tier", "min"),
        has_affordable_mode=("fare_tier", lambda x: int((x <= 2).any())),
    ).reset_index()

    # Nearest stop distance per kelurahan centroid
    gdf["centroid"] = gdf.geometry.centroid
    gdf["centroid_lon"] = gdf["centroid"].x
    gdf["centroid_lat"] = gdf["centroid"].y

    from scipy.spatial import cKDTree
    stop_coords = transit_stops_gdf[["stop_lon", "stop_lat"]].values
    kel_coords = gdf[["centroid_lon", "centroid_lat"]].values
    tree = cKDTree(stop_coords)
    dist_deg, _ = tree.query(kel_coords, k=1)
    # Approximate degrees → meters (at Jakarta latitude, ~111km/°)
    gdf["min_dist_to_transit_m"] = dist_deg * 111_000

    gdf = gdf.merge(transit_by_kel, on="kelurahan_id", how="left")
    gdf["n_transit_stops"] = gdf["n_transit_stops"].fillna(0).astype(int)
    gdf["avg_headway_min"] = gdf["avg_headway_min"].fillna(120.0)
    gdf["transit_mode_diversity"] = gdf["transit_mode_diversity"].fillna(0).astype(int)
    gdf["best_mode_fare_tier"] = gdf["best_mode_fare_tier"].fillna(4).astype(int)
    gdf["has_affordable_mode"] = gdf["has_affordable_mode"].fillna(0).astype(int)

    # 4. Generalized cost (Layer 5) — no r5py dependency
    logger.info("Computing generalized cost (Layer 5)...")
    gc_results = gdf.apply(
        lambda row: compute_gc(
            centroid_lat=row["centroid_lat"],
            centroid_lon=row["centroid_lon"],
            transit_time_min=row.get("poi_reach_cbd_min"),
            transit_fare_idr=None,  # will be estimated after L3
            n_transfers=1,
            first_mile_min=row["min_dist_to_transit_m"] / (1.2 * 1000 / 5),  # ~4km/h walk
        ),
        axis=1,
        result_type="expand",
    )
    gdf = pd.concat([gdf.reset_index(drop=True), gc_results.reset_index(drop=True)], axis=1)

    # 5. r5py CBD journey chain (Layer 3)
    if skip_r5py:
        logger.warning("--skip-r5py: L3 set to null (0.5 placeholder). Run without flag for real compute.")
        cbd_times = pd.Series(dtype=float)
    else:
        gtfs_list = sorted(GTFS_DIR.glob("**/*.zip"))
        if not gtfs_list or not OSM_PBF.exists():
            logger.warning(
                f"GTFS files or OSM PBF missing — skipping r5py.\n"
                f"  GTFS dir: {GTFS_DIR} ({len(gtfs_list)} feeds)\n"
                f"  OSM PBF:  {OSM_PBF} (exists={OSM_PBF.exists()})\n"
                "Re-run without --skip-r5py once data is in place."
            )
            cbd_times = pd.Series(dtype=float)
        else:
            cbd_times = compute_cbd_travel_times(
                kelurahan_gdf=gdf,
                cbd_zones_path=CBD_ZONES_GEOJSON,
                gtfs_paths=gtfs_list,
                osm_pbf_path=OSM_PBF,
            )

    # 6. Compute all TAI layers
    logger.info("Computing TAI layers...")
    gdf["tai_l1_first_mile"] = compute_l1_first_mile(gdf)
    gdf["tai_l2_service_quality"] = compute_l2_service_quality(gdf)
    gdf["tai_l3_cbd_journey"] = compute_l3_cbd_journey(cbd_times, gdf)
    gdf["tai_l4_last_mile"] = compute_l4_last_mile(gdf)
    gdf["tai_l5_cost_competitiveness"] = compute_l5_cost_competitiveness(gdf)

    # 7. Composite TNI and TAI
    logger.info("Computing composite TNI and TAI...")
    gdf["tni_score"] = compute_tni(gdf)
    gdf["tai_score"] = compute_tai(gdf)

    # 8. Equity gap and quadrant
    gdf["equity_gap"] = (gdf["tni_score"] - gdf["tai_score"]).round(4)
    gdf["quadrant"] = assign_quadrant(gdf["tni_score"], gdf["tai_score"])

    # 9. Traffic extension fields — null by default (v2 future)
    gdf["avg_traffic_speed_kmh"] = None
    gdf["peak_congestion_index"] = None
    gdf["traffic_adjusted_access"] = None

    # 10. Select and order output columns per DATA_MODEL.md
    output_cols = [
        # Identity
        "kelurahan_id", "kelurahan_name", "kecamatan_name", "kota_kab_name", "area_km2",
        # TNI
        "population", "pop_density", "poverty_rate", "avg_household_expenditure",
        "zero_vehicle_hh_pct", "dependency_ratio", "tni_score",
        # Road network
        "road_length_km", "road_density_km_per_km2", "pct_primary_secondary",
        "pct_residential_tertiary", "pct_footway_pedestrian", "avg_road_class_score",
        "network_connectivity",
        # Access (TAI inputs)
        "n_transit_stops", "n_transit_routes", "avg_headway_min",
        "min_dist_to_transit_m", "transit_mode_diversity",
        "best_mode_fare_tier", "has_affordable_mode",
        # TAI layers
        "tai_l1_first_mile", "tai_l2_service_quality", "tai_l3_cbd_journey",
        "tai_l4_last_mile", "tai_l5_cost_competitiveness",
        # Layer 5 GC
        "gc_transit_idr", "gc_car_idr", "gc_motorcycle_idr",
        "cheapest_private_mode", "tcr_vs_car", "tcr_vs_motorcycle",
        "tcr_combined", "transit_competitive_zone", "distance_to_sudirman_km",
        # Composite + equity
        "tai_score", "equity_gap", "quadrant",
        # Traffic (null)
        "avg_traffic_speed_kmh", "peak_congestion_index", "traffic_adjusted_access",
        # Geometry
        "geometry",
    ]
    # Keep only cols that exist in gdf
    output_cols = [c for c in output_cols if c in gdf.columns or c == "geometry"]
    result = gdf[output_cols].copy()

    # 11. Save
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    result.to_file(OUTPUT_PATH, driver="GeoJSON")
    logger.info(f"Saved {len(result)} kelurahan records → {OUTPUT_PATH}")

    # Quick summary
    if "quadrant" in result.columns:
        q_counts = result["quadrant"].value_counts().to_dict()
        logger.info(f"Quadrant distribution: {q_counts}")
    if "tni_score" in result.columns:
        logger.info(f"TNI — mean={result['tni_score'].mean():.3f}, std={result['tni_score'].std():.3f}")
    if "tai_score" in result.columns:
        logger.info(f"TAI — mean={result['tai_score'].mean():.3f}, std={result['tai_score'].std():.3f}")

    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MVP-23: Compute 5-layer TAI + TNI per kelurahan")
    parser.add_argument(
        "--skip-r5py",
        action="store_true",
        help="Skip r5py routing (Layer 3 placeholder). Use when GTFS/OSM not ready.",
    )
    args = parser.parse_args()
    run(skip_r5py=args.skip_r5py)
