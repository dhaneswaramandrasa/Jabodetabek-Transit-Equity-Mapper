# Roadmap

**Project**: Jabodetabek Transit Equity Mapper
**Start date**: 2026-03-16
**Target date**: 2026-03-31
**Last updated**: 2026-03-16

---

## Milestones

| # | Milestone | Target Date | Status | Key Deliverable |
|---|-----------|-------------|--------|-----------------|
| M1 | Foundation Complete | 2026-03-18 | Done | Research framing + methodology confirmed, Linear set up, docs bootstrapped |
| M2 | Literature & Remaining Methodology | 2026-03-21 | Not Started | Source map (MVP-2), PRD refined (MVP-3), TNI/H3/GC design finalized (MVP-5/7/8) |
| M3 | Data Pipeline Complete | 2026-03-25 | Not Started | All raw data acquired, processed, scored at kelurahan + H3 (MVP-19 → MVP-25) |
| M4 | Paper Draft Complete | 2026-03-27 | Not Started | All paper sections drafted (MVP-9 → MVP-16) |
| M5 | Product Complete | 2026-03-29 | Not Started | UI migrated to real data, all core features working (MVP-26 → MVP-34) |
| M6 | Deliverables Shipped | 2026-03-31 | Not Started | Paper submitted, dataset published, product deployed (MVP-35 → MVP-38) |

---

## Weekly Plan

### Week 1 (Mon Mar 16 – Sun Mar 22)
- [x] Bootstrap docs system (this session)
- [ ] MVP-2: Literature scan + source map
- [ ] MVP-3: Refine PRD with gap statement
- [ ] MVP-5: Finalize TNI weighting
- [ ] MVP-7: Finalize H3 derivation design
- [ ] MVP-8: Finalize three-way GC model
- [ ] MVP-19: Download + validate GTFS feeds
- [ ] MVP-20: Extract OSM road network

### Week 2 (Mon Mar 23 – Sun Mar 29)
- [ ] MVP-21: Extract strict POIs
- [ ] MVP-22: Assemble BPS demographics
- [ ] MVP-23: Compute TAI/TNI per kelurahan (heavy compute: 2–4 hrs)
- [ ] MVP-24: Generate H3 grid + derive indicators (heavy compute: 8–16 hrs)
- [ ] MVP-25: Equity gap, Gini, LISA
- [ ] MVP-9/10/11: Literature review sections
- [ ] MVP-12/13: Introduction + methods paper sections
- [ ] MVP-26: Audit existing prototype
- [ ] MVP-27: Migrate to real data

### Week 3 (Mon Mar 30 – Mon Mar 31)
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
| Timeline too aggressive (16 days for full pipeline + paper + product) | H | H | Prioritize E6 data pipeline → core features → paper; defer MVP-38 (presentation) |
