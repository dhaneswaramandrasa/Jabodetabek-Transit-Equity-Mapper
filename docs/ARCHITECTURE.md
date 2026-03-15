# Architecture

**Last updated**: 2026-03-16
**Status**: Skeleton — product not built yet. Will be updated after E7 (UI Foundation).

---

## Stack

| Layer | Technology | Notes |
|-------|-----------|-------|
| Framework | Next.js (App Router) | Existing prototype at github.com/dhaneswaramandrasa/transit-access |
| Styling | Tailwind CSS | |
| Map | deck.gl + Mapbox GL | GeoJSON layers, choropleth, hexagon rendering |
| State | Zustand | Client-side state for map interactions, filters, selections |
| Data processing | Python (geopandas, r5py, h3-py, pysal) | Offline pipeline; output consumed by web app as static GeoJSON |
| Hosting | Vercel | Static export + serverless if needed |

---

## Directory Structure (Planned)

```
jabodetabek-transity-equity-mapper/
├── app/                        — Next.js App Router pages
│   ├── page.tsx                — Main map view
│   └── layout.tsx              — Root layout
├── components/                 — UI components (< 150 lines each)
│   ├── MapView.tsx             — Main deck.gl map
│   ├── DetailPanel.tsx         — Click-to-explore side panel
│   ├── QuadrantLegend.tsx      — Quadrant color legend
│   ├── CostComparisonCard.tsx  — Three-way GC breakdown
│   ├── TAIBreakdownCard.tsx    — 5-layer TAI scores
│   ├── ResolutionToggle.tsx    — Kelurahan / H3 switch
│   ├── WhatIfSimulator.tsx     — Station placement tool
│   └── JourneyChainViz.tsx     — CBD journey chain display
├── lib/
│   ├── types.ts                — TypeScript interfaces = DATA_MODEL.md schema
│   ├── mock-data.ts            — Must match DATA_MODEL.md exactly
│   ├── data-utils.ts           — Wrangling helpers (filter, aggregate, normalize)
│   └── constants.ts            — CBD zones, quadrant thresholds, color scales
├── public/
│   ├── data/                   — GeoJSON files consumed by map
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
│   ├── ingestion/              — Data acquisition scripts
│   ├── processing/             — Wrangling, scoring, H3 derivation
│   ├── analysis/               — Gini, LISA, sensitivity
│   └── export/                 — Export to web-ready GeoJSON
├── data/                       — Raw + processed data (gitignored)
│   ├── raw/                    — Downloaded datasets
│   └── processed/              — Pipeline outputs
│       ├── transit/
│       ├── networks/
│       ├── poi/
│       ├── demographics/
│       ├── scores/
│       └── analysis/
├── paper/                      — Research paper sections
│   └── sections/
├── docs/                       — Living documentation
├── CLAUDE.md                   — Agent instructions
├── package.json
└── README.md
```

---

## Data Flow

```
Raw Sources                    Python Pipeline                Web App
─────────────                  ───────────────                ───────
GTFS feeds ─────┐
OSM PBF ────────┤
Overpass API ───┤              src/ingestion/
BPS tables ─────┤──────────▶   src/processing/  ──────▶  public/data/*.geojson
WorldPop TIFF ──┤              src/analysis/              (static files)
GADM boundaries ┤              src/export/                     │
H3 grid (gen) ──┘                                              ▼
                                                         Next.js + deck.gl
                                                         (client-side rendering)
```

---

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `NEXT_PUBLIC_MAPBOX_TOKEN` | Mapbox GL access token for base map | Yes |
| `GOOGLE_MAPS_API_KEY` | Distance Matrix API (v2 traffic extension) | No (v2) |

---

## Deployment

- **Platform**: Vercel (free tier)
- **Build**: `next build` → static export
- **GeoJSON budget**: Total < 15 MB for acceptable load time
- **CDN**: Vercel Edge Network for static assets
- **Domain**: TBD (custom domain optional)

---

## Key Architectural Decisions

| Decision | Rationale |
|----------|-----------|
| Static GeoJSON, no server API | All data pre-computed offline; no API keys client-side; faster loads |
| deck.gl for map rendering | Handles large GeoJSON (15k+ hexagons) better than Leaflet; GPU-accelerated |
| Python pipeline separate from web app | Heavy geospatial compute (r5py, pysal) not suitable for browser; clean separation |
| Zustand over Redux | Simpler for map state (selected unit, active layer, resolution toggle) |
| Dual-resolution as two GeoJSON files | Simpler than on-the-fly aggregation; consistent with pre-computed scores |
