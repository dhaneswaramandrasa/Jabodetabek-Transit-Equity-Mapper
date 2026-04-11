# Architecture

**Last updated**: 2026-04-11
**Status**: Updated — MVP-109 monorepo consolidation. Web app moved from `transit-access` repo into `web/` here.

---

## Stack

| Layer | Technology | Notes |
|-------|-----------|-------|
| Framework | Next.js 14 (App Router) | Lives at `web/` in this repo (consolidated from transit-access repo via MVP-109) |
| Styling | Tailwind CSS | Utility-first; dark mode support for map UI |
| Map | deck.gl + MapLibre GL JS | GeoJSON layers, choropleth, hexagon rendering; MapLibre preferred over Mapbox for open-source |
| State | Zustand | Client-side state for map interactions, filters, selections |
| Data processing | Python 3.11+ (geopandas, r5py, h3-py, pysal) | Offline pipeline; output consumed by web app as static GeoJSON |
| Hosting | Vercel | Static export; free tier sufficient for portfolio project |

---

## Directory Structure

```
jabodetabek-transity-equity-mapper/        ← single monorepo (MVP-109)
├── web/                        — Next.js 14 web app (run: cd web && npm run dev)
│   ├── src/
│   │   ├── app/                — App Router pages (page.tsx, layout.tsx, api/)
│   │   ├── components/         — UI components (< 150 lines each)
│   │   │   ├── AccessibilityMap.tsx    — Main deck.gl map container
│   │   │   ├── ResultsLayout.tsx       — Click-to-explore side panel
│   │   │   ├── EntryScreen.tsx         — Persona selection entry screen
│   │   │   ├── EquityDashboard.tsx     — Gini, Lorenz, LISA, resolution stats
│   │   │   ├── MapLegend.tsx           — Quadrant color legend (Q1–Q4)
│   │   │   └── results/                — Card components (TransitScoreCard, DemographicsCard…)
│   │   ├── hooks/              — useAISummary, useDemographics, useReachablePOIs, useTransitStops
│   │   └── lib/
│   │       ├── store.ts        — Zustand store (HexProperties, MapStats, Persona…)
│   │       └── colorScale.ts   — TAI → color mapping (domain 0–1)
│   └── public/
│       └── data/               — Static GeoJSON + CSV served to browser
│           ├── kelurahan_scores.geojson  (2.8 MB)
│           ├── h3_scores.geojson         (17.9 MB — optimize in MVP-37)
│           ├── equity_summary.json
│           ├── lorenz_kelurahan.csv / lorenz_h3.csv
│           └── lisa_kelurahan.geojson / lisa_h3.geojson
├── src/                        — Python data pipeline (offline)
│   ├── ingestion/              — Data acquisition scripts
│   ├── processing/             — Wrangling, scoring, H3 derivation
│   └── analysis/               — Gini, LISA, sensitivity
├── scripts/
│   └── export_to_web.py        — Migrates pipeline output → web/public/data/
├── data/                       — Raw + processed data (gitignored)
│   ├── raw/
│   │   ├── gtfs/               — GTFS feeds (TransJakarta, KRL, MRT, LRT)
│   │   ├── osm/                — Java PBF extract
│   │   ├── boundaries/         — GADM/Geoportal kelurahan polygons
│   │   ├── demographics/       — BPS CSV/tables
│   │   └── worldpop/           — Population raster GeoTIFF
│   └── processed/
│       ├── scores/             — TAI, TNI, quadrant at both resolutions
│       └── analysis/           — Gini, LISA, sensitivity outputs
├── paper/                      — Research paper sections
│   └── sections/
├── docs/                       — Living documentation
├── notebooks/                  — EDA Jupyter notebooks
├── CLAUDE.md                   — Agent instructions
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

Phase 4: Export (scripts/export_to_web.py)
──────────────────────────────────────────
data/processed/ ──▶ export_to_web.py ──▶ web/public/data/*.geojson + analysis files

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
| Monorepo (pipeline + web app) | Single source of truth; `scripts/export_to_web.py` bridges `data/processed/` → `web/public/data/`; heavy compute still offline in `src/` |
| Zustand over Redux | Simpler for map state (selected unit, active layer, resolution toggle); less boilerplate |
| Dual-resolution as two GeoJSON files | Simpler than on-the-fly aggregation; consistent with pre-computed scores; lazy-load H3 |
| What-if computed client-side | Simplified buffer model (no r5py needed); instant feedback; labeled as indicative |
