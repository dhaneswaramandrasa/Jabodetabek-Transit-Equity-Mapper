# 3D Showcase Map: Plan

**Status:** plan, not started · **Owner:** Dhaneswara · **Date:** 2026-10-30

## Goal

A single scroll-through 3D map that shows what this project has already found and what it is building
towards, at the same level as the portfolio's Omni and Persona Atlas demos. It doesn't replace the Next.js app
in `web/`. It's a fast, linkable showcase that points into it.

Unlike the other demos, this one uses **real open data**: GTFS, OSM, BPS and WorldPop outputs already in
`web/public/data/`. Nothing is simulated. Every step is labelled with its status so the unfinished parts
read as a roadmap, not as results.

| Badge | Meaning |
|---|---|
| **Done** | computed by the pipeline, numbers in `equity_summary.json` / `state.md` |
| **Preliminary** | computed, with a known limitation stated on screen |
| **Planned** | designed in `methodology.md` / `prd.md`, not built yet; shown as a mock-up |

## Story (7 steps)

| # | Step | What the map shows | Data | Status |
|---|---|---|---|---|
| 1 | **Who needs transit** | 9,083 H3 res-8 hexes as 3D columns. Height = population, colour = Transit Need Index (density, poverty, expenditure, zero-vehicle households, dependency) | `h3_scores.geojson`: `population`, `tni_score` | Done |
| 2 | **Where transit goes** | Glowing lines for 74 routes (MRT, LRT, KRL, TransJakarta) and stops; hexes recolour to Transit Accessibility Index | `jakarta_transit_routes/stops.geojson`, `tai_score` | Done |
| 3 | **The gap** | Four quadrants. **Q4 transit deserts** (high need, low access) rise and glow red, the rest fade. 27.6% of kelurahan, 28.0% of hexes | `quadrant`, `equity_gap` | Done |
| 4 | **Resolution changes the story** | Toggle: kelurahan polygons (1,502) ↔ H3 hexes. Gini of access 0.24 → 0.61; Cohen's κ 0.61, 29% of areas change quadrant | `kelurahan_scores.geojson`, `resolution_comparison.json` | Done |
| 5 | **Clusters, not noise** | LISA hot and cold spots: Moran's I = 0.94 on hexes. Deserts form contiguous belts, not scattered cells | `lisa_h3.geojson` | Done |
| 6 | **The commute to Sudirman** | Arcs from hexes to Sudirman–Thamrin, coloured by r5py journey time; unreachable areas greyed | `tai_l3_cbd_journey`, `poi_reach_cbd_min` | **Preliminary**: only 11.2% of hexes routed, the rest fall back to 180 min |
| 7 | **What a new station would change** | Drop a station pin, re-score nearby hexes, show how many Q4 deserts flip | what-if simulator spec in `prd.md` | **Planned**: last-mile (L4) and cost-competitiveness (L5) layers are still placeholders; shown as a labelled mock-up |

A closing card lists the roadmap: L4/L5 layers, full r5py routing, the what-if simulator, the paper.

## Design

- Same look as the Omni map: dark basemap (OpenFreeMap `dark`), glass panels, step tabs, hover tooltips.
- Colour: need = warm ramp (purple → amber); access = cool ramp (navy → cyan); Q4 = hot red; Q1–Q3 muted.
- Transit lines in mode colours (MRT, LRT, KRL, TransJakarta), drawn as glowing `PathLayer`s.
- Mobile: panel at the bottom, fewer arcs.

## Build

1. **Export script** `scripts/export_showcase.py`: reads the processed GeoJSON and writes one compact
   `showcase/data/showcase.json`. It holds hex centroids (from `h3_index`) plus rounded scores and quadrant,
   kelurahan polygons simplified, routes, stops and summary stats. Target under 3 MB; today's raw files are about 30 MB.
2. **Page** `showcase/index.html`: one static file, MapLibre 4.7.1 + deck.gl 9.0.38 from unpkg, no build step.
   Layers: `ColumnLayer` (hexes), `PolygonLayer` extruded (kelurahan), `PathLayer` (routes), `ScatterplotLayer` (stops), `ArcLayer` (step 6).
3. **Deploy** with a GitHub Pages workflow publishing `showcase/`, giving
   `dhaneswaramandrasa.github.io/jabodetabek-transit-equity-mapper/`. The Next.js app stays on Vercel.
4. **README**: animated GIF of the map at the top with a "▶ Open the 3D map" link, like the other project repos.
5. **Portfolio**: card or featured block on the website linking to it.

## Open decisions

1. **Where it lives:** a static `showcase/` page on GitHub Pages (recommended: fast, and matches the other demos),
   or a `/3d` route inside the Next.js app (one product, but heavier and tied to the app's build).
2. **Step 7:** show the what-if as a clearly labelled mock-up now, or leave it as a roadmap card until it's built.
3. **Scope:** all of Jabodetabek (9,083 hexes), or start with DKI Jakarta (`jakarta_h3_scores.geojson`) for a smaller first cut.

## Repo conventions

Per `CLAUDE.md`, this should get a Linear ticket under E8 (Core Features) before code is written, a
`showcase/…` branch, and a PR. `docs/state.md`, `docs/EPICS_TASKS.md` and `docs/ARCHITECTURE.md` get
updated when it ships.
