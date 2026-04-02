# EDA Report — MVP-100
**Date**: 2026-03-29
**Data**: kelurahan_scores.geojson (N=1,502), h3_scores.geojson (N=9,083)
**Pipeline run**: E6/MVP-98 (--skip-r5py flag active)

---

## 1. TAI Score Distribution

### Kelurahan (N=1,502)
| Stat | Value |
|---|---|
| Mean | 0.3972 |
| Median | 0.3608 |
| Std | 0.0774 |
| Min | 0.3450 |
| Max | 0.6295 |
| Q25 | 0.3495 |
| Q75 | 0.3854 |

**Note**: The narrow interquartile range (IQR = 0.036) and tight min (0.345) indicate that TAI scores are compressed in the lower register. This is explained below under L3 null impact — three of five layer components (L3, L4, L5) are hardcoded to 0.5 neutral, leaving real variance driven almost entirely by L1 and L2. The max of 0.630 represents the ceiling achievable with only two informative layers.

### H3 Res-8 (N=9,083)
| Stat | Value |
|---|---|
| Mean | 0.3321 |
| Median | 0.2957 |
| Std | 0.0904 |
| Min | 0.2700 |
| Max | 0.7300 |
| Q25 | 0.2761 |
| Q75 | 0.3414 |

H3 TAI has a wider range (0.460 span vs 0.285 at kelurahan) because hexagonal aggregation introduces more spatial granularity. The H3 maximum of 0.730 suggests some hexagons in high-service corridors capture stronger combined L1+L2 signal than any kelurahan polygon can.

---

## 2. TNI Score Distribution

### Kelurahan (N=1,502)
| Stat | Value |
|---|---|
| Mean | 0.4835 |
| Median | 0.4866 |
| Std | 0.0934 |
| Min | 0.2102 |
| Max | 0.7502 |
| Q25 | 0.4214 |
| Q75 | 0.5455 |

### H3 Res-8 (N=9,083)
| Stat | Value |
|---|---|
| Mean | 0.4454 |
| Median | 0.4466 |
| Std | 0.0874 |
| Min | 0.1947 |
| Max | 0.7192 |
| Q25 | 0.3870 |
| Q75 | 0.5033 |

TNI distributions are broader and more symmetric than TAI, indicating that transit need (driven by socioeconomic variables: poverty rate, zero-vehicle households, dependency ratio) varies more smoothly across the Jabodetabek region. H3 TNI is slightly lower on average (0.445 vs 0.484), consistent with hexagonal cells averaging across heterogeneous sub-kelurahan populations.

---

## 3. Quadrant Breakdown

| Quadrant | Kelurahan (N, %) | H3 (N, %) | Interpretation |
|---|---|---|---|
| Q1 (High TAI, Low TNI) | 338 (22.5%) | 2,001 (22.0%) | Well-served, low need — predominantly inner DKI Jakarta |
| Q2 (High TAI, High TNI) | 413 (27.5%) | 2,541 (28.0%) | Over-served relative to need — unexpected transit surplus zones |
| Q3 (Low TAI, Low TNI) | 338 (22.5%) | 2,000 (22.0%) | Low-need, low-service — rural/peri-urban fringe with low demand |
| Q4 (Low TAI, High TNI) | 413 (27.5%) | 2,541 (28.0%) | **Transit deserts — priority intervention zones** |

The near-perfect split between Q2 and Q4 (both 413/27.5% at kelurahan; both 2,541/28.0% at H3) is arithmetically expected from the median-split quadrant construction: when TAI and TNI medians bisect the distribution, Q2 and Q4 will always balance Q1 and Q3 by construction. This is not a finding but a methodological property to note in the paper.

Total Q4 kelurahan: 413 (27.5%); Q4 H3 hexagons: 2,541 (28.0%).

---

## 4. Spatial Distribution

Q4 kelurahan by administrative region (`kota_kab_name`):

| Region | Q4 Count | Q4 % of region's kelurahan |
|---|---|---|
| Bogor (Kabupaten) | 193 | ~largest peripheral district |
| Tangerang (Kabupaten) | 123 | |
| Bekasi (Kabupaten) | 68 | |
| KotaBogor | 8 | |
| KotaBekasi | 7 | |
| KotaTangerang | 5 | |
| KepulauanSeribu | 5 | |
| Depok | 3 | |
| TangerangSelatan | 1 | |
| **DKI Jakarta (all 5 kotas)** | **0** | **0.0%** |

DKI Jakarta (JakartaBarat, JakartaPusat, JakartaSelatan, JakartaTimur, JakartaUtara) contributes **zero** Q4 kelurahan. KepulauanSeribu (the island chain, formally DKI) contributes 5 Q4 units.

**H1 quantified:**
- Q4 in DKI Jakarta (5 main kotas): 0 / 268 = **0.0%**
- Q4 in Bodetabek: 408 / 1,234 = **33.1%**
- Q4 units as share of all Q4: DKI = 1.2% (5 Kepulauan Seribu), Bodetabek = 98.8%

---

## 5. Hypothesis Previews

### H1: Spatial periphery claim
*"Q4 transit deserts are concentrated in peripheral Bodetabek areas, not central DKI Jakarta"*

- Q4 in DKI Jakarta (5 main kotas): 0.0% of those kelurahan
- Q4 in Bodetabek: 33.1% of those kelurahan
- Bodetabek share of all Q4: **98.8%** (408/413)
- Top Q4 districts: Kabupaten Bogor (193), Kabupaten Tangerang (123), Kabupaten Bekasi (68)

**Signal: STRONGLY SUPPORTS**

The concentration is near-total. DKI Jakarta's formal 5-kota territory contains no Q4 kelurahan. The pattern aligns with expected infrastructure gradient: Commuter Line and BRT coverage concentrate in the inner ring, leaving outer Bodetabek kabupaten unserved.

**Caveat**: Kepulauan Seribu (5 Q4 units) is technically DKI Jakarta but geographically peripheral — it is appropriate to report this as a special case rather than evidence against H1.

---

### H2: MAUP / resolution sensitivity
*"Kelurahan Gini > H3 Gini (MAUP effect — coarser resolution underestimates inequality)"*

- Gini TAI kelurahan: **-0.0896** (absolute: 0.0896)
- Gini TAI H3: **-0.1228** (absolute: 0.1228)
- H3 |Gini| > kelurahan |Gini|: **YES** (0.1228 > 0.0896)
- Delta: -0.0332 (H3 shows 37% more inequality than kelurahan)
- Cohen's kappa: **0.609** (strong agreement, κ ≥ 0.6)
- Percent reclassified across resolutions: **29.3%**

**CRITICAL FLAG — Gini sign is negative at both resolutions.**

The `equity_summary.json` `h2_hypothesis_signal.gini_h3_gt_kelurahan` is reported as `false` because the pipeline compares raw signed values (-0.1228 < -0.0896). However, Gini coefficients are defined on [0,1] and should be non-negative. Negative values indicate a pipeline calculation error — likely the Gini formula was applied to centered/normalized TAI scores rather than raw [0,1] values, or the sign of the inequality direction was inverted.

**Signal: SUPPORTS the directional claim (H3 shows greater inequality magnitude), but the negative Gini values are a pipeline bug that must be corrected before MVP-14 (Results writing).**

Substantive interpretation:
- H3 res-8 captures finer-grained intra-kelurahan heterogeneity, producing a larger |Gini|
- 29.3% reclassification rate confirms the MAUP effect is real and substantial
- Cohen's κ = 0.609 (strong) indicates the two resolutions are not measuring entirely different things — they agree on ~71% of quadrant assignments
- The confusion matrix shows the sharpest disagreement is Q1 kelurahan being split into Q4 H3 cells (524 cells) and Q4 kelurahan split into Q1 H3 cells (320 cells), confirming sub-kelurahan heterogeneity

---

### H3: Equity gap magnitude
*"Equity gap: Q4 TAI meaningfully lower than Q1/Q2 TAI"*

**Kelurahan resolution:**
- Mean TAI Q4: **0.3500**
- Mean TAI Q1: **0.4365**
- Mean TAI Q2: **0.4500**
- Mean TAI Q3: **0.3512** (comparable to Q4 — see note below)
- Delta Q4 vs avg(Q1,Q2): **-0.0932**

**H3 resolution:**
- Mean TAI Q4: **0.2781**
- Mean TAI Q1: **0.3702**
- Mean TAI Q2: **0.3978**
- Delta Q4 vs avg(Q1,Q2): **-0.1059**

**Signal: SUPPORTS**

The equity gap is consistent across both resolutions. Q4 TAI is ~0.093–0.106 lower than the average of Q1+Q2. Given the full TAI range (0.345–0.630 at kelurahan), a gap of 0.093 represents approximately 33% of the working range — substantial.

**Note on Q3**: Q3 mean TAI (0.351) is nearly identical to Q4 (0.350). This is expected: both Q3 and Q4 have low TAI by definition. The equity gap distinguishes Q4 not by lower TAI per se, but by the combination of low TAI AND high TNI — Q3 has low need so its low TAI does not constitute a transit desert condition.

**Note on equity_gap score**: The `equity_gap` column (TNI - TAI) shows Q4 mean = 0.211, Q2 mean = -0.049, Q1 mean = 0.118. Q4 has the highest gap score (greatest TNI surplus over TAI), confirming the quadrant logic is internally consistent.

---

## 6. L3 Null Impact (--skip-r5py)

The pipeline was run with `--skip-r5py`, meaning L3 (CBD journey time via transit) was not computed from the R5py routing engine.

**What actually happened (from layer component data):**
- `tai_l3_cbd_journey`: null=0, mean=0.500, std=0.000, min=0.500, max=0.500
- `tai_l4_last_mile`: mean=0.500, std=0.000 (also flat)
- `tai_l5_cost_competitiveness`: mean=0.500, std=0.000 (also flat)
- Only `tai_l1_first_mile` (mean=0.213) and `tai_l2_service_quality` (mean=0.197) carry real variance

**L3 was not nulled out — it was filled with the neutral midpoint value 0.5.** The same fill was applied to L4 (last mile) and L5 (cost competitiveness). This means three of five layers (combined design weight: L3=0.35 + L4=0.15 + L5=0.15 = 0.65 of the total TAI weight) contribute no discriminatory power to the TAI composite.

**Impact on the composite:**
The TAI score is effectively: TAI ≈ (0.2 × L1) + (0.15 × L2) + (0.65 × 0.5 constant). This compresses all TAI scores toward 0.325 (the neutral contribution floor), explaining the narrow IQR and the minimum of 0.345. The rank ordering of kelurahan is driven entirely by L1 (first-mile access: road network quality, proximity to transit stops) and L2 (service quality: headway, route diversity).

**Implications for the Results section:**
1. H1 finding (Q4 concentration in Bodetabek) is robust because it reflects L1/L2 deficits — exactly the access and service quality dimensions most meaningful for first-mile equity
2. H2/H3 magnitudes are attenuated: the "real" Gini and equity gap, once L3 is computed via R5py, will be larger (L3 journey time is expected to be very poor in Bodetabek — adding genuine variance will widen the distribution)
3. The MVP-14 Results section must clearly caveat: "TAI composite reflects L1+L2 only; L3/L4/L5 set to neutral 0.5 pending R5py routing computation (MVP-XX)"
4. The pipeline has a broader issue: L4 and L5 are also flat at 0.5. This suggests the --skip-r5py flag may be triggering a broader neutral-fill beyond just L3. This should be investigated before the full pipeline run.

---

## 7. Key Findings for Results Section

1. **Bodetabek spatial concentration is unambiguous**: 98.8% of Q4 transit deserts fall in Bodetabek (primarily Kabupaten Bogor, Kabupaten Tangerang, Kabupaten Bekasi). DKI Jakarta's five main kotas contain zero Q4 kelurahan — the clearest possible H1 confirmation.

2. **Resolution mismatch is real and quantified**: 29.3% of H3 hexagons are classified differently from their parent kelurahan, with Cohen's κ = 0.609. This demonstrates the MAUP effect directly: coarser kelurahan polygons mask intra-unit heterogeneity, but the two resolutions substantially agree (71%) on the spatial pattern of transit access.

3. **Equity gap is consistent and spatially concentrated**: Q4 TAI is 0.093 below the Q1/Q2 mean at kelurahan resolution and 0.106 lower at H3 resolution — a gap representing ~33% of the active TAI range. The equity gap score (TNI − TAI) for Q4 kelurahan averages 0.211, compared to −0.049 for Q2 (over-served areas), quantifying the directional disparity.

---

## 8. Blockers / Concerns for MVP-14 (Results writing)

1. **CRITICAL — Negative Gini coefficients**: All Gini values in `equity_summary.json` are negative (kelurahan TAI: −0.0896, H3 TAI: −0.1228). Gini must be in [0,1]. This is a pipeline bug — the sign is inverted or the calculation was applied to signed deviations. The H2 hypothesis signal field `gini_h3_gt_kelurahan: false` is therefore incorrect (the absolute values do support H2). **Must be fixed in the pipeline before Results section cites these numbers.**

2. **CRITICAL — Global Moran's I all null**: All `global_morans_i_tai` and `global_morans_i_equity_gap` fields are null at both resolutions. This means spatial autocorrelation was not computed (likely a missing spatial weights matrix or a dependency like `libpysal`/`esda` failing silently). LISA clustering is also entirely "NS" (not significant) for all 10,585 features. Without Moran's I, the spatial clustering claims in the paper have no statistical backing. **Must be resolved before MVP-14.**

3. **MODERATE — Three layers flat at 0.5**: L3, L4, and L5 are all filled with neutral 0.5, not just L3. The `--skip-r5py` flag appears to trigger a broader neutral-fill. If L4 (last mile) and L5 (cost competitiveness) were expected to have real data from non-R5py sources, this is a data wrangling gap that should be investigated independently of the R5py routing question.

4. **MODERATE — Transit competitive ratio columns all empty**: `gc_transit_idr`, `tcr_vs_car`, `tcr_vs_motorcycle`, `tcr_combined` and `avg_traffic_speed_kmh`, `peak_congestion_index`, `traffic_adjusted_access` are all empty (0 unique values) in kelurahan_scores.geojson. These appear to be unpopulated L5/traffic fields. If these feed L5, it explains why L5 is flat — the upstream data was never written.

5. **LOW — H3 has no admin region column**: The H3 GeoJSON does not carry a `kota_kab_name` or any administrative identifier. H1 spatial claims must be derived from kelurahan data (which does have `kota_kab_name`). The H3 layer cannot independently corroborate which regions have Q4 hexagons without a spatial join back to admin boundaries.

6. **LOW — Q2 and Q4 counts are identical by construction**: The median-split quadrant method produces mirror counts (Q1=Q3, Q2=Q4 at both resolutions). The paper should note this is a known property of median-bisection quadrant assignment, not an empirical coincidence.
