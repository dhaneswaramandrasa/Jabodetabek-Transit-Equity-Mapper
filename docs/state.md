# Project State

**Last updated**: 2026-05-04
**Active tracks**: (1) Main research project — E7 UI; (2) Trans-Eng final project — 6-mode MNL verified

---

## Track 1: Main Research Project

**Phase**: E7 (UI Foundation) — UX P1 issues resolved, L06 discrete choice extensions complete.
**Branch**: `ui/stitch-redesign`
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

---

## Track 2: Trans-Eng Final Project (Hiroshima University AY2026)

**Branch**: `trans-eng/final-project-jabodetabek`
**Deadline**: June 3, 2026 (Session L15 — Presentation & Q&A)
**Full spec**: `notebooks/trans-eng-final/trans-eng-final-project.md`

### Last Action (2026-05-04) — Option B: 6-mode reduction + MNL verification
- **Option B implemented**: Reduced from 9 modes to 6 (dropped 2WRH, 4WRH, LRT).
  4 actions completed:
  1. ✅ Notebook 01 updated: MODE_LABELS, TRUE_DGP, LOS generation all 6-mode
  2. ✅ Notebook 02 updated: 6-mode DGP, 2 nests {transit: KRL/MRT/TJ/Royal}, {private: car/moto}
  3. ✅ Spec §4, §5, §7 documented: mode set reduction with BPS 2023 + thin-cell citations
  4. ✅ Both notebooks re-executed cleanly, CSVs regenerated
- **MNL recovery verified — 12/12 params within 2 SE**:
  - All signs correct (β_time < 0, β_cost < 0)
  - No SE=0 (robust SE fallback for MRT flat-Hessian directions)
  - Analytical gradient ||∇LL|| = 0.115 (near zero; flatness expected for MNL on NL data)
  - L-BFGS-B converged; BFGS polish at precision limit
  - ASC_moto largest deviation (est=0.589 vs true=0.048, still within 2 robust SE)

### Verification results (6-mode NL DGP, λ=0.7, seed=20260601)
| Criterion | Result |
|---|---|
| 12/12 params within 2 SE | ✅ ALL parameters recovered |
| All signs correct | ✅ 6 β_time < 0, β_cost < 0, ASCs mixed |
| No SE=0 | ✅ Robust SE fallback for MRT (low-sample zone) |
| Analytical gradient ≈ 0 | ✅ ||∇LL|| = 0.115 |
| Choice distribution realistic | moto=36.7%, tj=34.0%, krl=17.8%, royal=9.1%, mrt=1.4%, car=1.0% |
| Nest shares | transit=62.3%, private=37.7% |

### Last Action (2026-05-09) — 03_nl_estimation.ipynb complete
- **§7.6** added to spec: documented 3 DGP limitations (ASC calibration, Car share ~1%, VOT_car bias)
- **01_data_prep.ipynb cell 1279bd9b**: removed dead `TRUE_DGP_NL` block; replaced with explanatory comment on why homogeneous λ=0.7 is used
- **03_nl_estimation.ipynb**: built (32 cells) + executed cleanly
  - L-BFGS-B converged (1736 iter, |grad|=0.34)
  - 13/13 params within 2 SE
  - λ̂ = 0.763 ± 0.068, CI95: [0.627, 0.900], λ=1 excluded
  - LR stat = 8.57, p = 0.0034 — REJECT H₀ at p<0.01
  - ΔLL = +4.29; AIC: NL wins by 6.6 units; BIC: tie (expected at N=5000)
  - bt(car) = 0.0 (hits bound; Car ~1% share, true=-0.024 ≈ 0, §7.6)
  - Free-TJ ΔCS = +1.28 Th IDR/trip (correct welfare direction)
  - All 12/12 verification checks PASS
  - Exports `data/nl_estimates.json`

### Last Action (2026-05-11) — 03b_mixed_logit.ipynb complete
- **spec §7.6.4** added: documented λ̂ upward bias (9%, within 2 SE) + BIC tie explanation
- **03b_mixed_logit.ipynb**: built (32 cells) + executed cleanly (12/12 checks PASS)
  - Random β_cost only: β_cost_n = μ_cost + σ_cost·η_n, η ~ N(0,1)
  - 13 params: 6 β_time + μ_cost + σ_cost + 5 ASC; σ_cost = exp(σ_raw)
  - R=100 Halton draws (base=2); L-BFGS-B converged (66 iter)
  - σ̂_cost = 0.0100 ± 0.0331; Wald stat = 0.0908, p = 0.763 → FAIL TO REJECT σ=0
  - LL_MXL = −5048.79 ≈ LL_MNL = −5048.83 (|ΔLL|=0.03 — MXL adds no signal)
  - AIC: NL=10115 beats MXL=10123 by 8.5 units; BIC: MXL=10208 >> NL=10200
  - Mixed-DGP Wald correctly detects σ>0 when σ_TRUE=0.02 (p≈0) ✅
  - Exports `mxl_estimates.json` and `best_model.json` (selected: NL)
- **spec §14**: 03b updated to ✅ Done

### Next Action
**Pending explicit greenlight from user before 04.**
1. ~~Build `01_data_prep.ipynb`~~ ✅ Done
2. ~~Build `02_mnl_estimation.ipynb`~~ ✅ Done
3. ~~Build `03_nl_estimation.ipynb`~~ ✅ Done
4. ~~Build `03b_mixed_logit.ipynb`~~ ✅ Done
5. **[AWAITING GREENLIGHT] Build `04_policy_simulation.ipynb`** — 8 scenarios (A–H), reads `best_model.json`

### Notebook Status
| Notebook | Status | Notes |
|---|---|---|
| `01_data_prep.ipynb` | ✅ Done | 6-mode, 7 zones, 5,000 persons, μ=25 scale |
| `02_mnl_estimation.ipynb` | ✅ Done | 12/12 recovered, MNL on NL data, IIA violation demo |
| `03_nl_estimation.ipynb` | ✅ Done | 13/13 recovered; λ̂=0.763±0.068; LR=8.57 p=0.003; ΔCS free-TJ=+1.28 |
| `03b_mixed_logit.ipynb` | ✅ Done | σ̂=0.010 (p_Wald=0.763); NL wins AIC+8.5; best_model=NL |
| `04_policy_simulation.ipynb` | ⬜ Not started | 8 scenarios (A–H) from §8; reads `best_model.json` — AWAITING GREENLIGHT |
| Report draft | ⬜ Not started | After all 5 notebooks done |
