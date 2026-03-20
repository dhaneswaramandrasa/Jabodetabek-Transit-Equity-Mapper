# Architecture

**Last updated**: 2026-03-21
**Status**: **Signed off** — 2026-03-21 (MVP-83). Skeleton complete; will be updated as E6–E9 are implemented.

---

## Stack

| Layer | Technology | Notes |
|-------|-----------|-------|
| Framework | Next.js 14 (App Router) | Existing prototype at github.com/dhaneswaramandrasa/transit-access |
| Styling | Tailwind CSS | Utility-first; dark mode support for map UI |
| Map | deck.gl + MapLibre GL JS | GeoJSON layers, choropleth, hexagon rendering; MapLibre preferred over Mapbox for open-source |
| State | Zustand | Client-side state for map interactions, filters, selections |
| Data processing | Python 3.11+ (geopandas, r5py, h3-py, pysal) | Offline pipeline; output consumed by web app as static GeoJSON |
| Hosting | Vercel | Static export; free tier sufficient for portfolio project |

---

## Directory Structure

```
jabodetabek-transity-equity-mapper/
├── app/                        — Next.js App Router pages
│   ├── page.tsx                — Main map view
│   └── layout.tsx              — Root layout + metadata
├── components/                 — UI components (< 150 lines each)
│   ├── MapView.tsx             — Main deck.gl map container
│   ├── DetailPanel.tsx         — Click-to-explore side panel
│   ├── QuadrantLegend.tsx      — Quadrant color legend (Q1–Q4)
│   ├── CostComparisonCard.tsx  — Three-way GC breakdown (transit/car/motorcycle)
│   ├── TAIBreakdownCard.tsx    — 5-layer TAI score visualization
│   ├── ResolutionToggle.tsx    — Kelurahan ↔ H3 switch
│   ├── WhatIfSimulator.tsx     — Hypothetical station placement tool
│   ├── JourneyChainViz.tsx     — CBD journey chain display
│   ├── EquityDashboard.tsx     — Gini, Lorenz, quadrant distribution summary
│   └── TransitCompetitiveMap.tsx — TCR choropleth (green/amber/red)
├── lib/
│   ├── types.ts                — TypeScript interfaces = DATA_MODEL.md schema
│   ├── mock-data.ts            — Must match DATA_MODEL.md exactly
│   ├── data-utils.ts           — Wrangling helpers (filter, aggregate, normalize)
│   └── constants.ts            — CBD zones, quadrant thresholds, color scales
├── public/
│   ├── data/                   — GeoJSON files consumed by map (< 15 MB total)
│   │   ├── kelurahan_scores.geojson
│   │   ├── h3_scores.geojson
│   │   ├── cbd_zones.geojson
│   │   ├── road_network.geojson
│   │   └── transit_stops.geojson
│   └── dataset/                — Cleaned data for public download (CC BY 4.0)
│       ├── kelurahan_scores.geojson
│       ├── h3_scores.geojson
│       ├── equity_metrics.json
│       └── README.md
├── src/                        — Python data pipeline (offline)
│   ├── ingestion/              — Data acquisition scripts (MVP-6 verified)
│   ├── processing/             — Wrangling, scoring, H3 derivation
│   ├── analysis/               — Gini, LISA, sensitivity
│   └── export/                 — Export to web-ready GeoJSON
├── data/                       — Raw + processed data (gitignored)
│   ├── raw/
│   │   ├── gtfs/               — GTFS feeds (TransJakarta, KRL, MRT, LRT)
│   │   ├── osm/                — Java PBF extract
│   │   ├── boundaries/         — GADM/Geoportal kelurahan polygons
│   │   ├── demographics/       — BPS CSV/tables
│   │   └── worldpop/           — Population raster GeoTIFF
│   └── processed/
│       ├── transit/            — Unified stops, headways
│       ├── networks/           — Clipped road network, metrics
│       ├── poi/                — Filtered POIs by category
│       ├── demographics/       — Kelurahan-level demographics
│       ├── scores/             — TAI, TNI, quadrant at both resolutions
│       └── analysis/           — Gini, LISA, sensitivity outputs
├── paper/                      — Research paper sections
│   └── sections/
├── docs/                       — Living documentation
├── CLAUDE.md                   — Agent instructions
├── package.json
└── README.md
```

---

## Data Flow

### Pipeline Overview

```
Phase 1: Acquisition (src/ingestion/)
──────────────────────────────────────
GTFS feeds ─────┐
OSM PBF ────────┤
Overpass API ───┤──▶ data/raw/
BPS tables ─────┤
WorldPop TIFF ──┤
GADM boundaries ┘

Phase 2: Processing (src/processing/)
──────────────────────────────────────
data/raw/ ──▶ Steps 1–16 (kelurahan pipeline) ──▶ data/processed/scores/kelurahan_scores.*
          ──▶ Steps 17–22 (H3 pipeline)        ──▶ data/processed/scores/h3_scores.*

Phase 3: Analysis (src/analysis/)
─────────────────────────────────
data/processed/scores/ ──▶ Steps 23–25 (Gini, LISA, What-if) ──▶ data/processed/analysis/

Phase 4: Export (src/export/)
─────────────────────────────
data/processed/ ──▶ export_to_web.py ──▶ public/data/*.geojson (< 15 MB total)
                                    ──▶ public/dataset/*       (CC BY 4.0 download)

Phase 5: Serve (Next.js + Vercel)
─────────────────────────────────
public/data/*.geojson ──▶ fetch() in client ──▶ deck.gl layers ──▶ user interaction
```

### Pipeline Step Reference

Steps 1–25 are defined in `docs/methodology.md` §2.5. Key compute bottlenecks:
- **Step 14** (r5py kelurahan routing): ~16,200 queries, 2–4 hours
- **Step 21** (r5py H3 routing): ~15,000–20,000 queries, 8–16 hours
- **Step 24** (LISA at H3): spatial weights for ~15k+ units

---

## Frontend Architecture

### State Management (Zustand)

```
MapStore:
  selectedUnit: KelurahanUnit | H3Unit | null
  activeResolution: 'kelurahan' | 'h3'
  activeLayer: 'quadrant' | 'tai' | 'tni' | 'tcr' | 'road_network'
  whatIfStations: WhatIfStation[]
  filters: { kota_kab?: string, quadrant?: string[] }
```

### Component Hierarchy

```
layout.tsx
└── page.tsx
    ├── MapView.tsx (deck.gl canvas)
    │   ├── GeoJsonLayer (kelurahan choropleth)
    │   ├── H3HexagonLayer (H3 hexagons)
    │   ├── PathLayer (journey chain polylines)
    │   ├── ScatterplotLayer (transit stops, POIs)
    │   └── GeoJsonLayer (road network, toggleable)
    ├── ResolutionToggle.tsx
    ├── QuadrantLegend.tsx
    ├── DetailPanel.tsx (appears on click)
    │   ├── TAIBreakdownCard.tsx
    │   ├── CostComparisonCard.tsx
    │   └── JourneyChainViz.tsx
    ├── EquityDashboard.tsx
    ├── TransitCompetitiveMap.tsx
    └── WhatIfSimulator.tsx
```

### Data Loading Strategy

- All GeoJSON loaded client-side via `fetch()` on mount
- Kelurahan GeoJSON loaded by default; H3 loaded on toggle (lazy)
- Road network loaded on toggle (large file, lazy)
- No server-side API routes — everything is static

---

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `NEXT_PUBLIC_MAPBOX_TOKEN` | MapLibre/Mapbox GL access token for base map tiles | Yes |
| `GOOGLE_MAPS_API_KEY` | Distance Matrix API (v2 traffic extension) | No (v2) |

---

## Deployment

- **Platform**: Vercel (free tier)
- **Build**: `next build` → static export (`output: 'export'` in next.config)
- **GeoJSON budget**: Total < 15 MB for acceptable load time (target: < 5s initial load)
- **CDN**: Vercel Edge Network for static assets
- **Domain**: TBD (custom domain optional)
- **Performance targets**: Initial load < 5s, map click response < 1s

---

## Key Architectural Decisions

| Decision | Rationale |
|----------|-----------|
| Static GeoJSON, no server API | All data pre-computed offline; no API keys client-side; simplest deployment |
| deck.gl for map rendering | Handles large GeoJSON (15k+ hexagons) with GPU acceleration; built-in H3 layer |
| MapLibre over Mapbox | Open-source; free tile hosting options; compatible with deck.gl |
| Python pipeline separate from web app | Heavy geospatial compute (r5py, pysal) not suitable for browser; clean separation of concerns |
| Zustand over Redux | Simpler for map state (selected unit, active layer, resolution toggle); less boilerplate |
| Dual-resolution as two GeoJSON files | Simpler than on-the-fly aggregation; consistent with pre-computed scores; lazy-load H3 |
| What-if computed client-side | Simplified buffer model (no r5py needed); instant feedback; labeled as indicative |
