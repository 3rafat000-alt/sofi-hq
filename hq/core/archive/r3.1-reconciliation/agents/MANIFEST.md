# MANIFEST — R3.1 Reconciliation Archive (agents)

**FILE: hq/core/archive/r3.1-reconciliation/agents/MANIFEST.md**
**Date:** 2026-09-05 · **Owner:** knw-lead (Knowledge room) · **Decision:** brd-ceo verdict (Task, 2026-09-05 — conditions أ/ب/ج/د) · **Phase-B releaser:** brd-ceo (single source for un-archiving any entry below)
**Math closed:** 115 disk agents → 6 renamed (dat→arc, kept live in `.opencode/agent/`) + 7 archived here = **108** = registry.yaml `total_agents: 108`.

Every archived file is byte-identical to its live counterpart at archive time (sha256 equal before/after — Law 4 evidence). No live reference relies on any dat-* name as a working entity after Phase A (ب-5). The 6 dat→arc renames remain physically in place (`.opencode/agent/arc-*.md`) — see `hq/core/archive/r3.1-reconciliation/FINDINGS.md:60-62` for the old←new map.

## Archived files (7)

| # | File (previous live path) | Reason for archival | Decision | Owner | sha256 (before = after) |
|---|---------------------------|---------------------|----------|-------|--------------------------|
| 1 | `dat-lead.md` (`.opencode/agent/`) | Room 08 (Data) merged into Room 04 (Architecture) per Amendment R3.1 — the lead role is now absorbed by `arc-lead`; registry has no dat-* room | Archive (retire lead of merged room) | knw-lead → absorbed by arc-lead | `4e155f86ab9ad7e18ce0a6a840b096fdbbbb65499ed18ab8e4720b0ae3b0078d` |
| 2 | `dsn-content-strategist.md` | Retired in R3.1 room-charter trim (05-design reduced roster) | Archive (retired) | R3.1 | `ef027e2dac20ce4d1845853e44761b9523bd3312915a6a533290539f91faf708` |
| 3 | `dsn-motion-designer.md` | Retired in R3.1 room-charter trim | Archive (retired) | R3.1 | `c8b5577f74c19e9105266c5929a15b82f36ba9c52179f2a1ba9e079bd3e70aaf` |
| 4 | `fnt-vue-engineer.md` | **Banned role** — Vue.js banned by Stack Lock (owner order R3, 2026-09-04): Frontend = React 18+ EXCLUSIVE | Archive (vetoed role) | Stack Lock R3 (brd-ceo) | `9b207abb0ee9a6bcbeb91954b88de911888ff7d99596e39b44f3bff86255337c` |
| 5 | `res-data-researcher.md` | Retired in R3.1 room-charter trim (02-research roster) | Archive (retired) | R3.1 | `491da3432b91cf26f9499e03396a5b83278ac43e0b49453bff957cef1326acee` |
| 6 | `res-web-scout.md` | Retired in R3.1 room-charter trim | Archive (retired) | R3.1 | `a7cab05b13ad3281750ad3e5fca991efb9bdd015d7e28cb1de3aa0f004986347` |
| 7 | `qa-flutter-architect.md` | **Never registered** — no entry in `hq/core/nexus/registry.yaml` (never existed in any legal roster of 14 rooms / 108 agents); created by an uncertified parallel session (ADR-20260905-GTW-FLUTTER-QA-ARCHITECT `hq/brain/cortex-decisions.md`) | Archive (illegitimate record) | qa-lead (rejected role) | `31f62a093ab46ca1f10bf2b6ae301c84fa57ef4beea51c2e8abeca6b13d746c3` |

## Sibling skill directory (stays physically — WARN per ج-1, released in Phase B)

| Path | Note |
|------|------|
| `.opencode/skills/qa-flutter-architect/` | Skill dir created by the same parallel session; not indexed in `.opencode/skills/INDEX.md` (disk=111 vs INDEX 109 — PENDING-PHASE-B). Kept physically; **Phase-B ticket OPS-R3.1-B**: index reconciliation decision. Do not delete in Phase A. |

## Relation to Phase B (brd-ceo verdict ج-5)

This archive is **Phase A** output. The following are **Phase-B** items tracked by this MANIFEST (released only by brd-ceo):
1. Capsule migration `hq/core/domain/rooms/08-data/` → `04-architecture/` (7 dat-* capsule dirs + 08-data room dir).
2. Capsule cleanup for the 5 retired agents + dat-lead under their former rooms (12 dirs — they remain physically as PENDING-PHASE-B).
3. Body cleanup of the 6 renamed `arc-*.md` files (identity lines only were changed in Phase A per verdict أ-2; bodies still carry Data-room references → arc-lead).
4. `hq/core/system-state-current.md` → 14 rooms / 108 agents.
5. `AGENTS.md:258` phrasing fix ("113→108" arithmetic error — reality 114→108 = −6).
6. `.opencode/skills/INDEX.md` reconciliation (disk 111 + qa-flutter-architect entry) + residual constant removal from guards (14/108 stopgap constants lifted when B lands).

## Evidence
- sha256 before: `hq/core/archive/r3.1-reconciliation/agents/sha256-before.txt` · after: `hq/core/archive/r3.1-reconciliation/agents/sha256-after.txt` (identical hashes — captured 2026-09-05)
- git status final = renames/archives only (zero-deletion proof, ب-4) — capture in delivery evidence block.