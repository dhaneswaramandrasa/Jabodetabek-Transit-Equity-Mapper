#!/usr/bin/env python3
"""
04_fetch_boundaries.py — Download administrative boundary data for Indonesia.

Downloads from two sources:
  1. GADM v4.1 GeoPackage — kecamatan level (level 3)
  2. HDX/BPS Shapefile — kelurahan level (level 4)

GADM level 3 = kecamatan (sub-district), NOT kelurahan.
GADM level 4 data is not available in GADM v4.1 for Indonesia.
For kelurahan boundaries, we use the BPS-sourced shapefile from HDX.

Output:
  data/raw/boundaries/gadm41_IDN.gpkg              — GADM (levels 0-3)
  data/raw/boundaries/idn_adm_bps_20200401_SHP.zip — BPS kelurahan (level 4)

Usage:
  python src/ingestion/04_fetch_boundaries.py
"""

import hashlib
import os
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "boundaries"

SOURCES = {
    "gadm_gpkg": {
        "url": "https://geodata.ucdavis.edu/gadm/gadm4.1/gpkg/gadm41_IDN.gpkg",
        "filename": "gadm41_IDN.gpkg",
        "description": "GADM v4.1 — Indonesia levels 0-3 (country/province/kota-kab/kecamatan)",
        "expected_size_mb": 200,  # approximate
    },
    "bps_kelurahan_shp": {
        "url": "https://data.humdata.org/dataset/84a1d98a-790b-4d66-9d14-bbfa48500802/resource/53625e84-203d-4331-b3eb-01e6e8344413/download/idn_adm_bps_20200401_shp.zip",
        "filename": "idn_adm_bps_20200401_SHP.zip",
        "description": "BPS/HDX — Indonesia levels 0-4 (includes kelurahan/desa) SHP",
        "expected_size_mb": 470,
    },
}


def sha256_file(path: Path) -> str:
    """Compute SHA-256 hash of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def download_file(name: str, config: dict) -> bool:
    """Download a single boundary file. Returns True if successful."""
    out_path = RAW_DIR / config["filename"]

    # Idempotent check
    if out_path.exists():
        size_mb = out_path.stat().st_size / (1024 * 1024)
        print(f"\n[EXISTS] {name}: {out_path}")
        print(f"  Size: {size_mb:.1f} MB")
        checksum = sha256_file(out_path)
        print(f"  SHA-256: {checksum}")
        return True

    print(f"\n[DOWNLOAD] {name}: {config['description']}")
    print(f"  URL: {config['url']}")
    print(f"  Expected size: ~{config['expected_size_mb']} MB")
    print(f"  -> {out_path}")

    try:
        req = urllib.request.Request(
            config["url"],
            headers={"User-Agent": "jabodetabek-transit-equity-mapper/1.0"},
        )

        with urllib.request.urlopen(req, timeout=600) as response:
            total = int(response.headers.get("Content-Length", 0))
            total_mb = total / (1024 * 1024) if total else 0

            downloaded = 0
            with open(out_path, "wb") as f:
                while True:
                    chunk = response.read(1024 * 1024)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total:
                        pct = (downloaded / total) * 100
                        dl_mb = downloaded / (1024 * 1024)
                        print(
                            f"\r  Progress: {dl_mb:.1f} / {total_mb:.1f} MB ({pct:.1f}%)",
                            end="",
                            flush=True,
                        )

        print()
        size_mb = out_path.stat().st_size / (1024 * 1024)
        checksum = sha256_file(out_path)
        print(f"  Size: {size_mb:.1f} MB")
        print(f"  SHA-256: {checksum}")
        print(f"  Downloaded: {datetime.now().isoformat()}")
        return True

    except Exception as e:
        print(f"\n  ERROR: {e}", file=sys.stderr)
        if out_path.exists():
            out_path.unlink()
        return False


def main():
    print("=" * 60)
    print("Boundary Downloader — Jabodetabek Transit Equity Mapper")
    print("=" * 60)
    print(f"Output directory: {RAW_DIR}")
    print(f"Timestamp: {datetime.now().isoformat()}")

    RAW_DIR.mkdir(parents=True, exist_ok=True)

    results = {}
    for name, config in SOURCES.items():
        results[name] = download_file(name, config)

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for name, success in results.items():
        status = "OK" if success else "FAILED"
        print(f"  {name:30s} : {status}")

    print("\n--- NOTES ---")
    print("GADM level 3 = kecamatan (NOT kelurahan). Use for kecamatan boundaries.")
    print("BPS/HDX SHP = levels 0-4 including kelurahan/desa. Primary source for kelurahan.")
    print(
        "\nDuring wrangling, verify kelurahan count matches BPS expectation (~1,800 for Jabodetabek)."
    )
    print("Filter to Jabodetabek provinces: DKI Jakarta, Jawa Barat (Bogor/Depok/Bekasi),")
    print("Banten (Tangerang/Tangerang Selatan).")


if __name__ == "__main__":
    main()
