# Product Requirements Document
## Jabodetabek Transit Equity Mapper

**Last updated**: 2026-03-16
**Source**: `docs/research-framing.md` (Phase 1.2)

---

## 1. Overview

An interactive web-based map tool that diagnoses transit equity gaps across the Jabodetabek metropolitan region (Jakarta + Bogor, Depok, Tangerang, Bekasi). The product visualizes where public transit accessibility fails to match socioeconomic need, at both administrative (kelurahan) and hexagonal (H3) spatial resolutions. It is the deployed companion to a research paper analyzing the same data.

## 2. Problem Statement

Over 30 million people live in Jabodetabek. Millions of lower-to-middle-income suburban commuters depend on expensive, polluting private vehicles because transit service is concentrated in central Jakarta. Regional planning is fragmented across multiple municipal governments (DKI Jakarta, Kota/Kab Bogor, Depok, Tangerang, Bekasi) with no shared, granular, evidence-based tool to diagnose where transit investment is most urgently needed.

The product answers: **"Where should the next bus route or station go to reduce transit poverty the most?"** — backed by spatial data, not intuition.

## 3. Background

### 3.1 Research Context

Transit equity research in developing countries has grown (Delmelle & Casas 2012 on Cali; Accra study 2024; Belo Horizonte equity-quality tradeoff 2025), but three gaps persist:

1. **Jabodetabek is under-studied at the equity-gap level.** Existing Jakarta transit research focuses on BRT accessibility and TOD potential, but does not construct a composite need-vs-access gap framework spanning the full metropolitan region.
2. **Dual-resolution spatial analysis is rare.** Most studies use a single spatial unit. No study systematically compares how the same need-access gap manifests at two resolutions (kelurahan vs. H3) in the same metro area.
3. **"What-if" scenario simulation is disconnected from equity frameworks.** Few studies embed counterfactual infrastructure placement into a transit equity quadrant framework.

### 3.2 Two Outputs

| Output | Description | Audience |
|--------|-------------|----------|
| **Research paper** | Thesis chapter or journal article: dual-resolution transit equity gap methodology + Jabodetabek findings | Academic |
| **Web product** | Interactive map tool: quadrant classification, equity scores, what-if simulator, accessibility heatmaps | Planners, NGOs, operators, public |

## 4. User Personas

| Persona | Role | Primary Goal | Key Need |
|---------|------|-------------|----------|
| **Rina** | Dishub / Bappeda planner | Justify budget allocation for new transit routes in underserved areas | Quadrant map showing "High Need, Low Access" zones with downloadable data |
| **Adi** | ITDP / NGO researcher | Produce evidence-based transit equity reports for advocacy | Gini coefficients, LISA cluster maps, resolution comparison, exportable figures |
| **Budi** | TransJakarta / KAI operations manager | Identify where new feeder routes would have the highest ridership potential | What-if simulator + first-mile quality indicators |
| **Sari** | Graduate student / general public | Understand how transit equity varies across Jabodetabek | Simple quadrant map with clear color coding and click-to-explore detail panels |

## 5. Features

### 5.1 Quadrant Equity Map (Primary View)
- **Description**: Choropleth map classifying every spatial unit into Q1 (Well-Served), Q2 (Low Need, High Access), Q3 (Low Priority), Q4 (Transit Desert)
- **User story**: As Rina, I want to see which kelurahan are transit deserts so that I can prioritize them in budget planning
- **Acceptance criteria**:
  - [ ] 4-color quadrant choropleth at kelurahan level
  - [ ] Toggle to H3 hexagonal resolution
  - [ ] Click any unit → detail panel with TNI, TAI, 5-layer breakdown, equity gap
  - [ ] Color legend with quadrant descriptions

### 5.2 Dual-Resolution Toggle
- **Description**: Switch between kelurahan and H3 views to reveal how resolution affects equity classification
- **User story**: As Adi, I want to compare kelurahan vs H3 classification so that I can demonstrate the MAUP effect in my report
- **Acceptance criteria**:
  - [ ] Smooth toggle between kelurahan and H3 layers
  - [ ] Summary stats (% units per quadrant) update per resolution
  - [ ] Resolution comparison panel showing reclassified units

### 5.3 CBD Journey Chain Visualization
- **Description**: On click, show the optimal multi-modal transit journey from selected unit to Sudirman–Thamrin CBD
- **User story**: As Budi, I want to see the full journey chain so that I can identify where transfers or first-mile gaps hurt commuters
- **Acceptance criteria**:
  - [ ] Journey legs displayed: first-mile → station → ride → transfer → ride → last-mile
  - [ ] Each leg shows mode, time, fare
  - [ ] Path rendered on map as polyline
  - [ ] Side panel compares transit vs car vs motorcycle generalized cost

### 5.4 Transit Competitive Zone Map
- **Description**: Choropleth showing where transit beats private transport (car and motorcycle) in generalized cost
- **User story**: As Rina, I want to see the transit competitive zones so that I know where transit investment would shift mode choice
- **Acceptance criteria**:
  - [ ] Three-color map: green (transit wins), amber (swing), red (private wins)
  - [ ] Toggle between TCR_vs_car / TCR_vs_motorcycle / TCR_combined
  - [ ] Click shows full GC breakdown
  - [ ] Distance-to-CBD ring overlay

### 5.5 What-If Station Placement Simulator
- **Description**: User places a hypothetical transit station on the map and sees equity impact
- **User story**: As Budi, I want to simulate adding a feeder route so that I can estimate equity improvement
- **Acceptance criteria**:
  - [ ] Click map to place hypothetical station
  - [ ] Select mode type (KRL/MRT/BRT/Mikrotrans)
  - [ ] Configurable catchment radius (1km walk, 3km feeder)
  - [ ] Before/after: quadrant changes, Gini delta
  - [ ] Clearly labeled as "scenario simulation, not prediction"

### 5.6 POI Accessibility Heatmaps
- **Description**: Travel-time heatmaps to key POI categories (CBD, hospital, school, market, industrial, government)
- **User story**: As Sari, I want to see how long it takes to reach a hospital by transit from my area
- **Acceptance criteria**:
  - [ ] Dropdown to select POI category
  - [ ] Continuous color scale (green = short, red = long)
  - [ ] Both resolutions supported

### 5.7 Data Download
- **Description**: Cleaned dataset available for public download
- **User story**: As Adi, I want to download the raw equity scores so that I can run my own analysis
- **Acceptance criteria**:
  - [ ] `public/dataset/` contains kelurahan_scores.geojson, h3_scores.geojson, cbd_zones.geojson
  - [ ] README with field glossary and methodology summary
  - [ ] License: CC BY 4.0

## 6. Constraints

| Constraint | Details |
|-----------|---------|
| No API keys client-side | All data pre-computed; no server-side API calls in v1 |
| GeoJSON budget | Total GeoJSON < 15 MB for acceptable load times |
| Static GTFS | Schedule-based, not real-time |
| No informal transit | Angkot/ojek excluded due to data gaps |
| Cross-sectional | Single time snapshot, no longitudinal trends |
| Scenario disclaimer | What-if simulator is indicative, not predictive |

## 7. Out of Scope

- Informal transport (ojek, non-app ride-hailing)
- Real-time transit data (GTFS-RT)
- Causal inference on transit investment outcomes
- Fare optimization or pricing analysis
- Historical time-series analysis
- Mobile app development — web-only
- User accounts or saved sessions
- Real-time traffic integration (v2 enhancement)
