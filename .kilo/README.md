# .kilo — Generated Operating Mirror (Kilo Mirror)

> **Role of this folder:** Kilo's interface over the SOFI system — everything here is generated or tool state; the source always lives elsewhere.

| Item | Nature | Source |
|------|--------|--------|
| `agent/*.md` (106) | Generated mirror of agent specifications | `.opencode/agent/` via `node hq/core/tooling/port-agents.mjs` |
| `command/` | Operator slash commands | edited directly here |
| `plans/` · `agent-manager.json` · `run-script` · `setup-script` | Kilo session/tool state | managed by the tool itself |
| `package.json` + `node_modules/` | Kilo plugin (`@kilocode/plugin`) | managed by the tool |

**Rules:**
1. To edit an agent: modify its source in `.opencode/agent/<x>.md`, then rerun `node hq/core/tooling/port-agents.mjs` — never hand-edit the mirror.
2. Governance capsules (senses/memory/capabilities) live in `hq/core/domain/rooms/<room>/agents/<name>/`.
3. The official count of 106 is sovereign — registry: `hq/core/nexus/registry.yaml`.
