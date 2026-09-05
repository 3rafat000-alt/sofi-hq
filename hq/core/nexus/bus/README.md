# `hq/core/nexus/bus/` — Ticket Bus (Reserved)

> Reserved directory for the **ticket bus implementation**. The bus is the **transport layer**
> for the Strict JSON Handoff Scheme (P-02) — every cross-room communication goes through it.

Currently **empty**. The bus contract lives in `protocols.md:P-02` and the runtime persistence
lives in `hq/engine/mcp_server/data/tickets.db`.

---

## The plan (per `nexus/README.md`)

Future implementations of the bus:
- **Redis streams** — for cross-process / cross-server bus (production)
- **RabbitMQ** — for high-throughput / multi-tenant bus (enterprise)
- **In-process queue** — for single-server / dev bus (development)

All implementations must:
- Honor the **Strict JSON Handoff Scheme** (P-02)
- Keep the `note` ≤ 280 chars
- Be **100% local** (no external SaaS — INT-0003)
- Log every transition to `evidence` (Law 4)

---

## The bus contract (per `protocols.md:P-02`)

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

**Strict schema rules:**
1. `note` ≤ 280 chars — details live in the cited files
2. Full evidence stays in the `sofi-evidence` block (Law 4)
3. Any field outside the schema = automatic ticket rejection (L1)
4. Schema extension = new `v` with `brd-ceo` approval

---

## How to add a bus implementation

1. Choose a technology (Redis / RabbitMQ / in-process)
2. Implement the Strict JSON Handoff Scheme contract above
3. Add a `bus/<tech>-bus.md` spec file documenting the implementation
4. Wire the bus to the MCP server (`hq/engine/mcp_server/ticket_bus.py`)
5. Add tests (in `hq/engine/mcp_server/tests/`)
6. Run `bash hq/engine/scripts/validate.sh` to verify the change
7. Commit atomically — pre-commit enforces all 4 guards
8. Record ADR in CORTEX

**Forbidden:** using any external SaaS (e.g. AWS SQS, Google Pub/Sub, Azure Service Bus). Per
INT-0003, the bus must be **100% local**.

---

## See also

- [`../README.md`](../README.md) — `hq/core/nexus/` parent
- [`../nexus/README.md`](../README.md) — nexus parent
- [`../protocols.md:P-02`](../protocols.md) — Handoff Protocol
- [`../../standards/mcp-communication-standard.md`](../../standards/mcp-communication-standard.md) — bus rules
- [Top-level README](../../../README.md)
- [`AGENTS.md`](../../../AGENTS.md) — Law 2
