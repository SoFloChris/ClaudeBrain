#!/usr/bin/env bash
# Stop hook — if a substantive session is ending with nothing written to the vault,
# say so once. Deliberately conservative: silent whenever notes changed, silent if
# it already fired in the last 90 minutes, and never able to loop.
set -uo pipefail

DIR="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"
cd "$DIR" 2>/dev/null || exit 0

INPUT=$(cat)

# 1. Never loop: if we already blocked once in this stop-chain, let it stop.
if printf '%s' "$INPUT" | python3 -c "
import json,sys
try: sys.exit(0 if json.load(sys.stdin).get('stop_hook_active') else 1)
except Exception: sys.exit(0)
"; then
  exit 0
fi

# 2. Did anything in the vault actually change? If so, work was captured — stay quiet.
#    Check BOTH uncommitted edits and recent commits: a session that wrote notes and
#    then committed them leaves a clean tree, and must not be nagged for it.
if [ -n "$(git status --porcelain -- '*.md' 2>/dev/null)" ]; then
  exit 0
fi
if [ -n "$(git log --since='6 hours ago' --name-only --pretty=format: -- '*.md' 2>/dev/null | head -1)" ]; then
  exit 0
fi

# 3. Rate-limit: at most one nudge every 90 minutes.
MARKER="$DIR/90-System/Graph/.last-nudge"
mkdir -p "$(dirname "$MARKER")" 2>/dev/null
if [ -f "$MARKER" ]; then
  LAST=$(date -r "$MARKER" +%s 2>/dev/null || echo 0)
  NOW=$(date +%s)
  if [ $((NOW - LAST)) -lt 5400 ]; then
    exit 0
  fi
fi
touch "$MARKER" 2>/dev/null

# 4. Nudge. Exit 0 with JSON on stdout is the documented feedback channel
#    (exit 2 would discard stdout and use stderr instead — don't mix the two).
python3 - <<'PY'
import json
print(json.dumps({
    "decision": "block",
    "reason": (
        "This session is ending with no changes to any vault note. If anything durable "
        "came up — a person, company, or tool worth a wiki note; a question the vault "
        "couldn't answer; a decision worth an ADR; a fact about Chris worth remembering — "
        "capture it now (/wrap harvests the whole conversation). "
        "If genuinely nothing durable came up, say so in one line and stop."
    ),
}))
PY
exit 0
