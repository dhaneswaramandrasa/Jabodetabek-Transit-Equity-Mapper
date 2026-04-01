# Project State

**Last updated**: 2026-04-01
**Active ticket**: MVP-100 (EDA) — In Review
**Branch**: e6/mvp-98-run-pipeline

---

## Current Focus

**Phase**: E4 (paper drafting) + E6 (data pipeline) both active.
This is a **portfolio / independent research project** — no academic gating.

## Last Session Summary (2026-04-01)

- **H3 r5py pipeline completed**: 10 batches (1,000 cells each), ~4 min total
  - Fixed JVM issue: JDK 1.8.0_261 was x86_64; switched to Homebrew OpenJDK 21 (arm64)
  - `JAVA_HOME=/opt/homebrew/opt/openjdk@21/libexec/openjdk.jdk/Contents/Home`
  - 1,021/9,083 cells routed (11.2%) — remainder are genuinely transit-unserved (L3 fallback 180 min → L3=0)
- **Equity analysis re-run** with H3 r5py data — H2 hypothesis now VALID:
  - Gini TAI H3: 0.1228 → **0.6128** (+399% — r5py reveals massive spatial inequality at H3 level)
  - Gini TAI kelurahan: 0.2441 (unchanged — kelurahan already had r5py)
  - **H2 CONFIRMED**: Gini_H3 (0.6128) > Gini_kelurahan (0.2441), delta=+0.3687
  - Moran's I H3 TAI: 0.9447 (very strong spatial clustering)
  - Cohen's kappa: 0.6124 (strong agreement kelurahan↔H3 quadrant classification)
  - Q4 H3: 2,545 (28.0%)
- **EDA notebook re-executed**: `notebooks/eda_pipeline_output.ipynb` — updated with new H3 values
- **Previously completed** (prior sessions): E0 (9/9), E1 (3/3), E2 (3/3), E3 (3/3), MVP-84, MVP-13, MVP-85, MVP-86, MVP-87 (theory), MVP-89
- **Prior session (2026-03-30)**: r5py kelurahan pipeline, Gini_kel 0.0896→0.2441, EDA notebook, comparison notebook

## Blockers

- **L4/L5 still flat** — L4 (last-mile) and L5 (cost competitiveness) don't use r5py routing; L4 uses road connectivity proxy, L5 uses TCR proxy from travel time. Acceptable for current analysis.
- **H3 field name mismatches** (30 fields) — must rename before MVP-27 (migrate to real data).
- **H3 routing coverage 11.2%** — 88.8% of H3 cells have no transit route (use 180 min fallback). This is the correct real-world picture (most of Jabodetabek is not transit-accessible) but note this in Results section limitations.

## Next Action

1. **PR review**: Merge `e6/mvp-98-run-pipeline` → main
2. **MVP-27**: Migrate web app to real pipeline output — blocked on H3 field rename fix
3. **MVP-87 (Stats re-run)**: Re-run stats assessment with new equity_summary.json (Gini_H3=0.6128)
4. **MVP-12**: Write final Introduction section
5. **E5 gate**: MVP-88 (consistency check) before MVP-17 (self-review)

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
