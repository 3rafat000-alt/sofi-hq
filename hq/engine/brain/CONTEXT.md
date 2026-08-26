---
type: brain
mem: semantic
prj: PRJ-CADDY
---
# CONTEXT — PRJ-CADDY · Project Context

> A lightweight fact ledger, updated manually under the binding laws (`hq/core/constitution-master.md`).
> No fact without attribution: file:line, a brain reference, or an exit code (Law 4). Anything not recorded here with attribution = does not exist.
> Part of this project's own memory (`projects/caddy/brain/`) — separate from organization memory `hq/brain/` (Law 7).

## Project Identity
- **Project name:** `caddy` — the unified control center for domains and sites (reverse proxy / TLS / vhosts)
- **Reference RCCF work order:** SOFI-RCCF-20260824-CADDY-001 — a direct owner order ("you rearrange the system itself, equip it with all its power, and we make caddy a professional folder inside projects") — scope confirmed by a four-option quiz plus the owner's explicit endorsement "yes, correct" (HIPPOCAMPUS §INT-GTW-018)
- **Type:** infrastructure — no application stack; the templates/<stack> template is skipped by documented decision (no template fits infrastructure)
- **Project structure:** `Caddyfile` (short main file) · `sites/<domain>.caddy` (active sites) · `sites-disabled/` (disabled by relocation) · `php-fpm/{pool.d,disabled}` · `scripts/` · `cloudflare/` · `brain/` — as of ADR-002 (2026-08-25)
- **Track:** 🔴 FATEFUL — future production + TLS/domains security surface

## Involved Rooms and Leads (Laws 2 and 3)
| Room | Lead | Role in this project |
|--------|--------|-------------------|
| 04-architecture | arc-lead | design of the configuration contract and migration plan (S2) |
| 09-security | sec-lead | mandatory design review before G3 — brd-cso veto is absolute |
| 10-quality | qa-lead | testing configuration before any live touch |
| 11-devops | ops-lead | operations, deployment, and rollback plan at migration time |
| 14-gateway | gtw-dispatcher | intake and routing for all project work |

## Current Flow Stage (Law 1)
```
User input → gtw-intake-reformer → brd-ceo (+board) → room leads → agents → lead → CEO → user
```
- **Current position in the flow:** S1/S2 on paper — design before any live configuration (OWNER-DIRECTIVE-2026-0823 doctrine: "code speaks last")
- **Current task:** TKT-001 (project birth — executed) · next: design the configuration contract through G3 with signatures from 09+10

## Documented Domain Inventory (as of project birth)
| Domain | Status | Serves | Current config source |
|--------|--------|------|---------------------|
| tobacco.zanjour.com | 🌡️ **live production — untouchable** until separate migration ticket TKT-DRAFT-002 | tobacco-center store+POS | `/etc/caddy/Caddyfile` outside git — projects/tobacco-center/brain/SUMMARY.md:68 |
| jw.zanjour.com | SPIRIT development (Node :3000 via cloudflared tunnel) | jw project | same live Caddyfile — HIPPOCAMPUS §1010 |
| jw.local | local hosts entry | same jw | /etc/hosts + Caddyfile |
| shop.local | sofi-shop development (Next.js :3105 + Laravel :8123) | artisans marketplace | live Caddyfile + /etc/hosts — HIPPOCAMPUS §shop.local |
| :8090 | LAN interface for sofi-shop | same | live Caddyfile |
| zanjour.com portfolio · SAKK vhosts | removed 2026-07-24 | — | memory_index/memory-index.md:81 |

> **Update 2026-08-25 (ADR-002):** the table above is a historical snapshot as of project birth — current reality: sakk only is active (`sites/sakk.caddy`); everything else is disabled by relocation into `sites-disabled/` and covered by the 404 guard in the main file.

## Decisions (Law 7)
- `ADR-001 — project birth as unified control center and its exclusive scope — brain/DECISIONS.md`
- Decisions are promoted to organization memory (`hq/brain/cortex-decisions.md`) only with brd-ceo approval when they touch SOFI itself, not just this project.

## Lessons
- `sig:channel-fallback — brain/LESSONS.md LES-001`
- Lessons repeating ≥3 times across projects are promoted to `hq/brain/org_lessons/LESSONS.md` with brd-ceo approval.

## Standards Reconciliation Boundaries (an ADR due in design)
- **devops-standard.md:28-29** mandates a local caddy inside each project for development (`<project>/docker/caddy/Caddyfile` with `<project>.localhost` domains) — that stays as-is.
- This project owns only the global/live domain layer. Integration between the two layers is documented by an ADR within the design (S2) — layer integration, not conflict.
- Lesson SES-20260822-01 is binding for any future work here: audit references outside the repository (`/etc/caddy`, systemd, hosts) before any deletion or move.

## Session Evidence Block (Law 4)
- file:line — `projects/caddy/site/identity/public-readme.md` (structure by owner order) · `hq/core/structure-standard.md §2 + change log` · `memory_index/memory-index.md §Engine→Projects` · `identity/sofi-system-identity.md:18`
- exit code — `mkdir+cp brain init → 0` · `find hq/engine -type f → identity/public-readme.md only (caddy/ was empty)` · grep hq/engine references → 3 documentation files only, zero code references
- **Later owner decision during execution:** permanently delete the old predecessor without archiving ("I deleted it, I don't want it") and delete the entire `hq/archive/` folder — documented and executed after the fact (the owner overrides any plan)

## Infrastructure as Code (INT-GTW-032 · 2026-08-24)
This project became the **infrastructure command center** for all SOFI projects:
- `Caddyfile` + `php-fpm/pool.d/*` = canonical copies **byte-identical to live** (diff-live=0 as of today)
- `scripts/`: status·validate·diff-live·deploy (GitOps model: repository→validate→live)
- `cloudflare/CONFIG-OF-RECORD.md` DNS/SSL/tunnel record — never any tokens
- OPERATIONS.md runbook and emergency procedures
The owner order "set up caddy for every project, have cloudflare ready, php-fpm, and run everything" is fulfilled: all three services active and production returning 200.
