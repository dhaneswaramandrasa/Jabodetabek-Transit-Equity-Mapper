# Product Requirements Document
## Jabodetabek Transit Equity Mapper

**Last updated**: 2026-03-20
**Status**: Final (E0-008)
**Source**: `docs/research-framing.md`, `docs/methodology.md`, `docs/DATA_MODEL.md`, `docs/source-map.md`

---

## 1. Overview

An interactive web-based map tool that diagnoses transit equity gaps across the Jabodetabek metropolitan region (Jakarta + Bogor, Depok, Tangerang, Bekasi). The product visualizes where public transit accessibility fails to match socioeconomic need, using a 5-layer Transit Accessibility Index (TAI) and a Transit Need Index (TNI) at both administrative (kelurahan) and hexagonal (H3 resolution 8) spatial resolutions.

It is the deployed companion to a research paper analyzing the same data and methodology. Both outputs share the same scoring engine, data pipeline, and analytical framework defined in `docs/methodology.md`.

---

## 2. Problem Statement

Over 30 million people live in Jabodetabek. Millions of lower-to-middle-income suburban commuters depend on expensive, polluting private vehicles because transit service is concentrated in central Jakarta. Regional planning is fragmented across multiple municipal governments (DKI Jakarta, Kota/Kab Bogor, Depok, Tangerang, Bekasi) with no shared, granular, evidence-based tool to diagnose where transit investment is most urgently needed.

The product answers: **"Where should the next bus route or station go to reduce transit poverty the most?"** — backed by spatial data, not intuition.

---

## 3. Background

### 3.1 Research Context

Transit equity research in developing countries has grown significantly (Delmelle & Casas 2012; Pereira et al. 2019; Rathod et al. 2025), but four specific gaps persist that this project addresses:

1. **No composite need-vs-access equity framework for full Jabodetabek.** Existing Jakarta studies (Hardi & Murad 2023; Taki et al. 2018) cover only DKI Jakarta and do not construct a TNI–TAI gap framework spanning the full metropolitan region including the suburban Bodetabek ring where transit poverty is most severe.

2. **No dual-resolution comparison exposing MAUP in equity scoring.** Javanmard et al. (2023) demonstrate that MAUP significantly affects transit equity conclusions, but no study has compared the same equity gap framework at administrative (kelurahan) vs. uniform hexagonal (H3) resolutions in a single metropolitan area.

3. **No what-if scenario simulation embedded in an equity quadrant framework.** No study embeds counterfactual infrastructure placement directly into a transit equity quadrant classification to measure the shift in equity scores — making the analysis actionable rather than purely descriptive.

4. **No three-way generalized cost model for equity analysis.** Western transit equity studies compare transit against car only. In Jabodetabek and Southeast Asia broadly, the motorcycle is often the marginal competitor to transit (Ng 2018; Sukor & Bhayo 2024). No existing framework computes a three-way generalized cost comparison (transit vs. car vs. motorcycle) and integrates it as a cost-competitiveness layer within a composite accessibility index.

### 3.2 Two Outputs

| Output | Description | Audience |
|--------|-------------|----------|
| **Research paper** | Thesis chapter or journal article: dual-resolution transit equity gap methodology + Jabodetabek findings | Academic (thesis committee, reviewers) |
| **Web product** | Interactive map tool: quadrant classification, equity scores, what-if simulator, cost competitiveness maps | Planners, NGOs, operators, developers, public |

### 3.3 Research Question

> To what extent does the spatial distribution of public transit accessibility in the Jabodetabek metropolitan region align with the socioeconomic transit need of its population, and how does this alignment differ when measured at administrative (kelurahan) versus uniform hexagonal (H3) spatial resolutions?

### 3.4 Hypotheses the Product Must Support

| ID | Hypothesis | Product feature that enables testing |
|----|-----------|--------------------------------------|
| H1 | High Need / Low Access areas concentrate in suburban Bodetabek; Low Need / High Access clusters in central Jakarta | Quadrant Equity Map (5.1) |
| H2 | Kelurahan-level analysis underestimates equity gaps in heterogeneous suburban areas vs. H3 | Dual-Resolution Toggle (5.2) |
| H3 | Adding a station in Q4 produces larger equity improvement than in Q2 | What-If Simulator (5.5) |

---

## 4. User Personas

### 4.1 Rina — Government Planner
- **Role**: Dishub / Bappeda transport planner
- **Primary goal**: Justify budget allocation for new transit routes in underserved areas
- **Key need**: Quadrant map showing "High Need, Low Access" zones with downloadable data and what-if scenarios to support proposals
- **Technical level**: Moderate — familiar with GIS, expects data export
- **Key features**: Quadrant Map, Transit Competitive Zones, What-If Simulator, Data Download

### 4.2 Adi — NGO Researcher
- **Role**: ITDP Indonesia / NGO transit equity researcher
- **Primary goal**: Produce evidence-based transit equity reports for advocacy
- **Key need**: Gini coefficients, LISA cluster maps, resolution comparison, exportable figures and datasets
- **Technical level**: High — runs own analyses, needs raw data
- **Key features**: Dual-Resolution Toggle, Data Download, POI Accessibility Heatmaps

### 4.3 Budi — Transit Operations Manager
- **Role**: TransJakarta / KAI Commuter operations planning
- **Primary goal**: Identify where new feeder routes would have the highest ridership potential
- **Key need**: What-if simulator with catchment visualization and first-mile quality indicators
- **Technical level**: Moderate — uses dashboards, not GIS
- **Key features**: What-If Simulator, CBD Journey Chain, Road Network Layer

### 4.4 Sari — Student / General Public
- **Role**: Graduate student or curious citizen
- **Primary goal**: Understand how transit equity varies across Jabodetabek
- **Key need**: Simple, intuitive map with clear color coding and click-to-explore detail panels
- **Technical level**: Low — expects consumer-grade UX
- **Key features**: Quadrant Map, POI Accessibility Heatmaps

---

## 5. Features

### 5.1 Quadrant Equity Map (Primary View)
- **Description**: Choropleth map classifying every spatial unit into Q1 (Well-Served), Q2 (Low Need, High Access), Q3 (Low Priority), Q4 (Transit Desert) based on TNI and TAI scores
- **User story**: As Rina, I want to see which kelurahan are transit deserts so that I can prioritize them in budget planning
- **Methodology link**: TNI (5 indicators, equal weighting) vs. TAI (5-layer model) → equity_gap = tni_score − tai_score → quadrant classification
- **Acceptance criteria**:
  - [ ] 4-color quadrant choropleth at kelurahan level
  - [ ] Click any unit → detail panel showing:
    - TNI score + 5 indicator values (pop_density, poverty_rate, avg_household_expenditure, zero_vehicle_hh_pct, dependency_ratio)
    - TAI score + 5-layer breakdown (L1 first-mile, L2 service quality, L3 CBD journey chain, L4 last-mile, L5 cost competitiveness)
    - Equity gap score and quadrant label
  - [ ] Color legend with quadrant descriptions
  - [ ] Summary stats bar: % units and % population per quadrant

### 5.2 Dual-Resolution Toggle
- **Description**: Switch between kelurahan (~1,800 units) and H3 resolution 8 (~15,000–20,000 hexagons) to reveal how spatial resolution affects equity classification
- **User story**: As Adi, I want to compare kelurahan vs H3 classification so that I can demonstrate the MAUP effect in my report
- **Methodology link**: H3 derivation via 4 methods (dasymetric for socioeconomic, spatial clip for roads, point-in-polygon for stops, direct r5py for travel times)
- **Acceptance criteria**:
  - [ ] Smooth toggle between kelurahan polygons and H3 hexagons
  - [ ] Summary stats (% units per quadrant, Gini coefficient) update per resolution
  - [ ] Resolution comparison panel showing count of reclassified units between resolutions
  - [ ] Visual highlight of areas that change quadrant between resolutions

### 5.3 CBD Journey Chain Visualization
- **Description**: On click, show the optimal multi-modal transit journey from the selected unit to Sudirman–Thamrin CBD zone
- **User story**: As Budi, I want to see the full journey chain so that I can identify where transfers or first-mile gaps hurt commuters
- **Methodology link**: TAI Layer 3 (CBD journey chain) computed via r5py with gravity-weighted travel time to 9 CBD zones
- **Acceptance criteria**:
  - [ ] Journey legs displayed: first-mile walk → station → ride → transfer → ride → last-mile walk
  - [ ] Each leg shows mode, time (minutes), fare (IDR)
  - [ ] Path rendered on map as polyline with mode-colored segments
  - [ ] Side panel compares three-way generalized cost: transit vs car vs motorcycle
  - [ ] Transit competitive zone badge shown (transit_wins / swing / private_wins / transit_not_available)

### 5.4 Transit Competitive Zone Map
- **Description**: Choropleth showing where transit beats private transport in generalized cost, using the three-way GC model (transit vs. car vs. motorcycle)
- **User story**: As Rina, I want to see the transit competitive zones so that I know where transit investment would shift mode choice
- **Methodology link**: Layer 5 cost competitiveness — GC formulas with VOT Rp 500/min, car fuel Rp 1,000/km, motorcycle fuel Rp 200/km, fatigue brackets, tolls, parking
- **Acceptance criteria**:
  - [ ] Three-color choropleth: green (transit_wins, TCR > 1.2), amber (swing, 0.8–1.2), red (private_wins, TCR < 0.8), grey (transit_not_available)
  - [ ] Toggle between tcr_vs_car / tcr_vs_motorcycle / tcr_combined views
  - [ ] Click shows full GC breakdown: fare, fuel, toll, parking, VOT, discomfort, fatigue for each mode
  - [ ] Distance-to-CBD concentric ring overlay (5km, 10km, 15km, 20km, 30km)
  - [ ] Summary: % population in each competitive zone

### 5.5 What-If Station Placement Simulator
- **Description**: User places a hypothetical transit station on the map and sees the equity impact on surrounding spatial units
- **User story**: As Budi, I want to simulate adding a feeder route so that I can estimate equity improvement before proposing it
- **Methodology link**: Recomputes TAI Layer 1 (first-mile) and Layer 2 (service quality) within catchment radius; recalculates equity gap and quadrant
- **Acceptance criteria**:
  - [ ] Click map to place hypothetical station
  - [ ] Select mode type (KRL / MRT / BRT / Mikrotrans)
  - [ ] Configurable catchment radius: 1km walk, 3km feeder
  - [ ] Before/after comparison: quadrant changes, Gini delta, affected population count
  - [ ] Clearly labeled as **"scenario simulation, not prediction"**
  - [ ] Reset button to clear all hypothetical stations

### 5.6 Road Network Layer
- **Description**: Toggleable road network overlay color-coded by highway classification, with road quality indicators per spatial unit
- **User story**: As Budi, I want to see road network quality around transit stops so that I understand first-mile walkability constraints
- **Methodology link**: Road network indicators from OSM — road_density, pct_footway_pedestrian, network_connectivity feed into TAI Layer 1
- **Acceptance criteria**:
  - [ ] Road segments rendered via deck.gl layer, color-coded by highway class (primary/secondary/tertiary/residential/footway)
  - [ ] Toggleable on/off
  - [ ] Road quality summary in detail panel: road_density_km_per_km2, pct_footway_pedestrian, network_connectivity

### 5.7 POI Accessibility Heatmaps
- **Description**: Travel-time heatmaps to key POI categories computed via r5py
- **User story**: As Sari, I want to see how long it takes to reach a hospital by transit from my area
- **Methodology link**: TAI Layer 3 sub-indicators — poi_reach_cbd_min, poi_reach_hospital_min, poi_reach_school_min, poi_reach_market_min, poi_reach_industrial_min, poi_reach_govoffice_min
- **Acceptance criteria**:
  - [ ] Dropdown to select POI category (CBD, hospital, school, market, industrial zone, government office)
  - [ ] Continuous color scale (green < 30min, yellow 30–60min, red > 60min)
  - [ ] Both resolutions supported (kelurahan and H3)

### 5.8 Equity Summary Dashboard
- **Description**: Summary statistics panel showing key equity metrics across the study area
- **User story**: As Adi, I want to see headline equity metrics so that I can cite them in reports
- **Acceptance criteria**:
  - [ ] Gini coefficient (TAI distribution) at both resolutions
  - [ ] Population count per quadrant (bar chart)
  - [ ] Top 10 / bottom 10 kelurahan by equity gap
  - [ ] LISA cluster count (High-High, Low-Low, High-Low, Low-High)

### 5.9 Data Download
- **Description**: Cleaned dataset available for public download under CC BY 4.0
- **User story**: As Adi, I want to download the raw equity scores so that I can run my own analysis
- **Acceptance criteria**:
  - [ ] `public/dataset/` contains:
    - `kelurahan_scores.geojson` — all DATA_MODEL.md kelurahan fields
    - `h3_scores.geojson` — all DATA_MODEL.md H3 fields
    - `transit_stops.geojson` — unified stops with mode tags
    - `cbd_zones.geojson` — 9 CBD zone polygons
  - [ ] README with field glossary, source citations, methodology summary
  - [ ] License: CC BY 4.0
  - [ ] Download button in UI footer

---

## 6. Data Sources

All data sources verified in MVP-6 (E0-007). See `src/ingestion/VERIFICATION_REPORT.md`.

| # | Dataset | Format | Status | Notes |
|---|---------|--------|--------|-------|
| 1 | TransJakarta BRT GTFS | GTFS ZIP | Accessible | Mobility Database, last updated 2026-03-14 |
| 2 | KRL Commuterline GTFS | GTFS ZIP | **Must construct** | No published feed — build from comuline/api (MVP-39) |
| 3 | MRT Jakarta GTFS | GTFS ZIP | **Must construct** | No published feed — build from mrt-jakarta-api (MVP-39) |
| 4 | LRT Jabodebek stations | Manual GeoJSON | Compiled | 18 stations from Wikipedia/official sources |
| 5 | OSM road network | PBF → GeoDataFrame | Accessible | Geofabrik Java extract |
| 6 | POIs | GeoJSON | Accessible | Overpass API, 6 strict categories |
| 7 | Admin boundaries | GeoJSON | Accessible | GADM level 4 (kelurahan) + HDX/BPS shapefile |
| 8 | BPS demographic data | CSV / tables | Manual | 9 regional BPS websites, kecamatan level |
| 9 | WorldPop population raster | GeoTIFF | Accessible | WorldPop Indonesia 2020, ~100m resolution |
| 10 | H3 hexagonal grid | Generated | N/A | h3-py resolution 8 |

---

## 7. Technical Constraints

| Constraint | Details |
|-----------|---------|
| No API keys client-side | All data pre-computed server-side; static GeoJSON served from `public/` |
| GeoJSON budget | Total GeoJSON < 15 MB for acceptable load times |
| Static GTFS only | Schedule-based analysis (no GTFS-RT) |
| No informal transit | Angkot/ojek excluded due to data gaps |
| Cross-sectional snapshot | Single time period, no longitudinal trends |
| Scenario disclaimer | What-if simulator is indicative, not predictive — UI must clearly label |
| KRL/MRT GTFS gap | Feeds must be manually constructed before pipeline runs (MVP-39) |
| BPS manual collection | Demographic data from 9 BPS websites, kecamatan granularity |
| Component size limit | < 150 lines per component; wrangling in `lib/` only |
| Type safety | No `any`; all props typed against `docs/DATA_MODEL.md` |

---

## 8. Non-Functional Requirements

| Requirement | Target |
|------------|--------|
| Initial page load | < 5 seconds on broadband |
| Map interaction (click, pan, zoom) | < 1 second response |
| GeoJSON total size | < 15 MB |
| Browser support | Chrome, Firefox, Safari (latest 2 versions) |
| Mobile responsive | Map and panels usable on tablet; degraded on phone |
| Accessibility | Semantic HTML, keyboard navigation for panels, color-blind safe palette |
| Deployment | Vercel (free tier) |

---

## 9. Out of Scope

- Informal transport (ojek, non-app ride-hailing)
- Real-time transit data (GTFS-RT)
- Causal inference on transit investment outcomes
- Fare optimization or pricing analysis
- Historical time-series analysis
- Mobile app development — web-only
- User accounts or saved sessions
- Real-time traffic integration (v2 extension — `avg_traffic_speed_kmh`, `peak_congestion_index` fields reserved in DATA_MODEL.md)
- Angkot route integration (data quality insufficient)

---

## 10. Success Criteria

| Criterion | Measure |
|-----------|---------|
| Research question answerable from UI | User can identify Q4 transit deserts, compare resolutions, and run what-if scenarios |
| All 3 hypotheses testable | H1 via quadrant map, H2 via resolution toggle, H3 via what-if simulator |
| Data integrity | `lib/types.ts` = `docs/DATA_MODEL.md` = `lib/mock-data.ts` — all three match |
| Methodology fidelity | Product computes TAI/TNI/GC exactly as `docs/methodology.md` specifies |
| Public dataset | CC BY 4.0 dataset downloadable independently of the app |
| Academic-product convergence | Paper figures can be reproduced from product views |
