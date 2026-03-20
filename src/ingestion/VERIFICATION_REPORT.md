# Data Source Verification Report

**Date**: 2026-03-20
**Task**: MVP-6 (E0-007) — Define data acquisition plan and verify source access
**Author**: Automated verification via web search and fetch

---

## Summary

| # | Dataset | Status | URL Verified | Format | Freshness | Notes |
|---|---------|--------|-------------|--------|-----------|-------|
| 1 | TransJakarta BRT GTFS | **Accessible** | gtfs.transjakarta.co.id | GTFS ZIP | 2026-03-14 | Official endpoint confirmed; 236 routes, 8421 stops |
| 2 | KRL Commuterline GTFS | **Unavailable** | N/A | N/A | N/A | No official GTFS feed exists; manual construction required |
| 3 | MRT Jakarta GTFS | **Unavailable** | N/A | N/A | N/A | No official GTFS feed exists; manual construction required |
| 4 | LRT Jabodebek stations | **Manual** | Wikipedia/OSM | GeoJSON | 2023-08-28 (opening) | 18 stations compiled manually; coordinates approximate |
| 5 | OSM road network | **Accessible** | download.geofabrik.de | PBF | Updated daily | Java extract ~847 MB; Geofabrik mirrors updated daily |
| 6 | POIs (strict categories) | **Accessible** | overpass-api.de | JSON→GeoJSON | Live OSM data | API operational; rate-limited (2 concurrent queries) |
| 7 | Admin boundaries | **Accessible** | gadm.org + data.humdata.org | GPKG/SHP | 2020-04-01 (BPS) | GADM=level 3 (kecamatan); HDX/BPS=level 4 (kelurahan) |
| 8 | BPS demographic data | **Manual** | jakarta.bps.go.id + regional | CSV/tables | 2023-2024 | 9 regional BPS sites; manual collection required |
| 9 | WorldPop population raster | **Accessible** | data.worldpop.org | GeoTIFF | 2020 | 98.33 MB; ~100m resolution; CC BY 4.0 |
| 10 | H3 hexagonal grid | **N/A** | Generated in code | N/A | N/A | h3-py library; no external download needed |

**Accessible**: 5 of 10 (auto-downloadable)
**Manual required**: 3 of 10 (BPS, KRL GTFS, MRT GTFS)
**Self-generated**: 2 of 10 (LRT compiled, H3 grid)

---

## Detailed Findings

### 1. TransJakarta BRT GTFS

- **URL**: `https://gtfs.transjakarta.co.id/files/file_gtfs.zip`
- **Status**: Confirmed accessible (HTTP 200)
- **Feed freshness**: Last fetched 2026-03-14 (per Transitland)
- **Content**: 1 agency (PT Transportasi Jakarta), 236 routes, 8,421 stops
- **Calendar span**: 2004-01-15 through 2027-12-31
- **feed_info.txt**: Not included in latest version
- **Size**: ~1-2 MB
- **Verification needed**: Check if feed includes Mikrotrans feeder routes (inspect routes.txt route_type field)
- **Alternative source**: TUMI Datahub has an older snapshot (2019 vintage, published 2024-04-15)
- **Transitland feed ID**: f-transjakarta~id

### 2. KRL Commuterline GTFS

- **URL**: No official GTFS endpoint exists
- **Status**: UNAVAILABLE — KAI Commuter (operator) does not publish GTFS
- **Searched**: Mobility Database, Transitland, TUMI Datahub, GitHub — none have KRL GTFS
- **Fallback options**:
  1. `github.com/comuline/api` — Community API with KRL schedule data (JSON, not GTFS)
  2. `github.com/rasyidstat/krl` — R package with station and schedule data
  3. `commuterline.id` — Official website with schedule tables (would need scraping)
- **Recommendation**: Construct GTFS manually from schedule data. KRL has well-documented routes and schedules (GAPEKA 2025). The comuline/api project may provide a structured data source.
- **Impact**: Without KRL GTFS, r5py cannot route via KRL. This is a critical blocker for TAI computation since KRL is the backbone of Jabodetabek commuter rail.

### 3. MRT Jakarta GTFS

- **URL**: No official GTFS endpoint exists
- **Status**: UNAVAILABLE — MRT Jakarta does not publish GTFS
- **Searched**: Mobility Database, Transitland, TUMI Datahub, GitHub — none have MRT GTFS
- **Fallback options**:
  1. `github.com/reksamamur/mrt-jakarta-api` — Community API with MRT station/schedule data
  2. `jakartamrt.co.id` — Official website with schedule tables
- **Recommendation**: Construct GTFS manually. MRT has only 13 stations (North-South line) with simple schedules (every 5-10 minutes). Manual GTFS construction is feasible in 1-2 hours.
- **Impact**: Lower than KRL since MRT serves only a small corridor, but still needed for accurate r5py routing.

### 4. LRT Jabodebek Stations

- **URL**: Wikipedia + OpenStreetMap (manual compilation)
- **Status**: Compiled — 18 stations across 2 lines
- **Lines**:
  - Cibubur: Dukuh Atas → Harjamukti (12 stations)
  - Bekasi: Dukuh Atas → Jati Mulya (14 stations, 8 shared with Cibubur)
- **Coordinate accuracy**: Approximate (~50m), sourced from OSM/Maps
- **Wikipedia access**: Blocked by 403 (bot protection) during automated verification; coordinates compiled from OSM and cross-referenced
- **Schedule data**: Not available as GTFS; LRT included as point proximity only per methodology.md
- **Fare tier**: Tier 2 (Rp 5,000-20,000, distance-based)

### 5. OSM Road Network

- **URL**: `https://download.geofabrik.de/asia/indonesia/java-latest.osm.pbf`
- **Status**: Confirmed accessible
- **File size**: ~847 MB
- **Update frequency**: Daily (Geofabrik mirrors)
- **Last update observed**: 2026-03-18T21:21:31Z
- **Post-download**: Clip to Jabodetabek bbox using osmium extract
- **Jabodetabek bbox**: S=-6.75, W=106.40, N=-6.05, E=107.15

### 6. POIs (Overpass API)

- **URL**: `https://overpass-api.de/api/interpreter`
- **Status**: Operational (confirmed via /api/status)
- **Rate limits**: 2 concurrent queries; 10-second delay between requests recommended
- **Database**: Live OSM data (continuously updated)
- **Endpoint**: gall.openstreetmap.de
- **Test query**: Attempted hospital count query — timed out (504) on first attempt, but API status confirmed operational. Queries may need bbox optimization.
- **Categories to query**: hospitals, schools, markets, industrial zones, government offices
- **Post-download filtering**: Required per methodology.md 2.6e

### 7. Administrative Boundaries

- **GADM v4.1**: `https://geodata.ucdavis.edu/gadm/gadm4.1/gpkg/gadm41_IDN.gpkg`
  - Status: Confirmed accessible
  - Levels: 0 (country) through 3 (kecamatan)
  - Format: GeoPackage
  - **Important**: GADM level 3 = kecamatan, NOT kelurahan
- **BPS/HDX**: `https://data.humdata.org/dataset/cod-ab-idn`
  - Status: Confirmed accessible
  - Levels: 0 through 4 (includes kelurahan/desa)
  - Format: Shapefile (470.2 MB)
  - Date: 2020-04-01
  - Features: Level 3 = 7,069 kecamatan; Level 4 = partial kelurahan coverage
  - **This is the primary source for kelurahan boundaries**

### 8. BPS Demographic Data

- **URLs**: 9 regional BPS websites (see script 05)
- **Status**: Websites accessible; data requires manual collection
- **Data available**: Population, poverty rate, household expenditure, age distribution
- **Granularity**: Mostly kecamatan level; some kelurahan-level population data
- **Format**: Published statistical tables (HTML/PDF); some downloadable as Excel
- **Latest data**: 2023-2024 publications ("Dalam Angka 2024/2025")
- **Access restrictions**: None (open), but no bulk download API
- **Effort estimate**: 2-4 hours manual collection across all 9 regions

### 9. WorldPop Population Raster

- **URL**: `https://data.worldpop.org/GIS/Population/Global_2000_2020_Constrained/2020/BSGM/IDN/idn_ppp_2020_constrained.tif`
- **Status**: Confirmed accessible
- **File size**: 98.33 MB
- **Resolution**: 3 arc-seconds (~100m at equator)
- **Year**: 2020
- **CRS**: WGS84 (EPSG:4326)
- **Units**: People per pixel
- **Method**: Random Forests-based dasymetric redistribution (BSGM)
- **License**: CC BY 4.0
- **NoData**: Unsettled areas (from BSGM model)
- **Also available via**: Humanitarian Data Exchange (HDX), Google Earth Engine

### 10. H3 Hexagonal Grid

- **Source**: Generated via h3-py library
- **No external download needed**
- **Resolution 8**: ~0.74 km² per cell, ~15,000-20,000 cells for Jabodetabek
- **Command**: `h3.polyfill_geojson(study_area_geojson, res=8)`

---

## Critical Blockers

### 1. KRL and MRT GTFS feeds do not exist (HIGH PRIORITY)

This is the most significant finding. Without KRL and MRT GTFS feeds, r5py cannot compute multi-modal transit routing, which is the foundation of TAI Layer 3 (CBD journey chain, weighted at 35% of TAI).

**Recommended action**: Create a new ticket to manually construct KRL and MRT GTFS feeds from published schedule data. This should be done before the wrangling pipeline (E6-002).

**Estimated effort**:
- KRL: 4-6 hours (complex network, many lines/stations, GAPEKA schedule)
- MRT: 1-2 hours (simple linear network, regular headways)

**Resources**:
- comuline/api (github.com/comuline/api) — structured KRL schedule data
- reksamamur/mrt-jakarta-api — structured MRT data
- GTFS specification: gtfs.org

### 2. BPS data requires manual collection (MEDIUM)

No API or bulk download. Plan 2-4 hours of manual work across 9 regional websites.

### 3. GADM does not include kelurahan level (RESOLVED)

GADM level 3 is kecamatan, not kelurahan. Resolved by using BPS/HDX shapefile which includes level 4 (kelurahan/desa).

---

## Recommendations for methodology.md 2.4 Update

The following clarifications should be added to the Data Acquisition Plan:

1. **TransJakarta GTFS**: Confirmed at `gtfs.transjakarta.co.id/files/file_gtfs.zip`. Feed refreshed regularly (last: 2026-03-14). 236 routes, 8,421 stops. Verify Mikrotrans inclusion.

2. **KRL/MRT GTFS**: NOT available from Mobility Database or any official source. Must be manually constructed from schedule APIs/websites. This is a prerequisite for r5py routing.

3. **Admin boundaries**: Primary source should be BPS/HDX shapefile (level 4 kelurahan), not GADM (which only goes to level 3 kecamatan). GADM useful as cross-reference for kecamatan boundaries.

4. **WorldPop**: Confirmed at data.worldpop.org. File: `idn_ppp_2020_constrained.tif` (98.33 MB). The "constrained" variant uses BSGM (Built-Settlement Growth Model) which excludes unsettled areas — appropriate for dasymetric mapping.

5. **Overpass API**: Operational but rate-limited. Use 10-second delays between queries. Cache results aggressively — repeated queries hit the same data.
