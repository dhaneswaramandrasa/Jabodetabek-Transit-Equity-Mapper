# Data Ingestion Scripts

Scripts to download and compile raw datasets for the Jabodetabek Transit Equity Mapper.

## Prerequisites

```bash
pip install requests  # only external dependency (most scripts use stdlib urllib)
```

Python 3.10+ required.

## Run Order

Scripts are numbered in dependency order. Run sequentially:

```bash
# 1. GTFS transit feeds (TransJakarta auto-downloads; KRL/MRT require manual construction)
python src/ingestion/01_fetch_gtfs.py

# 2. OSM road network (~847 MB download)
python src/ingestion/02_fetch_osm.py

# 3. POIs from Overpass API (5 categories, rate-limited)
python src/ingestion/03_fetch_overpass.py

# 4. Administrative boundaries (GADM + BPS/HDX kelurahan)
python src/ingestion/04_fetch_boundaries.py

# 5. BPS demographic data (prints manual collection guide)
python src/ingestion/05_fetch_bps.py

# 6. WorldPop population raster (~98 MB download)
python src/ingestion/06_fetch_worldpop.py

# 7. LRT Jabodebek stations (generates GeoJSON from compiled coordinates)
python src/ingestion/07_compile_lrt.py
```

## Output Directory Structure

```
data/raw/
├── gtfs/
│   ├── transjakarta/
│   │   └── transjakarta_gtfs.zip       # Auto-downloaded
│   ├── krl/
│   │   └── README.md                   # Manual construction instructions
│   └── mrt/
│       └── README.md                   # Manual construction instructions
├── osm/
│   ├── java-latest.osm.pbf            # ~847 MB Java island extract
│   └── java-latest.osm.pbf.md5        # MD5 checksum from Geofabrik
├── overpass/
│   ├── hospitals.geojson
│   ├── schools.geojson
│   ├── markets.geojson
│   ├── industrial.geojson
│   └── government_offices.geojson
├── boundaries/
│   ├── gadm41_IDN.gpkg                # GADM levels 0-3 (kecamatan)
│   └── idn_adm_bps_20200401_SHP.zip   # BPS levels 0-4 (kelurahan)
├── bps/
│   ├── collection_guide.json           # Programmatic reference
│   ├── template_population.csv         # CSV template
│   ├── template_poverty.csv            # CSV template
│   └── {region}_{table}.csv            # Manually collected data
├── worldpop/
│   └── idn_ppp_2020_constrained.tif   # ~98 MB population raster
└── lrt/
    └── lrt_jabodebek_stations.geojson  # 18 stations compiled
```

## Script Details

### 01_fetch_gtfs.py
Downloads GTFS feeds for Jabodetabek transit. TransJakarta has an official feed at `gtfs.transjakarta.co.id`. KRL Commuterline and MRT Jakarta do NOT have official GTFS feeds as of March 2026 — these must be manually constructed from schedule data.

**Outputs**: `data/raw/gtfs/transjakarta/transjakarta_gtfs.zip`

### 02_fetch_osm.py
Downloads the Java island PBF extract from Geofabrik (~847 MB). This covers all of Jabodetabek. The PBF is clipped to the Jabodetabek bbox during the wrangling step using `osmium extract`.

**Outputs**: `data/raw/osm/java-latest.osm.pbf`

### 03_fetch_overpass.py
Queries the Overpass API for 5 POI categories within the Jabodetabek bounding box. Uses strict OSM tag filters from methodology.md section 2.6e. Post-download filtering required to apply name-based and size-based criteria.

**Outputs**: `data/raw/overpass/{category}.geojson` (5 files)

### 04_fetch_boundaries.py
Downloads administrative boundary data from two sources:
- GADM v4.1 GeoPackage (levels 0-3, kecamatan is the finest level)
- BPS/HDX Shapefile (levels 0-4, includes kelurahan/desa)

**Outputs**: `data/raw/boundaries/gadm41_IDN.gpkg`, `data/raw/boundaries/idn_adm_bps_20200401_SHP.zip`

### 05_fetch_bps.py
Prints a detailed guide for manually collecting BPS demographic data from 9 regional BPS websites. Generates template CSVs and a JSON collection guide.

**Outputs**: `data/raw/bps/collection_guide.json`, template CSVs

### 06_fetch_worldpop.py
Downloads the WorldPop Indonesia 2020 constrained population GeoTIFF (~98 MB, ~100m resolution). Used for dasymetric mapping of socioeconomic data to H3 hexagons.

**Outputs**: `data/raw/worldpop/idn_ppp_2020_constrained.tif`

### 07_compile_lrt.py
Generates a GeoJSON file of all 18 LRT Jabodebek stations with manually compiled coordinates. No GTFS schedule data is available — LRT is included as point proximity only.

**Outputs**: `data/raw/lrt/lrt_jabodebek_stations.geojson`

## Idempotency

All download scripts skip files that already exist. To re-download, delete the target file and re-run.

## Manual Steps Required

1. **KRL GTFS**: Must be constructed manually from commuterline.id schedule data or community APIs (github.com/comuline/api)
2. **MRT GTFS**: Must be constructed manually from jakartamrt.co.id schedule data
3. **BPS data**: Must be manually collected from 9 regional BPS websites (see script 05 output)
4. **POI filtering**: Post-download filtering needed for hospitals (verify tipe A/B), schools (SMA/SMK/University only), markets (major only), industrial (>10ha), gov offices (kelurahan/kecamatan offices)
5. **LRT coordinates**: Verify approximate coordinates against OpenStreetMap

## Estimated Download Sizes

| Dataset | Size | Time (10 Mbps) |
|---------|------|----------------|
| TransJakarta GTFS | ~1-2 MB | <1 sec |
| Java OSM PBF | ~847 MB | ~12 min |
| Overpass POIs (all) | ~1-5 MB | <1 min |
| GADM GeoPackage | ~200 MB | ~3 min |
| BPS/HDX Shapefile | ~470 MB | ~6 min |
| WorldPop GeoTIFF | ~98 MB | ~1.5 min |
| **Total** | **~1.6 GB** | **~23 min** |
