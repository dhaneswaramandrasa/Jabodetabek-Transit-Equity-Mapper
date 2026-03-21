#!/usr/bin/env python3
"""
08_construct_krl_gtfs.py — Construct KRL Commuterline GTFS feed manually.

KAI Commuter does not publish an official GTFS feed. This script constructs
one from published station data and GAPEKA 2025 schedule information.

Lines included:
  1. Bogor/Nambo Line (Red)     — Jakarta Kota ↔ Bogor/Nambo
  2. Cikarang Line (Blue)       — Jakarta Kota ↔ Cikarang
  3. Rangkasbitung Line (Green) — Tanah Abang ↔ Rangkasbitung
  4. Tangerang Line (Brown)     — Duri ↔ Tangerang
  5. Tanjung Priok Line (Pink)  — Jakarta Kota ↔ Tanjung Priok

Station coordinates sourced from OpenStreetMap and cross-referenced with
Google Maps. Schedule headways based on GAPEKA 2025 published timetables.

Output: data/raw/gtfs/krl/krl_gtfs.zip
"""

import csv
import io
import os
import zipfile
from datetime import datetime, timedelta
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = PROJECT_ROOT / "data" / "raw" / "gtfs" / "krl"

# ─── Station Data ────────────────────────────────────────────────────────────
# Format: (stop_id, stop_name, lat, lon)
# Coordinates from OSM/Google Maps, ~10m accuracy

STATIONS = {
    # ── Shared Jakarta core stations ──
    "JKT": ("Jakarta Kota", -6.1376, 106.8145),
    "JAY": ("Jayakarta", -6.1412, 106.8230),
    "MGB": ("Mangga Besar", -6.1496, 106.8269),
    "SWB": ("Sawah Besar", -6.1607, 106.8276),
    "JUA": ("Juanda", -6.1667, 106.8310),
    "GDD": ("Gondangdia", -6.1857, 106.8333),
    "CKI": ("Cikini", -6.1907, 106.8393),
    "MRI": ("Manggarai", -6.2100, 106.8502),

    # ── Bogor Line (south from Manggarai) ──
    "TEB": ("Tebet", -6.2260, 106.8577),
    "CWG": ("Cawang", -6.2432, 106.8614),
    "DKA": ("Duren Kalibata", -6.2557, 106.8548),
    "PSM": ("Pasar Minggu", -6.2843, 106.8445),
    "PMB": ("Pasar Minggu Baru", -6.2917, 106.8414),
    "TJB": ("Tanjung Barat", -6.3083, 106.8397),
    "LNA": ("Lenteng Agung", -6.3307, 106.8353),
    "UNP": ("Universitas Pancasila", -6.3383, 106.8327),
    "UNI": ("Universitas Indonesia", -6.3600, 106.8310),
    "PDC": ("Pondok Cina", -6.3687, 106.8320),
    "DPB": ("Depok Baru", -6.3833, 106.8186),
    "DPK": ("Depok", -6.3897, 106.8166),
    "CTM": ("Citayam", -6.4500, 106.7978),
    "BJG": ("Bojong Gede", -6.4867, 106.7822),
    "CLB": ("Cilebut", -6.5150, 106.7694),
    "BGR": ("Bogor", -6.5959, 106.7906),

    # ── Nambo branch (from Citayam) ──
    "NMO": ("Nambo", -6.4835, 106.7460),

    # ── Cikarang Line (east from Manggarai) ──
    "JNG": ("Jatinegara", -6.2148, 106.8703),
    "KLD": ("Klender", -6.2167, 106.8931),
    "BUA": ("Buaran", -6.2183, 106.9078),
    "KLB": ("Klender Baru", -6.2200, 106.9194),
    "CKG": ("Cakung", -6.2233, 106.9383),
    "KRI": ("Kranji", -6.2267, 106.9600),
    "BKS": ("Bekasi", -6.2362, 106.9994),
    "BKT": ("Bekasi Timur", -6.2483, 107.0187),
    "TMB": ("Tambun", -6.2600, 107.0469),
    "CBT": ("Cibitung", -6.2717, 107.0678),
    "MTA": ("Metland Telaga Murni", -6.2800, 107.0839),
    "CKR": ("Cikarang", -6.2567, 107.1448),

    # ── Rangkasbitung Line (from Tanah Abang south-west) ──
    "THB": ("Tanah Abang", -6.1858, 106.8107),
    "PLM": ("Palmerah", -6.2067, 106.7972),
    "KBY": ("Kebayoran", -6.2374, 106.7828),
    "PDR": ("Pondok Ranji", -6.2747, 106.7441),
    "JMG": ("Jurang Mangu", -6.2867, 106.7294),
    "SDM": ("Sudimara", -6.2942, 106.7142),
    "RBU": ("Rawa Buntu", -6.3117, 106.6820),
    "SRP": ("Serpong", -6.3200, 106.6642),
    "CSK": ("Cisauk", -6.3333, 106.6372),
    "CCR": ("Cicayur", -6.3383, 106.6256),
    "PPJ": ("Parung Panjang", -6.3450, 106.5689),
    "CJT": ("Cilejit", -6.3567, 106.5292),
    "DAR": ("Daru", -6.3467, 106.4967),
    "TNJ": ("Tenjo", -6.3400, 106.4569),
    "TGR": ("Tigaraksa", -6.3417, 106.4325),
    "CKA": ("Cikoya", -6.3483, 106.4033),
    "MAJ": ("Maja", -6.3567, 106.3842),
    "CTS": ("Citeras", -6.3617, 106.3522),
    "RKB": ("Rangkasbitung", -6.3517, 106.2511),

    # ── Tangerang Line (from Duri west) ──
    "DU": ("Duri", -6.1500, 106.8008),
    "GGL": ("Grogol", -6.1583, 106.7858),
    "PSG": ("Pesing", -6.1583, 106.7703),
    "TMK": ("Taman Kota", -6.1583, 106.7567),
    "BJI": ("Bojong Indah", -6.1567, 106.7361),
    "RWB": ("Rawa Buaya", -6.1567, 106.7175),
    "KDS": ("Kalideres", -6.1533, 106.7022),
    "PRS": ("Poris", -6.1550, 106.6761),
    "BTC": ("Batu Ceper", -6.1583, 106.6556),
    "TNG": ("Tangerang", -6.1767, 106.6297),

    # ── Tanjung Priok Line (from Jakarta Kota north) ──
    "KPB": ("Kampung Bandan", -6.1317, 106.8253),
    "ANC": ("Ancol", -6.1233, 106.8386),
    "TPK": ("Tanjung Priok", -6.1117, 106.8744),

    # ── Additional shared stations ──
    "SUD": ("Sudirman", -6.2025, 106.8233),
    "KAT": ("Karet", -6.1950, 106.8200),
    "MPG": ("Mampang", -6.2467, 106.8267),
    "TNT": ("Tanah Tinggi", -6.1717, 106.8367),
    "GST": ("Gang Sentiong", -6.1750, 106.8433),
    "PSE": ("Pasar Senen", -6.1733, 106.8467),
    "KMR": ("Kemayoran", -6.1600, 106.8500),
    "RJW": ("Rajawali", -6.1450, 106.8417),
}

# ─── Line Definitions ────────────────────────────────────────────────────────
# Each line: (route_id, route_short_name, route_long_name, color, station_ids, headway_peak_min, headway_offpeak_min)

LINES = [
    {
        "route_id": "KRL-BOGOR",
        "short_name": "Bogor",
        "long_name": "Jakarta Kota - Bogor",
        "color": "ED1C24",
        "stations": [
            "JKT", "JAY", "MGB", "SWB", "JUA", "GDD", "CKI", "MRI",
            "TEB", "CWG", "DKA", "PSM", "PMB", "TJB", "LNA", "UNP",
            "UNI", "PDC", "DPB", "DPK", "CTM", "BJG", "CLB", "BGR",
        ],
        "headway_peak": 8,
        "headway_offpeak": 15,
        "first_departure": "04:30",
        "last_departure": "23:00",
        "avg_interstation_min": 3,
    },
    {
        "route_id": "KRL-CIKARANG",
        "short_name": "Cikarang",
        "long_name": "Jakarta Kota - Cikarang",
        "color": "0072BC",
        "stations": [
            "JKT", "JAY", "MGB", "SWB", "JUA", "GDD", "CKI", "MRI",
            "JNG", "KLD", "BUA", "KLB", "CKG", "KRI", "BKS", "BKT",
            "TMB", "CBT", "MTA", "CKR",
        ],
        "headway_peak": 10,
        "headway_offpeak": 20,
        "first_departure": "04:45",
        "last_departure": "22:30",
        "avg_interstation_min": 3,
    },
    {
        "route_id": "KRL-RANGKASBITUNG",
        "short_name": "Rangkasbitung",
        "long_name": "Tanah Abang - Rangkasbitung",
        "color": "00A651",
        "stations": [
            "THB", "PLM", "KBY", "PDR", "JMG", "SDM", "RBU", "SRP",
            "CSK", "CCR", "PPJ", "CJT", "DAR", "TNJ", "TGR", "CKA",
            "MAJ", "CTS", "RKB",
        ],
        "headway_peak": 15,
        "headway_offpeak": 30,
        "first_departure": "05:00",
        "last_departure": "21:00",
        "avg_interstation_min": 4,
    },
    {
        "route_id": "KRL-TANGERANG",
        "short_name": "Tangerang",
        "long_name": "Duri - Tangerang",
        "color": "8B4513",
        "stations": [
            "DU", "GGL", "PSG", "TMK", "BJI", "RWB", "KDS", "PRS",
            "BTC", "TNG",
        ],
        "headway_peak": 12,
        "headway_offpeak": 20,
        "first_departure": "05:00",
        "last_departure": "22:00",
        "avg_interstation_min": 3,
    },
    {
        "route_id": "KRL-TANJUNGPRIOK",
        "short_name": "Tanjung Priok",
        "long_name": "Jakarta Kota - Tanjung Priok",
        "color": "FF69B4",
        "stations": [
            "JKT", "KPB", "ANC", "TPK",
        ],
        "headway_peak": 15,
        "headway_offpeak": 30,
        "first_departure": "05:30",
        "last_departure": "21:00",
        "avg_interstation_min": 4,
    },
]


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
    w.writerow(["KAI-COMMUTER", "KAI Commuter", "https://commuterline.id", "Asia/Jakarta", "id"])
    files["agency.txt"] = buf.getvalue()

    # ── stops.txt ──
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["stop_id", "stop_name", "stop_lat", "stop_lon", "location_type"])
    used_stations = set()
    for line in LINES:
        for sid in line["stations"]:
            used_stations.add(sid)
    for sid in sorted(used_stations):
        name, lat, lon = STATIONS[sid]
        w.writerow([f"KRL-{sid}", name, f"{lat:.6f}", f"{lon:.6f}", 0])
    files["stops.txt"] = buf.getvalue()

    # ── routes.txt ──
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["route_id", "agency_id", "route_short_name", "route_long_name",
                "route_type", "route_color", "route_text_color"])
    for line in LINES:
        w.writerow([line["route_id"], "KAI-COMMUTER", line["short_name"],
                    line["long_name"], 2, line["color"], "FFFFFF"])
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

    for line in LINES:
        stations = line["stations"]
        n_stations = len(stations)
        avg_min = line["avg_interstation_min"]

        for service_id in ["WEEKDAY", "WEEKEND"]:
            headway = line["headway_peak"] if service_id == "WEEKDAY" else line["headway_offpeak"]

            first = parse_time(line["first_departure"])
            last = parse_time(line["last_departure"])

            # Peak hours: 06:00-09:00, 17:00-20:00
            peak_start_am = parse_time("06:00")
            peak_end_am = parse_time("09:00")
            peak_start_pm = parse_time("17:00")
            peak_end_pm = parse_time("20:00")

            # Generate trips in both directions
            for direction in [0, 1]:
                if direction == 0:
                    trip_stations = stations
                    headsign = STATIONS[stations[-1]][0]
                else:
                    trip_stations = list(reversed(stations))
                    headsign = STATIONS[stations[0]][0]

                dep = first
                while dep <= last:
                    # Determine headway based on peak/offpeak
                    if service_id == "WEEKDAY":
                        in_peak = (peak_start_am <= dep <= peak_end_am or
                                   peak_start_pm <= dep <= peak_end_pm)
                        current_headway = line["headway_peak"] if in_peak else line["headway_offpeak"]
                    else:
                        current_headway = line["headway_offpeak"]

                    trip_counter += 1
                    trip_id = f"{line['route_id']}-{service_id[0]}-{direction}-{trip_counter:04d}"

                    tw.writerow([line["route_id"], service_id, trip_id, headsign, direction])

                    for seq, sid in enumerate(trip_stations):
                        arr = dep + timedelta(minutes=seq * avg_min)
                        # 30 second dwell at each station
                        dep_stop = arr + timedelta(seconds=30) if seq < len(trip_stations) - 1 else arr
                        stw.writerow([trip_id, fmt_time(arr), fmt_time(dep_stop),
                                     f"KRL-{sid}", seq + 1])

                    dep += timedelta(minutes=current_headway)

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
    print("KRL Commuterline GTFS Constructor")
    print("=" * 60)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    files = build_gtfs()

    zip_path = OUT_DIR / "krl_gtfs.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, content in files.items():
            zf.writestr(name, content)

    # Count stats
    trips_count = files["trips.txt"].count("\n") - 1
    stops_count = files["stops.txt"].count("\n") - 1
    stop_times_count = files["stop_times.txt"].count("\n") - 1

    print(f"\nOutput: {zip_path}")
    print(f"Size: {zip_path.stat().st_size / 1024:.1f} KB")
    print(f"Stations: {stops_count}")
    print(f"Lines: {len(LINES)}")
    print(f"Trips: {trips_count}")
    print(f"Stop times: {stop_times_count}")
    print(f"Generated: {datetime.now().isoformat()}")
    print(f"Feed validity: 2026-01-01 to 2026-12-31")

    # Write metadata
    meta_path = OUT_DIR / "CONSTRUCTION_NOTES.md"
    with open(meta_path, "w") as f:
        f.write("# KRL Commuterline GTFS — Construction Notes\n\n")
        f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d')}\n")
        f.write("**Method**: Manual construction from published schedules and OSM station data\n")
        f.write("**Feed validity**: 2026-01-01 to 2026-12-31\n\n")
        f.write("## Sources\n\n")
        f.write("- Station coordinates: OpenStreetMap + Google Maps cross-reference\n")
        f.write("- Schedule headways: GAPEKA 2025 published timetables\n")
        f.write("- Line structure: KAI Commuter official route map\n")
        f.write("- Community reference: github.com/comuline/api\n\n")
        f.write("## Lines\n\n")
        f.write(f"| Line | Stations | Peak headway | Off-peak headway |\n")
        f.write(f"|------|----------|-------------|------------------|\n")
        for line in LINES:
            f.write(f"| {line['short_name']} | {len(line['stations'])} | "
                    f"{line['headway_peak']} min | {line['headway_offpeak']} min |\n")
        f.write(f"\n## Limitations\n\n")
        f.write("- Schedules are approximated from published headways, not exact timetables\n")
        f.write("- Inter-station travel times use average values, not actual per-segment times\n")
        f.write("- Express/limited-stop services are not modeled\n")
        f.write("- Holiday schedules not included (calendar.txt has WEEKDAY/WEEKEND only)\n")
        f.write("- Nambo branch not modeled as separate trips (would need branching logic)\n")

    print(f"\nMetadata: {meta_path}")


if __name__ == "__main__":
    main()
