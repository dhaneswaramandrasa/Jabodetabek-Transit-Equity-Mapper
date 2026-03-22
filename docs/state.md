# Project State

**Last updated**: 2026-03-22
**Active ticket**: MVP-13 (methods section) — In Review
**Branch**: e4/mvp-13-methods-section

---

## Current Focus

**Phase**: E4 (paper drafting) + E6 (data pipeline) both active.
This is a **portfolio / independent research project** — no academic gating.

## Last Session Summary

- **MVP-13**: Methods section written (~5,450 words) at paper/sections/03-methodology.md
  - All 10 subsections: study area, framework, TNI, TAI 5-layer, dual-resolution, data sources, equity analysis, sensitivity, what-if, limitations
  - Matches docs/methodology.md exactly — no invented methods
  - Includes NTL proxy investigation note (Mellander 2015, Utomo 2023)
  - 16 papers cited from source-map.md
- **Source map updated**: 3 NTL papers added (#16-18)
- **MVP-19 through MVP-22**: Marked Done in EPICS_TASKS.md
- **PR #10**: E6 data acquisition (MVP-19-22) open for review
- **Previously completed**: E0 (9/9), E1 (3/3), E2 (3/3), E3 (3/3), MVP-84

## Blockers

- None

## Next Action

1. **Review**: MVP-13 methods section PR pending review
2. **E4 pre-work**: MVP-85 (lit sweep) → MVP-86 (gap debate) must run before MVP-12 (Introduction)
3. **E6 continues**: MVP-23 (compute TAI/TNI) — unblocked after PR #10 merge
4. **E6 gate**: MVP-87 (hypothesis validator) must complete before MVP-14 (Results)
5. **E5 gate**: MVP-88 (consistency check) must complete before MVP-17 (self-review)
6. Paper and product tracks can run in parallel

## AutoResearchClaw Integration (2026-03-22)

Four new tickets added integrating AutoResearchClaw phases into paper quality pipeline:
- **MVP-85**: Phase B lit sweep + Phase H citation audit (E4 pre-work, blocks MVP-12)
- **MVP-86**: Phase C gap debate agent (E4 pre-work, blocks MVP-12)
- **MVP-87**: Phase F hypothesis validator (E6 gate, blocks MVP-14)
- **MVP-88**: Phase G+H consistency check + quality gate (E5 gate, blocks MVP-17)

Install: `pip install researchclaw && researchclaw setup`
Full subagent prompts in CLAUDE.md — AutoResearchClaw Integration section.
Cache outputs go to: `cache/lit-gap-report.md`, `cache/gap-debate-report.md`,
`cache/hypothesis-validation-report.md`, `cache/section-consistency-report.md`

## Open Questions

- Methods section is ~5,450 words (above 3,000-4,000 target). May need trimming — GC model details could move to supplementary appendix. MVP-88 will flag this for human decision.
