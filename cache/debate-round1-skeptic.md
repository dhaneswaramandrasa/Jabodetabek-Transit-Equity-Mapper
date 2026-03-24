# Round 1 — Skeptic

**Role**: Find the strongest counterargument to each novelty claim. Identify the closest prior paper. Argue where the claimed gap is overstated, incremental, or definitional. Do NOT concede without specific evidence to the contrary.

---

## Gap #1: No composite need-vs-access (TNI–TAI) equity gap framework has been applied to the full Jabodetabek metropolitan region at kelurahan resolution.

**Verdict: Overstated — the gap is primarily geographic, not methodological. The TNI–TAI framework is already well-established in developing-country megacities.**

The closest prior work is Andani et al. (2025), published September 2025, which performs multi-modal job accessibility evaluation for Jakarta at kecamatan level using Gini coefficient and Theil index, explicitly stratifying by income group across car, motorcycle, and public transport modes. This study covers DKI Jakarta's kecamatan tier — directly adjacent to the kelurahan tier claimed as novel. More critically, Pereira et al. (2019) applied distributional equity analysis with GTFS routing to Rio de Janeiro — a developing-country megacity of comparable scale (~13M) — and produced income-stratified equity maps that structurally resemble what this research proposes. Delmelle and Casas (2012) did the same for Cali's BRT.

The claim that "no composite need-vs-access framework has been applied to Jabodetabek" reduces primarily to a geographic novelty claim: the same methods exist, they simply have not been applied to this particular city-region. Geographic novelty is the weakest form of scholarly contribution. The peer-reviewed literature already has need-supply gap frameworks (Currie 2010), transit desert operationalization at metropolitan scale (Jiao & Dillivan 2013; Jomehpour & Smith-Colin 2020), and composite accessibility indices for developing countries (Rathod et al. 2025). The kelurahan resolution is also not genuinely novel — it is simply the finest available administrative unit in Indonesian census data, which any researcher applying this framework to Indonesia would naturally use.

The honest framing is: this is an **application study** — the methodological apparatus is imported wholesale from the Western/Latin American literature and applied to a new geographic context. That has value, but claiming a "gap" in the framework itself is misleading when the gap is really "nobody bothered to do this in Jabodetabek yet."

---

## Gap #2: No study has systematically compared the same transit equity gap framework at two resolutions — administrative (kelurahan) vs. uniform hexagonal (H3 res 8) — within a single metropolitan area to expose MAUP effects.

**Verdict: Weakly overstated — MAUP in transit equity is already demonstrated; the H3-specific framing is incremental.**

Javanmard et al. (2023) is the direct prior art. That paper explicitly tests MAUP effects on transit equity conclusions at multiple aggregation levels (stop, route, neighborhood) in Winnipeg, and its core finding — that scale choice changes whether transit appears equitable or inequitable — is exactly the phenomenon this research claims to discover. The fact that Javanmard et al. used administrative tiers (stop → route → neighborhood) rather than administrative vs. hexagonal grids is a methodological variant, not a conceptual gap.

The claim that H3 hexagons are uniquely revealing versus administrative boundaries has a strong prior: the general literature on MAUP (originating from Openshaw 1984, well-established by 2023) already demonstrates that uniform areal units reduce boundary-induced artifacts. Using H3 as the uniform comparator is a sensible implementation choice, but it is not a theoretical advance. Numerous spatial analysis studies across urban planning use equal-area tessellations (fishnet grids, hexagonal grids) versus administrative units for precisely this reason — this is standard practice in spatial epidemiology and crime analysis.

Furthermore, Andani et al. (2025) itself acknowledges spatial granularity limitations at the kecamatan tier and calls for finer-grained analysis — which means a kelurahan-level study would be seen as an incremental resolution improvement rather than a novel dual-resolution framework. The research can reasonably claim to be the **first to use H3 hexagons specifically** for Jabodetabek transit equity, but it cannot claim the MAUP insight itself as novel. That insight belongs to Javanmard et al. (2023) and decades of spatial analysis literature before it.

---

## Gap #3: No existing study embeds counterfactual infrastructure placement (what-if: add a transit node here) directly into a transit equity quadrant classification to measure the shift in equity scores.

**Verdict: Partially valid but overstated — scenario simulation and before-after analysis in equity frameworks are well-established; the specific integration is incremental, not transformative.**

The claim mischaracterizes the state of the literature. Pereira et al. (2019) explicitly performs a before-and-after comparison of Rio's transit investments (BRT and metro lines) against equity outcomes — measuring which income groups gained accessibility. That is structurally a counterfactual analysis: "what if these lines had not been built?" maps directly onto "what if a new node were placed here?" The difference is that Pereira et al. used real infrastructure changes rather than simulated ones, but the analytical logic is identical: recompute accessibility with changed infrastructure, compare equity metrics before and after.

Jomehpour and Smith-Colin (2020) integrates transit desert identification with scenario-like framing for intervention prioritization. Gelb and Alizadeh (2025) develop a vertical equity diagnostics toolbox explicitly designed to evaluate interventions — their toolbox is built for "what does this policy change do to equity?" questions. The claim that no study "embeds" scenario simulation within a quadrant framework is a definitional sleight of hand: it requires that the scenario be embedded in the quadrant classification itself (rather than run alongside it), and that the quadrant shift be the measured outcome. This is a presentation-layer distinction, not a methodological one.

More critically, the scenario in H3 is a single simulated node — not a full infrastructure evaluation. The counterfactual "add one transit node here" is closer to sensitivity analysis than to genuine scenario planning. The contribution is real but modest: it demonstrates that the quadrant framework can be used as a prioritization input for planners. Claiming this constitutes a gap in the literature overstates how novel it is when accessibility scenario modeling has been standard practice in transport planning for decades (e.g., LUTI models, transport appraisal tools).

---

## Gap #4: No study integrates a full three-mode generalized cost model (transit vs. car vs. motorcycle) as a named composite index layer within a transit equity gap framework.

**Verdict: The strongest claim, but weaker than presented — three-mode cost modeling for Jakarta already exists in Andani et al. (2025), and the "named composite index layer" framing is architectural rather than conceptual.**

Andani et al. (2025) — published September 2025, post-dating the project's literature scan — evaluates job accessibility in Jakarta across car, motorcycle, and public transport modes explicitly, using Gini and Theil to compare equity across modes. Its key finding (motorcycles provide the most equitably distributed access for low/medium-income groups) directly addresses the motorcycle-vs-transit competition framing that this research claims as novel. While Andani et al. does not call it a "generalized cost model" with formal cost components (time, fare, fuel cost), the functional comparison is the same: assessing whether transit serves residents better or worse than motorcycle across the accessibility distribution.

Ng (2018) provides the behavioral foundation: motorcycle dominance in Jakarta/Bangkok/Manila is explained by low operating cost, congestion flexibility, and poor transit first/last-mile — which is precisely what a generalized cost comparison formalizes. Sukor and Bhayo (2024) models modal shift from motorcycle to transit, which inherently requires comparing the full cost of both modes. The literature has been doing three-mode comparisons; what this research adds is formalizing it as a specifically-weighted layer (L5 = 15% of TAI) within a composite index.

The genuine question is whether that architectural choice — making three-mode cost comparison an explicit, named layer within the TAI formula — constitutes a "gap" or a design decision. It is a good design decision for the Southeast Asian context, but calling it a literature gap risks overstating the contribution. The more defensible framing is: existing studies compare modes for accessibility but do not incorporate this comparison as a weighted component of a composite transit accessibility index used for equity gap classification. That is incremental but real.
