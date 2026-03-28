# Prototype Audit — MVP-26

**Audited**: 2026-03-28
**Source repo**: https://github.com/dhaneswaramandrasa/transit-access
**Against**: docs/DATA_MODEL.md (signed off 2026-03-21, MVP-82)

---

## Current Data Model (prototype)

### HexProperties (web/src/lib/store.ts)

| Field | Type | Notes |
|-------|------|-------|
| `h3_index` | string | Present |
| `composite_score` | number | Legacy scoring — not in new DATA_MODEL.md |
| `score_30min` | number | Legacy — replaced by `tai_score` |
| `score_60min` | number | Legacy — no equivalent in new schema |
| `percentile_rank` | number | Present; no direct equivalent in DATA_MODEL.md (derived stat) |
| `hospital_30min` | number | Legacy POI-count-by-threshold model; replaced by `poi_reach_hospital_min` |
| `hospital_60min` | number | Same |
| `clinic_30min` | number | Same |
| `clinic_60min` | number | Same |
| `market_30min` | number | Same |
| `market_60min` | number | Same |
| `supermarket_30min` | number | Same |
| `supermarket_60min` | number | Same |
| `school_30min` | number | Same |
| `school_60min` | number | Same |
| `park_30min` | number | Same |
| `park_60min` | number | Same |
| `pop_total` | number | Maps to `population` |
| `pct_dependent` | number | Maps to `dependency_ratio` (computed differently) |
| `pct_zero_vehicle` | number | Maps to `zero_vehicle_hh_pct` |
| `avg_njop` | number | Not in DATA_MODEL.md — property tax value; closest is `avg_household_expenditure` |
| `is_informal_settlement` | boolean | Not in DATA_MODEL.md |
| `dist_to_transit` | number | Maps to `min_dist_to_transit_m` (unit: km in prototype vs m in schema) |
| `is_walkable_transit` | boolean | Not in DATA_MODEL.md (derived flag; implied by `min_dist_to_transit_m < 1000`) |
| `transit_capacity_weight` | number | Not in DATA_MODEL.md (subsumed into L2 formula inputs) |
| `local_poi_density` | number | Not in DATA_MODEL.md as standalone field |
| `transit_shed_poi_count` | number | Not in DATA_MODEL.md as standalone field |
| `transit_need_score` | number [0,100] | Maps to `tni_score` [0,1] — scale differs |
| `transit_accessibility_score` | number [0,100] | Maps to `tai_score` [0,1] — scale differs |
| `equity_gap` | number | Present — scale differs (prototype 0–100 range, schema [-1,1]) |
| `quadrant` | EquityQuadrant | Present — label format differs (see note below) |

**Quadrant label mapping**:
| Prototype | DATA_MODEL.md |
|-----------|--------------|
| `"transit-desert"` | `Q4` (high need, low access) |
| `"transit-ideal"` | `Q1` (high need, high access) |
| `"over-served"` | `Q2` (low need, high access) |
| `"car-suburb"` | `Q3` (low need, low access) |

The prototype uses descriptive string labels; DATA_MODEL.md uses Q1–Q4 enum with the same 2×2 logic.

### Demographics (web/src/lib/store.ts)

| Field | Type | In DATA_MODEL.md? |
|-------|------|-------------------|
| `h3_index` | string | Yes |
| `kelurahan` | string | Maps to `kelurahan_name` |
| `kecamatan` | string | Maps to `kecamatan_name` |
| `city_code` | string | Partial match — `kota_kab_name` in schema |
| `population_density` | number | Maps to `pop_density` |
| `total_population` | number | Maps to `population` |
| `age_distribution` | Record<string, number> | Not in DATA_MODEL.md (summary fields only: `dependency_ratio`) |
| `dominant_age_group` | string | Not in DATA_MODEL.md |
| `sex_ratio` | number | Not in DATA_MODEL.md |
| `pct_dependent` | number | Maps to `dependency_ratio` |
| `pct_zero_vehicle` | number | Maps to `zero_vehicle_hh_pct` |
| `avg_njop` | number | Not in DATA_MODEL.md |
| `bps_source` | string | Not in DATA_MODEL.md |

---

## Schema Gap Analysis

Fields in DATA_MODEL.md absent from the prototype, ranked by priority for MVP-27.

| Field | In prototype? | DATA_MODEL.md type | Priority | Blocks |
|-------|---------------|--------------------|----------|--------|
| `tai_score` | No (has `transit_accessibility_score` 0–100 scaled) | float [0,1] | **P1 — Critical** | All quadrant + equity logic |
| `tni_score` | No (has `transit_need_score` 0–100 scaled) | float [0,1] | **P1 — Critical** | Quadrant classification |
| `quadrant` (Q1–Q4 enum) | No (has string labels) | enum Q1/Q2/Q3/Q4 | **P1 — Critical** | Map choropleth, filters |
| `n_transit_stops` | No | int | **P1** | Layer 1 + 2 formula display |
| `n_transit_routes` | No | int | **P1** | Layer 2 display |
| `avg_headway_min` | No | float | **P1** | Layer 2 (service quality) |
| `transit_mode_diversity` | No | int | **P1** | Layer 2 display card |
| `poi_reach_cbd_min` | No | float | **P1 — Core hypothesis** | Layer 3 (35% TAI weight) |
| `poi_reach_hospital_min` | No (has count-within-threshold only) | float | **P1** | Layer 3 display |
| `poi_reach_school_min` | No | float | **P1** | Layer 3 display |
| `poi_reach_market_min` | No | float | **P1** | Layer 3 display |
| `poi_reach_industrial_min` | No | float | **P1** | Layer 3 display |
| `poi_reach_govoffice_min` | No | float | **P1** | Layer 3 display |
| `best_mode_fare_tier` | No | int [1–4] | **P2** | Layer 2 (fare component) |
| `has_affordable_mode` | No | bool | **P2** | Layer 2 |
| `est_cbd_journey_fare_idr` | No | int/null | **P2** | Layer 5 cost card (MVP-28) |
| `gc_transit_idr` | No | float | **P2** | Layer 5 — MVP-28 required |
| `gc_car_idr` | No | float | **P2** | Layer 5 — MVP-28 required |
| `gc_motorcycle_idr` | No | float | **P2** | Layer 5 — MVP-28 required |
| `tcr_vs_car` | No | float | **P2** | Transit competitive zone map (MVP-32) |
| `tcr_vs_motorcycle` | No | float | **P2** | Same |
| `tcr_combined` | No | float | **P2** | Same |
| `transit_competitive_zone` | No | enum | **P2** | MVP-32 choropleth |
| `distance_to_sudirman_km` | No | float | **P2** | Layer 5 distance ring |
| `road_adjusted_access` | Partial (`transit_capacity_weight` is a proxy) | float | **P3** | Layer 1 formula accuracy |
| `road_length_km` | No | float | **P3** | Road network layer (MVP-28) |
| `road_density_km_per_km2` | No | float | **P3** | Same |
| `pct_primary_secondary` | No | float | **P3** | Road layer coloring |
| `pct_residential_tertiary` | No | float | **P3** | Same |
| `pct_footway_pedestrian` | No | float | **P3** | Layer 1 (first-mile formula) |
| `avg_road_class_score` | No | float | **P3** | Layer 1 |
| `network_connectivity` | No | float | **P3** | Layer 1 |
| `poverty_rate` | No | float | **P3** | TNI completeness |
| `avg_household_expenditure` | No | float | **P3** | TNI completeness |
| `area_km2` | No | float | **P4** | Area normalisation |
| `kelurahan_id` | No (has `kelurahan` name string only) | string (BPS code) | **P4** | Join key |
| `kota_kab_name` | Partial (`city_code`) | string | **P4** | Display |
| `geometry` | Present via GeoJSON | polygon | Already handled | — |
| `h3_geometry` | Present via GeoJSON | polygon | Already handled | — |
| `avg_traffic_speed_kmh` | No | float/null | **v2** | Traffic extension — null default |
| `peak_congestion_index` | No | float/null | **v2** | Same |
| `traffic_adjusted_access` | No | float/null | **v2** | Same |

**Fields in prototype NOT in DATA_MODEL.md** (to evaluate for removal or retention):

| Field | Decision |
|-------|----------|
| `composite_score` | Remove — superseded by `tai_score` |
| `score_30min` / `score_60min` | Remove — superseded by `poi_reach_*_min` travel-time model |
| `hospital_30min`…`park_60min` (12 POI-count fields) | Remove — superseded by `poi_reach_*_min` |
| `avg_njop` | Keep in Demographics only — useful for context display; not part of TNI formula |
| `is_informal_settlement` | Evaluate — not in DATA_MODEL.md; could be a computed flag from poverty_rate threshold |
| `is_walkable_transit` | Convert to derived display flag in UI; not a stored schema field |
| `transit_capacity_weight` | Remove from schema — subsumed into TAI layer formula inputs |
| `local_poi_density` | Remove — no standalone equivalent; replaced by specific `poi_reach_*_min` values |
| `transit_shed_poi_count` | Remove — replaced by structured poi_reach fields |
| `percentile_rank` | Keep as derived stat for display only (not stored in schema) |

---

## Component Inventory

### app/

| File | Purpose | Uses real data? | Migration effort |
|------|---------|-----------------|-----------------|
| `app/page.tsx` | Root page — assembles map + overlay phases | No (phase-based) | Low — no data deps |
| `app/layout.tsx` | Root layout, global CSS | No | None |
| `app/globals.css` | Global Tailwind styles | No | None |
| `app/methodology/` | Methodology explainer page | No | None |
| `app/api/analyze/route.ts` | POST — streams AI equity analysis via OpenRouter | Reads HexProperties fields | Medium — field renames needed |
| `app/api/pois/route.ts` | GET — proxies Overpass API for live POI fetch | Live Overpass data | Low — no schema dep |
| `app/api/geocode/route.ts` | GET — proxies Nominatim forward geocoding | No schema dep | None |

### components/

| File | Purpose | Uses real data? | Migration effort |
|------|---------|-----------------|-----------------|
| `components/AccessibilityMap.tsx` | Core map — DeckGL + MapLibre, renders all layers | Yes — loads GeoJSON files from `/public/data/` | **High** — loads legacy GeoJSON, all field refs need updating |
| `components/MapLegend.tsx` | Map legend for hex layer color scale | Partial — reads quadrant colors | Low — update quadrant labels |
| `components/ResultsLayout.tsx` | Right-side panel shell | Store only | Low — no schema deps |
| `components/landing/LandingOverlay.tsx` | Search bar landing screen | No | None |
| `components/landing/SearchBar.tsx` | Geocode search input | API only | None |
| `components/loading/LoadingSequence.tsx` | Animated loading stages | Store phase | None |
| `components/ui/GlassPanel.tsx` | Frosted-glass wrapper panel | No | None |
| `components/results/CardGrid.tsx` | Orchestrates result card layout | No (delegates) | None |
| `components/results/TransitScoreCard.tsx` | Displays TAI score, quadrant, need/access bars, score breakdown | Yes — all HexProperties fields | **High** — field renames + scale change (0–100 → 0–1), new 5-layer breakdown needed |
| `components/results/DemographicsCard.tsx` | Demographics display | Yes — Demographics object | Medium — field renames |
| `components/results/POIAccessCard.tsx` | "What can you reach?" POI list | Yes — reachablePOIs | Medium — remove threshold model; show travel-time values |
| `components/results/TransitLinesCard.tsx` | Nearby transit stops list | Yes — nearbyTransitStops | Low — stop data format compatible |
| `components/results/AIAnalysisCard.tsx` | AI narrative equity analysis | Yes — calls /api/analyze | Medium — field renames in request body |
| `components/results/ScoreCircle.tsx` | SVG score circle visualization | Numeric score prop | Medium — scale from 0–100 to 0–1 (or multiply × 100 for display) |

### hooks/

| File | Purpose | Uses real data? | Migration effort |
|------|---------|-----------------|-----------------|
| `hooks/useReachablePOIs.ts` | Computes reachable POIs; fetches live from Overpass | Threshold-based model | Medium — logic changes: threshold model → show stored travel-time values from `poi_reach_*_min` |
| `hooks/useTransitStops.ts` | Fetches nearby transit stops from GeoJSON | Yes | Low — stop schema compatible |
| `hooks/useDemographics.ts` | Loads demographics JSON, looks up by H3 | Yes | Medium — field renames |
| `hooks/useAISummary.ts` | Triggers AI analysis call | Store-dependent | Medium — field renames in call |

### lib/

| File | Purpose | Uses real data? | Migration effort |
|------|---------|-----------------|-----------------|
| `lib/store.ts` | Zustand state (HexProperties, Demographics, all app state) | Schema definition | **High** — HexProperties and Demographics interfaces need full rewrite |
| `lib/colorScale.ts` | Color scale helpers for quadrant/score display | Quadrant enum | Low — update enum values |
| `lib/osrmRoute.ts` | Fetches walking routes via OSRM | No schema dep | None |
| `lib/poiUtils.ts` | Filters/sorts POIs by distance and threshold | Threshold model | Medium — adapt to stored travel-time values |

---

## Store Audit

### Current Zustand state shape vs. required shape

**Compatible (keep as-is or minor rename):**
- `appPhase`, `loadingStage`, `searchQuery`, `locationName` — UI state, no schema dep
- `clickedCoordinate`, `selectedHex`, `mapStats` — structural pattern is correct
- `h3Resolution` (7 | 8 — note: DATA_MODEL.md uses only res 8; res 7 not in schema)
- `boundaryMode` ("kelurahan" | "kecamatan" | "hex") — compatible with schema's dual-resolution design
- `allPOIs`, `reachablePOIs`, `selectedPOI` — structure compatible; category list needs expanding
- `allTransitStops`, `nearbyTransitStops`, `selectedTransitStop` — compatible
- `aiSummary`, `aiLoading`, `aiError` — no schema dep
- `threshold` (30 | 60) — no longer needed in new model (replaced by stored `poi_reach_*_min` values); can be deprecated or repurposed

**Needs significant changes:**

| Current | Required change |
|---------|-----------------|
| `HexProperties.composite_score` | Remove |
| `HexProperties.score_30min / score_60min` | Remove |
| `HexProperties.*_30min / *_60min` (12 POI count fields) | Remove; add `poi_reach_*_min` (6 fields) |
| `HexProperties.transit_need_score` (0–100) | Rename to `tni_score`, normalize to [0,1] |
| `HexProperties.transit_accessibility_score` (0–100) | Rename to `tai_score`, normalize to [0,1] |
| `HexProperties.equity_gap` (0–100 range) | Keep name; normalize to [-1,1] |
| `HexProperties.quadrant` (string labels) | Change to enum `Q1\|Q2\|Q3\|Q4` |
| `HexProperties.dist_to_transit` (km) | Rename to `min_dist_to_transit_m` (meters) |
| `HexProperties` — missing all TAI layer fields | Add: `n_transit_stops`, `n_transit_routes`, `avg_headway_min`, `transit_mode_diversity`, `best_mode_fare_tier`, `has_affordable_mode`, `road_adjusted_access`, all `poi_reach_*_min`, all `gc_*_idr`, all `tcr_*`, `transit_competitive_zone` |
| `HexProperties` — missing road network fields | Add: `road_length_km`, `road_density_km_per_km2`, `pct_*` road fields, `avg_road_class_score`, `network_connectivity` |
| `Demographics.kelurahan` | Rename to `kelurahan_name` |
| `Demographics.kecamatan` | Rename to `kecamatan_name` |
| `Demographics.city_code` | Rename to `kota_kab_name` |
| `Demographics.total_population` | Rename to `population` |
| `Demographics.population_density` | Rename to `pop_density` |
| `Demographics.pct_dependent` | Rename to `dependency_ratio` |
| `Demographics.pct_zero_vehicle` | Rename to `zero_vehicle_hh_pct` |
| `Demographics` — missing fields | Add: `poverty_rate`, `avg_household_expenditure`, `kelurahan_id`, `area_km2` |
| `MapStats` | Recalculate: `avg_score`/`median_score` → based on `tai_score`; add Gini coefficient fields |
| `h3Resolution: 7 \| 8` | Keep; note res 7 is not in DATA_MODEL.md schema — confirm with product spec |

**New state to add:**
- `selectedPersona` ('commuter' | 'explorer' | 'researcher' | 'planner' | null) — per MVP-90

---

## API Routes

| Route | Method | Purpose | External dependency | Schema-coupled? |
|-------|--------|---------|--------------------|--------------|
| `/api/analyze` | POST | AI equity narrative via OpenRouter | OpenRouter API | Yes — sends HexProperties fields in prompt |
| `/api/pois` | GET | Live POI fetch proxy | Overpass API | No |
| `/api/geocode` | GET | Forward geocoding proxy | Nominatim | No |

No route handlers exist for: data serving (all served as static GeoJSON from `/public/data/`), H3 computation, or transit routing. The pipeline outputs are served as static files.

---

## Public Data Files

| File | Current state | Migration action |
|------|--------------|-----------------|
| `jakarta_h3_scores.geojson` | Synthetic — legacy schema (~9,000 H3 res 8 cells) | Replace with real pipeline output; rename fields to DATA_MODEL.md schema |
| `jakarta_h3_scores_res7.geojson` | Synthetic — res 7 (not in DATA_MODEL.md) | Evaluate: keep if dual-res product feature retained, otherwise remove |
| `jakarta_kelurahan_boundaries.geojson` | Synthetic | Replace with real GADM/Geoportal boundaries + all kelurahan-level computed fields |
| `jakarta_kecamatan_boundaries.geojson` | Synthetic | Replace with real boundaries |
| `jakarta_demographics.json` | Synthetic — legacy Demographics schema | Replace with real BPS data; rename to DATA_MODEL.md field names |
| `jakarta_transit_stops.geojson` | Synthetic | Replace with real unified GTFS stops (all 4 modes) |
| `jakarta_transit_routes.geojson` | Synthetic | Replace with real GTFS route geometries |
| `jakarta_pois.geojson` | Pre-loaded from Overpass (12 categories) | Align categories with DATA_MODEL.md POI types (hospital, school, market, industrial, govoffice, CBD) |

**Missing public data files** (required by new schema):
- `jakarta_road_network.geojson` — road segments with highway class (Layer 1 + MVP-28)
- `jakarta_cbd_zones.geojson` — CBD polygon definitions (Sudirman–Thamrin zone + secondary CBDs)

---

## Migration Plan (for MVP-27)

Ordered steps from synthetic prototype to real pipeline output:

1. **Update `lib/store.ts` — HexProperties interface**
   Rewrite to DATA_MODEL.md schema. Remove legacy fields. Add all new fields. Change quadrant to `Q1|Q2|Q3|Q4`. Change score scales to [0,1]. This is the blocking step — every downstream component depends on it.

2. **Update `lib/store.ts` — Demographics interface**
   Rename fields to match DATA_MODEL.md. Add `kelurahan_id`, `poverty_rate`, `avg_household_expenditure`, `area_km2`.

3. **Update `lib/colorScale.ts`**
   Update quadrant color mapping to use Q1–Q4 keys. Update score normalization to [0,1] scale.

4. **Run `export_to_web.py`** (Python pipeline side)
   Export real pipeline outputs with new field names to `web/public/data/`. Produce the missing road network and CBD zone files.

5. **Replace GeoJSON files in `web/public/data/`**
   Swap all 8 synthetic files with real pipeline outputs. Verify field name alignment with updated `HexProperties` and `Demographics` interfaces.

6. **Update `AccessibilityMap.tsx`**
   Update all field references (`transit_accessibility_score` → `tai_score`, etc.). Update quadrant color lookup. Add road network layer (if `jakarta_road_network.geojson` is available). Update tooltip field display.

7. **Update `TransitScoreCard.tsx`**
   Replace 2-component breakdown (need + access) with 5-layer TAI breakdown (L1–L5). Update field references. Update score display from 0–100 to 0–1 (or multiply × 100 for display — decide once). Update quadrant label display from string labels to Q1–Q4 with descriptions.

8. **Update `DemographicsCard.tsx`**
   Rename field references to match new Demographics interface.

9. **Update `POIAccessCard.tsx` and `hooks/useReachablePOIs.ts`**
   Remove threshold-based POI count model. Show stored `poi_reach_*_min` travel-time values from HexProperties instead of live-computed reachable list. The live Overpass fetch for location-specific POIs can be retained as supplementary.

10. **Update `hooks/useDemographics.ts`**
    Update field lookups and joins to use `kelurahan_id` as key.

11. **Update `/api/analyze` route.ts**
    Update `AnalyzeRequest` interface and prompt builder to use new field names and include L1–L5 breakdown data.

12. **Verify `ScoreCircle.tsx`**
    Confirm score input range — if scores stored as [0,1], pass `score × 100` for display or update the component to accept [0,1] directly.

13. **Add `selectedPersona` to Zustand store** (MVP-90 dependency)

14. **Smoke test**: Load app with real data, verify: map renders, hex click shows real TAI/TNI values, quadrant classification correct, Demographics card shows real BPS data.

---

## Verdict

**The prototype is a solid architectural base, but requires significant schema surgery before it can accept real pipeline output.**

Strengths:
- DeckGL + MapLibre stack is correct for the product requirements
- Dual-resolution toggle (hex / kelurahan / kecamatan) is already wired
- Zustand store architecture is clean and well-structured
- API routes for geocoding and POI are production-ready (no changes needed)
- AI analysis card and OpenRouter integration are working
- Component decomposition is appropriate (cards, hooks, lib separation)

Gaps:
- The entire scoring model is legacy (POI-count-by-threshold) vs. required (r5py travel-time + 5-layer TAI formula). This is a fundamental data model difference, not just field renames.
- 12 legacy POI count fields (`*_30min/*_60min`) must be removed and replaced with 6 `poi_reach_*_min` travel-time fields — this changes the `POIAccessCard` and `useReachablePOIs` logic significantly.
- All TAI layer component fields (L1–L5) are absent from the store and GeoJSON.
- All generalized cost / transit competitive zone fields (Layer 5) are absent — blocks MVP-28 and MVP-32.
- Road network fields absent — blocks road layer (MVP-28).
- Score scale mismatch (0–100 vs [0,1]) affects `TransitScoreCard`, `ScoreCircle`, `MapStats`, and `colorScale`.
- Quadrant enum format change (string label → Q1–Q4) touches every component that reads `quadrant`.

**Migration effort: Large.**
The architecture does not need rebuilding, but the data model touches every component. The critical path is: (1) rewrite `lib/store.ts` types, (2) replace GeoJSON files with real pipeline output, (3) update all field references in components. Steps 1 and 2 are blockers for everything else. Estimated ~3–5 days of focused migration work after pipeline outputs are ready (MVP-23–25).
