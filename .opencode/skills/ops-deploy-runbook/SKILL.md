---
name: ops-deploy-runbook
description: >-
  When shipping a release to production safely with a rollback plan. Triggers — "deploy
  the release", "run the deployment", "deploy to production", "run migration and deploy", "health check
  after deployment", "prepare rollback", "roll out the update to production", "cut operating
  cost". English: "deploy release", "run deployment", "ship to production",
  "run migration then deploy", "post-deploy health check", "prepare rollback
  plan", "release runbook", "optimize infra cost". Invoked inside the Operations room to execute a disciplined production release — not for writing feature code nor designing infrastructure from scratch.
---

# ops-deploy-runbook — The Safe Deployment Playbook ⬛

> Turns an approved release into a production deployment that tolerates no surprises: CI/CD → migration → deploy on the live tree → health check → rollback plan ready before touching production → cost optimization — every step documented with evidence.

## 🎯 When to invoke (When) ⬛
- A release passed the quality gate and needs production deployment (the production path is defined by the project's RCCF; usually inside `projects/<name>` or its live path if hosted externally).
- Database migrations must run before/with deployment with rollback guaranteed.
- A post-deployment health check, a formal rollback plan, or an operating-cost review was requested.
**Do not invoke** for: writing feature code (Backend/Frontend rooms), designing cloud infrastructure from scratch (`arc-infra-architect`), or diagnosing an ongoing production incident (Observability room 12).

## 📥 Required inputs (Inputs) ⬛
- RCCF work order (Law 5) — no deployment without it; defines version, scope, and deployment window.
- The approved release: tag/commit passing the quality gate (Gate-5) + green CI log.
- Required migrations (if any) + a matching rollback script for each.
- Target environment: the production path defined by the project's RCCF, `.env` (single copy), health-check criteria (endpoint + expected exit code).
- Authority confirmation: agents operate **without sudo** — any step requiring elevated privileges is escalated, never executed.

## 🔧 Steps (Steps) ⬛
1. Read the RCCF; fix version, migrations, deployment window, and health-check success criterion.
2. **CI/CD:** verify the pipeline is green for this commit (test + build) — pipeline building/maintenance via `cicd-pipeline-skill` (ops-cicd-engineer). Capture result log + exit code.
3. **Prepare rollback first (before any change):** note the current production tag/commit + rollback script per migration. Never continue without a written rollback plan.
4. **Migration:** run it inside a transaction where possible; log the executed command + exit code + affected row/table counts.
5. **Deploy directly onto the live production tree** (Law 10 — no worktree, no isolated copy): update files, set permissions, reload Caddy via the available non-sudo means (`caddy reload` within your permissions, or escalate).
6. **Health check:** call the health endpoint + inspect Caddy service; log HTTP response + exit code. Any failure → execute the step-3 rollback immediately and restore state.
7. **Cost optimization:** review resource consumption after stabilization (size, cache, assets); record recommendations without executing anything touching production outside the RCCF scope.
8. Review completeness internally (Law 8), then produce the evidence block (below) via the `sofi-evidence` skill.

## 📤 Outputs + evidence (Outputs & Evidence) ⬛
- Output: a stable production deployment on the RCCF-defined path + applied migrations + green health check + documented rollback plan + cost recommendation.
- **Evidence (Law 4) — DevOps type:** use the `sofi-evidence` skill:
  - **deploy log**: CI/CD, deployment, and migration commands, each with its `exit code` (Law 4), plus the deployed tag/commit.
  - **health check**: health endpoint response + Caddy status (HTTP status + exit code + timestamp).
  - **rollback plan**: previous tag/commit + rollback script per migration + restore command, ready and logically tested.
  - `file:line` for any modified configuration file (Caddyfile, `.env`, deployment scripts).

## 🔗 Handoff ⬛
- Deliver deployment + evidence block to the **room lead `ops-lead`** only (Law 3) via the `sofi-handoff` skill as an RCCF ticket.
- Only `ops-lead` consolidates and delivers upward to `brd-ceo`. No direct delivery to the user, nor addressing another room (Law 2).
- Explicit acceptance closes the release deployment.

## ⛔ Constraints ⬛
- No deployment without a written rollback plan, logically tested before touching production — non-negotiable.
- Work directly on the project's production tree only — no worktree, no isolated branch, no side copies (Law 10; documented worktree precedent).
- Agents have no sudo: any step requiring root privileges escalates to `ops-lead`; never worked around.
- One `.env` copy — never duplicated and its secrets never exposed in logs or evidence.
- No deployment without green CI and a valid RCCF; emergencies only with explicit CEO authorization (Law 8).
- Never override any of the thirteen laws.

## 🧠 Memory ⬜
- Record the deployment decision (version, migrations, health check result, rollback plan) in `hq/brain/cortex-decisions.md`; failures/rollbacks in `hq/brain/amygdala-incidents.md` (Law 7).

## 📚 References ⬜
- `hq/core/contracts.md` → Operations contracts (deployment/delivery).
- `hq/core/protocols.md` → P-02 (delivery), P-03.8 (DevOps evidence types).
- Shared skills: `sofi-evidence`, `sofi-handoff`.
- Documented precedent — Caddy serves production; agents operate without sudo.
- **Owner (Law 9):** DevOps room 11-devops — `ops-lead`.

## ⬛ Linear Program v2 (OWNER-DIRECTIVE-2026-0823-R2)
Stage map: S1 intake(00·01·14) → S2 experience(02·03) → S3 foundation(04·08) → S4 backend/OpenAPI(05) → S5 unified Flutter/Dart dual interfaces(06·07) → S6 shield operations(09-13).
**Your position: S6** — disciplined deployment with a mandatory rollback plan **written before execution**.
Migrations on production proceed carefully and ordered, coordinated with the Data room (08).
Next.js builds follow `hq/core/standards/nextjs-standards-legacy.md`. *(legacy only — existing projects non_retroactive · R2)*
Caddy changes touch live production: no change without a config backup and post-application validation.
Secrets scrubbed before any external push (GitHub/Cloudflare) with Security approval (09).
Laws: OpenAPI-first · cross-boundary mocks forbidden (internal testing substitutes exempt) · Envelope `hq/core/standards/api-envelope.md` · capsule `hq/core/standards/ddd-capsule.md`.
Delivery: `sofi-handoff` + `sofi-evidence` with a full deployment log including exit codes.
