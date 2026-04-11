# Project State

**Last updated**: 2026-04-11
**Active ticket**: MVP-109 — In Review (PR #29 open on this repo)
**Branch**: mvp-109/consolidate-web-monorepo

---

## Current Focus

**Phase**: E8/E9 — MVP-109 monorepo consolidation done, PR #29 open.
This is a **portfolio / independent research project** — no academic gating.

## Last Session Summary (2026-04-11)

- **MVP-109 DONE** (this session): Consolidated web app into monorepo — PR #29
  - `web/` added at repo root (copied from transit-access/web/)
  - `scripts/export_to_web.py` path updated → `web/public/data/`
  - `.gitignore` updated; `docs/ARCHITECTURE.md` updated
  - transit-access PR #5 closed with redirect note
  - `npm run build` passes ✅
- **MVP-94 DONE** (this session): Equity Summary Dashboard — now in `web/src/components/EquityDashboard.tsx`
  - `EquityDashboard.tsx`: floating 360px panel, 4 tabs (Overview, Lorenz, LISA, Resolution)
  - Overview: Gini TAI side-by-side (kelurahan=0.2441, H3=0.6128), Moran's I, quadrant bar chart
  - Lorenz: SVG curve with kelurahan/H3 toggle; fills 5 analysis files to public/data/
  - LISA: HH/HL/LH/LL/NS counts for both resolutions
  - Resolution: κ=0.6124, 29% reclassified, H2 confirmed badge
  - `scripts/export_to_web.py` updated — now also copies equity_summary.json, lorenz_*.csv, lisa_*.geojson
- **MVP-29 DONE** (prev session): Quadrant choropleth + resolution toggle — PR #4 on transit-access
  - ResultsLayout: compact Admin/H3 toggle + inline Q1–Q4 quadrant badge
- **MVP-90 DONE** (prev session): Persona entry screen — PR #3 on transit-access
- **MVP-27 DONE** (prev session): Real pipeline data migrated — PR #28 on transit-access (research repo)
- **MVP-14 DONE** (prior session): Results section, 2,543 words
- **Previously completed**: E0–E3, MVP-84/13/85/86/87/89/98/99/100

## Blockers

- **L4/L5 still flat** — L4 (last-mile) and L5 (cost competitiveness) don't use r5py routing; L4 uses road connectivity proxy, L5 uses TCR proxy from travel time. Acceptable for current analysis.
- **H3 field name mismatches** (30 fields) — must rename before MVP-27 (migrate to real data).
- **H3 routing coverage 11.2%** — 88.8% of H3 cells have no transit route (use 180 min fallback). This is the correct real-world picture (most of Jabodetabek is not transit-accessible) but note this in Results section limitations.

## Next Action

1. **Merge PRs**: #29 (MVP-109 monorepo, includes MVP-94) — smoke test: `cd web && npm run dev`
2. **MVP-28** — Road network layer + cost comparison card (`web/src/components/`)
3. **MVP-15 (Discussion)** — fill placeholders with real metric values (paper track)
4. **MVP-88** — Section consistency check gate (paper track)

> Note: All future web app work happens in `web/` inside this repo. transit-access repo is now archived/deprecated.

## Pipeline Status (as of 2026-03-30)

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
