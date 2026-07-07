#!/usr/bin/env bash
# Build (or incrementally refresh) the Graphify knowledge graph for this vault.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

if ! command -v graphify >/dev/null 2>&1; then
  echo "graphify CLI not found. Install it first:" >&2
  echo "  pipx install graphifyy   # or: uv tool install graphifyy" >&2
  exit 1
fi

if ! python3 scripts/check-links.py; then
  echo "Fix broken wikilinks above before rebuilding the graph." >&2
  exit 1
fi

if [ -f graphify-out/graph.json ]; then
  graphify extract . --update "$@"
else
  graphify extract . "$@"
fi
echo "Graph refreshed: graphify-out/graph.json"
