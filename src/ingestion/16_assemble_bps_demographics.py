#!/usr/bin/env python3
"""
16_assemble_bps_demographics.py — Assemble BPS demographic data for Jabodetabek kelurahan.

Creates SYNTHETIC but realistic demographic data matching DATA_MODEL.md TNI indicators.
BPS data requires manual download from multiple provincial BPS websites — this script
generates realistic synthetic data as a placeholder that can be replaced with real BPS data.

Spatial gradients are modeled using distance from Jakarta CBD:
  - Poverty rate: higher in periphery
  - Household expenditure: higher in center
  - Zero-vehicle HH %: higher in dense urban core, moderate in periphery
  - Dependency ratio: higher in periphery (more families with children)

Output:
  - data/processed/demographics/bps_kelurahan_demographics.csv
  - data/processed/demographics/kelurahan_demographics.geojson (merged with boundaries)

Usage:
  python src/ingestion/16_assemble_bps_demographics.py
"""

from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
BOUNDARIES = PROJECT_ROOT / "data" / "raw" / "boundaries" / "jabodetabek_kelurahan.geojson"
POP_CSV = PROJECT_ROOT / "data" / "processed" / "demographics" / "worldpop_kelurahan_pop.csv"
OUT_DIR = PROJECT_ROOT / "data" / "processed" / "demographics"

CBD_LAT, CBD_LON = -6.200, 106.823


def load_inputs():
    """Load kelurahan boundaries and WorldPop population."""
    kel = gpd.read_file(BOUNDARIES)
    print(f"  [load] {len(kel)} kelurahan boundaries")

    pop = pd.read_csv(POP_CSV)
    print(f"  [load] {len(pop)} kelurahan population records")

    return kel, pop


def compute_spatial_gradient(kel: gpd.GeoDataFrame) -> np.ndarray:
    """Compute normalized distance from each kelurahan centroid to CBD."""
    centroids = kel.geometry.centroid
    dist = np.sqrt(
        (centroids.y - CBD_LAT) ** 2 + (centroids.x - CBD_LON) ** 2
    )
    # Normalize to [0, 1]
    return (dist - dist.min()) / (dist.max() - dist.min())


def generate_demographics(kel: gpd.GeoDataFrame, pop: pd.DataFrame) -> pd.DataFrame:
    """Generate synthetic but realistic BPS demographics.

    Based on published BPS statistics for Jabodetabek (2020-2023):
    - DKI Jakarta poverty rate: ~4-5%
    - Bodetabek poverty rate: ~5-10%
    - DKI avg household expenditure: ~5-8M IDR/month
    - Bodetabek avg household expenditure: ~3-5M IDR/month
    """
    np.random.seed(42)
    n = len(kel)
    dist_norm = compute_spatial_gradient(kel)

    # Poverty rate: 2-15%, higher in periphery
    poverty_base = 0.03 + 0.10 * dist_norm
    poverty_rate = poverty_base + np.random.normal(0, 0.015, n)
    poverty_rate = np.clip(poverty_rate, 0.02, 0.15)

    # Avg household expenditure: 2-8M IDR/month, higher in center
    expenditure_base = 7_000_000 - 4_500_000 * dist_norm
    expenditure = expenditure_base + np.random.normal(0, 800_000, n)
    expenditure = np.clip(expenditure, 2_000_000, 8_000_000).round(-3)

    # Zero-vehicle HH %: U-shaped — high in dense urban core (no parking),
    # moderate in middle suburbs, higher again in poor periphery
    zvh_urban = 0.30 * np.exp(-8 * dist_norm ** 2)  # Urban peak
    zvh_peripheral = 0.15 * dist_norm  # Peripheral rise
    zvh_base = 0.08 + zvh_urban + zvh_peripheral
    zero_vehicle = zvh_base + np.random.normal(0, 0.04, n)
    zero_vehicle = np.clip(zero_vehicle, 0.05, 0.40)

    # Dependency ratio: 0.30-0.70, higher in periphery (more families)
    dep_base = 0.35 + 0.20 * dist_norm
    dependency = dep_base + np.random.normal(0, 0.05, n)
    dependency = np.clip(dependency, 0.30, 0.70)

    df = pd.DataFrame({
        "kelurahan_id": kel["kelurahan_id"],
        "kelurahan_name": kel["kelurahan_name"],
        "kecamatan_name": kel["kecamatan_name"],
        "kota_kab_name": kel["kota_kab_name"],
        "poverty_rate": poverty_rate.round(4),
        "avg_household_expenditure": expenditure.astype(int),
        "zero_vehicle_hh_pct": zero_vehicle.round(4),
        "dependency_ratio": dependency.round(4),
        "data_source": "synthetic_v1",
    })

    # Merge WorldPop population
    df = df.merge(
        pop[["kelurahan_id", "population", "pop_density", "area_km2"]],
        on="kelurahan_id",
        how="left",
    )

    return df


def main():
    print("=" * 70)
    print("BPS Demographics Assembler — Jabodetabek Transit Equity Mapper (MVP-22)")
    print("=" * 70)

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Step 1: Load inputs
    print("\n--- Step 1: Load inputs ---")
    kel, pop = load_inputs()

    # Step 2: Generate demographics
    print("\n--- Step 2: Generate synthetic demographics ---")
    demo = generate_demographics(kel, pop)
    print(f"  Generated {len(demo)} kelurahan records")

    # Step 3: Export CSV
    print("\n--- Step 3: Export ---")
    csv_path = OUT_DIR / "bps_kelurahan_demographics.csv"
    demo.to_csv(csv_path, index=False)
    print(f"  CSV: {csv_path}")

    # Step 4: Merge with boundaries → GeoJSON
    merged = kel.merge(demo.drop(columns=["kelurahan_name", "kecamatan_name",
                                           "kota_kab_name"]),
                       on="kelurahan_id", how="left")
    geo_path = OUT_DIR / "kelurahan_demographics.geojson"
    merged.to_file(geo_path, driver="GeoJSON")
    size_mb = geo_path.stat().st_size / (1024 * 1024)
    print(f"  GeoJSON: {geo_path} ({size_mb:.1f} MB)")

    # Summary
    print("\n--- Summary Statistics ---")
    print(f"  {'Field':<30s} {'Mean':>10s} {'Min':>10s} {'Max':>10s} {'Std':>10s}")
    print("  " + "-" * 72)
    for col in ["population", "pop_density", "poverty_rate",
                "avg_household_expenditure", "zero_vehicle_hh_pct",
                "dependency_ratio"]:
        vals = demo[col].dropna()
        if col in ["population", "avg_household_expenditure", "pop_density"]:
            print(f"  {col:<30s} {vals.mean():>10,.0f} {vals.min():>10,.0f} "
                  f"{vals.max():>10,.0f} {vals.std():>10,.0f}")
        else:
            print(f"  {col:<30s} {vals.mean():>10.4f} {vals.min():>10.4f} "
                  f"{vals.max():>10.4f} {vals.std():>10.4f}")

    print(f"\n  Total population: {demo['population'].sum():,.0f}")
    print(f"  NOTE: Demographics are SYNTHETIC (data_source=synthetic_v1)")
    print(f"  Replace with real BPS data when available.")

    print("\n" + "=" * 70)
    print("Done.")
    print("=" * 70)


if __name__ == "__main__":
    main()
