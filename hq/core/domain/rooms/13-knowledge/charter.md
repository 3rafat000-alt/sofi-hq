# Knowledge Room

> **⚡ Structural update 2026-08-25 — read first:** The system structure and operating model have changed ("sakk only" cleanup + root simplification + archival of institutional memories). The updated binding source is `hq/core/system-state-current.md` — interpret any legacy path in your texts against it.
**Room:** 13-knowledge
**Code:** knw
**Room lead:** `knw-lead`

---

## | Identity

**Purpose:**
Knowledge management, documentation, institutional memory, reflection

**Agent count:** 6

---

## | Agent Roster

- `knw-lead` — lead
- `knw-brain-query` — brain-query
- `knw-doc-writer` — doc-writer
- `knw-historian` — historian
- `knw-memory-curator` — memory-curator
- `knw-reflector` — reflector

**Operational agent definitions:** `.opencode/agent/` — the single source of truth.

---

## | Standard Operating Procedure (SOP)

1. Document major decisions
2. Organize knowledge
3. Answer agent inquiries
4. Reflect and review lessons learned
5. Update CORTEX

---

## | Connected Rooms

All rooms

---

## | Gate Ownership

**My stage in production line v2:** supports all stages — CORTEX documentation at closures — full map at `nexus/gates.yaml#stage_map`.

All stages (support)

---

## | Handoff Protocol

1. The agent completes its task and records evidence
2. The agent hands off to the room lead
3. The room lead reviews and unifies
4. The room lead hands off to brd-ceo
5. brd-ceo delivers to the user

**Forbidden:**
- An agent delivering directly to the user
- An agent addressing another room
- A room lead executing the work personally

---

## | Skills

- **Room playbook:** `knw-brain-write` + `skill-forge` — invoked through the Skill tool for room tasks.
- **Shared (mandatory):** `sofi-evidence` (Law 4) before any delivery · `sofi-handoff` (Law 3) for every hierarchical handoff.
- **External room skills:** `skill-creator` · `docx` · `pdf`⚠️High · `pptx` · `xlsx` · `doc-coauthoring`
- **Full map:** `.opencode/skills/INDEX.md`.

---

## | Room Law

The Knowledge Room operates within the bounds of the constitution (hq/core/constitution-master.md).
All decisions comply with the Room Isolation Law.
Communication with other rooms happens through the room lead only.

**Memory Consolidation Ritual — knw-reflector (Axis 8 fix 2026-08-31 · P-06.7):** `knw-reflector` (Shatha Al-Sirraj) executes `python3 hq/core/tooling/memory_summarizer.py` as a binding ritual:
- **Trigger:** every 10 agent turns (P-06.7) + every Gate-8 closure + whenever `hq/brain/hippocampus-sessions.md` >800 lines or `hq/brain/amygdala-incidents.md` >600 lines (token-burn guard).
- **Actions:** keep last 5 sessions in full in hippocampus, summarize older to 1-line each; deduplicate repeated amygdala escalations (e.g., ticket #1 spam) keeping first 2 + last 2; never touch `hq/brain/cortex-decisions.md` (permanent). Backup to `.md.bak.YYYYMMDD` before compaction.
- **Evidence:** `hq/core/tooling/memory_summarizer.py --check` exit code + before/after line counts + bak filename logged to `hq/brain/cortex-decisions.md` + `hq/brain/hippocampus-sessions.md` header.
- **Failure = L1 for knw-lead** (skipped consolidation per P-06.7) — token burn without ritual is a violation.

**Documentation Link Hygiene — knw-doc-writer (Axis 9 fix 2026-08-31 · Gate-6):** `knw-doc-writer` runs `python3 hq/core/tooling/law13_path_guard.py` + `python3 hq/core/tooling/evidence_guard.py --staged --strict` at every Gate-6 (Staging) closure and at UAT sign-off. Every internal `.md` link must resolve to a real home (Law 13); every `file:line` must exist (Law 4). Broken links = Gate-6 blocked until fixed. Index freshness is verified via `hq/core/standards/room-dod-and-execution-rules.md` DoD for Knowledge room.
