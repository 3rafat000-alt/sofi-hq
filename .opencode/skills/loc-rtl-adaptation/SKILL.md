---
name: loc-rtl-adaptation
description: >-
  Arabic localization & RTL adaptation protocol — translation memory + cultural adaptation + RTL mirror validation + voice & tone, applied per locale for SOFI products (audit P1 gap). Triggers — "localize this screen", "translate to Arabic", "RTL mirror", "voice & tone guide", "cultural adaptation Arabic", "Law 11 Arabic simple", "DSN DFR Arabic co-sign". Invoked by loc-translation-manager (room 08) on any Arabic copy or RTL change — never for general translation (use deepwiki/context7) or DSN (use dsn-design-handoff).
---

# loc-rtl-adaptation — Arabic Localization & RTL Adaptation Protocol

> **Core value:** end-to-end Arabic localization — translation, cultural adaptation, RTL mirror, voice & tone — one coherent per-locale pipeline feeding DFR co-sign.

## 🎯 When to invoke (When) ⬛
- Any Arabic copy, UI string, or RTL change arrives needing adaptation
- A screen needs Arabic mirror validation + cultural imagery review
- Voice & tone must be unified across localized strings (Law 11)
**Do not invoke** for: general translation quality (use deepwiki MCP) · DSN design tokens (use dsn-design-handoff) · security review (sec-threat-model).

## 📥 Required inputs (Inputs) ⬛
- RCCF work order from `loc-translation-manager` (Law 5)
- Source strings (English) + design tokens + RTL mirrors
- The approved `glossary-ar.md` + `voice-and-tone.md` standards

## 🔧 Steps (Steps) ⬛
1. **Translate:** `loc-translation-manager` runs translation memory + glossary check — `file:line` per term
2. **Adapt culturally:** `loc-cultural-adapter` reviews imagery/examples — `file:line` evidence
3. **Mirror RTL:** `loc-rtl-specialist` applies `rtl-mirror-validator` + screenshots 360/768/1024
4. **Voice & tone:** `loc-voice-tone-expert` unifies Law 11 Arabic simple
5. **DFR co-sign:** `loc-rtl-specialist` co-signs DFR with dsn-lead + sec-lead + qa-lead
6. **Hand off:** `loc-translation-manager` → dsn-lead → brd-ceo (Law 3)

## 📤 Outputs + evidence (Outputs & Evidence) ⬛
- Output: localized strings + RTL screenshots + DFR co-sign
- Evidence (Law 4): `sofi-evidence` — `file:line` per translation + RTL screenshots + glossary diff
- Handoff: `sofi-handoff` ticket to `loc-translation-manager`

## 🔗 Handoff ⬛
- Deliver to `loc-translation-manager` only (Law 3)
- No direct delivery to user · no other-room addressing (Law 2)
- DFR co-sign is mandatory before any Arabic UI ships

## ⛔ Constraints ⬛
- Advisory on Arabic quality; DFR + Gate-5 are the binding gates
- Glossary + voice-and-tone are binding (Law 7 — kept in `hq/core/standards/`)
- Privacy (PII Arabic copy) escalates to `loc-privacy-officer` (room 08)
- License (Law 15): no paid translation API without sec-license-auditor

## 🧠 Memory ⬜
- Per Law 7: project localization in `projects/<slug>/brain/localization/`
- Org glossary in `hq/core/standards/glossary-ar.md` (TBD)

## 📚 References 📚
- `hq/core/domain/rooms/08-localization/charter.md:1` · `.opencode/skills/rtl-mirror-validator/SKILL.md` · `hq/core/standards/uiux-standard.md`
