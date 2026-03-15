# RESEARCH FRAMING
## Jabodetabek Transit Equity Mapper
### A Dual-Resolution Spatial Diagnostic for Transit Need-Access Gaps

| Field              | Details                                                  |
|--------------------|----------------------------------------------------------|
| Researcher         | Dhanes                                                   |
| Program            | Master of Smart Society, Hiroshima University             |
| Supervisor         | TBD                                                      |
| Target Venue       | TBD — keeping options open (thesis chapter / journal / conference) |
| Prototype Audience | Government planners (Dishub, Bappeda, BPTJ), NGOs (ITDP), transport operators (TransJakarta, Gojek/Grab), real estate developers, general public |
| Status             | **Draft** — awaiting literature scan (Phase 1.3)         |

---

## Research Question

**Draft RQ**: To what extent does the spatial distribution of public transit accessibility in the Jabodetabek metropolitan region align with the socioeconomic transit need of its population, and how does the measurement of this alignment differ when analyzed at administrative (kelurahan) versus uniform hexagonal (H3) spatial resolutions?

## Hypothesis

**H1**: Areas classified as "High Need, Low Access" are disproportionately concentrated in the suburban peripheries of Bodetabek (Bogor, Depok, Tangerang, Bekasi), while "Low Need, High Access" areas cluster in central Jakarta — and this pattern is more clearly detected at H3 resolution than at kelurahan level due to reduced aggregation bias.

**H2** (secondary): Simulating the placement of a single new transit node (station or route) in a "High Need, Low Access" zone produces a measurably larger equity score improvement than the same intervention in a "Low Need, High Access" zone — validating the quadrant framework as a prioritization tool.

---

## Why This Matters

### Academic contribution

Transit equity research in developing countries has grown significantly (Delmelle & Casas 2012 on Cali; Accra study 2024; Belo Horizonte equity-quality tradeoff 2025), but three gaps persist:

1. **Jabodetabek is under-studied at the equity-gap level.** Existing Jakarta transit research focuses on BRT accessibility (Hardi & Murad, 2023) and TOD potential (Taki et al., 2018), but does not construct a composite need-vs-access gap framework that spans the full metropolitan region including the suburban Bodetabek ring.

2. **Dual-resolution spatial analysis is rare.** Most transit equity studies use a single spatial unit — either administrative zones (census tracts, TAZs, districts) or grid cells. No study systematically compares how the same need-access gap manifests at two resolutions (administrative kelurahan vs. H3 hexagon) in the same metro area, exposing the Modifiable Areal Unit Problem (MAUP) in equity scoring.

3. **"What-if" scenario simulation is disconnected from equity frameworks.** While scenario planning and accessibility modeling are mature fields, few studies embed counterfactual infrastructure placement (e.g., "add a station here") directly into a transit equity quadrant framework to measure the shift in equity scores — making the gap analysis actionable rather than descriptive.

### Public / practical contribution

Over 30 million people live in Jabodetabek. Millions of lower-to-middle-income suburban commuters depend on expensive, polluting private vehicles because transit service is concentrated in central Jakarta. Regional planning is fragmented across multiple municipal governments (DKI Jakarta, Kota/Kab Bogor, Depok, Tangerang, Bekasi) with no shared, granular, evidence-based tool to diagnose where transit investment is most urgently needed.

The product gives planners an answer to: **"Where should the next bus route or station go to reduce transit poverty the most?"** — backed by spatial data, not intuition.

---

## The Two Outputs

| Output | Description | Audience |
|--------|-------------|----------|
| **Research paper** | Thesis chapter or journal article presenting the dual-resolution transit equity gap analysis methodology and Jabodetabek findings | Academic (thesis committee, potential journal reviewers) |
| **Web product** | Interactive map-based tool: quadrant classification, equity scores, what-if simulator, accessibility heatmaps — deployed and publicly accessible | Government planners, NGOs, transport operators, developers, public |

---

## Scope

### In Scope
- **Geography**: Jabodetabek metropolitan region (DKI Jakarta + Bogor, Depok, Tangerang, Bekasi — both kota and kabupaten)
- **Transit modes**: All formal public transit — MRT, LRT, KRL Commuter Line, TransJakarta BRT, JakLingko/Mikrotrans feeder routes, Angkot (where data exists)
- **Spatial units**: Kelurahan (administrative) and H3 hexagons (resolution TBD, likely 7 or 8)
- **Need indicators**: Population density, socioeconomic proxies (poverty rate, vehicle ownership, household expenditure), demographic structure
- **Access indicators**: Proximity to transit stops/stations, transit frequency/headway, route coverage, travel time isochrones to key POIs (hospitals, schools, CBD)
- **Analysis**: Composite need score, composite access score, quadrant classification, Gini coefficient for equity measurement, what-if scenario simulation
- **Product features**: Quadrant map, equity scores, what-if simulator, POI accessibility heatmaps

### Out of Scope
- Informal transport (ojek, non-app ride-hailing) — acknowledged as important but too data-sparse for systematic inclusion
- Real-time transit data (GTFS-RT) — static GTFS and schedule-based analysis only
- Causal inference on transit investment outcomes — this is descriptive/exploratory, not causal
- Fare optimization or pricing analysis
- Historical time-series analysis (cross-sectional snapshot, not longitudinal)
- Mobile app development — web-only prototype

---

## Key Risks & Open Questions

| Risk / Question | Impact | Mitigation |
|-----------------|--------|------------|
| GTFS data availability for non-TransJakarta modes (KRL, LRT, Mikrotrans) | Cannot compute frequency/headway-based access scores | Fall back to stop-proximity; manual GTFS construction from published schedules |
| Socioeconomic data granularity at kelurahan level | Need scores may be coarse | Supplement BPS data with SUSENAS microdata or spatial interpolation |
| H3 resolution choice affects results | MAUP — different resolution = different conclusions | Sensitivity analysis across resolutions 7, 8, 9 |
| "What-if" simulator validity | Simplistic model may mislead users | Clearly label as indicative/scenario-based, not predictive |
| Supervisor alignment | Research direction may shift after Hiroshima orientation | Keep framing flexible; finalize venue after supervisor meeting |

---

*Next step: Phase 1.3 — Literature Scan to sharpen the RQ and build the Source Map.*
