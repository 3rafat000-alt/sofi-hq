# `skills/` — Harness-Level Skills (Metadata Registry)

> The OpenCode (or compatible) harness-level **skill metadata registry**. This is **not** the
> SOFI operating manuals (those live in `.opencode/skills/`); this is the harness's own
> metadata for skill registration + routing.

> **Note:** anything in `skills/` is owned by the **harness maintainers**, not by SOFI HQ. The
> 116 actual SOFI skills live in `.opencode/skills/` and are bound to rooms via
> `hq/core/domain/SKILLS-ASSIGNMENT.md`.

---

## What's in this directory

| Subdirectory | Purpose | Owner |
|--------------|---------|-------|
| `agent-reach/` | Harness-level: agent discovery + reach utilities | harness |
| `ddd-strategic/` | Harness-level: DDD strategic patterns (not SOFI-specific) | harness |
| `devops-kubernetes/` | Harness-level: DevOps with Kubernetes (NOT in Stack Lock R3) | harness |
| `event-driven/` | Harness-level: event-driven architecture patterns | harness |
| `flutter-mobile/` | Harness-level: Flutter mobile patterns | harness |
| `laravel-backend/` | Harness-level: Laravel backend patterns | harness |
| `mcp-architecture/` | Harness-level: MCP architecture patterns | harness |
| `owasp-security/` | Harness-level: OWASP security patterns | harness |
| `react-frontend/` | Harness-level: React frontend patterns | harness |

> These 9 subdirectories are **harness-level** — they provide patterns the OpenCode harness uses
> to coordinate agents, but they are **not** the canonical SOFI skills (those are the 116 in
> `.opencode/skills/`).

---

## What lives here vs. `.opencode/skills/`

| Type | Location | Binding? | Description |
|------|----------|----------|-------------|
| **SOFI operating manuals** | `.opencode/skills/` | YES (constitutional) | The 116 skills that bind to rooms |
| **Harness metadata** | `skills/` (this directory) | NO (harness) | 9 subdirectories of patterns + utilities |

The two are **clearly separated** by directory location. The harness uses both — the metadata
in `skills/` for routing, and the operating manuals in `.opencode/skills/` for actual skill execution.

---

## How to add to this directory

1. Create the subdirectory with the standard pattern (frontmatter + body)
2. If it affects SOFI (e.g. references a constitutional concept), ensure it cites `file:line` per Law 4
3. Commit atomically — pre-commit enforces all 4 guards

**Forbidden:** adding SOFI operating manuals here (they belong in `.opencode/skills/`).

---

## See also

- [Top-level README](../README.md)
- [`.opencode/skills/README.md`](../.opencode/skills/README.md) — the 116 canonical SOFI skills
- [`hq/core/domain/SKILLS-ASSIGNMENT.md`](../hq/core/domain/SKILLS-ASSIGNMENT.md) — skill ownership
- [`.opencode/README.md`](../.opencode/README.md) — operating layer
- [`AGENTS.md`](../AGENTS.md) — supreme law
