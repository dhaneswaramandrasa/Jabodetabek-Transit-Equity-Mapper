# CLAUDE.md — Research Project

This repo produces two co-equal outputs: a **research paper** and a **deployable web product**.
They evolve in parallel, share the same methodology and data, and converge into a single
deliverable bundle. Neither is an afterthought.

You are operating in **Claude Code (terminal)**. This means:
- You have full repo access — read and write files directly
- You manage git: branch, commit, push, open PRs
- You maintain the `docs/` system automatically
- You do not re-scan the codebase at the start of each session — you read `docs/state.md` instead

---

## On Session Start

Do this at the start of **every** session, before anything else:

```
1. Read docs/state.md
2. Read docs/EPICS_TASKS.md — find the active ticket
3. Say: "Resuming [TICKET-ID] — [title]. Last action: [from state.md]. Ready."
4. If docs/state.md doesn't exist → generate it from docs/templates/state.md.template
```

Do not scan the full codebase. Do not ask "where were we?" — `docs/state.md` tells you.

---

## On Session End

Do this at the end of **every** session, before closing:

```
1. Update docs/state.md — what was done, current focus, next action
2. Update docs/EPICS_TASKS.md — all ticket statuses touched this session
3. Update docs/ROADMAP.md — if any milestone or weekly status changed
4. Check stable docs — update only if content actually changed:
   - docs/methodology.md   → if methods, schema, or wrangling logic changed
   - docs/ARCHITECTURE.md  → if components, routes, integrations, or env vars changed
   - docs/DATA_MODEL.md    → if schema fields were added, renamed, or retyped
   - docs/prd.md           → if scope, features, personas, or constraints changed
5. If a stable doc was updated, note it in the Linear ticket comment:
   docs/[filename].md updated — [what changed and why]
6. Commit all doc updates: docs(project): update session docs — [date]
```

---

## Docs System

Seven living docs in `docs/`. Templates in `docs/templates/`.

| File | Volatility | Purpose |
|---|---|---|
| `docs/source-map.md` | Stable | Literature scan: papers, synthesis, gap statement |
| `docs/state.md` | **Auto every session** | Current state, active ticket, blockers, next action |
| `docs/EPICS_TASKS.md` | **Auto on status change** | Epics, tasks, ACs, dependencies, estimates |
| `docs/ROADMAP.md` | **Auto on timeline change** | Milestones, weekly plan, risks |
| `docs/methodology.md` | Stable | RQ, hypothesis, methods, data pipeline |
| `docs/ARCHITECTURE.md` | Stable | Stack, directory structure, data flow, deployment |
| `docs/DATA_MODEL.md` | Stable | Schema, field definitions, wrangling map, mock data spec |
| `docs/prd.md` | Stable | What we're building, why, for whom, constraints |

### Bootstrap a new project

Run once when setting up a new repo:

```bash
mkdir -p docs
cp docs/templates/*.template docs/
for f in docs/*.template; do mv "$f" "${f%.template}"; done
```

Then fill each doc from the confirmed Phase 1 and Phase 2 outputs:
- `prd.md` ← Phase 1 PRD (drafted in Claude for Mac)
- `methodology.md` ← Phase 2 methodology summary
- `EPICS_TASKS.md` ← Phase 3 Linear epic/ticket structure
- `ROADMAP.md` ← Phase 3 milestone dates
- `ARCHITECTURE.md` ← fill after Phase 4D scaffold
- `DATA_MODEL.md` ← Phase 2.3 target schema
- `state.md` ← generate fresh after first session

---

## Linear Workflow

Full conventions in `docs/references/linear-workflow.md`. Summary:

### Before starting any ticket
```
1. Pull ticket: get_issue {TICKET-ID}
2. Read previous ticket's comments for handoff notes
3. Set status → In Progress
4. Create branch: git checkout -b {ticket-id}/{short-description}
   (branch off main unless ticket is blocked by unmerged branch — then branch off that)
```

### While working
- Add implementation notes as Linear comments
- If a blocker is found: comment with details, leave status In Progress

### After completing a ticket
```
1. Run any API tests listed in the ticket
2. Post completion comment on Linear ticket:

   **What was done**
   - [bullet]

   **Key files changed**
   - `path/to/file` — what changed

   **Handoff notes**
   - what the next ticket needs to know
   - any deviations from spec and why

3. Atomic commits — Conventional Commits format:
   feat(scope): description
   fix(scope): description
   refactor(scope): description
   docs(scope): description

4. Set status → In Review (needs human review) or Done (self-contained)
5. Push branch, open PR to main:
   Title: [{TICKET-ID}] {ticket title}

   ## Overview
   {1–2 sentences}

   ## Changes
   - `file` — what changed

   ## Testing
   - step-by-step verification

   ## Linear
   {ticket URL}

6. Post PR URL as follow-up comment on the Linear ticket
```

---

## Phase 0: Detect Where You Are

Read `docs/state.md` and `docs/EPICS_TASKS.md`, then jump to the right phase:

| Signal | Phase |
|---|---|
| `docs/` doesn't exist | Bootstrap docs, then Phase 1.1 |
| Has draft RQ, no literature scan | Phase 1.3 (literature scan) |
| Has literature scan, no confirmed framing | Phase 1.3 (refinement loop) |
| Has confirmed framing + source map, no methodology | Phase 2 |
| Methodology confirmed, no Linear setup | Phase 3 |
| Linear set up, paper tickets active | Phase 4P |
| Linear set up, product tickets active | Phase 4D |
| Code or paper drafts need review | Phase 5P / 5D |
| All tickets done | Phase 6 |

---

## Phase 1: Literature Scan (if not done yet)

Phases 1.1–1.2 (interview + draft framing) are typically done in Claude for Mac.
If arriving at the terminal with a draft RQ but no Source Map yet, run the scan here.

### The loop
```
Draft RQ → Literature scan → Source Map → Refined framing → Phase 2
```

### Step 1 — Web search
Generate 3–5 search queries from the draft RQ. Search Google Scholar, Semantic Scholar,
arXiv, and domain-specific sources. Scale depth to complexity:
- Narrow / well-defined RQ → 5–8 papers
- Broad / interdisciplinary RQ → 12–20 papers
- Stop when you find 2–3 papers that directly address the RQ

### Step 2 — User additions
After web search, ask: "Any specific papers, DOIs, or PDFs to add?"
Fetch links/DOIs via web_fetch. Read uploaded PDFs directly. Merge and deduplicate.

### Per-paper extraction (exactly these fields)
| Field | What to capture |
|---|---|
| Citation | Author(s), year, title, venue — APA format |
| Method + findings | What they did and found (2–3 sentences) |
| Data sources used | Datasets, APIs, or tools they relied on |
| Relevance to RQ | High / Medium / Low + 1 sentence why |

### Source Map output
```
## Source Map

| # | Citation | Method + Findings | Data Sources | Relevance to RQ |
|---|---|---|---|---|
| 1 | [APA citation] | [2–3 sentences] | [datasets/tools] | High — [why] |

## Synthesis
### What the literature establishes
[What is well-covered, dominant methods, commonly used data]

### The gap your research fills
[What is NOT answered — sharpens the RQ]

### Methodological precedents
[Papers using the closest approach — what to borrow]

### Data sources to consider
[Datasets/APIs from existing work — feeds Phase 2.3 directly]
```

### After the scan
1. Update the draft research framing doc with any RQ refinements
2. Save Source Map to `docs/source-map.md`
3. Update `docs/methodology.md`:
   - §Theoretical Framework — insert top 3–5 papers as foundation
   - §Methodological precedents — note which methods/tools from literature to adopt or adapt
   - §Data sources — add any new datasets discovered in the literature
   - §Validation approach — incorporate any validation strategies from comparable studies
4. Update `docs/state.md` — note scan complete, N papers found
5. Confirm refined framing with user before Phase 2

### What the Source Map feeds downstream
| Downstream | What it gets |
|---|---|
| `docs/methodology.md` §Theoretical Framework | Top 3–5 papers as foundation |
| E3 Linear epic (Literature Review) | Raw material — no cold start |
| Phase 2.2 method choices | Methodological precedents |
| Phase 2.3 data acquisition | Data sources already used by others |
| `docs/prd.md` §3.1 Background | Gap statement |

---

## Phase 3: Linear Setup (if not done yet)

Phases 1–2 are typically done in Claude for Mac. If arriving here with confirmed framing +
methodology, set up Linear immediately.

### Epic structure

| Epic | Track | Name |
|---|---|---|
| E1 | Shared | Research Framing |
| E2 | Shared | Methodology & Data Design |
| E3 | Paper | Literature Review |
| E4 | Paper | Paper Drafting |
| E5 | Paper | Paper Review & Revision |
| E6 | Product | Data Pipeline |
| E7 | Product | UI Foundation |
| E8 | Product | Core Features |
| E9 | Product | Code Review & QA |
| E10 | Convergence | Deliverables |

Dependency order: E1 → E2 → [E3/E4/E5 ∥ E6/E7/E8/E9] → E10

### Ticket template
```
Title: [action-oriented verb phrase]

## Context
[1–2 sentences linking to the phase/doc this comes from]
[Note: Paper track or Product track]

## Acceptance Criteria
- [ ] [specific, verifiable outcome]

## Technical Notes
[Schema fields, library choices, constraints, paper section notes]

## Blocked by
[ticket ID or "none"]
```

After confirming the full epic/ticket list, create in Linear and bootstrap `docs/`:
```bash
mkdir -p docs
cp docs/templates/*.template docs/
for f in docs/*.template; do mv "$f" "${f%.template}"; done
```

---

## Phase 4P: Paper Writing

Work ticket by ticket through E3–E5.

### Paper section → doc mapping
| Section | Source doc |
|---|---|
| Literature Review (E3) | `docs/source-map.md` — raw material, expand into academic prose |
| Methods | `docs/methodology.md` — rewrite as academic prose, never diverge |
| Results | Must reference same data/figures used in the product |
| Discussion | Must answer the research question from `docs/methodology.md` |

### After each paper ticket
Post completion comment (see Linear Workflow above).
Set status → In Review for supervisor feedback.

---

## Phase 4D: Data Pipeline + Product Build

Work ticket by ticket through E6–E9. Always pull ticket, read handoff notes, set In Progress,
branch, build, then post completion comment + commit + PR.

### Repo structure
```
my-app/
├── app/                    — Next.js App Router pages
├── components/             — UI components (under 150 lines each)
├── lib/
│   ├── mock-data.ts        — must match DATA_MODEL.md schema exactly
│   ├── data-utils.ts       — wrangling helpers (filter, aggregate, normalize)
│   └── types.ts            — TypeScript interfaces = DATA_MODEL.md schema
├── public/
│   └── dataset/            — cleaned dataset + README for public download
├── docs/                   — living documentation (this system)
│   ├── state.md
│   ├── EPICS_TASKS.md
│   ├── ROADMAP.md
│   ├── methodology.md
│   ├── ARCHITECTURE.md
│   ├── DATA_MODEL.md
│   ├── prd.md
│   ├── source-map.md       — literature scan output (Phase 1.3)
│   └── templates/          — source templates for all docs above
├── CLAUDE.md               — this file
├── package.json
└── README.md               — setup + research context
```

### Data layer
| Source | Implementation |
|---|---|
| Mock/synthetic | `lib/mock-data.ts` — field names/ranges from `docs/DATA_MODEL.md` |
| CSV upload | `<input type="file">` → `papaparse` → state |
| Live API | `fetch` in `useEffect`, loading/error states, no API keys client-side |

### Code standards
- Components < 150 lines; no `any`; all props typed
- Wrangling logic in `lib/` only — never inline in components
- `lib/mock-data.ts` field names must exactly match `docs/DATA_MODEL.md`
- Loading, empty, and error states required for all async/uploaded data
- No secrets or API keys in code

### When DATA_MODEL.md changes
If the schema changes during implementation:
1. Update `docs/DATA_MODEL.md`
2. Update `lib/types.ts` to match
3. Update `lib/mock-data.ts` to match
4. Update `docs/methodology.md` wrangling section if the pipeline changed
5. Note all changes in the Linear ticket comment

---

## Phase 5P: Paper Review

Run this checklist before marking any paper ticket Done:

- [ ] Research question stated clearly in the introduction
- [ ] Hypothesis is testable and the paper actually tests it
- [ ] Methods section matches `docs/methodology.md` exactly
- [ ] Results directly address the hypothesis
- [ ] Discussion connects findings back to the research question
- [ ] All claims cited or derived from data
- [ ] Limitations acknowledged (from methodology.md)
- [ ] Figures match those used in the product
- [ ] `docs/methodology.md` and paper Methods section are in sync

Output: ✅ / ⚠️ / ❌ — one line + fix per item.

---

## Phase 5D: Code Review

Run this checklist before marking any product ticket Done:

- [ ] No runtime errors (undefined, null, missing keys)
- [ ] All PRD user stories addressed
- [ ] Research question answerable from the UI
- [ ] `lib/mock-data.ts` field names match `docs/DATA_MODEL.md` exactly
- [ ] Wrangling in `lib/`, not inline
- [ ] `public/dataset/` has cleaned data + README
- [ ] Loading / empty / error states all handled
- [ ] All E6–E9 Linear tickets Done or In Review
- [ ] PRs opened and URLs posted on tickets

Output: ✅ / ⚠️ / ❌ — one line + fix per item.

---

## Phase 6: Deliverables

Final checklist before close-out:

### Paper
- [ ] All sections complete and supervisor-approved
- [ ] Abstract written last
- [ ] Citations in correct format for venue
- [ ] Figures match product

### Dataset
- [ ] `public/dataset/` has cleaned CSV/GeoJSON + README
- [ ] License: CC BY 4.0
- [ ] Published to Zenodo or institutional repo

### Product
- [ ] Deployed to Vercel / Netlify
- [ ] App links to paper and dataset
- [ ] `README.md` includes research context

### Linear close-out
- [ ] All E1–E10 tickets Done or Canceled
- [ ] Final comment: paper URL + dataset URL + deployed app URL

### Commit and tag
```bash
git tag v1.0.0 -m "Research project complete — paper + dataset + product"
git push origin v1.0.0
```

---

## Core Principles

- **Read `docs/state.md` first, every time.** Never re-scan the codebase cold.
- **Update `docs/` at session end, every time.** Future-you will thank you.
- **Methodology is the contract.** Paper Methods section = `docs/methodology.md` = `lib/` logic. All three must match.
- **Schema is the contract.** `docs/DATA_MODEL.md` = `lib/types.ts` = `lib/mock-data.ts`. All three must match.
- **Science first, UI second.** Don't touch code until methodology is confirmed.
- **Linear before code.** Tickets before implementation, always.
- **Public by default.** Dataset is CC BY 4.0. Product is deployed. Paper is submitted.
- **Both outputs or neither.** The paper without the product is inaccessible. The product without the paper is ungrounded.

---

## Agent Teams

This project has two parallel tracks — paper and product — that can run simultaneously
using subagents. The orchestrator (main Claude Code session) delegates to specialist
subagents and collects results.

### How subagents work in Claude Code

The orchestrator spawns subagents via the `Task` tool. Each subagent:
- Gets its own context window — does **not** inherit the orchestrator's context
- Must be given everything it needs upfront in its prompt
- Can read/write files, run shell commands, make commits
- Reports back a result when done

**`docs/` is the shared memory layer.** Since subagents don't share context, every
subagent prompt must start with:
```
Read docs/state.md and docs/EPICS_TASKS.md first, then proceed.
```
This is why `docs/state.md` exists — it's the handshake between the orchestrator and
every subagent it spawns.

---

### Pattern 1: Parallel paper + product sprint

Use when E3–E5 (paper) and E6–E9 (product) tickets are both unblocked.

Orchestrator spawns two agents simultaneously:

**Paper subagent:**
```
You are the paper agent for this research project.
Read docs/state.md, docs/methodology.md, docs/prd.md.
Task: [E4-002] Write the methodology section of the paper.
- Must match docs/methodology.md exactly — rewrite as academic prose, do not invent
- Target: 600–900 words
- Save to: paper/sections/03-methodology.md
- Post completion comment on Linear [E4-002], set status In Review
Report: word count, file path, open questions for supervisor.
```

**Product subagent:**
```
You are the product agent for this research project.
Read docs/state.md, docs/DATA_MODEL.md, docs/methodology.md §2.5.
Task: [E6-002] Implement the data wrangling pipeline.
- Follow step-by-step plan in docs/methodology.md §2.5 exactly
- Output: lib/data-utils.ts with typed wrangling helpers
- lib/mock-data.ts must match docs/DATA_MODEL.md schema
- Branch: e6-002/wrangling-pipeline
- Commit: feat(data): implement wrangling pipeline per methodology §2.5
- Post completion comment on Linear [E6-002], set status In Review
Report: files changed, schema deviations if any, next unblocked ticket.
```

Orchestrator collects both reports → updates `docs/state.md` + `docs/EPICS_TASKS.md`.

---

### Pattern 2: Sequential pipeline

Use when tasks depend on each other — acquire → wrangle → EDA → mock data.

```
Run E6 as a sequential chain:
1. E6-001: acquire datasets → report file paths
2. E6-002: wrangle (uses E6-001 output) → report cleaned schema
3. E6-003: EDA (uses E6-002 output) → report key findings
4. E6-004: populate lib/mock-data.ts (uses E6-003) → report record count

Each subagent receives the previous one's report as context before starting.
Update docs/EPICS_TASKS.md after each step completes.
```

The orchestrator passes each agent's output explicitly to the next:
```
You are the EDA agent. The wrangling pipeline produced this schema: [E6-002 report].
Your task: [E6-003] Run EDA per docs/methodology.md §2.6...
```

---

### Pattern 3: Specialist review agents

Use for Phase 5P + 5D — spawn one reviewer per concern, in parallel.

```
Spawn three reviewers simultaneously:

Agent 1 — Argument reviewer:
  Read paper/sections/*.md and docs/methodology.md.
  Check: Phase 5P argument structure checklist.
  Report: ✅/⚠️/❌ per item + one-line fix per issue.

Agent 2 — Consistency checker:
  Read paper/sections/03-methodology.md vs docs/methodology.md.
  Read lib/mock-data.ts vs docs/DATA_MODEL.md.
  Check: paper ↔ methodology ↔ code all in sync?
  Report: any divergences + files to update.

Agent 3 — Code reviewer:
  Read lib/, components/, docs/DATA_MODEL.md.
  Run: npm run build (report errors).
  Check: Phase 5D checklist.
  Report: ✅/⚠️/❌ per item + one-line fix per issue.
```

Orchestrator consolidates all three reports → creates fix tickets in Linear if needed
→ updates `docs/state.md` with open items.

---

### Subagent prompt template

Every subagent prompt must have these four parts:

```
## Context
Read docs/state.md and docs/EPICS_TASKS.md first.
[Paste any additional context: schema excerpt, methodology section, previous agent output]

## Task
[TICKET-ID] — [ticket title]
[Specific instructions]

## Constraints
- Follow docs/methodology.md for any data/analysis work
- Follow docs/DATA_MODEL.md for any schema work
- Branch: {ticket-id}/{short-description}
- Commit: {type}({scope}): {description}
- Post Linear completion comment + set ticket status

## Report back
[What the orchestrator needs: files created, schema changes, findings, next unblocked ticket]
```

---

### Guardrails

**Subagents must never:**
- Modify `docs/methodology.md` or `docs/DATA_MODEL.md` unilaterally — schema/methodology
  changes need orchestrator confirmation (and ultimately human confirmation)
- Push directly to `main` — always branch + PR
- Skip the Linear completion comment
- Run destructive commands without orchestrator approval

**Orchestrator always:**
- Updates `docs/state.md` after subagents complete — never delegate this
- Resolves conflicts between subagent outputs (two agents touching the same file)
- Gates the next wave on the previous wave completing successfully

---

### When NOT to use subagents

| Task | Why not |
|---|---|
| Updating `docs/state.md` | Orchestrator owns session state |
| Resolving schema conflicts | Needs full project context |
| Supervisor feedback review | Nuanced judgment, needs full paper context |
| Anything touching `docs/methodology.md` | Contract-level — needs human confirmation |
| Phase 1–2 (framing, methodology) | Done in Claude for Mac, not terminal |
