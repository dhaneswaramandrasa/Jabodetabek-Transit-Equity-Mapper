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
| Framework | Next.js (App Router) |
| Map | deck.gl + Mapbox GL |
| State | Zustand |
| Data pipeline | Python (geopandas, r5py, h3-py, pysal) |
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
├── app/                    — Next.js pages
├── components/             — UI components
├── lib/                    — Types, data utilities, constants
├── public/
│   ├── data/               — GeoJSON for map rendering
│   └── dataset/            — Cleaned data for download (CC BY 4.0)
├── src/                    — Python data pipeline (offline)
│   ├── ingestion/          — Data acquisition
│   ├── processing/         — Wrangling, scoring, H3 derivation
│   ├── analysis/           — Gini, LISA, sensitivity
│   └── export/             — Export to web-ready GeoJSON
├── docs/                   — Living project documentation
└── CLAUDE.md               — Agent instructions
```

## Getting Started

```bash
# Install dependencies
npm install

# Set environment variable
cp .env.example .env.local
# Add your NEXT_PUBLIC_MAPBOX_TOKEN

# Run dev server
npm run dev
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
