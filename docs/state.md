# Project State

**Last updated**: 2026-04-03
**Active ticket**: MVP-14 (Results section) — In Review
**Branch**: e4/mvp-14-results-section

---

## Current Focus

**Phase**: E4 (paper drafting) + E6 (data pipeline) both active.
This is a **portfolio / independent research project** — no academic gating.

## Last Session Summary (2026-04-03)

- **MVP-14 DONE**: Results section written — `paper/sections/04-results.md`, 2,543 words
  - Covers: TAI/TNI distributions, quadrant classification (Table 1), H1 spatial mismatch (Table 2), H2 resolution effect, H3 equity gap scenario, hypothesis outcome summary (Table 4)
  - All three hypotheses confirmed: H1 (98.8% Q4 in Bodetabek), H2 (Gini delta=+0.3687), H3 (Q4/Q1 ratio=1.65×)
- **MVP-98/99/100 DONE** (prior session): H3 r5py pipeline, equity analysis re-run, EDA notebook
  - H3 r5py: 1,021/9,083 cells routed (11.2%), Gini H3=0.6128
  - Moran's I H3 TAI: 0.9447; Cohen's kappa: 0.6124; 29.0% reclassified
- **MVP-87 Stats re-run DONE** (prior session): All three hypotheses PROCEED; hypothesis-stats-assessment.md + hypothesis-validation-report.md updated
- **Previously completed**: E0 (9/9), E1 (3/3), E2 (3/3), E3 (3/3), MVP-84, MVP-13, MVP-85, MVP-86, MVP-87, MVP-89, MVP-98/99/100

## Blockers

- **L4/L5 still flat** — L4 (last-mile) and L5 (cost competitiveness) don't use r5py routing; L4 uses road connectivity proxy, L5 uses TCR proxy from travel time. Acceptable for current analysis.
- **H3 field name mismatches** (30 fields) — must rename before MVP-27 (migrate to real data).
- **H3 routing coverage 11.2%** — 88.8% of H3 cells have no transit route (use 180 min fallback). This is the correct real-world picture (most of Jabodetabek is not transit-accessible) but note this in Results section limitations.

## Next Action

1. **PR #26 review**: Merge `e6/mvp-98-run-pipeline` → main (all pipeline work done)
2. **MVP-14 Linear**: Post completion comment on ticket, set to In Review, push branch, open PR
3. **MVP-15 (Discussion)**: v0.1 exists at `paper/sections/05-discussion.md` — fill placeholders with real metric values now that Results are written
4. **MVP-27**: Migrate web app to real pipeline output — blocked on H3 field rename fix (30 fields)
5. **MVP-88**: Section consistency check + quality gate (gate before MVP-17 self-review)

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
