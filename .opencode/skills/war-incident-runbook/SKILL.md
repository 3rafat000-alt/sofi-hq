---
name: war-incident-runbook
description: >-
  WarRoom P0 incident runbook — detection → triage → containment → rollback → comms → postmortem (audit P0 gap). Triggers — "P0 incident", "production down", "data breach", "rollback fire", "war room", "AMYGDALA log". Invoked by war-incident-commander (room 15) on any P0 — never for non-emergency (use obs-incident-response).
---

# war-incident-runbook — WarRoom P0 Incident Runbook

> **Core value:** MTTR drive under P0 pressure — freeze + rollback + communicate + postmortem in one disciplined flow.

## 🎯 When to invoke (When) ⬛
- A P0 incident is declared (SEV-1, security breach, production down)
- `obs-incident-commander` or `sec-incident-responder` raises the alert
- `brd-ceo` issues emergency RCCF

**Do not invoke** for: non-P0 incidents (use `obs-incident-response`) · planned maintenance · general change management.

## 📥 Required inputs (Inputs) ⬛
- Emergency RCCF from `brd-ceo` (Law 5) — `war-incident-commander` is the field commander
- The live incident: scope + affected services + initial signals
- The rollback plan (from `ops-deploy-runbook` — pre-staged)

## 🔧 Steps (Steps) ⬛
1. **Declare:** `war-incident-commander` takes command — Law 14 freeze on affected RCCFs
2. **Triage:** `war-forensic-analyst` collects evidence (hash before touch) — `file:line` + `exit code`
3. **Containment:** `war-rollback-engineer` activates rollback window per `ops-deploy-runbook` — health check
4. **Communicate:** `war-communication-lead` briefs owner every 30 min (Law 11 Arabic simple) + every team
5. **Recover:** restore service + verify with live health checks
6. **Postmortem:** within 24h — `hq/brain/amygdala-incidents.md` + re-evaluate linked Gate

## 📤 Outputs + evidence (Outputs & Evidence) ⬛
- Output: incident closure + AMYGDALA entry + postmortem + Gate re-eval
- Evidence (Law 4): `sofi-evidence` — `file:line` per forensic finding + `exit code` per rollback
- Handoff: `sofi-handoff` ticket to `war-incident-commander` → `brd-ceo` (Law 3)

## 🔗 Handoff ⬛
- `war-incident-commander` is the field commander — brd-ceo signs closure
- No direct delivery to user — via `war-communication-lead` → `brd-ceo` → user
- AMYGDALA log is mandatory — never hide an incident (Law 6 + Law 7)

## ⛔ Constraints ⬛
- **Advisory only in normal times** — P0 = `war-incident-commander` commands the field
- **Law 14 freeze** — no third blind attempt
- **No rollback without documented plan** (per `ops-deploy-runbook`)
- **Communication every 30 min** even if "still investigating"

## 🧠 Memory ⬜
- Per Law 7: AMYGDALA is the org incident log — never delete, always snapshot
- `hq/brain/amygdala-incidents.md` + per-incident file

## 📚 References 📚
- `hq/core/domain/rooms/15-warroom/charter.md:1` · `.opencode/skills/obs-incident-response/SKILL.md` (inherits) · `.opencode/skills/ops-deploy-runbook/SKILL.md` (rollback) · `hq/brain/amygdala-incidents.md`
