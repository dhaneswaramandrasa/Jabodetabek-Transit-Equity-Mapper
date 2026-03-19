#!/usr/bin/env python3
"""
06_fetch_worldpop.py — Download WorldPop Indonesia 2020 constrained population raster.

Downloads the constrained (BSGM) population GeoTIFF for Indonesia at ~100m resolution.
This raster is used for:
  1. Dasymetric mapping of BPS kecamatan-level data to kelurahan
  2. Population allocation from kelurahan to H3 hexagons
  3. Zonal statistics for H3 cell population estimates

Output: data/raw/worldpop/idn_ppp_2020_constrained.tif (~98 MB)

Usage:
  python src/ingestion/06_fetch_worldpop.py
"""

import hashlib
import os
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "worldpop"

# WorldPop Indonesia 2020 constrained population
WORLDPOP_URL = "https://data.worldpop.org/GIS/Population/Global_2000_2020_Constrained/2020/BSGM/IDN/idn_ppp_2020_constrained.tif"
OUTPUT_FILE = "idn_ppp_2020_constrained.tif"
EXPECTED_SIZE_MB = 98.33


def sha256_file(path: Path) -> str:
    """Compute SHA-256 hash of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    print("=" * 60)
    print("WorldPop Downloader — Jabodetabek Transit Equity Mapper")
    print("=" * 60)

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    out_path = RAW_DIR / OUTPUT_FILE

    print(f"Source: {WORLDPOP_URL}")
    print(f"Output: {out_path}")
    print(f"Expected size: ~{EXPECTED_SIZE_MB} MB")
    print(f"Resolution: 3 arc-seconds (~100m at equator)")
    print(f"CRS: WGS84 (EPSG:4326)")
    print(f"Units: People per pixel")
    print(f"License: CC BY 4.0")
    print(f"Timestamp: {datetime.now().isoformat()}")

    # Idempotent check
    if out_path.exists():
        size_mb = out_path.stat().st_size / (1024 * 1024)
        print(f"\n[EXISTS] File already downloaded: {out_path}")
        print(f"  Size: {size_mb:.1f} MB")
        checksum = sha256_file(out_path)
        print(f"  SHA-256: {checksum}")
        print("\n  To re-download, delete the file and run again.")
        return

    print(f"\n[DOWNLOAD] Downloading WorldPop Indonesia 2020...")

    try:
        req = urllib.request.Request(
            WORLDPOP_URL,
            headers={"User-Agent": "jabodetabek-transit-equity-mapper/1.0"},
        )

        with urllib.request.urlopen(req, timeout=300) as response:
            total = int(response.headers.get("Content-Length", 0))
            total_mb = total / (1024 * 1024) if total else EXPECTED_SIZE_MB
            print(f"  Server-reported size: {total_mb:.1f} MB")

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

        print("\n--- NEXT STEPS ---")
        print("1. Clip to Jabodetabek bbox using rasterio or GDAL:")
        print(f"   gdal_translate -projwin 106.40 -6.05 107.15 -6.75 "
              f"{out_path} data/raw/worldpop/jabodetabek_pop_2020.tif")
        print("2. Use rasterstats for zonal statistics per kelurahan/H3 cell")

    except Exception as e:
        print(f"\n  ERROR: {e}", file=sys.stderr)
        if out_path.exists():
            out_path.unlink()
        sys.exit(1)


if __name__ == "__main__":
    main()
