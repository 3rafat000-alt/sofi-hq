# SKILL.md — The Unified Template (SOFI Skill Template)

> Copy this file to `.opencode/skills/<name>/SKILL.md` and fill it in. ⬛ = mandatory section. ⬜ = optional as needed.
> Delete these guiding lines after filling.

```markdown
---
name: <room-prefix>-<kebab-name>
description: <when invoked — English triggers. One or two sentences. Real phrases a student would say. Not "what it does".>
---

# <name> — <the clear title> ⬛

> <one line: the skill's core value — why it exists.>

## 🎯 When to invoke (When) ⬛
- <use case 1>
- <use case 2>
**Do not invoke** for: <a nearby but wrong case — prevents over-invocation>

## 📥 Required inputs (Inputs) ⬛
- RCCF work order (Law 5) — no execution without it.
- <skill-specific input: file, URL, scope...>

## 🔧 Steps (Steps) ⬛
1. <precise actionable step>
2. <...>
3. Produce the evidence block (see below).

## 📤 Outputs + evidence (Outputs & Evidence) ⬛
- Output: <exactly what is produced>
- **Evidence (Law 4):** per agent type — use the `sofi-evidence` skill:
  - Engineer → `file:line` per change + exit code + test output
  - Designer → screenshot before/after + design tokens + a11y
  - Researcher → source URL + query + extract + confidence
  - Architect → diagram + ADR + migration plan
  - Security → threat model + scan + pentest report
  - QA → test plan + results + coverage + regression
  - DevOps → deploy log + health check + rollback plan

## 🔗 Handoff ⬛
- Deliver output to the **room lead** only (Law 3) via the `sofi-handoff` skill.
- No direct delivery to the user. No addressing another room (Law 2).

## ⛔ Constraints ⬛
- <specific constraint>
- Never override any of the thirteen laws.

## 🧠 Memory ⬜
- Record important decisions in `hq/brain/cortex-decisions.md` (Law 7).

## 📚 References ⬜
- <additional references/ files, internal links>
```

---

## Quick fill-in rules

1. `name` in the frontmatter = exactly the folder name.
2. `description` is the most important line — without good triggers the skill is never invoked.
3. Do not delete any ⬛ section.
4. Keep steps executable (verb + object), not vague descriptions.
5. Every skill ends with evidence + hierarchical handoff. No exceptions.
