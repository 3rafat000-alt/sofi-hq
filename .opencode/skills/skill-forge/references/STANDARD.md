# SOFI Skill Authoring Standard

> The governing law for authoring every SOFI skill. Derives from the constitution (`hq/core/constitution-master.md`) and the protocols. Violating it = the skill is rejected.

---

## 1. Design Principles

- **Single responsibility.** One skill does one thing well. "Do everything" = do nothing.
- **Trigger before content.** `description` decides invocation. Write it first and test it mentally: "would phrase X invoke this?".
- **Bilingual heritage, English-first.** Triggers were Arabic + English; per workspace policy they are now English.
- **Progressive disclosure.** SKILL.md concise (< ~200 lines). Long details go to `references/`. Never drown the context.
- **Executable.** Steps as actions, not philosophy. The agent executes, not contemplates.
- **Constitutional by design.** Every skill enforces Laws 2/3/4/5 on its outputs — never leave them optional.

## 2. Naming

- Room skill: `<prefix>-<kebab>` — prefix = room code (`sec-`, `qa-`, ...).
- Shared skill: `sofi-<kebab>`.
- Folder name = `name` field = exactly, no spaces, kebab-case only.

## 3. Mandatory Constitutional Compliance

Every skill, without exception, satisfies:

| Law | What the skill enforces |
|---------|------------------|
| 2 — Isolation | never instruct addressing another room directly |
| 3 — Hierarchical handoff | output → room lead, not the user |
| 4 — Evidence | every output accompanied by a verifiable evidence block |
| 5 — RCCF | remind to request a work order before execution |
| 7 — Memory | important decisions → CORTEX/HIPPOCAMPUS |
| 8 — Quality | no delivery without review |

## 4. Structure

- All mandatory ⬛ sections present (When / Inputs / Steps / Outputs+Evidence / Handoff / Constraints).
- Examples specific and realistic, never vague placeholders.
- `references/` for any content longer than one section (templates, tables, extended examples).

---

## Validation Checklist (the approval gate)

Pass every item. Any **failure (❌)** = skill rejected, not approved.

- [ ] `name` in frontmatter = exact folder name, kebab-case, with the correct prefix.
- [ ] `description` describes *when*, not *what*, and carries invocation triggers.
- [ ] Frontmatter passes strict YAML (`python3` + `yaml.safe_load`); any `description` containing `:` is written as a block scalar: `description: >-`.
- [ ] All ⬛ sections present and filled (no leftover placeholder).
- [ ] Evidence section names the correct evidence type per agent type (Protocol 03 §P-03.8).
- [ ] Handoff section states hierarchical delivery to the room lead (Law 3).
- [ ] No step bypassing CEO or room lead, nor delivering to the user directly.
- [ ] No step has an agent addressing another room directly (Law 2).
- [ ] Skill reminds about RCCF (Law 5) in Inputs.
- [ ] SKILL.md < ~200 lines; long detail lives in references/.
- [ ] No duplication of an existing skill in `INDEX.md` (you searched first).
- [ ] One owner defined (room/lead) — Law 9.
- [ ] Registered in `INDEX.md` and the approval decision logged in CORTEX.

**Result:** all items ✅ → approve. Any ❌ → fix then re-validate.

---

## Common mistakes (Anti-patterns) — avoid them

- ❌ A description explaining what the skill does instead of when to invoke it → it never gets invoked.
- ❌ A giant skill covering an entire room → split into playbooks.
- ❌ Steps without evidence → output rejected at the gate.
- ❌ "Deliver results to the user" → L3 violation.
- ❌ Copying all content into SKILL.md → context flooding. Use references/.
