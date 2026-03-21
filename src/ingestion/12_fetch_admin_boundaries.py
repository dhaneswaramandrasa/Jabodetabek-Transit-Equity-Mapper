#!/usr/bin/env python3
"""
12_fetch_admin_boundaries.py — Download and prepare Jabodetabek kelurahan boundaries.

Uses GADM level-4 (kelurahan) boundaries for Indonesia, clipped to Jabodetabek.
Jabodetabek = DKI Jakarta + Kota/Kab Bogor + Kota Depok +
              Kota/Kab Tangerang + Kota Tangerang Selatan + Kota/Kab Bekasi

Output: data/raw/boundaries/jabodetabek_kelurahan.geojson

Usage:
  python src/ingestion/12_fetch_admin_boundaries.py
"""

import json
from pathlib import Path

import geopandas as gpd
import requests

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = PROJECT_ROOT / "data" / "raw" / "boundaries"

# GADM level 4 for Indonesia (kelurahan level)
GADM_URL = "https://geodata.ucdavis.edu/gadm/gadm4.1/json/gadm41_IDN_4.json.zip"

# Jabodetabek administrative units at GADM NAME_1 (province) and NAME_2 (kota/kab) levels
# Note: GADM uses concatenated names without spaces (e.g., "JakartaRaya", "JawaBarat")
JABODETABEK_FILTER = {
    "JakartaRaya": None,  # All kota/kab in DKI Jakarta
    "JawaBarat": [
        "Bogor", "KotaBogor",
        "Depok",
        "Bekasi", "KotaBekasi",
    ],
    "Banten": [
        "KotaTangerang", "Tangerang",
        "TangerangSelatan",
    ],
}


def download_gadm() -> gpd.GeoDataFrame:
    """Download GADM level 4 boundaries for Indonesia."""
    cache_path = OUT_DIR / "gadm41_IDN_4.json.zip"

    if cache_path.exists():
        print(f"  [cache] Using cached GADM file: {cache_path}")
    else:
        print(f"  [download] Downloading GADM level 4 for Indonesia...")
        print(f"  [download] URL: {GADM_URL}")
        print(f"  [download] This may take a few minutes (~50 MB)...")

        r = requests.get(GADM_URL, stream=True, timeout=300)
        r.raise_for_status()

        cache_path.parent.mkdir(parents=True, exist_ok=True)
        with open(cache_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

        size_mb = cache_path.stat().st_size / (1024 * 1024)
        print(f"  [download] Saved: {cache_path} ({size_mb:.1f} MB)")

    print("  [load] Reading GADM GeoJSON...")
    gdf = gpd.read_file(cache_path)
    print(f"  [load] Total Indonesia kelurahan: {len(gdf)}")
    return gdf


def filter_jabodetabek(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Filter to Jabodetabek jurisdictions."""
    masks = []
    for province, cities in JABODETABEK_FILTER.items():
        if cities is None:
            # All cities in province
            mask = gdf["NAME_1"] == province
        else:
            mask = (gdf["NAME_1"] == province) & (gdf["NAME_2"].isin(cities))
        masks.append(mask)

    import functools
    import operator
    combined_mask = functools.reduce(operator.or_, masks)
    result = gdf[combined_mask].copy()

    print(f"\n  Jabodetabek kelurahan: {len(result)}")
    print(f"  Jurisdictions:")
    for province in result["NAME_1"].unique():
        cities = result[result["NAME_1"] == province]["NAME_2"].unique()
        for city in sorted(cities):
            count = ((result["NAME_1"] == province) & (result["NAME_2"] == city)).sum()
            print(f"    {province} / {city}: {count} kelurahan")

    return result


def main():
    print("=" * 70)
    print("Admin Boundary Fetcher — Jabodetabek Transit Equity Mapper")
    print("=" * 70)

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Download GADM
    print("\n--- Step 1: Download GADM level 4 ---")
    gdf = download_gadm()

    # Filter to Jabodetabek
    print("\n--- Step 2: Filter to Jabodetabek ---")
    jbd = filter_jabodetabek(gdf)

    # Standardize column names for downstream use
    jbd = jbd.rename(columns={
        "GID_4": "kelurahan_id",
        "NAME_4": "kelurahan_name",
        "NAME_3": "kecamatan_name",
        "NAME_2": "kota_kab_name",
        "NAME_1": "province_name",
    })

    # Compute area
    jbd_proj = jbd.to_crs(epsg=32748)  # UTM 48S
    jbd["area_km2"] = jbd_proj.geometry.area / 1e6

    # Keep relevant columns
    keep_cols = [
        "kelurahan_id", "kelurahan_name", "kecamatan_name",
        "kota_kab_name", "province_name", "area_km2", "geometry",
    ]
    jbd = jbd[keep_cols].copy()

    # Export
    print("\n--- Step 3: Export ---")
    out_path = OUT_DIR / "jabodetabek_kelurahan.geojson"
    jbd.to_file(out_path, driver="GeoJSON")
    size_mb = out_path.stat().st_size / (1024 * 1024)

    print(f"  Output: {out_path}")
    print(f"  Size: {size_mb:.1f} MB")
    print(f"  Total kelurahan: {len(jbd)}")
    print(f"  Area range: {jbd['area_km2'].min():.2f} – {jbd['area_km2'].max():.2f} km²")
    print(f"  Total area: {jbd['area_km2'].sum():.0f} km²")

    print("\n" + "=" * 70)
    print("Done. Admin boundaries ready for downstream pipeline.")
    print("=" * 70)


if __name__ == "__main__":
    main()
