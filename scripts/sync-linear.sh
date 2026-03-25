#!/bin/bash
# sync-linear.sh — Push EPICS_TASKS.md status changes to Linear
# Usage: ./scripts/sync-linear.sh
# Or with a specific ticket: ./scripts/sync-linear.sh MVP-23 "In Progress"
#
# Reads LINEAR_API_KEY from environment or ~/.claude/settings.json (linear-personal)

set -e

API_KEY="${LINEAR_API_KEY:-}"
TEAM_ID="3e556f7f-ca5b-4db5-9a96-e197fda40f53"
API="https://api.linear.app/graphql"

# Pull key from ~/.claude/settings.json if not in env
if [ -z "$API_KEY" ]; then
  API_KEY=$(python3 -c "
import json, sys
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
    | python3 -c "import sys,json; d=json.load(sys.stdin); n=d['data']['team']['issues']['nodes']; print(n[0]['id'] if n else '') " 2>/dev/null
}

# Update a single ticket
update_ticket() {
  local identifier="$1"   # e.g. MVP-23
  local new_status="$2"   # e.g. "In Progress"
  local comment="$3"      # optional

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

# ─── Parse EPICS_TASKS.md and sync all statuses ───────────────────────────────
sync_all() {
  echo "Syncing EPICS_TASKS.md → Linear..."
  local epics_file="docs/EPICS_TASKS.md"

  python3 - <<'PYEOF'
import re, subprocess, sys

with open("docs/EPICS_TASKS.md") as f:
    content = f.read()

# Extract all MVP-N + Status pairs
pattern = r'### (MVP-\d+)[^\n]*\n(?:.*\n)*?- \*\*Status\*\*: (\w[\w ]*)'
matches = re.findall(pattern, content)

for ticket, status in matches:
    print(f"{ticket}|{status.strip()}")
PYEOF
}

# ─── Main ─────────────────────────────────────────────────────────────────────
if [ "$1" = "--all" ] || [ -z "$1" ]; then
  # Sync all tickets from EPICS_TASKS.md
  echo "Reading EPICS_TASKS.md..."
  while IFS='|' read -r ticket status; do
    update_ticket "$ticket" "$status"
  done < <(sync_all)
  echo "Done."

elif [ -n "$1" ] && [ -n "$2" ]; then
  # Single ticket update: ./sync-linear.sh MVP-23 "In Progress" "optional comment"
  echo "Updating $1 → $2"
  update_ticket "$1" "$2" "$3"
  echo "Done."

else
  echo "Usage:"
  echo "  ./scripts/sync-linear.sh              # sync all from EPICS_TASKS.md"
  echo "  ./scripts/sync-linear.sh MVP-23 'In Progress' 'optional comment'"
  exit 1
fi
