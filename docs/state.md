# Project State

**Last updated**: 2026-03-30
**Active ticket**: MVP-100 (EDA) — In Review
**Branch**: e6/mvp-98-run-pipeline

---

## Current Focus

**Phase**: E4 (paper drafting) + E6 (data pipeline) both active.
This is a **portfolio / independent research project** — no academic gating.

## Last Session Summary (2026-03-30)

- **r5py pipeline completed**: 31 batches processed (~1 min total), L3 CBD journey now uses real r5py routing
- **Equity analysis re-run** with r5py data — dramatic changes:
  - Gini TAI kelurahan: 0.0896 → **0.2441** (+172% — r5py reveals much more inequality)
  - TAI mean: 0.397 → **0.256** (real routing shows lower accessibility)
  - TAI std: 0.077 → **0.139** (much wider spread)
  - Moran's I: 0.8418 → **0.8876** (stronger spatial clustering)
  - Q4 transit deserts: 413 → **415** kelurahan
  - H2 signal reversed at kelurahan level: Gini_kelurahan (0.2441) > Gini_H3 (0.1228) — H3 not yet re-run with r5py
- **Comparison notebook**: `notebooks/comparison_r5py_vs_baseline.ipynb` — full visual comparison of r5py vs no-r5py
  - TAI distribution histograms, layer-by-layer violin plots, spatial choropleths, quadrant shift heatmaps
- **EDA notebook**: `notebooks/eda_pipeline_output.ipynb` — comprehensive EDA with visualizations
  - TAI/TNI distributions, equity gap analysis, spatial maps, LISA clusters, Lorenz curves
  - H1/H2/H3 hypothesis testing sections with visual evidence
  - Summary dashboard with KPIs
- **Baseline cached**: `cache/baseline_no_r5py/` has pre-r5py kelurahan_scores, h3_scores, equity_summary
- **Previously completed** (prior sessions): E0 (9/9), E1 (3/3), E2 (3/3), E3 (3/3), MVP-84, MVP-13, MVP-85, MVP-86, MVP-87 (theory), MVP-89

## Blockers

- **L4/L5 still flat at 0.5** — these layers don't use r5py routing. L4 (last-mile) and L5 (cost competitiveness) need separate computation.
- **H3 scores not re-run with r5py** — h3_scores.geojson still uses placeholder L3. H2 hypothesis comparison invalid until H3 is also re-run.
- **H3 field name mismatches** (30 fields) — must rename before MVP-27 (migrate to real data).

## Next Action

1. **Re-run H3 pipeline with r5py** — needed for valid H2 hypothesis test
2. **PR review**: Merge `e6/mvp-98-run-pipeline` → main
3. **MVP-27**: Migrate web app to real pipeline output — blocked on H3 field rename fix
4. **MVP-87 (Stats re-run)**: Re-run with r5py equity_summary.json
5. **MVP-12**: Write final Introduction section
6. **E5 gate**: MVP-88 (consistency check) before MVP-17 (self-review)

## Pipeline Status (as of 2026-03-30)

| File | Status | Notes |
|---|---|---|
| `data/processed/scores/kelurahan_scores.geojson` | ✅ 1,502 rows | L3 via r5py; L4/L5 still placeholder 0.5 |
| `data/processed/scores/h3_scores.geojson` | ⚠️ 9,083 cells | Still no-r5py version; needs re-run |
| `data/processed/analysis/equity_summary.json` | ✅ | Re-run with r5py kelurahan data |
| `data/processed/analysis/lorenz_*.csv` | ✅ | Updated |
| `data/processed/analysis/lisa_*.geojson` | ✅ | Updated |
| `data/processed/analysis/resolution_comparison.json` | ✅ | Cohen's kappa=0.6094, 29.2% reclassified |
| `notebooks/comparison_r5py_vs_baseline.ipynb` | ✅ | r5py vs no-r5py visual comparison |
| `notebooks/eda_pipeline_output.ipynb` | ✅ | Full EDA with visualizations |

## EDA Key Numbers (for Results section — r5py data)

- Q4 transit deserts: 415 kelurahan (27.6%), 2,541 H3 (28.0%)
- Gini TAI: kelurahan=0.2441, H3=0.1228 (H3 needs r5py re-run for valid comparison)
- Gini equity gap: kelurahan=0.2608, H3=0.3318
- Cohen's kappa: 0.6094 (strong agreement; 29.2% reclassified)
- Global Moran's I (TAI): kelurahan=0.8876, H3=0.8928 (strong spatial clustering)
- TAI mean: 0.256 (was 0.397 without r5py)

## Open Questions

- H2 hypothesis needs H3 re-run with r5py before it can be properly tested
- Methods section is ~5,450 words (above target). MVP-88 will flag for human decision.
- MVP-89 convergence decisions resolved 2026-03-25. Introduction + Discussion v0.1 ready for MVP-12.
