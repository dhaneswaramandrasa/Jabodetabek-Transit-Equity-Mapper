# Hypothesis Stats Assessment — MVP-87 Agent Stats
*Role: pure data analyst — assessing from numerical evidence only*
*Methodology.md thresholds NOT consulted during this assessment*
*Data source: data/processed/analysis/equity_summary.json*
*Data status: AWAITING_DATA*
*Generated: 2026-03-28*

---

## Data Availability Check

**Path checked**: `data/processed/analysis/equity_summary.json`
**Result**: FILE NOT FOUND — directory `data/processed/analysis/` does not exist.

The pipeline scripts have been written (per project state) but have not yet been run
against real data. All three hypothesis assessments below use null metrics and the
AWAITING_DATA status. No numerical verdicts can be issued until the pipeline
produces `equity_summary.json`.

---

## H1 — Spatial Mismatch

**Metric observed**: Q4 unit count / percentage in Bodetabek vs. DKI Jakarta
- Kelurahan Q4 count: `null` — AWAITING_DATA
- H3 hexagon Q4 count: `null` — AWAITING_DATA
- Bodetabek-concentrated Q4 percentage: `null` — AWAITING_DATA
- Moran's I (Q4 spatial autocorrelation): `null` — AWAITING_DATA
- LISA cluster spatial distribution: `null` — AWAITING_DATA

**Spatial concentration**: AWAITING_DATA. Cannot assess whether Q4 units cluster
in Bodetabek periphery vs. DKI Jakarta core without spatial distribution data from
the analysis pipeline.

**Stats verdict**: AWAITING_DATA

**Observed value**: null

**Rationale**: The equity_summary.json file required for this assessment does not
exist. The pipeline scripts that compute quadrant classifications, spatial
distributions, and Moran's I statistics must be executed against the cleaned dataset
before any numerical verdict is possible. The Stats agent cannot issue PROCEED,
REFINE, or PIVOT without actual quadrant_counts and spatial_concentration fields
from the analysis output.

**Required pipeline outputs to unblock this assessment**:
- `quadrant_counts.kelurahan` — count and pct per quadrant (Q1/Q2/Q3/Q4)
- `quadrant_counts.h3` — same for H3 resolution
- `spatial_concentration.q4_bodetabek_pct` — % of Q4 units in Bodetabek municipalities
- `spatial_concentration.q4_jakarta_pct` — % of Q4 units in DKI Jakarta
- `morans_i.q4_cluster_z_score` — statistical significance of Q4 clustering

---

## H2 — Resolution Effect

**Metric observed**:
- Gini_TAI kelurahan: `null` — AWAITING_DATA
- Gini_TAI H3: `null` — AWAITING_DATA
- Gini delta (H3 − kelurahan): `null` — AWAITING_DATA
- Cohen's kappa (quadrant agreement): `null` — AWAITING_DATA
- h2_hypothesis_signal flag: `null` — AWAITING_DATA

**Stats verdict**: AWAITING_DATA

**Observed value**: null (Gini delta)

**Rationale**: The Gini coefficients computed at both kelurahan and H3 resolutions
are the core metric for H2. These are not available without pipeline execution.
The h2_hypothesis_signal field (if present in equity_summary.json output schema)
would directly flag whether Gini_H3 > Gini_kelurahan, but that field is null
because the file does not exist.

**Required pipeline outputs to unblock this assessment**:
- `gini.kelurahan_tai` — Gini coefficient for TAI distribution at kelurahan resolution
- `gini.h3_tai` — Gini coefficient for TAI distribution at H3 resolution
- `gini.delta` — H3 minus kelurahan (positive = H3 reveals more inequality)
- `resolution_comparison.cohens_kappa` — quadrant agreement between resolutions
- `resolution_comparison.disagreement_count` — units where kelurahan vs H3 quadrant differs
- `resolution_comparison.h2_hypothesis_signal` — boolean or flag from pipeline

---

## H3 — Scenario Validation

**Metric observed**:
- Scenario delta (Q4 node placement): `null` — AWAITING_DATA
- Scenario delta (Q1/Q2 node placement): `null` — AWAITING_DATA
- Delta ratio Q4/Q1_Q2: `null` — AWAITING_DATA
- Quadrant membership shift (Q4 units exiting Q4): `null` — AWAITING_DATA
- EGS baseline vs. simulated comparison: `null` — AWAITING_DATA

**Stats verdict**: AWAITING_DATA

**Observed value**: null (delta ratio)

**Rationale**: The scenario simulation output — comparing equity score delta for a
new transit node placed in a Q4 zone vs. a Q1/Q2 zone — requires the scenario
analysis scripts to have been executed. No numerical evidence is available to assess
whether the Q4 placement produces a larger delta. The Stats agent cannot
independently derive this from any available file.

**Required pipeline outputs to unblock this assessment**:
- `scenario.q4_node.mean_egs_delta` — mean Equity Gap Score improvement for Q4 intervention
- `scenario.q1q2_node.mean_egs_delta` — same for Q1/Q2 intervention
- `scenario.delta_ratio` — Q4 delta / Q1_Q2 delta (target: > 1.5)
- `scenario.q4_units_reclassified` — count of Q4 units exiting Q4 quadrant post-simulation
- `scenario.q1q2_units_reclassified` — same for Q1/Q2 comparison

---

## Overall Stats Verdict

| Hypothesis | Stats Verdict | Observed Metric | Threshold to Watch |
|------------|---------------|-----------------|-------------------|
| H1 | AWAITING_DATA | null | Q4 Bodetabek pct ≥ 60% |
| H2 | AWAITING_DATA | null | Gini_H3 − Gini_kelurahan > 0 |
| H3 | AWAITING_DATA | null | Delta ratio Q4/Q1_Q2 > 1.5 |

**Gate status**: All three hypotheses are blocked pending pipeline execution.
No statistical evidence is available to confirm or refute any hypothesis.

**Next action required**: Run the data pipeline to generate
`data/processed/analysis/equity_summary.json`. Once that file exists,
re-run Agent Stats to produce a real numerical assessment.
