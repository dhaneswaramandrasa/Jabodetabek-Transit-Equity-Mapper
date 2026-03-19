# H3 Derivation Pipeline: Dasymetric and Area-Weighted Methods

**Ticket**: MVP-7 (E0-004)
**Status**: Draft
**Last updated**: 2026-03-19
**Feeds**: `docs/methodology.md` Section 2.3 (H3 schema), Section 2.5 Steps 17-22; `docs/DATA_MODEL.md` Secondary Schema

---

## 1. H3 Resolution Selection

### 1.1 Primary Resolution: H3 Resolution 8

The primary analytical grid uses H3 resolution 8, producing hexagonal cells of approximately **0.74 km^2** (~461,354 m^2 exact average area). At this resolution, the edge-to-edge distance across a cell is approximately 860 m, which corresponds closely to a walkable neighborhood catchment (roughly 10 minutes of walking at 5 km/h).

**Why resolution 8:**

| Criterion | Res-7 (~5.16 km^2) | Res-8 (~0.74 km^2) | Res-9 (~0.11 km^2) |
|-----------|---------------------|---------------------|---------------------|
| Cell count (Jabodetabek) | ~3,000-5,000 | ~15,000-20,000 | ~50,000-70,000 |
| Comparable urban unit | Large kampung cluster | Walkable neighborhood | City block |
| Population per cell (avg) | ~6,000-10,000 | ~800-2,000 | ~100-300 |
| Within-kelurahan variation | Coarse (2-8 cells per kelurahan) | Good (10-50 cells per kelurahan) | Very fine (70-350 cells per kelurahan) |
| Computational cost (r5py routing) | Low (~5k origins) | Moderate (~18k origins) | High (~60k origins) |
| WorldPop raster fit | Multiple raster cells per hex | ~74 raster cells per hex (100m grid) | ~11 raster cells per hex |

Resolution 8 balances three concerns:

1. **Analytical granularity**: With 10-50 cells per kelurahan, res-8 can detect within-kelurahan variation in both socioeconomic need and transit access -- directly testing H2 (the resolution effect hypothesis). Resolution 7 is too coarse for this; only 2-8 cells per kelurahan would fail to expose internal heterogeneity in larger suburban kelurahan.

2. **Statistical robustness**: At ~800-2,000 persons per cell (metropolitan average), each cell contains enough population to produce meaningful socioeconomic indicators. Resolution 9 cells averaging ~100-300 persons risk unstable estimates, particularly for rate-based indicators like poverty_rate and zero_vehicle_hh_pct where small-number effects introduce noise.

3. **Computational feasibility**: The r5py travel time matrix computation from ~18,000 H3 centroids to ~9 CBD zones (plus hospitals, schools, markets, industrial zones, government offices) is tractable on a standard workstation. At res-9 (~60,000 centroids), the same computation would require roughly 3.3x more routing calls, potentially exceeding memory constraints for the R5 engine.

The choice of res-8 is consistent with emerging practice in urban transport analytics. While no single standard exists for H3 resolution in transit studies, res-8 is the most commonly used resolution for metropolitan-scale walkability and accessibility analyses in the H3 literature (Uber Engineering, 2018). The cell size approximates the "pedestrian shed" concept used in transit-oriented development planning.

### 1.2 Sensitivity Analysis at Resolutions 7 and 9

To address MAUP concerns and validate the robustness of findings, the full analytical pipeline will be re-run at two additional resolutions:

- **Resolution 7** (~5.16 km^2, ~3,000-5,000 cells): Tests whether coarser aggregation produces materially different equity conclusions. Expected: res-7 will smooth over within-kelurahan variation and produce results more similar to the kelurahan-level analysis, serving as a bridge between the two spatial frameworks.

- **Resolution 9** (~0.11 km^2, ~50,000-70,000 cells): Tests whether finer granularity reveals additional patterns invisible at res-8. Expected: res-9 will amplify edge effects and produce noisier socioeconomic estimates due to small-cell populations, but may reveal micro-scale accessibility gaps (e.g., a pocket of residents separated from transit by a highway or waterway).

The sensitivity analysis is detailed in Section 5 below.

---

## 2. Grid Generation Procedure

### 2.1 Bounding Box and Study Area Definition

The study area is the Jabodetabek metropolitan region, comprising:
- DKI Jakarta (5 kota administrasi)
- Kota Bogor, Kabupaten Bogor
- Kota Depok
- Kota Tangerang, Kabupaten Tangerang, Kota Tangerang Selatan
- Kota Bekasi, Kabupaten Bekasi

**Boundary source**: GADM level-3 (kecamatan) polygons, dissolved to the study area boundary. Using GADM rather than BPS boundaries ensures consistency with international geocoding standards while maintaining sub-kelurahan precision.

### 2.2 Grid Generation Steps

```
Step 1: Load Jabodetabek boundary
  - Load GADM level-3 polygons for all kota/kabupaten in Jabodetabek
  - Dissolve to single study area polygon (union of all boundaries)
  - Buffer by 500m to capture edge cells that straddle the boundary

Step 2: Generate H3 cells
  - Use h3.polyfill_geojson(study_area_geojson, resolution=8)
  - This returns all H3 cell IDs whose centroids fall within the polygon
  - Convert to GeoDataFrame with h3 cell boundaries via h3.h3_to_geo_boundary()

Step 3: Clip to study area
  - Spatial join: retain only H3 cells whose centroid falls within the
    unbuffered study area boundary (removes buffer-only cells)
  - Alternative: retain cells with >= 50% area overlap with the study area
    (prevents edge artifacts where centroids fall just outside)

Step 4: Validate
  - Count cells: expect ~15,000-20,000 at res-8
  - Visual check: overlay on admin boundary map
  - Verify: no gaps in coverage (H3 tessellation is seamless)
  - Verify: coastal cells over water are flagged (low/zero WorldPop population)
```

### 2.3 Estimated Cell Counts

| Resolution | Estimated Cells | Computation Note |
|------------|----------------|------------------|
| Res-7 | ~3,000-5,000 | Each res-7 cell contains exactly 7 res-8 children |
| Res-8 | ~15,000-20,000 | Primary analysis unit |
| Res-9 | ~50,000-70,000 | Each res-8 cell contains exactly 7 res-9 children |

The exact count depends on boundary definition and edge-cell handling. Actual counts will be reported after grid generation.

### 2.4 Edge Cell Handling

Cells at the study area boundary may be only partially within Jabodetabek. These are handled as follows:

- **Coastal cells**: Cells partially over water (Jakarta Bay, rivers) will have reduced WorldPop population. No special treatment needed -- dasymetric mapping naturally assigns low population to water areas.
- **Border cells**: Cells straddling the Jabodetabek boundary with neighboring regions (e.g., Kabupaten Lebak, Kabupaten Karawang) are included if their centroid falls within the study area. Socioeconomic data is available only for the Jabodetabek side; the cell is assigned the value of the overlapping kelurahan.
- **Flag field**: A boolean `is_edge_cell` flag will be added to identify boundary cells for sensitivity checks (exclude edge cells and verify results are stable).

---

## 3. Dual-Method Derivation Strategy

The core challenge of the H3 grid is that source data originates at different spatial units (kelurahan administrative polygons, 100m raster cells, point coordinates, network segments). Each data type requires a different derivation method to produce accurate H3-level values. Four methods are used, each matched to the spatial nature of the underlying data.

### 3.1 Dasymetric Mapping (WorldPop-Weighted) -- Socioeconomic Indicators

**Applies to**: `population`, `pop_density`, `poverty_rate`, `avg_household_expenditure`, `zero_vehicle_hh_pct`, `dependency_ratio`

**Rationale**: Socioeconomic indicators from BPS are reported at kecamatan level and disaggregated to kelurahan level (methodology.md step 9) before H3 derivation. Simply distributing kelurahan rates uniformly across all H3 cells within the kelurahan would still be incorrect -- population is concentrated in built-up areas, with portions of a kelurahan being agricultural land, water, or open space (particularly in outer Bodetabek). Dasymetric mapping uses an ancillary population raster (WorldPop Indonesia, ~100m resolution) to allocate values proportionally to where people actually live.

**WorldPop raster specification**:
- Dataset: WorldPop Indonesia Constrained Individual Countries 2020, ~100m (3 arc-second)
- CRS: WGS84 (EPSG:4326) -- matches H3 native coordinate system
- Each raster cell contains an estimated population count
- "Constrained" variant uses building footprints and land cover to ensure population is only allocated to settled areas

**Derivation formula -- population**:

```
pop_h3 = sum of WorldPop raster cell values within H3 cell boundary

Implementation:
  1. Use rasterstats.zonal_stats(h3_polygon, worldpop_raster, stats=['sum'])
  2. This sums all raster cell populations that fall within each H3 hexagon
  3. Result: estimated population per H3 cell
```

**Derivation formula -- rate-based indicators (poverty_rate, etc.)**:

For indicators that are rates (not counts), the derivation is more nuanced. A single H3 cell may overlap with one or more kelurahan (at boundaries). The formula uses population-weighted allocation:

```
value_h3 = sum(pop_raster_in_h3_and_kelurahan_k * value_kelurahan_k)
         / sum(pop_raster_in_h3)

Where:
  - k indexes each kelurahan that overlaps the H3 cell
  - pop_raster_in_h3_and_kelurahan_k = WorldPop population sum within
    the intersection of the H3 cell and kelurahan k
  - value_kelurahan_k = the kelurahan-level indicator value (e.g., poverty_rate)
    (disaggregated from kecamatan BPS data in methodology.md step 9)
  - sum(pop_raster_in_h3) = total WorldPop population within the H3 cell

For H3 cells entirely within one kelurahan (the vast majority):
  value_h3 = value_kelurahan  (the rate passes through unchanged)

For H3 cells straddling a kelurahan boundary:
  value_h3 = weighted average of the two kelurahan values, weighted by
  the population in each kelurahan's portion of the cell
```

**Implementation steps**:

```
Step 1: Zonal population
  - For each H3 cell, compute total WorldPop population (rasterstats sum)
  - Store as pop_h3

Step 2: Spatial overlay
  - Intersect H3 grid with kelurahan boundaries (geopandas overlay)
  - This produces intersection polygons, each tagged with both h3_index
    and kelurahan_id

Step 3: Population within intersections
  - For each intersection polygon, compute WorldPop population sum
  - This gives pop_in_intersection(h3, kelurahan)

Step 4: Population-weighted rate allocation
  - For each H3 cell:
    poverty_rate_h3 = sum(pop_in_intersection(h3, k) * poverty_rate_k)
                    / pop_h3
  - Repeat for avg_household_expenditure, zero_vehicle_hh_pct,
    dependency_ratio
  - Note: kelurahan-level rates are pre-computed from kecamatan BPS data
    via dasymetric disaggregation (methodology.md step 9)

Step 5: Derived fields
  - pop_density_h3 = pop_h3 / h3_area_km2  (constant ~0.74 km^2)
```

**Assumptions and limitations of dasymetric approach**:

1. WorldPop accuracy depends on building footprint detection and land cover classification. In rapidly developing peri-urban areas (e.g., Cibitung, Cikarang), recent construction may not be reflected.
2. The method assumes within-kelurahan variation in rates (poverty, expenditure) follows population density patterns. This is a standard assumption in dasymetric mapping (Mennis, 2003) but may not hold in areas where low-density settlements are systematically different from high-density ones (e.g., gated communities vs. kampung).
3. H3 cells with zero WorldPop population (water, forest, industrial land) will have undefined rates. These cells are flagged as `pop_h3 = 0` and excluded from statistical analysis but retained in the spatial grid for visualization.

### 3.2 Area-Weighted Spatial Clip -- Infrastructure Indicators

**Applies to**: `road_length_km`, `road_density_km_per_km2`, `pct_primary_secondary`, `pct_residential_tertiary`, `pct_footway_pedestrian`, `avg_road_class_score`, `network_connectivity`

**Rationale**: Road segments are physical features with known geometries. Unlike socioeconomic rates, road density is a property of the physical space, not of the population. The correct method is to clip road geometries to each H3 cell boundary and recompute metrics from the clipped segments.

**Derivation procedure**:

```
Step 1: Clip road network to H3 grid
  - Use geopandas.overlay(roads_gdf, h3_gdf, how='intersection')
  - Each road segment is split at H3 cell boundaries
  - Each resulting fragment retains its highway classification tag

Step 2: Compute per-cell road metrics
  For each H3 cell:
  - road_length_km = sum of clipped segment lengths (in km)
  - road_density_km_per_km2 = road_length_km / h3_area_km2
  - pct_primary_secondary = length of primary+secondary segments / road_length_km
  - pct_residential_tertiary = length of residential+tertiary segments / road_length_km
  - pct_footway_pedestrian = length of footway+pedestrian+path segments / road_length_km
  - avg_road_class_score = weighted average of road class scores
    (primary=5, secondary=4, tertiary=3, residential=2, footway=1),
    weighted by segment length

Step 3: Compute intersection density (network_connectivity)
  - Extract road network nodes (intersections with degree >= 3) from OSM
  - Point-in-polygon join: count nodes within each H3 cell
  - network_connectivity = node_count / h3_area_km2
```

**Why not population-weighted**: Road infrastructure does not scale with population -- a highway passes through both populated and unpopulated areas equally. Area-weighted clipping captures the actual physical infrastructure within each cell, which is what matters for first-mile walkability assessment.

**Edge handling**: Road segments that cross H3 cell boundaries are split at the boundary. Each fragment is assigned to its containing cell. This is geometrically exact (no double-counting).

### 3.3 Point-in-Polygon -- Discrete Features

**Applies to**: `n_transit_stops`, `n_transit_routes`, `transit_mode_diversity`, `avg_headway_min`

**Rationale**: Transit stops and POIs have exact point coordinates. Each point belongs to exactly one H3 cell. The derivation is a straightforward spatial join.

**Derivation procedure**:

```
Step 1: Spatial join stops to H3
  - geopandas.sjoin(stops_gdf, h3_gdf, predicate='within')
  - Each stop is assigned to its containing H3 cell

Step 2: Aggregate per cell
  - n_transit_stops = count of unique stops in cell
  - n_transit_routes = count of unique route_ids serving stops in cell
  - transit_mode_diversity = count of distinct mode types
    (BRT, KRL, MRT, LRT, Mikrotrans) among stops in cell
  - avg_headway_min = mean of median headways across all stops in cell
    (median headway per stop computed from GTFS stop_times departure diffs)

Step 3: Handle cells with zero stops
  - n_transit_stops = 0 (valid -- transit desert)
  - n_transit_routes = 0
  - transit_mode_diversity = 0
  - avg_headway_min = NaN, imputed to max value (worst case) for
    normalization, as specified in the missing data strategy
```

**Alternative considered**: Using `h3.geo_to_h3(lat, lng, resolution=8)` to convert each stop's coordinates directly to an H3 index (avoiding the spatial join entirely). This is computationally faster and geometrically equivalent -- the h3 library places each point in exactly the correct cell. This approach is preferred for implementation efficiency.

### 3.4 Direct Computation -- Travel Times and Distances

**Applies to**: `min_dist_to_transit_m`, `poi_reach_cbd_min` (gravity-weighted), `poi_reach_hospital_min`, `poi_reach_school_min`, `poi_reach_market_min`, `poi_reach_industrial_min`, `poi_reach_govoffice_min`, all generalized cost fields (`gc_transit_idr`, `gc_car_idr`, `gc_motorcycle_idr`, etc.)

**Rationale**: Travel times and distances are origin-dependent. Redistributing kelurahan-level travel times to H3 cells would be methodologically incorrect -- a kelurahan centroid may be 2 km from a transit stop, but specific H3 cells within that kelurahan could range from 100 m to 4 km away. The correct approach is to compute travel times fresh from each H3 cell's centroid.

**Derivation procedure**:

```
Step 1: Extract H3 centroids
  - For each H3 cell, compute the centroid (h3.h3_to_geo returns center point)
  - These ~18,000 centroids become the origin points for all routing

Step 2: Network distance to nearest transit stop
  - For each centroid, find the nearest transit stop using:
    Option A: osmnx shortest-path network distance (preferred, captures
    actual walking routes)
    Option B: Euclidean distance (fallback if network routing is too slow
    for 18k origins)
  - Store as min_dist_to_transit_m

Step 3: Multi-modal travel times via r5py
  - Build r5py TransportNetwork from GTFS feeds (#1-3) + OSM PBF (#5)
  - Compute travel time matrix: 18,000 H3 centroids x destinations
  - r5py configuration (from methodology.md Section 2.6a):
    transport_mode: TRANSIT
    access_mode: WALK
    egress_mode: WALK
    max_walk_time: 20 min
    max_trip_duration: 120 min
    max_transfers: 3
    transfer_penalty: 600 sec (10 min)
    departure_time: 07:00 weekday
    departure_window: 60 min (7:00-8:00 AM)
  - Destinations: 9 CBD zone centroids, nearest hospital, nearest school,
    nearest market, nearest industrial zone, nearest government office

Step 4: Gravity-weighted CBD travel time
  - For each H3 centroid, compute:
    poi_reach_cbd_weighted = sum(tt_to_CBD_i * weight_i) / sum(weight_i)
  - Weights as defined in methodology.md Section 2.6a:
    Sudirman-Thamrin: 5.0, Kuningan: 4.0, Gatot Subroto: 3.5,
    TB Simatupang: 3.0, Kelapa Gading: 2.0, PIK: 1.5,
    BSD/Summarecon Bekasi/Summarecon Serpong: 1.0 each

Step 5: Generalized cost computation
  - For each H3 centroid, compute gc_transit_idr, gc_car_idr,
    gc_motorcycle_idr using the formulas in methodology.md Section 2.2
  - Derive tcr_vs_car, tcr_vs_motorcycle, tcr_combined,
    transit_competitive_zone
```

**Why direct computation is essential**: This is the strongest methodological argument for the H3 grid. Two H3 cells within the same large suburban kelurahan (e.g., in Kabupaten Bogor) may have dramatically different travel times to Sudirman-Thamrin -- one cell is 500 m from a KRL station, the other is 3 km away with no feeder service. The kelurahan-level analysis assigns both the same `poi_reach_cbd_min` value (from the kelurahan centroid), masking this critical within-unit variation. H3 direct computation exposes it.

This is precisely the mechanism underlying H2 (resolution effect hypothesis): kelurahan-level analysis systematically underestimates equity gaps in heterogeneous suburban areas because a single centroid-based travel time cannot represent the internal variation that multiple H3 centroids reveal.

---

## 4. MAUP Mitigation Strategy

### 4.1 The MAUP Problem in Transit Equity Analysis

The Modifiable Areal Unit Problem (MAUP) is a well-documented source of bias in spatial analysis: results change depending on the choice of spatial unit boundaries and scale (Openshaw, 1984). Javanmard et al. (2023) demonstrated this directly for transit equity, showing that route-level analysis of Winnipeg's bus system indicated equitable distribution, while stop-level and neighborhood-level analyses revealed significant inequity. The spatial scale of analysis changed the equity conclusion.

In the Jabodetabek context, MAUP manifests in two ways:

1. **Scale effect**: Kelurahan boundaries aggregate heterogeneous areas. A large kelurahan in Kabupaten Bekasi (~20-50 km^2) may contain both dense residential areas near a KRL station and rural/agricultural land far from any transit. The kelurahan-level average masks this internal variation.

2. **Zoning effect**: Kelurahan boundaries are administrative, not functionally defined. They do not correspond to transit catchment areas, employment zones, or socioeconomic neighborhoods. H3 hexagons, being uniform and boundary-independent, avoid the zoning effect entirely.

### 4.2 Dual-Resolution Comparison as MAUP Control

The research design addresses MAUP not by solving it (which is theoretically impossible for any single spatial unit) but by explicitly measuring its impact through dual-resolution comparison:

- **Resolution A**: Kelurahan boundaries (~1,800 units, variable size 0.5-50 km^2)
- **Resolution B**: H3 res-8 hexagons (~15,000-20,000 units, constant ~0.74 km^2)
- **Extended test**: H3 res-7 and res-9 for additional scale sensitivity

The identical analytical pipeline (TNI construction, TAI construction, equity gap, quadrant classification, Gini coefficient, Moran's I) is run at both resolutions. Differences in results are attributable to the spatial unit choice, directly quantifying the MAUP effect on transit equity conclusions.

### 4.3 Literature Support

Javanmard et al. (2023) provide the most direct precedent: they tested transit equity metrics at stop, route, and neighborhood levels, finding that "the choice of spatial aggregation level changes equity conclusions" -- the core motivation for our dual-resolution design. Their recommendation to "report metrics at multiple aggregation levels" is operationalized in our design as a systematic comparison with quantified divergence metrics.

The use of uniform hexagonal grids as a MAUP-mitigating spatial framework is supported by the broader spatial analysis literature. H3's uniform cell size eliminates the scale component of MAUP (all cells are the same area), though it does not eliminate the zoning component (any tessellation imposes arbitrary boundaries). The dual-resolution comparison across res-7, res-8, and res-9 tests both components by varying the scale while holding the zoning system constant (hexagonal).

---

## 5. Resolution Sensitivity Analysis Plan

### 5.1 Protocol

The full analytical pipeline (Steps 17-22 in methodology.md Section 2.5) will be run at three H3 resolutions:

| Step | Res-7 | Res-8 | Res-9 |
|------|-------|-------|-------|
| Grid generation | ~3-5k cells | ~15-20k cells | ~50-70k cells |
| Dasymetric socioeconomic mapping | Full | Full | Full |
| Road network clip | Full | Full | Full |
| Point-in-polygon (stops/POIs) | Full | Full | Full |
| r5py travel time matrix | Full | Full | Budget-dependent* |
| TNI/TAI/equity gap/quadrant | Full | Full | Full |
| Gini + Lorenz | Full | Full | Full |
| Moran's I / LISA | Full | Full | Full |

*Note: At res-9, the r5py travel time matrix requires ~60,000 routing origins. If computational budget is exceeded, a stratified sample of res-9 centroids (e.g., every 3rd cell, or cells within Q4 zones only) may be used. This is an open question -- see Section 7.

### 5.2 Comparison Metrics

**Quadrant classification stability**:

```
Confusion matrix: Res-8 quadrant vs. Res-7 quadrant

                Res-7
           Q1    Q2    Q3    Q4
Res-8 Q1 [ n11   n12   n13   n14 ]
      Q2 [ n21   n22   n23   n24 ]
      Q3 [ n31   n32   n33   n34 ]
      Q4 [ n41   n42   n43   n44 ]

Report:
- % cells reclassified (off-diagonal sum / total)
- Cohen's kappa coefficient (agreement beyond chance)
- Per-quadrant stability: % of Q4 cells at res-8 that remain Q4 at res-7
  (most policy-relevant: are transit deserts stable across resolutions?)
```

The same confusion matrix is computed for res-8 vs. res-9.

For the kelurahan vs. H3 comparison, each kelurahan is assigned the modal (most common) quadrant among its constituent H3 cells, then compared against its direct kelurahan-level classification.

**Distributional metrics**:

| Metric | Comparison |
|--------|------------|
| Gini coefficient (TAI) | Report at kelurahan, res-7, res-8, res-9 |
| Moran's I (equity gap) | Report at kelurahan, res-7, res-8, res-9 |
| TNI-TAI correlation (Pearson r) | Report at all four resolutions |
| Q4 cell count / percentage | Report at all four resolutions |
| Spatial pattern (visual) | Side-by-side choropleth maps at all resolutions |

**Expected patterns**:

1. Res-7 will produce similar results to kelurahan-level analysis (comparable cell size to medium kelurahan), supporting the claim that the kelurahan-level analysis is not an artifact of administrative boundaries per se, but of the scale.

2. Res-8 will reveal within-kelurahan variation, particularly in large outer-ring kelurahan, increasing the detected number of Q4 (transit desert) zones relative to kelurahan-level analysis.

3. Res-9 may produce noisier results (small populations, unstable rates) but should preserve the major spatial patterns from res-8. If Q4 clusters at res-9 closely match res-8 patterns, this confirms robustness. If they diverge significantly, this indicates that the specific choice of res-8 materially affects conclusions -- a finding worth reporting.

### 5.3 Reporting

The sensitivity analysis will be reported in the paper as follows:
- Main results at res-8 (primary analysis)
- Kelurahan comparison in the dual-resolution section
- Res-7 and res-9 results in a supplementary table + appendix figure
- Summary statistic: "X% of H3 res-8 cells retain their quadrant classification at both res-7 and res-9, indicating [robust/moderate/weak] spatial pattern stability"

---

## 6. Indicator-Method Mapping Summary

This table consolidates the derivation method for every field in the H3 schema.

### 6.1 Dasymetric (WorldPop-weighted)

| Field | Source Unit | Formula | Notes |
|-------|-----------|---------|-------|
| `population` | Raster cell | `sum(WorldPop cells in H3)` | Direct zonal sum |
| `pop_density` | Computed | `population / h3_area_km2` | Constant denominator |
| `poverty_rate` | Kelurahan (from BPS kecamatan via step 9) | `sum(pop_intersection_k * rate_k) / pop_h3` | Population-weighted from overlapping kelurahan(s) |
| `avg_household_expenditure` | Kelurahan (from BPS kecamatan via step 9) | Same as poverty_rate | Population-weighted |
| `zero_vehicle_hh_pct` | Kelurahan (from BPS kecamatan via step 9) | Same as poverty_rate | Population-weighted |
| `dependency_ratio` | Kelurahan (from BPS kecamatan via step 9) | Same as poverty_rate | Population-weighted |

### 6.2 Area-Weighted Spatial Clip

| Field | Source | Method | Notes |
|-------|--------|--------|-------|
| `road_length_km` | OSM segments | Clip segments to H3 boundary, sum lengths | Geometrically exact |
| `road_density_km_per_km2` | Computed | `road_length_km / h3_area_km2` | |
| `pct_primary_secondary` | OSM clipped | Length ratio from clipped segments | |
| `pct_residential_tertiary` | OSM clipped | Length ratio from clipped segments | |
| `pct_footway_pedestrian` | OSM clipped | Length ratio from clipped segments | |
| `avg_road_class_score` | OSM clipped | Length-weighted class score average | |
| `network_connectivity` | OSM nodes | Count degree-3+ nodes in cell / area | Point-in-polygon for nodes |

### 6.3 Point-in-Polygon

| Field | Source | Method | Notes |
|-------|--------|--------|-------|
| `n_transit_stops` | GTFS stops | Count stops in cell | Via h3.geo_to_h3() or spatial join |
| `n_transit_routes` | GTFS routes | Count unique routes at stops in cell | |
| `transit_mode_diversity` | GTFS | Count distinct modes at stops in cell | |
| `avg_headway_min` | GTFS stop_times | Mean of median headways per stop in cell | NaN if no stops |

### 6.4 Direct Computation (from H3 centroid)

| Field | Source | Method | Notes |
|-------|--------|--------|-------|
| `min_dist_to_transit_m` | H3 centroid + stops | Network distance (osmnx) or Euclidean | Computed fresh |
| `poi_reach_cbd_min` | H3 centroid + CBDs | r5py gravity-weighted (Section 2.6a) | 9 CBD destinations |
| `poi_reach_hospital_min` | H3 centroid + hospitals | r5py nearest | |
| `poi_reach_school_min` | H3 centroid + schools | r5py nearest | |
| `poi_reach_market_min` | H3 centroid + markets | r5py nearest | |
| `poi_reach_industrial_min` | H3 centroid + industrial | r5py nearest | |
| `poi_reach_govoffice_min` | H3 centroid + gov offices | r5py nearest | |
| `gc_transit_idr` | r5py + fare model | Full generalized cost formula | See methodology Section 2.2 |
| `gc_car_idr` | Distance-based model | Fuel + toll + parking + VOT | |
| `gc_motorcycle_idr` | Distance-based model | Fuel + parking + VOT + fatigue | |
| `tcr_vs_car` | Computed | `gc_car_idr / gc_transit_idr` | |
| `tcr_vs_motorcycle` | Computed | `gc_motorcycle_idr / gc_transit_idr` | |
| `tcr_combined` | Computed | `min(gc_car, gc_motorcycle) / gc_transit` | |
| `transit_competitive_zone` | Computed | Thresholds on tcr_combined | |
| `road_adjusted_access` | H3 road metrics + proximity | Formula from Section 2.6c | Uses H3-level road metrics |
| `tni_score` | H3 need indicators | Min-max normalize + weighted sum | Same formula as kelurahan |
| `tai_score` | H3 access indicators | 5-layer TAI formula | Same formula as kelurahan |
| `equity_gap` | Computed | `tni_score - tai_score` | |
| `quadrant` | Computed | Median-split classification | |

---

## 7. Literature Citations

| Decision | Supporting Literature |
|----------|---------------------|
| Dasymetric mapping as preferred disaggregation method | Mennis, J. (2003). Generating Surface Models of Population Using Dasymetric Mapping. *The Professional Geographer*, 55(1), 31-42. Standard reference for population-weighted areal interpolation. |
| WorldPop as allocation surface | Tatem, A.J. (2017). WorldPop, open data for spatial demography. *Scientific Data*, 4, 170004. Validates WorldPop accuracy in developing-country urban contexts. |
| H3 hexagonal grid for spatial analysis | Uber Engineering (2018). H3: Uber's Hexagonal Hierarchical Spatial Index. Uniform cell area eliminates one component of MAUP; hierarchical nesting enables multi-resolution analysis. |
| MAUP affects transit equity conclusions | Javanmard, R., Lee, J., Kim, J., Liu, L., & Diab, E. (2023). The impacts of the modifiable areal unit problem (MAUP) on social equity analysis of public transit reliability. *Journal of Transport Geography*, 106, 103523. Directly demonstrates scale-dependent equity conclusions. |
| Multi-resolution comparison as MAUP control | Javanmard et al. (2023), plus Openshaw, S. (1984). *The Modifiable Areal Unit Problem*. CATMOG 38. Norwich: Geo Books. Foundational MAUP reference. |
| Need-supply gap framework at spatial unit level | Currie, G. (2010); Mamun & Lownes (2011); Jiao & Dillivan (2013). Equity gap analysis applied at census tract / neighborhood spatial units -- our H3 cells serve the analogous role. |
| r5py for travel time matrices | Fink et al. (2022). r5py Python wrapper for R5 engine; used for all direct-computation travel times from H3 centroids. |
| Transit equity in developing-country metro context | Pereira et al. (2019). Distributional equity analysis in Rio de Janeiro using R5 routing; methodological precedent for r5py-based accessibility computation at scale. Delmelle & Casas (2012). Gini-based equity measurement applied to BRT in Cali, Colombia. |

---

## 8. Open Questions and Risks

### 8.1 Computational Budget

**r5py at res-9**: Computing travel time matrices from ~60,000 origins is approximately 3.3x the cost of res-8 (~18,000 origins). Each origin requires routing to multiple destinations (9 CBDs + nearest of each POI category). On a standard workstation with 16 GB RAM, the R5 engine may exceed memory constraints at this scale.

**Mitigation options**:
- Batch processing: split origins into chunks of 5,000, process sequentially
- Stratified sampling: compute res-9 travel times for a random 33% sample of cells, then interpolate (acceptable for sensitivity analysis, not for primary results)
- Downgrade res-9 to "spot check" status: compute only for cells that changed quadrant between res-7 and res-8, to test whether finer resolution resolves ambiguous cases

**Recommendation**: Attempt full res-9 computation first. If it fails due to resource constraints, fall back to stratified sampling and report the limitation.

### 8.2 WorldPop Temporal Mismatch

WorldPop Indonesia Constrained 2020 is the most recent available. BPS demographic data may be from 2021-2023 census/survey rounds. The ~1-3 year gap between population distribution (WorldPop) and socioeconomic rates (BPS) could introduce bias in rapidly developing areas where new housing estates have been built since 2020. This is acknowledged as a limitation but is unavoidable given data availability.

### 8.3 DATA_MODEL.md Field Updates

After reviewing the current DATA_MODEL.md against this derivation plan, the following updates are recommended:

1. **Add `is_edge_cell` field** (boolean) to the H3 schema -- flags cells at the study area boundary for sensitivity checks.
2. **Clarify `population` type at H3 level**: Currently listed as `float` in the methodology but `int` in DATA_MODEL.md's kelurahan schema. At H3 level, dasymetric-derived population should be `float` (it is an estimate, not a census count). This is already implied by the "same fields" statement but should be made explicit.
3. **Add `kelurahan_ids` field** (list of strings) to H3 schema -- records which kelurahan(s) overlap with each cell, supporting traceability of dasymetric allocation.

These are minor additions that do not change the existing schema contract. They should be reviewed and confirmed before implementation.

---

## 9. Implementation Sequence

The H3 derivation pipeline maps to wrangling Steps 17-22 in methodology.md Section 2.5:

| Priority | Step | Dependencies | Estimated Effort |
|----------|------|-------------|-----------------|
| 1 | Grid generation (Step 17) | Admin boundary GeoJSON (#7) | Low |
| 2 | Dasymetric socioeconomic mapping (Step 18) | Grid + WorldPop raster + BPS data | Medium-High |
| 3 | Area-weighted road clip (Step 19) | Grid + OSM road GDF | Medium |
| 4 | Point-in-polygon stops/POIs (Step 20) | Grid + unified stops + POIs | Low |
| 5 | Direct computation travel times (Step 21) | Grid + r5py TransportNetwork | High (compute-bound) |
| 6 | Composite index computation (Step 22) | All above | Low |
| 7 | Sensitivity analysis (res-7, res-9) | Full pipeline validated at res-8 | Medium-High |

Steps 2-4 can run in parallel after Step 1 completes. Step 5 is the computational bottleneck and should be initiated early. Step 7 runs after the res-8 pipeline is validated end-to-end.
