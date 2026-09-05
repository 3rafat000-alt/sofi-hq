# `hq/core/domain/` — DDD Subdirectories

> The `hq/core/domain/` directory is the DDD domain layer. The parent README
> (`hq/core/domain/README.md`) is the entry point. This file documents the subdirectories
> that are **not** the per-room capsules (`rooms/`).

---

## The subdirectories

| Subdirectory | Purpose | Edit by |
|--------------|---------|---------|
| `context-map.yaml` | The single official inter-room interface (Law 2) | `brd-arbiter` (Law 14 disputes) |
| `MCP_PROTOCOL_BINDING.md` | How MCP protocol binds to the domain | `gtw-dispatcher` |
| `README.md` | Parent README (you are in the grandparent) | `knw-lead` |
| `SKILLS-ASSIGNMENT.md` | Skill → room → lead ownership map (the full deed registry) | `knw-lead` |
| `communication-matrix.md` | Cross-room consultation rules (4 consultation rows) | `knw-lead` |
| `rooms/` | The 17 room capsules (charter + agents/) | per-room lead |
| `shared-kernel/` | The shared kernel — glossary + identity + envelope + evidence-rule | `brd-ceo` (shared kernel — Law 2) |
| `bus/` (reserved) | Reserved for the ticket bus implementation | `gtw-dispatcher` |

---

## The shared kernel (`shared-kernel/`)

> The `shared-kernel/` is the **only** place where shared concepts can be modified — and it
> requires `brd-ceo` approval. Per Law 2, the shared kernel is the lingua franca of the
> organization.

Current contents (per the DDD convention):
- `glossary.md` — the shared terms (DDD ubiquitous language)
- `identity.md` — the shared identity types (User, Role, Permission, Tenant)
- `envelope.md` — the shared envelope (API response wrapper, per `standards/api-envelope.md`)
- `evidence-rule.md` — the shared evidence rule (Law 4 + `sofi-evidence` skill)

---

## The bus (`bus/`)

Reserved directory for the ticket bus implementation. Currently empty. The **Strict JSON
Handoff Scheme** (P-02) lives in `protocols.md:P-02` and `nexus/mcp-routing.yaml:17` — see
also `hq/engine/mcp_server/data/tickets.db` for the runtime persistence.

Future implementations: Redis streams · RabbitMQ · in-process queue. The bus must remain
**100% local** (no external SaaS — per INT-0003).

---

## How to read this directory

1. Start at `hq/core/domain/README.md` — the parent
2. For shared concepts: read `context-map.yaml` + `shared-kernel/`
3. For room-by-room: read `rooms/<room>/charter.md`
4. For the bus: read `protocols.md:P-02` + `nexus/mcp-routing.yaml:17`

---

## See also

- [`../README.md`](../README.md) — `hq/core/` parent
- [`./README.md`](./README.md) — `hq/core/domain/` parent
- [`./context-map.yaml`](./context-map.yaml) — the interface map
- [`./shared-kernel/`](./shared-kernel/) — shared kernel
- [`./rooms/`](./rooms/) — 17 room capsules
- [Top-level README](../../../README.md)
- [`AGENTS.md`](../../../AGENTS.md) — Law 2
