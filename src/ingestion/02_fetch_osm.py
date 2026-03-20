#!/usr/bin/env python3
"""
02_fetch_osm.py — Download Java OSM PBF extract from Geofabrik.

Downloads the Java island PBF file (~847 MB) which covers all of Jabodetabek.
The PBF will later be clipped to the Jabodetabek bounding box using osmium
during the wrangling step.

Output: data/raw/osm/java-latest.osm.pbf

Usage:
  python src/ingestion/02_fetch_osm.py
"""

import hashlib
import os
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "osm"

# Geofabrik Java extract
GEOFABRIK_URL = "https://download.geofabrik.de/asia/indonesia/java-latest.osm.pbf"
GEOFABRIK_MD5_URL = "https://download.geofabrik.de/asia/indonesia/java-latest.osm.pbf.md5"
OUTPUT_FILE = "java-latest.osm.pbf"

# Jabodetabek bounding box (for reference — used in wrangling step, not here)
JABODETABEK_BBOX = {
    "south": -6.75,
    "west": 106.40,
    "north": -6.05,
    "east": 107.15,
    "description": "Jabodetabek metro area (DKI Jakarta + Bogor, Depok, Tangerang, Bekasi)",
}


def sha256_file(path: Path) -> str:
    """Compute SHA-256 hash of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def download_with_progress(url: str, dest: Path) -> bool:
    """Download a large file with progress reporting."""
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "jabodetabek-transit-equity-mapper/1.0"},
        )
        with urllib.request.urlopen(req, timeout=600) as response:
            total = int(response.headers.get("Content-Length", 0))
            total_mb = total / (1024 * 1024) if total else 0
            print(f"  Expected size: {total_mb:.1f} MB")

            downloaded = 0
            with open(dest, "wb") as f:
                while True:
                    chunk = response.read(1024 * 1024)  # 1 MB chunks
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

        print()  # newline after progress
        return True

    except Exception as e:
        print(f"\n  ERROR: {e}", file=sys.stderr)
        if dest.exists():
            dest.unlink()
        return False


def main():
    print("=" * 60)
    print("OSM PBF Downloader — Jabodetabek Transit Equity Mapper")
    print("=" * 60)

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    out_path = RAW_DIR / OUTPUT_FILE

    print(f"Source: {GEOFABRIK_URL}")
    print(f"Output: {out_path}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"\nJabodetabek bbox (for later clipping):")
    print(f"  S={JABODETABEK_BBOX['south']}, W={JABODETABEK_BBOX['west']}, "
          f"N={JABODETABEK_BBOX['north']}, E={JABODETABEK_BBOX['east']}")

    # Idempotent check
    if out_path.exists():
        size_mb = out_path.stat().st_size / (1024 * 1024)
        print(f"\n[EXISTS] File already downloaded: {out_path}")
        print(f"  Size: {size_mb:.1f} MB")
        checksum = sha256_file(out_path)
        print(f"  SHA-256: {checksum}")
        print("\n  To re-download, delete the file and run again.")
        return

    print(f"\n[DOWNLOAD] Downloading Java PBF (~847 MB)...")
    print("  This may take several minutes depending on connection speed.")

    success = download_with_progress(GEOFABRIK_URL, out_path)

    if success:
        size_mb = out_path.stat().st_size / (1024 * 1024)
        checksum = sha256_file(out_path)
        print(f"\n  Size: {size_mb:.1f} MB")
        print(f"  SHA-256: {checksum}")
        print(f"  Downloaded: {datetime.now().isoformat()}")

        # Download MD5 checksum for verification
        md5_path = RAW_DIR / f"{OUTPUT_FILE}.md5"
        print(f"\n[DOWNLOAD] Fetching MD5 checksum...")
        try:
            req = urllib.request.Request(
                GEOFABRIK_MD5_URL,
                headers={"User-Agent": "jabodetabek-transit-equity-mapper/1.0"},
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                md5_content = resp.read().decode("utf-8").strip()
            with open(md5_path, "w") as f:
                f.write(md5_content)
            print(f"  MD5 checksum saved: {md5_path}")
            print(f"  Content: {md5_content}")
        except Exception as e:
            print(f"  WARNING: Could not fetch MD5: {e}")

        print("\n--- NEXT STEP ---")
        print("Clip to Jabodetabek bbox using osmium:")
        print(f"  osmium extract -b {JABODETABEK_BBOX['west']},{JABODETABEK_BBOX['south']},"
              f"{JABODETABEK_BBOX['east']},{JABODETABEK_BBOX['north']} "
              f"{out_path} -o data/raw/osm/jabodetabek.osm.pbf")
    else:
        print("\n  Download failed. Please retry or download manually from:")
        print(f"  {GEOFABRIK_URL}")
        sys.exit(1)


if __name__ == "__main__":
    main()
