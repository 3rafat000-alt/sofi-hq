# `.opencode/` — Operating Layer (Article 00 — Single Source of Truth)

> The **operating layer** of SOFI HQ. This directory is loaded directly by the OpenCode (or
> compatible) harness. Per **Constitution Article 00**, this is the **sole source of truth**
> for the runtime — every agent file here must 1:1 match `hq/core/nexus/registry.yaml`.

> **The 4 constitutional guards enforce this on every commit:**
> - `registry_guard` (Law 12) — `registry.yaml` ↔ `.opencode/agent/*` ↔ `domain/rooms/*/agents/*` capsules
> - `count_sync` (Law 12/13) — derived vs declared vs textual vs disk
> - `evidence_guard` (Law 4) — every `file:line` resolves
> - `gitleaks` (Law 8 + P-08.1) — no secrets in code

---

## What's in this directory

| Item | Nature | True source | Current state |
|------|--------|-------------|---------------|
| `agent/*.md` | **Canonical agent specifications** (single source of truth) | Article 00 — `.opencode/agent/` IS the source | **121 files** |
| `skills/` | Skill installation area (the operating manuals) | binding ownership in `hq/core/domain/rooms/<room>/capabilities/skills.yaml` | **116 skills** |
| `package.json` | OpenCode runtime dependencies | tool-managed | version-pinned |
| `node_modules/` | OpenCode runtime node packages | tool-managed | gitignored |
| `command/` | OpenCode CLI commands (per harness) | tool-managed | harness-level |
| `package-lock.json` | OpenCode runtime lockfile | tool-managed | version-pinned |

---

## The binding rules

1. **To add/edit an agent:** modify `.opencode/agent/<name>.md` directly (this is the source of truth) + add the capsule in `hq/core/domain/rooms/<room>/agents/<name>/{capabilities,senses,memory}.yaml` + update `hq/core/nexus/registry.yaml` + `personas.yaml` + `routing.yaml` + bump `AGENTS.md:62,256` + commit atomically.
2. **To add/edit a skill:** create `.opencode/skills/<name>/SKILL.md` with frontmatter (name · description · when · inputs · steps · outputs · handoff · constraints · memory · refs) + add row to `.opencode/skills/INDEX.md` + bump `SKILLS_BASELINE` in `registry_guard.py:20` + `count_sync.py:22`.
3. **To regenerate the mirror:** `node hq/core/tooling/port-agents.mjs` (the harness mirror in `.kilo/agent/` is generated, never hand-edited).
4. **The official counts** in `hq/core/nexus/registry.yaml` (17 rooms · 121 agents) + `count_sync.py:22` (`SKILLS_BASELINE = 116`) govern every generation. Mismatch = loud failure.

---

## How to use this directory

```bash
# List all agents
ls .opencode/agent/*.md | wc -l    # → 121

# List all skills
ls -d .opencode/skills/*/         # → 116 directories

# Read an agent
cat .opencode/agent/qa-laravel-architect.md

# Read a skill
cat .opencode/skills/qa-laravel-architect/SKILL.md

# Verify the constitutional guards
python3 hq/core/tooling/sofi-audit.py
```

---

## The agent file format (frontmatter + body)

Every agent file follows this structure:

```markdown
---
name: <kebab-case-agent-name>
description: <name> — <role> in the <room> room
mode: subagent
model: opencode/big-pickle
---

# <Name> — <Role>

> ⚡ Structural update 2026-08-25 — read first: the system's structure...

## 🎯 Core Purpose
<one-line purpose>

## 🧠 Identity & Expertise
- **Name:** <Arabic name>
- **Role:** <role>
- **Room:** <room>
- **Skills:** <skills>
- **Mindset:** <mindset>

## 🛠️ Responsibilities
1. ...
2. ...
3. ...

## 🚫 Constraints
- ...

## 🔗 Team Collaboration
- **Inputs:** ...
- **Outputs:** ...
- **Escalation:** ...

## 🧰 Available Skills <!-- SKILLS-WIRED -->
- **Your domain playbook:** <name>
- **Before any delivery:** sofi-evidence (Law 4)
- **At delivery:** sofi-handoff (Law 3)
Full index: `.opencode/skills/INDEX.md`. Violate no law — skipping CEO/delivery skills is rejected.

## ⬛ Linear Program v2 (OWNER-DIRECTIVE-2026-0823-R2)
- **Phase map (official v2):** S1 → S2 → S3 → S4 → S5 → S6
- **Your position:** <where in the S1-S6 line>
- **Binding laws:** OpenAPI-first · no mocks crossing boundaries · api-envelope · ddd-capsule
- **Delivery:** sofi-handoff + sofi-evidence
```

---

## The skill file format (frontmatter + body)

```markdown
---
name: <kebab-case-skill-name>
description: <multi-line description — when to invoke>
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
- ...

## 🔗 Handoff
- ...

## ⛔ Constraints
- ...

## 🧠 Memory
- ...

## 📚 References
- ...
```

---

## The 4 guard scripts that enforce this directory

```bash
# 1) registry_guard — .opencode/agent/* 1:1 with registry.yaml
python3 hq/core/tooling/registry_guard.py --strict
# Expected: PASS · zero pending

# 2) count_sync — derived vs declared vs textual vs disk
python3 hq/core/tooling/count_sync.py
# Expected: PASS · zero pending

# 3) evidence_guard — every file:line resolves
python3 hq/core/tooling/evidence_guard.py hq/core --strict
# Expected: PASS · 0 broken

# 4) gitleaks — no secrets in code
gitleaks git --staged --pre-commit --config gitleaks.toml
# Expected: no leaks found
```

All 4 are wired into `hq/core/tooling/hooks/pre-commit:1` (installed via `hooks/install.sh`).

---

## The license (Law 15)

Every dependency in `package.json` must be:
- **Allowed license:** MIT · Apache-2.0 · BSD-2/3 · ISC · MPL-2.0
- **Vetoed:** GPL/AGPL/SSPL/unknown

To check: `python3 hq/core/tooling/sofi-security-scanner.py` (or the standalone gitleaks step).

---

## See also

- [Top-level README](../README.md)
- [`AGENTS.md`](../AGENTS.md) — Law 12
- [`hq/core/tooling/README.md`](../hq/core/tooling/README.md) — 4 guards
- [`hq/core/nexus/README.md`](../hq/core/nexus/README.md) — the registry
- [`hq/core/standards/latest-version-mandatory.md`](../hq/core/standards/latest-version-mandatory.md) — Context7 + DeepWiki
- [`.opencode/skills/INDEX.md`](./skills/INDEX.md) — 116 skills
