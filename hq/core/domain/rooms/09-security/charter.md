# Security Room

> **⚡ Structural update 2026-08-25 — read first:** The system structure and operating model have changed ("sakk only" cleanup + root simplification + archival of institutional memories). The updated binding source is `hq/core/system-state-current.md` — interpret any legacy path in your texts against it.
**Room:** 09-security
**Code:** sec
**Room lead:** `sec-lead`

---

## | Identity

**Purpose:**
Application security, penetration testing, compliance, secrets management

**Agent count:** 9

---

## | Agent Roster

- `sec-lead` — lead
- `sec-pentester` — pentester
- `sec-appsec-engineer` — appsec-engineer
- `sec-authn-engineer` — authn-engineer
- `sec-compliance-auditor` — compliance-auditor
- `sec-incident-responder` — incident-responder
- `sec-threat-modeler` — threat-modeler
- `sec-secrets-warden` — secrets-warden
- `sec-license-auditor` — license-auditor *(2026-08-26: dependency license & IP gate before every merge · Law 15)*

**Operational agent definitions:** `.opencode/agent/` — the single source of truth.

---

## | Standard Operating Procedure (SOP)

1. Review every stage gate
2. Produce threat models
3. Audit code and infrastructure
4. Report vulnerabilities
5. Escalate to the CSO when necessary

---

## | Connected Rooms

All rooms (cross-cutting)

---

## | Gate Ownership

**My stage in production line v2:** S3 (DFR signature) · S6 (security-signoff) — full map at `nexus/gates.yaml#stage_map`.

Gate-0–8 (audit) · **DFR — mandatory signature alongside qa-lead at the end of S3**: review of data + API + interfaces before the first line of code (`gates.yaml#dfr`)

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

- **Room playbook:** `sec-threat-model` + `sec-mcp-vetting` — invoked through the Skill tool for room tasks.
- **Shared (mandatory):** `sofi-evidence` (Law 4) before any delivery · `sofi-handoff` (Law 3) for every hierarchical handoff.
- **External room skills:** `api-compliance-checker` · `mcp-builder`
- **Full map:** `.opencode/skills/INDEX.md`.

---

## | Room Law

The Security Room operates within the bounds of the constitution (hq/core/constitution-master.md).
All decisions comply with the Room Isolation Law.
Communication with other rooms happens through the room lead only.
