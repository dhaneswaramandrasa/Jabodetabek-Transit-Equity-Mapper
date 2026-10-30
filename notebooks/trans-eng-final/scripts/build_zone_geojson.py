"""
Build zone-level GeoJSON for the trans-eng web app.
Dissolves 360 kelurahan into 7 zones, merges attributes + scenario results.
"""

import json
import pathlib

import geopandas as gpd
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]  # notebooks/trans-eng-final/
REPO = ROOT.parents[1]  # repo root

# ── KEC_TO_ZONE mapping (from 01_data_prep.ipynb Cell 3) ──
KEC_TO_ZONE = {
    # J1a — Kota Bogor
    "BogorBarat": "J1a", "BogorSelatan": "J1a", "BogorTengah": "J1a",
    "BogorTimur": "J1a", "BogorUtara": "J1a", "TanahSereal": "J1a",
    # J1b — Kab. Bogor outer
    "Parung": "J1b", "Ciseeng": "J1b", "Kemang": "J1b", "GunungSindur": "J1b",
    # J2 — Kota Bekasi
    "BekasiBarat": "J2", "BekasiSelatan": "J2", "BekasiTimur": "J2",
    "BekasiUtara": "J2", "BandarGebang": "J2", "JatiAsih": "J2",
    "JatiSampurna": "J2", "MedanSatria": "J2", "MustikJaya": "J2",
    "PondokGede": "J2", "PondokMelati": "J2", "RawalumbuBekasi": "J2",
    # J3a — BSD Serpong
    "Serpong": "J3a", "SerpongUtara": "J3a", "Setu": "J3a",
    # J3b — Gading Serpong / Karawaci
    "Pagedangan": "J3b", "KelapaDua": "J3b", "Curug": "J3b",
    "Legok": "J3b", "Karawaci": "J3b",
    # J4 — Kota Depok
    "Beji": "J4", "Bojongsari": "J4", "Cilodong": "J4", "Cimanggis": "J4",
    "Cinere": "J4", "Cipayung": "J4", "Limo": "J4", "Pancoran Mas": "J4",
    "Sawangan": "J4", "Sukmajaya": "J4", "Tapos": "J4",
    # J5 — South Jakarta
    "Cilandak": "J5", "Jagakarsa": "J5", "KebayoranBaru": "J5",
    "KebayoranLama": "J5", "Mampang Prapatan": "J5", "Pancoran": "J5",
    "PasarMinggu": "J5",
}

ZONE_NAMES = {
    "J1a": "Kota Bogor",
    "J1b": "Kab. Bogor Outer (Parung)",
    "J2": "Kota Bekasi",
    "J3a": "BSD Serpong",
    "J3b": "Gading Serpong / Karawaci",
    "J4": "Kota Depok",
    "J5": "South Jakarta",
}


def main():
    # ── Load kelurahan polygons ──
    kel_path = REPO / "data" / "processed" / "scores" / "kelurahan_scores.geojson"
    print(f"Loading {kel_path} ...")
    gdf = gpd.read_file(kel_path)
    print(f"  {len(gdf)} kelurahan loaded")

    # ── Assign zone_id via kecamatan_name ──
    gdf["zone_id"] = gdf["kecamatan_name"].map(KEC_TO_ZONE)
    matched = gdf.dropna(subset=["zone_id"]).copy()
    print(f"  {len(matched)} kelurahan matched to zones")

    # ── Dissolve into 7 zone polygons ──
    zones = matched.dissolve(by="zone_id").reset_index()
    zones["zone_name"] = zones["zone_id"].map(ZONE_NAMES)
    print(f"  {len(zones)} zones created")

    # ── Merge zone attributes from CSV ──
    csv_path = ROOT / "data" / "jabodetabek_zones.csv"
    attrs = pd.read_csv(csv_path)
    # Keep only cols we need from CSV (zone_id used as key)
    attr_cols = [
        "zone_id", "population", "avg_income_k", "poverty_pct",
        "distance_cbd_km", "character",
        "avail_car", "avail_moto", "avail_krl", "avail_tj",
        "avail_royal", "avail_mrt",
    ]
    attrs = attrs[attr_cols]
    zones = zones[["zone_id", "zone_name", "geometry"]].merge(attrs, on="zone_id")
    print(f"  Merged zone attributes")

    # ── Merge scenario ΔCS by zone ──
    policy_path = ROOT / "data" / "policy_results.json"
    with open(policy_path) as f:
        policy = json.load(f)

    for sc_key, sc_data in policy["scenarios"].items():
        col = f"dcs_{sc_key.lower()}"
        zones[col] = zones["zone_id"].map(sc_data["dCS_by_zone"]).fillna(0.0).round(4)

    # ── Simplify geometry slightly for web performance ──
    zones["geometry"] = zones["geometry"].simplify(tolerance=0.002, preserve_topology=True)

    # ── Write output ──
    out_path = ROOT / "app" / "public" / "data" / "zones.geojson"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    zones.to_file(out_path, driver="GeoJSON")
    print(f"  Wrote {out_path} ({out_path.stat().st_size / 1024:.1f} KB)")

    # ── Copy policy_results.json ──
    import shutil
    dest = ROOT / "app" / "public" / "data" / "policy_results.json"
    shutil.copy2(policy_path, dest)
    print(f"  Copied policy_results.json")

    # ── Copy best_model.json ──
    model_path = ROOT / "data" / "best_model.json"
    model_dest = ROOT / "app" / "public" / "data" / "best_model.json"
    shutil.copy2(model_path, model_dest)
    print(f"  Copied best_model.json")

    print("Done!")


if __name__ == "__main__":
    main()
