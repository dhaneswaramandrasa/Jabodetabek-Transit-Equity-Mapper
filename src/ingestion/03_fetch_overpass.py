#!/usr/bin/env python3
"""
03_fetch_overpass.py — Fetch POIs from Overpass API for Jabodetabek.

Queries the Overpass API for each POI category using strict OSM tag filters
defined in methodology.md section 2.6e.

Categories:
  1. Hospitals (amenity=hospital, filtered for RSUD / RS tipe A/B)
  2. Schools (amenity=school/university, filtered for SMA/SMK/MA/University)
  3. Markets (amenity=marketplace + shop=supermarket, major only)
  4. Industrial zones (landuse=industrial, >10 hectares or named estates)
  5. Government offices (amenity=townhall + office=government)

Note: CBD zones are defined as fixed polygons (see methodology.md 2.6a),
not queried from OSM. Transit stations come from GTFS, not OSM.

Output: data/raw/overpass/{category}.geojson

Usage:
  python src/ingestion/03_fetch_overpass.py
"""

import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "overpass"

# Jabodetabek bounding box (south, west, north, east)
BBOX = "-6.75,106.40,-6.05,107.15"

# Overpass API endpoint
OVERPASS_URL = "https://overpass-api.de/api/interpreter"

# Rate limit: wait between queries (seconds)
RATE_LIMIT_SECONDS = 10

# Overpass QL queries per category (strict filters from methodology.md 2.6e)
QUERIES = {
    "hospitals": {
        "description": "Hospitals — amenity=hospital (filter for RSUD / RS tipe A/B post-download)",
        "query": f"""
[out:json][timeout:120][bbox:{BBOX}];
(
  node["amenity"="hospital"];
  way["amenity"="hospital"];
  relation["amenity"="hospital"];
);
out center body;
""",
    },
    "schools": {
        "description": "Schools — SMA, SMK, Madrasah Aliyah, University/Politeknik only",
        "query": f"""
[out:json][timeout:120][bbox:{BBOX}];
(
  node["amenity"="school"];
  way["amenity"="school"];
  node["amenity"="university"];
  way["amenity"="university"];
  node["amenity"="college"];
  way["amenity"="college"];
);
out center body;
""",
    },
    "markets": {
        "description": "Markets — major pasar tradisional + large supermarkets/hypermarkets",
        "query": f"""
[out:json][timeout:120][bbox:{BBOX}];
(
  node["amenity"="marketplace"];
  way["amenity"="marketplace"];
  node["shop"="supermarket"];
  way["shop"="supermarket"];
  node["shop"="mall"];
  way["shop"="mall"];
);
out center body;
""",
    },
    "industrial": {
        "description": "Industrial zones — landuse=industrial (filter for >10ha or named estates post-download)",
        "query": f"""
[out:json][timeout:120][bbox:{BBOX}];
(
  way["landuse"="industrial"];
  relation["landuse"="industrial"];
);
out center body;
""",
    },
    "government_offices": {
        "description": "Government offices — townhall + office=government",
        "query": f"""
[out:json][timeout:120][bbox:{BBOX}];
(
  node["amenity"="townhall"];
  way["amenity"="townhall"];
  node["office"="government"];
  way["office"="government"];
);
out center body;
""",
    },
}


def overpass_to_geojson(data: dict) -> dict:
    """Convert Overpass API JSON response to GeoJSON FeatureCollection."""
    features = []
    for element in data.get("elements", []):
        # Get coordinates
        if element["type"] == "node":
            coords = [element["lon"], element["lat"]]
            geom_type = "Point"
        elif element["type"] in ("way", "relation") and "center" in element:
            coords = [element["center"]["lon"], element["center"]["lat"]]
            geom_type = "Point"
        else:
            continue

        properties = {
            "osm_id": element["id"],
            "osm_type": element["type"],
        }
        properties.update(element.get("tags", {}))

        features.append(
            {
                "type": "Feature",
                "geometry": {"type": geom_type, "coordinates": coords},
                "properties": properties,
            }
        )

    return {
        "type": "FeatureCollection",
        "features": features,
        "metadata": {
            "source": "Overpass API",
            "bbox": BBOX,
            "timestamp": datetime.now().isoformat(),
            "generator": "03_fetch_overpass.py",
        },
    }


def fetch_category(name: str, config: dict) -> bool:
    """Fetch a single POI category from Overpass API. Returns True if successful."""
    out_path = RAW_DIR / f"{name}.geojson"

    # Idempotent check
    if out_path.exists():
        size_kb = out_path.stat().st_size / 1024
        with open(out_path) as f:
            data = json.load(f)
        n_features = len(data.get("features", []))
        print(f"\n[EXISTS] {name}: {out_path}")
        print(f"  Features: {n_features}")
        print(f"  Size: {size_kb:.1f} KB")
        return True

    print(f"\n[FETCH] {name}: {config['description']}")

    try:
        # URL-encode the query
        encoded = urllib.parse.urlencode({"data": config["query"].strip()})
        req = urllib.request.Request(
            OVERPASS_URL,
            data=encoded.encode("utf-8"),
            headers={
                "User-Agent": "jabodetabek-transit-equity-mapper/1.0",
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )

        print("  Querying Overpass API...")
        with urllib.request.urlopen(req, timeout=180) as response:
            raw_data = json.loads(response.read().decode("utf-8"))

        n_elements = len(raw_data.get("elements", []))
        print(f"  Raw elements returned: {n_elements}")

        # Convert to GeoJSON
        geojson = overpass_to_geojson(raw_data)
        n_features = len(geojson["features"])

        # Save
        with open(out_path, "w") as f:
            json.dump(geojson, f, indent=2, ensure_ascii=False)

        size_kb = out_path.stat().st_size / 1024
        print(f"  GeoJSON features: {n_features}")
        print(f"  Size: {size_kb:.1f} KB")
        print(f"  Saved: {out_path}")
        return True

    except urllib.error.HTTPError as e:
        print(f"  HTTP ERROR {e.code}: {e.reason}", file=sys.stderr)
        if e.code == 429:
            print("  Rate limited — increase RATE_LIMIT_SECONDS and retry")
        return False
    except urllib.error.URLError as e:
        print(f"  URL ERROR: {e.reason}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"  ERROR: {e}", file=sys.stderr)
        return False


def main():
    print("=" * 60)
    print("Overpass POI Fetcher — Jabodetabek Transit Equity Mapper")
    print("=" * 60)
    print(f"Output directory: {RAW_DIR}")
    print(f"Bounding box: {BBOX}")
    print(f"Timestamp: {datetime.now().isoformat()}")

    RAW_DIR.mkdir(parents=True, exist_ok=True)

    results = {}
    for i, (name, config) in enumerate(QUERIES.items()):
        if i > 0:
            print(f"\n  [Waiting {RATE_LIMIT_SECONDS}s for rate limit...]")
            time.sleep(RATE_LIMIT_SECONDS)
        results[name] = fetch_category(name, config)

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for name, success in results.items():
        status = "OK" if success else "FAILED"
        print(f"  {name:25s} : {status}")

    print("\n--- POST-DOWNLOAD FILTERING REQUIRED ---")
    print("After download, apply strict filters from methodology.md 2.6e:")
    print("  hospitals  : Keep only RSUD, RS tipe A/B (verify vs Kemenkes RS Online)")
    print("  schools    : Keep only SMA, SMK, MA, University, Politeknik (filter by name)")
    print("  markets    : Keep only major pasar (>100 vendors) + large supermarkets")
    print("  industrial : Keep only >10ha or named estates (Jababeka, MM2100, etc.)")
    print("  gov offices: Keep Kantor Kelurahan/Kecamatan/Walikota/Bupati")


if __name__ == "__main__":
    main()
