---
type: brain
mem: procedural
prj: PRJ-CADDY
---
# DECISIONS — PRJ-CADDY · ADR log

> One `## ADR-NNN` block per decision.
> Every irreversible decision carries a rollback plan or it is rejected (hq/core/CONSTITUTION.md — Law 8: Quality before Speed; procedure: hq/core/PROTOCOLS.md).
> Date comes from the RCCF Work Order approved by brd-ceo — agents never invent timestamps. Rationale is never compressed.
> This file is the per-project ADR log; HQ's own active ADR chain lives in hq/brain/CORTEX.md.

## ADR-000 (2026-08-24) — Project charter accepted
**By:** brd-ceo
**Decision:** PRJ-CADDY enters the mandatory pipeline under the Nine Binding Laws (hq/core/CONSTITUTION.md); protocols per hq/core/PROTOCOLS.md.
**Why:** every project starts under its governing law, never with code.
**Reversible?** yes — project can be archived before first delivery at zero downstream cost.

## ADR-001 (2026-08-24) — Birth of the "unified control center" and its exclusive scope
**By:** the owner (four-option quiz + explicit endorsement "yes, correct") — executed via the gateway following the documented channel-outage precedent
**Decision:**
1. The project = a unified control center owning the global and live domain layer for all SOFI projects (reverse proxy / TLS / vhosts) — replacing configuration scattered outside the system (`/etc/caddy/Caddyfile` outside git).
2. **Non-goals:** no touching any live configuration at this stage — `/etc/caddy/Caddyfile` remains untouchable until a separately approved migration ticket passes G3 and full testing.
3. Local caddy inside each project for development (`<project>/docker/caddy/Caddyfile`) stays as-is per DEVOPS-STANDARD.md:28-29 — this project does not replace it but complements it with a global layer; detailed reconciliation via an ADR inside the design.
4. The project's predecessor `hq/engine/` (empty caddy/sites + README): the archival plan was replaced by **permanent deletion on the owner's order during execution** ("I deleted it, I don't want it") — along with deleting the entire `hq/archive/` folder. The owner overrides any plan; documented after the fact.
5. Internal project structure: **`site/`** for the domains work order (*.caddy files) — verbatim naming directed by the owner ("for caddy in the project it should be caddy/site").
**Why:** a documented owner decision across four candidate options, all answered: comprehensive system audit · unified control center · migrate live after building, not immediately · move hq/engine/caddy and archive in place. Live configuration outside git = a single ungoverned risk source (lesson SES-20260822-01: a demo page broke because of an out-of-repository reference nobody audited).
**Rollback plan:** the project is a fully reversible paper birth — delete `projects/caddy/`, restore `hq/engine/` from the archive, and restore the three modified lines in documentation. Zero impact on any live system.
**Reversible?** yes — zero cost before the first live migration; after any live migration cost escalates and requires a rollback runbook specific to that ticket.

## ADR-002 (2026-08-25) — "sakk only" restructuring: sites/ + sites-disabled/ + pool reduction
**By:** the owner — direct execution order for the cleanup plan (`.kilo/plans/1787677024434-sofi-cleanup-caddy-docs-plan.md`), security gate documented by delegation in `cleanup-workspace/reports/GATE-APPROVAL.md`
**Decision:** the main file became short (shared snippets + `http://:80 → 404` guard + `import sites/*.caddy`); sakk's configuration moved verbatim into `sites/sakk.caddy`; the jw/wa/tobacco/wildcard/localhost blocks were disabled by verbatim relocation into `sites-disabled/`; non-sakk fpm pools moved to `php-fpm/disabled/` (live disabling pending `sudo bash php-fpm/disable-pools.sh`); `site/` replaced by `sites/` per the newer 2026-08-25 plan superseding the 2026-08-24 note; the empty `docs/` removed; `README-LIVE.md` merged into `OPERATIONS.md`.
**Why:** a single active scope shrinks the security surface and makes adding a future domain = one file in `sites/`, never touching the main file.
**Reversible?** yes — the complete original is archived with an sha256 fingerprint in `../SOFI-archive-20260825-2040/caddy/` alongside `restore.sh`; rollback = restore the old Caddyfile + reload (under two minutes).
**Evidence:** validate exit=0 · graceful reload via admin API · sakk.local→200/1ms · sakk.zanjour.com→200/1.7s · jw/tobacco.local→clean 404 · public /admin→404 · caddy error log empty.
