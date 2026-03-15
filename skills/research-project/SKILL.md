---
name: research-project
description: >
  End-to-end skill for graduate research projects that produce BOTH a research paper/thesis
  AND a deployable public-facing product — in parallel, from day one. Use this skill whenever
  a user wants to turn a research idea into something more than just a paper: a working web app,
  a public dataset, a poster, or a product anyone can use. Covers the full journey: research
  framing → scientific methodology → Linear project setup (with parallel paper + product epics)
  → paper writing (intro, lit review, methods, results, discussion) → data pipeline + product
  build (React/Next.js) → paper review → code review → unified deliverables (paper + app +
  dataset + presentation). Trigger this skill when the user mentions "research project",
  "thesis", "graduate research", "research paper", "paper and product", "research prototype",
  "publish a dataset", "research poster", or says they want their research to be usable by
  others beyond the academic context.
---

# Research Project Skill

For graduate research that produces both a paper and a product — evolving in parallel, not
sequentially. The paper explains *why* and *what*. The product makes it *usable* by anyone.

Both tracks share the same methodology and data. Neither is an afterthought.

Linear workflow conventions: `references/linear-workflow.md`.
PRD template: `assets/PRD_Template_Core_Product.docx`.

---

## The Core Idea

Most research stops at the paper. This skill treats the paper and the product as two outputs
of the same research process — with shared methodology, shared data, and shared milestones.

At every phase, ask: **"What does this phase produce for the paper, and what does it produce
for the product?"** Both questions must be answered before moving on.

---

## Phase 0: Detect Starting Point

| Signal | Jump to |
|---|---|
| Raw research idea, nothing written | Phase 1.1 (interview) |
| Has draft RQ, no literature scan | Phase 1.3 (literature scan) |
| Has literature scan, no confirmed framing | Phase 1.3 (refinement loop) |
| Has confirmed framing + source map, no methodology | Phase 2 |
| Has methodology, not in Linear | Phase 3 |
| In Linear, working on paper sections | Phase 4P |
| In Linear, working on data/product | Phase 4D |
| Has drafts to review | Phase 5P or 5D |
| Everything done, assembling deliverables | Phase 6 |

---

## Phase 1: Research Framing

Establish the research context. This phase feeds both the PRD (product framing) and the paper
(academic framing). Produce both documents before moving on.

### 1.1 Interview (if starting from scratch, max 5 questions)
- What is the core problem or question you want to investigate?
- Who is the academic audience (supervisor, conference, journal)?
- Who is the public audience (the people the product will serve)?
- What domain are you in? (urban planning, public health, economics, CS, etc.)
- Do you have any data yet, or is this still exploratory?

### 1.2 Research Framing Document

```
RESEARCH FRAMING
[Project Title]
[Subtitle]

| Field              | Details                                     |
| Researcher         | [Name]                                      |
| Program            | [e.g. Master of Smart Society, Hiroshima U] |
| Supervisor         | [Name, if known]                            |
| Target Venue       | [thesis / conference / journal — TBD ok]    |
| Prototype Audience | [who will use the product]                  |
| Status             | Draft                                       |

## Research Question
[One clear, answerable, falsifiable question]

## Hypothesis
[A specific, testable statement]

## Why this matters
### Academic contribution
[What gap in the literature does this fill?]

### Public / practical contribution
[What real problem does this solve for non-academics?]

## The two outputs
| Output | Description | Audience |
| Research paper | [thesis chapter / conf paper / journal article] | [academic] |
| Web product | [what it does, who uses it] | [general public / practitioners] |

## Scope
- In Scope: [fill in]
- Out of Scope: [fill in]
```

### 1.3 Literature Scan

Run this **after** the draft framing (1.2) and **before** finalising it. The literature
informs the research question — you can't sharpen the question without knowing what's
already been done, and you can't evaluate sources without a question to search around.

**The loop:**
```
Draft RQ (1.2) → Literature scan (1.3) → Refined RQ + confirmed framing → Phase 2
```

#### Search strategy

**Step 1 — Web search** (Claude runs this automatically using web_search):
- Generate 3–5 search queries from the draft research question
- Search Google Scholar, Semantic Scholar, arXiv, and domain-specific sources
- Prioritise: peer-reviewed papers → working papers → high-quality reports
- Scale depth to complexity:
  - Narrow / well-defined RQ → 5–8 papers sufficient
  - Broad / novel / interdisciplinary RQ → 12–20 papers needed
  - Rule of thumb: keep searching until you find 2–3 papers that directly address
    the RQ. If you can't find any, the RQ may be genuinely novel — or too vague.

**Step 2 — User additions** (after web search):
Ask: *"Are there specific papers, reports, or sources you already know are relevant?
You can paste links, DOIs, or upload PDFs."*
- If links/DOIs provided → fetch and extract
- If PDFs uploaded → read and extract
- Merge with web search results, deduplicate

#### Per-paper extraction

For each paper, extract exactly these fields — no more:

| Field | What to capture |
|---|---|
| **Citation** | Author(s), year, title, venue — APA format |
| **Method + findings** | What they did and what they found (2–3 sentences) |
| **Data sources used** | Datasets, APIs, or tools they relied on |
| **Relevance to your RQ** | How directly does this address your question? (High / Medium / Low + 1 sentence why) |

#### Source map output

After extracting all papers, produce a **Source Map** — a structured table plus a
synthesis paragraph:

```
## Source Map

| # | Citation | Method + Findings | Data Sources | Relevance to RQ |
|---|---|---|---|---|
| 1 | [Author, Year. Title. Venue.] | [2–3 sentences] | [datasets/tools] | High — [why] |
| 2 | ... | ... | ... | Medium — [why] |

## Synthesis

### What the literature establishes
[2–3 sentences: what is well-covered, what methods dominate, what data is commonly used]

### The gap your research fills
[1–2 sentences: what is NOT answered — this sharpens the research question]

### Methodological precedents
[Which papers use methods closest to your planned approach? What can you borrow?]

### Data sources to consider
[Datasets or APIs used by existing work that you could also use — feeds directly into Phase 2.3]
```

#### Framing refinement

After the Source Map, revisit the draft framing from 1.2:
- **Research question**: does it need sharpening based on what already exists?
- **Hypothesis**: is it differentiated from existing findings?
- **Academic contribution**: update the "gap" section now that you've seen the field
- **Methodology hints**: note any methods or data sources worth adopting in Phase 2

Update the Research Framing Document (1.2) with any changes before moving on.

#### What the Source Map feeds downstream

| Downstream | What it gets |
|---|---|
| `docs/methodology.md` §Theoretical Framework | Top 3–5 papers as the theoretical foundation |
| E3 (Literature Review epic) | Full source map becomes the raw material for E3 tickets |
| Phase 2.2 (Methodology) | Methodological precedents inform method choices |
| Phase 2.3 (Data requirements) | Data sources used by others inform your acquisition plan |
| `docs/prd.md` §Background | Gap statement feeds Section 3.1 |

---

### 1.4 PRD (Product Requirements Document)

Use the 11-section template in `assets/PRD_Template_Core_Product.docx` as the reference.
For this phase, Sections 1–6 are required; 7–11 optional.

Key differences from a pure product PRD:
- Section 3.1 (Background): use the **gap statement** from the Source Map (1.3)
- Section 4 (Objectives): include both product metrics AND research outcomes
- Section 6 (User Stories): include researcher/analyst personas alongside end-user personas

✋ Confirm framing doc (1.2, updated after 1.3) + Source Map + PRD before moving to Phase 2.

---

## Phase 2: Scientific Methodology

The single methodology that both the paper and the product are built on. Everything here
appears in the paper's Methods section AND drives the product's data layer.

### 2.1 Research Question & Hypothesis (refine from Phase 1)
- **Research Question**: specific, measurable, answerable
- **Hypothesis**: falsifiable statement
- **Analysis Type**: Descriptive / Exploratory / Explanatory / Predictive

### 2.2 Methodology Definition

| Field | Details |
|---|---|
| Analysis Type | [e.g. spatial, time-series, regression, clustering, NLP] |
| Statistical Methods | [e.g. Pearson correlation, OLS, K-means, Gini coefficient] |
| Validation Approach | [e.g. train/test split, cross-validation, expert review] |
| Key Assumptions | [e.g. data is representative, variables are independent] |
| Limitations | [e.g. covers 2020–2024 only, no causal inference] |

### 2.3 Data Requirements & Schema Design

| # | Dataset | Description | Granularity | Format | Required Fields |
|---|---|---|---|---|---|
| 1 | [name] | [description] | [level] | [CSV/API/GeoJSON] | [fields] |

Target schema (cleaned, analysis-ready):

| Field | Type | Description | Source | In paper | In product |
|---|---|---|---|---|---|
| [field] | [type] | [desc] | [source] | ✓ | ✓ |

The last two columns ensure every field is traceable to at least one output.

### 2.4 Data Acquisition Plan

| Dataset | Source | Method | Access | Notes |
|---|---|---|---|---|
| [name] | [URL/institution] | [API/download/scrape] | [open/restricted] | [rate limits, auth] |

Flag restricted datasets — they need synthetic fallbacks for the prototype.

### 2.5 Data Processing & Wrangling Plan

| Step | Operation | Input | Output | Tool |
|---|---|---|---|---|
| 1 | [normalize columns] | raw CSV | cleaned CSV | pandas |
| 2 | [spatial join] | points + polygons | GeoDataFrame | geopandas |
| 3 | [impute nulls] | cleaned CSV | imputed CSV | pandas/sklearn |
| 4 | [compute index] | multiple columns | score column | custom |

- **Missing data strategy**: drop / impute mean / flag / model
- **Outlier strategy**: keep / cap / remove / investigate
- **Join keys**: what links datasets together

### 2.6 EDA Plan

| Check | What to look for | Visualization | In paper | In product |
|---|---|---|---|---|
| Distributions | Skew, outliers, nulls | histogram, boxplot | ✓ | optional |
| Correlations | Key variable relationships | heatmap, scatter | ✓ | ✓ |
| Spatial patterns | Clustering, hotspots | choropleth | ✓ | ✓ |
| Time trends | Seasonality, drift | line chart | ✓ | ✓ |

---

Produce a **Methodology Summary** (1-page condensed) and confirm.

✋ Confirm before moving to Phase 3.

---

## Phase 3: Linear Project Setup

Set up Linear *before* writing or building anything. Read `references/linear-workflow.md`
for exact conventions (statuses, branch names, commit format, PR structure).

### Step 1: Check or create Linear project
Named after the research project title from Phase 1.

### Step 2: Create Epics — two parallel tracks + shared work

**Shared epics (must complete before parallel tracks start):**

| Epic | Name | Covers |
|---|---|---|
| E1 | Research Framing | Phase 1 docs: framing doc, PRD |
| E2 | Methodology & Data Design | Phase 2 docs: methodology, schema, acquisition plan |

**Paper track (parallel with product track):**

| Epic | Name | Covers |
|---|---|---|
| E3 | Literature Review | Related work, theoretical framework, citations |
| E4 | Paper Drafting | Introduction, methods section, results, discussion |
| E5 | Paper Review & Revision | Supervisor feedback, argument quality, citations |

**Product track (parallel with paper track):**

| Epic | Name | Covers |
|---|---|---|
| E6 | Data Pipeline | Acquisition scripts, wrangling, EDA notebook |
| E7 | UI Foundation | Scaffold, styling, layout shell |
| E8 | Core Features | Feature tickets from PRD user stories |
| E9 | Code Review & QA | Review checklist, edge cases, deployment notes |

**Convergence epic:**

| Epic | Name | Covers |
|---|---|---|
| E10 | Deliverables | Paper final draft, published dataset, deployed app, presentation/poster |

Dependency order: E1 → E2 → [E3/E4/E5 ∥ E6/E7/E8/E9] → E10

### Step 3: Ticket template

```
Title: [action-oriented verb phrase]

## Context
[1–2 sentences linking to the Phase/section this comes from]
[Note which track: Paper or Product]

## Acceptance Criteria
- [ ] [specific, verifiable outcome]
- [ ] [another outcome]

## Technical Notes
[Schema fields, API endpoints, library choices, constraints, paper section structure]

## Blocked by
[ticket ID or "none"]
```

### Step 4: Confirm ticket list before creating

Show the full epic + ticket structure and get confirmation first.

### Step 5: Create tickets in Linear

After confirmation: use `save_issue` per ticket. Status = `Todo`.
Priority: P0 → Urgent, P1 → High, P2 → Medium.
Post a setup comment on the project:
> "Linear set up with 10 epics across paper + product tracks. Paper and product run in
> parallel from E3/E6 onward. Converge at E10 for final deliverables."

✋ Confirm before starting Phase 4.

---

## Phase 4P: Paper Writing

Work ticket by ticket through E3–E5. Pull each ticket from Linear before starting.

### Standard paper structure (adapt to venue requirements)

| Section | Paper Track Ticket | Links to |
|---|---|---|
| Abstract | Written last | All sections |
| 1. Introduction | E4 ticket: write introduction | Research framing doc (Phase 1) |
| 2. Related Work | E3 tickets: lit review | Research question + domain |
| 3. Methodology | E4 ticket: write methods section | Phase 2 methodology doc (verbatim basis) |
| 4. Results | E4 ticket: write results | EDA + analysis outputs (Phase 4D) |
| 5. Discussion | E4 ticket: write discussion | Hypothesis from Phase 2 |
| 6. Conclusion | E4 ticket: write conclusion | Research question + contribution |
| References | Ongoing | All citations |

### Writing guidelines

- **Methods section = Phase 2 methodology doc**, rewritten in academic prose. Never diverge.
  If the implementation changed during Phase 4D, update both.
- **Results section** must reference the same data and visualizations used in the product.
  Shared figures reduce effort and ensure consistency.
- **Discussion** must answer the research question stated in Phase 1, and reflect on both
  the academic finding and the practical product implication.
- **Citation management**: note sources inline as `[AUTHOR YEAR]` while drafting; resolve
  to proper format at the end.

### After completing each paper ticket
Post a completion comment on the Linear ticket:

```
**What was written**
- [section name + word count]

**Key decisions**
- [framing choice, argument structure, sources used]

**Handoff notes**
- [what the next section needs from this one]
- [open questions for supervisor review]
```

Set status to `In Review` and tag for supervisor feedback if applicable.

---

## Phase 4D: Data Pipeline + Product Build

Work ticket by ticket through E6–E9. Read `references/linear-workflow.md` for
branch naming, commit format, and PR conventions. Pull each ticket before starting;
set to `In Progress`; branch as `{ticket-id}/{short-description}`.

### Data layer strategy

| Source | Implementation |
|---|---|
| Mock / synthetic | `lib/mock-data.ts` — field names and ranges must match target schema from Phase 2.3 |
| CSV / file upload | `<input type="file">` → `papaparse` → state |
| Live API | `fetch` in `useEffect` with loading/error states; no API keys client-side |
| Database | Out of prototype scope — mock + annotate real integration point |

### UI styling decision (before E7)

Present 3 options:

**Option A — Tailwind + shadcn/ui**: professional, component-rich, best for data dashboards
**Option B — Tailwind only**: flexible, distinctive, good for academic/data-journalism look
**Option C — Tailwind + DaisyUI**: themed presets (corporate, dark, pastel), less boilerplate

Also confirm: dark mode / mobile-responsive / data display style (tables/charts/maps/mixed).
Update E7 tickets with the chosen stack.

### Project file structure (downloadable Next.js)

```
my-app/
├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   └── globals.css
├── components/
│   └── [feature components]
├── lib/
│   ├── mock-data.ts       ← labeled mock data, matching Phase 2.3 schema exactly
│   ├── data-utils.ts      ← wrangling helpers (filter, aggregate, normalize)
│   └── types.ts           ← TypeScript interfaces matching target schema
├── public/
│   └── dataset/           ← cleaned dataset files for public download
├── package.json
└── README.md              ← setup + data pipeline + research context
```

The `public/dataset/` folder is intentional — the product doubles as a dataset distribution
point. Include a `README` inside it linking to the paper.

### Code quality standards
- Components under 150 lines; no `any`; props typed
- Wrangling logic in `lib/` — never inline in components
- Mock data uses realistic values from Phase 2.3 target schema
- Loading, empty, and error states handled
- No hardcoded secrets or API keys

### After completing each product ticket
Post completion comment per `references/linear-workflow.md`:

```
**What was built**
- [bullet list]

**Key files changed**
- `{file}` — {what changed}

**Handoff notes**
- {what the next ticket needs}
- {deviations from spec and why}
```

Atomic commits (Conventional Commits), open PR, post PR URL on ticket.

---

## Phase 5P: Paper Review

Check the draft against these criteria:

### Argument structure
- [ ] Research question from Phase 1 is clearly stated in the introduction
- [ ] Hypothesis is testable and the paper actually tests it
- [ ] Methods section matches Phase 2 methodology exactly
- [ ] Results directly address the hypothesis
- [ ] Discussion connects findings back to the research question
- [ ] Conclusion states the contribution clearly (academic AND practical)

### Academic quality
- [ ] All claims are cited or derived from the data
- [ ] Limitations are acknowledged (from Phase 2.2)
- [ ] Related work situates this research in the field
- [ ] Figures and tables are numbered and referenced in text

### Paper ↔ product consistency
- [ ] Figures used in the paper also appear (or could appear) in the product
- [ ] Data described in the paper is the same data in `lib/mock-data.ts` / `public/dataset/`
- [ ] Any changes to methodology during implementation are reflected in both

Output: **✅ looks good** / **⚠️ minor issue** / **❌ needs fix** — one line + suggested fix.

---

## Phase 5D: Code Review

### Correctness
- [ ] No runtime errors (undefined access, null refs, missing keys)
- [ ] State updates correct (no stale closures, no direct mutation)
- [ ] All PRD user stories from Phase 1 addressed
- [ ] Research question from Phase 2.1 is actually answerable from the UI

### Data layer
- [ ] Mock data field names and types match Phase 2.3 schema exactly
- [ ] Wrangling logic correct and isolated in `lib/`
- [ ] `public/dataset/` contains the cleaned dataset with a README

### Code quality
- [ ] Components under 150 lines; no `any`; props typed
- [ ] Wrangling helpers in `lib/`, not inline

### UX
- [ ] Loading / empty / error states handled
- [ ] Charts/tables correct with edge case data (nulls, empty arrays)
- [ ] Non-technical users can understand what the product shows

### Linear hygiene
- [ ] All E6–E9 tickets Done or In Review
- [ ] Completion comments posted with handoff notes
- [ ] PRs opened and URLs posted on tickets

Output: **✅ / ⚠️ / ❌** — one line + fix per item.

---

## Phase 6: Deliverables

Assemble all outputs and check completeness before submission.

### Paper
- [ ] All sections complete, reviewed (Phase 5P), and supervisor-approved
- [ ] References in required citation format (APA / IEEE / ACM — check venue)
- [ ] Abstract written last, reflects actual contribution
- [ ] Figures match those in the product

### Dataset
- [ ] Cleaned dataset in `public/dataset/` with field descriptions
- [ ] `README.md` inside dataset folder: field glossary, source citations, license
- [ ] License selected (CC BY 4.0 recommended for open research data)

### Web product
- [ ] Deployed (Vercel / Netlify recommended for Next.js)
- [ ] Links to the paper and dataset from the app's About or footer
- [ ] `README.md` includes research context, not just setup instructions

### Presentation / poster
When preparing a presentation or poster, structure it to bridge both audiences:

**Academic poster structure** (A0 / conference format):
```
[Title + authors]
[Research question + hypothesis]    [Key finding + figure from product]
[Methodology summary]               [Product screenshot + QR code]
[Results + key chart]               [Conclusion + future work]
[References]
```

**Slide deck structure** (10–12 slides):
1. Problem (1 slide — for both academics and practitioners)
2. Related work (1–2 slides)
3. Research question + hypothesis (1 slide)
4. Methodology (1–2 slides)
5. Results (2–3 slides — use product screenshots as figures)
6. Discussion + limitations (1 slide)
7. Product demo (1 slide — QR code or live demo)
8. Conclusion + future work (1 slide)

The product demo slide is non-negotiable. Show it. It makes your research tangible.

### Linear close-out
- [ ] All E1–E10 tickets Done or Canceled (with reason)
- [ ] Final comment on project with links: paper URL, dataset URL, deployed app URL

---

## General Principles

- **Paper and product are co-equal outputs.** Neither is the "real" output. The paper without
  the product is inaccessible. The product without the paper is ungrounded. Both together
  is the contribution.
- **Shared methodology means shared data.** If you change the wrangling logic in Phase 4D,
  the paper's Methods section must be updated too. They are not separate documents.
- **Public by default.** The dataset should be publishable (open license). The product should
  be deployable. Design for this from Phase 1.
- **Science first, then UI.** Don't scaffold the product until the methodology is confirmed.
- **Linear before code.** Set up epics and tickets before writing or building anything.
- **Iterate.** After each phase, invite feedback before moving forward.
- **PRD template** at `assets/PRD_Template_Core_Product.docx` — reference for formatting
  or produce a `.docx` on request.
- **Linear conventions** in `references/linear-workflow.md` — branch names, commits, PRs,
  and completion comments must follow this exactly.

---

## Living Documentation System

The project maintains 7 docs in `docs/`. Each has a volatility tier that determines when
Claude updates it. Templates for all docs are in `references/docs/*.template`.

### Doc inventory

| File | Volatility | Updated | Purpose |
|---|---|---|---|
| `docs/state.md` | **Volatile** | Auto — every session | Current state, active ticket, blockers, next action |
| `docs/EPICS_TASKS.md` | **Volatile** | Auto — when ticket statuses change | Full epic/task breakdown with ACs, dependencies, estimates |
| `docs/ROADMAP.md` | **Volatile** | Auto — when timeline or status changes | Delivery timeline, milestones, weekly focus, risks |
| `docs/methodology.md` | Stable | Only when methodology changes | RQ, hypothesis, methods, data pipeline |
| `docs/ARCHITECTURE.md` | Stable | Only when system structure changes | Tech stack, directory structure, data flow, deployment |
| `docs/DATA_MODEL.md` | Stable | Only when schema changes | Full schema, field definitions, wrangling map, mock data spec |
| `docs/prd.md` | Stable | Only when product definition changes | What we're building, why, for whom, constraints |

### Update rules

**At the START of every session** — Claude must:
1. Read `docs/state.md` first — this is the context bootstrap, not the codebase
2. Read `docs/EPICS_TASKS.md` to find the current active ticket
3. Proceed directly to the active ticket — no codebase re-scan needed

**At the END of every session** — Claude must always update:
1. `docs/state.md` — what was done, current focus, next action
2. `docs/EPICS_TASKS.md` — all ticket statuses touched this session
3. `docs/ROADMAP.md` — milestone and weekly status if anything changed

**For stable docs** — update only when content actually changed:
- `docs/methodology.md` → if methods, schema, or wrangling logic changed
- `docs/ARCHITECTURE.md` → if new components, routes, integrations, or env vars were added
- `docs/DATA_MODEL.md` → if schema fields were added, removed, renamed, or retyped
- `docs/prd.md` → if scope, features, personas, or constraints changed

When updating a stable doc, add a note to the Linear ticket comment:
> `docs/[filename].md updated — [what changed and why]`

### Generating docs for a new project

When setting up Phase 3, generate all 7 docs from templates:

```bash
cp references/docs/*.template docs/
for f in docs/*.template; do mv "$f" "${f%.template}"; done
```

Fill each doc from confirmed Phase 1 and Phase 2 outputs:
- `prd.md` ← Phase 1.3 PRD
- `methodology.md` ← Phase 2 Methodology Summary
- `EPICS_TASKS.md` ← Phase 3 Linear epic/ticket structure
- `ROADMAP.md` ← Phase 3 milestone dates
- `ARCHITECTURE.md` ← Phase 4D initial scaffold decisions
- `DATA_MODEL.md` ← Phase 2.3 target schema
- `state.md` ← generated fresh after first session

### state.md is the session handshake

Every session starts by reading `docs/state.md`. It tells Claude:
- What was just done (skip re-reading completed code)
- The active ticket and branch (jump straight in)
- Any blockers (surface immediately, don't discover mid-session)
- Open questions (raise before starting work)

If `docs/state.md` doesn't exist, generate it from `references/docs/state.md.template`
before doing anything else.
