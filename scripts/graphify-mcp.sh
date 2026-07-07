#!/usr/bin/env bash
# Launch the Graphify MCP server for this vault's graph. Invoked by .mcp.json —
# not meant to be run by hand except to sanity-check the setup.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

GRAPH_FILE="graphify-out/graph.json"
if [ ! -f "$GRAPH_FILE" ]; then
  echo "No graph found at $GRAPH_FILE. Run ./scripts/graphify-sync.sh first." >&2
  exit 1
fi

PYTHON_BIN="python3"
command -v python3 >/dev/null 2>&1 || PYTHON_BIN="python"

if ! "$PYTHON_BIN" -c "import graphify" >/dev/null 2>&1; then
  echo "graphify Python package not importable by $PYTHON_BIN. Install it first:" >&2
  echo "  pipx install graphifyy   # or: uv tool install graphifyy" >&2
  exit 1
fi

exec "$PYTHON_BIN" -m graphify.serve "$GRAPH_FILE"
