# Hypothesis Theory Assessment — MVP-87 Agent Theory
*Role: theoretical evaluator — assessing from methodology.md predictions only*
*Data outputs NOT consulted during this assessment*
*Source: docs/methodology.md §2.1, §2.1b, §2.1c, §2.2*
*Generated: 2026-03-28*

---

## H1 — Spatial Mismatch

**Theoretical prediction**: Areas classified as Q4 ("High Need, Low Access") are
disproportionately concentrated in the suburban peripheries of Bodetabek (Bogor,
Depok, Tangerang, Bekasi), while Q1 ("Low Need, High Access") areas cluster in
central Jakarta. This prediction follows from the Need-Supply Gap Framework
(Currie 2010; Jiao & Dillivan 2013): transit investment has historically concentrated
in the DKI Jakarta core along trunk corridors (MRT NS, KRL Manggarai hub, Busway
corridors), while peripheral suburban areas that have grown rapidly through
urbanisation remain underserved. Transit-dependent populations (low income, zero-vehicle
households, high dependency ratios) are increasingly displaced outward from Jakarta
due to housing costs, making the mismatch spatially predictable.

**PROCEED threshold**: Q4 ≥ 60% of units concentrated in Bodetabek periphery (outer
municipalities: Kota Bogor, Kab. Bogor, Kota Depok, Kota Tangerang, Kab. Tangerang,
Kota Tangerang Selatan, Kota Bekasi, Kab. Bekasi). Equivalently: the geographic centroid
of Q4 units falls clearly outside DKI Jakarta boundary, and Moran's I LISA clusters of
Q4 are statistically significant and spatially coherent in the periphery.

**REFINE threshold**: Q4 40–60% in Bodetabek — partial support. The mismatch exists
but is less pronounced than expected; Q4 units appear in both Jakarta inner-ring areas
(North Jakarta kampungs, East Jakarta industrial corridors) and Bodetabek periphery.
This would suggest the mismatch is real but spatially diffuse — requiring reframing from
"suburban periphery" to "multi-ring spatial inequality."

**PIVOT threshold**: Q4 < 40% in Bodetabek, or Q4 distribution is roughly uniform
across all municipalities, or Q4 clusters significantly inside DKI Jakarta (e.g.,
concentrated in North/East Jakarta). PIVOT would imply the transit desert is an inner-city
problem (dense but unserved pockets), not a suburban periphery problem — contradicting
the central claim of H1 and requiring fundamental reframing of the spatial narrative.

**Theoretical verdict**: PROCEED (theoretical confidence — pending data confirmation)

**Confidence**: High

**Rationale**: The theoretical prediction is well-grounded in three independent lines
of evidence. First, the spatial geography of Jabodetabek makes the mismatch structurally
predictable: transit trunk lines were built inward-facing (KRL star topology, MRT NS
corridor), and Bodetabek growth has outpaced infrastructure extension. Second, the
Need-Supply Gap literature (Currie 2010; Jiao & Dillivan 2013) consistently finds
this pattern in radial metro systems in middle-income cities. Third, existing Jakarta-specific
studies (Hardi & Murad 2023; BPTJ regional reports) document low BRT/KRL penetration
in outer municipalities. The 60% threshold is conservative relative to theoretical
expectation; the prediction would be falsified only if transit investment has been
more equalizing than the literature suggests.

---

## H2 — Resolution Effect

**Theoretical prediction**: The dual-resolution comparison reveals that kelurahan-level
Gini analysis systematically underestimates equity gaps compared to H3 hexagonal
analysis. Large, heterogeneous kelurahan in suburban areas average over both well-served
and underserved sub-units, producing a compressed Gini. H3 hexagons (uniform 0.74 km²
cells) expose the within-kelurahan variation that administrative boundaries suppress.
This prediction is directly derived from the MAUP sensitivity literature: Javanmard et al.
(2023) demonstrated empirically that spatial unit choice substantively alters equity
conclusions in transit analysis. In Jabodetabek specifically, kelurahan area variance is
extreme (0.5–50 km²) — large peripheral kelurahan are most susceptible to within-unit
averaging, precisely where transit inequity is highest (H1 predicted).

**PROCEED threshold**: Gini_H3 > Gini_kelurahan (any positive delta, i.e., Gini_H3
is larger than Gini_kelurahan, indicating that finer resolution reveals greater
distributional inequality). The magnitude expected is Gini_H3 − Gini_kelurahan > 0.03
based on MAUP literature showing 5–15% Gini inflation at finer scales. Cohen's kappa
for quadrant agreement between the two resolutions should be moderate (0.40–0.70),
indicating meaningful but not random disagreement — systematic disagreement where large
kelurahan contain mixed H3 quadrant classes.

**REFINE threshold**: |Gini_H3 − Gini_kelurahan| < 0.01 — the two resolutions produce
nearly identical distributional inequality estimates. This would suggest Jabodetabek's
kelurahan are internally homogeneous enough that the MAUP effect is weak, or that the
TAI composite itself smooths over fine-grained variation. Reframing required: resolution
does not materially change equity conclusions.

**PIVOT threshold**: Gini_H3 < Gini_kelurahan — finer resolution actually produces
lower measured inequality than administrative units. This would contradict both MAUP
theory and H2's direction of effect, suggesting administrative units are amplifying
rather than masking inequity (possible if administrative boundaries were drawn to
segregate low-access areas). This outcome would require fundamental reframing of the
resolution comparison's interpretation.

**Theoretical verdict**: PROCEED (theoretical confidence — pending data confirmation)

**Confidence**: High

**Rationale**: H2 is the most theoretically secure of the three hypotheses because it
rests on a well-established empirical regularity (MAUP; Javanmard et al. 2023) and
the specific structural conditions in Jabodetabek strongly favour the predicted
direction. The extreme variance in kelurahan area (0.5–50 km²) is the key driver:
very large suburban kelurahan are guaranteed to contain heterogeneous sub-units across
the access spectrum. The only theoretical path to PIVOT would require kelurahan
boundaries to have been drawn along high-equity-variation lines — unlikely given that
Indonesian administrative boundaries were drawn for governance, not for internal
homogeneity of infrastructure service.

---

## H3 — Scenario Validation

**Theoretical prediction**: Simulating a new transit node in a Q4 ("High Need, Low Access")
zone produces a larger equity score improvement (delta_Equity_Gap_Score) than the same
intervention in a Q1 or Q2 ("Low Need, High Access") zone, validating the quadrant
framework as a planning prioritization tool. This prediction follows from the mathematical
structure of the Equity Gap Score (EGS = TNI − TAI, normalized): a unit with high TNI
and low TAI has maximum room for improvement in TAI — any new transit node raises TAI
from a low base, producing a large delta. A Q1 unit with low TNI and already-high TAI
is near ceiling — the same node produces a smaller TAI increment because the formula
is bounded at 1.0 and the area is already well-served. The transit desert identification
literature (Jomehpour & Smith-Colin 2020) supports this: interventions in underserved
areas produce larger system-wide equity improvements per infrastructure dollar.

**PROCEED threshold**: Q4 improvement > 1.5× Q1/Q2 improvement, where improvement
is measured as delta_Equity_Gap_Score = |EGS_baseline − EGS_simulated|. The 1.5×
threshold is meaningful (not marginal) and corresponds to the theoretical expectation
that the TAI increment from a new node is larger when the baseline TAI is in the
lower half of the distribution (because the normalization is sensitive to floor effects
in areas with near-zero accessibility). Cohen's kappa or quadrant membership shift
counts should also show more Q4 units exiting the Q4 quadrant than Q1 units moving
to a better quadrant.

**REFINE threshold**: Q4 improvement 1.0–1.5× Q1/Q2 improvement — the direction
of effect is correct (Q4 improves more) but the magnitude is not strongly
differentiating. This could occur if the simulated node is placed in a location where
the isochrone coverage is limited (e.g., no GTFS routing improvement because the node
is modeled as a simple proximity buffer). Reframing: the framework is directionally
valid but the simulation method (simplified buffer model, per methodology.md limitations)
may not be sensitive enough to demonstrate a strong effect.

**PIVOT threshold**: Q4 improvement ≤ Q1/Q2 improvement — the new node in the transit
desert produces no greater equity gain than the same node in an already-served area.
This would directly invalidate the quadrant framework as a prioritization tool and
require fundamental reframing of the scenario analysis. The most plausible mechanism
for this outcome: the simulated node is placed in a Q4 area that has such poor first-mile
infrastructure (L1 = very low) that even a new station does not materially change TAI —
the first-mile bottleneck absorbs the improvement. PIVOT would therefore not necessarily
mean the quadrant framework is wrong, but that the simulation method does not adequately
model the real-world constraints.

**Theoretical verdict**: PROCEED (theoretical confidence — pending data confirmation)

**Confidence**: Medium

**Rationale**: H3 is theoretically well-founded but has the weakest theoretical
confidence of the three, for two reasons. First, the scenario simulation is explicitly
described in methodology.md as a "simplified buffer/isochrone model" — not a full
transit assignment model — which may not be sensitive enough to detect TAI improvements
at the margin. Second, the outcome depends on the specific placement of the simulated
node: if the scenario design places the Q4 node in a maximally deprived area while
the Q1 comparison node is placed in an already-saturated area, the differential will
be large; if both placements are near the median of their quadrant distributions, the
1.5× threshold may not be reached. The theoretical direction of effect is robust, but
the magnitude threshold is sensitive to scenario design choices.

---

## Overall Theory Verdict

| Hypothesis | Description | Theory Verdict | Confidence | MVP-14 Gate (theory alone) |
|------------|-------------|---------------|------------|---------------------------|
| H1 | Spatial mismatch — Q4 concentrated in Bodetabek periphery | PROCEED | High | Clear (theory) |
| H2 | Resolution effect — Gini_H3 > Gini_kelurahan | PROCEED | High | Clear (theory) |
| H3 | Scenario validation — Q4 delta > 1.5× Q1/Q2 delta | PROCEED | Medium | Conditional (simulation sensitivity) |

**Note**: All three hypotheses receive theoretical PROCEED verdicts. However, theory alone
cannot gate MVP-14 — the Stats assessment (Agent Stats) must confirm with actual data.
The critical gate is the Reconciler's synthesis of both assessments. H3's medium confidence
means it carries the highest risk of REFINE or PIVOT when real data is available.
