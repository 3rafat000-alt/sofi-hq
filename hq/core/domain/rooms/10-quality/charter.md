# Quality Room

> **⚡ Structural update 2026-08-25 — read first:** The system structure and operating model have changed ("sakk only" cleanup + root simplification + archival of institutional memories). The updated binding source is `hq/core/system-state-current.md` — interpret any legacy path in your texts against it.
**Room:** 10-quality
**Code:** qa
**Room lead:** `qa-lead`

---

## | Identity

**Purpose:**
Quality assurance, automation, performance testing, regression control

**Agent count:** 10

---

## | Agent Roster

- `qa-lead` — lead
- `qa-test-architect` — test-architect
- `qa-automation-engineer` — automation-engineer
- `qa-manual-explorer` — manual-explorer
- `qa-perf-analyst` — perf-analyst
- `qa-design-auditor` — design-auditor
- `qa-regression-warden` — regression-warden
- `qa-flutter-architect` — flutter-architect (Phase B — added 2026-09-05 per ADR-20260905-GTW-FLUTTER-QA-ARCHITECT)
- `qa-react-architect` — react-architect (Phase B — added 2026-09-05 per ADR-20260905-GTW-REACT-DDD-ARCHITECT)
- `qa-laravel-architect` — laravel-architect (Phase B — added 2026-09-05 per ADR-20260905-GTW-LARAVEL-DDD-ARCHITECT)

**Operational agent definitions:** `.opencode/agent/` — the single source of truth.

---

## | Standard Operating Procedure (SOP)

1. Review gate requirements
2. Plan the tests
3. Execute automation
4. Test manually
5. Issue the report
6. Give a PASS/BLOCK verdict

---

## | Connected Rooms

All rooms (cross-cutting)

---

## | Gate Ownership

**My stage in production line v2:** S3 (DFR signature) · S6 — stage lead (qa-verdict) — full map at `nexus/gates.yaml#stage_map`.

Gate-5 (Quality) · **DFR — mandatory signature alongside sec-lead at the end of S3**: freeze of all designs before the first line of code (`gates.yaml#dfr`)

---

## | Handoff Protocol

1. The agent completes its task and records evidence
2. The agent hands off to the room lead
3. The room lead reviews and unifies
4. The room lead hands off to brd-ceo
5. brd-ceo delivers to the user

**Forbidden:**
- An agent delivering directly to the user
- An agent addressing another room
- A room lead executing the work personally

---

## | Skills

- **Room playbook:** `qa-test-plan` — invoked through the Skill tool for room tasks.
- **Shared (mandatory):** `sofi-evidence` (Law 4) before any delivery · `sofi-handoff` (Law 3) for every hierarchical handoff.
- **External room skills:** `playwright-skill` · `cypress-skill` · `smartui-skill` · `webapp-testing` · `selenium-skill` · `webdriverio-skill` · `cucumber-skill` · `test-framework-migration-skill`
- **Full map:** `.opencode/skills/INDEX.md`.

---

## | Room Law

The Quality Room operates within the bounds of the constitution (hq/core/constitution-master.md).
All decisions comply with the Room Isolation Law.
Communication with other rooms happens through the room lead only.
