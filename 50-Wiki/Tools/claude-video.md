---
type: tool
aliases: ["/watch", "watch skill", "claude-video", "Claude video skill"]
related: ["[[Claude Code]]", "[[Every Level of a Claude Second Brain]]"]
repo: "https://github.com/bradautomates/claude-video"
---

# claude-video

A [[Claude Code]] skill pack (MIT, by GitHub user `bradautomates`) that gives Claude a video input: `/watch <url>` downloads a video, extracts frames, transcribes the audio, and hands all of it to the model. Verified real — 10.8k stars, 1.1k forks as of 2026-07.

## Key facts (researched 2026-07)

- **Install:** `/plugin marketplace add bradautomates/claude-video` then `/plugin install watch@claude-video`. Also `npx skills add bradautomates/claude-video -g` for Codex/Cursor/Copilot, or a `.skill` download for claude.ai.
- **Dependencies:** `yt-dlp` (download) + `ffmpeg` (frames), auto-installed via brew on macOS; Linux/Windows print the exact commands.
- **Transcription is free by default** — it pulls existing captions with yt-dlp and only falls back to Whisper when a video has none. Groq `whisper-large-v3` is preferred over OpenAI `whisper-1` on cost and speed. No API key needed for most public videos.
- **Detail modes trade tokens for coverage:** `transcript` (text only) · `efficient` (~50 keyframes) · `balanced` (~100 scene frames) · `token-burner` (uncapped). Frame dedup drops near-identical frames automatically.
- **`--start` / `--end`** narrow to a section and raise frame density (capped at 2 fps). Past ~10 minutes the capped modes warn that coverage is sparse — the intended workflow is focused re-runs, not one giant pass.
- Works on anything yt-dlp supports (YouTube, Instagram, X, Vimeo). A fork, `mathiaschu/watch`, swaps in local `mlx-whisper` for fully offline transcription.

## Why it matters to me

This vault's founding note — [[Every Level of a Claude Second Brain]] — is a distilled YouTube video, done by hand. `/watch` industrialises exactly that: paste a URL, get the substance, write the note, keep nothing raw. It's a **capture pipeline for Level 2**, and the guardrail is unchanged — the transcript is not the artifact, the distilled note is ([[Context vs Connections]]).

Worth installing before the next research-video binge. Start in `transcript` mode; frames only matter when the video *demonstrates* something (a UI walkthrough, a file tree) rather than explains it.

## Related

- [[Claude Code]] — the harness; this installs as a plugin/skill
- [[Verify the Claim, Steal the Architecture]] — the counter-example that keeps that filter honest: this one went viral *and* was real
