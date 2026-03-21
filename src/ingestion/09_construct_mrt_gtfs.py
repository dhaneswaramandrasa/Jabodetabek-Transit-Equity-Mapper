#!/usr/bin/env python3
"""
09_construct_mrt_gtfs.py — Construct MRT Jakarta GTFS feed manually.

MRT Jakarta does not publish an official GTFS feed. This script constructs
one from published station data and official schedule information.

Lines included:
  1. North-South Line Phase 1 — Lebak Bulus Grab ↔ Bundaran HI (13 stations)

MRT Phase 2 (Bundaran HI → Kota) is under construction and not included.

Output: data/raw/gtfs/mrt/mrt_gtfs.zip
"""

import csv
import io
import zipfile
from datetime import datetime, timedelta
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = PROJECT_ROOT / "data" / "raw" / "gtfs" / "mrt"

# ─── Station Data ────────────────────────────────────────────────────────────
# MRT North-South Line Phase 1 (operational since March 2019)
# Coordinates from OpenStreetMap, cross-referenced with jakartamrt.co.id
# Format: (stop_id, stop_name, lat, lon, is_underground)

STATIONS = [
    ("LBB", "Lebak Bulus Grab", -6.2893, 106.7744, False),
    ("FTM", "Fatmawati Indomaret", -6.2920, 106.7930, False),
    ("CPR", "Cipete Raya", -6.2783, 106.7978, False),
    ("HJN", "Haji Nawi", -6.2662, 106.7972, False),
    ("BLA", "Blok A", -6.2547, 106.7983, False),
    ("BLM", "Blok M BCA", -6.2442, 106.7983, True),
    ("ASN", "ASEAN", -6.2383, 106.7983, True),
    ("SNY", "Senayan", -6.2271, 106.8019, True),
    ("IST", "Istora Mandiri", -6.2218, 106.8069, True),
    ("BNH", "Bendungan Hilir", -6.2150, 106.8150, True),
    ("STB", "Setiabudi Astra", -6.2088, 106.8219, True),
    ("DKA", "Dukuh Atas BNI", -6.2008, 106.8228, True),
    ("BHI", "Bundaran HI", -6.1950, 106.8231, True),
]

# Schedule parameters from jakartamrt.co.id (2025-2026)
SCHEDULE = {
    "first_departure": "05:00",
    "last_departure": "24:00",  # midnight
    "headway_peak_min": 5,      # 06:00-09:00 and 17:00-20:00
    "headway_offpeak_min": 10,  # other hours
    "headway_weekend_min": 10,
    "avg_interstation_min": 2,  # avg ~2 min between stations (total ~24 min end-to-end)
}

# Fare structure (for reference, not in GTFS)
# Base: Rp 3,000 + Rp 1,000/km, max Rp 14,000
# Lebak Bulus → Bundaran HI: ~Rp 14,000


def parse_time(s: str) -> timedelta:
    h, m = map(int, s.split(":"))
    return timedelta(hours=h, minutes=m)


def fmt_time(td: timedelta) -> str:
    total_seconds = int(td.total_seconds())
    h = total_seconds // 3600
    m = (total_seconds % 3600) // 60
    s = total_seconds % 60
    return f"{h:02d}:{m:02d}:{s:02d}"


def build_gtfs() -> dict[str, str]:
    """Build all GTFS files as {filename: csv_content}."""
    files = {}

    # ── agency.txt ──
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["agency_id", "agency_name", "agency_url", "agency_timezone", "agency_lang"])
    w.writerow(["MRT-JAKARTA", "PT MRT Jakarta", "https://jakartamrt.co.id", "Asia/Jakarta", "id"])
    files["agency.txt"] = buf.getvalue()

    # ── stops.txt ──
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["stop_id", "stop_name", "stop_lat", "stop_lon", "location_type"])
    for sid, name, lat, lon, _ in STATIONS:
        w.writerow([f"MRT-{sid}", name, f"{lat:.6f}", f"{lon:.6f}", 0])
    files["stops.txt"] = buf.getvalue()

    # ── routes.txt ──
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["route_id", "agency_id", "route_short_name", "route_long_name",
                "route_type", "route_color", "route_text_color"])
    w.writerow(["MRT-NS", "MRT-JAKARTA", "North-South",
                "Lebak Bulus Grab - Bundaran HI", 1, "009B3A", "FFFFFF"])
    files["routes.txt"] = buf.getvalue()

    # ── calendar.txt ──
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["service_id", "monday", "tuesday", "wednesday", "thursday",
                "friday", "saturday", "sunday", "start_date", "end_date"])
    w.writerow(["WEEKDAY", 1, 1, 1, 1, 1, 0, 0, "20260101", "20261231"])
    w.writerow(["WEEKEND", 0, 0, 0, 0, 0, 1, 1, "20260101", "20261231"])
    files["calendar.txt"] = buf.getvalue()

    # ── trips.txt + stop_times.txt ──
    trips_buf = io.StringIO()
    st_buf = io.StringIO()
    tw = csv.writer(trips_buf)
    stw = csv.writer(st_buf)
    tw.writerow(["route_id", "service_id", "trip_id", "trip_headsign", "direction_id"])
    stw.writerow(["trip_id", "arrival_time", "departure_time", "stop_id", "stop_sequence"])

    trip_counter = 0
    avg_min = SCHEDULE["avg_interstation_min"]

    peak_start_am = parse_time("06:00")
    peak_end_am = parse_time("09:00")
    peak_start_pm = parse_time("17:00")
    peak_end_pm = parse_time("20:00")

    first = parse_time(SCHEDULE["first_departure"])
    last = parse_time(SCHEDULE["last_departure"])

    station_ids = [s[0] for s in STATIONS]

    for service_id in ["WEEKDAY", "WEEKEND"]:
        for direction in [0, 1]:
            if direction == 0:
                trip_stations = station_ids
                headsign = "Bundaran HI"
            else:
                trip_stations = list(reversed(station_ids))
                headsign = "Lebak Bulus Grab"

            dep = first
            while dep <= last:
                # Determine headway
                if service_id == "WEEKDAY":
                    in_peak = (peak_start_am <= dep <= peak_end_am or
                               peak_start_pm <= dep <= peak_end_pm)
                    headway = SCHEDULE["headway_peak_min"] if in_peak else SCHEDULE["headway_offpeak_min"]
                else:
                    headway = SCHEDULE["headway_weekend_min"]

                trip_counter += 1
                trip_id = f"MRT-NS-{service_id[0]}-{direction}-{trip_counter:04d}"

                tw.writerow(["MRT-NS", service_id, trip_id, headsign, direction])

                for seq, sid in enumerate(trip_stations):
                    arr = dep + timedelta(minutes=seq * avg_min)
                    dep_stop = arr + timedelta(seconds=20) if seq < len(trip_stations) - 1 else arr
                    stw.writerow([trip_id, fmt_time(arr), fmt_time(dep_stop),
                                 f"MRT-{sid}", seq + 1])

                dep += timedelta(minutes=headway)

    files["trips.txt"] = trips_buf.getvalue()
    files["stop_times.txt"] = st_buf.getvalue()

    # ── feed_info.txt ──
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["feed_publisher_name", "feed_publisher_url", "feed_lang",
                "feed_start_date", "feed_end_date", "feed_version"])
    w.writerow(["JTEM Research Project", "https://github.com/dhaneswaramandrasa/Jabodetabek-Transit-Equity-Mapper",
                "id", "20260101", "20261231", f"manual-{datetime.now().strftime('%Y%m%d')}"])
    files["feed_info.txt"] = buf.getvalue()

    return files


def main():
    print("=" * 60)
    print("MRT Jakarta GTFS Constructor")
    print("=" * 60)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    files = build_gtfs()

    zip_path = OUT_DIR / "mrt_gtfs.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, content in files.items():
            zf.writestr(name, content)

    trips_count = files["trips.txt"].count("\n") - 1
    stops_count = files["stops.txt"].count("\n") - 1
    stop_times_count = files["stop_times.txt"].count("\n") - 1

    print(f"\nOutput: {zip_path}")
    print(f"Size: {zip_path.stat().st_size / 1024:.1f} KB")
    print(f"Stations: {stops_count}")
    print(f"Lines: 1 (North-South Phase 1)")
    print(f"Trips: {trips_count}")
    print(f"Stop times: {stop_times_count}")
    print(f"Generated: {datetime.now().isoformat()}")
    print(f"Feed validity: 2026-01-01 to 2026-12-31")

    # Write metadata
    meta_path = OUT_DIR / "CONSTRUCTION_NOTES.md"
    with open(meta_path, "w") as f:
        f.write("# MRT Jakarta GTFS — Construction Notes\n\n")
        f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d')}\n")
        f.write("**Method**: Manual construction from published schedules and OSM station data\n")
        f.write("**Feed validity**: 2026-01-01 to 2026-12-31\n\n")
        f.write("## Line\n\n")
        f.write("- **North-South Phase 1**: Lebak Bulus Grab → Bundaran HI (13 stations)\n")
        f.write("- Peak headway: 5 min (06:00-09:00, 17:00-20:00)\n")
        f.write("- Off-peak headway: 10 min\n")
        f.write("- End-to-end time: ~24 min\n")
        f.write("- Operating hours: 05:00-24:00\n\n")
        f.write("## Sources\n\n")
        f.write("- Station coordinates: OpenStreetMap + jakartamrt.co.id\n")
        f.write("- Schedule: jakartamrt.co.id published timetable (2025-2026)\n")
        f.write("- Community reference: github.com/reksamamur/mrt-jakarta-api\n\n")
        f.write("## Limitations\n\n")
        f.write("- Phase 2 extension (Bundaran HI → Kota) not included (under construction)\n")
        f.write("- Exact per-segment travel times approximated with 2-min average\n")
        f.write("- Holiday schedules not included\n")
        f.write("- Fare data not encoded in GTFS (no fare_attributes.txt)\n")

    print(f"Metadata: {meta_path}")


if __name__ == "__main__":
    main()
