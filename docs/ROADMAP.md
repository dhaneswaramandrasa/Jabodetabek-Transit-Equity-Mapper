# Roadmap

**Project**: Jabodetabek Transit Equity Mapper
**Start date**: 2026-03-16
**Target date**: TBD — portfolio project, no hard deadline
**Last updated**: 2026-03-21

---

## Milestones

| # | Milestone | Target | Status | Key Deliverable |
|---|-----------|--------|--------|-----------------|
| M0 | E0 Foundation Complete | 2026-03-20 | **Done** | Literature scan, methodology finalized, schema confirmed, data plan verified, PRD done |
| M1 | E1 Research Framing Complete | 2026-03-21 | **Done** | research-framing.md confirmed, source map verified, ROADMAP.md generated |
| M2 | E2 Methodology & Data Design Signed Off | 2026-03-21 | **Done** | methodology.md signed off, DATA_MODEL.md signed off, ARCHITECTURE.md skeleton |
| M3 | E6 Data Pipeline Complete | 2026-04-13 | Not Started | All raw data acquired, processed, scored at kelurahan + H3 (MVP-84, MVP-19–25) |
| M4 | E3 Literature Review Complete | 2026-04-06 | Not Started | Theoretical framework, related work, methodology precedents sections (MVP-9–11) |
| M5 | E7 UI Foundation Complete | 2026-04-20 | Not Started | Prototype audited, real data migrated, road network + cost layers (MVP-26–28) |
| M6 | E4 Paper Drafting Complete | 2026-04-27 | Not Started | Introduction, methods, results, discussion, conclusion (MVP-12–16) |
| M7 | E8 Core Features Complete | 2026-05-04 | Not Started | Quadrant map, journey chain, what-if, competitive zones (MVP-29–32) |
| M8 | E5 Paper Review Complete | 2026-05-11 | Not Started | Self-review + revision (MVP-17–18) |
| M9 | E9 Code Review & QA Complete | 2026-05-11 | Not Started | Phase 5D checklist, edge case testing (MVP-33–34) |
| M10 | E10 Deliverables Shipped | 2026-05-18 | Not Started | Paper submitted, dataset published, product deployed (MVP-35–38) |

---

## Dependency Graph

```
E0 ✅ → E1 ✅ → E2 ✅
                              │
                ┌─────────────┴──────────────┐
                ▼                            ▼
        Paper Track                   Product Track
        E3 (Lit Review)               E6 (Data Pipeline)
            │                         + MVP-84 (GTFS)
            ▼                            │
        E4 (Paper Drafting)              ▼
            │                         E7 (UI Foundation)
            ▼                            │
        E5 (Paper Review)                ▼
                │                     E8 (Core Features)
                │                        │
                │                        ▼
                │                     E9 (Code Review)
                └────────┬───────────────┘
                         ▼
                    E10 (Deliverables)
```

Paper (E3→E4→E5) and Product (E6→E7→E8→E9) tracks run in parallel after E2.
E4 Results section (MVP-14) depends on E6 data pipeline output.

---

## Weekly Plan

### Week 1: Mar 16–22 — Foundation (E0 + E1)
- [x] Bootstrap docs system
- [x] E0 complete: literature scan, methodology, schema, data plan, PRD (9/9 tickets)
- [x] Phase 3 Linear setup: E1–E10 milestones + tickets created
- [x] **MVP-78**: Confirm research-framing.md ✅
- [x] **MVP-79**: Verify source map ✅
- [x] **MVP-80**: Generate ROADMAP.md ✅

### Week 2: Mar 23–29 — E2 Sign-Off + E3/E6 Start
- [ ] **MVP-81**: Sign off methodology.md
- [ ] **MVP-82**: Sign off DATA_MODEL.md
- [ ] **MVP-83**: Generate ARCHITECTURE.md skeleton
- [ ] **MVP-84**: Construct KRL + MRT GTFS feeds (can start parallel with E2)
- [ ] **MVP-9**: Write theoretical framework section (E3 start)

### Week 3: Mar 30–Apr 5 — E3 Literature Review + E6 Data Acquisition
- [ ] **MVP-10**: Write related work section (Jakarta/Jabodetabek studies)
- [ ] **MVP-11**: Write methodology precedents section
- [ ] **MVP-19**: Download, validate, merge GTFS + LRT stations
- [ ] **MVP-20**: Extract and process OSM road network
- [ ] **MVP-21**: Extract strict POIs via Overpass API
- [ ] **MVP-22**: Assemble BPS demographics + WorldPop disaggregation

### Week 4: Apr 6–12 — E6 Compute Pipeline
- [ ] **MVP-23**: Compute 5-layer TAI and TNI per kelurahan (2–4 hrs compute)
- [ ] **MVP-24**: Generate H3 grid + derive all indicators (8–16 hrs compute)
- [ ] **MVP-25**: Compute equity gap, Gini, LISA at both resolutions
- [ ] **MVP-12**: Write introduction (E4 start)

### Week 5: Apr 13–19 — E7 UI Foundation + E4 Paper
- [ ] **MVP-26**: Audit existing prototype against new methodology
- [ ] **MVP-27**: Migrate from synthetic to real pipeline output
- [ ] **MVP-13**: Write methods section
- [ ] **MVP-28**: Add road network layer + cost comparison card

### Week 6: Apr 20–26 — E8 Core Features + E4 Paper
- [ ] **MVP-29**: Implement quadrant map with dual-resolution toggle
- [ ] **MVP-30**: Implement CBD journey chain visualization
- [ ] **MVP-14**: Write results section (needs E6 data)
- [ ] **MVP-15**: Write discussion section

### Week 7: Apr 27–May 3 — E8 Features + E4/E5 Paper
- [ ] **MVP-31**: Implement what-if station placement simulator
- [ ] **MVP-32**: Implement transit competitive zone map
- [ ] **MVP-16**: Write conclusion and abstract
- [ ] **MVP-17**: Self-review against Phase 5P checklist

### Week 8: May 4–10 — E9 QA + E5 Paper Review
- [ ] **MVP-33**: Code review against Phase 5D checklist
- [ ] **MVP-34**: Edge case testing + deployment verification
- [ ] **MVP-18**: Final paper review and revision

### Week 9: May 11–18 — E10 Deliverables
- [ ] **MVP-35**: Final paper assembly + reference formatting
- [ ] **MVP-36**: Package dataset for public distribution
- [ ] **MVP-37**: Deploy product to Vercel + link paper and dataset
- [ ] **MVP-38**: Prepare presentation / poster with product demo

---

## Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| KRL/MRT GTFS construction takes longer than estimated | H | M | Start MVP-84 parallel with E2; budget 6–8 hours total |
| r5py compute time exceeds budget (16k+ route queries) | H | M | Batch H3 centroids in chunks of 1000; use cloud compute if needed |
| BPS data not available at kelurahan level | M | H | Disaggregate from kecamatan via WorldPop dasymetric; document as limitation |
| Scope creep on features | M | M | Stick to PRD; defer v2 enhancements |
| E4 Results section blocked by E6 data pipeline | H | M | Paper intro/methods can proceed while pipeline runs; results section waits |
| Figma design vs prototype integration complexity | M | M | Integration strategy decided: keep Next.js infra, adopt Figma layout; detailed in MVP-26 audit |
| Timeline may stretch beyond 9 weeks | L | M | Portfolio project — no hard deadline; prioritize data pipeline + core features first |

---

## Completed Milestones

### M0: E0 Foundation (2026-03-16 → 2026-03-20) ✅
- 9/9 tickets completed
- Key outputs: source-map.md (15 papers), literature_review.md (v0.1), methodology.md (5-layer TAI, TNI, GC, H3), DATA_MODEL.md, prd.md (9 features, 4 personas)
- KRL/MRT GTFS gap discovered → MVP-84 created
