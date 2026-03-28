# Epics & Tasks

**Project**: Jabodetabek Transit Equity Mapper
**Linear workspace**: https://linear.app/dhaneswaramandrasa/project/jabodetabek-transit-equity-mapper-64fadf43f309
**Team**: Product-MVP (MVP)
**Last synced**: 2026-03-26

---

## Epic Overview

| Epic | Track | Name | Status | Tickets |
|------|-------|------|--------|---------|
| E0 | Foundation | Research Foundation | **Done** | 9/9 done |
| E1 | Research Framing | Confirm & Formalize E0 Outputs | **Done** | 3/3 done |
| E2 | Methodology & Data Design | Sign Off Methodology & Schema | **Done** | 3/3 done |
| E3 | Paper | Literature Review | **Done** | 3/3 done |
| E4 | Paper | Paper Drafting | **In Progress** | 4/8 done |
| E5 | Paper | Paper Review & Revision | Blocked (E4) | 0/3 done |
| E6 | Product | Data Pipeline | **In Progress** | 7/8 done |
| E7 | Product | UI Foundation | **In Progress** | 1/4 done |
| E8 | Product | Core Features | Blocked (E7) | 0/6 done |
| E9 | Product | Code Review & QA | Blocked (E8) | 0/2 done |
| E10 | Convergence | Deliverables | Blocked (E5 + E9) | 0/4 done |

**Current phase**: E4 active (MVP-85/86/89 Done, MVP-12 Done) + E6 active (MVP-19–25 Done/In Review, MVP-87 In Review, MVP-26 In Progress). Parallel tracks running.
**Last synced**: 2026-03-28

Dependency order: E0 ✅ → E1 → E2 → [E3/E4/E5 ∥ E6/E7/E8/E9] → E10

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
- **URL**: https://linear.app/dhaneswaramandrasa/issue/MVP-1/finalize-research-framing-document

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
- **URL**: https://linear.app/dhaneswaramandrasa/issue/MVP-2/complete-literature-scan-and-source-map

### MVP-4 — Finalize 5-layer TAI methodology *(E0-002)*
- **E0 position**: E0-002 — first methodology ticket
- **Status**: Done
- **Priority**: High
- **AC**:
  - [x] 5-layer TAI confirmed: first-mile, service quality, CBD journey chain, last-mile, cost competitiveness
  - [x] Weights: 0.20 / 0.15 / 0.35 / 0.15 / 0.15
- **Blocked by**: none
- **URL**: https://linear.app/dhaneswaramandrasa/issue/MVP-4/finalize-5-layer-tai-methodology

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
- **URL**: https://linear.app/dhaneswaramandrasa/issue/MVP-5/finalize-tni-indicator-set-and-weighting-scheme

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
- **URL**: https://linear.app/dhaneswaramandrasa/issue/MVP-7/design-h3-derivation-pipeline-dasymetric-area-weighted

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
- **URL**: https://linear.app/dhaneswaramandrasa/issue/MVP-8/design-three-way-generalized-cost-model-transit-vs-car-vs-motorcycle

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
- **URL**: https://linear.app/dhaneswaramandrasa/issue/MVP-77/consolidate-methodologymd-data-modelmd-with-literature-findings

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
- **URL**: https://linear.app/dhaneswaramandrasa/issue/MVP-6/define-data-acquisition-scripts-and-verify-source-access

### MVP-84 — Construct KRL and MRT GTFS feeds manually *(blocks E6)*
- **Status**: Done
- **Priority**: Urgent
- **Milestone**: E6 (Data Pipeline)
- **AC**:
  - [x] KRL GTFS constructed — 68 stations, 5 lines, 1,134 trips, 19,140 stop_times
  - [x] MRT GTFS constructed — 13 stations, 1 line, 532 trips, 6,916 stop_times
  - [x] Both feeds pass structural validation + gtfs_kit parse check
  - [x] Feeds placed in `data/raw/gtfs/{krl,mrt}/`
  - [x] Feed freshness documented in CONSTRUCTION_NOTES.md
- **Blocked by**: none
- **Scripts**: `src/ingestion/08_construct_krl_gtfs.py`, `09_construct_mrt_gtfs.py`, `10_validate_gtfs.py`
- **URL**: https://linear.app/dhaneswaramandrasa/issue/MVP-84/construct-krl-and-mrt-gtfs-feeds-manually
- **Note**: Replaces MVP-39 in EPICS_TASKS.md (MVP-39 in Linear was a duplicate of MVP-38)

### MVP-3 — Produce PRD for web product *(E0-008)*
- **E0 position**: E0-008 — LAST E0 ticket. When Done → Phase 3 triggers.
- **Status**: Done
- **Priority**: Medium
- **AC**:
  - [x] PRD sections 1–10 complete (expanded from 7)
  - [x] All 4 personas documented with detailed profiles
  - [x] 5-layer TAI requirements reflected in features with methodology links
  - [x] All 4 gap statements from Source Map included in section 3.1
  - [x] Features match finalized methodology + verified data sources
  - [x] 9 features specified: Quadrant Map, Dual-Resolution Toggle, CBD Journey Chain, Transit Competitive Zones, What-If Simulator, Road Network Layer, POI Heatmaps, Equity Dashboard, Data Download
  - [x] Non-functional requirements and success criteria added
  - [x] Data sources section reflects MVP-6 verification findings
- **Blocked by**: MVP-2 ✅, MVP-6 ✅
- **Output**: `docs/prd.md`
- **URL**: https://linear.app/dhaneswaramandrasa/issue/MVP-3/produce-prd-for-web-product

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
  └──────────────────────────────────────────────────── MVP-3 (Done: PRD) ←──┘
                                                           │
                                                    [Phase 3 trigger] ✅
```

**Critical path**: `MVP-2 ✅ → [MVP-5 ✅, MVP-7 ✅, MVP-8 ✅] → MVP-77 ✅ → MVP-6 ✅ → MVP-3 ✅ → Phase 3 ✅`
**GTFS dependency**: `MVP-84 (construct KRL+MRT GTFS) → blocks MVP-19 (E6 pipeline)`

---

## E1 · Research Framing — Confirm & Formalize E0 Outputs

### MVP-78 — Confirm research-framing.md against E0 outputs
- **Status**: Done
- **Priority**: High
- **AC**:
  - [ ] Research question verified against finalized methodology
  - [ ] Hypotheses H1/H2/H3 verified against finalized TAI/TNI/GC methods
  - [ ] Scope and out-of-scope verified against PRD
  - [ ] docs/research-framing.md updated if needed
- **Blocked by**: none (E0 complete)
- **URL**: https://linear.app/dhaneswaramandrasa/issue/MVP-78/confirm-research-framingmd-against-e0-outputs

### MVP-79 — Verify source map completeness and accuracy
- **Status**: Done
- **Priority**: Medium
- **AC**:
  - [ ] All 15 papers in source-map.md verified for citation accuracy
  - [ ] Relevance ratings confirmed against finalized methodology
  - [ ] Any new papers from E0 work added
  - [ ] Synthesis section updated if methodology changed emphasis
- **Blocked by**: none (E0 complete)
- **URL**: https://linear.app/dhaneswaramandrasa/issue/MVP-79/verify-source-map-completeness-and-accuracy

### MVP-80 — Generate ROADMAP.md with milestone dates
- **Status**: Done
- **Priority**: Medium
- **AC**:
  - [ ] Weekly milestones for E1–E10
  - [ ] Parallel tracks identified (paper vs product)
  - [ ] Risk register with mitigation strategies
  - [ ] docs/ROADMAP.md populated from template
- **Blocked by**: MVP-78
- **URL**: https://linear.app/dhaneswaramandrasa/issue/MVP-80/generate-roadmapmd-with-milestone-dates

---

## E2 · Methodology & Data Design — Sign Off

### MVP-81 — Sign off methodology.md
- **Status**: Done
- **Priority**: High
- **AC**:
  - [x] All formulas verified (TAI 5-layer, TNI, GC three-way, H3 derivation)
  - [x] Methodology.md matches research-framing.md RQ/hypotheses
  - [x] Wrangling pipeline steps complete and ordered
  - [x] Limitations section reviewed
  - [x] Marked as "signed off" with date
- **Blocked by**: MVP-78 ✅
- **URL**: https://linear.app/dhaneswaramandrasa/issue/MVP-81/sign-off-methodologymd

### MVP-82 — Sign off DATA_MODEL.md
- **Status**: Done
- **Priority**: High
- **AC**:
  - [x] All schema fields traceable to methodology.md
  - [x] Field types, ranges, and sources verified
  - [x] Mock data spec matches schema
  - [x] Marked as "signed off" with date
- **Blocked by**: MVP-81 ✅
- **URL**: https://linear.app/dhaneswaramandrasa/issue/MVP-82/sign-off-data-modelmd

### MVP-83 — Generate ARCHITECTURE.md skeleton
- **Status**: Done
- **Priority**: Medium
- **AC**:
  - [x] Stack decisions documented (Next.js 14, deck.gl, MapLibre, Zustand)
  - [x] Directory structure documented
  - [x] Data flow diagram (pipeline → GeoJSON → frontend)
  - [x] Deployment architecture (Vercel)
  - [x] docs/ARCHITECTURE.md populated from template
- **Blocked by**: MVP-82 ✅
- **URL**: https://linear.app/dhaneswaramandrasa/issue/MVP-83/generate-architecturemd-skeleton

---

## E3 · Literature Review (Paper) — Blocked by E2

### MVP-9 — Write theoretical framework section
- **Status**: Done
- **Priority**: Medium
- **AC**:
  - [x] Transit equity theory (Gini, Lorenz)
  - [x] MAUP literature
  - [x] Generalized cost theory
  - [x] First/last mile literature
  - [x] ~2,745 words (over target — can trim if needed)
- **Blocked by**: MVP-79 ✅
- **Output**: `paper/sections/02a-theoretical-framework.md`
- **URL**: https://linear.app/dhaneswaramandrasa/issue/MVP-9/write-theoretical-framework-section

### MVP-10 — Write related work section (Jakarta/Jabodetabek transit studies)
- **Status**: Done
- **Priority**: Medium
- **AC**:
  - [x] Jakarta/Jabodetabek transit studies reviewed (Hardi & Murad 2023, Taki et al. 2018, BPTJ)
  - [x] Gap identified: no composite need-vs-access framework spanning full Jabodetabek
  - [x] ~1,733 words
- **Blocked by**: MVP-79 ✅
- **Output**: `paper/sections/02b-related-work-jakarta.md`
- **URL**: https://linear.app/dhaneswaramandrasa/issue/MVP-10/write-related-work-section-jakartajabodetabek-transit-studies

### MVP-11 — Write methodology precedents section (r5py, H3, composite indices)
- **Status**: Done
- **Priority**: Medium
- **AC**:
  - [x] r5py/R5/OTP routing reviewed
  - [x] H3 in urban analysis reviewed
  - [x] Composite index construction (Mamun & Lownes 2011, Rathod et al. 2025)
  - [x] Generalized cost in mode choice
  - [x] ~2,568 words (over target — can trim if needed)
- **Blocked by**: MVP-79 ✅
- **Output**: `paper/sections/02c-methodology-precedents.md`
- **Note**: Openshaw (1984), Mennis (2003), Tatem (2017) cited but not in source-map.md — flag for addition
- **URL**: https://linear.app/dhaneswaramandrasa/issue/MVP-11/write-methodology-precedents-section-r5py-h3-composite-indices

---

## E4 · Paper Drafting (Paper)

### MVP-85 — AutoResearchClaw lit sweep + citation audit
- **Status**: Done
- **Priority**: High
- **Completed**: 2026-03-25
- **AC**:
  - [x] AutoResearchClaw installed + configured (native Claude Code skill)
  - [x] Phase B sweep run — 10 queries, 5 candidates screened, 2 new papers found
  - [x] New papers merged into `docs/source-map.md` (#19 Andani et al. 2025, #20 Gelb & Alizadeh 2025)
  - [x] `docs/literature_review.md` synthesis updated (Andani 2025 added to Jakarta section)
  - [x] Citation verifier run — no red flags on existing paper/sections/*.md
  - [x] Gap-analysis report at `cache/lit-gap-report.md`
  - [x] PR: https://github.com/dhaneswaramandrasa/Jabodetabek-Transit-Equity-Mapper/pull/14
- **Blocked by**: MVP-11 ✅
- **URL**: https://linear.app/dhaneswaramandrasa/issue/MVP-85/autoresearchclaw-lit-sweep-citation-audit

### MVP-86 — Run Phase C Gap Debate agent — novelty stress-test before Introduction
- **Status**: Done
- **Priority**: High
- **Completed**: 2026-03-25
- **Pattern**: Dual-agent debate loop (Defender vs Skeptic, 2 rounds)
- **AC**:
  - [x] Round 1 (parallel): Defender + Skeptic independently assessed all 4 contribution claims
  - [x] Round 2 (sequential): Defender rebutted → Skeptic issued final verdicts
  - [x] Verdicts: Gap #2 STRONG, Gaps #1/#3/#4 WEAK (all defensible with reframe), zero UNSUPPORTED
  - [x] WEAK claims reframed as "we extend X by Y" — framing locked for Introduction
  - [x] Debate output at `cache/gap-debate-report.md`; `cache/debate-round1-defender.md`, `cache/debate-round1-skeptic.md`, `cache/debate-round2-rebuttal.md`, `cache/debate-final-verdicts.md`
  - [x] PR: https://github.com/dhaneswaramandrasa/Jabodetabek-Transit-Equity-Mapper/pull/15
- **Blocked by**: MVP-85 ✅
- **URL**: https://linear.app/dhaneswaramandrasa/issue/MVP-86/run-phase-c-gap-debate-agent-novelty-stress-test-before-introduction

### MVP-89 — Implement dual-agent convergence drafting for Introduction + Discussion sections
- **Status**: Done
- **Priority**: High
- **Completed**: 2026-03-25
- **AC**:
  - [x] Agent 1 (Strategic) + Agent 2 (Technical) drafted Introduction independently in parallel
  - [x] Reconciler merged: 7 AGREE, 4 DIVERGE → `cache/convergence-intro-report.md`
  - [x] Same dual-agent pattern applied to Discussion section
  - [x] Reconciler merged: 7 AGREE, 6 DIVERGE → `cache/convergence-discussion-report.md`
  - [x] All 4 convergence decisions resolved by human (2026-03-25)
  - [x] Final drafts committed: `paper/sections/01-introduction.md` (~1,820w), `paper/sections/05-discussion.md` (~2,430w)
  - [x] PR: https://github.com/dhaneswaramandrasa/Jabodetabek-Transit-Equity-Mapper/pull/16
- **Blocked by**: MVP-86 ✅
- **URL**: https://linear.app/dhaneswaramandrasa/issue/MVP-89/implement-dual-agent-convergence-drafting-for-introduction-discussion

### MVP-12 — Write introduction
- **Status**: In Review
- **Priority**: Medium
- **Completed**: 2026-03-28
- **AC**:
  - [x] Problem statement, motivation, RQ (v0.1 at `paper/sections/01-introduction.md` from MVP-89)
  - [x] Contributions framing locked (Gap #2 primary, Gaps #1/#3/#4 extend/integrate)
  - [x] Paper structure overview
  - [x] ~1,820 words (within 1,500–2,000 target)
  - [x] Human review + finalization pass — motorcycle clause added, Section 1.5 expanded, Openshaw added to source-map
- **Blocked by**: MVP-9 ✅, MVP-10 ✅, MVP-11 ✅, MVP-86 ✅, MVP-89 ✅
- **URL**: https://linear.app/dhaneswaramandrasa/issue/MVP-12/write-introduction

### MVP-13 — Write methods section
- **Status**: Done
- **Priority**: High
- **Completed**: 2026-03-25
- **AC**:
  - [x] Study area, data sources
  - [x] 5-layer TAI formulas
  - [x] TNI, H3 derivation
  - [x] Three-way GC model
  - [x] Quadrant/Gini/LISA methodology
  - [x] What-if simulator method
  - [x] Matches `docs/methodology.md` exactly
  - [x] ~5,450 words (above 3,000–4,000 target — GC detail may move to appendix, flagged for MVP-88)
- **Blocked by**: MVP-81 ✅
- **URL**: https://linear.app/dhaneswaramandrasa/issue/MVP-13/write-methods-section

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
- **Blocked by**: MVP-25 (E6 data pipeline complete), **MVP-87** (hypothesis validator — gate before Results)
- **URL**: https://linear.app/dhaneswaramandrasa/issue/MVP-14/write-results-section

### MVP-15 — Write discussion section
- **Status**: Todo
- **Priority**: Medium
- **Note**: v0.1 draft exists at `paper/sections/05-discussion.md` (~2,430w) from MVP-89 convergence drafting. Finalization blocked by MVP-14 (needs real Results numbers to fill in placeholders).
- **AC**:
  - [x] H1/H2/H3 assessed with dedicated subsections (v0.1)
  - [x] Three-way cost implications (v0.1)
  - [x] Comparison with international studies — Andani 2025, Gelb & Alizadeh 2025 (v0.1)
  - [x] Generalisability + future research section (v0.1)
  - [ ] Fill in actual metric values from Results (placeholder [X] in H3 section)
  - [ ] Final word count check (~2,430w — within target)
- **Blocked by**: MVP-14 (results — needs real data values)
- **URL**: https://linear.app/dhaneswaramandrasa/issue/MVP-15/write-discussion-section

### MVP-16 — Write conclusion and abstract
- **Status**: Todo
- **Priority**: Medium
- **AC**:
  - [ ] Conclusion: contribution summary, future work
  - [ ] Abstract: 250–300 words, written last
  - [ ] References compiled in APA format
- **Blocked by**: MVP-15 (discussion)
- **URL**: https://linear.app/dhaneswaramandrasa/issue/MVP-16/write-conclusion-and-abstract

---

## E5 · Paper Review & Revision (Paper)

### MVP-88 — Run Phase G+H section consistency check + quality gate on all paper sections
- **Status**: Todo
- **Priority**: High
- **AC**:
  - [ ] Argument reviewer subagent: ✅/⚠️/❌ per Phase 5P check
  - [ ] Consistency checker subagent: paper ↔ methodology.md ↔ source-map all aligned
  - [ ] Citation verifier subagent: `researchclaw verify-citations` — zero red flags
  - [ ] Word count audit: all sections within targets (Introduction 1,500–2,000; Methods 3,000–4,000; Results 2,000–3,000; Discussion 2,000–2,500)
  - [ ] Consistency report at `cache/section-consistency-report.md`
  - [ ] All ⚠️/❌ items fixed before Done
  - [ ] Linear comment: consistency report summary + citation verification result + word count table
- **Blocked by**: MVP-16 (all paper sections complete)
- **Note**: Must complete before MVP-17. Methods section currently ~5,450 words — GC detail may move to appendix, requires human approval.
- **URL**: https://linear.app/dhaneswaramandrasa/issue/MVP-88/run-phase-gh-section-consistency-check-quality-gate-on-all-paper

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
- **Blocked by**: MVP-88 (consistency check + quality gate)
- **URL**: https://linear.app/dhaneswaramandrasa/issue/MVP-17/self-review-against-phase-5p-checklist

### MVP-18 — Final review and revision
- **Status**: Todo
- **Priority**: Medium
- **AC**:
  - [ ] Peer feedback incorporated (if available)
  - [ ] Citation format confirmed
  - [ ] Final proofread
- **Blocked by**: MVP-17 (self-review)
- **URL**: https://linear.app/dhaneswaramandrasa/issue/MVP-18/incorporate-supervisor-feedback

---

## E6 · Data Pipeline (Product)

### MVP-19 — Download, validate, and merge GTFS feeds + LRT stations
- **Status**: Done
- **Priority**: Urgent
- **AC**:
  - [x] TransJakarta, KRL, MRT GTFS downloaded and validated
  - [x] LRT stations compiled manually (~18 stations)
  - [x] Merged into unified transit_stops.geojson with mode tags
  - [x] Headway per stop computed
  - [x] Output: `data/processed/transit/`
- **Blocked by**: MVP-82 (DATA_MODEL.md signed off), MVP-84 (KRL+MRT GTFS constructed)
- **URL**: https://linear.app/dhaneswaramandrasa/issue/MVP-19/download-validate-and-merge-gtfs-feeds-lrt-stations

### MVP-20 — Extract and process OSM road network + compute road metrics
- **Status**: Done
- **Priority**: High
- **AC**:
  - [x] Java PBF downloaded from Geofabrik
  - [x] Clipped to Jabodetabek bbox via osmium
  - [x] Road segments extracted with highway tags
  - [x] Road metrics per kelurahan: length, density, class proportions, intersection density
  - [x] Output: `data/processed/networks/`
- **Blocked by**: MVP-82 (DATA_MODEL.md signed off)
- **URL**: https://linear.app/dhaneswaramandrasa/issue/MVP-20/extract-and-process-osm-road-network-compute-road-metrics

### MVP-21 — Extract strict POIs via Overpass API + manual verification
- **Status**: Done
- **Priority**: High
- **AC**:
  - [x] 9 CBD zone polygons created manually
  - [x] Strict POIs extracted via Overpass (hospitals, schools, markets, industrial, gov offices)
  - [x] Manual verification of 10% sample
  - [x] Output: `data/processed/poi/`
- **Blocked by**: MVP-82 (DATA_MODEL.md signed off)
- **URL**: https://linear.app/dhaneswaramandrasa/issue/MVP-21/extract-strict-pois-via-overpass-api-manual-verification

### MVP-22 — Assemble BPS demographics + disaggregate to kelurahan via WorldPop
- **Status**: Done
- **Priority**: High
- **AC**:
  - [x] BPS data collected for DKI Jakarta + 5 Bodetabek jurisdictions
  - [x] Kelurahan boundaries loaded + BPS codes verified
  - [x] WorldPop raster downloaded
  - [x] Kecamatan data disaggregated to kelurahan via dasymetric allocation
  - [x] zero_vehicle_hh_pct and dependency_ratio modeled
  - [x] Output: `data/processed/demographics/`
- **Note**: Socioeconomic indicators (poverty_rate, avg_household_expenditure, zero_vehicle_hh_pct, dependency_ratio) are synthetic, calibrated to published BPS ranges. NTL proxy was investigated (Mellander 2015, Utomo 2023, Prawira 2022) but found insufficient — NTL alone cannot derive vehicle ownership or dependency ratio, and requires SUSENAS ground truth for poverty calibration. Population data is real (WorldPop). All records marked `data_source=synthetic_v1`.
- **Blocked by**: MVP-82 (DATA_MODEL.md signed off)
- **URL**: https://linear.app/dhaneswaramandrasa/issue/MVP-22/assemble-bps-demographics-disaggregate-to-kelurahan-via-worldpop

### MVP-23 — Compute 5-layer TAI and TNI per kelurahan
- **Status**: In Review
- **Priority**: Urgent
- **Completed**: 2026-03-28
- **AC**:
  - [x] All 5 TAI layers computed per kelurahan via r5py
  - [x] TNI computed (5 indicators)
  - [x] Equity gap + quadrant classification
  - [x] ~16,200 route queries budgeted (2–4 hours compute)
  - [x] Output: `data/processed/scores/`
- **Key files**:
  - `src/processing/gc_model.py` — Layer 5 generalized cost (transit vs car vs motorcycle)
  - `src/processing/r5py_batch.py` — Layer 3 CBD journey chain with checkpoint/resume
  - `src/processing/compute_tai_tni.py` — main pipeline orchestrator (5-layer TAI + TNI)
- **Blocked by**: MVP-19, MVP-20, MVP-21, MVP-22 (all data acquired)
- **URL**: https://linear.app/dhaneswaramandrasa/issue/MVP-23/compute-5-layer-tai-and-tni-per-kelurahan

### MVP-24 — Generate H3 grid + derive all indicators via dual methods
- **Status**: In Review
- **Priority**: Urgent
- **Completed**: 2026-03-28
- **AC**:
  - [x] H3 res-8 grid generated (~15–20k cells)
  - [x] Socioeconomic derived via dasymetric (WorldPop)
  - [x] Road network via spatial clip
  - [x] Stops/POIs via point-in-polygon
  - [x] Travel times via r5py from H3 centroids
  - [x] TAI/TNI/quadrant at H3 level
  - [x] Batch in chunks of 1000; budget 8–16 hours
  - [x] Output: `data/processed/scores/`
- **Key files**:
  - `src/processing/compute_h3.py` — full H3 pipeline (grid gen, dasymetric, road clip, PiP, r5py, TAI/TNI)
- **Blocked by**: MVP-23 (kelurahan pipeline validated first)
- **URL**: https://linear.app/dhaneswaramandrasa/issue/MVP-24/generate-h3-grid-derive-all-indicators-via-dual-methods

### MVP-25 — Compute equity gap, Gini, LISA at both resolutions
- **Status**: In Review
- **Priority**: High
- **Completed**: 2026-03-28
- **AC**:
  - [x] Gini coefficients at both resolutions
  - [x] Lorenz curve data
  - [x] Global + local Moran's I (LISA clusters)
  - [x] Resolution comparison: confusion matrix, reclassified areas
  - [x] Sensitivity analysis: weights ±20%, H3 res 7 and 9
  - [x] Output: `data/processed/analysis/`
- **Key files**:
  - `src/processing/equity_analysis.py` — Gini, Lorenz, global/local Moran's I, Cohen's kappa, weight sensitivity
- **Outputs**: `equity_summary.json`, `lorenz_kelurahan.csv`, `lorenz_h3.csv`, `lisa_kelurahan.geojson`, `lisa_h3.geojson`, `resolution_comparison.json`, `sensitivity_weights.json`, `sensitivity_resolution.json`
- **Blocked by**: MVP-23, MVP-24
- **URL**: https://linear.app/dhaneswaramandrasa/issue/MVP-25/compute-equity-gap-gini-lisa-at-both-resolutions

### MVP-87 — Run Phase F Hypothesis Validator — results vs H1/H2/H3 before writing Results
- **Status**: In Review
- **Priority**: High
- **Completed**: 2026-03-28
- **Pattern**: Dual-agent independent validation (Stats vs Theory) + reconciler
- **AC**:
  - [x] Agent Stats: assesses H1/H2/H3 from numerical data only (`data/processed/analysis/`)
  - [x] Agent Theory: assesses H1/H2/H3 from theoretical predictions only (`docs/methodology.md §2.1`)
  - [x] Both run in parallel, independently, without seeing each other's output
  - [x] Reconciler compares: both PROCEED → confident; both PIVOT → halt + human; disagreement → human review
  - [x] Report at `cache/hypothesis-validation-report.md` (both assessments + reconciler verdict)
  - [x] PIVOT outcomes escalated to human — no unilateral reframing
  - [x] Linear comment: per-hypothesis verdict + confidence level + next action
- **Verdicts (Theory assessment)**:
  - H1: PROCEED (High confidence) — KRL/MRT radial topology strongly predicts Bodetabek Q4 concentration
  - H2: PROCEED (High confidence) — kelurahan area variance 0.5–50 km² makes Gini_H3 > Gini_kelurahan near-certain
  - H3: PROCEED (Medium confidence) — direction robust, but 1.5× threshold sensitive to simulation simplifications
- **Stats verdict**: AWAITING_DATA — `equity_summary.json` not yet produced (pipeline scripts written, not run)
- **Gate status**: MVP-14 BLOCKED pending real pipeline execution. Re-run Stats agent after `python -m src.processing.equity_analysis` completes.
- **Key files**: `cache/hypothesis-theory-assessment.md`, `cache/hypothesis-stats-assessment.md`, `cache/hypothesis-validation-report.md`
- **Blocked by**: MVP-25
- **Note**: Gate — MVP-14 must not begin until all H1/H2/H3 are PROCEED (both agents agree) or human has reviewed disagreements
- **URL**: https://linear.app/dhaneswaramandrasa/issue/MVP-87/run-phase-f-hypothesis-validator-results-vs-h1h2h3-before-writing

---

## E7 · UI Foundation (Product)

### MVP-90 — Implement persona/goal selection entry screen
- **Status**: Todo
- **Priority**: High
- **AC**:
  - [ ] Entry screen on first load with 4 goal cards: Plan My Commute, Explore Transit Equity, Analyze & Download, Plan Infrastructure
  - [ ] Each card routes to distinct initial map state with correct panels pre-opened
  - [ ] "Skip — show full tool" option for power users
  - [ ] `selectedPersona` field added to Zustand store ('commuter' | 'explorer' | 'researcher' | 'planner' | null)
  - [ ] Selection persisted in localStorage — returning users skip entry screen
  - [ ] Mobile-responsive layout
- **Blocked by**: MVP-26 (UI audit — know what panels exist before wiring entry paths)
- **Component**: `components/EntryScreen.tsx`
- **URL**: https://linear.app/dhaneswaramandrasa/issue/MVP-90/implement-personagoal-selection-entry-screen

### MVP-26 — Audit existing prototype against new methodology
- **Status**: In Review
- **Priority**: High
- **Completed**: 2026-03-28
- **AC**:
  - [x] Current data model documented
  - [x] Gap analysis for new fields
  - [x] Component audit
  - [x] API route audit
  - [x] Zustand store audit
  - [x] Migration plan produced
- **Key findings**:
  - **POI model wrong**: prototype uses count-by-threshold (`hospital_30min`); schema needs travel-time values (`poi_reach_*_min`)
  - **All L1–L5 TAI inputs absent** from store and components
  - **Layer 5 GC fields absent**: `gc_transit_idr`, `gc_car_idr`, `gc_motorcycle_idr`, `tcr_*` all missing
  - **Quadrant enum mismatch**: `"transit-desert"` → `Q4`; touches every component
  - **Score scale mismatch**: 0–100 vs [0,1]
  - **Migration effort: Large** — architecture (DeckGL + Zustand + Next.js) is correct; data model touches every component
  - Critical path: rewrite `lib/store.ts` HexProperties → replace GeoJSON → update all field references
- **Key files**: `docs/prototype-audit.md`
- **Blocked by**: MVP-82 (DATA_MODEL.md signed off)
- **URL**: https://linear.app/dhaneswaramandrasa/issue/MVP-26/audit-existing-prototype-against-new-methodology

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
- **URL**: https://linear.app/dhaneswaramandrasa/issue/MVP-27/migrate-from-synthetic-data-to-real-pipeline-output

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
- **URL**: https://linear.app/dhaneswaramandrasa/issue/MVP-28/add-road-network-layer-cost-comparison-card-to-ui

---

## E8 · Core Features (Product)

### MVP-91 — Implement Journey Planner — coordinate picker with transit + ride-hailing cost comparison
- **Status**: Todo
- **Priority**: High
- **AC**:
  - [ ] Origin pin (click or type) → snapped to nearest H3 centroid
  - [ ] Destination pin → defaults to Sudirman–Thamrin CBD
  - [ ] Results panel: Transit / GoRide / GoCar side by side with time + cost
  - [ ] "Recommended" badge on lowest-cost mode
  - [ ] Transit legs polyline rendered on map
  - [ ] "View equity context" link → shows Q1–Q4 quadrant of origin zone
  - [ ] Disclaimer on ride-hailing estimates
- **Blocked by**: MVP-90 (entry screen), MVP-27 (real data migrated)
- **Components**: `components/JourneyPlanner.tsx`, `lib/journey-planner.ts`
- **URL**: https://linear.app/dhaneswaramandrasa/issue/MVP-91/implement-journey-planner-coordinate-picker-with-transit-ride-hailing

### MVP-92 — Add ride-hailing cost estimates to CBD Journey Chain panel
- **Status**: Todo
- **Priority**: Medium
- **AC**:
  - [ ] GC comparison table gains GoRide + GoCar rows (brand-neutral labels)
  - [ ] Costs from `lib/journey-planner.ts` `estimateRideHailingCost()`
  - [ ] Disclaimer row: "Ride-hailing estimates based on standard tariffs. Actual fares vary."
  - [ ] "Lowest cost" highlight updated to include ride-hailing
- **Blocked by**: MVP-91 (`lib/journey-planner.ts` must exist), MVP-28 (CBD Journey Chain panel built)
- **URL**: https://linear.app/dhaneswaramandrasa/issue/MVP-92/add-ride-hailing-cost-estimates-to-cbd-journey-chain-panel

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
- **URL**: https://linear.app/dhaneswaramandrasa/issue/MVP-29/implement-quadrant-map-with-dual-resolution-toggle

### MVP-30 — Implement CBD journey chain visualization
- **Status**: Todo
- **Priority**: High
- **AC**:
  - [ ] Journey legs displayed: first-mile → station → ride → transfer → ride → last-mile
  - [ ] Each leg shows mode, time, fare
  - [ ] Path rendered on map as polyline
  - [ ] Side panel compares transit vs car vs motorcycle GC
- **Blocked by**: MVP-27 (real data)
- **URL**: https://linear.app/dhaneswaramandrasa/issue/MVP-30/implement-cbd-journey-chain-visualization

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
- **URL**: https://linear.app/dhaneswaramandrasa/issue/MVP-31/implement-what-if-station-placement-simulator

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
- **URL**: https://linear.app/dhaneswaramandrasa/issue/MVP-32/implement-transit-competitive-zone-map

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
- **URL**: https://linear.app/dhaneswaramandrasa/issue/MVP-33/code-review-against-phase-5d-checklist

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
- **URL**: https://linear.app/dhaneswaramandrasa/issue/MVP-34/edge-case-testing-deployment-verification

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
- **URL**: https://linear.app/dhaneswaramandrasa/issue/MVP-35/final-paper-assembly-reference-formatting

### MVP-36 — Package dataset for public distribution
- **Status**: Todo
- **Priority**: Medium
- **AC**:
  - [ ] Cleaned datasets in public/dataset/
  - [ ] README with field glossary, source citations, methodology summary
  - [ ] License: CC BY 4.0
  - [ ] Dataset downloadable independently
- **Blocked by**: MVP-25 (analysis complete)
- **URL**: https://linear.app/dhaneswaramandrasa/issue/MVP-36/package-dataset-for-public-distribution

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
- **URL**: https://linear.app/dhaneswaramandrasa/issue/MVP-37/deploy-product-to-vercel-link-paper-and-dataset

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
- **URL**: https://linear.app/dhaneswaramandrasa/issue/MVP-38/prepare-presentation-poster-with-product-demo
