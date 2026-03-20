#!/usr/bin/env python3
"""
01_fetch_gtfs.py — Download GTFS feeds for Jabodetabek transit systems.

Downloads:
  1. TransJakarta BRT + Mikrotrans GTFS (from official TransJakarta endpoint)
  2. KRL Commuterline GTFS (from Mobility Database / community sources)
  3. MRT Jakarta GTFS (from Mobility Database / community sources)

Output: data/raw/gtfs/{transjakarta,krl,mrt}/*.zip

Notes:
  - TransJakarta has a confirmed official GTFS endpoint (gtfs.transjakarta.co.id)
  - KRL and MRT feeds are NOT officially published by operators as of 2026-03.
    The Mobility Database and Transitland only index the TransJakarta feed.
    KRL/MRT feeds must be sourced from community repositories or constructed
    manually from schedule data. This script includes fallback search logic.
  - The TransJakarta feed (236 routes, 8421 stops) may include Mikrotrans feeder
    routes — verify after download by inspecting routes.txt.

Usage:
  python src/ingestion/01_fetch_gtfs.py
"""

import hashlib
import os
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "gtfs"

# Known GTFS feed sources
FEEDS = {
    "transjakarta": {
        "url": "https://gtfs.transjakarta.co.id/files/file_gtfs.zip",
        "description": "TransJakarta BRT + Mikrotrans (official feed)",
        "status": "confirmed",
    },
    "krl": {
        # No official GTFS endpoint from KAI Commuter as of 2026-03.
        # Community sources:
        #   - github.com/soluvas/gtfs-indonesia (placeholder repo, no data)
        #   - github.com/rasyidstat/krl (R package with schedule data, not GTFS)
        #   - TUMI Datahub only has TransJakarta
        #   - Transitland only indexes TransJakarta
        # Fallback: construct GTFS from commuterline.id schedule API or manual compilation.
        "url": None,
        "description": "KRL Commuterline (no official GTFS — manual construction required)",
        "status": "unavailable",
        "fallback_sources": [
            "https://commuterline.id/ (official schedule — scrape with care)",
            "https://github.com/rasyidstat/krl (R package with station/schedule data)",
            "https://github.com/comuline/api (community API for KRL schedule data)",
        ],
    },
    "mrt": {
        # No official GTFS endpoint from MRT Jakarta as of 2026-03.
        # MRT Jakarta has only 13 stations on the North-South line + 6 on East-West Phase 1.
        # Fallback: construct GTFS from jakartamrt.co.id schedule or manual compilation.
        "url": None,
        "description": "MRT Jakarta (no official GTFS — manual construction required)",
        "status": "unavailable",
        "fallback_sources": [
            "https://jakartamrt.co.id/ (official schedule)",
            "https://github.com/reksamamur/mrt-jakarta-api (community MRT API)",
        ],
    },
}


def sha256_file(path: Path) -> str:
    """Compute SHA-256 hash of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def download_feed(name: str, feed: dict) -> bool:
    """Download a single GTFS feed. Returns True if successful."""
    out_dir = RAW_DIR / name
    out_dir.mkdir(parents=True, exist_ok=True)

    if feed["url"] is None:
        print(f"\n[SKIP] {name}: {feed['description']}")
        print(f"  Status: {feed['status']}")
        if "fallback_sources" in feed:
            print("  Fallback sources:")
            for src in feed["fallback_sources"]:
                print(f"    - {src}")
        # Write a README with instructions
        readme_path = out_dir / "README.md"
        with open(readme_path, "w") as f:
            f.write(f"# {name.upper()} GTFS Feed\n\n")
            f.write(f"**Status**: {feed['status']}\n\n")
            f.write(f"{feed['description']}\n\n")
            if "fallback_sources" in feed:
                f.write("## Fallback Sources\n\n")
                for src in feed["fallback_sources"]:
                    f.write(f"- {src}\n")
            f.write("\n## Manual Construction\n\n")
            f.write(
                "This GTFS feed must be manually constructed from schedule data.\n"
            )
            f.write("See src/ingestion/README.md for instructions.\n")
        return False

    filename = f"{name}_gtfs.zip"
    out_path = out_dir / filename

    # Idempotent: skip if already downloaded
    if out_path.exists():
        size_mb = out_path.stat().st_size / (1024 * 1024)
        checksum = sha256_file(out_path)
        print(f"\n[EXISTS] {name}: {out_path}")
        print(f"  Size: {size_mb:.2f} MB")
        print(f"  SHA-256: {checksum}")
        return True

    print(f"\n[DOWNLOAD] {name}: {feed['url']}")
    print(f"  -> {out_path}")

    try:
        req = urllib.request.Request(
            feed["url"],
            headers={"User-Agent": "jabodetabek-transit-equity-mapper/1.0"},
        )
        with urllib.request.urlopen(req, timeout=120) as response:
            data = response.read()

        with open(out_path, "wb") as f:
            f.write(data)

        size_mb = len(data) / (1024 * 1024)
        checksum = sha256_file(out_path)
        print(f"  Size: {size_mb:.2f} MB")
        print(f"  SHA-256: {checksum}")
        print(f"  Downloaded: {datetime.now().isoformat()}")
        return True

    except Exception as e:
        print(f"  ERROR: {e}", file=sys.stderr)
        return False


def main():
    print("=" * 60)
    print("GTFS Feed Downloader — Jabodetabek Transit Equity Mapper")
    print("=" * 60)
    print(f"Output directory: {RAW_DIR}")
    print(f"Timestamp: {datetime.now().isoformat()}")

    results = {}
    for name, feed in FEEDS.items():
        results[name] = download_feed(name, feed)

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for name, success in results.items():
        status = "OK" if success else "MANUAL REQUIRED"
        print(f"  {name:20s} : {status}")

    print("\n--- IMPORTANT ---")
    print(
        "KRL and MRT do NOT have official GTFS feeds. You must construct them"
    )
    print("manually from schedule data. See data/raw/gtfs/{krl,mrt}/README.md")
    print("and the community sources listed above.")
    print(
        "\nThe TransJakarta feed should be inspected to verify it includes"
    )
    print("Mikrotrans feeder routes (check routes.txt for route_type values).")


if __name__ == "__main__":
    main()
