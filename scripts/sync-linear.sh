#!/bin/bash
# sync-linear.sh — Push EPICS_TASKS.md status changes to Linear
# Usage: ./scripts/sync-linear.sh
# Or with a specific ticket: ./scripts/sync-linear.sh MVP-23 "In Progress" "optional comment"
#
# Reads LINEAR_API_KEY from environment or ~/.claude/settings.json (linear-personal)
# --all mode also syncs projectMilestoneId and projectId for every ticket

set -e

API_KEY="${LINEAR_API_KEY:-}"
TEAM_ID="3e556f7f-ca5b-4db5-9a96-e197fda40f53"
PROJECT_ID="d9c39f66-614b-4b42-ae84-868516a82742"
API="https://api.linear.app/graphql"

# Pull key from ~/.claude/settings.json if not in env
if [ -z "$API_KEY" ]; then
  API_KEY=$(python3 -c "
import json, os
with open(os.path.expanduser('~/.claude/settings.json')) as f:
    d = json.load(f)
print(d['mcpServers']['linear-personal']['env']['LINEAR_API_KEY'])
" 2>/dev/null || echo "")
fi

if [ -z "$API_KEY" ]; then
  echo "ERROR: LINEAR_API_KEY not set."
  echo "  Export it: export LINEAR_API_KEY=lin_api_..."
  echo "  Or store in ~/.claude/settings.json under mcpServers.linear-personal.env.LINEAR_API_KEY"
  exit 1
fi

# State name → ID map for Product-MVP team
declare -A STATE_IDS=(
  ["Todo"]="0f1ef1eb-ee11-41a8-9023-1f1440e8692b"
  ["In Progress"]="642befcf-d9c7-4759-a736-da0378cd8977"
  ["In Review"]="fac339f7-9bac-4694-968f-a78038a2af5d"
  ["Done"]="546e736b-4095-4059-9269-9bdc08811899"
  ["Backlog"]="d0314f0c-61e2-4d9f-98ac-860e97826400"
  ["Canceled"]="df19592c-e4f1-4ee0-b317-328255f9e45a"
)

# Epic name → milestone ID map for Jabodetabek Transit Equity Mapper project
declare -A MILESTONE_IDS=(
  ["E1 · Research Framing"]="02f6f60f-d186-4c18-bd9b-29cede020c7a"
  ["E2 · Methodology & Data Design"]="4280095b-917c-4ef2-a0af-7facd69c8e28"
  ["E3 · Literature Review"]="66c3a12c-0414-4cee-8bce-6ceebfc3dadd"
  ["E4 · Paper Drafting"]="4688466d-7211-4eea-bd38-4ab7dc303fff"
  ["E5 · Paper Review & Revision"]="fec9c166-5992-4e04-bb38-846affe861b0"
  ["E6 · Data Pipeline"]="aef8ddfa-18c4-47ae-b976-860ad115579c"
  ["E7 · UI Foundation"]="0f0aa5a2-4a31-4a4f-9c30-d5c382860c93"
  ["E8 · Core Features"]="726f31ba-b7d3-4b03-8c31-b078178c8c2d"
  ["E9 · Code Review & QA"]="f370aaa9-be35-48ab-a9ba-dc563a5bab16"
  ["E10 · Deliverables"]="e0914382-7b03-417b-a211-4520425d54ce"
)

gql() {
  curl -s -X POST "$API" \
    -H "Content-Type: application/json" \
    -H "Authorization: $API_KEY" \
    -d "$1"
}

# Get issue ID by number
get_issue_id() {
  local number="$1"
  gql "{\"query\": \"{ team(id: \\\"$TEAM_ID\\\") { issues(filter: { number: { eq: $number } }) { nodes { id identifier state { name } } } } }\"}" \
    | python3 -c "import sys,json; d=json.load(sys.stdin); n=d['data']['team']['issues']['nodes']; print(n[0]['id'] if n else '')" 2>/dev/null
}

# Update a single ticket — status only (single-ticket CLI mode)
update_ticket_status() {
  local identifier="$1"
  local new_status="$2"
  local comment="$3"

  local number="${identifier#MVP-}"
  local issue_id
  issue_id=$(get_issue_id "$number")

  if [ -z "$issue_id" ]; then
    echo "  ✗ $identifier: not found in Linear"
    return
  fi

  local state_id="${STATE_IDS[$new_status]}"
  if [ -z "$state_id" ]; then
    echo "  ✗ $identifier: unknown status '$new_status'"
    return
  fi

  gql "{\"query\": \"mutation { issueUpdate(id: \\\"$issue_id\\\", input: { stateId: \\\"$state_id\\\" }) { success issue { identifier state { name } } } }\"}" \
    | python3 -c "import sys,json; d=json.load(sys.stdin); r=d['data']['issueUpdate']['issue']; print(f\"  ✓ {r['identifier']}: → {r['state']['name']}\")"

  if [ -n "$comment" ]; then
    local payload
    payload=$(python3 -c "
import json, sys
q = 'mutation AddComment(\$issueId: String!, \$body: String!) { commentCreate(input: { issueId: \$issueId, body: \$body }) { success } }'
print(json.dumps({'query': q, 'variables': {'issueId': sys.argv[1], 'body': sys.argv[2]}}))
" "$issue_id" "$comment")
    gql "$payload" | python3 -c "import sys,json; d=json.load(sys.stdin); print('    comment: ' + str(d['data']['commentCreate']['success']))"
  fi
}

# Update a ticket with status + milestone + project (bulk sync mode)
update_ticket_full() {
  local identifier="$1"
  local new_status="$2"
  local epic_name="$3"

  local number="${identifier#MVP-}"
  local issue_id
  issue_id=$(get_issue_id "$number")

  if [ -z "$issue_id" ]; then
    echo "  ✗ $identifier: not found in Linear"
    return
  fi

  local state_id="${STATE_IDS[$new_status]}"
  if [ -z "$state_id" ]; then
    echo "  ✗ $identifier: unknown status '$new_status'"
    return
  fi

  local milestone_id="${MILESTONE_IDS[$epic_name]}"

  # Build input fields — always set state + project; conditionally set milestone
  local input_fields="stateId: \\\"$state_id\\\", projectId: \\\"$PROJECT_ID\\\""
  if [ -n "$milestone_id" ]; then
    input_fields="$input_fields, projectMilestoneId: \\\"$milestone_id\\\""
  fi

  local result
  result=$(gql "{\"query\": \"mutation { issueUpdate(id: \\\"$issue_id\\\", input: { $input_fields }) { success issue { identifier state { name } projectMilestone { name } } } }\"}")

  local state_name milestone_name
  state_name=$(echo "$result" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['data']['issueUpdate']['issue']['state']['name'])" 2>/dev/null)
  milestone_name=$(echo "$result" | python3 -c "import sys,json; d=json.load(sys.stdin); m=d['data']['issueUpdate']['issue'].get('projectMilestone'); print(m['name'] if m else '(no epic)')" 2>/dev/null)

  echo "  ✓ $identifier: → $state_name | $milestone_name"
}

# ─── Parse EPICS_TASKS.md → ticket|status|epic triples ───────────────────────
parse_epics_tasks() {
  python3 - <<'PYEOF'
import re, sys

with open("docs/EPICS_TASKS.md") as f:
    lines = f.readlines()

current_epic = None
current_ticket = None

for i, line in enumerate(lines):
    line = line.rstrip()

    # ## E4 · Paper Drafting  (epic section header)
    epic_match = re.match(r'^## (E\d+\s·\s.+)$', line)
    if epic_match:
        current_epic = epic_match.group(1).strip()
        continue

    # ### MVP-85 — ...  (ticket header)
    ticket_match = re.match(r'^### (MVP-\d+)', line)
    if ticket_match:
        current_ticket = ticket_match.group(1)
        continue

    # - **Status**: Done
    if current_ticket:
        status_match = re.match(r'^- \*\*Status\*\*:\s*(.+)$', line)
        if status_match:
            status = status_match.group(1).strip()
            epic = current_epic or ""
            print(f"{current_ticket}|{status}|{epic}")
            current_ticket = None
PYEOF
}

# ─── Main ─────────────────────────────────────────────────────────────────────
if [ "$1" = "--all" ] || [ -z "$1" ]; then
  echo "Syncing EPICS_TASKS.md → Linear (status + milestone + project)..."
  while IFS='|' read -r ticket status epic; do
    update_ticket_full "$ticket" "$status" "$epic"
  done < <(parse_epics_tasks)
  echo "Done."

elif [ -n "$1" ] && [ -n "$2" ]; then
  # Single ticket: ./sync-linear.sh MVP-23 "In Progress" "optional comment"
  echo "Updating $1 → $2"
  update_ticket_status "$1" "$2" "$3"
  echo "Done."

else
  echo "Usage:"
  echo "  ./scripts/sync-linear.sh                          # sync all from EPICS_TASKS.md"
  echo "  ./scripts/sync-linear.sh MVP-23 'In Progress'     # single ticket status update"
  echo "  ./scripts/sync-linear.sh MVP-23 'Done' 'comment'  # with comment"
  exit 1
fi
