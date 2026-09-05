# `hq/core/protocols/` — Protocol Subdirectory

> Some protocols are large enough to warrant their own directory (e.g. `protocol-04-mcp-routing.md`).
> The canonical list of all 17 protocols (P-01..P-20) lives in `hq/core/protocols.md` — see
> that file for the master table.

---

## Files

| File | Protocol | Purpose |
|------|----------|---------|
| `protocol-04-mcp-routing.md` | P-04 + extended | The full MCP routing spec — 27 servers, room distribution, 6 binding rules |
| `sofi-broker-protocol.md` | (broker) | The SOFI broker — ticket bus + multi-agent coordination protocol |

> Other protocols (P-01, P-02, P-03, P-05, P-06, P-07, P-08, P-09, P-10, P-11, P-12, P-13, P-14, P-16,
> P-17, P-18, P-19, P-20) live inline in `hq/core/protocols.md`.

---

## How to read

1. Start at `hq/core/protocols.md` — master table + inline text for short protocols
2. Drill into this directory for the **long-form** version of selected protocols
3. Each file here cross-references its inline counterpart

---

## See also

- [`../README.md`](../README.md) — `hq/core/` parent
- [`../protocols.md`](../protocols.md) — master protocol file
- [Top-level README](../../../README.md)
- [`AGENTS.md`](../../../AGENTS.md)
