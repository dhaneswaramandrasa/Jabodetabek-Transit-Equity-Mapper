# Epics & Tasks

**Project**: Jabodetabek Transit Equity Mapper
**Linear workspace**: https://linear.app/olsera-mitra-modal/project/jabodetabek-transit-equity-mapper-64fadf43f309
**Team**: Product-MVP (MVP)
**Last synced**: 2026-03-16

---

## Epic Overview

| Epic | Track | Name | Status | Tickets |
|------|-------|------|--------|---------|
| E0 | Foundation | Research Foundation | In Progress | 8/9 done |
| E3 | Paper | Literature Review | Draft — confirm after E0 | 0/3 done |
| E4 | Paper | Paper Drafting | Draft — confirm after E0 | 0/5 done |
| E5 | Paper | Paper Review & Revision | Draft — confirm after E0 | 0/2 done |
| E6 | Product | Data Pipeline | Draft — confirm after E0 | 0/7 done |
| E7 | Product | UI Foundation | Draft — confirm after E0 | 0/3 done |
| E8 | Product | Core Features | Draft — confirm after E0 | 0/4 done |
| E9 | Product | Code Review & QA | Draft — confirm after E0 | 0/2 done |
| E10 | Convergence | Deliverables | Draft — confirm after E0 | 0/4 done |

**Current phase**: E0 (Foundation)
**Phase 3 trigger**: When MVP-3 (E0-008) is Done → create E1, E2, confirm E3–E10

Dependency order: E0 → E1 → E2 → [E3/E4/E5 ∥ E6/E7/E8/E9] → E10

> **Note**: E1 (Research Framing) and E2 (Methodology & Data Design) will be created in Phase 3
> after E0 completes. Their tickets confirm and formalize the E0 outputs in the docs system.
> E3–E10 tickets below are **drafts** from initial planning — they will be reviewed and
> refined in Phase 3 based on finalized methodology.

---

## E0 · Foundation

MVP-1 through MVP-8 + MVP-77. These must ALL complete before Phase 3 triggers.

### MVP-1 — Finalize research framing document *(E0 pre-work, Phase 1.2)*
- **E0 position**: Pre-E0 (Phase 1.2 output)
- **Status**: Done
- **Priority**: High
- **AC**:
  - [x] Research question defined (dual-resolution transit equity gap)
  - [x] Hypotheses H1, H2, H3 stated
  - [x] Two outputs defined (paper + web product)
  - [x] Scope and out-of-scope documented
- **Blocked by**: none
- **URL**: https://linear.app/olsera-mitra-modal/issue/MVP-1/finalize-research-framing-document

### MVP-2 — Complete literature scan and source map *(E0-001)*
- **E0 position**: E0-001 — first E0 ticket, unblocks all methodology work
- **Status**: Done
- **Priority**: High
- **AC**:
  - [x] 12 search queries on Google Scholar, Semantic Scholar, web
  - [x] 15 papers extracted (citation, method+findings, data sources, relevance)
  - [x] `docs/source-map.md`: Source Map table + synthesis produced
  - [x] `docs/literature_review.md`: Academic prose by theme (v0.1, ~2,200 words)
  - [x] `docs/methodology.md` §2.1b Theoretical Framework updated with top papers
  - [x] `docs/methodology.md` §2.1c Methodological Precedents updated
  - [x] Refinements identified: TNI indicators confirmed (literature supports current set); GC motorcycle parameters confirmed (Ng 2018); MAUP dual-resolution confirmed (Javanmard 2023)
  - [x] `docs/research-framing.md` updated — RQ confirmed, no changes needed
- **Blocked by**: none
- **URL**: https://linear.app/olsera-mitra-modal/issue/MVP-2/complete-literature-scan-and-source-map

### MVP-4 — Finalize 5-layer TAI methodology *(E0-002)*
- **E0 position**: E0-002 — first methodology ticket
- **Status**: Done
- **Priority**: High
- **AC**:
  - [x] 5-layer TAI confirmed: first-mile, service quality, CBD journey chain, last-mile, cost competitiveness
  - [x] Weights: 0.20 / 0.15 / 0.35 / 0.15 / 0.15
- **Blocked by**: none
- **URL**: https://linear.app/olsera-mitra-modal/issue/MVP-4/finalize-5-layer-tai-methodology

### MVP-5 — Finalize TNI indicator set and weighting scheme *(E0-003)*
- **E0 position**: E0-003 — TNI methodology, informed by literature scan
- **Status**: Done
- **Priority**: Medium
- **AC**:
  - [x] TNI indicators confirmed: pop_density, poverty_rate, avg_household_expenditure, zero_vehicle_hh_pct, dependency_ratio
  - [x] Normalization method confirmed (min-max with winsorization at 2nd/98th percentile)
  - [x] Weighting confirmed (equal default, sensitivity analysis via ±20% perturbation + PCA check)
  - [x] Edge cases documented (missing data, zero variance, outliers)
  - [x] Literature precedents cited: Mamun & Lownes (2011), Jiao & Dillivan (2013), Currie (2010), Rathod et al. (2025)
- **Blocked by**: MVP-2 ✅
- **Output**: `docs/drafts/mvp5-tni-methodology.md`
- **URL**: https://linear.app/olsera-mitra-modal/issue/MVP-5/finalize-tni-indicator-set-and-weighting-scheme

### MVP-7 — Design H3 derivation pipeline *(E0-004)*
- **E0 position**: E0-004 — H3 methodology, informed by literature scan
- **Status**: Done
- **Priority**: Medium
- **AC**:
  - [x] Dual-method H3 derivation designed
  - [x] Dasymetric (WorldPop) for socioeconomic — from kelurahan-level values (step 9 output)
  - [x] Area-weighted (spatial clip) for infrastructure
  - [x] Point-in-polygon for stops/POIs
  - [x] Direct computation for travel times
  - [x] Resolution sensitivity plan (7, 8, 9) with confusion matrices + Cohen's kappa
  - [x] Literature precedents cited: Javanmard et al. (2023), Mennis (2003), Tatem (2017), Openshaw (1984)
- **Blocked by**: MVP-2 ✅
- **Output**: `docs/drafts/mvp7-h3-methodology.md`
- **URL**: https://linear.app/olsera-mitra-modal/issue/MVP-7/design-h3-derivation-pipeline-dasymetric-area-weighted

### MVP-8 — Design three-way generalized cost model *(E0-005)*
- **E0 position**: E0-005 — GC methodology, informed by literature scan
- **Status**: Done
- **Priority**: High
- **AC**:
  - [x] Layer 5 formulas finalized (transit, car, motorcycle)
  - [x] Cost parameters confirmed: VOT Rp 500/min, car fuel Rp 1,000/km, motorcycle fuel Rp 200/km, tolls, parking, fatigue brackets
  - [x] Motorcycle toll exclusion modeled with structural implications analysis
  - [x] TCR thresholds validated with 3 worked examples: BSD (0.87 swing), Ciputat (0.66 private wins), Tebet (0.69 private wins)
  - [x] Literature precedents cited: Ng (2018), Sukor & Bhayo (2024), Ortuzar & Willumsen (2011), Hardi & Murad (2023)
- **Blocked by**: MVP-2 ✅
- **Output**: `docs/drafts/mvp8-gc-methodology.md`
- **URL**: https://linear.app/olsera-mitra-modal/issue/MVP-8/design-three-way-generalized-cost-model-transit-vs-car-vs-motorcycle

### MVP-77 — Consolidate methodology.md + DATA_MODEL.md with literature findings *(E0-006)*
- **E0 position**: E0-006 — consolidation gate before data acquisition
- **Status**: Done
- **Priority**: High
- **AC**:
  - [x] `docs/methodology.md` §Theoretical Framework updated with top papers from source-map.md
  - [x] `docs/methodology.md` §Methodological Precedents updated with methods from literature
  - [x] All formula references verified against literature (TAI, TNI, GC, H3)
  - [x] `docs/DATA_MODEL.md` confirmed against finalized methodology — all fields traceable
  - [x] `docs/methodology.md` and `docs/DATA_MODEL.md` in sync
  - [x] Methodology refinements documented: motorcycle fuel Rp 400→200/km, H3 source kecamatan→kelurahan, transit_not_available enum, is_edge_cell, kelurahan_ids, population as float at H3
  - [x] research-methodology-verifier validated alignment
- **Blocked by**: MVP-5 ✅, MVP-7 ✅, MVP-8 ✅
- **URL**: https://linear.app/olsera-mitra-modal/issue/MVP-77/consolidate-methodologymd-data-modelmd-with-literature-findings

### MVP-6 — Define data acquisition plan and verify source access *(E0-007)*
- **E0 position**: E0-007 — data acquisition plan, needs confirmed schema
- **Status**: Done
- **Priority**: High
- **AC**:
  - [x] All 10 data sources verified: 5 accessible, 2 unavailable (KRL/MRT GTFS — need manual construction), 2 manual (LRT/BPS), 1 generated (H3)
  - [x] Acquisition scripts in `src/ingestion/` (7 scripts + README + verification report)
  - [x] TransJakarta GTFS confirmed fresh (2026-03-14), OSM/Overpass/WorldPop accessible, GADM+HDX for boundaries
  - [x] Data sources mapped to DATA_MODEL.md schema
- **Blocked by**: MVP-77 ✅
- **New blocker discovered**: KRL and MRT GTFS feeds do not exist — must be manually constructed from community APIs before E6 pipeline. See MVP-39.
- **Output**: `src/ingestion/`, `src/ingestion/VERIFICATION_REPORT.md`

### MVP-39 — Construct KRL and MRT GTFS feeds manually *(new — blocks E6)*
- **E0 position**: New ticket — discovered during MVP-6 verification
- **Status**: Todo
- **Priority**: Urgent
- **AC**:
  - [ ] KRL GTFS constructed from comuline/api + published schedules (~80 stations, 6 lines)
  - [ ] MRT GTFS constructed from mrt-jakarta-api + published schedules (~13 stations, 1 line)
  - [ ] Both feeds pass `gtfs_kit` validation
  - [ ] Feeds placed in `data/raw/gtfs/`
  - [ ] Feed freshness documented
- **Blocked by**: none
- **Estimated effort**: KRL 4-6 hours, MRT 1-2 hours
- **URL**: https://linear.app/olsera-mitra-modal/issue/MVP-6/define-data-acquisition-scripts-and-verify-source-access

### MVP-3 — Produce PRD for web product *(E0-008)*
- **E0 position**: E0-008 — LAST E0 ticket. When Done → Phase 3 triggers.
- **Status**: Todo
- **Priority**: Medium
- **AC**:
  - [ ] PRD sections 1–7 complete
  - [ ] All 4 personas documented
  - [ ] 5-layer TAI requirements reflected in features
  - [ ] Gap statement from Source Map included
  - [ ] Features match finalized methodology + verified data sources
- **Blocked by**: MVP-2 (gap statement), MVP-6 (verified data sources)
- **URL**: https://linear.app/olsera-mitra-modal/issue/MVP-3/produce-prd-for-web-product
- **Notes**: Draft PRD pre-filled in `docs/prd.md` from research-framing.md; will be refined after E0

---

## E0 Dependency Chain

```
MVP-1 (Done) ─┐
              │
MVP-4 (Done) ─┤
              │
MVP-2 (Done) ─────────────┐
  │                       │
  ├→ MVP-5 (Done: TNI) ──┐
  ├→ MVP-7 (Done: H3)  ──┤→ MVP-77 (Done: consolidate) → MVP-6 (Done: acquisition)
  └→ MVP-8 (Done: GC)  ──┘                                        │
  │                                                                  │
  └──────────────────────────────────────────────────── MVP-3 (E0-008: PRD) ←──┘
                                                           │
                                                    [Phase 3 trigger]
```

**Critical path**: `MVP-2 ✅ → [MVP-5 ✅, MVP-7 ✅, MVP-8 ✅] → MVP-77 ✅ → MVP-6 ✅ → MVP-3 → Phase 3`
**New dependency**: `MVP-39 (construct KRL+MRT GTFS) → blocks E6 pipeline (MVP-19)`

---

## E3–E10: Draft Tickets (to be confirmed in Phase 3)

> These tickets were created during initial planning. They will be **reviewed, refined, and
> potentially restructured** in Phase 3 after E0 completes and methodology is finalized.
> Dependencies may change based on finalized methodology and data acquisition results.

---

## E3 · Literature Review (Paper) — Draft

### MVP-9 — Write theoretical framework section
- **Status**: Todo (draft)
- **Priority**: Medium
- **AC**:
  - [ ] Transit equity theory (Gini, Lorenz)
  - [ ] MAUP literature
  - [ ] Generalized cost theory
  - [ ] First/last mile literature
  - [ ] ~1500–2000 words
- **Blocked by**: MVP-2 (source map)
- **URL**: https://linear.app/olsera-mitra-modal/issue/MVP-9/write-theoretical-framework-section

### MVP-10 — Write related work section (Jakarta/Jabodetabek transit studies)
- **Status**: Todo (draft)
- **Priority**: Medium
- **AC**:
  - [ ] Jakarta/Jabodetabek transit studies reviewed (Hardi & Murad 2023, Taki et al. 2018, BPTJ)
  - [ ] Gap identified: no composite need-vs-access framework spanning full Jabodetabek
  - [ ] ~1000–1500 words
- **Blocked by**: MVP-2 (source map)
- **URL**: https://linear.app/olsera-mitra-modal/issue/MVP-10/write-related-work-section-jakartajabodetabek-transit-studies

### MVP-11 — Write methodology precedents section (r5py, H3, composite indices)
- **Status**: Todo (draft)
- **Priority**: Medium
- **AC**:
  - [ ] r5py/R5/OTP routing reviewed
  - [ ] H3 in urban analysis reviewed
  - [ ] Composite index construction (Currie 2010, Kaeoruean et al. 2020)
  - [ ] Generalized cost in mode choice
  - [ ] ~1000–1500 words
- **Blocked by**: MVP-2 (source map)
- **URL**: https://linear.app/olsera-mitra-modal/issue/MVP-11/write-methodology-precedents-section-r5py-h3-composite-indices

---

## E4 · Paper Drafting (Paper) — Draft

### MVP-12 — Write introduction
- **Status**: Todo (draft)
- **Priority**: Medium
- **AC**:
  - [ ] Problem statement, motivation, RQ
  - [ ] Contributions: 5-layer TAI, dual resolution, three-way cost model, what-if simulator
  - [ ] Paper structure overview
  - [ ] ~1500–2000 words
- **Blocked by**: MVP-9, MVP-10, MVP-11 (literature review sections)
- **URL**: https://linear.app/olsera-mitra-modal/issue/MVP-12/write-introduction

### MVP-13 — Write methods section
- **Status**: Todo (draft)
- **Priority**: High
- **AC**:
  - [ ] Study area, data sources
  - [ ] 5-layer TAI formulas
  - [ ] TNI, H3 derivation
  - [ ] Three-way GC model
  - [ ] Quadrant/Gini/LISA methodology
  - [ ] What-if simulator method
  - [ ] Matches `docs/methodology.md` exactly
  - [ ] ~3000–4000 words
- **Blocked by**: MVP-4, MVP-5, MVP-7, MVP-8 (methodology finalized)
- **URL**: https://linear.app/olsera-mitra-modal/issue/MVP-13/write-methods-section

### MVP-14 — Write results section
- **Status**: Todo (draft)
- **Priority**: High
- **AC**:
  - [ ] Quadrant distribution, spatial patterns
  - [ ] Gini comparison, LISA clusters
  - [ ] Resolution comparison
  - [ ] Cost competitiveness map
  - [ ] What-if scenarios
  - [ ] ~2000–3000 words
- **Blocked by**: MVP-25 (E6 data pipeline complete)
- **URL**: https://linear.app/olsera-mitra-modal/issue/MVP-14/write-results-section

### MVP-15 — Write discussion section
- **Status**: Todo (draft)
- **Priority**: Medium
- **AC**:
  - [ ] Assess H1/H2/H3
  - [ ] First-mile paradox analysis
  - [ ] Three-way cost implications
  - [ ] Comparison with international studies
  - [ ] Practical implications for all 4 audiences
  - [ ] ~2000–2500 words
- **Blocked by**: MVP-14 (results)
- **URL**: https://linear.app/olsera-mitra-modal/issue/MVP-15/write-discussion-section

### MVP-16 — Write conclusion and abstract
- **Status**: Todo (draft)
- **Priority**: Medium
- **AC**:
  - [ ] Conclusion: contribution summary, future work
  - [ ] Abstract: 250–300 words, written last
  - [ ] References compiled in APA format
- **Blocked by**: MVP-15 (discussion)
- **URL**: https://linear.app/olsera-mitra-modal/issue/MVP-16/write-conclusion-and-abstract

---

## E5 · Paper Review & Revision (Paper) — Draft

### MVP-17 — Self-review against Phase 5P checklist
- **Status**: Todo (draft)
- **Priority**: Medium
- **AC**:
  - [ ] RQ stated in intro
  - [ ] Hypotheses tested
  - [ ] Methods match methodology.md
  - [ ] Results address hypotheses
  - [ ] Claims cited
  - [ ] Limitations acknowledged
  - [ ] Figures numbered and matching product
- **Blocked by**: MVP-16 (all paper sections complete)
- **URL**: https://linear.app/olsera-mitra-modal/issue/MVP-17/self-review-against-phase-5p-checklist

### MVP-18 — Final review and revision
- **Status**: Todo (draft)
- **Priority**: Medium
- **AC**:
  - [ ] Peer feedback incorporated (if available)
  - [ ] Citation format confirmed
  - [ ] Final proofread
- **Blocked by**: MVP-17 (self-review)
- **URL**: https://linear.app/olsera-mitra-modal/issue/MVP-18/incorporate-supervisor-feedback

---

## E6 · Data Pipeline (Product) — Draft

### MVP-19 — Download, validate, and merge GTFS feeds + LRT stations
- **Status**: Todo (draft)
- **Priority**: Urgent
- **AC**:
  - [ ] TransJakarta, KRL, MRT GTFS downloaded and validated
  - [ ] LRT stations compiled manually (~18 stations)
  - [ ] Merged into unified transit_stops.geojson with mode tags
  - [ ] Headway per stop computed
  - [ ] Output: `data/processed/transit/`
- **Blocked by**: MVP-6 (data acquisition scripts must be defined first)
- **URL**: https://linear.app/olsera-mitra-modal/issue/MVP-19/download-validate-and-merge-gtfs-feeds-lrt-stations

### MVP-20 — Extract and process OSM road network + compute road metrics
- **Status**: Todo (draft)
- **Priority**: High
- **AC**:
  - [ ] Java PBF downloaded from Geofabrik
  - [ ] Clipped to Jabodetabek bbox via osmium
  - [ ] Road segments extracted with highway tags
  - [ ] Road metrics per kelurahan: length, density, class proportions, intersection density
  - [ ] Output: `data/processed/networks/`
- **Blocked by**: MVP-6 (data acquisition scripts must be defined first)
- **URL**: https://linear.app/olsera-mitra-modal/issue/MVP-20/extract-and-process-osm-road-network-compute-road-metrics

### MVP-21 — Extract strict POIs via Overpass API + manual verification
- **Status**: Todo (draft)
- **Priority**: High
- **AC**:
  - [ ] 9 CBD zone polygons created manually
  - [ ] Strict POIs extracted via Overpass (hospitals, schools, markets, industrial, gov offices)
  - [ ] Manual verification of 10% sample
  - [ ] Output: `data/processed/poi/`
- **Blocked by**: MVP-6 (data acquisition scripts must be defined first)
- **URL**: https://linear.app/olsera-mitra-modal/issue/MVP-21/extract-strict-pois-via-overpass-api-manual-verification

### MVP-22 — Assemble BPS demographics + disaggregate to kelurahan via WorldPop
- **Status**: Todo (draft)
- **Priority**: High
- **AC**:
  - [ ] BPS data collected for DKI Jakarta + 5 Bodetabek jurisdictions
  - [ ] Kelurahan boundaries loaded + BPS codes verified
  - [ ] WorldPop raster downloaded
  - [ ] Kecamatan data disaggregated to kelurahan via dasymetric allocation
  - [ ] zero_vehicle_hh_pct and dependency_ratio modeled
  - [ ] Output: `data/processed/demographics/`
- **Blocked by**: MVP-6 (data acquisition scripts must be defined first)
- **URL**: https://linear.app/olsera-mitra-modal/issue/MVP-22/assemble-bps-demographics-disaggregate-to-kelurahan-via-worldpop

### MVP-23 — Compute 5-layer TAI and TNI per kelurahan
- **Status**: Todo (draft)
- **Priority**: Urgent
- **AC**:
  - [ ] All 5 TAI layers computed per kelurahan via r5py
  - [ ] TNI computed (5 indicators)
  - [ ] Equity gap + quadrant classification
  - [ ] ~16,200 route queries budgeted (2–4 hours compute)
  - [ ] Output: `data/processed/scores/`
- **Blocked by**: MVP-19, MVP-20, MVP-21, MVP-22 (all data acquired)
- **URL**: https://linear.app/olsera-mitra-modal/issue/MVP-23/compute-5-layer-tai-and-tni-per-kelurahan

### MVP-24 — Generate H3 grid + derive all indicators via dual methods
- **Status**: Todo (draft)
- **Priority**: Urgent
- **AC**:
  - [ ] H3 res-8 grid generated (~15–20k cells)
  - [ ] Socioeconomic derived via dasymetric (WorldPop)
  - [ ] Road network via spatial clip
  - [ ] Stops/POIs via point-in-polygon
  - [ ] Travel times via r5py from H3 centroids
  - [ ] TAI/TNI/quadrant at H3 level
  - [ ] Batch in chunks of 1000; budget 8–16 hours
  - [ ] Output: `data/processed/scores/`
- **Blocked by**: MVP-23 (kelurahan pipeline validated first)
- **URL**: https://linear.app/olsera-mitra-modal/issue/MVP-24/generate-h3-grid-derive-all-indicators-via-dual-methods

### MVP-25 — Compute equity gap, Gini, LISA at both resolutions
- **Status**: Todo (draft)
- **Priority**: High
- **AC**:
  - [ ] Gini coefficients at both resolutions
  - [ ] Lorenz curve data
  - [ ] Global + local Moran's I (LISA clusters)
  - [ ] Resolution comparison: confusion matrix, reclassified areas
  - [ ] Sensitivity analysis: weights ±20%, H3 res 7 and 9
  - [ ] Output: `data/processed/analysis/`
- **Blocked by**: MVP-23, MVP-24
- **URL**: https://linear.app/olsera-mitra-modal/issue/MVP-25/compute-equity-gap-gini-lisa-at-both-resolutions

---

## E7 · UI Foundation (Product) — Draft

### MVP-26 — Audit existing prototype against new methodology
- **Status**: Todo (draft)
- **Priority**: High
- **AC**:
  - [ ] Current data model documented
  - [ ] Gap analysis for new fields
  - [ ] Component audit
  - [ ] API route audit
  - [ ] Zustand store audit
  - [ ] Migration plan produced
- **Blocked by**: none
- **URL**: https://linear.app/olsera-mitra-modal/issue/MVP-26/audit-existing-prototype-against-new-methodology

### MVP-27 — Migrate from synthetic data to real pipeline output
- **Status**: Todo (draft)
- **Priority**: Urgent
- **AC**:
  - [ ] Synthetic data replaced with real pipeline output
  - [ ] export_to_web.py updated
  - [ ] All GeoJSON files in web/public/data/ replaced
  - [ ] Road network + CBD zones files added
  - [ ] Zustand store types updated
  - [ ] App loads with real data verified
- **Blocked by**: MVP-23 (kelurahan scores), MVP-26 (audit)
- **URL**: https://linear.app/olsera-mitra-modal/issue/MVP-27/migrate-from-synthetic-data-to-real-pipeline-output

### MVP-28 — Add road network layer + cost comparison card to UI
- **Status**: Todo (draft)
- **Priority**: High
- **AC**:
  - [ ] Road network deck.gl layer (color-coded by highway class, toggleable)
  - [ ] CBD zone polygons rendered on map
  - [ ] Three-way cost comparison card (GC transit/car/motorcycle)
  - [ ] Transit competitive zone badge
  - [ ] 5-layer TAI breakdown card (L1–L5)
  - [ ] First-mile quality indicators on detail panel
- **Blocked by**: MVP-27 (real data migrated)
- **URL**: https://linear.app/olsera-mitra-modal/issue/MVP-28/add-road-network-layer-cost-comparison-card-to-ui

---

## E8 · Core Features (Product) — Draft

### MVP-29 — Implement quadrant map with dual-resolution toggle
- **Status**: Todo (draft)
- **Priority**: High
- **AC**:
  - [ ] Quadrant choropleth at kelurahan level (4 colors)
  - [ ] Toggle to H3 hexagon view
  - [ ] Color legend with quadrant descriptions
  - [ ] Click shows detail panel (TNI, TAI, 5 layers, equity gap, quadrant)
  - [ ] Smooth resolution transitions
- **Blocked by**: MVP-27 (real data)
- **URL**: https://linear.app/olsera-mitra-modal/issue/MVP-29/implement-quadrant-map-with-dual-resolution-toggle

### MVP-30 — Implement CBD journey chain visualization
- **Status**: Todo (draft)
- **Priority**: High
- **AC**:
  - [ ] Journey legs displayed: first-mile → station → ride → transfer → ride → last-mile
  - [ ] Each leg shows mode, time, fare
  - [ ] Path rendered on map as polyline
  - [ ] Side panel compares transit vs car vs motorcycle GC
- **Blocked by**: MVP-27 (real data)
- **URL**: https://linear.app/olsera-mitra-modal/issue/MVP-30/implement-cbd-journey-chain-visualization

### MVP-31 — Implement what-if station placement simulator
- **Status**: Todo (draft)
- **Priority**: Medium
- **AC**:
  - [ ] Click map to place hypothetical station
  - [ ] Select mode type (KRL/MRT/BRT/Mikrotrans)
  - [ ] Configurable catchment (1km walk, 3km feeder)
  - [ ] Before/after: quadrant changes, Gini delta
  - [ ] Labeled as "scenario simulation, not prediction"
- **Blocked by**: MVP-29 (quadrant map)
- **URL**: https://linear.app/olsera-mitra-modal/issue/MVP-31/implement-what-if-station-placement-simulator

### MVP-32 — Implement transit competitive zone map
- **Status**: Todo (draft)
- **Priority**: High
- **AC**:
  - [ ] Three-color choropleth: green (transit wins), amber (swing), red (private wins)
  - [ ] Toggle TCR_vs_car / TCR_vs_motorcycle / TCR_combined
  - [ ] Click shows full GC breakdown
  - [ ] Distance-to-CBD ring overlay
  - [ ] Summary stats: % population per zone
- **Blocked by**: MVP-27 (real data)
- **URL**: https://linear.app/olsera-mitra-modal/issue/MVP-32/implement-transit-competitive-zone-map

---

## E9 · Code Review & QA (Product) — Draft

### MVP-33 — Code review against Phase 5D checklist
- **Status**: Todo (draft)
- **Priority**: High
- **AC**:
  - [ ] No runtime errors
  - [ ] PRD user stories addressed
  - [ ] RQ answerable from UI
  - [ ] Data schema matches methodology
  - [ ] Wrangling in lib/, not inline
  - [ ] Dataset in public/dataset/ with README
  - [ ] Components < 150 lines, no `any`
  - [ ] Loading/empty/error states
- **Blocked by**: MVP-29, MVP-30, MVP-31, MVP-32 (all core features)
- **URL**: https://linear.app/olsera-mitra-modal/issue/MVP-33/code-review-against-phase-5d-checklist

### MVP-34 — Edge case testing + deployment verification
- **Status**: Todo (draft)
- **Priority**: Medium
- **AC**:
  - [ ] Zero-transit-stop kelurahan tested
  - [ ] H3 cells spanning kelurahan boundaries tested
  - [ ] What-if at boundary locations tested
  - [ ] Large kelurahan > 20 km² tested
  - [ ] Vercel deployment loads all GeoJSON
  - [ ] Performance: map < 3s, click < 1s
  - [ ] Mobile responsive
- **Blocked by**: MVP-33 (code review)
- **URL**: https://linear.app/olsera-mitra-modal/issue/MVP-34/edge-case-testing-deployment-verification

---

## E10 · Deliverables (Convergence) — Draft

### MVP-35 — Final paper assembly + reference formatting
- **Status**: Todo (draft)
- **Priority**: High
- **AC**:
  - [ ] All paper sections assembled in order
  - [ ] References formatted (APA default)
  - [ ] Figures numbered matching product screenshots
  - [ ] Abstract written last
  - [ ] PDF generated
- **Blocked by**: MVP-17 (paper self-review)
- **URL**: https://linear.app/olsera-mitra-modal/issue/MVP-35/final-paper-assembly-reference-formatting

### MVP-36 — Package dataset for public distribution
- **Status**: Todo (draft)
- **Priority**: Medium
- **AC**:
  - [ ] Cleaned datasets in public/dataset/
  - [ ] README with field glossary, source citations, methodology summary
  - [ ] License: CC BY 4.0
  - [ ] Dataset downloadable independently
- **Blocked by**: MVP-25 (analysis complete)
- **URL**: https://linear.app/olsera-mitra-modal/issue/MVP-36/package-dataset-for-public-distribution

### MVP-37 — Deploy product to Vercel + link paper and dataset
- **Status**: Todo (draft)
- **Priority**: High
- **AC**:
  - [ ] Production build clean
  - [ ] Deployed to Vercel
  - [ ] About/footer links to paper + dataset
  - [ ] README with research context
  - [ ] Performance < 5s load, < 15 MB GeoJSON
  - [ ] OG meta tags for social sharing
- **Blocked by**: MVP-34 (edge case testing)
- **URL**: https://linear.app/olsera-mitra-modal/issue/MVP-37/deploy-product-to-vercel-link-paper-and-dataset

### MVP-38 — Prepare presentation / poster with product demo
- **Status**: Todo (draft)
- **Priority**: Medium
- **AC**:
  - [ ] Slide deck (10–12 slides)
  - [ ] Product demo slide with QR code to live app
  - [ ] Key figures from paper reused
  - [ ] Speaker notes
  - [ ] Optional academic poster (A0)
  - [ ] Practice: 15–20 min + 10 min Q&A
- **Blocked by**: MVP-37 (product deployed)
- **URL**: https://linear.app/olsera-mitra-modal/issue/MVP-38/prepare-presentation-poster-with-product-demo
