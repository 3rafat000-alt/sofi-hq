# `tools/` — Harness Utilities (NOT SOFI Constitution)

> Internal harness utilities — this is **not** SOFI constitutional material. This directory
> contains the operational tools that the OpenCode (or compatible) harness uses to coordinate
> agents, manage the MCP bus, run tests, and enforce security.

> **Note:** anything in `tools/` is owned by the **harness maintainers**, not by SOFI HQ. Changes
> here do **not** require `brd-ceo` approval (unless they cross a constitutional boundary, in
> which case the change is logged in CORTEX).

---

## What's in this directory

| Subdirectory | Purpose | Owner |
|--------------|---------|-------|
| `__init__.py` | Python package init | harness |
| `__pycache__/` | Python bytecode (gitignored) | — |
| `agents/` | (legacy) harness-level agent utilities | harness |
| `mcp/` | MCP integration code (broker + clients) | `gtw-dispatcher` |
| `mcp_broker/` | The MCP broker (legacy name) | `gtw-dispatcher` |
| `shared/` | Shared utilities across tools | harness |
| `testing/` | Harness testing framework | harness |

---

## `mcp/` and `mcp_broker/`

The MCP broker routes requests between the OpenCode harness and the 27 MCP servers
(`hq/core/nexus/mcp-routing.yaml:13`). The bus is **100% local** (no external SaaS — INT-0003).

The broker implements the **Strict JSON Handoff Scheme** (P-02) and persists tickets in
`hq/engine/mcp_server/data/tickets.db` (CONDITION-FOLLOW-UP applies).

---

## `testing/`

The harness testing framework — for testing the OpenCode runtime, not SOFI products. SOFI product
testing lives in `projects/<slug>/tests/` and is governed by room 10 (Quality).

---

## `shared/`

Cross-tool utilities — anything reused across `mcp/`, `mcp_broker/`, `testing/`. Includes the
Python package init (`__init__.py`) and common helpers.

---

## What lives here vs. the constitution

| Type | Location | Binding? | Approved by |
|------|----------|----------|-------------|
| Constitution | `AGENTS.md` + `hq/core/` | YES | `brd-ceo` (owner) |
| Runtime config | `opencode.json` (root) + `.opencode/` | YES (harness) | `gtw-dispatcher` |
| Operational tools | `tools/` (this directory) | NO (harness) | harness maintainers |
| MCP server | `hq/engine/mcp_server/` | YES (operational) | `gtw-dispatcher` |

---

## How to add to this directory

1. Create the tool file in the appropriate subdirectory
2. If it interacts with SOFI constitution (e.g. calls a guard), reference it from the relevant
   `protocols.md` section
3. If it's a pure harness utility, no ceremony is required
4. Commit atomically — pre-commit enforces all 4 guards (including `gitleaks` for secrets)

**Forbidden:** adding tools that depend on external SaaS (e.g. Slack webhooks, PagerDuty).
All tools must be **100% local** (per INT-0003).

---

## See also

- [Top-level README](../README.md)
- [`AGENTS.md`](../AGENTS.md) — supreme law
- [`hq/core/tooling/README.md`](../hq/core/tooling/README.md) — constitutional guards
- [`hq/engine/mcp_server/README.md`](../hq/engine/mcp_server/README.md) — the MCP server
- [`hq/core/nexus/mcp-routing.yaml`](../hq/core/nexus/mcp-routing.yaml) — the 27 MCP routes
- [`hq/core/standards/mcp-communication-standard.md`](../hq/core/standards/mcp-communication-standard.md) — bus rules
