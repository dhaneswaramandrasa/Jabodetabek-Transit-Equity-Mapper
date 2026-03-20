#!/usr/bin/env python3
"""
05_fetch_bps.py — BPS demographic data acquisition (manual collection guide).

BPS (Badan Pusat Statistik / Statistics Indonesia) data requires manual
collection from multiple regional BPS websites. There is no single API
or bulk download endpoint.

Required data:
  - Population by kecamatan/kelurahan
  - Poverty rate (% penduduk miskin) by kecamatan
  - Average household expenditure by kecamatan
  - Age distribution (for dependency ratio) by kecamatan
  - Vehicle ownership proxies (from SUSENAS or kecamatan estimates)

Sources (must be collected individually):
  - DKI Jakarta: jakarta.bps.go.id
  - Kota Bogor: kotabogor.bps.go.id
  - Kabupaten Bogor: bogorkab.bps.go.id
  - Kota Depok: depokkota.bps.go.id
  - Kota Tangerang: tangerangkota.bps.go.id
  - Kota Tangerang Selatan: tangselkota.bps.go.id
  - Kabupaten Tangerang: tangerangkab.bps.go.id
  - Kota Bekasi: bekasikota.bps.go.id
  - Kabupaten Bekasi: bekasikab.bps.go.id

Output: data/raw/bps/ (manually populated CSV/Excel files)

Usage:
  python src/ingestion/05_fetch_bps.py
"""

import json
import os
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "bps"

# BPS regional websites for Jabodetabek
BPS_SOURCES = {
    "DKI Jakarta (province)": {
        "url": "https://jakarta.bps.go.id",
        "kota_kab": [
            "Jakarta Pusat",
            "Jakarta Utara",
            "Jakarta Barat",
            "Jakarta Selatan",
            "Jakarta Timur",
            "Kepulauan Seribu",
        ],
        "sub_urls": {
            "Jakarta Pusat": "https://jakpuskota.bps.go.id",
            "Jakarta Utara": "https://jakutkota.bps.go.id",
            "Jakarta Barat": "https://jakbarkota.bps.go.id",
            "Jakarta Selatan": "https://jakselkota.bps.go.id",
            "Jakarta Timur": "https://jaktimkota.bps.go.id",
        },
        "publication_key": "Kota [X] Dalam Angka 2024/2025",
    },
    "Kota Bogor": {
        "url": "https://kotabogor.bps.go.id",
        "publication_key": "Kota Bogor Dalam Angka 2024/2025",
    },
    "Kabupaten Bogor": {
        "url": "https://bogorkab.bps.go.id",
        "publication_key": "Kabupaten Bogor Dalam Angka 2024/2025",
    },
    "Kota Depok": {
        "url": "https://depokkota.bps.go.id",
        "publication_key": "Kota Depok Dalam Angka 2024/2025",
    },
    "Kota Tangerang": {
        "url": "https://tangerangkota.bps.go.id",
        "publication_key": "Kota Tangerang Dalam Angka 2024/2025",
    },
    "Kota Tangerang Selatan": {
        "url": "https://tangselkota.bps.go.id",
        "publication_key": "Kota Tangerang Selatan Dalam Angka 2024/2025",
    },
    "Kabupaten Tangerang": {
        "url": "https://tangerangkab.bps.go.id",
        "publication_key": "Kabupaten Tangerang Dalam Angka 2024/2025",
    },
    "Kota Bekasi": {
        "url": "https://bekasikota.bps.go.id",
        "publication_key": "Kota Bekasi Dalam Angka 2024/2025",
    },
    "Kabupaten Bekasi": {
        "url": "https://bekasikab.bps.go.id",
        "publication_key": "Kabupaten Bekasi Dalam Angka 2024/2025",
    },
}

# Required tables to extract from each "Dalam Angka" publication
REQUIRED_TABLES = [
    {
        "id": "population",
        "description": "Jumlah Penduduk Menurut Kecamatan",
        "field": "population",
        "granularity": "kecamatan (some kelurahan)",
        "notes": "Total population by kecamatan. Some publications break down to kelurahan.",
    },
    {
        "id": "poverty",
        "description": "Persentase Penduduk Miskin / Garis Kemiskinan",
        "field": "poverty_rate",
        "granularity": "kota/kab (kecamatan if available)",
        "notes": "Poverty rate. Often only at kota/kab level; kecamatan estimates from Susenas.",
    },
    {
        "id": "expenditure",
        "description": "Rata-rata Pengeluaran Rumah Tangga per Bulan",
        "field": "avg_household_expenditure",
        "granularity": "kota/kab or kecamatan",
        "notes": "Monthly average household expenditure. Often only kota/kab level.",
    },
    {
        "id": "age_distribution",
        "description": "Penduduk Menurut Kelompok Umur",
        "field": "dependency_ratio (computed)",
        "granularity": "kecamatan",
        "notes": "Population by age group to compute dependency ratio = (age<15 + age>64) / (15-64).",
    },
    {
        "id": "vehicle_ownership",
        "description": "Jumlah Kendaraan Bermotor / Kepemilikan Kendaraan",
        "field": "zero_vehicle_hh_pct (modeled)",
        "granularity": "kota/kab",
        "notes": "Vehicle registration data as proxy. Will model zero_vehicle_hh_pct from "
                 "density + expenditure if household-level data unavailable.",
    },
]


def main():
    print("=" * 60)
    print("BPS Data Acquisition Guide — Jabodetabek Transit Equity Mapper")
    print("=" * 60)
    print(f"Output directory: {RAW_DIR}")
    print(f"Timestamp: {datetime.now().isoformat()}")

    RAW_DIR.mkdir(parents=True, exist_ok=True)

    print("\n" + "=" * 60)
    print("MANUAL DATA COLLECTION INSTRUCTIONS")
    print("=" * 60)

    print("\nBPS data must be manually downloaded from regional BPS websites.")
    print("For each region, find the '[Region] Dalam Angka 2024' or '2025' publication.")
    print("Extract the following tables and save as CSV in data/raw/bps/\n")

    print("--- Required tables ---")
    for table in REQUIRED_TABLES:
        print(f"\n  {table['id']}:")
        print(f"    Description: {table['description']}")
        print(f"    Maps to field: {table['field']}")
        print(f"    Granularity: {table['granularity']}")
        print(f"    Notes: {table['notes']}")

    print("\n\n--- BPS Regional Sources ---")
    for region, info in BPS_SOURCES.items():
        print(f"\n  {region}:")
        print(f"    URL: {info['url']}")
        print(f"    Publication: {info['publication_key']}")
        if "sub_urls" in info:
            print("    Municipal BPS sites:")
            for city, url in info["sub_urls"].items():
                print(f"      {city}: {url}")

    # Save the guide as JSON for programmatic reference
    guide = {
        "sources": BPS_SOURCES,
        "required_tables": REQUIRED_TABLES,
        "timestamp": datetime.now().isoformat(),
        "notes": [
            "BPS data requires manual collection from multiple regional websites.",
            "Look for '[Region] Dalam Angka 2024' or '2025' publications.",
            "Data is typically at kecamatan level; kelurahan estimates derived in wrangling.",
            "Poverty and expenditure may only be available at kota/kab level.",
            "Vehicle ownership will be modeled from density + expenditure proxies.",
            "Save each table as CSV in data/raw/bps/ with naming: {region}_{table_id}.csv",
        ],
    }

    guide_path = RAW_DIR / "collection_guide.json"
    with open(guide_path, "w") as f:
        json.dump(guide, f, indent=2, ensure_ascii=False)
    print(f"\n\nCollection guide saved: {guide_path}")

    # Create template CSV headers
    template_path = RAW_DIR / "template_population.csv"
    with open(template_path, "w") as f:
        f.write("province,kota_kab,kecamatan,kelurahan,population,year,source_url\n")
        f.write("DKI Jakarta,Jakarta Pusat,Gambir,,123456,2024,https://jakpuskota.bps.go.id/...\n")
    print(f"Template CSV saved: {template_path}")

    template_path2 = RAW_DIR / "template_poverty.csv"
    with open(template_path2, "w") as f:
        f.write("province,kota_kab,kecamatan,poverty_rate_pct,year,source_url\n")
        f.write("DKI Jakarta,Jakarta Pusat,,4.5,2024,https://jakpuskota.bps.go.id/...\n")
    print(f"Template CSV saved: {template_path2}")

    print("\n\n--- FILE NAMING CONVENTION ---")
    print("  data/raw/bps/{region}_{table_id}.csv")
    print("  Example: data/raw/bps/dki_jakarta_population.csv")
    print("  Example: data/raw/bps/kota_bekasi_age_distribution.csv")

    print("\n--- EXPECTED OUTPUT ---")
    print("After manual collection, the following files should exist:")
    for region in BPS_SOURCES:
        slug = region.lower().replace(" ", "_").replace("(", "").replace(")", "")
        for table in REQUIRED_TABLES:
            print(f"  data/raw/bps/{slug}_{table['id']}.csv")


if __name__ == "__main__":
    main()
