"""
r5py Batching Helper — Layer 3 CBD Journey Chain
Computes gravity-weighted CBD travel time per kelurahan centroid via r5py.

Runs in chunks of 50 centroids with checkpoint saves so compute can resume
if interrupted (budget: 2–4 hours for ~1,800 kelurahan × 9 CBD zones).

Peak window: 7:00–8:00 AM, departure date: 2025-09-16 (Tuesday, regular weekday).
CBD weights: Sudirman–Thamrin × 5, satellite CBDs × 1 each.
"""

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path

import geopandas as gpd
import pandas as pd

logger = logging.getLogger(__name__)

# ── CBD zones and weights ──────────────────────────────────────────────────────
CBD_WEIGHTS = {
    "sudirman_thamrin": 5,
    "kuningan":         1,
    "gatot_subroto":    1,
    "tanah_abang":      1,
    "kemayoran":        1,
    "mangga_dua":       1,
    "pluit":            1,
    "pancoran":         1,
    "kebayoran_baru":   1,
}
TOTAL_WEIGHT = sum(CBD_WEIGHTS.values())

# r5py routing parameters
DEPARTURE_DATE = datetime(2025, 9, 16, 7, 0)   # Tuesday 07:00
DEPARTURE_WINDOW_MIN = 60                        # 07:00–08:00
MAX_EGRESS_WALK_MIN = 20
TRANSFER_PENALTY_S = 600                         # 10 min per transfer
BATCH_SIZE = 50
CHECKPOINT_DIR = Path("data/processed/scores/checkpoints")


def _load_cbd_centroids(cbd_zones_path: Path) -> gpd.GeoDataFrame:
    """Load CBD zone centroids from cbd_zones.geojson."""
    gdf = gpd.read_file(cbd_zones_path)
    gdf = gdf.to_crs("EPSG:4326")
    gdf["centroid"] = gdf.geometry.centroid
    return gdf


def _checkpoint_path(batch_idx: int) -> Path:
    CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)
    return CHECKPOINT_DIR / f"batch_{batch_idx:04d}.csv"


def _load_existing_checkpoints() -> pd.DataFrame:
    """Load all saved checkpoint CSVs into a single DataFrame."""
    files = sorted(CHECKPOINT_DIR.glob("batch_*.csv"))
    if not files:
        return pd.DataFrame()
    return pd.concat([pd.read_csv(f) for f in files], ignore_index=True)


def compute_cbd_travel_times(
    kelurahan_gdf: gpd.GeoDataFrame,
    cbd_zones_path: Path,
    gtfs_paths: list[Path],
    osm_pbf_path: Path,
) -> pd.Series:
    """
    Compute gravity-weighted CBD travel time per kelurahan.

    Returns a pd.Series indexed by kelurahan_id with poi_reach_cbd_weighted values.
    Resumes from checkpoints if interrupted.
    """
    try:
        import r5py
    except ImportError:
        logger.warning(
            "r5py not installed. Install with: pip install r5py\n"
            "Returning null travel times — L3 will be skipped."
        )
        return pd.Series(None, index=kelurahan_gdf["kelurahan_id"])

    cbd_gdf = _load_cbd_centroids(cbd_zones_path)

    # Map CBD zone names to weights
    cbd_gdf["weight"] = cbd_gdf["zone_name"].map(CBD_WEIGHTS).fillna(1)

    # Build origins GeoDataFrame (kelurahan centroids)
    origins = kelurahan_gdf.copy().to_crs("EPSG:4326")
    origins["geometry"] = origins.geometry.centroid
    origins = origins[["kelurahan_id", "geometry"]].rename(columns={"kelurahan_id": "id"})

    # Build r5py transport network
    logger.info("Building r5py transport network (this takes ~2–5 min)...")
    transport_network = r5py.TransportNetwork(
        osm_pbf_path,
        gtfs_paths,
    )

    # Load existing checkpoints
    existing = _load_existing_checkpoints()
    done_ids = set(existing["kelurahan_id"].tolist()) if not existing.empty else set()
    remaining = origins[~origins["id"].isin(done_ids)].copy()
    logger.info(f"Centroids: {len(origins)} total, {len(done_ids)} done, {len(remaining)} remaining")

    results = [existing] if not existing.empty else []

    batches = [remaining.iloc[i:i + BATCH_SIZE] for i in range(0, len(remaining), BATCH_SIZE)]
    for batch_idx, batch in enumerate(batches):
        logger.info(f"Batch {batch_idx + 1}/{len(batches)} — {len(batch)} centroids")

        # Compute travel time matrix from this batch to all CBD centroids
        ttm = r5py.TravelTimeMatrixComputer(
            transport_network,
            origins=batch,
            destinations=cbd_gdf[["zone_name", "centroid"]].rename(
                columns={"zone_name": "id", "centroid": "geometry"}
            ),
            departure=DEPARTURE_DATE,
            departure_time_window=timedelta(minutes=DEPARTURE_WINDOW_MIN),
            transport_modes=[
                r5py.TransportMode.TRANSIT,
                r5py.TransportMode.WALK,
            ],
            max_time=timedelta(minutes=120),
            percentiles=[50],
        ).compute_travel_times()

        # Gravity-weighted average across CBD zones
        ttm = ttm.merge(
            cbd_gdf[["zone_name", "weight"]].rename(columns={"zone_name": "to_id"}),
            on="to_id",
            how="left",
        )
        batch_result = (
            ttm.groupby("from_id")
            .apply(lambda g: (g["travel_time_p50"] * g["weight"]).sum() / g["weight"].sum())
            .reset_index()
            .rename(columns={"from_id": "kelurahan_id", 0: "poi_reach_cbd_weighted"})
        )

        # Save checkpoint
        cp = _checkpoint_path(batch_idx)
        batch_result.to_csv(cp, index=False)
        results.append(batch_result)
        logger.info(f"  Checkpoint saved: {cp}")

    combined = pd.concat(results, ignore_index=True).drop_duplicates("kelurahan_id")
    return combined.set_index("kelurahan_id")["poi_reach_cbd_weighted"]
