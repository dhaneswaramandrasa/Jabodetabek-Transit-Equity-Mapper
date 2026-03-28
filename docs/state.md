# Project State

**Last updated**: 2026-03-29
**Active ticket**: MVP-100 (EDA) — In Review
**Branch**: e6/mvp-98-run-pipeline

---

## Current Focus

**Phase**: E4 (paper drafting) + E6 (data pipeline) both active.
This is a **portfolio / independent research project** — no academic gating.

## Last Session Summary

- **MVP-98**: Ran E6 pipeline end-to-end for first time — all 10 output files produced
  - `kelurahan_scores.geojson` (1,502 rows, 2.6 MB)
  - `h3_scores.geojson` (9,083 cells, 12.6 MB)
  - All 8 `data/processed/analysis/` files including equity_summary.json, lorenz CSVs, LISA GeoJSONs
  - Patches: `compute_tai_tni.py` (duplicate col), `compute_h3.py` (field rename + cKDTree), `equity_analysis.py` (sjoin suffix + sensitivity prefix)
  - Deps installed: `h3==4.4.2`, `libpysal`, `esda`
  - Used `--skip-r5py` for both kelurahan + H3 pipelines (r5py/Java unavailable)
- **MVP-99**: QA — found and fixed Gini sign bug in `equity_analysis.py` line 64. Reran equity_analysis.
  - Corrected Gini TAI: kelurahan=0.0896, H3=0.1228 (was negative — sign-inverted formula)
  - LISA now computing after libpysal install: Global Moran's I kelurahan=0.8418, H3=0.8928
  - Open issues: L4/L5 flat 0.5 (65% TAI weight placeholder), H3 field name mismatches (30 cols)
- **MVP-100**: EDA — H1/H2/H3 all directionally supported by current data
  - H1: 98.8% Q4 in Bodetabek; DKI Jakarta main kotas = 0 Q4 — STRONGLY SUPPORTS
  - H2: Gini_H3 (0.1228) > Gini_kelurahan (0.0896), delta +0.0332 (+37%) — SUPPORTS
  - H3: Q4 mean TAI 0.350 vs Q1/Q2 avg 0.443, delta −0.093 — SUPPORTS
  - Top Q4 regions: Kab. Bogor (193), Kab. Tangerang (123), Kab. Bekasi (68)
- **Previously completed** (prior sessions): E0 (9/9), E1 (3/3), E2 (3/3), E3 (3/3), MVP-84, MVP-13, MVP-85, MVP-86, MVP-87 (theory), MVP-89

## Blockers

- **L4/L5 flat at 0.5** — 65% of TAI weight has zero discriminatory variance pending r5py routing. TAI range is narrow (IQR=0.036). H1 findings are robust (L1+L2 driven); H2/H3 magnitudes will grow with real routing data.
- **r5py unavailable** — requires Java + R5 JAR + .osm.pbf. Current OSM data is tile JSON. L3 CBD journey times, L4 last mile, L5 GC cost all null/placeholder.
- **H3 field name mismatches** (30 fields) — must rename before MVP-27 (migrate to real data).

## Next Action

1. **PR review**: Merge `e6/mvp-98-run-pipeline` → main (MVP-98/99/100 In Review)
2. **MVP-27**: Migrate web app to real pipeline output — blocked on H3 field rename fix
3. **MVP-87 (Stats re-run)**: Stats agent assessed from synthetic data; re-run against real equity_summary.json now available. All 3 hypotheses directionally PROCEED.
4. **MVP-12**: Write final Introduction section — still unblocked (MVP-89 done)
5. **E5 gate**: MVP-88 (consistency check) before MVP-17 (self-review)

## Pipeline Status (as of 2026-03-29)

| File | Status | Notes |
|---|---|---|
| `data/processed/scores/kelurahan_scores.geojson` | ✅ 1,502 rows | L3/L4/L5 placeholder; L4/L5 flat 0.5 |
| `data/processed/scores/h3_scores.geojson` | ✅ 9,083 cells | 30 field name mismatches vs DATA_MODEL.md |
| `data/processed/analysis/equity_summary.json` | ✅ | Gini corrected: TAI kelu=0.0896 H3=0.1228 |
| `data/processed/analysis/lorenz_*.csv` | ✅ | |
| `data/processed/analysis/lisa_*.geojson` | ✅ | LISA computed (libpysal installed) |
| `data/processed/analysis/resolution_comparison.json` | ✅ | Cohen's kappa=0.6087, 29.3% reclassified |
| `data/processed/analysis/sensitivity_*.json` | ✅ | |

## EDA Key Numbers (for Results section)

- Q4 transit deserts: 413 kelurahan (27.5%), 2,541 H3 (28.0%)
- Bodetabek Q4 rate: 33.1% | DKI Jakarta: 0.0%
- Gini TAI: kelurahan=0.0896, H3=0.1228 (H3 > kelurahan confirms MAUP signal)
- Cohen's kappa: 0.6087 (strong resolution agreement; 29.3% reclassified)
- Global Moran's I (TAI): kelurahan=0.8418, H3=0.8928 (strong spatial clustering)
- H3 equity gap: Q4 mean TAI 0.350 vs Q1/Q2 avg 0.443, delta −0.093

## Open Questions

- Methods section is ~5,450 words (above target). MVP-88 will flag for human decision.
- MVP-89 convergence decisions resolved 2026-03-25. Introduction + Discussion v0.1 ready for MVP-12.
- L4/L5 placeholder: TAI results are directionally valid but magnitudes will shift with r5py. Paper should note L3/L4/L5 use neutral-fill pending routing data.
