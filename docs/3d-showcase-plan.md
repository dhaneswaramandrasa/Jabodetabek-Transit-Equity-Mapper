# 3D Showcase Map: Build Spec

**Status:** ready to build · **Owner:** Dhaneswara · **Date:** 2026-10-30
**Decisions (confirmed):** static page on GitHub Pages · all of Jabodetabek · step 7 as a labelled mock-up · no Linear ticket

This spec is written for an agent picking the work up cold. Everything needed is here or in the files it links.

---

## 1. Goal

One scroll-through 3D map that shows what this project has found so far and what it is building towards.
It sits at the same level as the portfolio's other demos, and it is a fast, linkable showcase. It does **not**
replace the Next.js app in `web/`; it links into it.

It uses **real open data** (GTFS, OSM, BPS, WorldPop) already processed in this repo. Nothing is simulated.
Each step carries a status badge so unfinished parts read as a roadmap, not as results:

| Badge | Meaning | Colour |
|---|---|---|
| **Done** | computed by the pipeline; numbers match `web/public/data/equity_summary.json` | green |
| **Preliminary** | computed, with a known limitation shown on screen | amber |
| **Planned** | designed in `docs/methodology.md` / `docs/prd.md`, not built; shown as a mock-up | grey, dashed border |

### Reference implementation

Copy the structure, style and interaction patterns from the Omni demo. It is a single static HTML file with the
same stack:

- live: https://dhaneswaramandrasa.github.io/omni-market-intelligence/
- source: https://github.com/dhaneswaramandrasa/omni-market-intelligence/blob/main/web/index.html
- Pages workflow: https://github.com/dhaneswaramandrasa/omni-market-intelligence/blob/main/.github/workflows/pages.yml

Reuse from it: the dark basemap, glass panels (left story panel, right info card), step tabs with Back/Next,
`?step=N` deep links, `?embed` mode (hides panels, for recording), hover tooltip, the `flyTo` per step and the
mobile layout (panel at the bottom).

---

## 2. Story: 7 steps

| # | Tab | Heading | Map | Right card | Status |
|---|---|---|---|---|---|
| 1 | Need | **Who needs transit** | H3 hexes as columns. Height = `population`, colour = `tni_score` on the warm ramp | What TNI is made of (density, poverty, expenditure, zero-vehicle households, dependency); total population | Done |
| 2 | Access | **Where transit goes** | Transit routes as glowing paths in mode colours + stops; hexes recolour to `tai_score` on the cool ramp, lower height | Route counts by mode (MRT 2, LRT 4, KRL 7, TransJakarta 61); the 5 TAI layers listed, with L4 and L5 marked "placeholder" | Done |
| 3 | Gap | **The gap** | Quadrant colours. Q4 (high need, low access) hexes raised and glowing red; Q1–Q3 low and muted. Quadrant legend can be toggled | Big number: **28.0% of hexes / 27.6% of kelurahan are transit deserts**; quadrant counts; a 2×2 quadrant diagram | Done |
| 4 | Resolution | **Resolution changes the story** | Toggle **Kelurahan ↔ H3**: kelurahan as extruded polygons coloured by quadrant vs. hex columns | Gini of TAI **0.24 (kelurahan) → 0.61 (H3)**; Cohen's κ **0.61**; **29%** of areas change quadrant; small 4×4 confusion matrix | Done |
| 5 | Clusters | **Clusters, not noise** | `lisa_cluster` colours: HH, LL, HL, LH, NS (NS faded) | Global Moran's I of TAI: **0.89 kelurahan, 0.94 H3** (p = 0.001); cluster counts | Done |
| 6 | Commute | **The commute to Sudirman** | `ArcLayer` from each routed hex centroid to Sudirman–Thamrin, colour = `poi_reach_cbd_min` (1–121 min). Unrouted hexes grey | **1,021 of 9,083 hexes (11.2%) routed with r5py**; the rest default to 180 min. Say why: limited GTFS coverage | **Preliminary** |
| 7 | What-if | **What a new station would change** | Mock-up: a fixed station pin at a chosen Q4 cluster, a pulsing catchment ring (~800 m and 1.5 km), hexes inside animate from red to amber | Label **"Mock-up: simulator not built yet"**. Explain the planned method (re-score L1/L2 in the catchment, recount Q4); what's missing (L4 last-mile and L5 cost layers are placeholders, full r5py routing). End with a roadmap list and a link to the app | **Planned** |

Text tone: short, plain sentences, like the Omni demo. Every number on screen must come from the exported
JSON (no hard-coded stats except the GTFS route counts, which also come from the data).

**Step 7 location:** pick the largest contiguous Q4 HH-cluster in Bodetabek from the data (largest connected Q4
component by population) and put the pin at its population-weighted centroid. Compute this in the export script
and store it as `mockup_station`; do not hand-pick coordinates.

---

## 3. Data export: `scripts/export_showcase.py`

Inputs (all exist today):

| File | Rows | Used fields |
|---|---|---|
| `web/public/data/h3_scores.geojson` | 9,083 | `h3_index`, `population`, `tni_score`, `tai_score`, `equity_gap`, `quadrant`, `poi_reach_cbd_min`, `tai_l3_cbd_journey`, `n_transit_stops` |
| `web/public/data/lisa_h3.geojson` | 9,083 | `h3_index`, `lisa_cluster` |
| `web/public/data/kelurahan_scores.geojson` | 1,502 | geometry, `kelurahan_name`, `kota_kab_name`, `population`, `tni_score`, `tai_score`, `quadrant` |
| `web/public/data/lisa_kelurahan.geojson` | 1,502 | `lisa_cluster` |
| `web/public/data/jakarta_transit_routes.geojson` | 74 | geometry, `type`, `line` |
| `web/public/data/jakarta_transit_stops.geojson` | 407 | geometry, `type`, `name` |
| `web/public/data/equity_summary.json` | – | all summary stats + `resolution_comparison` |
| `data/processed/poi/cbd_zones.geojson` | – | Sudirman–Thamrin point (arc target) |

Output: **`showcase/data/showcase.json`**, under 3 MB. Shape:

```jsonc
{
  "meta": { "generated": "...", "source_commit": "...", "stats": { /* equity_summary.json, as is */ },
            "cbd": [lon, lat], "mockup_station": { "lonlat": [lon, lat], "q4_hexes_in_ring": 123 } },
  "hex": {                     // column-oriented arrays, same order
    "lon": [...], "lat": [...],             // from h3.cell_to_latlng(h3_index), 5 dp
    "pop": [...],                            // int
    "tni": [...], "tai": [...], "gap": [...],// 3 dp
    "q": [...],                              // 1-4
    "lisa": [...],                           // 0 NS, 1 HH, 2 LL, 3 HL, 4 LH
    "cbd_min": [...]                         // int or -1 when not routed
  },
  "kel": { "type": "FeatureCollection", "features": [...] },   // simplified (shapely simplify 0.0005, preserve_topology), 4 dp coords, props: name, kota, pop, tni, tai, q, lisa
  "routes": { ... },  // 4 dp, props: type, line
  "stops":  { ... }   // props: type, name
}
```

Rules:
- Use `h3` (already a pipeline dependency) for centroids; don't ship hex polygons (`ColumnLayer` with
  `diskResolution: 6` draws hexes from centroids; radius ≈ 430 m for res-8 with a small gap).
- Round floats, write with `separators=(",", ":")`. Print the file size and fail if it is over 3 MB.
- Assert counts: 9,083 hexes, 1,502 kelurahan, 74 routes, 407 stops, and that Q4 share matches `equity_summary.json`.
- Note: `jakarta_transit_routes.geojson` / `stops` may only cover DKI routes. If routes outside DKI exist in
  `data/processed/transit/`, prefer those for full Jabodetabek and say which one was used in a comment.

---

## 4. Page: `showcase/index.html`

- One static file, no build step. MapLibre GL **4.7.1** and deck.gl **9.0.38** from unpkg (same as the Omni demo), plus
  Archivo + IBM Plex Mono from Google Fonts.
- Basemap: `https://tiles.openfreemap.org/styles/dark`. Start view: center ≈ [106.83, -6.30], zoom 9.4, pitch 50, bearing -12.
- Layers: `ColumnLayer` (hexes), `PolygonLayer` extruded (kelurahan, step 4), `PathLayer` (routes, wide + low-alpha
  underlay for glow), `ScatterplotLayer` (stops, step 7 ring), `ArcLayer` (step 6), all via `deck.MapboxOverlay`.
- Colours:
  - need ramp (warm): `#2b1660 → #8a1d8f → #e0446a → #fb9a3c → #fde16a`
  - access ramp (cool): `#0b1f4d → #1d4e89 → #2a9fd6 → #7fe3f0`
  - quadrants: Q1 `#4fbf8f` well served, Q2 `#6c7bd9` overserved, Q3 `#5b6070` low priority, **Q4 `#ff3b5c` desert**
  - LISA: HH `#ff3b5c`, LL `#2a9fd6`, HL `#ffb347`, LH `#9b7bff`, NS `#3a3f55` at low alpha
  - modes: MRT `#e5484d`, LRT `#9b7bff`, KRL `#ffb347`, TransJakarta `#38bdf8`
- Height scaling: sqrt of the value, capped; heights animate on step change (`transitions: {getElevation: 600}`).
- Each step: badge (Done / Preliminary / Planned) next to the heading; camera `flyTo`; right card content as in §2.
- Hover tooltip: area name (kelurahan) or "Hex · pop N", plus the active metric.
- Footer: "Real open data: GTFS (Mobility Database), OSM, BPS, WorldPop. Methods and paper in this repo." and links to the
  repo and the Next.js app.
- Must load fast: one `fetch` of `showcase.json`, show a small loading line until it arrives, then an error message if it fails.

---

## 5. Deploy, README, portfolio

1. `.github/workflows/pages.yml` publishing the `showcase/` folder (copy the Omni workflow, change `path: showcase`).
   Repo owner sets **Settings → Pages → Source: GitHub Actions** once. Live URL:
   `https://dhaneswaramandrasa.github.io/jabodetabek-transit-equity-mapper/`.
   The Next.js app on Vercel is untouched.
2. Record a 9–12 s loop of step 3 (Q4 deserts rising) in `?embed&step=2` mode with Playwright, convert it to
   `docs/showcase-3d.gif` (720 px wide, 12 fps, under 5 MB) with ffmpeg.
3. **README:** put the GIF at the very top, linked to the live page, with a centred "▶ Open the 3D map" link and a
   one-line caption. Same block as the top of https://github.com/dhaneswaramandrasa/omni-market-intelligence.
4. **Portfolio** (separate repo `dhaneswaramandrasa.github.io`, separate PR): add a card in "Industry work" or
   "Research" with poster + mp4 loop, linking to the live map and the repo.

---

## 6. Acceptance criteria

- [ ] `python scripts/export_showcase.py` runs from a clean checkout and writes `showcase/data/showcase.json` under 3 MB with the asserted counts
- [ ] `cd showcase && python -m http.server` shows all 7 steps with no console errors; `?step=0…6` deep links work
- [ ] Every number on screen matches `equity_summary.json` / the exported data
- [ ] Each step shows its badge; step 6 states the 11.2% routing coverage; step 7 is clearly labelled a mock-up
- [ ] Works on a 390 px wide phone (panel at the bottom, map visible)
- [ ] Pages workflow deploys; live URL loads
- [ ] README opens with the GIF and the "Open the 3D map" link
- [ ] `docs/state.md`, `docs/ARCHITECTURE.md` (new `showcase/` folder + Pages deploy) updated per `CLAUDE.md` session-end rules

## 7. Out of scope

- Changing scores, the pipeline or `docs/methodology.md`
- Building the real what-if simulator (step 7 stays a mock-up)
- Changes to the Next.js app in `web/`
