# Epics & Tasks

**Project**: Jabodetabek Transit Equity Mapper
**Linear workspace**: https://linear.app/olsera-mitra-modal/project/jabodetabek-transit-equity-mapper-64fadf43f309
**Team**: Product-MVP (MVP)
**Last synced**: 2026-03-16

---

## Epic Overview

| Epic | Track | Name | Status | Tickets |
|------|-------|------|--------|---------|
| E1 | Shared | Research Framing | In Progress | 1/3 done |
| E2 | Shared | Methodology & Data Design | In Progress | 1/5 done |
| E3 | Paper | Literature Review | Not Started | 0/3 done |
| E4 | Paper | Paper Drafting | Not Started | 0/5 done |
| E5 | Paper | Paper Review & Revision | Not Started | 0/2 done |
| E6 | Product | Data Pipeline | Not Started | 0/7 done |
| E7 | Product | UI Foundation | Not Started | 0/3 done |
| E8 | Product | Core Features | Not Started | 0/4 done |
| E9 | Product | Code Review & QA | Not Started | 0/2 done |
| E10 | Convergence | Deliverables | Not Started | 0/4 done |

Dependency order: E1 → E2 → [E3/E4/E5 ∥ E6/E7/E8/E9] → E10

---

## E1 · Research Framing (Shared)

### MVP-1 — Finalize research framing document
- **Status**: Done
- **Priority**: High
- **AC**:
  - [x] Research question defined (dual-resolution transit equity gap)
  - [x] Hypotheses H1, H2, H3 stated
  - [x] Two outputs defined (paper + web product)
  - [x] Scope and out-of-scope documented
- **Blocked by**: none
- **URL**: https://linear.app/olsera-mitra-modal/issue/MVP-1/finalize-research-framing-document

### MVP-2 — Complete literature scan and source map
- **Status**: Todo
- **Priority**: High
- **AC**:
  - [ ] 3–5 search queries on Google Scholar, Semantic Scholar
  - [ ] 10–15 papers extracted (citation, method+findings, data sources, relevance)
  - [ ] Source Map table produced
  - [ ] Synthesis: established knowledge, gap, methodological precedents, data sources
- **Blocked by**: none
- **URL**: https://linear.app/olsera-mitra-modal/issue/MVP-2/complete-literature-scan-and-source-map

### MVP-3 — Produce PRD for web product
- **Status**: Todo
- **Priority**: Medium
- **AC**:
  - [ ] PRD sections 1–7 complete
  - [ ] All 4 personas documented
  - [ ] 5-layer TAI requirements reflected in features
  - [ ] Gap statement from Source Map included
- **Blocked by**: MVP-2 (needs gap statement from source map)
- **URL**: https://linear.app/olsera-mitra-modal/issue/MVP-3/produce-prd-for-web-product
- **Notes**: Draft PRD pre-filled in `docs/prd.md` from research-framing.md; will be refined after MVP-2

---

## E2 · Methodology & Data Design (Shared)

### MVP-4 — Finalize 5-layer TAI methodology
- **Status**: Done
- **Priority**: High
- **AC**:
  - [x] 5-layer TAI confirmed: first-mile, service quality, CBD journey chain, last-mile, cost competitiveness
  - [x] Weights: 0.20 / 0.15 / 0.35 / 0.15 / 0.15
- **Blocked by**: none
- **URL**: https://linear.app/olsera-mitra-modal/issue/MVP-4/finalize-5-layer-tai-methodology

### MVP-5 — Finalize TNI indicator set and weighting scheme
- **Status**: Todo
- **Priority**: Medium
- **AC**:
  - [ ] TNI indicators confirmed: pop_density, poverty_rate, avg_household_expenditure, zero_vehicle_hh_pct, dependency_ratio
  - [ ] Normalization method confirmed (min-max)
  - [ ] Weighting confirmed (equal default, sensitivity analysis planned)
  - [ ] Edge cases documented
- **Blocked by**: MVP-2 (literature scan may refine indicators)
- **URL**: https://linear.app/olsera-mitra-modal/issue/MVP-5/finalize-tni-indicator-set-and-weighting-scheme

### MVP-6 — Define data acquisition scripts and verify source access
- **Status**: Todo
- **Priority**: High
- **AC**:
  - [ ] All 10 data sources verified accessible
  - [ ] Acquisition scripts in `src/ingestion/`
  - [ ] GTFS, OSM, Overpass, BPS, WorldPop, GADM downloads tested
- **Blocked by**: MVP-5, MVP-7, MVP-8 (methodology must be finalized before data acquisition)
- **URL**: https://linear.app/olsera-mitra-modal/issue/MVP-6/define-data-acquisition-scripts-and-verify-source-access

### MVP-7 — Design H3 derivation pipeline (dasymetric + area-weighted)
- **Status**: Todo
- **Priority**: Medium
- **AC**:
  - [ ] Dual-method H3 derivation designed
  - [ ] Dasymetric (WorldPop) for socioeconomic
  - [ ] Area-weighted (spatial clip) for infrastructure
  - [ ] Point-in-polygon for stops/POIs
  - [ ] Direct computation for travel times
  - [ ] Resolution sensitivity plan (7, 8, 9)
- **Blocked by**: MVP-2 (literature scan may inform derivation methods)
- **URL**: https://linear.app/olsera-mitra-modal/issue/MVP-7/design-h3-derivation-pipeline-dasymetric-area-weighted

### MVP-8 — Design three-way generalized cost model (transit vs car vs motorcycle)
- **Status**: Todo
- **Priority**: High
- **AC**:
  - [ ] Layer 5 formulas finalized
  - [ ] Cost parameters confirmed (VOT, fuel, toll, parking, fatigue)
  - [ ] Motorcycle toll exclusion modeled
  - [ ] TCR thresholds validated with 3 worked examples (BSD, Ciputat, Tebet)
- **Blocked by**: MVP-2 (literature scan may refine cost parameters)
- **URL**: https://linear.app/olsera-mitra-modal/issue/MVP-8/design-three-way-generalized-cost-model-transit-vs-car-vs-motorcycle

---

## E3 · Literature Review (Paper)

### MVP-9 — Write theoretical framework section
- **Status**: Todo
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
- **Status**: Todo
- **Priority**: Medium
- **AC**:
  - [ ] Jakarta/Jabodetabek transit studies reviewed (Hardi & Murad 2023, Taki et al. 2018, BPTJ)
  - [ ] Gap identified: no composite need-vs-access framework spanning full Jabodetabek
  - [ ] ~1000–1500 words
- **Blocked by**: MVP-2 (source map)
- **URL**: https://linear.app/olsera-mitra-modal/issue/MVP-10/write-related-work-section-jakartajabodetabek-transit-studies

### MVP-11 — Write methodology precedents section (r5py, H3, composite indices)
- **Status**: Todo
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

## E4 · Paper Drafting (Paper)

### MVP-12 — Write introduction
- **Status**: Todo
- **Priority**: Medium
- **AC**:
  - [ ] Problem statement, motivation, RQ
  - [ ] Contributions: 5-layer TAI, dual resolution, three-way cost model, what-if simulator
  - [ ] Paper structure overview
  - [ ] ~1500–2000 words
- **Blocked by**: MVP-9, MVP-10, MVP-11 (literature review sections)
- **URL**: https://linear.app/olsera-mitra-modal/issue/MVP-12/write-introduction

### MVP-13 — Write methods section
- **Status**: Todo
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
- **Status**: Todo
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
- **Status**: Todo
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
- **Status**: Todo
- **Priority**: Medium
- **AC**:
  - [ ] Conclusion: contribution summary, future work
  - [ ] Abstract: 250–300 words, written last
  - [ ] References compiled in APA format
- **Blocked by**: MVP-15 (discussion)
- **URL**: https://linear.app/olsera-mitra-modal/issue/MVP-16/write-conclusion-and-abstract

---

## E5 · Paper Review & Revision (Paper)

### MVP-17 — Self-review against Phase 5P checklist
- **Status**: Todo
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
- **Status**: Todo
- **Priority**: Medium
- **AC**:
  - [ ] Peer feedback incorporated (if available)
  - [ ] Citation format confirmed
  - [ ] Final proofread
- **Blocked by**: MVP-17 (self-review)
- **URL**: https://linear.app/olsera-mitra-modal/issue/MVP-18/incorporate-supervisor-feedback

---

## E6 · Data Pipeline (Product)

### MVP-19 — Download, validate, and merge GTFS feeds + LRT stations
- **Status**: Todo
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
- **Status**: Todo
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
- **Status**: Todo
- **Priority**: High
- **AC**:
  - [ ] 9 CBD zone polygons created manually
  - [ ] Strict POIs extracted via Overpass (hospitals, schools, markets, industrial, gov offices)
  - [ ] Manual verification of 10% sample
  - [ ] Output: `data/processed/poi/`
- **Blocked by**: MVP-6 (data acquisition scripts must be defined first)
- **URL**: https://linear.app/olsera-mitra-modal/issue/MVP-21/extract-strict-pois-via-overpass-api-manual-verification

### MVP-22 — Assemble BPS demographics + disaggregate to kelurahan via WorldPop
- **Status**: Todo
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
- **Status**: Todo
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
- **Status**: Todo
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
- **Status**: Todo
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

## E7 · UI Foundation (Product)

### MVP-26 — Audit existing prototype against new methodology
- **Status**: Todo
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
- **Status**: Todo
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
- **Status**: Todo
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

## E8 · Core Features (Product)

### MVP-29 — Implement quadrant map with dual-resolution toggle
- **Status**: Todo
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
- **Status**: Todo
- **Priority**: High
- **AC**:
  - [ ] Journey legs displayed: first-mile → station → ride → transfer → ride → last-mile
  - [ ] Each leg shows mode, time, fare
  - [ ] Path rendered on map as polyline
  - [ ] Side panel compares transit vs car vs motorcycle GC
- **Blocked by**: MVP-27 (real data)
- **URL**: https://linear.app/olsera-mitra-modal/issue/MVP-30/implement-cbd-journey-chain-visualization

### MVP-31 — Implement what-if station placement simulator
- **Status**: Todo
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
- **Status**: Todo
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

## E9 · Code Review & QA (Product)

### MVP-33 — Code review against Phase 5D checklist
- **Status**: Todo
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
- **Status**: Todo
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

## E10 · Deliverables (Convergence)

### MVP-35 — Final paper assembly + reference formatting
- **Status**: Todo
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
- **Status**: Todo
- **Priority**: Medium
- **AC**:
  - [ ] Cleaned datasets in public/dataset/
  - [ ] README with field glossary, source citations, methodology summary
  - [ ] License: CC BY 4.0
  - [ ] Dataset downloadable independently
- **Blocked by**: MVP-25 (analysis complete)
- **URL**: https://linear.app/olsera-mitra-modal/issue/MVP-36/package-dataset-for-public-distribution

### MVP-37 — Deploy product to Vercel + link paper and dataset
- **Status**: Todo
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
- **Status**: Todo
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
