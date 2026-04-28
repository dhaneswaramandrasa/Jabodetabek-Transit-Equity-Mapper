# Project State

**Last updated**: 2026-04-28
**Active focus**: L06 notebook extension DONE — Claude Design + remaining UX improvements next
**Branch**: `ui/stitch-redesign`

---

## Current Focus

**Phase**: E7 (UI Foundation) — UX P1 issues resolved, L06 discrete choice extensions complete.
This is a **portfolio / independent research project** — no academic gating.

## Last Session Summary (2026-04-28)

- **L06 notebook extension DONE**: `notebooks/logit_eda_mle.ipynb` — 56 cells (31 code, 25 markdown), all executing cleanly
  - Sections 13-17 added from L06 Discrete Choice lectures:
    - Logsum / Inclusive Value — accessibility in currency units (ΔCS = Δlogsum/|β_cost|)
    - Option Value — value of having each mode available
    - Consumer Surplus — LRT scenario (30% transit time reduction)
    - Three SE Estimators — Hessian, BHHH, Robust/Sandwich (divergence = misspecification diagnostic)
    - NL vs MNL Welfare — different ΔCS from nest correlation dampening
  - Debugging saga: corrupted cell merge, column names (`time_motorcycle`→`time_moto`), string CHOICE→numeric, `mnl5_result`→`result_mnl5`, missing `.x` on OptimizeResult → all fixed
  - NaN SEs in misspecification cells expected behavior (near-singular Hessian)
- **Previous session (2026-04-27)**:
  - UX P1 fixes DONE (R1–R4 from `docs/ux-review-commuter.md`)
  - EDA notebook DONE: 43 cells, MNL + Nested Logit MLE from scratch

## Blockers

- **L4/L5 still flat** — acceptable for current analysis
- **H3 routing coverage 11.2%** — methodologically valid, note in Results limitations

## Next Action

1. **Run Claude Design** with the drafted prompt (`docs/claude-design-prompt.md`) to generate refreshed screens
2. **Cross-check generated screens** against `docs/ux-review-commuter.md` recommendations
3. **Implement design updates** in `web/src/` once screens are approved
4. **Consider remaining UX items**: journey polyline on map (R5), pin bounds validation (R7), "Show other modes" toggle (R11)

## Pipeline Status (as of 2026-04-27)

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
| `notebooks/logit_eda_mle.ipynb` | ✅ 56 cells | MNL + NL MLE + L06 extensions (logsum, option value, CS, 3 SE estimators, NL vs MNL welfare) |

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
