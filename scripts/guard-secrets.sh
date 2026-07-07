#!/usr/bin/env bash
# Shared secret / build-artifact guard, run by both CI and the local pre-commit
# hook (scripts/install-hooks.sh) so violations are caught before they're even
# committed, not just at PR time.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

if [ -d graphify-out ]; then
  echo "graphify-out/ must not be committed — it's regenerable build output." >&2
  exit 1
fi
if [ -f .env ]; then
  echo ".env must not be committed — copy .env.example instead." >&2
  exit 1
fi
if find . -path ./.git -prune -o \( -name '*.pem' -o -name '*.key' \) -print | grep -q .; then
  echo "Found a *.pem/*.key file — private keys must never be committed." >&2
  exit 1
fi
# Anthropic / OpenAI / Google / AWS / GitHub / Slack tokens + raw PEM key blocks
if grep -RInE \
    "sk-ant-[A-Za-z0-9_-]{20,}|sk-proj-[A-Za-z0-9_-]{20,}|AIza[0-9A-Za-z_-]{35}|AKIA[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|xox[baprs]-[A-Za-z0-9-]{10,}|-----BEGIN[A-Z ]*PRIVATE KEY-----" \
    --exclude-dir=.git .; then
  echo "Possible API key or private key found in a tracked file." >&2
  exit 1
fi
echo "guard-secrets: clean"
