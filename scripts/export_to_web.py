"""
export_to_web.py — Export real pipeline output to transit-access web app.

Renames H3 field names to match DATA_MODEL.md schema, adds null placeholders
for missing fields, and writes both GeoJSONs to the web app's public/data/.

Usage:
    python scripts/export_to_web.py
"""

import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIPELINE_DIR = os.path.join(ROOT, "data", "processed", "scores")
WEB_DIR = os.path.join(
    os.path.dirname(ROOT), "transit-access", "web", "public", "data"
)

H3_INPUT = os.path.join(PIPELINE_DIR, "h3_scores.geojson")
KEL_INPUT = os.path.join(PIPELINE_DIR, "kelurahan_scores.geojson")

H3_OUTPUT = os.path.join(WEB_DIR, "h3_scores.geojson")
KEL_OUTPUT = os.path.join(WEB_DIR, "kelurahan_scores.geojson")

# H3 field renames: old_name → new_name (DATA_MODEL.md)
H3_RENAMES = {
    "n_stops": "n_transit_stops",
    "min_headway_min": "avg_headway_min",
    "mode_diversity": "transit_mode_diversity",
    "fare_tier": "best_mode_fare_tier",
    "has_affordable": "has_affordable_mode",
    "l1_first_mile": "tai_l1_first_mile",
    "l2_service_quality": "tai_l2_service_quality",
    "l3_cbd_journey": "tai_l3_cbd_journey",
    "l4_last_mile": "tai_l4_last_mile",
    "l5_cost_competitiveness": "tai_l5_cost_competitiveness",
    "poi_reach_cbd_weighted": "poi_reach_cbd_min",
}

# Fields to add as null in H3 GeoJSON (not computed at H3 level yet)
H3_NULL_FIELDS = [
    "kelurahan_id", "kelurahan_name", "kecamatan_name", "kota_kab_name",
    "area_km2", "n_transit_routes", "pct_primary_secondary",
    "pct_residential_tertiary", "avg_road_class_score", "road_adjusted_access",
    "poi_reach_hospital_min", "poi_reach_school_min", "poi_reach_market_min",
    "poi_reach_industrial_min", "poi_reach_govoffice_min",
    "est_cbd_journey_fare_idr", "gc_transit_idr", "gc_car_idr",
    "gc_motorcycle_idr", "cheapest_private_mode", "tcr_vs_car",
    "tcr_vs_motorcycle", "tcr_combined", "transit_competitive_zone",
    "distance_to_sudirman_km", "avg_traffic_speed_kmh",
    "peak_congestion_index", "traffic_adjusted_access",
]

# Kelurahan fields to add as null (traffic extension — v2)
KEL_NULL_FIELDS = [
    "avg_traffic_speed_kmh", "peak_congestion_index", "traffic_adjusted_access",
    "poi_reach_hospital_min", "poi_reach_school_min", "poi_reach_market_min",
    "poi_reach_industrial_min", "poi_reach_govoffice_min",
    "road_adjusted_access", "est_cbd_journey_fare_idr",
]


def migrate_h3(features):
    out = []
    for feat in features:
        props = dict(feat["properties"])

        # Rename fields
        for old, new in H3_RENAMES.items():
            if old in props:
                props[new] = props.pop(old)

        # Compute pop_density from population / h3_area_km2
        if "pop_density" not in props:
            pop = props.get("population") or 0
            area = props.get("h3_area_km2") or 1
            props["pop_density"] = round(pop / area, 2) if area > 0 else None

        # Add null fields
        for field in H3_NULL_FIELDS:
            if field not in props:
                props[field] = None

        out.append({**feat, "properties": props})
    return out


def migrate_kelurahan(features):
    out = []
    for feat in features:
        props = dict(feat["properties"])

        # Add null fields for missing schema fields
        for field in KEL_NULL_FIELDS:
            if field not in props:
                props[field] = None

        # H3-specific fields (null for kelurahan)
        for field in ["h3_index", "h3_area_km2", "is_edge_cell", "kelurahan_ids",
                       "has_feeder_service"]:
            if field not in props:
                props[field] = None

        out.append({**feat, "properties": props})
    return out


def main():
    os.makedirs(WEB_DIR, exist_ok=True)

    # --- H3 ---
    print(f"Reading {H3_INPUT}...")
    with open(H3_INPUT) as f:
        h3 = json.load(f)

    h3_features = migrate_h3(h3["features"])
    h3_out = {**h3, "features": h3_features}

    print(f"Writing {H3_OUTPUT} ({len(h3_features)} features)...")
    with open(H3_OUTPUT, "w") as f:
        json.dump(h3_out, f, separators=(",", ":"))

    # --- Kelurahan ---
    print(f"Reading {KEL_INPUT}...")
    with open(KEL_INPUT) as f:
        kel = json.load(f)

    kel_features = migrate_kelurahan(kel["features"])
    kel_out = {**kel, "features": kel_features}

    print(f"Writing {KEL_OUTPUT} ({len(kel_features)} features)...")
    with open(KEL_OUTPUT, "w") as f:
        json.dump(kel_out, f, separators=(",", ":"))

    print("Done.")
    print(f"H3 sample fields: {list(h3_features[0]['properties'].keys())[:15]}")
    print(f"Kel sample fields: {list(kel_features[0]['properties'].keys())[:15]}")


if __name__ == "__main__":
    main()
