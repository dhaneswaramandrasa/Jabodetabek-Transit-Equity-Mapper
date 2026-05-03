# Project State

**Last updated**: 2026-05-01
**Active tracks**: (1) Main research project — E7 UI; (2) Trans-Eng final project — scoping done

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

### Last Action (2026-05-03)
- **DGP redesign — 3 changes applied to enable fair MNL vs NL vs MXL comparison**:

**Change 1 — NL DGP choice generation (02_mnl_estimation.ipynb cell 5)**:
  - Replaced iid Gumbel choice simulation with NL GEV probability simulation
  - λ=0.7, 3 nests: transit (krl/mrt/tj/royal/lrt), private_car (car/4wrh), two_wheeler (moto/2wrh)
  - Exact GEV probabilities: P(m) = P(m|k) × P(k) with P(k) = S_k^λ / Σ S_ℓ^λ
  - `choice` + `choice_idx` persisted to persons_jkt.csv (cell 6) for 03/04 reuse
  - Seed = 20260601

**Change 2 — Dropped TIME_CV (01_data_prep.ipynb)**:
  - Removed person-level time noise cell (was cell 21, id=l2ybj8wqkwc)
  - With μ=25 + λ=0.7, Gumbel noise alone produces rich multimodal distributions

**Change 3 — Spec §7 updated**:
  - Added "Scale convention and error structure" paragraph:
    - σ=25 normalization (VOT scale-invariant, β recovered at μ=25 scale)
    - Nest correlation λ=0.7 (Train 2009 §4)
    - No random coefficients in DGP
  - Updated "Parameter recovery" section: MNL on NL data intentional — slight bias proves NL needed

### Verification results (NL DGP, λ=0.7, seed=20260601)
| Criterion | Result |
|---|---|
| No mode <3% in every zone | ✅ All modes ≥10% where available |
| No mode >55% in any zone | ✅ Max=35.8% (moto J1b) |
| MC+2WRH 30-45% | ✅ 33.5% |
| KRL highest in Bogor corridor | ✅ 25.5% in J1a (J1b no transit by design) |
| Nest shares | transit=37%, private_car=29.5%, two_wheeler=33.5% |

### Next Action
1. ~~Create `notebooks/trans-eng-final/` folder structure + `data/` subfolder~~ ✅ Done
2. ~~Build `01_data_prep.ipynb` — zone table, LOS matrix, synthetic population~~ ✅ Done
3. ~~Build `02_mnl_estimation.ipynb` — NL DGP, MNL estimation, 18-param recovery~~ ✅ Done
4. **Re-run 01 then 02 in Jupyter** to regenerate CSVs with NL choices
5. Build `03_nl_estimation.ipynb` (reuse cells 27-36 from logit_eda_mle.ipynb)
6. Build `03b_mixed_logit.ipynb` — L07 lab Tasks 3+3.5; output `data/best_model.json`
7. Build `04_policy_simulation.ipynb` — read `best_model.json`, 8 scenarios

### Notebook Status
| Notebook | Status | Notes |
|---|---|---|
| `01_data_prep.ipynb` | ⚠️ Needs re-run | TIME_CV cell removed, V/μ=25 → CSV. Re-run in Jupyter. |
| `02_mnl_estimation.ipynb` | ⚠️ Needs re-run | NL DGP choice generation, MNL estimation on NL data. Re-run after 01. |
| `03_nl_estimation.ipynb` | ⬜ Not started | Reuse cells 27-36 from `logit_eda_mle.ipynb`. Reads choice from persons_jkt.csv. |
| `03b_mixed_logit.ipynb` | ⬜ Not started | Adapt L07 lab Tasks 3+3.5; random β_time, Wald primary, Mixed-DGP recovery |
| `04_policy_simulation.ipynb` | ⬜ Not started | 8 scenarios (A–H) from §8; reads `best_model.json` |
| Report draft | ⬜ Not started | After all 5 notebooks done |

### Blockers
- **01 CSVs stale**: `jabodetabek_zones.csv`, `od_skim_jkt.csv`, `persons_jkt.csv` need regeneration with person-level time variation. Run `01_data_prep.ipynb` in Jupyter (system NumPy 2.4.4 incompatible with pandas/geopandas — Jupyter kernel has compatible env).
- **02_mnl_estimation.ipynb** has scaffold (30 cells) but old outputs pre-fix — re-run in Jupyter after 01 CSVs regenerated.
