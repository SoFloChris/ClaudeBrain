#!/usr/bin/env bash
# Rebuild the Graphify knowledge graph for this vault (incremental).
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

if ! command -v graphify >/dev/null 2>&1; then
  echo "graphify CLI not found. Install it first:" >&2
  echo "  pipx install graphifyy   # or: uv tool install graphifyy" >&2
  exit 1
fi

graphify extract . --update
echo "Graph refreshed: graphify-out/graph.json"
