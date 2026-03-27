"""
Generalized Cost Model — Layer 5 of the 5-layer TAI
Computes GC for transit, car, and motorcycle to Sudirman–Thamrin CBD.

Cost parameters finalized in MVP-8 / docs/methodology.md §2.2 Layer 5.
"""

import math

# ── Constants ──────────────────────────────────────────────────────────────────

SUDIRMAN_LON = 106.823
SUDIRMAN_LAT = -6.200

VOT_PER_MIN = 500           # IDR/min — Jakarta UMR proxy (~Rp 30k/hr)
TRANSFER_FRICTION = 5_000   # IDR per transfer (~10 min equivalent)
DISCOMFORT_PEAK = 3_000     # IDR peak-hour crowding penalty

# Car parameters
CAR_FUEL_PER_KM = 1_000     # IDR/km (12 km/L × Rp 10k/L Pertalite, rounded)
CAR_PARKING_CBD = 25_000    # IDR flat
CAR_FATIGUE = 0             # climate-controlled

# Motorcycle parameters
MOTO_FUEL_PER_KM = 200      # IDR/km (50 km/L × Rp 10k/L — 5:1 car:moto ratio)
MOTO_PARKING_CBD = 8_000    # IDR flat
# Motorcycles cannot use toll roads (PP No. 15/2005)

# Toll cost lookup by distance bracket (car only)
TOLL_BRACKETS = [
    (8,  0),
    (15, 8_000),
    (25, 15_000),
    (35, 25_000),
    (50, 35_000),
    (999, 40_000),
]

# Transit fare lookup by distance (KRL/MRT/BRT weighted average)
TRANSIT_FARE_BRACKETS = [
    (10, 3_000),    # KRL base fare
    (20, 6_500),
    (35, 10_000),
    (999, 13_000),
]


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Straight-line distance in km."""
    R = 6_371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlam / 2) ** 2
    return R * 2 * math.asin(math.sqrt(a))


def _lookup(value: float, brackets: list) -> float:
    for threshold, cost in brackets:
        if value <= threshold:
            return cost
    return brackets[-1][1]


def _fatigue_premium_moto(ride_min: float) -> float:
    """Motorcycle fatigue premium — heat/rain/exhaust exposure."""
    if ride_min < 20:
        return 0
    elif ride_min < 40:
        return 5_000
    elif ride_min < 60:
        return 10_000
    else:
        return 15_000


def compute_gc(
    centroid_lat: float,
    centroid_lon: float,
    transit_time_min: float | None,
    transit_fare_idr: float | None,
    n_transfers: int = 0,
    first_mile_min: float = 10.0,
) -> dict:
    """
    Compute generalized cost (IDR) for all three modes from a kelurahan
    centroid to Sudirman–Thamrin.

    Parameters
    ----------
    centroid_lat, centroid_lon : float
        Kelurahan centroid coordinates.
    transit_time_min : float | None
        Door-to-door transit travel time from r5py (None = no transit service).
    transit_fare_idr : float | None
        Estimated transit fare (None = no transit service).
    n_transfers : int
        Number of transit transfers (0 = direct).
    first_mile_min : float
        Walk/ojol first-mile time (minutes).

    Returns
    -------
    dict with keys: gc_transit_idr, gc_car_idr, gc_motorcycle_idr,
                    cheapest_private_mode, tcr_vs_car, tcr_vs_motorcycle,
                    tcr_combined, transit_competitive_zone,
                    distance_to_sudirman_km
    """
    dist_km = haversine_km(centroid_lat, centroid_lon, SUDIRMAN_LAT, SUDIRMAN_LON)
    # Add 20% road routing buffer
    road_dist_km = dist_km * 1.20

    # ── Car ───────────────────────────────────────────────────────────────────
    car_fuel = road_dist_km * CAR_FUEL_PER_KM
    car_toll = _lookup(dist_km, TOLL_BRACKETS)
    # Approximate car travel time: dist / 25 km/h (Jakarta congestion)
    car_time_min = (road_dist_km / 25.0) * 60.0
    gc_car = (
        car_fuel
        + car_toll
        + CAR_PARKING_CBD
        + car_time_min * VOT_PER_MIN
        + CAR_FATIGUE
    )

    # ── Motorcycle ────────────────────────────────────────────────────────────
    moto_fuel = road_dist_km * MOTO_FUEL_PER_KM
    # Motorcycles use surface roads — ~30 km/h accounting for traffic signals
    moto_time_min = (road_dist_km / 30.0) * 60.0
    moto_fatigue = _fatigue_premium_moto(moto_time_min)
    gc_motorcycle = (
        moto_fuel
        + MOTO_PARKING_CBD
        + moto_time_min * VOT_PER_MIN
        + moto_fatigue
    )

    # ── Transit ───────────────────────────────────────────────────────────────
    if transit_time_min is None or transit_fare_idr is None:
        gc_transit = None
        transit_competitive_zone = "transit_not_available"
        tcr_vs_car = None
        tcr_vs_motorcycle = None
        tcr_combined = None
        cheapest_private = "motorcycle" if gc_motorcycle < gc_car else "car"
    else:
        first_mile_cost = first_mile_min * VOT_PER_MIN  # walk time monetized
        gc_transit = (
            transit_fare_idr
            + transit_time_min * VOT_PER_MIN
            + n_transfers * TRANSFER_FRICTION
            + first_mile_cost
            + DISCOMFORT_PEAK
        )

        cheapest_private = "motorcycle" if gc_motorcycle < gc_car else "car"
        cheapest_private_gc = min(gc_car, gc_motorcycle)

        tcr_vs_car = gc_car / gc_transit if gc_transit > 0 else None
        tcr_vs_motorcycle = gc_motorcycle / gc_transit if gc_transit > 0 else None
        tcr_combined = cheapest_private_gc / gc_transit if gc_transit > 0 else None

        if tcr_combined is None:
            transit_competitive_zone = "transit_not_available"
        elif tcr_combined > 1.2:
            transit_competitive_zone = "transit_wins"
        elif tcr_combined >= 0.8:
            transit_competitive_zone = "swing"
        else:
            transit_competitive_zone = "private_wins"

    return {
        "gc_transit_idr": round(gc_transit) if gc_transit is not None else None,
        "gc_car_idr": round(gc_car),
        "gc_motorcycle_idr": round(gc_motorcycle),
        "cheapest_private_mode": "motorcycle" if gc_motorcycle < gc_car else "car",
        "tcr_vs_car": round(tcr_vs_car, 3) if tcr_vs_car is not None else None,
        "tcr_vs_motorcycle": round(tcr_vs_motorcycle, 3) if tcr_vs_motorcycle is not None else None,
        "tcr_combined": round(tcr_combined, 3) if tcr_combined is not None else None,
        "transit_competitive_zone": transit_competitive_zone,
        "distance_to_sudirman_km": round(dist_km, 2),
    }
