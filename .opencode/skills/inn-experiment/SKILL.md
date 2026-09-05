---
name: inn-experiment
description: >-
  Innovation experiment protocol — tech scouting + experiment design + PoC + ADR drafting in the isolated sandbox (audit P2 gap). Triggers — "PoC this", "innovation ADR", "tech scout", "sandbox experiment", "evaluate emerging tech". Invoked by inn-lab-lead (room 16) on any new PoC request — never for production code (use bck-feature-build) or R&D (use res-journey-map).
---

# inn-experiment — Innovation Experiment Protocol

> **Core value:** safe experimentation — sandboxes, PoCs, ADR drafting — all in isolation, never touching production (Law 10 + Innovation charter).

## 🎯 When to invoke (When) ⬛
- A new technology needs PoC validation
- An ADR experimental is requested by `brd-cto` or `brd-cso`
- A PoC needs structured design + measurement

**Do not invoke** for: production code (use bck-feature-build) · user research (use res-journey-map) · security classification (sec-threat-model).

## 📥 Required inputs (Inputs) ⬛
- RCCF work order from `inn-lab-lead` (Law 5) — `brd-cto` + `brd-cso` approval attached
- Sandbox path: `hq/engine/sandbox/<tech>/` or `projects/innovation-lab/<slug>/`
- Success metric: measurable, e.g. "model serves <100ms p95 with 90% accuracy"

## 🔧 Steps (Steps) ⬛
1. **Scout:** `inn-tech-scout` writes tech brief at `hq/brain/knowledge/innovations/<tech>.md` — `file:line` per claim
2. **Design:** `inn-lab-lead` writes experiment design + PoC scope — ADR template
3. **Isolate:** experiment in sandbox — NO production touch (Law 10)
4. **Measure:** `inn-ml-engineer` (if ML) or `inn-tech-scout` runs PoC — exit code + timing
5. **ADR draft:** `inn-lab-lead` writes experimental ADR with go/no-go
6. **Archive or promote:** either archive (experiment done) or promote to `brd-cto` for fateful ADR

## 📤 Outputs + evidence (Outputs & Evidence) ⬛
- Output: experiment design + PoC results + ADR draft
- Evidence (Law 4): `sofi-evidence` — `file:line` + `exit code` + sandbox isolation check
- Handoff: `sofi-handoff` ticket to `inn-lab-lead` → `brd-cto`

## 🔗 Handoff ⬛
- Deliver to `inn-lab-lead` only (Law 3)
- No direct delivery to user · no other-room addressing (Law 2)
- `brd-cto` is the only path to production promotion

## ⛔ Constraints ⬛
- **Sandbox only** — no production touch (Law 10 + Innovation charter)
- Free only (INT-0003) — no paid API
- License (Law 15) via `sec-license-auditor` before any new dependency
- Security: `sec-threat-model` review before any PoC touching real data

## 🧠 Memory ⬜
- Per Law 7: innovation logs in `hq/brain/knowledge/innovations/`
- Project innovations in `projects/innovation-lab/<slug>/brain/`

## 📚 References 📚
- `hq/core/domain/rooms/16-innovation/charter.md:1` · `.opencode/skills/qa-test-plan/SKILL.md` (PoC test design) · `hq/core/standards/latest-tech-2026.md`
