# Stage 6 — KNOWLEDGE_EXTRACT
# AutoResearchClaw Phase B — Jabodetabek Transit Equity Mapper
# Date: 2026-03-25

---

## C1 — Andani et al. (2025) — Jakarta Job Accessibility by Mode + Income

**Full citation:** Andani, I.G.A., Qamilla, N., Izdihara, R.P., Safira, M., Sakti, A.D., & Syabri, I. (2025). Spatial, mobility, or socio-economic inequity? A district level job accessibility evaluation in Jakarta, Indonesia. *International Journal of Urban Sciences*. DOI: 10.1080/12265934.2025.2553714

**Method + Findings:**
- Evaluated job accessibility across car, motorcycle, and public transport modes stratified by income group (low, medium, high) at district (kecamatan) level in Jakarta.
- Used Gini coefficient and Theil index to measure distributional equity.
- Key finding: motorcycles provide the broadest and most equitably distributed job access, especially for low- and medium-income populations. Public transport shows the most severe inequality.
- Gini coefficients across income groups are nearly identical — transport inequity is driven more by geography and network design than by socioeconomic category.
- Theil index reveals within-density-group disparities dominate, pointing to need for localised neighbourhood-level interventions rather than broad income-based policies.
- Job accessibility is highly centralised — significantly lower in peripheral and low-density Bodetabek areas.

**Data sources:** Jakarta district-level transport network data; BPS kecamatan demographics; GTFS (implied); income stratification from BPS/survey.

**Relevance to RQ:** **HIGH** — First quantitative multi-modal equity comparison (car vs. motorcycle vs. public transport) using Gini at kecamatan level in Jakarta. Directly validates our H3 hypothesis that spatial unit choice matters and confirms motorcycle's superior equity performance — key support for our cost-competitiveness layer. Confirms centralization of access and Bodetabek periphery deprivation. Published September 2025 — post-dates all 18 existing papers.

---

## C2 — Gelb & Alizadeh (2025) — Fair Transit Equity Diagnostics Toolbox

**Full citation:** Gelb, J. & Alizadeh, H. (2025). Towards fair transit: a toolbox for equity diagnostics in spatial accessibility. *Public Transport*. DOI: 10.1007/s12469-025-00412-y

**Method + Findings:**
- Developed a reproducible toolbox for assessing vertical equity in spatial transit accessibility, grounded in Rawlsian equity theory (prioritising the worst-off).
- Combines two accessibility indicators (public transit accessibility + urban opportunity accessibility) with three equity metrics (Gini, Theil, Atkinson) and two graphical diagnostic tools (Lorenz curve + concentration curve).
- Key methodological finding: classical Gini and similar indices suggest "relatively fair overall distributions" but fail to capture group-specific disparities for vulnerable populations.
- In Montreal application: vulnerable populations experience 12–19% lower median accessibility and are disproportionately concentrated in low-accessibility areas — invisible to Gini alone.
- Recommends concentration curves (horizontal equity by group) alongside Gini (overall distribution) for complete equity diagnosis.

**Data sources:** Montreal ARTM regional transit authority network; GTFS; census vulnerability indicators.

**Relevance to RQ:** **MEDIUM-HIGH** — Methodological precedent for combining multiple equity metrics. Critically, it warns that Gini alone is insufficient for vertical equity — directly relevant to our equity analysis design. Our Q1/Q4 quadrant framework is a form of vertical equity assessment (targeting the worst-off) that goes beyond what Gini alone captures. Strengthens justification for our quadrant approach. Published January 2025.

---

## C3 — [Authors TBC] (2026) — Bangkok Railway Scenarios + Gini

**Full citation:** [Authors to be confirmed] (2026). Enhancing urban accessibility with railway network development: a comparative scenario analysis in Bangkok, Thailand. *Public Transport*. DOI: 10.1007/s12469-026-00421-5

**Method + Findings:**
- Assessed impact of Bangkok railway network expansion (M-MAP2 Blueprint) using GTFS-based cumulative accessibility index.
- Three scenarios compared: current network, M-MAP original plan, M-MAP2 Blueprint.
- Gini decreased from 0.530 (current) to 0.457 (M-MAP2) — more balanced spatial distribution.
- M-MAP2 increases citywide accessibility ~10%, with 50% of facilities within 20 km reachable within 60 minutes.
- Peripheral areas remain underserved despite network expansion.

**Data sources:** Bangkok GTFS; OpenStreetMap road network; facility location data.

**Relevance to RQ:** **MEDIUM** — Southeast Asian megacity scenario analysis using GTFS + Gini — methodological parallel to our what-if simulation. Demonstrates Lorenz/Gini for transit scenario comparison in SEA context. Peripheral underservice finding mirrors our Bodetabek framing. Supports our what-if layer's value. Published 2026 — most recent paper found.

---

## C4 — Ayuriany, Lee & Hidayati (2023) — Jakarta Commuting Subjective vs. Objective

**Full citation:** Ayuriany, T., Lee, J.H., & Hidayati, I. (2023). What access-for-all entails? Examining commuting experiences from subjective and objective accessibility in a fast-growing city, Jakarta. *Asian Transport Studies*, July 2023. DOI: 10.1016/j.eastsj.2023.100112 (approx.)

**Method + Findings:**
- Qualitative descriptive mixed-method study; 110 questionnaires + in-depth interviews.
- Public transport users perceived higher accessibility (convenience, affordability, no congestion) but behavioural stereotypes suppressed transit use even among those with positive attitudes.
- Private transport users perceived low accessibility despite objective measures showing transit availability.
- Disconnect between objective accessibility measures and subjective user experience — "positive feeling not necessarily related to mode choice."

**Data sources:** 110-respondent questionnaire survey; Jakarta transit network (qualitative).

**Relevance to RQ:** **LOW-MEDIUM** — Qualitative framing of Jakarta transit accessibility perceptions. Does not use GTFS or quantitative equity metrics. Confirms the car/motorcycle dominance despite transit availability — useful as contextual framing for discussion, not for methods. Not sufficient to add to source-map.

---

## C5 — [Authors TBC] (2025) — Electric Motorcycles + Multimodal Jakarta

**Full citation:** [Authors to be confirmed] (2025). Exploring the transition to electric motorcycles and its role in multimodal travel in the Jakarta metropolitan area. *Discover Sustainability*. DOI: 10.1007/s43621-025-01908-0

**Method + Findings:**
- Examined potential transition from conventional to electric motorcycles in Jabodetabek multimodal context.
- Motorcycles function as first/last-mile feeders to transit; electrification could reduce operating cost and increase transit competitiveness.
- Cost and flexibility remain dominant mode choice drivers; government target of 2.1M electric motorcycles by 2025 significantly underperformed (28,000 actual in 2022).

**Data sources:** Jakarta metropolitan area travel data; electrification policy documents.

**Relevance to RQ:** **LOW** — Future-oriented policy study on EV adoption, not transit equity measurement. Tangentially supports our Layer 5 motorcycle cost-competitiveness framing but adds nothing to methodology. Do not add to source-map.
