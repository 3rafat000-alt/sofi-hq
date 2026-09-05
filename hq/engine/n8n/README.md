# `hq/engine/n8n/` — n8n Orchestrator Workflows

> The n8n orchestrator workflows that automate the SOFI HQ ticket bus + team-snapshot + dispatch
> flow. Per `OPERATIONS.md`, n8n is the **engine** for the team-snapshot + dispatch pipeline.

Owned by `ops-cicd-engineer` (room 11) + `gtw-dispatcher` (room 14).

---

## Layout

```
n8n/
├── README.md                       ← you are here
└── workflows/                       ← the 3 orchestration workflows
    ├── 01-team-read.json
    ├── 02-team-edit.json
    └── 03-team-dispatch.json
```

---

## The 3 workflows (in `workflows/`)

| # | Workflow | Trigger | Purpose |
|---|----------|---------|---------|
| 01 | `team-read.json` | on-demand | **Read** a team snapshot (per room) — returns current agent list + skills + status |
| 02 | `team-edit.json` | on-demand | **Edit** a team snapshot (per room) — used by `gtw-conflict-resolver` for re-assignment |
| 03 | `team-dispatch.json` | on RCCF issuance | **Dispatch** a task to the right team — auto-routes via P-01.8 lane + room rules |

---

## The dispatch flow (workflow 03)

```
RCCF issued (by brd-ceo or room lead)
  → workflow 03 (team-dispatch)
  → reads hq/core/nexus/registry.yaml
  → determines target room(s) per lane:
      - 🟢 Fast → single lead
      - 🟡 Standard → brd-ceo
      - 🔴 Fateful → brd-ceo + Board consult
  → creates a ticket in hq/engine/mcp_server/data/tickets.db
  → notifies the room lead via ticket bus
  → if Lane=Standard/Fateful: requires explicit acceptance (P-02.4)
```

---

## The bus (P-02 — Strict JSON Handoff Scheme)

> Source: `protocols.md:P-02` + `nexus/mcp-routing.yaml:17`.

```json
{
  "v": 1,
  "ticket_id": "PRJ-ID-001",
  "from_agent": "bck-api-engineer",
  "to_agent": "bck-lead",
  "direction": "upward-only",
  "type": "handoff|acceptance|rejection",
  "rccf_ref": "RCCF-2026-0823-NAME",
  "artifacts": ["projects/<name>/app/Domains/X/Actions.php"],
  "evidence_digest": {
    "files_changed": 3,
    "checks": {"static_analysis": "PASS", "tests": "PASS"},
    "exit_codes": [0]
  },
  "context_refs": ["hq/core/standards/api-envelope.md#envelope-v1"],
  "status": "ready-for-review|in-flight|delivered|rejected",
  "note": "≤280 chars"
}
```

The `note` ≤ 280 chars keeps the ticket lean — details live in the cited files.

---

## The CONDITION-FOLLOW-UP (DEC-R3.4)

> `hq/engine/n8n/workflows/*.json` are **never** truncated in delivery handoffs. They are part
> of the operational canon. They live in git and are versioned.

**Why:** these workflows define the dispatch logic — truncating or modifying them without
traceability breaks the bus contract.

---

## The 100% local guarantee (per `sofi-mcp-fleet`)

The n8n instance + the MCP server + all 27 MCP routes are **100% local** (no SaaS, no npx cloud, no
paid API). Per INT-0003, any paid key is auto-rejected. Self-hosted alternative is the only
allowed mode.

---

## How to add a new workflow

1. Design the workflow in n8n (visually)
2. Export to JSON
3. Save in `workflows/<NN>-<name>.json`
4. Add a row to the table above
5. Add tests (in `mcp_server/tests/`)
6. Commit atomically — pre-commit enforces all 4 guards
7. Record ADR in CORTEX if the new workflow changes constitutional behavior

**Forbidden:** making the orchestrator depend on any external SaaS (e.g. Zapier, Make, n8n Cloud).

---

## See also

- [`../README.md`](../README.md) — `hq/engine/` parent
- [`../mcp_server/README.md`](../mcp_server/README.md) — the MCP server
- [`../../core/protocols.md:P-02`](../../core/protocols.md) — Handoff Protocol
- [`../../core/standards/mcp-communication-standard.md`](../../core/standards/mcp-communication-standard.md) — bus rules
- [Top-level README](../../../README.md)
- [`AGENTS.md`](../../../AGENTS.md)
