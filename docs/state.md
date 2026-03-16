# Project State

**Last updated**: 2026-03-16
**Active ticket**: MVP-5 — Finalize TNI indicator set and weighting scheme (E0-003)
**Branch**: main

---

## Current Focus

**Phase**: E0 (Foundation) — completing foundational research work before execution epics.
This is a **portfolio / independent research project** — no academic gating.

## Last Session Summary

- **MVP-2 (E0-001) completed**: Literature scan + source map
  - 12 search queries across 3 rounds (Google Scholar, Semantic Scholar, web)
  - 15 papers extracted with full citation, method+findings, data sources, relevance
  - `docs/source-map.md` written: full paper table (15 entries) + synthesis (4 sections)
  - `docs/literature_review.md` written: ~2,200 words of academic prose by theme (v0.1)
    - 4 thematic clusters: transit accessibility measurement, urban mobility equity in developing countries, MAUP/H3/composite indices, generalized cost models
    - Gap section: confirmed 4 research gaps
  - `docs/methodology.md` updated: added §2.1b Theoretical Framework + §2.1c Methodological Precedents
  - `docs/research-framing.md` updated: RQ confirmed, no refinements needed
  - Literature validates all four gap claims from research framing
  - Key findings from scan:
    - TNI indicator set confirmed by Mamun & Lownes (2011) precedent
    - MAUP dual-resolution approach strongly supported by Javanmard et al. (2023)
    - Three-way GC model (incl. motorcycle) is novel — no existing framework does this
    - Transit desert (Q4) concept well-established (Jiao 2013, Jomehpour 2020)
    - r5py/r5r is the standard tool for multimodal accessibility computation
    - Hardi & Murad (2023) found 58% of Jakarta BRT stations poorly connected — validates first-mile focus
- 3 tickets Done (MVP-1, MVP-4, MVP-2); 6 remaining in E0

## Blockers

- None — MVP-5, MVP-7, MVP-8 are all unblocked (were waiting on MVP-2)

## Next Action

Three tickets are now unblocked in parallel:
1. **MVP-5** (E0-003): Finalize TNI indicator set and weighting scheme
   - Literature precedent: Mamun & Lownes (2011) TNI with poverty, zero-vehicle HH, dependency ratio
   - Confirm or refine current 5-indicator set; document weighting rationale
2. **MVP-7** (E0-004): Design H3 derivation pipeline
   - Literature precedent: Javanmard et al. (2023) MAUP sensitivity; dasymetric methods from WorldPop
   - Confirm dual-method derivation strategy
3. **MVP-8** (E0-005): Design three-way generalized cost model
   - Literature precedent: Ng (2018) motorcycle mode choice; Sukor & Bhayo (2024) first-mile as swing factor
   - Validate cost parameters against SE Asian literature

**E0 critical path**: `MVP-2 ✅ → [MVP-5, MVP-7, MVP-8] → MVP-77 → MVP-6 → MVP-3`
**Phase 3 trigger**: When MVP-3 (E0-008) is Done → create E1, E2, confirm E3–E10

## Open Questions

- Ask user: "Any specific papers, DOIs, or PDFs to add to the literature scan?" (per CLAUDE.md Phase 1.3 Step 2)
