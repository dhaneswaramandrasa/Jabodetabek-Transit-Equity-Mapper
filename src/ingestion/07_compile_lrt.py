#!/usr/bin/env python3
"""
07_compile_lrt.py — Compile LRT Jabodebek station data into GeoJSON.

The LRT Jabodebek does not have an official GTFS feed. This script creates
a GeoJSON file of all 18 stations with manually compiled coordinates.

Coordinates sourced from:
  - OpenStreetMap (primary)
  - Google Maps (cross-reference)
  - Wikipedia station articles (cross-reference)

The LRT Jabodebek opened commercially on 28 August 2023.
Two lines share a common trunk (Dukuh Atas — Cawang):
  - Cibubur Line: Dukuh Atas → Cawang → Harjamukti (12 stations)
  - Bekasi Line:  Dukuh Atas → Cawang → Jati Mulya (14 stations)

Total unique stations: 18 (Dukuh Atas through Cawang shared by both lines)

Output: data/raw/lrt/lrt_jabodebek_stations.geojson

Usage:
  python src/ingestion/07_compile_lrt.py
"""

import json
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "lrt"

# LRT Jabodebek station data
# Coordinates: [longitude, latitude] (GeoJSON convention)
# Sources: OpenStreetMap, Google Maps, Wikipedia
#
# Trunk section (shared by both lines): Dukuh Atas → Cawang (8 stations)
# Cibubur branch: Cawang → Harjamukti (5 additional stations, 4 unique beyond Cawang)
# Bekasi branch: Cawang → Jati Mulya (7 additional stations, 6 unique beyond Cawang)

STATIONS = [
    # === TRUNK SECTION (shared) ===
    {
        "name": "Dukuh Atas",
        "coordinates": [106.8231, -6.2005],
        "lines": ["Cibubur", "Bekasi"],
        "is_interchange": True,
        "interchange_with": ["MRT Jakarta (North-South)", "KRL Commuterline", "TransJakarta", "Airport Rail Link"],
        "notes": "Major multimodal hub — connects LRT, MRT, KRL, BRT, and airport rail",
    },
    {
        "name": "Setiabudi",
        "coordinates": [106.8300, -6.2090],
        "lines": ["Cibubur", "Bekasi"],
        "is_interchange": False,
        "notes": "CBD area station",
    },
    {
        "name": "Rasuna Said",
        "coordinates": [106.8370, -6.2185],
        "lines": ["Cibubur", "Bekasi"],
        "is_interchange": False,
        "notes": "Kuningan CBD area",
    },
    {
        "name": "Kuningan",
        "coordinates": [106.8330, -6.2280],
        "lines": ["Cibubur", "Bekasi"],
        "is_interchange": False,
        "notes": "Near Mega Kuningan",
    },
    {
        "name": "Pancoran",
        "coordinates": [106.8420, -6.2440],
        "lines": ["Cibubur", "Bekasi"],
        "is_interchange": False,
        "notes": "Near Pancoran interchange",
    },
    {
        "name": "Cikoko",
        "coordinates": [106.8520, -6.2520],
        "lines": ["Cibubur", "Bekasi"],
        "is_interchange": False,
        "notes": "Residential area",
    },
    {
        "name": "Ciliwung",
        "coordinates": [106.8590, -6.2570],
        "lines": ["Cibubur", "Bekasi"],
        "is_interchange": False,
        "notes": "Near Ciliwung river",
    },
    {
        "name": "Cawang",
        "coordinates": [106.8680, -6.2620],
        "lines": ["Cibubur", "Bekasi"],
        "is_interchange": True,
        "interchange_with": ["TransJakarta Cawang"],
        "notes": "Branch point — Cibubur and Bekasi lines diverge here",
    },
    # === CIBUBUR BRANCH (4 unique stations beyond Cawang) ===
    {
        "name": "TMII",
        "coordinates": [106.8800, -6.2990],
        "lines": ["Cibubur"],
        "is_interchange": False,
        "notes": "Near Taman Mini Indonesia Indah",
    },
    {
        "name": "Kampung Rambutan",
        "coordinates": [106.8830, -6.3120],
        "lines": ["Cibubur"],
        "is_interchange": True,
        "interchange_with": ["TransJakarta Kampung Rambutan"],
        "notes": "Near Kampung Rambutan bus terminal",
    },
    {
        "name": "Ciracas",
        "coordinates": [106.8780, -6.3280],
        "lines": ["Cibubur"],
        "is_interchange": False,
        "notes": "Ciracas sub-district",
    },
    {
        "name": "Harjamukti",
        "coordinates": [106.8850, -6.3530],
        "lines": ["Cibubur"],
        "is_interchange": False,
        "notes": "Cibubur line terminus — Harjamukti, Depok border area",
    },
    # === BEKASI BRANCH (6 unique stations beyond Cawang) ===
    {
        "name": "Halim",
        "coordinates": [106.8900, -6.2680],
        "lines": ["Bekasi"],
        "is_interchange": False,
        "notes": "Near Halim Perdanakusuma area",
    },
    {
        "name": "Jatibening Baru",
        "coordinates": [106.9170, -6.2730],
        "lines": ["Bekasi"],
        "is_interchange": False,
        "notes": "Jatibening area, Bekasi border",
    },
    {
        "name": "Cikunir 1",
        "coordinates": [106.9440, -6.2690],
        "lines": ["Bekasi"],
        "is_interchange": False,
        "notes": "Cikunir area",
    },
    {
        "name": "Cikunir 2",
        "coordinates": [106.9580, -6.2640],
        "lines": ["Bekasi"],
        "is_interchange": False,
        "notes": "Cikunir area",
    },
    {
        "name": "Bekasi Barat",
        "coordinates": [106.9750, -6.2560],
        "lines": ["Bekasi"],
        "is_interchange": False,
        "notes": "Near Bekasi Barat station area",
    },
    {
        "name": "Jati Mulya",
        "coordinates": [106.9900, -6.2470],
        "lines": ["Bekasi"],
        "is_interchange": False,
        "notes": "Bekasi line terminus — Jati Mulya, Bekasi",
    },
]


def build_geojson() -> dict:
    """Build GeoJSON FeatureCollection from station data."""
    features = []
    for i, station in enumerate(STATIONS):
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": station["coordinates"],
            },
            "properties": {
                "station_id": f"lrt_jbd_{i+1:03d}",
                "name": station["name"],
                "operator": "PT LRT Jabodebek",
                "mode": "LRT",
                "lines": station["lines"],
                "is_interchange": station["is_interchange"],
                "interchange_with": station.get("interchange_with", []),
                "notes": station.get("notes", ""),
                "schedule_available": False,
                "fare_tier": 2,  # LRT Jabodebek is Tier 2 (Rp 5,000-20,000)
            },
        }
        features.append(feature)

    return {
        "type": "FeatureCollection",
        "features": features,
        "metadata": {
            "system": "LRT Jabodebek",
            "operator": "PT LRT Jabodebek (subsidiary of PT KAI)",
            "opened": "2023-08-28",
            "total_stations": len(STATIONS),
            "lines": {
                "Cibubur": "Dukuh Atas - Harjamukti (12 stations)",
                "Bekasi": "Dukuh Atas - Jati Mulya (14 stations)",
            },
            "shared_trunk": "Dukuh Atas - Cawang (8 stations shared by both lines)",
            "unique_stations": 18,
            "coordinate_sources": [
                "OpenStreetMap",
                "Google Maps (cross-reference)",
                "Wikipedia station articles",
            ],
            "coordinate_accuracy": "Approximate (~50m). Verify against OSM/Google Maps.",
            "schedule_data": "Not available as GTFS. LRT included as point proximity only.",
            "fare_range": "Rp 5,000 - Rp 20,000 (distance-based)",
            "generated": datetime.now().isoformat(),
            "generator": "07_compile_lrt.py",
        },
    }


def main():
    print("=" * 60)
    print("LRT Jabodebek Station Compiler — Jabodetabek Transit Equity Mapper")
    print("=" * 60)

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    out_path = RAW_DIR / "lrt_jabodebek_stations.geojson"

    # Build GeoJSON
    geojson = build_geojson()

    # Check if file already exists
    if out_path.exists():
        print(f"\n[EXISTS] {out_path}")
        print("  Overwriting with latest compiled data...")

    # Save
    with open(out_path, "w") as f:
        json.dump(geojson, f, indent=2, ensure_ascii=False)

    size_kb = out_path.stat().st_size / 1024
    print(f"\nOutput: {out_path}")
    print(f"Size: {size_kb:.1f} KB")
    print(f"Total stations: {len(STATIONS)}")

    # Print station summary
    print(f"\n--- Station List ---")
    print(f"{'#':>3}  {'Station':<25} {'Line(s)':<20} {'Lat':>8} {'Lon':>9}  {'Interchange'}")
    print("-" * 90)
    for i, station in enumerate(STATIONS):
        lines = ", ".join(station["lines"])
        lat = station["coordinates"][1]
        lon = station["coordinates"][0]
        interchange = "Yes" if station["is_interchange"] else ""
        print(f"{i+1:>3}  {station['name']:<25} {lines:<20} {lat:>8.4f} {lon:>9.4f}  {interchange}")

    print(f"\n--- IMPORTANT ---")
    print("Coordinates are approximate. Verify against OpenStreetMap before final analysis.")
    print("LRT has NO GTFS schedule data — included as point proximity only in TAI.")
    print("Fare tier: 2 (Rp 5,000-20,000, distance-based)")


if __name__ == "__main__":
    main()
