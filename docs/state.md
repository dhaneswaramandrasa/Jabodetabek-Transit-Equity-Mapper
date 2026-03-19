# Project State

**Last updated**: 2026-03-19
**Active ticket**: MVP-77 — Consolidate methodology.md + DATA_MODEL.md with literature findings (E0-006)
**Branch**: main

---

## Current Focus

**Phase**: E0 (Foundation) — completing foundational research work before execution epics.
This is a **portfolio / independent research project** — no academic gating.

## Last Session Summary

- **MVP-5 (E0-003) completed**: TNI indicator set and weighting scheme finalized
  - All 5 indicators confirmed: pop_density, poverty_rate, avg_household_expenditure, zero_vehicle_hh_pct, dependency_ratio
  - Equal weighting default, min-max normalization, sensitivity via ±20% perturbation + PCA check
  - Edge cases documented (missing data, zero variance, outliers with winsorization at 2nd/98th percentile)
  - Literature precedents: Mamun & Lownes (2011), Jiao & Dillivan (2013), Currie (2010), Rathod et al. (2025)
  - Draft: `docs/drafts/mvp5-tni-methodology.md`

- **MVP-7 (E0-004) completed**: H3 derivation pipeline designed
  - Res-8 primary (~15-20k cells), sensitivity at res-7 and res-9
  - Four derivation methods confirmed: dasymetric (WorldPop) for socioeconomic from kelurahan-level values, area-weighted clip for roads, point-in-polygon for stops/POIs, direct r5py for travel times
  - MAUP mitigation via dual-resolution comparison (Javanmard et al. 2023)
  - Resolution sensitivity analysis plan with confusion matrices and Cohen's kappa
  - Draft: `docs/drafts/mvp7-h3-methodology.md`

- **MVP-8 (E0-005) completed**: Three-way generalized cost model designed
  - All cost parameters sourced: VOT Rp 500/min, car fuel Rp 1,000/km, motorcycle fuel Rp 200/km
  - TCR thresholds: <0.8 private wins, 0.8–1.2 swing, >1.2 transit wins
  - Key finding: motorcycle beats transit at all three test distances (BSD, Ciputat, Tebet)
  - First-mile ojol cost confirmed as decisive swing factor (Sukor & Bhayo 2024)
  - Motorcycle toll exclusion creates structural cost floor transit must beat
  - Draft: `docs/drafts/mvp8-gc-methodology.md`

- **Methodology fixes applied** (from research-methodology-verifier review):
  - Motorcycle fuel cost corrected: Rp 400/km → Rp 200/km in methodology.md + worked examples
  - H3 dasymetric source corrected: kecamatan → kelurahan (derives from step 9 output)
  - BSD example: motorcycle GC = Rp 64k, TCR = 0.91 (swing zone)
  - Tebet example: motorcycle GC = Rp 16.5k, TCR = 0.79 (private wins)

- **DATA_MODEL.md updated** (4 additions):
  - `transit_competitive_zone` enum: added `"transit_not_available"`
  - `population` at H3 level: explicitly `float` (dasymetric estimate)
  - `is_edge_cell`: boolean for boundary sensitivity checks
  - `kelurahan_ids`: list[string] for dasymetric traceability

- 6 tickets Done (MVP-1, MVP-4, MVP-2, MVP-5, MVP-7, MVP-8); 3 remaining in E0

## Blockers

- None — MVP-77 is now unblocked (all three methodology tickets done)

## Next Action

1. **MVP-77** (E0-006): Consolidate methodology.md + DATA_MODEL.md with literature findings
   - Merge the three drafts (`docs/drafts/mvp5-*.md`, `mvp7-*.md`, `mvp8-*.md`) into `docs/methodology.md`
   - Verify all formula references against literature
   - Confirm DATA_MODEL.md and methodology.md are in sync
   - This is the consolidation gate before data acquisition

**E0 critical path**: `[MVP-5 ✅, MVP-7 ✅, MVP-8 ✅] → MVP-77 → MVP-6 → MVP-3`
**Phase 3 trigger**: When MVP-3 (E0-008) is Done → create E1, E2, confirm E3–E10

## Open Questions

- None currently blocking
