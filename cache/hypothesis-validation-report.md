# Hypothesis Validation Report — MVP-87 Reconciler
*Generated: 2026-03-28*
*Theory assessment: cache/hypothesis-theory-assessment.md*
*Stats assessment: cache/hypothesis-stats-assessment.md*

---

## Reconciliation Summary

| Hypothesis | Theory | Stats | Reconciled | Confidence | MVP-14 Gate |
|---|---|---|---|---|---|
| H1 | PROCEED | AWAITING_DATA | BLOCKED | High (theory), null (data) | BLOCKED — awaiting real data |
| H2 | PROCEED | AWAITING_DATA | BLOCKED | High (theory), null (data) | BLOCKED — awaiting real data |
| H3 | PROCEED | AWAITING_DATA | BLOCKED | Medium (theory), null (data) | BLOCKED — awaiting real data |

---

## H1 Detail

**Theory said**: Q4 units will be disproportionately concentrated (≥ 60%) in Bodetabek
suburban periphery rather than DKI Jakarta core. Theoretical confidence is HIGH — the
prediction is grounded in transit network structure (KRL/MRT inward-facing topology),
urbanisation patterns (peripheral growth outpacing transit extension), and the
Need-Supply Gap literature (Currie 2010; Jiao & Dillivan 2013). PROCEED threshold:
Q4 ≥ 60% Bodetabek. REFINE: 40–60%. PIVOT: < 40% or uniform distribution.

**Stats showed**: null — `data/processed/analysis/equity_summary.json` does not exist.
No quadrant_counts, spatial_concentration, or Moran's I data available.

**Agreement/disagreement**: Not assessable. Theory has issued PROCEED; Stats cannot
yet confirm or contradict.

**Recommended action**: Execute data pipeline to produce equity_summary.json. Once
`spatial_concentration.q4_bodetabek_pct` is available, compare directly against
the 60% threshold. If the value is ≥ 60%, this moves to confident PROCEED. If
40–60%, flag for supervisor as a partial-support finding to be discussed in Discussion
section. If < 40%, escalate immediately for hypothesis reframing before MVP-14.

**Risk level for PIVOT**: Low-to-medium (theory strongly predicts PROCEED, but the
simplified pipeline may not fully capture spatial patterns if the kelurahan dataset
coverage is incomplete).

---

## H2 Detail

**Theory said**: Gini_H3 > Gini_kelurahan — finer resolution reveals greater
distributional inequality, consistent with MAUP theory (Javanmard et al. 2023).
Theoretical confidence is HIGH — the structural conditions in Jabodetabek (extreme
kelurahan area variance, 0.5–50 km²) make within-unit heterogeneity a near-certainty
in large suburban kelurahan. PROCEED threshold: any positive Gini delta. REFINE:
|delta| < 0.01. PIVOT: Gini_H3 < Gini_kelurahan.

**Stats showed**: null — Gini coefficients at both resolutions unavailable. Cohen's
kappa for quadrant agreement also unavailable.

**Agreement/disagreement**: Not assessable.

**Recommended action**: Execute pipeline to generate both Gini values. The H2 verdict
is the most mechanically straightforward to compute — it reduces to a single arithmetic
comparison (H3 Gini minus kelurahan Gini). If the pipeline runs correctly, this should
be the first hypothesis resolved. Suggest running EDA script with Gini computation
as a minimal viable check before full equity_summary.json generation.

**Risk level for PIVOT**: Very low. The only scenario producing PIVOT is if kelurahan
boundaries systematically isolate high- and low-access sub-units — an unlikely design
criterion for Indonesian administrative boundaries drawn for governance, not transit
service homogeneity.

---

## H3 Detail

**Theory said**: New transit node in Q4 zone produces delta_EGS > 1.5× the delta
from the same node in Q1/Q2 zone. Theoretical confidence is MEDIUM — the direction
of effect is robust (high-need areas have more room to improve in TAI) but the 1.5×
magnitude threshold is sensitive to scenario design and the simplified buffer/isochrone
simulation model described in methodology.md limitations. PROCEED: delta ratio > 1.5.
REFINE: ratio 1.0–1.5. PIVOT: ratio ≤ 1.0.

**Stats showed**: null — no scenario simulation outputs available.

**Agreement/disagreement**: Not assessable.

**Recommended action**: When pipeline runs, pay particular attention to the scenario
simulation implementation. If the buffer model produces only small TAI increments
even in Q4 zones (due to first-mile bottleneck absorbing the improvement), consider
whether REFINE is the correct outcome rather than PIVOT — theory is directionally
correct but simulation sensitivity may be insufficient for the 1.5× threshold. Flag
this for supervisor review if the delta ratio lands in the 1.0–1.5 range.

**Risk level for PIVOT**: Medium. H3 carries the highest methodological risk because
the scenario simulation is explicitly a simplified model. However, PIVOT would not
invalidate the quadrant framework — it would indicate the simulation method is not
sensitive enough to demonstrate the effect, which is a limitation to acknowledge
rather than a finding that requires reframing the entire analysis.

---

## Gate Status for MVP-14 (Results Writing)

**Status: BLOCKED — awaiting real pipeline data**

MVP-14 (Results writing) must NOT begin until equity_summary.json exists and Agent
Stats can produce a real numerical assessment for all three hypotheses.

**What would unblock the gate:**

1. Run the data pipeline scripts to produce `data/processed/analysis/equity_summary.json`
2. Re-run Agent Stats (MVP-87 Step 2) with real data
3. Re-run Reconciler (MVP-87 Step 3) with both real assessments
4. If all three hypotheses converge on PROCEED or REFINE → **CLEAR TO PROCEED**
5. If any hypothesis shows PIVOT → **HUMAN REVIEW REQUIRED before MVP-14**

**Minimum viable unblock**: If time is constrained, H2 can be assessed first with
only Gini computation (no spatial analysis needed) as an early-stage gate check.
H1 and H3 require the full pipeline.

---

## Open Items

| Item | Hypothesis | Action Required | Responsible |
|------|------------|-----------------|-------------|
| Pipeline not run — equity_summary.json absent | H1, H2, H3 | Execute data pipeline scripts | Data pipeline owner |
| H3 simulation sensitivity risk | H3 | When data available: review delta ratio carefully; if 1.0–1.5× flag for supervisor | Human review |
| H1 potential partial support | H1 | If Q4 Bodetabek pct = 40–60%, prepare nuanced framing for Discussion | Paper author |
| Re-run Agent Stats with real data | H1, H2, H3 | After pipeline execution: update hypothesis-stats-assessment.md with real values | Agent Stats (MVP-87 re-run) |
| Re-run Reconciler with real Stats | H1, H2, H3 | After Stats re-run: update this report with final verdicts | Reconciler (MVP-87 re-run) |

---

## Notes for Paper Writing (when gate clears)

- If H1 PROCEEDS: Introduction and Discussion can claim "Q4 zones are disproportionately
  peripheral — consistent with the radial transit investment pattern in Jabodetabek."
- If H2 PROCEEDS: The dual-resolution comparison can be framed as "H3 reveals X% greater
  Gini inequality than kelurahan — confirming that administrative boundaries mask
  within-unit variation in heterogeneous suburban areas."
- If H3 PROCEEDS: The scenario section can conclude "Infrastructure placed in transit
  deserts yields N× greater equity improvement than equivalent investment in already-served
  areas — validating the quadrant framework as a planning prioritization tool."
- Any REFINE verdict should be reported as a nuanced finding, not a failure. Partial
  support or smaller-than-expected effect sizes are valid academic findings in
  descriptive spatial analysis.
- Any PIVOT verdict requires escalation to supervisor before drafting Results section.
