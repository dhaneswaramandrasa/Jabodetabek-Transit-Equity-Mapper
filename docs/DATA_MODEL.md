# Data Model

**Last updated**: 2026-03-16
**Source**: `docs/methodology.md` §2.3
**Contract**: This file = `lib/types.ts` = `lib/mock-data.ts`. All three must match.

---

## Primary Schema — Kelurahan Level

### Identity & Geography

| Field | Type | Description | Source Dataset |
|-------|------|-------------|---------------|
| `kelurahan_id` | string | Unique admin code (BPS code) | #7 Admin boundaries |
| `kelurahan_name` | string | Name | #7 |
| `kecamatan_name` | string | Parent kecamatan | #7 |
| `kota_kab_name` | string | Parent kota/kabupaten | #7 |
| `geometry` | polygon | Kelurahan boundary | #7 |
| `area_km2` | float | Area in square kilometers | Computed from #7 |

### Need Indicators (TNI)

| Field | Type | Description | Source Dataset |
|-------|------|-------------|---------------|
| `population` | int | Total population | #8 BPS + #9 WorldPop |
| `pop_density` | float | Population per km² | Computed |
| `poverty_rate` | float | % population below poverty line | #8 (kecamatan disaggregated) |
| `avg_household_expenditure` | float | Monthly avg (IDR) | #8 (kecamatan disaggregated) |
| `zero_vehicle_hh_pct` | float | Est. % households with no motor vehicle | #8 modeled |
| `dependency_ratio` | float | (Age <15 + >64) / working-age | #8 |
| `tni_score` | float [0,1] | Composite Transit Need Index | Computed |

### Road Network Indicators

| Field | Type | Description | Source Dataset |
|-------|------|-------------|---------------|
| `road_length_km` | float | Total road length within kelurahan | #5 OSM |
| `road_density_km_per_km2` | float | Road length / area | Computed |
| `pct_primary_secondary` | float | % road length that is primary/secondary | #5 |
| `pct_residential_tertiary` | float | % road length that is residential/tertiary | #5 |
| `pct_footway_pedestrian` | float | % road length classified as footway/pedestrian/path | #5 |
| `avg_road_class_score` | float | Weighted avg road hierarchy score | #5 Computed |
| `network_connectivity` | float | Intersection density (nodes/km²) | #5 Computed |

### Access Indicators (TAI)

| Field | Type | Description | Source Dataset |
|-------|------|-------------|---------------|
| `n_transit_stops` | int | Count of unique transit stops | #1–4 GTFS |
| `n_transit_routes` | int | Count of unique routes serving stops | #1–4 |
| `avg_headway_min` | float | Average scheduled headway (minutes) | #1–3 stop_times |
| `min_dist_to_transit_m` | float | Distance from centroid to nearest stop | #1–4, #5 |
| `transit_mode_diversity` | int | Count of distinct modes (BRT, KRL, MRT, LRT, Mikrotrans) | #1–4 |
| `road_adjusted_access` | float | Access score weighted by road network quality | #1–5 Computed |
| `poi_reach_cbd_min` | float | Gravity-weighted travel time to CBD zones | #1–3, #6 (r5py) |
| `poi_reach_hospital_min` | float | Travel time to nearest major hospital | #1–3, #6 |
| `poi_reach_school_min` | float | Travel time to nearest SMA/SMK/University | #1–3, #6 |
| `poi_reach_market_min` | float | Travel time to nearest major market | #1–3, #6 |
| `poi_reach_industrial_min` | float | Travel time to nearest industrial zone | #1–3, #6 |
| `poi_reach_govoffice_min` | float | Travel time to nearest government office | #1–3, #6 |

### Fare Tier Indicators

| Field | Type | Description | Source Dataset |
|-------|------|-------------|---------------|
| `best_mode_fare_tier` | int [1–4] | Fare tier of best available mode | #1–4 Computed |
| `has_affordable_mode` | bool | Tier 1–2 mode available? | #1–4 Computed |
| `est_cbd_journey_fare_idr` | int \| null | Estimated cumulative fare to Sudirman–Thamrin | Computed post-hoc |

### Three-Way Cost Comparison (Layer 5)

| Field | Type | Description | Source |
|-------|------|-------------|--------|
| `gc_transit_idr` | float | Generalized cost: transit to Sudirman–Thamrin | Computed |
| `gc_car_idr` | float | Generalized cost: car to Sudirman–Thamrin | Computed |
| `gc_motorcycle_idr` | float | Generalized cost: motorcycle to Sudirman–Thamrin | Computed |
| `cheapest_private_mode` | enum (car/motorcycle) | Which private mode has lower GC | Computed |
| `tcr_vs_car` | float | GC_car / GC_transit | Computed |
| `tcr_vs_motorcycle` | float | GC_motorcycle / GC_transit | Computed |
| `tcr_combined` | float | min(GC_car, GC_motorcycle) / GC_transit | Computed |
| `transit_competitive_zone` | enum | "transit_wins" (>1.2) / "swing" (0.8–1.2) / "private_wins" (<0.8) | Computed |
| `distance_to_sudirman_km` | float | Straight-line distance to Sudirman–Thamrin centroid | Computed |

### Traffic Extension (v2 — null by default)

| Field | Type | Description | Source |
|-------|------|-------------|--------|
| `avg_traffic_speed_kmh` | float \| null | Average road traffic speed | Future #11/#12 |
| `peak_congestion_index` | float \| null | Peak-hour / free-flow speed ratio | Future #11/#12 |
| `traffic_adjusted_access` | float \| null | Access re-weighted by traffic | Future computed |

### Composite & Derived

| Field | Type | Description | Source |
|-------|------|-------------|--------|
| `tai_score` | float [0,1] | Composite Transit Accessibility Index | Computed |
| `equity_gap` | float [-1,1] | tni_score − tai_score | Computed |
| `quadrant` | enum (Q1/Q2/Q3/Q4) | Quadrant classification | Computed |

---

## Secondary Schema — H3 Level

Same fields as kelurahan, plus:

| Field | Type | Description | Derivation |
|-------|------|-------------|------------|
| `h3_index` | string | H3 cell ID at resolution 8 | h3-py |
| `h3_geometry` | polygon | Hexagon boundary | h3-py |
| `h3_area_km2` | float | ~0.74 km² (constant) | h3-py |

---

## H3 Derivation Methods

| Data Type | Method | Rationale |
|-----------|--------|-----------|
| Socioeconomic (population, poverty, expenditure, vehicle ownership) | **Dasymetric mapping** via WorldPop raster | Population not uniform within kelurahan; WorldPop captures at ~100m |
| Infrastructure counts (road network, road class proportions) | **Area-weighted / spatial clip** | Physical features with known locations; direct clipping is accurate |
| Point features (transit stops, POIs) | **Point-in-polygon** spatial join | Exact coordinates; assign to containing H3 cell |
| Travel-time based (poi_reach_*, min_dist_to_transit) | **Direct computation** from H3 centroid | Fresh routing from hex centroid; no redistribution needed |

---

## Raw Datasets

| # | Dataset | Format | Source | Access |
|---|---------|--------|--------|--------|
| 1 | TransJakarta BRT GTFS | GTFS ZIP | Mobility Database | Open |
| 2 | KRL Commuterline GTFS | GTFS ZIP | Mobility Database | Open |
| 3 | MRT Jakarta GTFS | GTFS ZIP | Mobility Database | Open |
| 4 | LRT Jabodebek stations | Manual GeoJSON | Wikipedia/official | Open (manual) |
| 5 | OSM road network | PBF → GeoDataFrame | Geofabrik | Open |
| 6 | POIs (strict categories) | GeoJSON | Overpass API | Open |
| 7 | Admin boundaries | GeoJSON | GADM / Geoportal | Open |
| 8 | BPS demographic data | CSV / tables | BPS | Open |
| 9 | WorldPop population raster | GeoTIFF | WorldPop | Open |
| 10 | H3 hexagonal grid | Generated | h3-py | N/A |

---

## Join Keys

| Join | Left Key | Right Key | Type |
|------|----------|-----------|------|
| Demographics → Kelurahan | BPS kelurahan code | kelurahan_id | 1:1 |
| Transit stops → Kelurahan | stop geometry | kelurahan polygon | spatial (point-in-polygon) |
| Road network → Kelurahan | road geometry | kelurahan polygon | spatial (overlay/clip) |
| WorldPop → H3 | raster cell | H3 polygon | zonal stats |
| Kelurahan rates → H3 | kelurahan polygon | H3 polygon | spatial overlay + pop weighting |
| Transit stops → H3 | stop geometry | H3 polygon | spatial (point-in-polygon) |

---

## TAI Formula (5-Layer Model)

```
TAI = 0.20 × L1_first_mile
    + 0.15 × L2_service_quality
    + 0.35 × L3_cbd_journey_chain
    + 0.15 × L4_last_mile
    + 0.15 × L5_cost_competitiveness
```

### Layer Formulas

```
L1 = 0.35 × norm(1/walk_dist) + 0.25 × norm(pct_footway) + 0.20 × norm(connectivity) + 0.20 × norm(has_feeder)
L2 = 0.35 × norm(1/headway) + 0.25 × norm(mode_diversity) + 0.20 × norm(1/fare_tier) + 0.20 × norm(has_affordable)
L3 = norm(1/poi_reach_cbd_weighted)
L4 = r5py egress + 0.50 × norm(cbd_station_integration) + 0.50 × norm(cbd_mode_transfer)
L5 = norm(clamp(TCR_combined, 0.3, 2.0))
```

---

## Mock Data Spec

- Kelurahan record count: ~1,800 (Jabodetabek)
- H3 record count: ~15,000–20,000 (resolution 8)
- Generated from: methodology formulas with realistic ranges per field
- Field names must exactly match this schema
