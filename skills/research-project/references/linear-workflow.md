# Linear Workflow Reference

Verbatim conventions from the project's CLAUDE.md. Follow these exactly.

## Ticket Status Flow
Backlog → Todo → In Progress → In Review → Done (or Canceled)

## Branch Naming
{ticket-id}/{short-description}
Example: ifi-15/tenant-schema, ifi-16/tenant-registration-form
- Branch off main unless ticket is blocked by an unmerged ticket — then branch off that ticket's branch

## Commit Format (Conventional Commits)
feat(scope): description       — new feature or endpoint
fix(scope): description        — bug fix
refactor(scope): description   — restructure without behavior change
chore(scope): description      — tooling, deps, config
docs(scope): description       — documentation only

Atomic commits: group logically related files. Do not commit file-by-file, but don't dump everything in one commit either.

## PR Title Format
[{TICKET-ID}] {ticket title}
Example: [IFI-15] Database Schema — Core Tables

## PR Description Format
## Overview
{1–2 sentences describing what this PR does and why}
- {Key detail or decision}

## Changes
- `{file or area}` — {what changed}

## Testing
- {Step-by-step verification instructions}
- {Seed data, env vars, or setup needed}

## Notes
{Deviations from spec, caveats — omit if nothing notable}

## Linear
{Linear ticket URL}

## Completion Comment Format (post on ticket after finishing)
**What was built**
- {bullet list of features/endpoints/UI pages}

**Key files changed**
- `{file path}` — {what changed}

**API test results**
✅ {test case}: passed — {actual response summary}
❌ {test case}: failed — {error}

**Handoff notes**
- {Context the next ticket needs}
- {Deviations from spec and why}

## Finding Next Ticket
- Work in epic dependency order: E1 → E2 → E3/E4/E7 (parallel) → E5 → E6
- Within an epic, work tickets in numeric order unless unblocked earlier
- Always pull full ticket before starting — never work from memory alone
