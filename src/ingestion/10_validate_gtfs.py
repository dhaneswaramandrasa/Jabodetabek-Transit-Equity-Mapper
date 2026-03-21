#!/usr/bin/env python3
"""
10_validate_gtfs.py — Validate constructed KRL and MRT GTFS feeds.

Runs structural validation on the GTFS feeds:
  1. All required files present
  2. CSV structure valid
  3. Foreign key references valid (stop_id in stop_times → stops.txt)
  4. Time ordering valid (stop_times sorted within each trip)
  5. Coordinate sanity (within Jabodetabek bounding box)
  6. Optional: gtfs_kit validation if available

Output: Validation report to stdout + data/raw/gtfs/VALIDATION_REPORT.md
"""

import csv
import io
import sys
import zipfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
GTFS_DIR = PROJECT_ROOT / "data" / "raw" / "gtfs"

# Jabodetabek bounding box (generous)
BBOX = {
    "min_lat": -6.80,
    "max_lat": -6.05,
    "min_lon": 106.20,
    "max_lon": 107.20,
}

REQUIRED_FILES = ["agency.txt", "stops.txt", "routes.txt", "trips.txt",
                  "stop_times.txt", "calendar.txt"]


def read_csv_from_zip(zf: zipfile.ZipFile, name: str) -> list[dict]:
    with zf.open(name) as f:
        text = io.TextIOWrapper(f, encoding="utf-8-sig")
        return list(csv.DictReader(text))


def validate_feed(zip_path: Path) -> dict:
    """Validate a single GTFS ZIP. Returns {checks: [(name, pass, detail)]}."""
    results = []
    feed_name = zip_path.stem

    if not zip_path.exists():
        results.append(("file_exists", False, f"{zip_path} not found"))
        return {"name": feed_name, "checks": results}

    results.append(("file_exists", True, f"{zip_path.stat().st_size / 1024:.1f} KB"))

    with zipfile.ZipFile(zip_path, "r") as zf:
        file_list = zf.namelist()

        # 1. Required files
        for req in REQUIRED_FILES:
            present = req in file_list
            results.append((f"has_{req}", present, "present" if present else "MISSING"))

        if not all(req in file_list for req in REQUIRED_FILES):
            return {"name": feed_name, "checks": results}

        # 2. Read data
        stops = read_csv_from_zip(zf, "stops.txt")
        routes = read_csv_from_zip(zf, "routes.txt")
        trips = read_csv_from_zip(zf, "trips.txt")
        stop_times = read_csv_from_zip(zf, "stop_times.txt")
        calendar = read_csv_from_zip(zf, "calendar.txt")

        results.append(("stops_count", True, f"{len(stops)} stops"))
        results.append(("routes_count", True, f"{len(routes)} routes"))
        results.append(("trips_count", True, f"{len(trips)} trips"))
        results.append(("stop_times_count", True, f"{len(stop_times)} stop_times"))
        results.append(("calendar_count", True, f"{len(calendar)} service periods"))

        # 3. Coordinate sanity
        bad_coords = []
        for stop in stops:
            lat = float(stop["stop_lat"])
            lon = float(stop["stop_lon"])
            if not (BBOX["min_lat"] <= lat <= BBOX["max_lat"] and
                    BBOX["min_lon"] <= lon <= BBOX["max_lon"]):
                bad_coords.append(f"{stop['stop_id']} ({lat}, {lon})")
        results.append(("coords_in_bbox", len(bad_coords) == 0,
                        "all OK" if not bad_coords else f"OUT OF BBOX: {bad_coords}"))

        # 4. Foreign key: stop_times.stop_id → stops.stop_id
        stop_ids = {s["stop_id"] for s in stops}
        orphan_stops = set()
        for st in stop_times:
            if st["stop_id"] not in stop_ids:
                orphan_stops.add(st["stop_id"])
        results.append(("fk_stop_times_stops", len(orphan_stops) == 0,
                        "all OK" if not orphan_stops else f"ORPHANS: {orphan_stops}"))

        # 5. Foreign key: trips.route_id → routes.route_id
        route_ids = {r["route_id"] for r in routes}
        orphan_routes = set()
        for t in trips:
            if t["route_id"] not in route_ids:
                orphan_routes.add(t["route_id"])
        results.append(("fk_trips_routes", len(orphan_routes) == 0,
                        "all OK" if not orphan_routes else f"ORPHANS: {orphan_routes}"))

        # 6. Foreign key: trips.service_id → calendar.service_id
        service_ids = {c["service_id"] for c in calendar}
        orphan_services = set()
        for t in trips:
            if t["service_id"] not in service_ids:
                orphan_services.add(t["service_id"])
        results.append(("fk_trips_calendar", len(orphan_services) == 0,
                        "all OK" if not orphan_services else f"ORPHANS: {orphan_services}"))

        # 7. Time ordering within trips
        trip_times: dict[str, list[str]] = {}
        for st in stop_times:
            trip_times.setdefault(st["trip_id"], []).append(st["arrival_time"])
        bad_order = 0
        for tid, times in trip_times.items():
            for i in range(1, len(times)):
                if times[i] < times[i - 1]:
                    bad_order += 1
                    break
        results.append(("time_ordering", bad_order == 0,
                        "all OK" if bad_order == 0 else f"{bad_order} trips with bad ordering"))

        # 8. No duplicate stop_ids
        dup_stops = len(stop_ids) != len(stops)
        results.append(("no_duplicate_stops", not dup_stops,
                        "all unique" if not dup_stops else "DUPLICATES FOUND"))

    return {"name": feed_name, "checks": results}


def main():
    print("=" * 60)
    print("GTFS Feed Validator — Jabodetabek Transit Equity Mapper")
    print("=" * 60)

    feeds = [
        GTFS_DIR / "krl" / "krl_gtfs.zip",
        GTFS_DIR / "mrt" / "mrt_gtfs.zip",
    ]

    all_results = []
    all_pass = True

    for feed_path in feeds:
        result = validate_feed(feed_path)
        all_results.append(result)

        print(f"\n── {result['name']} ──")
        for check_name, passed, detail in result["checks"]:
            status = "PASS" if passed else "FAIL"
            icon = "✓" if passed else "✗"
            print(f"  {icon} {check_name:25s} : {status} — {detail}")
            if not passed:
                all_pass = False

    # Write report
    report_path = GTFS_DIR / "VALIDATION_REPORT.md"
    with open(report_path, "w") as f:
        f.write("# GTFS Validation Report\n\n")
        f.write(f"**Date**: {__import__('datetime').datetime.now().strftime('%Y-%m-%d')}\n")
        f.write(f"**Overall**: {'PASS' if all_pass else 'FAIL'}\n\n")

        for result in all_results:
            f.write(f"## {result['name']}\n\n")
            f.write("| Check | Status | Detail |\n")
            f.write("|-------|--------|--------|\n")
            for check_name, passed, detail in result["checks"]:
                status = "PASS" if passed else "**FAIL**"
                f.write(f"| {check_name} | {status} | {detail} |\n")
            f.write("\n")

    print(f"\n{'=' * 60}")
    print(f"OVERALL: {'PASS' if all_pass else 'FAIL'}")
    print(f"Report: {report_path}")

    # Try gtfs_kit for read validation (confirms feed is parseable)
    try:
        import gtfs_kit as gk
        print("\ngtfs_kit available — confirming feeds are parseable...")
        for feed_path in feeds:
            if feed_path.exists():
                print(f"\n── gtfs_kit: {feed_path.name} ──")
                feed = gk.read_feed(str(feed_path), dist_units="km")
                print(f"  agency: {len(feed.agency)} rows")
                print(f"  stops: {len(feed.stops)} rows")
                print(f"  routes: {len(feed.routes)} rows")
                print(f"  trips: {len(feed.trips)} rows")
                print(f"  stop_times: {len(feed.stop_times)} rows")
                print(f"  calendar: {len(feed.calendar)} rows")
                print("  Feed parsed successfully by gtfs_kit")
    except ImportError:
        print("\ngtfs_kit not installed — skipping parse check.")
        print("Install with: pip install gtfs_kit")

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
