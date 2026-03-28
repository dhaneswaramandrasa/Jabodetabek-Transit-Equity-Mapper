"""
MVP-25 — Compute equity gap, Gini, LISA at both resolutions.

Reads kelurahan_scores.geojson + h3_scores.geojson and produces:
  data/processed/analysis/equity_summary.json      — Gini, global Moran's I, Q counts
  data/processed/analysis/lorenz_kelurahan.csv     — Lorenz curve data (kelurahan)
  data/processed/analysis/lorenz_h3.csv            — Lorenz curve data (H3)
  data/processed/analysis/lisa_kelurahan.geojson   — LISA cluster classification
  data/processed/analysis/lisa_h3.geojson          — LISA cluster classification
  data/processed/analysis/resolution_comparison.json — confusion matrix + Cohen's kappa
  data/processed/analysis/sensitivity_weights.json — TAI weight ±20% Gini impact
  data/processed/analysis/sensitivity_resolution.json — res-7 / res-9 placeholder

Usage:
    python -m src.processing.equity_analysis
    python -m src.processing.equity_analysis --skip-sensitivity
"""

import argparse
import json
import logging
import sys
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

# ── Paths ──────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "processed"

KELURAHAN_SCORES = DATA / "scores" / "kelurahan_scores.geojson"
H3_SCORES        = DATA / "scores" / "h3_scores.geojson"
OUT_DIR          = DATA / "analysis"

# TAI layer weights (methodology.md)
TAI_WEIGHTS = {
    "l1_first_mile":           0.20,
    "l2_service_quality":      0.15,
    "l3_cbd_journey":          0.35,
    "l4_last_mile":            0.15,
    "l5_cost_competitiveness": 0.15,
}
SENSITIVITY_DELTA = 0.20  # ±20% weight perturbation


# ── Gini + Lorenz ──────────────────────────────────────────────────────────────

def gini(series: pd.Series) -> float:
    """Gini coefficient (0 = perfectly equal, 1 = maximally unequal)."""
    s = series.dropna().sort_values().values
    n = len(s)
    if n == 0 or s.sum() == 0:
        return float("nan")
    cumsum = np.cumsum(s)
    return float((2 * np.sum(cumsum) / cumsum[-1] / n) - (n + 1) / n)


def lorenz_curve(series: pd.Series) -> pd.DataFrame:
    """
    Compute Lorenz curve data.

    Returns DataFrame with columns:
      population_share  — cumulative share of units (0–1)
      access_share      — cumulative share of TAI (0–1)
    """
    s = series.dropna().sort_values().values
    n = len(s)
    total = s.sum()
    if total == 0:
        return pd.DataFrame({"population_share": [0, 1], "access_share": [0, 1]})
    pop_share = np.arange(1, n + 1) / n
    access_share = np.cumsum(s) / total
    # Prepend origin
    pop_share = np.concatenate([[0], pop_share])
    access_share = np.concatenate([[0], access_share])
    return pd.DataFrame({"population_share": pop_share, "access_share": access_share})


# ── Spatial weights + Moran's I ────────────────────────────────────────────────

def _build_weights(gdf: gpd.GeoDataFrame, id_col: str):
    """Build Queen contiguity weights via libpysal."""
    try:
        from libpysal.weights import Queen
        w = Queen.from_dataframe(gdf, idVariable=id_col, silence_warnings=True)
        w.transform = "r"   # row-standardise
        return w
    except ImportError:
        logger.warning("libpysal not installed — skipping spatial weights. pip install libpysal")
        return None


def global_morans_i(series: pd.Series, weights) -> dict:
    """Compute global Moran's I."""
    if weights is None:
        return {"moran_i": None, "p_value": None, "z_score": None}
    try:
        from esda.moran import Moran
        mi = Moran(series.values, weights)
        return {
            "moran_i": round(float(mi.I), 4),
            "p_value": round(float(mi.p_sim), 4),
            "z_score": round(float(mi.z_norm), 4),
        }
    except ImportError:
        logger.warning("esda not installed — skipping Moran's I. pip install esda")
        return {"moran_i": None, "p_value": None, "z_score": None}


def local_lisa(gdf: gpd.GeoDataFrame, series: pd.Series, weights, id_col: str) -> gpd.GeoDataFrame:
    """
    Compute local Moran's I (LISA) and classify clusters:
      HH — High-High (significant transit desert surroundings)
      LL — Low-Low
      HL — High-Low (spatial outlier)
      LH — Low-High (spatial outlier)
      NS — Not significant (p >= 0.05)
    """
    out = gdf[[id_col, "geometry", "quadrant", "tai_score", "tni_score"]].copy()
    out["lisa_cluster"] = "NS"
    out["lisa_p_value"] = np.nan
    out["lisa_i"] = np.nan

    if weights is None:
        return out

    try:
        from esda.moran import Moran_Local
        lm = Moran_Local(series.values, weights, transformation="r", permutations=999)
        sig = lm.p_sim < 0.05
        q = lm.q  # 1=HH, 2=LH, 3=LL, 4=HL
        cluster_map = {1: "HH", 2: "LH", 3: "LL", 4: "HL"}
        labels = np.where(sig, np.vectorize(cluster_map.get)(q), "NS")
        out["lisa_cluster"] = labels
        out["lisa_p_value"] = np.round(lm.p_sim, 4)
        out["lisa_i"] = np.round(lm.Is, 4)
    except ImportError:
        logger.warning("esda not installed — LISA clusters will be NS. pip install esda")

    return out


# ── Resolution comparison ──────────────────────────────────────────────────────

def resolution_comparison(
    kel_gdf: gpd.GeoDataFrame,
    h3_gdf: gpd.GeoDataFrame,
) -> dict:
    """
    Quantify MAUP effect: how many H3 cells disagree with the kelurahan
    quadrant they overlap?

    Returns:
      confusion_matrix   — 4×4 counts (kelurahan quadrant vs H3 quadrant)
      cohen_kappa        — agreement statistic
      pct_reclassified   — % H3 cells whose quadrant differs from parent kelurahan
      q4_count_kelurahan — number of Q4 (transit desert) kelurahan
      q4_count_h3        — number of Q4 H3 cells
    """
    # Spatial join H3 centroids → kelurahan
    h3_proj = h3_gdf.to_crs("EPSG:32748").copy()
    h3_proj["geometry"] = h3_proj.geometry.centroid
    kel_proj = kel_gdf[["kelurahan_id", "quadrant", "geometry"]].to_crs("EPSG:32748")

    joined = gpd.sjoin(
        h3_proj[["h3_index", "quadrant", "geometry"]],
        kel_proj,
        how="left",
        predicate="within",
        rsuffix="kel",
    )
    joined = joined.dropna(subset=["quadrant_kel"])
    # geopandas uses _left/_right suffixes when both frames share a column name
    h3_q_col = "quadrant_left" if "quadrant_left" in joined.columns else "quadrant"
    joined = joined.rename(columns={h3_q_col: "quadrant_h3"})

    # Confusion matrix
    labels = ["Q1", "Q2", "Q3", "Q4"]
    cm = pd.crosstab(
        joined["quadrant_kel"],
        joined["quadrant_h3"],
        rownames=["kelurahan"],
        colnames=["h3"],
    ).reindex(index=labels, columns=labels, fill_value=0)

    # Cohen's kappa
    try:
        from sklearn.metrics import cohen_kappa_score
        kappa = float(cohen_kappa_score(joined["quadrant_kel"], joined["quadrant_h3"]))
    except ImportError:
        # Manual kappa calculation
        n = len(joined)
        po = (joined["quadrant_kel"] == joined["quadrant_h3"]).sum() / n
        pe = sum(
            (joined["quadrant_kel"] == q).sum() / n * (joined["quadrant_h3"] == q).sum() / n
            for q in labels
        )
        kappa = float((po - pe) / (1 - pe)) if pe < 1 else 0.0

    pct_reclassified = float(
        (joined["quadrant_kel"] != joined["quadrant_h3"]).sum() / len(joined) * 100
    )

    return {
        "confusion_matrix": cm.to_dict(),
        "cohen_kappa": round(kappa, 4),
        "pct_reclassified": round(pct_reclassified, 2),
        "q4_count_kelurahan": int((kel_gdf["quadrant"] == "Q4").sum()),
        "q4_count_h3": int((h3_gdf["quadrant"] == "Q4").sum()),
        "total_kelurahan": len(kel_gdf),
        "total_h3": len(h3_gdf),
    }


# ── Sensitivity analysis: TAI weights ±20% ────────────────────────────────────

def sensitivity_weights(
    kel_gdf: gpd.GeoDataFrame,
    h3_gdf: gpd.GeoDataFrame,
) -> dict:
    """
    Perturb each TAI layer weight by ±20% (renormalise remaining weights),
    recompute TAI, and report the resulting Gini at both resolutions.

    Returns dict: {layer_name: {"+20%": gini_kel, "-20%": gini_kel, ...}}
    """
    layer_cols = list(TAI_WEIGHTS.keys())
    results = {}

    for perturb_layer in layer_cols:
        results[perturb_layer] = {}
        for sign, delta in [("+20%", SENSITIVITY_DELTA), ("-20%", -SENSITIVITY_DELTA)]:
            # Perturbed weights
            new_w = TAI_WEIGHTS.copy()
            new_w[perturb_layer] = max(0.0, new_w[perturb_layer] + delta)
            total = sum(new_w.values())
            new_w = {k: v / total for k, v in new_w.items()}  # renormalise

            # Recompute TAI for both GDFs
            # kelurahan columns have a 'tai_' prefix; H3 columns do not
            def _resolve_col(gdf, key):
                if key in gdf.columns:
                    return key
                if f"tai_{key}" in gdf.columns:
                    return f"tai_{key}"
                return None

            def _recompute_tai(gdf, weights):
                terms = []
                for col, w in weights.items():
                    resolved = _resolve_col(gdf, col)
                    if resolved is not None:
                        terms.append(gdf[resolved] * w)
                return sum(terms) if terms else gdf["tai_score"]

            gini_kel = gini(_recompute_tai(kel_gdf, new_w))
            gini_h3  = gini(_recompute_tai(h3_gdf,  new_w))
            results[perturb_layer][sign] = {
                "gini_kelurahan": round(gini_kel, 4),
                "gini_h3": round(gini_h3, 4),
                "weights_used": {k: round(v, 4) for k, v in new_w.items()},
            }

    # Baseline
    results["_baseline"] = {
        "gini_kelurahan": round(gini(kel_gdf["tai_score"]), 4),
        "gini_h3": round(gini(h3_gdf["tai_score"]), 4),
        "weights_used": TAI_WEIGHTS,
    }
    return results


# ── Sensitivity: H3 resolution (placeholder) ──────────────────────────────────

def sensitivity_resolution_placeholder() -> dict:
    """
    Placeholder for res-7 / res-9 sensitivity (full r5py rerun required).
    Returns structure; populated values require separate compute runs.
    """
    return {
        "note": (
            "Full res-7 and res-9 sensitivity requires separate r5py compute runs "
            "(res-9 ~60k origins, 24-48h budget). Placeholder values — run "
            "compute_h3.py with H3_RESOLUTION=7 or 9 and populate from output."
        ),
        "res_7": {
            "expected_cells": "~3,000-5,000",
            "gini_tai": None,
            "q4_count": None,
            "cohen_kappa_vs_res8": None,
        },
        "res_8": {
            "expected_cells": "~15,000-20,000",
            "gini_tai": None,   # populated at runtime
            "q4_count": None,
            "is_primary": True,
        },
        "res_9": {
            "expected_cells": "~50,000-70,000",
            "gini_tai": None,
            "q4_count": None,
            "cohen_kappa_vs_res8": None,
            "note": "Stratified sampling fallback recommended for r5py at res-9",
        },
    }


# ── Main ───────────────────────────────────────────────────────────────────────

def run(skip_sensitivity: bool = False) -> None:
    logger.info("=== MVP-25: Equity gap, Gini, LISA at both resolutions ===")
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Load scores
    logger.info("Loading kelurahan scores...")
    if not KELURAHAN_SCORES.exists():
        logger.error(f"Missing: {KELURAHAN_SCORES} — run compute_tai_tni.py first")
        sys.exit(1)
    kel_gdf = gpd.read_file(KELURAHAN_SCORES)

    logger.info("Loading H3 scores...")
    if not H3_SCORES.exists():
        logger.error(f"Missing: {H3_SCORES} — run compute_h3.py first")
        sys.exit(1)
    h3_gdf = gpd.read_file(H3_SCORES)

    id_col_kel = "kelurahan_id"
    id_col_h3  = "h3_index"

    # ── 1. Gini coefficients ────────────────────────────────────────────────
    logger.info("Computing Gini coefficients...")
    gini_tai_kel  = gini(kel_gdf["tai_score"])
    gini_tai_h3   = gini(h3_gdf["tai_score"])
    gini_tni_kel  = gini(kel_gdf["tni_score"])
    gini_tni_h3   = gini(h3_gdf["tni_score"])
    gini_gap_kel  = gini(kel_gdf["equity_gap"].abs())
    gini_gap_h3   = gini(h3_gdf["equity_gap"].abs())

    logger.info(f"Gini TAI — kelurahan: {gini_tai_kel:.4f}, H3: {gini_tai_h3:.4f}")
    logger.info(f"Gini TNI — kelurahan: {gini_tni_kel:.4f}, H3: {gini_tni_h3:.4f}")

    # ── 2. Lorenz curves ────────────────────────────────────────────────────
    logger.info("Computing Lorenz curves...")
    lorenz_kel = lorenz_curve(kel_gdf["tai_score"])
    lorenz_h3  = lorenz_curve(h3_gdf["tai_score"])
    lorenz_kel.to_csv(OUT_DIR / "lorenz_kelurahan.csv", index=False)
    lorenz_h3.to_csv(OUT_DIR / "lorenz_h3.csv", index=False)
    logger.info("Lorenz CSVs saved")

    # ── 3. Spatial weights ──────────────────────────────────────────────────
    logger.info("Building spatial weights (kelurahan)...")
    w_kel = _build_weights(kel_gdf, id_col_kel)
    logger.info("Building spatial weights (H3)...")
    w_h3 = _build_weights(h3_gdf, id_col_h3)

    # ── 4. Global Moran's I ─────────────────────────────────────────────────
    logger.info("Computing global Moran's I...")
    mi_kel = global_morans_i(kel_gdf["tai_score"], w_kel)
    mi_h3  = global_morans_i(h3_gdf["tai_score"], w_h3)
    mi_equity_kel = global_morans_i(kel_gdf["equity_gap"], w_kel)
    mi_equity_h3  = global_morans_i(h3_gdf["equity_gap"], w_h3)
    logger.info(f"Global Moran's I (TAI) — kelurahan: {mi_kel['moran_i']}, H3: {mi_h3['moran_i']}")

    # ── 5. LISA clusters ────────────────────────────────────────────────────
    logger.info("Computing LISA clusters (kelurahan equity_gap)...")
    lisa_kel = local_lisa(kel_gdf, kel_gdf["equity_gap"], w_kel, id_col_kel)
    lisa_kel.to_file(OUT_DIR / "lisa_kelurahan.geojson", driver="GeoJSON")

    logger.info("Computing LISA clusters (H3 equity_gap)...")
    lisa_h3 = local_lisa(h3_gdf, h3_gdf["equity_gap"], w_h3, id_col_h3)
    lisa_h3.to_file(OUT_DIR / "lisa_h3.geojson", driver="GeoJSON")
    logger.info("LISA GeoJSONs saved")

    # ── 6. Resolution comparison ────────────────────────────────────────────
    logger.info("Computing resolution comparison (confusion matrix + Cohen's kappa)...")
    res_comp = resolution_comparison(kel_gdf, h3_gdf)
    with open(OUT_DIR / "resolution_comparison.json", "w") as f:
        json.dump(res_comp, f, indent=2)
    logger.info(
        f"Cohen's kappa: {res_comp['cohen_kappa']}, "
        f"% reclassified: {res_comp['pct_reclassified']}%"
    )

    # ── 7. Sensitivity analysis ─────────────────────────────────────────────
    sens_weights = {}
    sens_resolution = sensitivity_resolution_placeholder()

    if not skip_sensitivity:
        logger.info("Running sensitivity analysis: TAI weights ±20%...")
        sens_weights = sensitivity_weights(kel_gdf, h3_gdf)
        # Populate res_8 actual values
        sens_resolution["res_8"]["gini_tai"] = gini_tai_h3
        sens_resolution["res_8"]["q4_count"] = int((h3_gdf["quadrant"] == "Q4").sum())

    with open(OUT_DIR / "sensitivity_weights.json", "w") as f:
        json.dump(sens_weights, f, indent=2)
    with open(OUT_DIR / "sensitivity_resolution.json", "w") as f:
        json.dump(sens_resolution, f, indent=2)

    # ── 8. Master summary ───────────────────────────────────────────────────
    q_kel = kel_gdf["quadrant"].value_counts().to_dict()
    q_h3  = h3_gdf["quadrant"].value_counts().to_dict()

    lisa_kel_counts = lisa_kel["lisa_cluster"].value_counts().to_dict()
    lisa_h3_counts  = lisa_h3["lisa_cluster"].value_counts().to_dict()

    summary = {
        "resolution_primary": "H3 res-8",
        "kelurahan": {
            "n": len(kel_gdf),
            "gini_tai": round(gini_tai_kel, 4),
            "gini_tni": round(gini_tni_kel, 4),
            "gini_equity_gap": round(gini_gap_kel, 4),
            "global_morans_i_tai": mi_kel,
            "global_morans_i_equity_gap": mi_equity_kel,
            "quadrant_counts": q_kel,
            "q4_pct": round(q_kel.get("Q4", 0) / len(kel_gdf) * 100, 2),
            "lisa_cluster_counts": lisa_kel_counts,
        },
        "h3": {
            "n": len(h3_gdf),
            "gini_tai": round(gini_tai_h3, 4),
            "gini_tni": round(gini_tni_h3, 4),
            "gini_equity_gap": round(gini_gap_h3, 4),
            "global_morans_i_tai": mi_h3,
            "global_morans_i_equity_gap": mi_equity_h3,
            "quadrant_counts": q_h3,
            "q4_pct": round(q_h3.get("Q4", 0) / len(h3_gdf) * 100, 2),
            "lisa_cluster_counts": lisa_h3_counts,
        },
        "resolution_comparison": res_comp,
        "h2_hypothesis_signal": {
            "gini_h3_gt_kelurahan": gini_tai_h3 > gini_tai_kel,
            "gini_delta": round(gini_tai_h3 - gini_tai_kel, 4),
            "kappa_interpretation": (
                "strong" if res_comp["cohen_kappa"] > 0.6
                else "moderate" if res_comp["cohen_kappa"] > 0.4
                else "weak"
            ),
        },
    }

    with open(OUT_DIR / "equity_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    logger.info("=== MVP-25 complete ===")
    logger.info(f"Gini TAI kelurahan: {gini_tai_kel:.4f} | H3: {gini_tai_h3:.4f}")
    logger.info(f"Q4 transit deserts — kelurahan: {q_kel.get('Q4', 0)}, H3: {q_h3.get('Q4', 0)}")
    logger.info(f"H2 signal: Gini_H3 {'>' if gini_tai_h3 > gini_tai_kel else '<='} Gini_kelurahan (delta={gini_tai_h3 - gini_tai_kel:+.4f})")
    logger.info(f"Cohen's kappa: {res_comp['cohen_kappa']} ({summary['h2_hypothesis_signal']['kappa_interpretation']} agreement)")
    logger.info(f"Outputs → {OUT_DIR}/")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MVP-25: Equity gap + Gini + LISA")
    parser.add_argument(
        "--skip-sensitivity",
        action="store_true",
        help="Skip weight sensitivity analysis (faster run)",
    )
    args = parser.parse_args()
    run(skip_sensitivity=args.skip_sensitivity)
