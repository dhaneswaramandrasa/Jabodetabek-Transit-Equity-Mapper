# Transit Need Index (TNI): Indicator Set, Normalization, and Weighting

**Ticket**: MVP-5 (E0-003)
**Status**: Draft — awaiting review before merge into `docs/methodology.md`
**Date**: 2026-03-19

---

## 1. Indicator Confirmation

### 1.1 Evaluation Framework

The TNI measures latent demand for public transit — populations who *need* transit most due to socioeconomic or demographic constraints on private vehicle use. The indicator set must satisfy three criteria:

1. **Theoretical grounding**: Each indicator must have a defensible causal link to transit dependence, supported by the transit equity literature.
2. **Data availability**: Each indicator must be obtainable from open BPS (Badan Pusat Statistik) data at kecamatan level or finer for the full Jabodetabek region.
3. **Non-redundancy**: Indicators should capture distinct dimensions of transit need; highly correlated indicators inflate the composite without adding information.

### 1.2 Indicator-by-Indicator Evaluation

#### Indicator 1: `pop_density` (Population per km²)

| Criterion | Assessment |
|-----------|------------|
| Literature support | Mamun & Lownes (2011a) include population density as a TNI component, reasoning that dense areas generate higher aggregate transit demand regardless of individual socioeconomic status. Jiao & Dillivan (2013) use population density as a primary demand-side variable in their transit desert framework. Currie (2010) uses population as a weighting factor in his social need index. |
| Causal link to transit need | Higher density increases aggregate demand for transit — more people per unit area means more potential riders. Dense areas also have land use patterns (mixed use, smaller lots, limited parking) that make private vehicle use less convenient, further increasing transit dependence. |
| Data availability | Derived from BPS population data (#8) and kelurahan area (#7). High availability. |
| Potential concern | Density is not a *socioeconomic* vulnerability indicator — it captures demand volume, not inability to use alternatives. A high-density, high-income area (e.g., Sudirman apartments) scores high on density but low on transit *need*. However, at the Jabodetabek scale, high-density areas in the periphery (e.g., dense kampung in Bekasi) typically correlate with lower income, making density a useful composite signal. |
| **Verdict** | **Confirmed.** Retain as the aggregate demand dimension. The other four indicators capture vulnerability; density captures volume. |

#### Indicator 2: `poverty_rate` (% population below poverty line)

| Criterion | Assessment |
|-----------|------------|
| Literature support | Core indicator in Mamun & Lownes (2011a): poverty is the strongest predictor of transit dependence because low-income populations cannot afford private vehicle ownership or operation. Currie (2010) uses SEIFA socioeconomic disadvantage, which includes poverty. Jomehpour & Smith-Colin (2020) integrate social vulnerability indicators including poverty. Delmelle & Casas (2012) stratify equity analysis by income group. |
| Causal link to transit need | Direct: households below the poverty line cannot afford car ownership (purchase + fuel + insurance + parking) or even consistent motorcycle ownership/maintenance. They are structurally dependent on public transit or walking. |
| Data availability | Available from BPS at kecamatan level. Disaggregated to kelurahan via population-weighted dasymetric mapping using WorldPop raster (methodology §2.5, step 9). |
| **Verdict** | **Confirmed.** Foundational indicator — present in nearly every TNI framework in the literature. |

#### Indicator 3: `avg_household_expenditure` (Monthly average, IDR)

| Criterion | Assessment |
|-----------|------------|
| Literature support | Not directly used in Mamun & Lownes (2011a) or Currie (2010), which rely on poverty rate or composite deprivation indices. However, household expenditure is a standard proxy for income in Indonesian statistics (BPS reports expenditure rather than income). Pereira et al. (2019) use income quintiles; expenditure serves the analogous role in the Indonesian context where income data is unreliable but expenditure surveys are robust. |
| Causal link to transit need | Expenditure is an inverse indicator: *lower* expenditure signals higher transit need (less disposable income for private transport). It captures a more granular economic gradient than the binary poverty_rate — two areas with 10% poverty rate may have very different expenditure distributions. |
| Data availability | Available from BPS SUSENAS aggregates at kecamatan level. Disaggregated to kelurahan via population-weighted dasymetric mapping. |
| Redundancy concern | Moderately correlated with `poverty_rate` — but captures different information. Poverty rate is binary (above/below line); expenditure captures the continuous gradient. An area with 5% poverty but very low average expenditure (near-poor population) has different transit need than one with 5% poverty and high average expenditure. |
| **Verdict** | **Confirmed.** Provides continuous economic gradient that poverty_rate (binary threshold) does not capture. Requires inversion during normalization (see §2). |

#### Indicator 4: `zero_vehicle_hh_pct` (% households with no motor vehicle)

| Criterion | Assessment |
|-----------|------------|
| Literature support | Explicitly used in Mamun & Lownes (2011a) as a TNI component. Jiao & Dillivan (2013) include zero-vehicle households in their transit demand calculation. Jomehpour & Smith-Colin (2020) use vehicle ownership as a vulnerability indicator. This is arguably the most direct measure of transit dependence — households without a car or motorcycle *must* use transit, walk, or rely on informal transport. |
| Causal link to transit need | Direct and unambiguous: no private vehicle means structural dependence on public transit for any trip beyond walking distance. In the Jabodetabek context, this includes households without motorcycles (the dominant private mode), making it an even stronger indicator than in Western contexts where "zero vehicle" typically means no car. |
| Data availability | Not directly available at kelurahan level from standard BPS publications. Must be modeled from kecamatan-level vehicle registration data combined with density proxies. This is the weakest data availability among the five indicators. |
| Modeling note | The methodology (§2.5, step 9) notes this is "modeled from kecamatan + density proxy." The proxy assumption is that within a kecamatan, denser areas have lower vehicle ownership rates (due to smaller housing, less parking, lower income). This is defensible but adds uncertainty. |
| **Verdict** | **Confirmed.** The most direct transit dependence indicator. Data modeling uncertainty is acknowledged in limitations. |

#### Indicator 5: `dependency_ratio` ((Age <15 + Age >64) / working-age population)

| Criterion | Assessment |
|-----------|------------|
| Literature support | Used in Mamun & Lownes (2011a) — they include elderly population percentage. Jiao & Dillivan (2013) include populations "too young, too old, or physically unable to drive" in their transit-dependent population definition. The dependency ratio captures both youth and elderly populations who are less likely to hold driving licenses or operate motorcycles. |
| Causal link to transit need | Moderate: dependents (children, elderly) cannot drive and are more likely to need transit for school, healthcare, and social trips. However, in the Jabodetabek context, many dependents are *driven* by working-age household members (parents drive children to school; adult children drive elderly parents). The dependency ratio is thus a noisier signal of transit need than in Western contexts where elderly and youth are more likely to travel independently. |
| Context-specific concern | In Indonesian cultural context, multi-generational households are common, and dependents' travel is often handled by working-age family members on motorcycles. A high dependency ratio does not necessarily translate to high transit ridership demand for dependents. However, it does increase the household's overall mobility burden — more trips needed, stretching the household's transport budget. |
| **Verdict** | **Confirmed with caveat.** Retain for consistency with Mamun & Lownes (2011a) framework and because it captures the mobility burden dimension. Note in limitations that Indonesian household travel patterns may attenuate its signal compared to Western TNI applications. |

### 1.3 Indicators Considered but Excluded

| Candidate | Why considered | Why excluded |
|-----------|---------------|--------------|
| `disability_rate` | Mamun & Lownes (2011a) include disability as a transit need factor | No reliable kelurahan- or kecamatan-level disability data available from BPS for Jabodetabek. Would require SUSENAS microdata (restricted access). Could be added in v2 if data becomes available. |
| `female_headed_hh_pct` | Some equity frameworks include gender as a vulnerability dimension | No consistent data at the required granularity. Also, the causal link to transit *need* (vs. transit *experience*) is less direct — better suited to a transit equity *quality* analysis than a need index. |
| `informal_employment_pct` | Informal workers have irregular schedules that transit may not serve well | No reliable data below provincial level. Also conflates transit need (demand) with transit suitability (supply-side mismatch), which should remain on the TAI side. |

### 1.4 Summary: Confirmed Indicator Set

| # | Indicator | Dimension | Direction | Literature precedent |
|---|-----------|-----------|-----------|---------------------|
| 1 | `pop_density` | Aggregate demand | Higher raw = higher need | Mamun & Lownes (2011a), Jiao & Dillivan (2013) |
| 2 | `poverty_rate` | Economic vulnerability | Higher raw = higher need | Mamun & Lownes (2011a), Currie (2010), Delmelle & Casas (2012) |
| 3 | `avg_household_expenditure` | Economic gradient | **Higher raw = LOWER need** (invert) | Pereira et al. (2019) income proxy; BPS standard |
| 4 | `zero_vehicle_hh_pct` | Transit dependence | Higher raw = higher need | Mamun & Lownes (2011a), Jiao & Dillivan (2013) |
| 5 | `dependency_ratio` | Demographic vulnerability | Higher raw = higher need | Mamun & Lownes (2011a), Jiao & Dillivan (2013) |

---

## 2. Normalization Method

### 2.1 Method: Min-Max Normalization to [0, 1]

All five indicators are normalized to a common [0, 1] scale using min-max normalization before composite index construction. This follows the approach used by Mamun & Lownes (2011a, 2011b) and Rathod et al. (2025).

**Formula (standard direction — higher raw = higher need):**

```
x_norm = (x - x_min) / (x_max - x_min)
```

Where `x_min` and `x_max` are computed across all spatial units (kelurahan or H3 cells) in the study area.

**Formula (inverted direction — higher raw = LOWER need):**

For `avg_household_expenditure`, where higher expenditure indicates *lower* transit need:

```
x_norm = 1 - (x - x_min) / (x_max - x_min)
     = (x_max - x) / (x_max - x_min)
```

This ensures that after normalization, a value of 1.0 always means "highest transit need" and 0.0 means "lowest transit need" across all five indicators.

### 2.2 Direction Summary

| Indicator | Raw direction | Normalization | After normalization |
|-----------|--------------|---------------|-------------------|
| `pop_density` | Higher = more demand | Standard min-max | 1.0 = densest area |
| `poverty_rate` | Higher = more poverty | Standard min-max | 1.0 = highest poverty |
| `avg_household_expenditure` | Higher = wealthier | **Inverted** min-max | 1.0 = lowest expenditure (highest need) |
| `zero_vehicle_hh_pct` | Higher = more carless | Standard min-max | 1.0 = most carless HH |
| `dependency_ratio` | Higher = more dependents | Standard min-max | 1.0 = highest dependency |

### 2.3 Why Min-Max Over Alternatives

| Method | Pros | Cons | Decision |
|--------|------|------|----------|
| **Min-max** | Simple, interpretable, bounded [0,1], preserves relative distances | Sensitive to outliers at extremes | **Selected** — matches Mamun & Lownes (2011a) precedent; outlier handling via capping (see §4.3) |
| Z-score | Not bounded; handles outliers better | Negative values; harder to interpret as "need level"; no natural [0,1] scale for composite | Rejected — unbounded scores complicate weighted combination and quadrant classification |
| Percentile rank | Robust to outliers | Loses magnitude information; all distributions become uniform | Rejected — magnitude matters (a kelurahan with 40% poverty rate is meaningfully different from one at 35%, not just ranked differently) |
| Robust scaler (IQR) | Outlier-resistant | Not bounded [0,1]; less interpretable | Rejected — adds complexity without clear benefit given our outlier capping strategy |

---

## 3. Weighting Scheme

### 3.1 Default: Equal Weighting

```
TNI = 0.20 × norm(pop_density)
    + 0.20 × norm(poverty_rate)
    + 0.20 × norm_inv(avg_household_expenditure)
    + 0.20 × norm(zero_vehicle_hh_pct)
    + 0.20 × norm(dependency_ratio)
```

### 3.2 Rationale for Equal Weighting

The literature provides no strong empirical basis for differential weighting of TNI indicators:

1. **Mamun & Lownes (2011a)** use equal weighting for their TNI components and do not test alternatives, noting that "no theoretical basis exists for assigning greater importance to one indicator over another" in the absence of local calibration data.

2. **Currie (2010)** uses a single composite deprivation index (SEIFA) rather than constructing weights, sidestepping the weighting question entirely.

3. **Rathod et al. (2025)** apply equal weighting as the default for their composite accessibility index in a data-constrained developing-country context, arguing that differential weighting requires either (a) expert elicitation via Analytic Hierarchy Process (AHP) or (b) statistical derivation via Principal Component Analysis (PCA), both of which demand calibration data or expert panels not available in many developing-country contexts.

4. **Jiao & Dillivan (2013)** use equal weighting across their demand-side indicators (population density, zero-vehicle households, elderly, youth, below-poverty-line population).

Equal weighting is therefore the consensus default in the TNI literature. It is transparent, reproducible, and avoids imposing researcher judgment on indicator importance without empirical justification.

### 3.3 Sensitivity Analysis: Weight Perturbation

To test whether the TNI results are robust to weighting assumptions, a perturbation analysis will be conducted:

**Method**: Monte Carlo weight perturbation with 1,000 iterations.

```
For each iteration:
  1. Draw 5 perturbation factors from Uniform(0.8, 1.2)  — i.e., ±20%
  2. Multiply each default weight (0.20) by its perturbation factor
  3. Renormalize weights to sum to 1.0
  4. Recompute TNI for all spatial units
  5. Record: (a) Spearman rank correlation with baseline TNI,
             (b) % of spatial units that change quadrant classification

Report:
  - Median and 95% CI of rank correlation across iterations
  - % of units with unstable quadrant assignment (changed in >10% of iterations)
  - Identify which indicator's weight perturbation has the largest effect on rankings
```

**Interpretation thresholds**:
- Spearman rho > 0.95 in >95% of iterations → results are robust to weighting; equal weighting is defensible
- Spearman rho < 0.90 in >10% of iterations → results are sensitive; consider PCA-derived or expert-elicited weights
- If a single indicator dominates sensitivity → discuss in limitations; consider alternative weight schemes in appendix

### 3.4 Alternative Weighting Schemes (for sensitivity comparison only)

| Scheme | Weights | Rationale | Role |
|--------|---------|-----------|------|
| **Equal** (default) | All 0.20 | Literature consensus; no a priori basis for differentiation | Primary analysis |
| **Economic-emphasis** | poverty 0.30, expenditure 0.25, vehicle 0.20, density 0.15, dependency 0.10 | Prioritizes direct economic vulnerability | Sensitivity check |
| **Vehicle-emphasis** | vehicle 0.30, poverty 0.25, density 0.20, expenditure 0.15, dependency 0.10 | Prioritizes the most direct transit dependence measure | Sensitivity check |
| **PCA-derived** | Weights from first principal component loadings | Data-driven; captures variance structure | Sensitivity check (if PCA loadings are interpretable) |

These alternatives are computed and compared in the results, but the equal-weighted scheme is the primary reported result. The paper will present a sensitivity comparison table showing how quadrant classifications shift under each scheme.

---

## 4. Edge Cases

### 4.1 Missing Data

**Scenario**: A kelurahan has missing values for one or more TNI indicators (e.g., BPS did not report poverty_rate for a particular kecamatan).

**Strategy (hierarchical fallback)**:

| Priority | Method | When to apply |
|----------|--------|---------------|
| 1 | **Parent kecamatan value** | If kelurahan data is missing but kecamatan-level data exists (most common case — BPS reports at kecamatan, we disaggregate to kelurahan) |
| 2 | **Adjacent kelurahan average** | If the kecamatan value is also missing, use the population-weighted mean of neighboring kelurahan within the same kota/kabupaten |
| 3 | **Kota/kabupaten average** | If no neighboring values are available |
| 4 | **Exclude from analysis** | If more than 2 of 5 indicators are missing for a spatial unit, exclude it entirely and flag in the output. Report count and spatial pattern of excluded units. |

**For H3 cells**: Missing data is less likely because H3 values are derived from kelurahan via dasymetric mapping. If the source kelurahan has missing data, the H3 cells within it inherit the same fallback value.

**Reporting requirement**: The paper must report:
- Total count of spatial units with any imputed values
- Which indicators had the most missing data
- Whether excluded units cluster spatially (potential systematic bias)

### 4.2 Zero Variance

**Scenario**: An indicator has zero variance across all spatial units (i.e., `x_max == x_min`). This would make the min-max denominator zero, producing undefined normalized values.

**Strategy**:

```
if x_max == x_min:
    # All spatial units have the same value for this indicator
    # The indicator provides no discriminatory power
    x_norm = 0.5 for all units  # neutral — contributes nothing to relative ranking
    # Flag this indicator in the analysis log
    # Redistribute its weight equally among remaining indicators
```

**In practice**: Zero variance is extremely unlikely for any of the five indicators across ~1,800 kelurahan in Jabodetabek (population density ranges from ~500/km² to >30,000/km²; poverty rates from <2% to >15%). If it occurs, it would indicate a data error rather than a real phenomenon.

**Near-zero variance** (coefficient of variation < 0.05): Flag but retain. Report in EDA that the indicator has limited discriminatory power and note that results may be insensitive to its inclusion.

### 4.3 Outliers

**Scenario**: Extreme values in one or more indicators (e.g., an industrial kelurahan with `pop_density` near zero, or a single kelurahan with `poverty_rate` of 45% when the next highest is 18%).

**Strategy: Winsorization at the 2nd and 98th percentiles.**

```
For each indicator:
  p2 = np.percentile(values, 2)
  p98 = np.percentile(values, 98)
  values_capped = np.clip(values, p2, p98)
  # Then apply min-max normalization to capped values
```

**Rationale**:
- The methodology (§2.5) states: "Keep outliers for spatial analysis (extreme values are the signal, not noise)." This applies to the spatial analysis and mapping — we do not delete outlier kelurahan.
- However, for *normalization*, extreme outliers compress the rest of the distribution. If one kelurahan has `pop_density` = 50,000/km² and the next highest is 25,000/km², min-max normalization squeezes all values into the lower half of [0, 1], reducing discriminatory power.
- Winsorization at 2/98 preserves the outlier units (they score 0.0 or 1.0) while preventing distribution compression for the remaining 96% of units.
- This follows the approach of Rathod et al. (2025), who cap extreme values before normalization in their composite index construction.

**Reporting requirement**: Report the count and identity of winsorized spatial units per indicator. If the same kelurahan is winsorized on multiple indicators, discuss whether it represents a genuine extreme case or a data quality issue.

### 4.4 Edge Case: Kelurahan with Zero Population

Some kelurahan in the Jabodetabek boundary may have near-zero residential population (e.g., industrial zones, airport areas, large parks/cemeteries). These are not meaningful units for transit need analysis.

**Strategy**:
- Exclude kelurahan with population < 100 from the TNI computation.
- They remain in the spatial dataset (for mapping completeness) but receive `tni_score = null` and `quadrant = null`.
- Report count and identity of excluded units.

### 4.5 Edge Case: H3 Cells at Study Area Boundary

H3 cells at the Jabodetabek boundary may be only partially within the study area, with partial population and infrastructure coverage.

**Strategy**:
- Include if >50% of the cell area falls within the Jabodetabek boundary polygon.
- Exclude if <50% and flag.
- For included boundary cells, scale population and area-weighted metrics by the fraction of cell area within the boundary.

---

## 5. Literature Citations Summary

| Design decision | Supporting citation(s) |
|-----------------|----------------------|
| Five-indicator TNI structure | Mamun & Lownes (2011a) — poverty, vehicle ownership, dependency ratio as core TNI components |
| Population density as demand indicator | Jiao & Dillivan (2013) — population density in transit desert demand calculation |
| Poverty rate as vulnerability indicator | Mamun & Lownes (2011a); Currie (2010) via SEIFA; Delmelle & Casas (2012) income stratification |
| Household expenditure as income proxy | Pereira et al. (2019) — income-based equity analysis; BPS methodological precedent |
| Zero-vehicle households | Mamun & Lownes (2011a); Jiao & Dillivan (2013) — direct transit dependence |
| Dependency ratio | Mamun & Lownes (2011a) — elderly population; Jiao & Dillivan (2013) — age-based transit dependence |
| Min-max normalization | Mamun & Lownes (2011a, 2011b); Rathod et al. (2025) — standardized grading scale |
| Equal weighting as default | Mamun & Lownes (2011a); Jiao & Dillivan (2013); Rathod et al. (2025) |
| Weight perturbation sensitivity | Rathod et al. (2025) — sensitivity testing for composite indices in developing-country contexts |
| Winsorization for outlier handling | Rathod et al. (2025) — capping extreme values before normalization |
| Need-supply gap framework (TNI vs TAI) | Currie (2010); Mamun & Lownes (2011a); Jiao & Dillivan (2013); Jomehpour & Smith-Colin (2020) |

---

## 6. Implementation Notes

### 6.1 Pseudocode for TNI Computation

```python
import numpy as np
import pandas as pd

def compute_tni(df: pd.DataFrame, weights: dict = None) -> pd.Series:
    """
    Compute Transit Need Index for all spatial units.

    Parameters
    ----------
    df : DataFrame with columns:
        pop_density, poverty_rate, avg_household_expenditure,
        zero_vehicle_hh_pct, dependency_ratio
    weights : dict mapping indicator name to weight (default: equal 0.20)

    Returns
    -------
    Series of TNI scores in [0, 1]
    """
    if weights is None:
        weights = {
            'pop_density': 0.20,
            'poverty_rate': 0.20,
            'avg_household_expenditure': 0.20,
            'zero_vehicle_hh_pct': 0.20,
            'dependency_ratio': 0.20,
        }

    # Indicators where higher raw = higher need (standard normalization)
    standard_indicators = [
        'pop_density', 'poverty_rate',
        'zero_vehicle_hh_pct', 'dependency_ratio'
    ]
    # Indicators where higher raw = LOWER need (inverted normalization)
    inverted_indicators = ['avg_household_expenditure']

    normalized = pd.DataFrame(index=df.index)

    for col in standard_indicators + inverted_indicators:
        values = df[col].copy()

        # Winsorize at 2nd and 98th percentiles
        p2 = values.quantile(0.02)
        p98 = values.quantile(0.98)
        values = values.clip(p2, p98)

        # Min-max normalize
        x_min, x_max = values.min(), values.max()

        if x_max == x_min:
            # Zero variance — assign neutral 0.5
            normalized[col] = 0.5
        elif col in inverted_indicators:
            # Invert: higher raw = lower need
            normalized[col] = (x_max - values) / (x_max - x_min)
        else:
            # Standard: higher raw = higher need
            normalized[col] = (values - x_min) / (x_max - x_min)

    # Weighted sum
    tni = sum(weights[col] * normalized[col] for col in weights)

    return tni
```

### 6.2 Consistency with DATA_MODEL.md

The current `docs/DATA_MODEL.md` schema defines the five TNI indicators and `tni_score` field. No changes to DATA_MODEL.md are required — the indicator set matches exactly.

The normalization direction for `avg_household_expenditure` (inverted) and the winsorization step are implementation details that live in the processing pipeline (`lib/data-utils.ts` or Python pipeline scripts), not in the schema definition.

---

## 7. Open Questions for Review

1. **Winsorization percentiles**: The 2nd/98th percentile thresholds are a judgment call. Should we test 1st/99th and 5th/95th as alternatives in the sensitivity analysis?

2. **Dependency ratio scope**: In the Indonesian context, should we narrow the dependency ratio to elderly-only (age >64) given that youth travel is typically handled by parents on motorcycles? Or keep the standard definition for comparability with Mamun & Lownes (2011a)?

3. **PCA as a robustness check**: If the first principal component of the five indicators explains >70% of variance and has interpretable loadings, should PCA-derived weights replace equal weights as the primary scheme? Or should PCA remain a sensitivity comparison only?

4. **Vehicle ownership proxy quality**: The `zero_vehicle_hh_pct` indicator requires the most modeling (kecamatan vehicle registration + density proxy). Should we flag this indicator's uncertainty more prominently, or is the current limitations note sufficient?
