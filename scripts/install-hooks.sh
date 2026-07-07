#!/usr/bin/env bash
# One-time setup: route git hooks through the versioned .githooks/ directory.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

chmod +x .githooks/pre-commit
git config core.hooksPath .githooks
echo "Pre-commit hook installed (git config core.hooksPath .githooks)."
