---
description: Semantic search — find vault notes by meaning, not just keywords
argument-hint: [what you're trying to remember]
allowed-tools: Bash(python3 *), Read, Grep
---

Find what the vault knows about: $ARGUMENTS

1. Run semantic search: `python3 "90-System/Scripts/brain_search.py" search "$ARGUMENTS" -k 8`
   - First run on a machine builds the index (downloads a small local embedding model once). If it fails with "sentence-transformers is not installed", tell me to run `pip install sentence-transformers` — don't install it yourself.
2. Also run a plain keyword Grep for the distinctive terms — semantic and keyword search miss different things.
3. Open the top-scoring notes and read the relevant sections.
4. Answer from the notes, citing each source as `[[Note Name]]`. If the vault has nothing, say so plainly rather than guessing.
