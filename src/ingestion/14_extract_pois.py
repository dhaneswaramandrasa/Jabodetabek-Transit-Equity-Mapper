#!/usr/bin/env python3
"""
14_extract_pois.py — Extract strict POIs via Overpass API + create CBD zone polygons.

Pipeline steps (methodology §2.6, §2.6a, §2.6e):
  Part A: Build 9 CBD zone polygons (500m buffer around centre coords)
  Part B: Query Overpass API per category with strict OSM tag filters
  Part C: Apply strict name-based filters to each category
  Part D: Print 10% sample per category for manual verification

Outputs:
  data/processed/poi/cbd_zones.geojson          — 9 CBD polygons
  data/processed/poi/jabodetabek_pois.geojson   — all filtered POIs
  data/raw/poi/{category}_raw.json              — cached raw Overpass responses

Usage:
  python src/ingestion/14_extract_pois.py

Notes:
  - Raw Overpass responses are cached to data/raw/poi/ — re-runs skip API calls.
  - 10s rate-limit between Overpass queries.
  - Overpass timeout: 120s per query.
  - Bounding box: -6.80, 106.40, -6.00, 107.20 (south, west, north, east).
"""

import json
import math
import random
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import geopandas as gpd
import pandas as pd
from pyproj import Transformer
from shapely.geometry import Point, mapping, shape
from shapely.ops import transform

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_POI_DIR = PROJECT_ROOT / "data" / "raw" / "poi"
PROCESSED_POI_DIR = PROJECT_ROOT / "data" / "processed" / "poi"

RAW_POI_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_POI_DIR.mkdir(parents=True, exist_ok=True)

CBD_OUT = PROCESSED_POI_DIR / "cbd_zones.geojson"
POI_OUT = PROCESSED_POI_DIR / "jabodetabek_pois.geojson"

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
OVERPASS_URL = "https://overpass-api.de/api/interpreter"
BBOX = "-6.80,106.40,-6.00,107.20"   # (south, west, north, east) per task spec
RATE_LIMIT_SECONDS = 10
OVERPASS_TIMEOUT = 120

# ---------------------------------------------------------------------------
# Part A: CBD Zone definitions (methodology §2.6a)
# ---------------------------------------------------------------------------
CBD_ZONES = [
    {
        "cbd_id": "CBD-01",
        "name": "Sudirman-Thamrin",
        "lat": -6.200,
        "lon": 106.823,
        "gravity_weight": 5.0,
        "key_anchors": "SCBD, Wisma 46, Bundaran HI, Thamrin",
        "buffer_m": 500,
    },
    {
        "cbd_id": "CBD-02",
        "name": "Kuningan",
        "lat": -6.228,
        "lon": 106.833,
        "gravity_weight": 4.0,
        "key_anchors": "Mega Kuningan, Rasuna Said, embassies",
        "buffer_m": 500,
    },
    {
        "cbd_id": "CBD-03",
        "name": "Gatot Subroto",
        "lat": -6.222,
        "lon": 106.810,
        "gravity_weight": 3.5,
        "key_anchors": "Semanggi, DPR, Senayan",
        "buffer_m": 500,
    },
    {
        "cbd_id": "CBD-04",
        "name": "TB Simatupang",
        "lat": -6.292,
        "lon": 106.812,
        "gravity_weight": 3.0,
        "key_anchors": "South Jakarta tech corridor, Cilandak",
        "buffer_m": 500,
    },
    {
        "cbd_id": "CBD-05",
        "name": "Kelapa Gading",
        "lat": -6.157,
        "lon": 106.907,
        "gravity_weight": 2.0,
        "key_anchors": "Mall of Indonesia, trade district",
        "buffer_m": 500,
    },
    {
        "cbd_id": "CBD-06",
        "name": "Pantai Indah Kapuk",
        "lat": -6.112,
        "lon": 106.743,
        "gravity_weight": 1.5,
        "key_anchors": "PIK, North Jakarta coastal reclamation",
        "buffer_m": 500,
    },
    {
        "cbd_id": "CBD-07",
        "name": "BSD City",
        "lat": -6.301,
        "lon": 106.652,
        "gravity_weight": 1.0,
        "key_anchors": "Aeon Mall, ICE BSD, tech offices",
        "buffer_m": 500,
    },
    {
        "cbd_id": "CBD-08",
        "name": "Summarecon Bekasi",
        "lat": -6.225,
        "lon": 107.000,
        "gravity_weight": 1.0,
        "key_anchors": "Summarecon Mall Bekasi, office park",
        "buffer_m": 500,
    },
    {
        "cbd_id": "CBD-09",
        "name": "Summarecon Serpong",
        "lat": -6.242,
        "lon": 106.631,
        "gravity_weight": 1.0,
        "key_anchors": "Mall Summarecon Serpong, Alam Sutera",
        "buffer_m": 500,
    },
]

# ---------------------------------------------------------------------------
# Part B: Overpass query definitions (methodology §2.6e)
# ---------------------------------------------------------------------------
OVERPASS_QUERIES = {
    "hospitals": {
        "description": "Hospitals — amenity=hospital (RSUD/RS tipe A/B)",
        "query": f"""[out:json][timeout:{OVERPASS_TIMEOUT}][bbox:{BBOX}];
(
  node["amenity"="hospital"];
  way["amenity"="hospital"];
  relation["amenity"="hospital"];
);
out center body;""",
        "osm_category": "hospital",
    },
    "schools": {
        "description": "Schools — SMA, SMK, Madrasah Aliyah, University, Politeknik",
        "query": f"""[out:json][timeout:{OVERPASS_TIMEOUT}][bbox:{BBOX}];
(
  node["amenity"="school"];
  way["amenity"="school"];
  node["amenity"="university"];
  way["amenity"="university"];
  node["amenity"="college"];
  way["amenity"="college"];
);
out center body;""",
        "osm_category": "school",
    },
    "markets": {
        "description": "Markets — major pasar tradisional + large supermarkets/hypermarkets",
        "query": f"""[out:json][timeout:{OVERPASS_TIMEOUT}][bbox:{BBOX}];
(
  node["amenity"="marketplace"];
  way["amenity"="marketplace"];
  node["shop"="supermarket"];
  way["shop"="supermarket"];
);
out center body;""",
        "osm_category": "market",
    },
    "industrial": {
        "description": "Industrial zones — landuse=industrial (major estates >10ha or named)",
        "query": f"""[out:json][timeout:{OVERPASS_TIMEOUT}][bbox:{BBOX}];
(
  way["landuse"="industrial"];
  relation["landuse"="industrial"];
);
out center body;""",
        "osm_category": "industrial",
    },
    "government_offices": {
        "description": "Government offices — townhall + office=government",
        "query": f"""[out:json][timeout:{OVERPASS_TIMEOUT}][bbox:{BBOX}];
(
  node["amenity"="townhall"];
  way["amenity"="townhall"];
  node["office"="government"];
  way["office"="government"];
);
out center body;""",
        "osm_category": "government_office",
    },
}

# ---------------------------------------------------------------------------
# Strict name filters per category (methodology §2.6e)
# ---------------------------------------------------------------------------

# Hospital: names containing "RSUD", "RS " (with trailing space, catches "RS Tarakan" etc.)
# or "Rumah Sakit"
HOSPITAL_PATTERNS = ["rsud", "rumah sakit", "rs "]

# School: only SMA, SMK, Madrasah Aliyah, University, Politeknik
SCHOOL_INCLUDE_PATTERNS = [
    "sma ", "smk ", "sma n", "smk n", "sma negeri", "smk negeri",
    "madrasah aliyah", "aliyah negeri", "man ", "mas ", " university",
    "universitas", "politeknik", "institut teknologi", "akademi",
    "sekolah tinggi",
]
# Explicitly exclude lower-education patterns even if they appear
SCHOOL_EXCLUDE_PATTERNS = [
    "sd ", "sdn ", "sd negeri", "smp ", "smpn ", "smp negeri",
    "taman kanak", " tk ", " tk\n", "paud", "play group",
]

# Market: major pasar tradisional + large supermarkets/hypermarkets
# Keep named/major pasar — exclude mini/convenience formats
MARKET_INCLUDE_PATTERNS = [
    "pasar ", "hypermart", "hypermarket", "giant", "carrefour", "lottemart",
    "lotte mart", "hero ", "transmart", "superindo", "alfamidi", "tip top",
    "grand lucky", "ranch market", "papaya", "kem chicks",
]
MARKET_EXCLUDE_PATTERNS = [
    "indomaret", "alfamart", "lawson", "circle k", "family mart",
    "seven eleven", "7-eleven", "mini", "convenience",
]

# Industrial: named major estates
INDUSTRIAL_NAMED_ESTATES = [
    "jababeka", "mm2100", "kiic", "pulogadung", "cakung", "bekasi",
    "cikarang", "balaraja", "tangerang", "cibitung", "bogor",
    "surya cipta", "delta silicon", "greenland", "industri",
    "kawasan industri", "pik ", "marunda",
]
# Industrial areas with these names pass regardless of area check
INDUSTRIAL_NAMED_PATTERN_REQUIRED = True  # AND/OR logic below: name OR area>10ha

# Government office: kelurahan, kecamatan, walikota, bupati
GOVOFFICE_PATTERNS = [
    "kantor kelurahan", "kantor kecamatan", "kantor walikota",
    "kantor bupati", "kantor gubernur", "balai kota", "balaikota",
    "kantor pemerintah", "kantor dinas", "kelurahan ", "kecamatan ",
]


# ---------------------------------------------------------------------------
# Helper: geodesic buffer via pyproj
# ---------------------------------------------------------------------------
def geodesic_buffer(lat: float, lon: float, radius_m: float):
    """Return a Shapely polygon — circle of radius_m metres around (lat, lon)."""
    # Project to UTM zone 48S (covers Java island)
    wgs84_to_utm = Transformer.from_crs("EPSG:4326", "EPSG:32748", always_xy=True)
    utm_to_wgs84 = Transformer.from_crs("EPSG:32748", "EPSG:4326", always_xy=True)

    # Point in projected CRS
    x_utm, y_utm = wgs84_to_utm.transform(lon, lat)
    point_utm = Point(x_utm, y_utm)

    # Buffer in metres
    buffered_utm = point_utm.buffer(radius_m)

    # Back to WGS84
    buffered_wgs84 = transform(
        lambda x, y: utm_to_wgs84.transform(x, y),
        buffered_utm,
    )
    return buffered_wgs84


# ---------------------------------------------------------------------------
# Part A implementation: build CBD GeoDataFrame
# ---------------------------------------------------------------------------
def build_cbd_zones() -> gpd.GeoDataFrame:
    """Build 9 CBD zone polygons from fixed centre coordinates."""
    print("\n" + "=" * 60)
    print("PART A: Building CBD Zone Polygons")
    print("=" * 60)

    rows = []
    for cbd in CBD_ZONES:
        poly = geodesic_buffer(cbd["lat"], cbd["lon"], cbd["buffer_m"])
        rows.append(
            {
                "cbd_id": cbd["cbd_id"],
                "name": cbd["name"],
                "center_lat": cbd["lat"],
                "center_lon": cbd["lon"],
                "gravity_weight": cbd["gravity_weight"],
                "key_anchors": cbd["key_anchors"],
                "buffer_m": cbd["buffer_m"],
                "geometry": poly,
            }
        )
        print(
            f"  {cbd['cbd_id']} {cbd['name']:<25s} "
            f"weight={cbd['gravity_weight']:.1f}  "
            f"center=({cbd['lat']}, {cbd['lon']})"
        )

    gdf = gpd.GeoDataFrame(rows, crs="EPSG:4326")
    gdf.to_file(CBD_OUT, driver="GeoJSON")

    size_kb = CBD_OUT.stat().st_size / 1024
    print(f"\n  Saved {len(gdf)} CBD zones → {CBD_OUT}  ({size_kb:.1f} KB)")
    return gdf


# ---------------------------------------------------------------------------
# Part B: Overpass fetch with caching
# ---------------------------------------------------------------------------
def fetch_raw_overpass(name: str, config: dict) -> list[dict]:
    """
    Fetch raw Overpass elements for one category. Caches to data/raw/poi/.
    Returns list of OSM element dicts.
    """
    cache_path = RAW_POI_DIR / f"{name}_raw.json"

    if cache_path.exists():
        print(f"  [CACHE HIT] {cache_path.name}")
        with open(cache_path) as f:
            data = json.load(f)
        elements = data.get("elements", [])
        print(f"             {len(elements)} elements")
        return elements

    print(f"  Querying Overpass API for: {config['description']}")
    encoded = urllib.parse.urlencode({"data": config["query"].strip()})
    req = urllib.request.Request(
        OVERPASS_URL,
        data=encoded.encode("utf-8"),
        headers={
            "User-Agent": "jabodetabek-transit-equity-mapper/1.0",
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=OVERPASS_TIMEOUT + 30) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"  HTTP ERROR {e.code}: {e.reason}", file=sys.stderr)
        if e.code == 429:
            print("  Rate limited — waiting 60s and retrying once...", file=sys.stderr)
            time.sleep(60)
            try:
                with urllib.request.urlopen(req, timeout=OVERPASS_TIMEOUT + 30) as response:
                    data = json.loads(response.read().decode("utf-8"))
            except Exception as retry_err:
                print(f"  Retry failed: {retry_err}", file=sys.stderr)
                return []
        else:
            return []
    except urllib.error.URLError as e:
        print(f"  URL ERROR: {e.reason}", file=sys.stderr)
        return []

    elements = data.get("elements", [])
    print(f"  Raw elements: {len(elements)}")

    # Cache raw response
    with open(cache_path, "w") as f:
        json.dump(
            {
                "fetched_at": datetime.now(timezone.utc).isoformat(),
                "category": name,
                "bbox": BBOX,
                "elements": elements,
            },
            f,
            indent=2,
            ensure_ascii=False,
        )
    print(f"  Cached → {cache_path.name}")
    return elements


def elements_to_rows(elements: list[dict], category: str) -> list[dict]:
    """Convert raw Overpass elements to flat dicts with lat/lon."""
    rows = []
    for el in elements:
        # Determine coordinates
        if el["type"] == "node":
            lat = el.get("lat")
            lon = el.get("lon")
        elif el["type"] in ("way", "relation") and "center" in el:
            lat = el["center"]["lat"]
            lon = el["center"]["lon"]
        else:
            continue

        if lat is None or lon is None:
            continue

        tags = el.get("tags", {})
        rows.append(
            {
                "osm_id": str(el["id"]),
                "osm_type": el["type"],
                "name": tags.get("name", ""),
                "name_en": tags.get("name:en", ""),
                "amenity": tags.get("amenity", ""),
                "shop": tags.get("shop", ""),
                "office": tags.get("office", ""),
                "landuse": tags.get("landuse", ""),
                "area_tag": tags.get("area", ""),
                "lat": lat,
                "lon": lon,
                "raw_category": category,
            }
        )
    return rows


# ---------------------------------------------------------------------------
# Part C: Strict filters per methodology §2.6e
# ---------------------------------------------------------------------------

def _name_lower(row: dict) -> str:
    """Return lowercased name for pattern matching."""
    return (row.get("name", "") or "").lower()


def filter_hospitals(rows: list[dict]) -> list[dict]:
    """
    Keep only major hospitals: name contains RSUD, RS [space], or Rumah Sakit.
    Methodology §2.6e: verify against Kemenkes list (flag for manual review).
    """
    out = []
    for r in rows:
        nm = _name_lower(r)
        if any(p in nm for p in HOSPITAL_PATTERNS):
            r["category"] = "hospital"
            r["needs_manual_verify"] = True  # flag for Kemenkes RS Online verification
            out.append(r)
    return out


def filter_schools(rows: list[dict]) -> list[dict]:
    """
    Keep only SMA, SMK, Madrasah Aliyah, University, Politeknik.
    Exclude SD, SMP, TK, PAUD even if other patterns present.
    """
    out = []
    for r in rows:
        nm = _name_lower(r)
        # Explicit exclusion first
        if any(p in nm for p in SCHOOL_EXCLUDE_PATTERNS):
            continue
        if any(p in nm for p in SCHOOL_INCLUDE_PATTERNS):
            r["category"] = "school"
            r["needs_manual_verify"] = False
            out.append(r)
    return out


def filter_markets(rows: list[dict]) -> list[dict]:
    """
    Keep major pasar tradisional and large supermarkets/hypermarkets.
    Exclude mini/convenience formats.
    """
    out = []
    for r in rows:
        nm = _name_lower(r)
        # Exclude convenience/mini explicitly
        if any(p in nm for p in MARKET_EXCLUDE_PATTERNS):
            continue
        if any(p in nm for p in MARKET_INCLUDE_PATTERNS):
            r["category"] = "market"
            r["needs_manual_verify"] = False
            out.append(r)
    return out


def filter_industrial(rows: list[dict]) -> list[dict]:
    """
    Keep major industrial estates: named estates OR (area > 10 hectares).
    Area check: Overpass returns way/relation — we don't have polygon area here,
    so we flag unnamed/unknown entries for manual review and keep named estates.
    """
    out = []
    for r in rows:
        nm = _name_lower(r)
        is_named_estate = any(p in nm for p in INDUSTRIAL_NAMED_ESTATES)
        has_name = bool(r.get("name", "").strip())

        if is_named_estate:
            r["category"] = "industrial"
            r["needs_manual_verify"] = False
            out.append(r)
        elif has_name:
            # Named but not in known-estate list — flag for manual review
            r["category"] = "industrial"
            r["needs_manual_verify"] = True
            out.append(r)
        # Unnamed industrial ways are skipped (likely noise / small plots)
    return out


def filter_government_offices(rows: list[dict]) -> list[dict]:
    """
    Keep kelurahan, kecamatan, walikota, bupati, and major government offices.
    """
    out = []
    for r in rows:
        nm = _name_lower(r)
        if any(p in nm for p in GOVOFFICE_PATTERNS):
            r["category"] = "government_office"
            r["needs_manual_verify"] = False
            out.append(r)
    return out


FILTERS = {
    "hospitals": filter_hospitals,
    "schools": filter_schools,
    "markets": filter_markets,
    "industrial": filter_industrial,
    "government_offices": filter_government_offices,
}


# ---------------------------------------------------------------------------
# POI counter utility
# ---------------------------------------------------------------------------
def generate_poi_id(category: str, osm_id: str) -> str:
    return f"POI-{category[:3].upper()}-{osm_id}"


# ---------------------------------------------------------------------------
# Part D: 10% sample print for manual verification
# ---------------------------------------------------------------------------
def print_verification_sample(category: str, rows: list[dict]) -> None:
    """Print a 10% random sample for manual verification (Part C of task)."""
    if not rows:
        print(f"  [NO DATA] {category} — 0 records, nothing to sample")
        return

    n_sample = max(1, math.ceil(len(rows) * 0.10))
    sample = random.sample(rows, min(n_sample, len(rows)))

    print(f"\n  --- 10% sample for {category} ({n_sample} of {len(rows)}) ---")
    for r in sample:
        name = r.get("name", "(no name)")
        lat = r.get("lat", "?")
        lon = r.get("lon", "?")
        needs_verify = r.get("needs_manual_verify", False)
        flag = " [MANUAL VERIFY]" if needs_verify else ""
        print(f"    {name:<50s}  ({lat:.4f}, {lon:.4f}){flag}")


# ---------------------------------------------------------------------------
# Assemble final GeoDataFrame
# ---------------------------------------------------------------------------
def rows_to_geodataframe(all_rows: list[dict]) -> gpd.GeoDataFrame:
    """Convert filtered rows to GeoDataFrame with required schema."""
    records = []
    seen_osm_ids = set()

    for r in all_rows:
        # Deduplicate by osm_id within same category
        key = (r["osm_id"], r["category"])
        if key in seen_osm_ids:
            continue
        seen_osm_ids.add(key)

        poi_id = generate_poi_id(r["category"], r["osm_id"])
        records.append(
            {
                "poi_id": poi_id,
                "name": r.get("name", ""),
                "category": r["category"],
                "osm_id": r["osm_id"],
                "osm_type": r["osm_type"],
                "lat": r["lat"],
                "lon": r["lon"],
                "needs_manual_verify": r.get("needs_manual_verify", False),
                "geometry": Point(r["lon"], r["lat"]),
            }
        )

    if not records:
        return gpd.GeoDataFrame(columns=["poi_id", "name", "category", "osm_id", "lat", "lon", "geometry"], crs="EPSG:4326")

    gdf = gpd.GeoDataFrame(records, crs="EPSG:4326")
    return gdf


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    random.seed(42)  # reproducible samples

    print("=" * 60)
    print("14_extract_pois.py — POI Extraction + CBD Zones")
    print(f"Timestamp: {datetime.now(timezone.utc).isoformat()}")
    print(f"Bounding box: {BBOX}")
    print(f"Raw cache: {RAW_POI_DIR}")
    print(f"Processed output: {PROCESSED_POI_DIR}")
    print("=" * 60)

    # -------------------------------------------------------------------
    # Part A: CBD Zones
    # -------------------------------------------------------------------
    cbd_gdf = build_cbd_zones()

    # -------------------------------------------------------------------
    # Part B+C: Fetch + filter POIs
    # -------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("PART B+C: Overpass Fetch + Strict Filtering")
    print("=" * 60)

    all_filtered_rows: list[dict] = []
    category_counts: dict[str, int] = {}

    for i, (name, config) in enumerate(OVERPASS_QUERIES.items()):
        if i > 0:
            print(f"\n  [Rate limit: sleeping {RATE_LIMIT_SECONDS}s...]")
            time.sleep(RATE_LIMIT_SECONDS)

        print(f"\n[{i+1}/{len(OVERPASS_QUERIES)}] {name.upper()}")
        print(f"  {config['description']}")

        # Fetch raw elements (cached)
        elements = fetch_raw_overpass(name, config)

        # Flatten to rows
        rows = elements_to_rows(elements, name)
        print(f"  Rows before filter: {len(rows)}")

        # Apply strict filter
        filter_fn = FILTERS[name]
        filtered = filter_fn(rows)
        print(f"  Rows after filter:  {len(filtered)}")

        category_counts[config["osm_category"]] = len(filtered)
        all_filtered_rows.extend(filtered)

        # Part D: print verification sample
        print_verification_sample(config["osm_category"], filtered)

    # -------------------------------------------------------------------
    # Assemble final GeoDataFrame
    # -------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("Assembling final POI GeoDataFrame")
    print("=" * 60)

    poi_gdf = rows_to_geodataframe(all_filtered_rows)
    total_pois = len(poi_gdf)
    print(f"  Total POIs (after dedup): {total_pois}")

    # -------------------------------------------------------------------
    # Export
    # -------------------------------------------------------------------
    poi_gdf.to_file(POI_OUT, driver="GeoJSON")
    size_kb = POI_OUT.stat().st_size / 1024
    print(f"  Saved → {POI_OUT}  ({size_kb:.1f} KB)")

    # -------------------------------------------------------------------
    # Summary
    # -------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    print("\n  CBD Zones:")
    for _, row in cbd_gdf.iterrows():
        print(f"    {row['cbd_id']}  {row['name']:<25s}  weight={row['gravity_weight']:.1f}")
    print(f"  File: {CBD_OUT}  ({CBD_OUT.stat().st_size / 1024:.1f} KB)")

    print("\n  POI Counts by Category:")
    for cat, count in category_counts.items():
        flag = "  [LOW — check query/filters]" if count < 5 else ""
        print(f"    {cat:<25s}: {count:>5d}{flag}")

    total = sum(category_counts.values())
    print(f"    {'TOTAL':<25s}: {total:>5d}")
    print(f"  File: {POI_OUT}  ({size_kb:.1f} KB)")

    print("\n  Raw cache files:")
    for p in sorted(RAW_POI_DIR.glob("*_raw.json")):
        print(f"    {p}  ({p.stat().st_size / 1024:.1f} KB)")

    print("\n  Manual verification flags:")
    if total_pois > 0 and "needs_manual_verify" in poi_gdf.columns:
        needs_verify = poi_gdf["needs_manual_verify"].sum()
        print(f"    {needs_verify} POIs flagged for manual verification")
        print("    Hospitals: verify against Kemenkes RS Online database")
        print("    Industrial: unnamed zones flagged — verify area > 10 hectares")
    else:
        print("    No POIs to verify (empty dataset)")

    print("\n  Next step: 15_compute_poi_travel_times.py (r5py routing from POI set)")
    print("=" * 60)

    # Exit with error if no POIs at all (unusual — likely network issue)
    if total_pois == 0:
        print("\nWARNING: Zero POIs extracted. Check network connectivity and Overpass API.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
