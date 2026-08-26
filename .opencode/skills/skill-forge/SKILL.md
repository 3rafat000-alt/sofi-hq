---
name: skill-forge
description: >-
  SOFI's self-build skill factory. Use it to build/update/validate any SOFI skill (.opencode/skills/<name>/SKILL.md) so it matches the constitution — Laws 3/4/5 (hierarchical delivery, evidence, RCCF). Triggers — "build a skill", "create SOFI skill", "scaffold skill", "author a room playbook", "forge skill", "validate skill". For any room lead who wants their room to author its own skill instead of waiting for a ready-made one.
---

# skill-forge — The Self-Build Skill Factory

> **Core idea:** the team builds its own skills. No waiting for external ready-made ones. Every room knows its craft — this factory converts that knowledge into an invocable skill matching SOFI's constitution.

---

## 🎯 When to invoke this skill (When)

- A room lead wants to create a new skill for their room (a craft playbook, recurring workflow, review standard).
- Updating an existing skill (new version, expanded triggers, fixing a constitutional violation).
- Validating a skill before approval.
- Converting successful recurring work into a permanent skill (instead of reinventing it every session).

**Do not invoke** for executing an ordinary task on a project — this builds *capabilities*, it doesn't consume them.

---

## 🏭 The Forge Loop — 6 steps

### 1. Identify
- **Name (`name`):** kebab-case, prefixed with the room code if a room skill: `str-`, `res-`, `dsn-`, `arc-`, `bck-`, `fnt-`, `mob-`, `dat-`, `sec-`, `qa-`, `ops-`, `obs-`, `knw-`, `gtw-`, `brd-`. Examples: `sec-threat-model`, `qa-test-plan`.
- Skills shared across rooms start with `sofi-`: e.g., `sofi-evidence`.
- **Owner:** exactly one responsible room (Law 9 — chain of responsibility). Record it in the table below and in `hq/brain/owners-matrix.yaml` if present.

### 2. Write the trigger (Description)
- The `description` field = *when* it is invoked, not *what* it does. It decides invocation.
- Provide invocation triggers in English (per workspace language policy). Use real phrases users/leads actually say.
- Be specific: a skill invoked by everything = invoked by nothing useful.

### 3. Scaffold
Copy `references/TEMPLATE.md` and fill the sections. Never delete a mandatory section (marked ⬛).

### 4. Compliance inject — mandatory
Every SOFI skill **must** remind its user of the laws governing its outputs:
- **Law 4 (Evidence):** every output produces an evidence block (file:line / exit code / URL+extract / screenshot). ← link to the `sofi-evidence` skill.
- **Law 3 (Hierarchical handoff):** output goes to the room lead, not directly to the user. ← link to the `sofi-handoff` skill.
- **Law 5 (RCCF):** no execution without a work order; the skill reminds about requesting an RCCF when missing.
- **Law 2 (Isolation):** the skill never has an agent address another room directly.

### 5. Validate — the gate checklist
Run the skill through `references/STANDARD.md` § "Validation Checklist". Any failed item = the skill is rejected (not approved).

### 6. Register
Add a row to `.opencode/skills/INDEX.md`: `| name | room | trigger-hook |`. Update the ownership table. Log the decision in `hq/brain/cortex-decisions.md` (approving a skill = an important decision, Law 7).

---

## 📐 Template and standard (Reference Files)

- `references/TEMPLATE.md` — the ready structure for any `SKILL.md`. Always start from it.
- `references/STANDARD.md` — the authoring law + full validation checklist.
- The installed `skill-creator` skill (anthropics) — a supporting tool for building/improving/measuring skills; feeds skill-forge as registered in `INDEX.md`, final approval remains through this factory loop.

Read the reference file **before** writing, not after.

---

## 🧩 SOFI Skill Taxonomy

| Type | Description | Example |
|-------|-------|------|
| **Playbook** | a recurring craft workflow for a room | `sec-threat-model`, `qa-test-plan` |
| **Standard** | an enforced standard/checklist | `sofi-evidence`, `fnt-a11y-audit` |
| **Generator** | generates structured output | `arc-adr`, `knw-doc-writer` |
| **Meta** | builds/governs other skills | `skill-forge` (this one) |

---

## ⛔ Factory limits (Constraints)

- A skill never overrides any of the thirteen laws. A skill "saving time" by skipping the CEO or delivering directly = **rejected L4**.
- One skill = one responsibility. No "does everything" skill.
- No duplication: before building, search `INDEX.md` for a skill covering the same purpose — update it instead of duplicating.
- A skill is guidance text only — it grants no new permissions and never overrides roles defined in `.opencode/agent/`.

---

## 🗂️ Skill ownership table (Ownership — update with every new skill)

| Code | Room | Owning lead | prefix |
|-----|--------|----------------|--------|
| 00 | Boardroom | brd-ceo | `brd-` |
| 01 | Strategy | str-lead | `str-` |
| 02 | Research | res-lead | `res-` |
| 03 | Design | dsn-lead | `dsn-` |
| 04 | Architecture | arc-lead | `arc-` |
| 05 | Backend | bck-lead | `bck-` |
| 06 | Frontend | fnt-lead | `fnt-` |
| 07 | Mobile | mob-lead | `mob-` |
| 08 | Data | dat-lead | `dat-` |
| 09 | Security | sec-lead | `sec-` |
| 10 | Quality | qa-lead | `qa-` |
| 11 | DevOps | ops-lead | `ops-` |
| 12 | Observability | obs-lead | `obs-` |
| 13 | Knowledge | knw-lead | `knw-` |
| 14 | Gateway | gtw-dispatcher | `gtw-` |
| — | Shared (all rooms) | knw-lead (custodian) | `sofi-` |

---

*The skill factory belongs to the Knowledge room (13). Every skill built with it is subject to the ten governing laws. Last updated: 2026-07-17.*
