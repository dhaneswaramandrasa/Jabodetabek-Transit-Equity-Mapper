# Project State

**Last updated**: 2026-04-11
**Active ticket**: MVP-27 — In Review (PR #28 open)
**Branch**: e7/mvp-27-migrate-real-data

---

## Current Focus

**Phase**: E7 (UI Foundation) — MVP-27 data migration done, PR #28 open.
This is a **portfolio / independent research project** — no academic gating.

## Last Session Summary (2026-04-11)

- **MVP-27 DONE** (this session): Real pipeline data migrated to transit-access web app
  - Created `scripts/export_to_web.py` — renames H3 fields to DATA_MODEL.md, exports both GeoJSONs
  - Full rewrite of `store.ts` HexProperties/Demographics/MapStats; EquityQuadrant → Q1/Q2/Q3/Q4
  - Updated colorScale.ts (domain 0–1), AccessibilityMap.tsx (file paths + field refs), TransitScoreCard.tsx (5-layer breakdown), DemographicsCard.tsx, MapLegend.tsx, useDemographics.ts, useAISummary.ts, useReachablePOIs.ts, useTransitStops.ts
  - Build passes ✅; PR #28 open
  - `h3_scores.geojson` = 9,083 features (17.9MB — note for MVP-37 size opt)
  - `kelurahan_scores.geojson` = 1,502 features (2.8MB)
- **MVP-14 DONE** (prior session): Results section, 2,543 words
- **Previously completed**: E0–E3, MVP-84/13/85/86/87/89/98/99/100

## Blockers

- **L4/L5 still flat** — L4 (last-mile) and L5 (cost competitiveness) don't use r5py routing; L4 uses road connectivity proxy, L5 uses TCR proxy from travel time. Acceptable for current analysis.
- **H3 field name mismatches** (30 fields) — must rename before MVP-27 (migrate to real data).
- **H3 routing coverage 11.2%** — 88.8% of H3 cells have no transit route (use 180 min fallback). This is the correct real-world picture (most of Jabodetabek is not transit-accessible) but note this in Results section limitations.

## Next Action

1. **Merge PR #28** (MVP-27) — smoke test in dev: load map, click kelurahan zone, verify TAI/TNI [0,1] values and Q1–Q4 quadrant display
2. **MVP-90** — Persona/goal selection entry screen (unblocked by MVP-27)
3. **MVP-29** — Quadrant choropleth map with dual-resolution toggle (unblocked by MVP-27)
4. **MVP-15 (Discussion)** — fill placeholders with real metric values (paper track)
5. **MVP-88** — Section consistency check gate (paper track)

## Pipeline Status (as of 2026-03-30)

| File | Status | Notes |
|---|---|---|
| `data/processed/scores/kelurahan_scores.geojson` | ✅ 1,502 rows | L3 via r5py; L4/L5 still placeholder 0.5 |
| `data/processed/scores/h3_scores.geojson` | ✅ 9,083 cells | L3 via r5py (1,021/9,083 routed; 88.8% fallback 180 min) |
| `data/processed/analysis/equity_summary.json` | ✅ | Re-run with r5py kelurahan data |
| `data/processed/analysis/lorenz_*.csv` | ✅ | Updated |
| `data/processed/analysis/lisa_*.geojson` | ✅ | Updated |
| `data/processed/analysis/resolution_comparison.json` | ✅ | Cohen's kappa=0.6094, 29.2% reclassified |
| `notebooks/comparison_r5py_vs_baseline.ipynb` | ✅ | r5py vs no-r5py visual comparison |
| `notebooks/eda_pipeline_output.ipynb` | ✅ | Full EDA with visualizations |

## EDA Key Numbers (for Results section — r5py data)

- Q4 transit deserts: 415 kelurahan (27.6%), 2,545 H3 (28.0%)
- **Gini TAI**: kelurahan=0.2441, H3=**0.6128** (r5py — H2 CONFIRMED: H3 shows more inequality)
- Gini equity gap: kelurahan=0.2608, H3=0.2003
- Cohen's kappa: 0.6124 (strong agreement; 29.0% reclassified)
- **Global Moran's I (TAI)**: kelurahan=0.8876, H3=**0.9447** (very strong spatial clustering)
- TAI mean: kelurahan=0.256, H3=0.119 (H3 shows lower mean — more transit deserts visible)
- **JVM note**: Use `JAVA_HOME=/opt/homebrew/opt/openjdk@21/libexec/openjdk.jdk/Contents/Home` for r5py

## Open Questions

- H3 routing coverage 11.2% — methodologically valid (reflects true transit coverage gaps) but should be noted in Results limitations
- Methods section is ~5,450 words (above target). MVP-88 will flag for human decision.
- MVP-89 convergence decisions resolved 2026-03-25. Introduction + Discussion v0.1 ready for MVP-12.
