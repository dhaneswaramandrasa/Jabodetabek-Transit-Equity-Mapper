# Pipeline QA Report — MVP-99
**Date**: 2026-03-29
**Branch**: e6/mvp-98-run-pipeline
**QA against**: docs/DATA_MODEL.md (signed off 2026-03-21) + docs/methodology.md

---

## Summary
**WARN overall** — pipeline is structurally sound (correct rows, no nulls in key fields, equity_gap formula exact, all 8 analysis files present), but three issues must be resolved before MVP-27 or MVP-14:

1. **GINI SIGN BUG** (HIGH) — `gini()` function returns negatives; all reported Gini values are sign-flipped.
2. **TAI LAYERS 3/4/5 FLAT AT 0.5** (HIGH) — L3 (CBD journey, 35% weight), L4 (last mile, 15%), L5 (cost, 15%) are all constant 0.5 placeholders. 65% of TAI weight carries no real signal. This is expected for mock data but must be resolved before real-data migration.
3. **H3 COLUMN NAME MISMATCHES** (MEDIUM) — H3 file uses abbreviated column names (`n_stops`, `min_headway_min`, `mode_diversity`, `fare_tier`, `has_affordable`, `has_feeder_service`) instead of the DATA_MODEL.md schema names (`n_transit_stops`, `avg_headway_min`, etc.).

---

## Schema Compliance

### Kelurahan
- Expected fields: 50 | Present: 47 | Missing: 8 | Extra: 5

| Field | Status | Notes |
|---|---|---|
| `road_adjusted_access` | MISSING | Not computed — depends on OSM + transit data |
| `poi_reach_cbd_min` | MISSING | Replaced by `tai_l3_cbd_journey` (flat mock) |
| `poi_reach_hospital_min` | MISSING | r5py routing not run |
| `poi_reach_school_min` | MISSING | r5py routing not run |
| `poi_reach_market_min` | MISSING | r5py routing not run |
| `poi_reach_industrial_min` | MISSING | r5py routing not run |
| `poi_reach_govoffice_min` | MISSING | r5py routing not run |
| `est_cbd_journey_fare_idr` | MISSING | Post-hoc compute not yet run |
| `tai_l1_first_mile` | EXTRA | Layer sub-score stored; not in schema |
| `tai_l2_service_quality` | EXTRA | Layer sub-score stored; not in schema |
| `tai_l3_cbd_journey` | EXTRA | Layer sub-score stored; not in schema |
| `tai_l4_last_mile` | EXTRA | Layer sub-score stored; not in schema |
| `tai_l5_cost_competitiveness` | EXTRA | Layer sub-score stored; not in schema |

### H3
- Expected fields: 49 | Present: 31 | Missing: 30 | Extra: 12

The H3 file uses abbreviated column names throughout. Key mismatches vs DATA_MODEL.md:

| DATA_MODEL.md name | Actual H3 name | Status |
|---|---|---|
| `n_transit_stops` | `n_stops` | RENAMED |
| `avg_headway_min` | `min_headway_min` | RENAMED (semantics differ) |
| `transit_mode_diversity` | `mode_diversity` | RENAMED |
| `best_mode_fare_tier` | `fare_tier` | RENAMED |
| `has_affordable_mode` | `has_affordable` | RENAMED |
| `poi_reach_cbd_min` | `poi_reach_cbd_weighted` | RENAMED + semantics differ |
| `l1_first_mile` through `l5_*` | `tai_l1_*` prefix in kelurahan | INCONSISTENT naming between resolutions |
| `pop_density` | MISSING | Not computed for H3 |
| `pct_primary_secondary` | MISSING | Not computed for H3 |
| `pct_residential_tertiary` | MISSING | Not computed for H3 |
| `avg_road_class_score` | MISSING | Not computed for H3 |
| `gc_transit_idr` | MISSING | Not computed for H3 |
| `tcr_vs_car` etc. | MISSING | Not computed for H3 |
| `transit_competitive_zone` | MISSING | Not computed for H3 |

---

## Data Quality

### Row Counts
| Dataset | Rows | Expected | Status |
|---|---|---|---|
| Kelurahan | 1,502 | ~1,800 | WARN — 298 fewer than mock data spec |
| H3 res-8 | 9,083 | 15,000–20,000 | WARN — well below expected range |

### Null Rates — Kelurahan
| Field | Null Count | Null % | Flag |
|---|---|---|---|
| `n_transit_routes` | 1,200 | 79.9% | OK — null only where `n_transit_stops = 0` |
| `gc_transit_idr` | 1,502 | 100.0% | HIGH — Layer 5 generalized cost not computed |
| `tcr_vs_car` | 1,502 | 100.0% | HIGH — TCR not computed |
| `tcr_vs_motorcycle` | 1,502 | 100.0% | HIGH — TCR not computed |
| `tcr_combined` | 1,502 | 100.0% | HIGH — TCR not computed |
| `avg_traffic_speed_kmh` | 1,502 | 100.0% | OK — v2 extension, null by design |
| `peak_congestion_index` | 1,502 | 100.0% | OK — v2 extension, null by design |
| `traffic_adjusted_access` | 1,502 | 100.0% | OK — v2 extension, null by design |

### Null Rates — H3
No nulls in any field. PASS.

### Range Checks
| Field | Min | Max | Expected | Status |
|---|---|---|---|---|
| Kelurahan `tai_score` | 0.345 | 0.630 | [0, 1] | WARN — narrow range (L3/L4/L5 flat) |
| H3 `tai_score` | 0.270 | 0.730 | [0, 1] | WARN — narrow range (L3/L5 flat) |
| Kelurahan `tni_score` | 0.210 | 0.750 | [0, 1] | PASS |
| H3 `tni_score` | 0.195 | 0.719 | [0, 1] | PASS |
| Kelurahan `equity_gap` | -0.368 | 0.388 | [-1, 1] | PASS |
| H3 `equity_gap` | -0.446 | 0.448 | [-1, 1] | PASS |

### Equity Gap Formula Check
`equity_gap = tni_score - tai_score`

Kelurahan: max absolute deviation = 0.000000 — PASS
H3: max absolute deviation = 0.000000 — PASS

### Quadrant Distribution

| Quadrant | Kelurahan | H3 |
|---|---|---|
| Q1 (High Access, Low Need) | 338 (22.5%) | 2,001 (22.0%) |
| Q2 (High Access, High Need) | 413 (27.5%) | 2,541 (28.0%) |
| Q3 (Low Access, Low Need) | 338 (22.5%) | 2,000 (22.0%) |
| Q4 (Low Access, High Need — Transit Desert) | 413 (27.5%) | 2,541 (28.0%) |

Q1=Q3 and Q2=Q4 at kelurahan level is a strong signal of symmetric/mock data. In real data these should differ. Distribution is PASS for format validity, WARN for real-data quality.

---

## Gini Check

### Bug Confirmed: Sign Inversion

The `gini()` function in `src/processing/equity_analysis.py` (line 64) uses the cumulative-sum variant:

```python
return float((2 * np.sum(cumsum) / cumsum[-1] / n) - (n + 1) / n)
```

This formula sums cumulative values rather than rank-weighted values. The resulting sign is inverted relative to the standard Gini formula. Verification:

- Perfectly equal distribution (all 1s): buggy returns 0.0, correct returns 0.0 — coincidentally agrees
- Maximum inequality ([0, 0, ..., 1]): buggy returns **-0.99**, correct returns **+0.99** — sign flipped

All negative Gini values in `equity_summary.json` are incorrect. The standard formula is:

```python
(2 * sum(i * x_i for i in 1..n) / (n * sum(x))) - (n + 1) / n
```

### Reported vs Corrected Values

| Metric | Reported (buggy) | Corrected |
|---|---|---|
| Gini TAI kelurahan | -0.0896 | **+0.0896** |
| Gini TAI H3 | -0.1228 | **+0.1228** |
| Gini TNI kelurahan | -0.1091 | **+0.1091** |
| Gini TNI H3 | -0.1106 | **+0.1106** |
| Gini equity_gap kelurahan | -0.3471 | **+0.3471** |
| Gini equity_gap H3 | -0.3318 | **+0.3318** |

The magnitudes are correct; only signs are wrong. The bug is a pure sign flip.

### H2 Hypothesis Impact

The `h2_hypothesis_signal.gini_h3_gt_kelurahan` field in `equity_summary.json` currently reports **false** because `-0.1228 > -0.0896` is false. With correct values, `0.1228 > 0.0896` is **true** — H2 PASSES. The delta is +0.0332. Cohen's kappa = 0.6087 (strong agreement) is unaffected.

---

## Equity Analysis Files

| File | Present | Size | Status |
|---|---|---|---|
| `equity_summary.json` | YES | 1,800 bytes | WARN — Gini values sign-inverted |
| `lorenz_kelurahan.csv` | YES | 57,972 bytes | PASS |
| `lorenz_h3.csv` | YES | 350,728 bytes | PASS |
| `lisa_kelurahan.geojson` | YES | 979,248 bytes | WARN — all NS (libpysal not installed) |
| `lisa_h3.geojson` | YES | 5,346,789 bytes | WARN — all NS (libpysal not installed) |
| `resolution_comparison.json` | YES | 527 bytes | PASS |
| `sensitivity_weights.json` | YES | 3,288 bytes | WARN — uses buggy Gini values |
| `sensitivity_resolution.json` | YES | 698 bytes | PASS — placeholder by design |

All 8 expected files present.

### LISA Cluster Types
Column name in file: `lisa_cluster` (not `cluster_type` — minor naming deviation from task spec).
All 1,502 kelurahan and all 9,083 H3 cells classified as "NS" (not significant).
Root cause: `libpysal` and `esda` packages not installed in the Python environment. The `local_lisa()` function catches the ImportError and defaults to "NS". PASS for schema structure; WARN for missing spatial statistics.

### Moran's I
Global Moran's I is null for all four metrics (TAI kelurahan, TAI H3, equity_gap kelurahan, equity_gap H3). Same root cause: `libpysal` not installed.

### Cohen's Kappa
`cohen_kappa = 0.6087` — strong agreement (>0.60 threshold). Valid. 29.3% of H3 cells reclassified vs parent kelurahan quadrant — demonstrates meaningful MAUP effect.

---

## Issues Flagged

| # | Issue | Severity | Action Required |
|---|---|---|---|
| 1 | `gini()` returns negative values — sign inversion bug in formula | HIGH | Fix formula in `src/processing/equity_analysis.py` line 64; rerun equity_analysis.py to regenerate `equity_summary.json` and `sensitivity_weights.json` |
| 2 | L3 (CBD journey, 0.35 weight), L4 kelurahan (0.15), L5 (0.15) are flat at 0.5 — 65% of TAI weight is a constant placeholder | HIGH | Acceptable for mock-data phase. Must be resolved in MVP-27 real-data migration. Flag for MVP-14 (Results): do not interpret TAI distribution as meaningful until real layers computed |
| 3 | H3 column names do not match DATA_MODEL.md schema (`n_stops` vs `n_transit_stops`, `fare_tier` vs `best_mode_fare_tier`, etc.) | MEDIUM | Rename columns in `src/processing/compute_h3.py` output to match schema before MVP-27 migration and before populating `lib/mock-data.ts` |
| 4 | `libpysal` and `esda` not installed — all Moran's I and LISA results are null/NS | MEDIUM | `pip install libpysal esda` then rerun equity_analysis.py. LISA spatial clusters are required for H3 hypothesis and paper Results section |
| 5 | 8 DATA_MODEL.md TAI input fields missing from kelurahan file: `poi_reach_*` (6 fields), `road_adjusted_access`, `est_cbd_journey_fare_idr` | MEDIUM | These require r5py routing and post-hoc fare computation. Track as MVP-27 prerequisite; L3/L4 scores currently placeholders as a result |
| 6 | `gc_transit_idr`, `tcr_vs_*`, `tcr_combined` 100% null in kelurahan — L5 cost competitiveness not computed | MEDIUM | Required for full TAI and paper Layer 5 analysis; currently contributing constant 0.5 × 0.15 = 0.075 to all TAI scores |
| 7 | Kelurahan row count 1,502 vs expected ~1,800; H3 row count 9,083 vs expected 15,000–20,000 | LOW | Likely correct for the actual study area boundary; update DATA_MODEL.md mock data spec if confirmed |
| 8 | Q2 = Q4 counts at kelurahan level (413 each) and Q1 = Q3 (338 each) — symmetric distribution signals mock/synthetic data | LOW | Expected for current mock phase; confirm distribution is asymmetric after real data migration |

---

## Verdict for MVP-27 (migrate to real data) and MVP-14 (Results writing)

**NOT READY — with conditions**

### Before MVP-27 (real data migration)
- [ ] Fix `gini()` sign bug and regenerate equity_summary.json
- [ ] Install `libpysal` + `esda` and rerun equity_analysis.py to get real LISA/Moran's I
- [ ] Rename H3 columns to match DATA_MODEL.md schema
- [ ] Verify row counts against confirmed study area boundary

### Before MVP-14 (Results writing)
- [ ] All MVP-27 conditions above
- [ ] L3 (CBD journey via r5py), L4 (last mile), L5 (cost competitiveness) must be computed with real data — currently 65% of TAI is a constant
- [ ] `poi_reach_*` fields populated
- [ ] `gc_transit_idr` / `tcr_*` fields populated

### What IS ready now
- Structural schema correct for kelurahan
- Equity gap formula correct (tni - tai = equity_gap, no error)
- Quadrant classification logic correct
- Resolution comparison and Cohen's kappa valid
- All 8 analysis output files present
- Lorenz curve data valid
- H2 hypothesis will PASS once Gini sign bug is fixed (corrected Gini_H3=0.1228 > Gini_kelurahan=0.0896)
