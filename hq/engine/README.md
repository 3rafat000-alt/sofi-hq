# `hq/engine/` — Live Publishing Layer

> The **runtime** of SOFI HQ. Caddy + PHP-FPM + Cloudflare + n8n + MCP server. This is what
> actually serves the live project (currently `sakk`) to the public.

The `hq/engine/` directory is **operational state** — not the constitution. It is governed by
`deploy-standard.md` + `devops-standard.md` + `runbooks/`, and managed by room 11 (DevOps).

---

## Layout

```
engine/
├── README.md                       ← you are here
├── Caddyfile                       ← canon — single source of truth for the live reverse-proxy
├── OPERATIONS.md                   ← operational runbook (per-room: devops + observability)
│
├── sites/                          ← per-domain .caddy files (one per public hostname)
│   ├── sakk.caddy                  ← sakk.local + sakk.zanjour.com
│   ├── zanjour-portal.caddy
│   ├── mcp.caddy                   ← MCP server endpoint
│   └── n8n.caddy                   ← orchestrator endpoint
│
├── php-fpm/                        ← PHP-FPM pools (one per Laravel app)
│   ├── README.md
│   ├── pool.d/                     ← live pools
│   │   └── sakk.conf
│   ├── disabled/                   ← archived pools
│   └── disable-pools.sh
│
├── scripts/                         ← the operational scripts (Caddy + PHP-FPM + deploy)
│   ├── bootstrap-live.sh           ← EUID guard + caddy import (sudo, one-time)
│   ├── validate.sh                 ← canon + live + PHP-FPM check (read-only, no sudo)
│   ├── deploy.sh                   ← reload Caddy via admin API (no sudo) + sudo fallback
│   ├── diff-live.sh                ← diff between canon Caddyfile and live /etc/caddy/Caddyfile
│   ├── check-env-guard.sh          ← minimal env / EUID check
│   └── status.sh                   ← health check for all layers
│
├── n8n/                            ← orchestrator workflow definitions
│   └── workflows/                   ← 01-team-read · 02-team-edit · 03-team-dispatch
│
├── mcp_server/                      ← the live MCP server (Docker, tickets.db, agents, etc.)
│   ├── README.md
│   ├── Dockerfile
│   ├── AGENT_GUIDE.md
│   ├── READY.md
│   ├── main.py                     ← server entry point
│   ├── agents_mcp.py · leads_mcp.py · meetings_mcp.py · memory.py · models.py · ticket_bus.py
│   ├── data/                       ← runtime data (tickets.db, server.log) — CONDITION-FOLLOW-UP
│   ├── brain/                      ← CORTEX mirror for live engine
│   └── scripts/                    ← run.sh · start-prod.sh · stop.sh · mcp-manage.sh
│
├── brain/                          ← CORTEX mirror for the live engine (separate from hq/brain)
│   ├── CONTEXT.md
│   ├── DECISIONS.md
│   ├── HANDOFFS.md
│   ├── LESSONS.md
│   └── verified/                   ← verified artifacts
│
├── cloudflare/                     ← Cloudflare config (per the deploy-standard)
│   └── CONFIG-OF-RECORD.md
│
└── logs/                           ← runtime logs (NOT in git, CONDITION-FOLLOW-UP applies)
```

---

## The operational flow (per `OPERATIONS.md`)

```
Owner pushes commit
  → CI runs pre-commit (4 guards)
  → ops-cicd-engineer triggers pipeline (on-merge automated)
  → ops-migration-runner runs migrations with rollback window
  → ops-release-manager ships via Caddy admin API (no sudo)
  → obs-monitoring-engineer activates dashboards + alerts
  → if SEV-1 → WarRoom 15 activates (Law 14 freeze)
  → on recovery → AMYGDALA log + Gate re-evaluation
```

---

## The 6 operational scripts (in `scripts/`)

| Script | Purpose | Privilege | Owner |
|--------|---------|-----------|-------|
| `bootstrap-live.sh:6` | Imports canon Caddyfile to `/etc/caddy/Caddyfile` (one-time, **sudo** required) | **sudo** | `ops-lead` |
| `validate.sh:1` | Validates canon Caddyfile + live `/etc/caddy/Caddyfile` + PHP-FPM pools | read-only | `ops-cicd-engineer` |
| `deploy.sh:7` | Reloads Caddy via admin API (no sudo, fallback to sudo) | no sudo + sudo fallback | `ops-release-manager` |
| `diff-live.sh` | Diffs canon Caddyfile against live `/etc/caddy/Caddyfile` | read-only | `ops-cicd-engineer` |
| `check-env-guard.sh` | Minimal environment / EUID check | read-only | `ops-lead` |
| `status.sh` | Health check for all layers (Caddy + PHP-FPM + MCP + n8n) | read-only | `obs-monitoring-engineer` |

---

## The 4 sites (in `sites/`)

| Site | Endpoint | Status | Owner |
|------|----------|--------|-------|
| `sakk.caddy` | `sakk.local` + `sakk.zanjour.com` | live | `ops-domain-warden` |
| `zanjour-portal.caddy` | portal zanjour | live | `ops-domain-warden` |
| `mcp.caddy` | MCP server endpoint | live | `gtw-dispatcher` |
| `n8n.caddy` | orchestrator endpoint | live | `ops-cicd-engineer` |

---

## The n8n orchestrator (in `n8n/workflows/`)

| Workflow | Purpose | Trigger |
|----------|---------|---------|
| `01-team-read.json` | Read a team snapshot | on-demand |
| `02-team-edit.json` | Edit a team snapshot | on-demand |
| `03-team-dispatch.json` | Dispatch a team task | RCCF issuance |

---

## The MCP server (in `mcp_server/`)

> Source: `mcp_server/README.md`. The live MCP server that **all 27 MCP routes** ultimately connect to.
> This is the **engine layer** for the 100% local fleet (per `mcp-routing.yaml:13`).

Key files:
- `main.py` — server entry point
- `agents_mcp.py` · `leads_mcp.py` · `meetings_mcp.py` — per-domain MCP tools
- `memory.py` · `models.py` · `ticket_bus.py` — the bus + memory + models
- `data/tickets.db` — runtime data (CONDITION-FOLLOW-UP: never truncate in handoff receipts)
- `data/server.log` — runtime log
- `Dockerfile` · `install-service.sh` · `run.sh` · `start-prod.sh` · `stop.sh` · `mcp-manage.sh` — operations
- `requirements.txt` — Python dependencies

---

## The CONDITION-FOLLOW-UP (DEC-R3.4)

> **No delivery handoff may truncate these runtime artifacts:**
> - `hq/engine/mcp_server/data/tickets.db`
> - `hq/engine/logs/*.log`
> - `hq/engine/n8n/workflows/*.json`
> - `hq/engine/sites/*.caddy`

This is enforced at the **handoff receipt** layer (P-02.5) and at every commit via the pre-commit
chain. The `git add` command should never stage any of these files (they are in `.gitignore` or
have explicit `pathspec` exclusion).

---

## See also

- [`hq/brain/`](../brain/README.md) — organization memory
- [`hq/core/standards/deploy-standard.md`](../core/standards/deploy-standard.md)
- [`hq/core/standards/devops-standard.md`](../core/standards/devops-standard.md)
- [`OPERATIONS.md`](./OPERATIONS.md) — per-room operational runbook
- [Top-level README](../../README.md)
- [`AGENTS.md`](../../AGENTS.md) — Law 8 + 10 + 11
