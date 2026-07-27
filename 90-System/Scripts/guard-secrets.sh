#!/usr/bin/env bash
# Fail if anything secret-shaped is tracked in this repo.
#
# Run by CI (.github/workflows/vault-check.yml); safe to run by hand any time.
#
# Scans TRACKED files only (`git ls-files`) rather than the working tree. The
# question this answers is "did a secret get committed", and scanning tracked
# files keeps gitignored build output (90-System/Graph/, __pycache__/, the
# search index) out of the results — those are large, regenerable, and noisy.
#
# Note that Memory.md says "never store secrets or credentials here". This is
# the mechanism behind that sentence; the vendored third-party skills under
# .claude/skills/ are exactly why it now matters.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

fail() {
  echo "guard-secrets: $1" >&2
  exit 1
}

if git ls-files --error-unmatch .env >/dev/null 2>&1; then
  fail ".env is tracked — it must never be committed."
fi

keyfiles="$(git ls-files -- '*.pem' '*.key')"
if [ -n "$keyfiles" ]; then
  echo "$keyfiles" >&2
  fail "a *.pem / *.key file is tracked — private keys must never be committed."
fi

# Anthropic / OpenAI / Google / AWS / GitHub / Slack tokens, plus raw PEM blocks.
# These match key *values*; variable names like GROQ_API_KEY are fine and common
# in the vendored skills.
pattern='sk-ant-[A-Za-z0-9_-]{20,}'
pattern="$pattern"'|sk-proj-[A-Za-z0-9_-]{20,}'
pattern="$pattern"'|AIza[0-9A-Za-z_-]{35}'
pattern="$pattern"'|AKIA[0-9A-Z]{16}'
pattern="$pattern"'|gh[pousr]_[A-Za-z0-9]{20,}'
pattern="$pattern"'|github_pat_[A-Za-z0-9_]{20,}'
pattern="$pattern"'|xox[baprs]-[A-Za-z0-9-]{10,}'
pattern="$pattern"'|-----BEGIN[A-Z ]*PRIVATE KEY-----'

# `|| true` because grep exits 1 on no-match, and xargs turns any non-zero child
# exit into 123 — neither is an error here. Emptiness of the output is the test.
matches="$(git ls-files -z | xargs -0 grep -InE "$pattern" 2>/dev/null || true)"
if [ -n "$matches" ]; then
  echo "$matches" >&2
  fail "possible API key or private key found in a tracked file (listed above)."
fi

echo "guard-secrets: clean"
