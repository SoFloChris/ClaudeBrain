---
type: tool
summary: "Local LLM runtime - no API key, no per-token cost, and nothing leaving the machine."
alternative_to: ["[[Voyage AI]]"]
related: ["[[Embeddings]]", "[[COMMAND — Quant Operations Platform]]"]
---

# Ollama

Local LLM runtime. Runs models on your own hardware — no API key, no per-token cost, nothing leaving the machine.

## Key facts

- In [[COMMAND — Quant Operations Platform]]: 9 local models on an RTX PRO 6000 (96 GB VRAM), served at port 11434. `model-router.ts` is **local-first** — it reaches for Ollama before paid APIs, escalating to [[Anthropic]]/OpenAI/Google/xAI only when needed.
- Also serves **embeddings**, which is the relevant angle for this vault: `embeddinggemma` (622MB), `nomic-embed-text` (274MB), `mxbai-embed-large` (670MB), `bge-m3` (1.2GB, hybrid dense+sparse).
- [[Smart Connections]] can point at Ollama instead of its bundled model for better semantic search quality.

## Why it matters to me

The "local-first, escalate when needed" routing pattern is the cost architecture worth copying: most calls are cheap and private, and only genuinely hard ones pay for a frontier model. [[brain_search]] follows the same instinct — local embeddings by default, [[Voyage AI]] documented as the upgrade path if ever needed.

## Related

- [[Local Embedding Models]] — model comparison
