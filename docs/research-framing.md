# RESEARCH FRAMING
## Jabodetabek Transit Equity Mapper
### A Dual-Resolution Spatial Diagnostic for Transit Need-Access Gaps

| Field              | Details                                                  |
|--------------------|----------------------------------------------------------|
| Researcher         | Dhanes                                                   |
| Program            | Master of Smart Society, Hiroshima University             |
| Supervisor         | TBD                                                      |
| Target Venue       | TBD — keeping options open (thesis chapter / journal / conference) |
| Prototype Audience | Government planners (Dishub, Bappeda, BPTJ), NGOs (ITDP), transport operators (TransJakarta, KAI Commuter), real estate developers, general public |
| Status             | **Confirmed** — verified against finalized methodology (E1, MVP-78) |

---

## Research Question

> To what extent does the spatial distribution of public transit accessibility in the Jabodetabek metropolitan region align with the socioeconomic transit need of its population, and how does this alignment differ when measured at administrative (kelurahan) versus uniform hexagonal (H3) spatial resolutions?

## Hypotheses

**H1** (Spatial mismatch): Areas classified as "High Need, Low Access" are disproportionately concentrated in the suburban peripheries of Bodetabek, while "Low Need, High Access" areas cluster in central Jakarta.

**H2** (Resolution effect): The dual-resolution comparison reveals that kelurahan-level analysis systematically underestimates equity gaps in heterogeneous suburban areas — large kelurahan mask internal variation that H3 hexagons expose.

**H3** (Scenario validation): Simulating a new transit node in a "High Need, Low Access" zone produces a larger equity score improvement than the same intervention in a "Low Need, High Access" zone, validating the quadrant framework as a prioritization tool.

---

## Why This Matters

### Academic contribution

Transit equity research in developing countries has grown significantly (Delmelle & Casas 2012 on Cali; Accra study 2024; Belo Horizonte equity-quality tradeoff 2025), but four gaps persist:

1. **No composite need-vs-access equity framework for full Jabodetabek.** Existing Jakarta studies (Hardi & Murad 2023; Taki et al. 2018) cover only DKI Jakarta and do not construct a TNI–TAI gap framework spanning the full metropolitan region including the suburban Bodetabek ring where transit poverty is most severe.

2. **No dual-resolution comparison exposing MAUP in equity scoring.** Javanmard et al. (2023) demonstrate that MAUP significantly affects transit equity conclusions, but no study has compared the same equity gap framework at administrative (kelurahan) vs. uniform hexagonal (H3) resolutions in a single metropolitan area.

3. **No what-if scenario simulation embedded in an equity quadrant framework.** No study embeds counterfactual infrastructure placement directly into a transit equity quadrant classification to measure the shift in equity scores — making the analysis actionable rather than purely descriptive.

4. **No three-way generalized cost model for equity analysis.** Western transit equity studies compare transit against car only. In Jabodetabek and Southeast Asia broadly, the motorcycle is often the marginal competitor to transit (Ng 2018; Sukor & Bhayo 2024). No existing framework computes a three-way generalized cost comparison (transit vs. car vs. motorcycle) and integrates it as a cost-competitiveness layer within a composite accessibility index.

### Public / practical contribution

Over 30 million people live in Jabodetabek. Millions of lower-to-middle-income suburban commuters depend on expensive, polluting private vehicles because transit service is concentrated in central Jakarta. Regional planning is fragmented across multiple municipal governments (DKI Jakarta, Kota/Kab Bogor, Depok, Tangerang, Bekasi) with no shared, granular, evidence-based tool to diagnose where transit investment is most urgently needed.

The product gives planners an answer to: **"Where should the next bus route or station go to reduce transit poverty the most?"** — backed by spatial data, not intuition.

---

## The Two Outputs

| Output | Description | Audience |
|--------|-------------|----------|
| **Research paper** | Thesis chapter or journal article presenting the dual-resolution transit equity gap analysis methodology and Jabodetabek findings | Academic (thesis committee, potential journal reviewers) |
| **Web product** | Interactive map-based tool: quadrant classification, equity scores, what-if simulator, cost competitiveness maps, accessibility heatmaps — deployed and publicly accessible | Government planners, NGOs, transport operators, developers, public |

---

## Scope

### In Scope
- **Geography**: Jabodetabek metropolitan region (DKI Jakarta + Bogor, Depok, Tangerang, Bekasi — both kota and kabupaten)
- **Transit modes**: Formal public transit — MRT, LRT Jabodebek, KRL Commuter Line, TransJakarta BRT, JakLingko/Mikrotrans feeder routes
- **Spatial units**: Kelurahan (~1,800 units, administrative) and H3 hexagons (resolution 8, ~15,000–20,000 cells)
- **Need indicators (TNI)**: Population density, poverty rate, average household expenditure, zero-vehicle household percentage, dependency ratio — equal-weighted, min-max normalized with winsorization at 2nd/98th percentile
- **Access indicators (TAI)**: 5-layer model — L1 first-mile walkability, L2 service quality, L3 CBD journey chain (gravity-weighted via r5py), L4 last-mile POI reach, L5 cost competitiveness (three-way generalized cost: transit vs. car vs. motorcycle)
- **Analysis**: Composite TNI/TAI scores, quadrant classification (Q1–Q4), equity gap, Gini coefficient + Lorenz curve, spatial autocorrelation (Global + Local Moran's I / LISA), what-if scenario simulation
- **Product features**: Quadrant map, dual-resolution toggle, CBD journey chain, transit competitive zones, what-if simulator, road network layer, POI accessibility heatmaps, equity summary dashboard, data download

### Out of Scope
- Informal transport (ojek, angkot, non-app ride-hailing) — data quality insufficient for systematic inclusion
- Real-time transit data (GTFS-RT) — static GTFS and schedule-based analysis only
- Causal inference on transit investment outcomes — this is descriptive/exploratory, not causal
- Fare optimization or pricing analysis
- Historical time-series analysis (cross-sectional snapshot, not longitudinal)
- Mobile app development — web-only
- User accounts or saved sessions

---

## Key Risks & Open Questions

| Risk / Question | Impact | Mitigation |
|-----------------|--------|------------|
| KRL/MRT GTFS feeds do not exist publicly | Cannot compute frequency/headway-based access scores | Manual GTFS construction from community APIs (comuline/api, mrt-jakarta-api) — MVP-84 |
| BPS socioeconomic data at kecamatan granularity only | TNI scores may be coarse at kelurahan level | Dasymetric disaggregation using WorldPop population raster |
| H3 resolution choice affects results (MAUP) | Different resolution = different conclusions | Primary analysis at resolution 8; sensitivity at 7 and 9 with confusion matrices + Cohen's kappa |
| "What-if" simulator validity | Simplistic model may mislead users | Clearly label as indicative/scenario-based, not predictive; recompute L1+L2 only within catchment |
| Supervisor alignment | Research direction may shift after Hiroshima orientation | Keep framing flexible; finalize venue after supervisor meeting |

---

*Literature scan complete (MVP-2, 2026-03-16). RQ confirmed — no refinements needed. The literature validates all four gap claims. See `docs/source-map.md` for full scan output and `docs/literature_review.md` for academic prose.*

*Verified against finalized methodology (MVP-78, 2026-03-21). Hypotheses updated from 2 to 3 (H2 resolution effect added). Gap claims updated from 3 to 4 (three-way GC added). Scope aligned with confirmed TAI/TNI/GC methods and PRD features.*
