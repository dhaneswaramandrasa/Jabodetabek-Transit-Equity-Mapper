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
| M2 | Literature & Remaining Methodology | 2026-03-21 | Not Started | Source map (TEQ-2), PRD refined (TEQ-3), TNI/H3/GC design finalized (TEQ-5/7/8) |
| M3 | Data Pipeline Complete | 2026-03-25 | Not Started | All raw data acquired, processed, scored at kelurahan + H3 (TEQ-19 → TEQ-25) |
| M4 | Paper Draft Complete | 2026-03-27 | Not Started | All paper sections drafted (TEQ-9 → TEQ-16) |
| M5 | Product Complete | 2026-03-29 | Not Started | UI migrated to real data, all core features working (TEQ-26 → TEQ-34) |
| M6 | Deliverables Shipped | 2026-03-31 | Not Started | Paper submitted, dataset published, product deployed (TEQ-35 → TEQ-38) |

---

## Weekly Plan

### Week 1 (Mon Mar 16 – Sun Mar 22)
- [x] Bootstrap docs system (this session)
- [ ] TEQ-2: Literature scan + source map
- [ ] TEQ-3: Refine PRD with gap statement
- [ ] TEQ-5: Finalize TNI weighting
- [ ] TEQ-7: Finalize H3 derivation design
- [ ] TEQ-8: Finalize three-way GC model
- [ ] TEQ-19: Download + validate GTFS feeds
- [ ] TEQ-20: Extract OSM road network

### Week 2 (Mon Mar 23 – Sun Mar 29)
- [ ] TEQ-21: Extract strict POIs
- [ ] TEQ-22: Assemble BPS demographics
- [ ] TEQ-23: Compute TAI/TNI per kelurahan (heavy compute: 2–4 hrs)
- [ ] TEQ-24: Generate H3 grid + derive indicators (heavy compute: 8–16 hrs)
- [ ] TEQ-25: Equity gap, Gini, LISA
- [ ] TEQ-9/10/11: Literature review sections
- [ ] TEQ-12/13: Introduction + methods paper sections
- [ ] TEQ-26: Audit existing prototype
- [ ] TEQ-27: Migrate to real data

### Week 3 (Mon Mar 30 – Mon Mar 31)
- [ ] TEQ-28/29/30/31/32: Core UI features
- [ ] TEQ-14/15/16: Results, discussion, conclusion
- [ ] TEQ-33/34: Code review + edge case testing
- [ ] TEQ-17: Paper self-review
- [ ] TEQ-35/36/37/38: Final deliverables

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
| Timeline too aggressive (16 days for full pipeline + paper + product) | H | H | Prioritize E6 data pipeline → core features → paper; defer TEQ-38 (presentation) |
