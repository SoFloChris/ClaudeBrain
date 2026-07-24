#!/usr/bin/env python3
"""ClaudeBrain semantic search — Level 3.

Search the vault by meaning, not just keywords. Local, private, free:
embeddings run on your machine via sentence-transformers; nothing leaves it.

One-time setup (per machine):
    pip install sentence-transformers

Usage:
    python3 brain_search.py index              # build/update the embedding index
    python3 brain_search.py search "query"     # top matches by meaning
    python3 brain_search.py search "query" -k 10
    python3 brain_search.py chunks             # dry-run: show chunking, no embeddings

Model: BAAI/bge-small-en-v1.5 by default (small, ungated, downloads once).
Override with the BRAIN_EMBED_MODEL env var — e.g. google/embeddinggemma-300m
for higher quality (larger download; requires accepting the Gemma license on
Hugging Face and being logged in via `huggingface-cli login`).

Index lives in 90-System/Search Index/ (gitignored — each machine builds its
own; incremental, so only changed notes are re-embedded).
"""

import hashlib
import json
import os
import re
import sys
from pathlib import Path

VAULT = Path(__file__).resolve().parents[2]
INDEX_DIR = VAULT / "90-System" / "Search Index"
MANIFEST = INDEX_DIR / "manifest.json"
VECTORS = INDEX_DIR / "vectors.npy"
MODEL = os.environ.get("BRAIN_EMBED_MODEL", "BAAI/bge-small-en-v1.5")
SKIP_DIRS = {".obsidian", ".git", ".trash", "node_modules", ".claude"}
SKIP_FILES = {"SETUP.md", "README.md"}
MAX_CHARS = 1600  # ~400 tokens; retrieval precision peaks around 256-512 tokens


def iter_notes():
    templates = VAULT / "90-System" / "Templates"
    for path in sorted(VAULT.rglob("*.md")):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.name in SKIP_FILES or path.is_relative_to(templates):
            continue
        yield path


def chunk_note(path):
    """Heading-based chunks: one per section, long sections split by paragraph.
    Each chunk is prefixed with its note title + heading path for context."""
    rel = path.relative_to(VAULT).as_posix()
    text = path.read_text(encoding="utf-8", errors="replace")
    if text.startswith("---"):  # drop frontmatter
        end = text.find("\n---", 3)
        if end != -1:
            text = text[end + 4:]

    sections, heading, buf = [], "", []
    for line in text.splitlines():
        m = re.match(r"^(#{1,4})\s+(.*)", line)
        if m:
            if "".join(buf).strip():
                sections.append((heading, "\n".join(buf).strip()))
            heading, buf = m.group(2).strip(), []
        else:
            buf.append(line)
    if "".join(buf).strip():
        sections.append((heading, "\n".join(buf).strip()))

    chunks = []
    for heading, body in sections:
        pieces = [body]
        if len(body) > MAX_CHARS:
            pieces, cur = [], ""
            for para in body.split("\n\n"):
                if cur and len(cur) + len(para) > MAX_CHARS:
                    pieces.append(cur.strip())
                    cur = para
                else:
                    cur = f"{cur}\n\n{para}" if cur else para
            if cur.strip():
                pieces.append(cur.strip())
        for piece in pieces:
            context = f"{path.stem}" + (f" > {heading}" if heading else "")
            chunks.append({"file": rel, "heading": heading, "text": f"{context}\n{piece}"})
    return chunks


def collect_chunks():
    all_chunks, states = [], {}
    for path in iter_notes():
        rel = path.relative_to(VAULT).as_posix()
        digest = hashlib.sha256(path.read_bytes()).hexdigest()[:16]
        states[rel] = digest
        for chunk in chunk_note(path):
            chunk["digest"] = digest
            all_chunks.append(chunk)
    return all_chunks, states


def load_model():
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        sys.exit(
            "sentence-transformers is not installed.\n"
            "Run:  pip install sentence-transformers\n"
            "(one-time per machine; the model downloads on first use)"
        )
    return SentenceTransformer(MODEL)


def build_index():
    import numpy as np

    chunks, _ = collect_chunks()
    old = {}
    if MANIFEST.exists() and VECTORS.exists():
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        if manifest.get("model") == MODEL:
            vectors = np.load(VECTORS)
            for i, c in enumerate(manifest["chunks"]):
                old[(c["file"], c["digest"], c["text"])] = vectors[i]

    todo = [c for c in chunks if (c["file"], c["digest"], c["text"]) not in old]
    if todo:
        model = load_model()
        print(f"embedding {len(todo)} new/changed chunks with {MODEL}...")
        new_vecs = model.encode(
            [c["text"] for c in todo], normalize_embeddings=True, show_progress_bar=True
        )
    else:
        new_vecs = []
        print("index up to date")

    rows, it = [], iter(new_vecs)
    for c in chunks:
        key = (c["file"], c["digest"], c["text"])
        rows.append(old[key] if key in old else next(it))

    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    np.save(VECTORS, np.array(rows, dtype="float32"))
    MANIFEST.write_text(
        json.dumps({"model": MODEL, "chunks": chunks}, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"index: {len(chunks)} chunks from the vault -> {INDEX_DIR.relative_to(VAULT)}")


def search(query, top_k=5):
    import numpy as np

    if not (MANIFEST.exists() and VECTORS.exists()):
        print("No index yet — building one first.")
        build_index()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest.get("model") != MODEL:
        print("Index was built with a different model — rebuilding.")
        build_index()
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    vectors = np.load(VECTORS)

    model = load_model()
    if "bge" in MODEL.lower():  # bge models want an instruction prefix on queries
        query_text = f"Represent this sentence for searching relevant passages: {query}"
    else:
        query_text = query
    q = model.encode([query_text], normalize_embeddings=True)[0]
    scores = vectors @ q

    seen_files = set()
    order = np.argsort(-scores)
    shown = 0
    for i in order:
        c = manifest["chunks"][int(i)]
        marker = "" if c["file"] in seen_files else "*"
        seen_files.add(c["file"])
        snippet = " ".join(c["text"].split())[:180]
        print(f"{scores[int(i)]:.3f} {marker:1} {c['file']}"
              + (f"  #{c['heading']}" if c["heading"] else ""))
        print(f"        {snippet}")
        shown += 1
        if shown >= top_k:
            break


def show_chunks():
    chunks, _ = collect_chunks()
    for c in chunks:
        print(f"{c['file']}  #{c['heading'] or '(top)'}  [{len(c['text'])} chars]")
    print(f"total: {len(chunks)} chunks")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "index":
        build_index()
    elif cmd == "search" and len(sys.argv) > 2:
        k = 5
        args = sys.argv[2:]
        if "-k" in args:
            i = args.index("-k")
            k = int(args[i + 1])
            args = args[:i] + args[i + 2:]
        search(" ".join(args), top_k=k)
    elif cmd == "chunks":
        show_chunks()
    else:
        print(__doc__)
