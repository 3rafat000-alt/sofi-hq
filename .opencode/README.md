# .opencode — Live Presentation Layer

> **Role of this folder:** what the opencode engine loads directly — never edit files here blindly; know each item's source.

| Item | Nature | True source |
|------|--------|-------------|
| `agent/*.md` (106) | **Canonical agent specifications** — sole source per constitutional Article 00 | embraced by capsules in `hq/core/domain/rooms/<room>/agents/<name>/` (senses · memory · capabilities around them) |
| `skills/` (106 + INDEX.md) | Skill installation area | binding ownership in `hq/core/domain/rooms/<room>/capabilities/skills.yaml`, ledger in `hq/core/domain/SKILLS-ASSIGNMENT.md` |
| `package.json` + `node_modules/` | layer runtime dependencies | tool-managed |

**Binding rules:**
1. To edit an agent: modify its file here, then rerun `node hq/core/tooling/port-agents.mjs` — the `.kilo/agent` mirror is generated, never hand-edited.
2. New skill: go through `skill-forge` and register ownership in the owning room's manifest before indexing.
3. The official count of 106 in `hq/core/nexus/registry.yaml` governs every generation (loud failure on mismatch).
