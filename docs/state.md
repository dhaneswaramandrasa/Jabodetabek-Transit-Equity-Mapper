# Project State

**Last updated**: 2026-03-25
**Active ticket**: MVP-86 (gap debate) — Done
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

1. **MVP-89**: Dual-agent convergence drafting — Introduction + Discussion (now unblocked). Input: cache/gap-debate-report.md
2. **E6 continues**: MVP-23 (compute TAI/TNI) — unblocked after PR #10 merge
3. **E6 gate**: MVP-87 (hypothesis validator) must complete before MVP-14 (Results)
4. **E5 gate**: MVP-88 (consistency check) must complete before MVP-17 (self-review)

## AutoResearchClaw + Dual-Agent Integration (2026-03-22/23)

Five new tickets added integrating AutoResearchClaw phases and dual-agent convergence pattern:
- **MVP-85**: Phase B lit sweep + Phase H citation audit (E4 pre-work, blocks MVP-86)
- **MVP-86**: Phase C gap debate — Defender vs Skeptic 2-round debate loop (blocks MVP-89)
- **MVP-87**: Phase F hypothesis validator — Stats vs Theory dual assessment (blocks MVP-14)
- **MVP-88**: Phase G+H consistency check + quality gate (E5 gate, blocks MVP-17)
- **MVP-89**: Dual-agent convergence drafting for Introduction + Discussion (blocks MVP-12)

Full dependency chain: MVP-85 → MVP-86 → MVP-89 → MVP-12 (Introduction)
                       MVP-25 → MVP-87 → MVP-14 (Results)
                       MVP-16 → MVP-88 → MVP-17 (E5 self-review)

Install AutoResearchClaw: `pip install researchclaw && researchclaw setup`
Pattern 4 (Dual-Agent Convergence) documented in CLAUDE.md — AutoResearchClaw Integration section.
All cache outputs: `cache/debate-*.md`, `cache/hypothesis-*.md`, `cache/draft-*.md`,
`cache/convergence-*.md`, `cache/section-consistency-report.md`

## Open Questions

- Methods section is ~5,450 words (above 3,000-4,000 target). May need trimming — GC model details could move to supplementary appendix. MVP-88 will flag this for human decision.
