# Hypothesis Validation Report — MVP-87 Reconciler
*Pattern: Dual-Agent Convergence (Stats vs Theory) + Reconciler*
*Stats assessment: cache/hypothesis-stats-assessment.md (re-run 2026-04-02)*
*Theory assessment: cache/hypothesis-theory-assessment.md (2026-03-28)*
*Data: full r5py pipeline at kelurahan + H3 resolution*
*Updated: 2026-04-02*

---

## Reconciler Method

For each hypothesis, compare Stats verdict vs Theory verdict:
- Both PROCEED → **confident PROCEED** — write Results as-is
- Both PIVOT → halt MVP-14, human escalation required
- Disagreement → flag for human review before writing

---

## H1 — Spatial Mismatch

| Agent | Verdict | Key Evidence |
|---|---|---|
| Theory | PROCEED (High) | KRL/MRT radial topology predicts Bodetabek Q4 concentration; threshold 60% |
| Stats | PROCEED (High) | 98.8% Q4 in Bodetabek; Moran's I 0.8876; LISA LL clusters peripheral |

**Reconciler**: AGREE → **PROCEED (High confidence)**

The stats result (98.8%) dramatically exceeds the theory threshold (60%). Both agents
independently predict and confirm the same spatial pattern: Q4 transit deserts are
concentrated in the Bodetabek kabupaten ring (Bogor, Tangerang, Bekasi), not in DKI
Jakarta. LISA LL clusters confirm the spatial coherence of the pattern statistically.

**Results writing guidance:**
- Lead with the 98.8% figure — it is the headline number for H1
- Describe the kabupaten breakdown (Bogor 46.5%, Tangerang 29.6%, Bekasi 16.1%)
- Note the 5 DKI Q4 units are Kepulauan Seribu (islands, not urban transit context)
- Connect to Moran's I 0.8876 (spatial autocorrelation confirms clustering, not random)
- LISA map shows LL clusters (transit desert clusters) in the south/west periphery

---

## H2 — Resolution Effect (MAUP)

| Agent | Verdict | Key Evidence |
|---|---|---|
| Theory | PROCEED (High) | Kelurahan area variance 0.5–50 km² guarantees MAUP effect; Gini_H3 > Gini_kel |
| Stats | PROCEED (High) | Gini_H3=0.6128 vs Gini_kel=0.2441; delta=+0.3687; kappa=0.6124 |

**Reconciler**: AGREE → **PROCEED (High confidence)**

Theory predicted Gini_H3 > Gini_kelurahan with a delta > 0.03 based on MAUP literature.
Stats observed delta = +0.3687 — approximately 12× the theoretical floor. Both agents
agree on direction and the magnitude far exceeds the threshold. The H2 signal is the
strongest of the three hypotheses numerically.

**One methodological nuance to flag in Results** (not a divergence — both agents
acknowledge this): The large Gini_H3 is partly driven by the 88.8% of H3 cells outside
the transit network getting L3=0. Theory predicted MAUP would drive the gap; the data
confirms MAUP plus genuine transit coverage sparsity both contribute. Both effects
are real and complementary — the Results section should note both.

**Results writing guidance:**
- Report Gini_H3 = 0.6128, Gini_kel = 0.2441, delta = +0.3687
- Explain the MAUP mechanism: H3 hexagons cut across administrative boundaries,
  exposing within-kelurahan variation masked by administrative aggregation
- Note the complementary role of transit coverage sparsity (11.2% H3 routing coverage)
- Cohen's kappa 0.6124 with 29% reclassification: strong agreement at aggregate but
  meaningful within-unit variation — use confusion matrix to illustrate
- Moran's I H3 = 0.9447 (higher than kelurahan 0.8876) — finer resolution reveals
  even stronger spatial structure

---

## H3 — Scenario Validation (Equity Gap Improvement Potential)

| Agent | Verdict | Key Evidence |
|---|---|---|
| Theory | PROCEED (Medium) | Mathematical structure of EGS guarantees Q4 has more room; 1.5× threshold |
| Stats | PROCEED (Medium-High) | Q4/Q1 equity gap ratio = 1.65×; Q4/(Q1+Q2) = 2.67× |

**Reconciler**: AGREE → **PROCEED (Medium confidence)**

Both agents reach PROCEED but with medium confidence. Stats observed 1.65× (above
the 1.5× threshold by 10%), which is meaningful but not a large margin. Theory flagged
that the simulation simplification (proxy equity gap rather than live transit simulation)
reduces confidence. Both agents converge on the same limitation: the H3 measurement
uses the equity gap differential as a proxy, not a forward-simulation of a new transit
node.

**Important caveat** (both agents agree): The 1.65× ratio is computed from existing
equity gaps, not from a simulated intervention. The Results section should:
1. Present the equity gap differential as the observable evidence
2. Note that Q4 units have 1.65× higher equity gap than Q1 units by construction of
   the TNI-TAI framework
3. Frame this as "improvement potential" rather than "intervention impact simulation"
4. Acknowledge that actual improvement depends on first-mile infrastructure (L1) and
   transit network connectivity, which are not modeled in the scenario

**Results writing guidance:**
- Present mean equity gap table: Q4=0.385, Q1=0.234, Q2=0.055, Q3=0.241
- Report Q4/Q1 ratio = 1.65× (clears 1.5× threshold)
- Note Q4/(Q1+Q2 avg) = 2.67× for robustness check
- Frame as "differential improvement potential" not "simulated outcome"
- Connect to LISA cluster map: LL clusters in periphery = where intervention is highest-leverage

---

## Final Verdict Summary

| Hypothesis | Theory | Stats | Reconciler | MVP-14 Gate |
|---|---|---|---|---|
| H1 | PROCEED (High) | PROCEED (High) | **PROCEED (High)** | ✅ Clear |
| H2 | PROCEED (High) | PROCEED (High) | **PROCEED (High)** | ✅ Clear |
| H3 | PROCEED (Medium) | PROCEED (Medium-High) | **PROCEED (Medium)** | ✅ Conditional |

**MVP-14 gate**: **UNBLOCKED — all three hypotheses PROCEED.**

No human escalation required. No hypothesis is PIVOT or requires reframing.
H3 carries a methodological caveat (proxy measurement) but does not change the verdict.

---

## Caveats to Address in Results Section

1. **H1**: 5 DKI Jakarta Q4 units = Kepulauan Seribu (remote islands). Exclude or
   footnote when reporting "DKI Jakarta Q4 = 1.2%".

2. **H2**: Gini_H3 amplification has two contributing factors — MAUP effect (the
   primary claim) and transit coverage sparsity (88.8% of H3 cells unrouted). Both
   are real and valid, but the distinction matters for interpretation. State clearly:
   "H3 reveals more inequality because (a) finer resolution exposes within-kelurahan
   variation, and (b) the transit network reaches only 11.2% of the spatial area."

3. **H3**: Equity gap differential is the observable proxy for improvement potential.
   A full scenario simulation (new transit node placement + TAI re-computation) was
   not implemented. The 1.65× figure is descriptive, not predictive.

---

## Data Sources Used in This Report

| File | Key values used |
|---|---|
| `data/processed/analysis/equity_summary.json` | Gini TAI kelurahan=0.2441, H3=0.6128; Q4 counts; Moran's I; Cohen's kappa |
| `data/processed/scores/kelurahan_scores.geojson` | Q4 by kota_kab_name; equity_gap by quadrant |
| `data/processed/analysis/lisa_kelurahan.geojson` | LISA cluster counts (LL=254, HH=214) |
