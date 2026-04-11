# Jabodetabek Transit Equity Mapper

A dual-resolution spatial diagnostic that maps transit equity gaps across the Jabodetabek metropolitan region (Jakarta + Bogor, Depok, Tangerang, Bekasi). Identifies where public transit accessibility fails to match socioeconomic need — and where the next bus route or station would reduce transit poverty the most.

## What This Does

Every spatial unit in Jabodetabek (both administrative kelurahan and H3 hexagons) is scored on two composite indices:

- **Transit Need Index (TNI)** — population density, poverty rate, household expenditure, vehicle ownership, dependency ratio
- **Transit Accessibility Index (TAI)** — 5-layer model: first-mile quality, service quality, CBD journey chain, last-mile quality, cost competitiveness vs car and motorcycle

Units are classified into four quadrants:

| Quadrant | Meaning |
|----------|---------|
| Q1: Well-Served | High need, high access — adequate match |
| Q2: Overinvested | Low need, high access — potential overinvestment |
| Q3: Low Priority | Low need, low access |
| Q4: Transit Desert | **High need, low access — priority for intervention** |

## Key Features

- **Quadrant equity map** — choropleth at kelurahan and H3 resolution
- **Dual-resolution toggle** — switch between administrative and hexagonal views to expose MAUP effects
- **CBD journey chain visualization** — full multi-modal commute path from any area to Sudirman–Thamrin
- **Transit competitive zone map** — where transit beats car/motorcycle in generalized cost (and where it doesn't)
- **What-if simulator** — place a hypothetical station and see equity score changes
- **Downloadable dataset** — CC BY 4.0

## Two Outputs

| Output | Description |
|--------|-------------|
| **Research paper** | Transit equity gap analysis methodology + Jabodetabek findings |
| **Web product** | Interactive map tool — this repo |

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | Next.js 14 (App Router) — lives in `web/` |
| Map | deck.gl + MapLibre GL |
| State | Zustand |
| Data pipeline | Python (geopandas, r5py, h3-py, pysal) — lives in `src/` |
| Hosting | Vercel |

## Data Sources

All open data:

- TransJakarta BRT, KRL Commuterline, MRT Jakarta — GTFS feeds via [Mobility Database](https://database.mobilitydata.org)
- LRT Jabodebek — manually compiled station locations
- Road network — [OpenStreetMap via Geofabrik](https://download.geofabrik.de/asia/indonesia.html)
- POIs — [Overpass API](https://overpass-api.de) (hospitals, schools, markets, industrial zones, government offices, CBD zones)
- Demographics — [BPS](https://bps.go.id) (population, poverty, expenditure)
- Population grid — [WorldPop](https://www.worldpop.org) (~100m resolution)
- Hexagonal grid — [H3](https://h3geo.org) resolution 8 (~0.74 km²)

## Project Structure

```
├── web/                        — Next.js 14 web app (monorepo — see below)
│   ├── src/
│   │   ├── app/                — App Router pages + API routes
│   │   ├── components/         — UI components
│   │   ├── hooks/              — Data hooks (AI summary, demographics, POIs)
│   │   └── lib/                — Store, color scale, types
│   └── public/data/            — GeoJSON + analysis files served to browser
├── src/                        — Python data pipeline (offline)
│   ├── ingestion/              — Data acquisition
│   ├── processing/             — Wrangling, scoring, H3 derivation
│   └── analysis/               — Gini, LISA, sensitivity
├── scripts/
│   └── export_to_web.py        — Exports pipeline output → web/public/data/
├── data/                       — Raw + processed data (gitignored)
├── paper/                      — Research paper sections
├── docs/                       — Living project documentation
└── CLAUDE.md                   — Agent instructions
```

## Running the Web App

The web prototype lives in `web/`. From the repo root:

```bash
cd web

# Install dependencies
npm install

# Copy environment variables
cp .env.example .env.local
# Edit .env.local — add your API keys:
#   ANTHROPIC_API_KEY=...        (AI analysis card)
#   NEXT_PUBLIC_MAPTILER_KEY=... (basemap tiles, optional)

# Run dev server
npm run dev
# → http://localhost:3000
```

**After running the data pipeline**, export fresh data to the web app:

```bash
# From repo root
python scripts/export_to_web.py
# Writes kelurahan_scores.geojson, h3_scores.geojson,
# equity_summary.json, lorenz_*.csv, lisa_*.geojson
# into web/public/data/
```

**Production build:**

```bash
cd web && npm run build
```

## Documentation

See `docs/` for full project documentation:

- [`docs/methodology.md`](docs/methodology.md) — research methodology, TAI/TNI formulas, data pipeline
- [`docs/DATA_MODEL.md`](docs/DATA_MODEL.md) — complete schema for kelurahan and H3 levels
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — tech stack, data flow, deployment
- [`docs/prd.md`](docs/prd.md) — product requirements, personas, features
- [`docs/ROADMAP.md`](docs/ROADMAP.md) — milestones and weekly plan

## Research Context

Over 30 million people live in Jabodetabek. Millions of lower-to-middle-income suburban commuters depend on private vehicles because transit service is concentrated in central Jakarta. This project provides an evidence-based answer to: **"Where should the next bus route or station go to reduce transit poverty the most?"**

Three gaps this project addresses:

1. No composite need-vs-access gap framework spanning the full Jabodetabek metro area
2. No dual-resolution comparison (kelurahan vs H3) exposing how spatial unit choice affects equity conclusions
3. No what-if simulation embedded in an equity framework to make gap analysis actionable

## License

- **Code**: MIT
- **Dataset**: CC BY 4.0
