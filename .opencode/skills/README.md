# `.opencode/skills/` — The 116 Skills (Operating Manuals)

> The **operating manuals** for every agent and room. Each skill is a self-contained playbook
> (when to invoke · inputs · steps · outputs · handoff · constraints). Per the binding ownership
> in `hq/core/domain/rooms/<room>/capabilities/skills.yaml` + `SKILLS-ASSIGNMENT.md`, every
> skill belongs to a specific room.

> Per Law 13.3, every file starts with a `## FILE: <path>` header. The 4 constitutional
> guards enforce this on every commit.

---

## What's in this directory

| Category | Count | Examples |
|----------|-------|----------|
| **Foundation** (all rooms) | 6 | `sofi-evidence` · `sofi-handoff` · `sofi-mcp-fleet` · `sofi-boot` · `sofi-project-spawn` · `skill-forge` |
| **Room playbooks** (1/room × 17 rooms) | 17 | `brd-decision-gate` · `gtw-intake-route` · `qa-test-plan` · `qa-flutter-architect` · `qa-react-architect` · `qa-laravel-architect` · `bck-feature-build` · `fnt-component-build` · `mob-feature-build` · `dsn-design-handoff` · `arc-adr` · `obs-incident-response` · `sec-threat-model` · `sec-mcp-vetting` · `loc-rtl-adaptation` · `inn-experiment` · `war-incident-runbook` |
| **Official Flutter/Dart pack** (22) | 22 | `flutter-add-widget-test` · `dart-run-static-analysis` · ... |
| **LambdaTest pack** (19) | 19 | `playwright-skill` · `phpunit-skill` · `laravel-dusk-skill` · `flutter-testing-skill` · ... |
| **Anthropic pack** (7) | 7 | `frontend-design` · `theme-factory` · `webapp-testing` · `skill-creator` · ... |
| **SOFI original** (6) | 6 | `systematic-debugging` · `brainstorming` · `writing-plans` · `dsn-design-intelligence` · `qa-agent-browser` · `res-web-scrape` |
| **Absorbed** (7) | 7 | `banner-design` · `brand` · `design` · `design-system` · `slides` · `ui-styling` · `ui-ux-pro-max` |
| **External packs (linked)** (38+) | 38+ | `api-*` · `dart-*` · `flutter-*` · `test-frameworks` · ... |
| **3 new skills (Audit-ALL-Phase3)** | 3 | `loc-rtl-adaptation` (08) + `inn-experiment` (16) + `war-incident-runbook` (15) |
| **Total** | | **116** |

---

## The skill file format (every file follows this)

```markdown
---
name: <kebab-case-skill-name>
description: <multi-line description — when to invoke, with triggers>
---

# <Skill Name>

> **Core value:** <one-line summary>

## 🎯 When to invoke (When)
- <trigger 1>
- <trigger 2>
**Do not invoke** for: <anti-triggers>

## 📥 Required inputs (Inputs)
- ...

## 🔧 Steps (Steps)
1. ...
2. ...
3. ...

## 📤 Outputs + evidence (Outputs & Evidence)
- Output: ...
- Evidence: <per `sofi-evidence` — file:line · exit code · fingerprint>
- Handoff: <per `sofi-handoff` — JSON ticket>

## 🔗 Handoff
- Deliver to: <upstream agent / lead>
- No direct delivery to user (Law 3)

## ⛔ Constraints
- ...

## 🧠 Memory
- Per Law 7: project notes in `projects/<slug>/brain/`
- Org notes in `hq/brain/` (CORTEX / HIPPOCAMPUS / AMYGDALA)

## 📚 References
- ...
```

---

## The 3 newest skills (Audit-ALL-Phase3)

### `loc-rtl-adaptation/` (08-localization)

> Arabic localization & RTL protocol — translation memory + cultural adaptation + RTL mirror
> validation + voice & tone, applied per locale for SOFI products.

**Triggers:** "localize this screen" · "translate to Arabic" · "RTL mirror" · "voice & tone guide"
· "cultural adaptation Arabic" · "Law 11 Arabic simple" · "DFR Arabic co-sign"

### `inn-experiment/` (16-innovation)

> Innovation experiment protocol — tech scouting + experiment design + PoC + ADR drafting in
> the isolated sandbox.

**Triggers:** "PoC this" · "innovation ADR" · "tech scout" · "sandbox experiment" · "evaluate
emerging tech"

### `war-incident-runbook/` (15-warroom)

> WarRoom P0 incident runbook — detection → triage → containment → rollback → comms → postmortem.

**Triggers:** "P0 incident" · "production down" · "data breach" · "rollback fire" · "war room" ·
"AMYGDALA log"

---

## The binding ownership map (per `hq/core/domain/SKILLS-ASSIGNMENT.md`)

Every skill belongs to exactly one room. The ownership is tracked in:
- `hq/core/domain/SKILLS-ASSIGNMENT.md` — the deed registry
- `hq/core/domain/rooms/<room>/capabilities/skills.yaml` — the room-level manifest
- `hq/core/nexus/skill-routing.yaml` — the routing

To find who owns a skill:
```bash
grep -A 2 "name: <skill-name>" hq/core/domain/rooms/*/capabilities/skills.yaml
```

---

## How to add a new skill

1. Use the `skill-forge` meta-skill (or follow the format above manually)
2. Create `.opencode/skills/<name>/SKILL.md` with the standard format
3. Register ownership in the owning room's `capabilities/skills.yaml`
4. Add row to `hq/core/domain/SKILLS-ASSIGNMENT.md`
5. Add row to `hq/core/nexus/skill-routing.yaml`
6. Add row to `.opencode/skills/INDEX.md`
7. Bump `SKILLS_BASELINE` in `hq/core/tooling/registry_guard.py:20` + `hq/core/tooling/count_sync.py:22`
8. Record ADR in CORTEX (skill creation is constitutional)
9. Commit atomically — pre-commit enforces all 4 guards

**Forbidden:** adding a skill without registering ownership in the room manifest (Law 12).
Adding a skill without bumping `SKILLS_BASELINE` triggers `registry_guard` + `count_sync` FAIL.

---

## The 6 binding MCP-FLEET rules (per `sofi-mcp-fleet`)

When a skill uses any MCP tool, the 6 rules apply:

1. **SOFI-Context** before any code touching a library (Latest-Version-Mandatory)
2. **SOFI-Wiki** before any external repo claim
3. **SOFI-Browser** for visual evidence
4. **SOFI-Reasoning** for complex branching
5. **`sec-mcp-vetting`** for any new server
6. **Everything is free** (no paid keys)

---

## See also

- [`../README.md`](../README.md) — `.opencode/` parent
- [`../agent/README.md`](../agent/README.md) — 121 agents
- [`./INDEX.md`](./INDEX.md) — the index
- [`../../hq/core/domain/SKILLS-ASSIGNMENT.md`](../../hq/core/domain/SKILLS-ASSIGNMENT.md) — ownership
- [`../../hq/core/standards/latest-version-mandatory.md`](../../hq/core/standards/latest-version-mandatory.md) — MCP rules
- [Top-level README](../../../README.md)
- [`AGENTS.md`](../../../AGENTS.md) — Law 4 + 13
