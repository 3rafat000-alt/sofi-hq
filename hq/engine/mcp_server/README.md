# `hq/engine/mcp_server/` — Live MCP Server

> The **live MCP server** that all 27 MCP routes ultimately connect to. This is the
> **engine layer** for the 100% local fleet (per `mcp-routing.yaml:13`).

Owned by `gtw-dispatcher` (room 14) — the gateway lead. The server is the source of truth for the
MCP bus and tickets.

---

## Layout

```
mcp_server/
├── README.md                       ← you are here
├── AGENT_GUIDE.md                  ← guide for agent developers using the MCP server
├── READY.md                        ← readiness checklist
├── main.py                         ← server entry point
├── agents_mcp.py                   ← agents-domain MCP tools
├── leads_mcp.py                     ← leads-domain MCP tools
├── meetings_mcp.py                  ← meetings-domain MCP tools
├── memory.py                       ← memory operations
├── models.py                       ← model routing
├── ticket_bus.py                    ← the bus (Strict JSON Handoff Scheme per P-02)
├── config.py                       ← configuration
├── agents.py / leads.py / ...       ← legacy / domain modules
├── data/                           ← runtime data — CONDITION-FOLLOW-UP applies
│   ├── tickets.db                  ← the bus persistence
│   └── server.log                  ← server log
├── brain/                          ← CORTEX mirror for the live engine
├── contracts/                      ← runtime contracts (consumed by agents)
├── design/                         ← runtime design notes
├── docs/                           ← supplementary docs
├── scripts/                        ← operations
│   ├── run.sh                      ← run in dev
│   ├── start-prod.sh               ← run in prod (systemd)
│   ├── stop.sh                     ← stop
│   ├── install-service.sh          ← install systemd service
│   └── mcp-manage.sh               ← manage service (start/stop/restart/status)
├── tests/                          ← test suite
├── Dockerfile                      ← container build
├── requirements.txt                ← Python dependencies
├── client/                         ← reference MCP client
└── __pycache__/                    ← Python bytecode (gitignored)
```

---

## The MCP server's role (per `mcp-routing.yaml`)

This server is the **engine** for the 27 MCP servers registered in `hq/core/nexus/mcp-routing.yaml:13`.
The 6 fleet servers (Context · Wiki · Browser · Reasoning · Time · Security) and the 21
organizational servers (MemoryHub · EpisodicMemory · WorkingMemory · Github · Network · ...) all
connect to this server.

The server is the **bus** — every cross-room communication goes through it (per P-02 Strict JSON
Handoff Scheme).

---

## The 3 main MCP tools

| Tool | Module | Purpose |
|------|--------|---------|
| **agents** | `agents_mcp.py` | List/get/create/update/delete agents (via `registry.yaml` + `.opencode/agent/`) |
| **leads** | `leads_mcp.py` | List/get room leads + lead-board structure |
| **meetings** | `meetings_mcp.py` | Schedule/list/update board meetings (per `room-meetings-standard.md`) |

Plus: `memory` (read/write CORTEX + HIPPOCAMPUS + AMYGDALA) · `models` (route LLM by task class) ·
`ticket_bus` (the bus itself — P-02).

---

## The 6 fleet servers (the 6 binding rules)

> Source: `mcp-routing.yaml:13` — the 6 binding rules for any MCP server (per `sofi-mcp-fleet`).

1. **SOFI-Context** before any code touching a library (Latest-Version-Mandatory)
2. **SOFI-Wiki** before any external repo claim
3. **SOFI-Browser** for visual evidence
4. **SOFI-Reasoning** for complex branching
5. **`sec-mcp-vetting`** for any new server (no self-enable)
6. **Everything is free** (no paid keys — INT-0003)

This server **implements** all 6 rules via the `memory.py` (knowledge) + `models.py` (routing) +
`ticket_bus.py` (the bus) + `data/tickets.db` (persistence).

---

## The runtime data (`data/`)

> ⚠️ **CONDITION-FOLLOW-UP (DEC-R3.4):** these runtime artifacts are **never** truncated in
> delivery handoffs.

- `data/tickets.db` — the bus persistence (SQLite) — **never delete or truncate**
- `data/server.log` — the server log — **never delete or truncate**

Both are in `.gitignore` (they are runtime, not source) but the **never-truncate** rule applies
even if they end up in a commit (e.g. during emergency recovery).

---

## The operations

| Script | Purpose |
|--------|---------|
| `run.sh` | Run in dev (foreground) |
| `start-prod.sh` | Run in prod (systemd) |
| `stop.sh` | Stop |
| `install-service.sh` | Install as systemd service |
| `mcp-manage.sh` | Manage (start / stop / restart / status) |

The server is typically run via systemd (`mcp.service`) and managed by `ops-release-manager`.

---

## How to add a new MCP tool

1. Create the tool in the appropriate domain module (`agents_mcp.py` / `leads_mcp.py` / `meetings_mcp.py`)
2. Use `sec-mcp-vetting` skill to vet the tool (mandatory)
3. Add the tool's signature to `mcp-routing.yaml`
4. Update `AGENT_GUIDE.md` + `README.md` with the new tool
5. Add tests in `tests/`
6. Commit atomically — pre-commit enforces all 4 guards
7. Record ADR in CORTEX if the new tool changes constitutional behavior

---

## See also

- [`../README.md`](../README.md) — `hq/engine/` parent
- [`../scripts/README.md`](../scripts/README.md) — operational scripts
- [`../../core/nexus/mcp-routing.yaml`](../../core/nexus/mcp-routing.yaml) — the 27 MCP routes
- [`../../core/standards/mcp-communication-standard.md`](../../core/standards/mcp-communication-standard.md) — bus rules
- [Top-level README](../../../README.md)
- [`AGENTS.md`](../../../AGENTS.md) — Law 8 (Security)
