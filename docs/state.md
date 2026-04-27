# Project State

**Last updated**: 2026-04-26
**Active focus**: UX review + Claude Design — commuter journey redesign
**Branch**: `ui/stitch-redesign`

---

## Current Focus

**Phase**: E7 (UI Foundation) — UX audit complete, design iteration in progress.
This is a **portfolio / independent research project** — no academic gating.

## Last Session Summary (2026-04-26)

- **MVP-111 DONE**: Nested logit mode choice + multi-modal transit chains
  - Deterministic GC "Recommended" → probabilistic nested logit (Transit Chain μ=0.50, Two-Wheeler μ=0.45, Four-Wheeler μ=0.60)
  - First/last mile auto-detection: walk ≤500m, GoRide feeder >500m
  - JourneyPanel: probability bars, chain labels, sort toggle, equity card moved above modes
  - `docs/methodology.md` §2.7.2a + §2.7.2b added
  - UX fixes: R8, Q2, Q3, Q5
- **UX Review DONE**: Full commuter journey audit by UX Researcher agent → `docs/ux-review-commuter.md`
- **Previous session (2026-04-11)**:
  - MVP-109 DONE: monorepo consolidation — PR #29
  - MVP-94 DONE: Equity Summary Dashboard (`EquityDashboard.tsx`)
  - MVP-29/90/27 DONE (prior sessions)

## Blockers

- **UX issues must be resolved before design sign-off** — see `docs/ux-review-commuter.md` for prioritized list
- **L4/L5 still flat** — acceptable for current analysis
- **H3 routing coverage 11.2%** — methodologically valid, note in Results limitations

## Next Action

1. **Address UX P1 issues**: reverse geocoding (R1), sidebar reduction (R2), loading theme fix (R3)
2. **Run Claude Design** with the drafted prompt to generate refreshed screens
3. **Cross-check generated screens** against `docs/ux-review-commuter.md` recommendations
4. **Implement design updates** in `web/src/` once screens are approved

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
