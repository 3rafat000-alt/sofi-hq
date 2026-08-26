---
name: dat-schema-migration
description: >-
  When to invoke: for any change to the production database schema. Triggers
  — "schema change", "write a migration", "add/drop column", "alter table",
  "data migration", "safe production migration", "rollback plan for DB",
  "modify the schema", "add a table/column", "change a column type",
  "drop a column". Invoked when modifying data structure directly on the main
  production tree — not for ordinary queries nor cache tuning.
---

> **⚠️ The critical track is mandatory (INT-GTW-024):** every migration on the production database = always critical under Law 1 however small it looks: intake → brd-ceo → Board consultation via `brd-decision-gate` → brd-cso veto applies → explicit RCCF work order. Never a fast track and never direct execution.

# dat-schema-migration — The Schema Change Playbook ⬛

> Changing the production schema safely: design → privacy check → ETL → rollback → supervised execution, without losing any critical security migration.

## 🎯 When to invoke (When) ⬛
- Modifying the production database structure: adding/removing/altering a table, column, index, constraint, or enum.
- Migrating data between two schemas or converting types that touch existing rows.
- Writing a new migration that needs a rollback plan before merging.
**Do not invoke** for: read/report queries (analytics), cache/TTL tuning, or single-row data edits with no structural change.

## 📥 Required inputs (Inputs) ⬛
- An RCCF work order (Law 5) — no execution without it.
- The current target schema + the text of the requested change (affected tables/columns).
- The production environment and the location of migrations on the main tree (Law 10 — no worktrees, no isolated copies).
- Classification of affected fields (do they hold PII/KYC?) — settled with dat-privacy-officer before execution.

## 🔧 Steps (Steps) ⬛
1. Design the migration explicitly forward plus its backward counterpart (up/down); no destructive change without a transition phase (expand → migrate → contract).
2. Review sequence conflicts: compare the latest migration on production against what you are writing — **never skip or drop a critical security migration** (SOFI precedent: KYC encryption, FK repair, enum conversions lost in a forgotten worktree merge).
3. Run the PII/privacy check through dat-privacy-officer: any sensitive column needs encryption/masking before migration.
4. Design the ETL for data migration when needed (backfill/transform), restartable (idempotent) with row-count measurement.
5. Write a tested rollback plan: how state is restored, and at which restore point/backup.
6. Execute on production inside a transaction wherever possible, in this order: backup → up → verify → (failure ⇒ down); test data-pipeline code (ETL/backfill) via `pytest-skill`/`unittest-skill`.
7. Produce the evidence block (see below).

## 📤 Outputs + evidence (Outputs & Evidence) ⬛
- Output: migration file(s) (up/down) + ETL script if any + rollback plan + production execution report.
- **Evidence (Law 4):** Engineer/Architect type — use the `sofi-evidence` skill:
  - **migration plan / ADR:** affected tables + expand-migrate-contract strategy + before/after diagram.
  - **file:line** for every changed migration/ETL file.
  - **exit code** for every executed command (up, backfill, verify, down during testing) + migrated row counts.
  - **rollback plan**, tested: the restore command + backup point + proof of successful restoration.
  - Post-execution verification log/screenshot (schema diff + count checks).

## 🔗 Handoff ⬛
- Deliver output to the **room lead (dat-lead)** only (Law 3) via the `sofi-handoff` skill.
- No direct delivery to the user. No addressing another room directly (Law 2) — coordinate with any room through the lead.

## ⛔ Constraints ⬛
- Direct execution on the main production tree only (Law 10). Worktrees or long-lived isolated branches forbidden.
- No execution without a documented backup and a tested rollback plan.
- No dropping/destroying a PII-bearing column without dat-privacy-officer approval.
- Never override any of the thirteen laws.

## 🧠 Memory ⬜
- Record the schema decision and rollback plan in `hq/brain/cortex-decisions.md`; any migration incident goes to AMYGDALA (Law 7).

## 📚 References ⬜
- `hq/core/contracts.md` — the data contract · `AGENTS.md` Law 10 (the documented worktree precedent).
