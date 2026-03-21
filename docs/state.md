# Project State

**Last updated**: 2026-03-22
**Active ticket**: MVP-19/20/21/22 complete — preparing PR for E6 data acquisition
**Branch**: e6/mvp-19-merge-gtfs-lrt

---

## Current Focus

**Phase**: E6 (data pipeline) — data acquisition complete (MVP-19 through MVP-22). Next: MVP-23 (compute TAI/TNI).
This is a **portfolio / independent research project** — no academic gating.

## Last Session Summary

- **MVP-19 through MVP-22** confirmed Done — all E6 data acquisition complete
- **NTL proxy investigation**: Researched nighttime lights (VIIRS) as alternative to synthetic BPS demographics
  - Finding: NTL alone cannot derive vehicle ownership or dependency ratio
  - NTL + covariates (Utomo et al. 2023) achieves r=0.954 but needs SUSENAS calibration
  - Decision: Keep synthetic data calibrated to BPS ranges; document limitation in paper
- **Source map updated**: Added 3 NTL papers (#16–18: Mellander 2015, Utomo 2023, Prawira 2022)
- **Previously completed**: E0 (9/9), E1 (3/3), E2 (3/3), E3 (3/3), MVP-84

## Blockers

- None — MVP-23 unblocked (all data acquisition done)

## Next Action

1. **PR**: Open PR for e6/mvp-19-merge-gtfs-lrt branch (MVP-19 through MVP-22)
2. **E6 continues**: MVP-23 (compute TAI/TNI per kelurahan) — next after PR merge
3. **E4** (paper track): MVP-12 (introduction), MVP-13 (methods) — both unblocked
4. Paper and product tracks can run in parallel

## Open Questions

- None
