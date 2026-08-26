---
name: mob-flutter-kb
description: >-
  Gateway to the local official Flutter/Dart knowledge base (full flutter.dev and dart.dev
  docs + 757 videos with their transcripts) — every Flutter question or pattern is answered from it
  with documented sources, never from general memory. Triggers — Arabic: "search the flutter KB", "the official
  way to do X", "how does widget X work", "best practice for X", "document a Flutter pattern", "check
  the documentation", "find a video about". English: "search the flutter KB", "official way to
  do X in Flutter", "how does widget X work", "flutter best practice", "ground
  this in docs", "find the video about". Invoked inside the Mobile room whenever a documented official
  source is needed before building/deciding on a Flutter/Dart pattern.
---

# mob-flutter-kb — The Official Flutter/Dart Knowledge Gateway (Flutter Knowledge Base Gateway) ⬛

> **Value:** every Flutter/Dart answer is built from what the Flutter team actually wrote (367 doc pages + 113 Dart pages + 757 video transcripts ≈ 372 hours) — cited as `file:line` — instead of guessing from general training data that may be stale.
> **Location:** `/home/es3dlll/flutter-knowledge-base` (local, updatable via the official refresh scripts).

## 🎯 When to invoke (When) ⬛
- Any «how / what is the official way» question in Flutter or Dart before implementing a critical pattern (architecture, state, perf, platform-integration, testing).
- Verifying a pattern proposed in a feature matches the team's official recommendations before adopting it (`mob-feature-build` step 2).
- Finding a ready Cookbook solution for a specific problem (lists, animation, networking, storage...).
- Extracting a recommendation from an official video (Widget of the Week, Decoding Flutter...) as supporting evidence.

**Do not invoke** for: Laravel/React questions (out of scope), or executing code itself (that's `mob-feature-build`) — this is a search-and-citation gateway only.

## 📥 Required inputs (Inputs) ⬛
- **RCCF work order** of the parent task (Law 5) — research runs within its cycle.
- The question/topic in specific form (widget name, problem, pattern) — "everything about Flutter" is not a question.

## 🔧 Steps (Steps) ⬛
1. **Route the question to the right source** (read the suitable index first — never sweep folders):
   | Need | Source | Index |
   |--------|--------|--------|
   | How do I do X practically? (ready recipes) | `docs/cookbook/` | skills index `.opencode/skills/INDEX.md` |
   | Architecture/state/data/testing/perf guidance | `docs/{app-architecture,data-and-backend,testing,perf}/` | skills index `.opencode/skills/INDEX.md` |
   | Platform integration/native/add-to-app | `docs/{platform-integration,add-to-app,deployment}/` | skills index `.opencode/skills/INDEX.md` |
   | Dart language / Effective Dart / null-safety / interop | `dart/{language,effective-dart,null-safety,interop,libraries}/` | index `.opencode/skills/INDEX.md` |
   | Concept/widget explained by video | `videos/<id>__<slug>.md` + `playlists/<nn>/_playlist.md` | `INDEX.md` |
2. **Search precisely:** grep with English keywords against the target path only (e.g., `grep -rn "SliverAppBar" <kb>/docs/ui/`) then read only candidate files — no random reading.
3. **Prioritize answer sources:** flutter.dev/dart.dev docs = governing reference; video = clarification and support (its speech-to-text transcripts contain expected typos). Conflict between them → written docs govern, and log the conflict.
4. **Check freshness for version/API-sensitive content:** if the pattern looks old, run `python3 <kb>/scripts/refresh_docs.py --no-fetch` to check last sync, or explicitly warn that the source is dated by file date.
5. **Answer with full citation (Law 4):** every technical claim ← `<kb-relative-path>:line` (e.g., `docs/app-architecture/case-study.md:42`). An uncited claim = rejected. What you cannot find in the base, say so plainly: "not found in available knowledge" — never fabricate.
6. Produce the evidence block via `sofi-evidence`.

## 📤 Outputs + evidence (Outputs & Evidence) ⬛
- **Output:** a sourced answer/recommendation: the practical takeaway + the recommended official pattern + source caveats if any.
- **Evidence (Law 4) — Researcher type** via `sofi-evidence`:
  - Per claim: file path within the base + line number + literal quote/excerpt.
  - The executed search command (grep) + result count.
  - Explicit statement of what was **not** found in the base (gaps are stated, never hidden).

## 🔗 Handoff ⬛
- Deliver results to **your room lead `mob-lead`** only (Law 3) via the `sofi-handoff` skill.
- No direct delivery to the user, nor addressing another room directly (Law 2).

## ⛔ Constraints ⬛
- This skill searches and cites — **never modifies project code** nor invents architectural decisions (that belongs to their owners).
- Video transcripts are not literally reliable (speech-to-text) — never quote code from them verbatim without verifying against written docs.
- Never load huge random files — reading is index-guided exclusively (agent context is limited).
- The base sits outside SOFI's tree: read-only, write only through the official refresh scripts (Law 10).
- Never override any of the thirteen laws.

## 🧠 Memory ⬜
- Critical patterns whose recommendations carried important decisions → log the reference with the decision in project memory `projects/<name>/brain/DECISIONS.md` (Law 7).

## 📚 References ⬜
- Base: `/home/es3dlll/flutter-knowledge-base` — `identity/public-readme.md` (structure + updates), `INDEX.md`, skills index `.opencode/skills/INDEX.md`.
- Refresh: `scripts/refresh.py` (YouTube) · `scripts/refresh_docs.py` (flutter.dev) · `scripts/refresh_dart.py` (dart.dev) — all support `--no-fetch`.
- Sibling Flutter skills: `mob-feature-build` (execution), the official `flutter-*` set (22 skills from flutter/agent-plugins).
- **Owner (Law 9):** Mobile room 07 — `mob-lead`.
