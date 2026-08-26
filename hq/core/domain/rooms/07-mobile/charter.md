# Mobile Room

> **⚡ Structural update 2026-08-25 — read first:** The system structure and operating model have changed ("sakk only" cleanup + root simplification + archival of institutional memories). The updated binding source is `hq/core/system-state-current.md` — interpret any legacy path in your texts against it.
**Room:** 07-mobile
**Code:** mob
**Room lead:** `mob-lead`

---

## | Identity

**Purpose:**
Mobile apps, Flutter, on-device performance

**Agent count:** 6

---

## | Agent Roster

- `mob-lead` — lead
- `mob-flutter-engineer` — flutter-engineer
- `mob-platform-engineer` — platform-engineer
- `mob-state-engineer` — state-engineer
- `mob-perf-profiler` — perf-profiler
- `mob-release-engineer` — release-engineer

**Operational agent definitions:** `.opencode/agent/` — the single source of truth.

---

## | Standard Operating Procedure (SOP)

1. Receive designs from dsn-lead
2. Develop the app
3. Test on real devices
4. Review performance
5. Hand off to brd-ceo (consulting dsn-lead is allowed without delivering)

---

## | Connected Rooms

03-design (design), 05-backend (API), 10-quality (quality)

---

## | Gate Ownership

**My stage in production line v2:** S5 — merged Flutter/Dart team (Gate-4b); locked until S4 is complete — full map at `nexus/gates.yaml#stage_map`.

Gate-4 (Build)

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

- **Room playbook:** `mob-feature-build` — invoked through the Skill tool for room tasks.
- **Shared (mandatory):** `sofi-evidence` (Law 4) before any delivery · `sofi-handoff` (Law 3) for every hierarchical handoff.
- **External room skills:** `flutter-testing-skill`⭐ + flutter-*/dart-* suite (22) · `espresso-skill` · `xcuitest-skill` · `detox-skill` · `appium-skill`⚠️blocked until sec-lead review
- **Full map:** `.opencode/skills/INDEX.md`.

---

## | Room Law

The Mobile Room operates within the bounds of the constitution (hq/core/constitution-master.md).
All decisions comply with the Room Isolation Law.
Communication with other rooms happens through the room lead only.
