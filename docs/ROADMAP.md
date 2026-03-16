# Roadmap

**Project**: Jabodetabek Transit Equity Mapper
**Start date**: 2026-03-16
**Target date**: 2026-03-31
**Last updated**: 2026-03-16

---

## Milestones

| # | Milestone | Target Date | Status | Key Deliverable |
|---|-----------|-------------|--------|-----------------|
| M0 | E0 Foundation Complete | 2026-03-21 | In Progress | Literature scan, methodology finalized, schema confirmed, data plan verified, PRD done |
| M1 | Phase 3: E1–E10 Setup | 2026-03-22 | Not Started | E1, E2 created; E3–E10 confirmed/refined from drafts |
| M2 | Data Pipeline Complete | 2026-03-26 | Not Started | All raw data acquired, processed, scored at kelurahan + H3 (MVP-19 → MVP-25) |
| M3 | Paper Draft Complete | 2026-03-28 | Not Started | All paper sections drafted (MVP-9 → MVP-16) |
| M4 | Product Complete | 2026-03-30 | Not Started | UI migrated to real data, all core features working (MVP-26 → MVP-34) |
| M5 | Deliverables Shipped | 2026-03-31 | Not Started | Paper submitted, dataset published, product deployed (MVP-35 → MVP-38) |

---

## Weekly Plan

### Week 1 (Mon Mar 16 – Sun Mar 22) — E0 Foundation
- [x] Bootstrap docs system
- [x] Introduce E0 epic + restructure tickets
- [x] **MVP-2** (E0-001): Literature scan + source map + literature review (v0.1)
- [ ] **MVP-5** (E0-003): Finalize TNI weighting (blocked by MVP-2)
- [ ] **MVP-7** (E0-004): Finalize H3 derivation design (blocked by MVP-2)
- [ ] **MVP-8** (E0-005): Finalize three-way GC model (blocked by MVP-2)
- [ ] **MVP-77** (E0-006): Consolidate methodology.md + DATA_MODEL.md (blocked by MVP-5/7/8)
- [ ] **MVP-6** (E0-007): Define data acquisition plan (blocked by MVP-77)
- [ ] **MVP-3** (E0-008): Produce PRD → **Phase 3 trigger** (blocked by MVP-2, MVP-6)

### Week 2 (Mon Mar 23 – Sun Mar 29) — Data Pipeline + Paper
- [ ] Phase 3: Create E1, E2; confirm E3–E10 tickets
- [ ] MVP-19–22: Download all data sources (blocked by MVP-6)
- [ ] MVP-23: Compute TAI/TNI per kelurahan (heavy compute: 2–4 hrs)
- [ ] MVP-24: Generate H3 grid + derive indicators (heavy compute: 8–16 hrs)
- [ ] MVP-25: Equity gap, Gini, LISA
- [ ] MVP-9/10/11: Literature review sections
- [ ] MVP-12/13: Introduction + methods paper sections
- [ ] MVP-26: Audit existing prototype
- [ ] MVP-27: Migrate to real data

### Week 3 (Mon Mar 30 – Mon Mar 31) — Ship
- [ ] MVP-28/29/30/31/32: Core UI features
- [ ] MVP-14/15/16: Results, discussion, conclusion
- [ ] MVP-33/34: Code review + edge case testing
- [ ] MVP-17: Paper self-review
- [ ] MVP-35/36/37/38: Final deliverables

---

## Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| GTFS feeds outdated or incomplete | H | M | Check feed freshness; fall back to stop-proximity if schedule data missing |
| r5py compute time exceeds budget | H | M | Batch H3 centroids in chunks of 1000; use cloud compute if needed |
| BPS data not available at kelurahan level | M | H | Disaggregate from kecamatan via WorldPop dasymetric; document as limitation |
| Scope creep on features | M | M | Stick to PRD; defer v2 enhancements |
| LRT Jabodebek has no GTFS feed | M | H | Include as point proximity only; flag as limitation |
| What-if simulator misleads users | M | L | Clear disclaimer labels; simplified buffer model only |
| Timeline too aggressive (16 days for full pipeline + paper + product) | H | H | Prioritize E0 → E6 data pipeline → core features → paper; defer MVP-38 (presentation) |
| Literature scan changes methodology significantly | M | M | E0-006 (MVP-77) consolidation gate catches all changes before data work starts |
