#!/usr/bin/env bash
# SessionStart hook — brief the agent on vault state and the growth mandate.
# stdout from a SessionStart hook is injected into the session context.
set -uo pipefail

DIR="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"
cd "$DIR" 2>/dev/null || exit 0

echo "=== ClaudeBrain vault state ==="
python3 "$DIR/90-System/Scripts/vault_stats.py" --brief 2>/dev/null || echo "(vault_stats unavailable)"
cat <<'BRIEF'

Reminder — this vault is co-authored, not just read. A session that only reads has failed.
Write notes as you go: any person/company/tool/concept that comes up gets a wiki note;
any question the vault couldn't answer gets its answer captured; any decision gets recorded.
Every curated link carries an em-dash clause saying how the notes relate.
Run /wrap before finishing a substantive conversation.
BRIEF
exit 0
