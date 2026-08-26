---
name: res-journey-map
description: >-
  Playbook for assembling the verified user-research dossier (journey map + JTBD-methodology personas + pain points + behavioral data + usability test scripts) and delivering it to the Design room via Contract 02 to close Gate-1. Triggers — Arabic: "research dossier", "user journey map", "personas and pain points", "JTBD user jobs", "usability test script", "research for design", "close Gate-1", "deliver user research". English: "research dossier", "journey map", "user personas", "JTBD jobs", "usability test script", "pain points", "behavioral data for design", "close Gate-1". Invoked by a Research room agent when brd-ceo/Design request verified user research as the source of truth for design decisions.
---

# res-journey-map — The User Research Dossier for Design ⬛

> **Value:** turns raw user research into one verified, methodologically documented dossier that becomes the Design room's source of truth — no design decision without research (Contract 02).

## 🎯 When to invoke (When) ⬛
- brd-ceo passes a ticket requesting user research before design starts (Gate-1 open).
- The Design room needs a journey map / personas / pain points / behavioral data as source of truth.
- Re-verifying an expired dossier (after 20 agent cycles — Contract 02).

**Do not invoke** for: pure market/competitor research (that's `res-competitor-analyst`), or designing interfaces themselves (that's the Design room — Law 2).

## 📥 Required inputs (Inputs) ⬛
- **Formal RCCF work order (Law 5)** — no execution without it; defines scope + success criterion + constraints.
- Target user persona/segment + the research question.
- Available sources: behavioral data, interviews, surveys, analytics, trusted web sources.
- SLA time limit (current session unless scope exceeds 10 cycles — Contract 02).

## 🔧 Steps (Steps) ⬛
1. **Read the RCCF**; fix scope and success criterion; if vague → return to your lead (never guess).
2. **Design the methodology first:** collection method, sample size/source, validity criteria — methodology mandatory (research without methodology = returned, Contract 02).
3. **Collect behavioral evidence** from actual sources; per claim log: source URL + query + literal extract + confidence (no LLM summaries — Law 4, Researcher type).
4. **Build Personas** from evidence-documented recurring patterns, never assumptions.
5. **Frame jobs with JTBD methodology:** per persona extract the job they hire the product for in «when [situation], I want [motivation], so I can [outcome]» form, classified functional/emotional/social — this is what later links research to design decisions (what to build and why), not demographics alone.
6. **Draw the Journey Map**: stages × (actions, thoughts, feelings, touchpoints) + **pain points** tagged with their source evidence, each tied to its JTBD job.
7. **Rank pain points** by severity and frequency, with a confidence level per item.
8. **Write usability test scripts** for the biggest doubts: measurable tasks ("complete X unaided") + a success question per task — consumed by Design/QA when field-validating assumptions.
9. **Review quality** (Law 8): every claim ← verifiable source evidence before delivery.
10. **Produce the evidence block** via the `sofi-evidence` skill (Researcher type).

## 📤 Outputs + evidence (Outputs & Evidence) ⬛
- **Output:** one research dossier with Contract 02's three sections:
  - `journey-map/` — journey stages, touchpoints, tagged pain points.
  - `persona/` — 1–3 evidence-based personas + JTBD jobs per persona.
  - `findings/` — findings + methodology + confidence level + recommendations + usability test scripts.
- **Evidence (Law 4) — Researcher type exclusively** (via `sofi-evidence`):
  - `source URL` per claim + used `query` + literal `extract` from source + `confidence` (high/med/low).
  - LLM-generated summaries/inferences **forbidden** as evidence — unverifiable evidence is rejected at the gate.
  - Methodology documented (collection method + sample) — without it the dossier returns.
- **Sample evidence line:** `Source: <url> → query:"onboarding drop-off" → "63% abandon at OTP step" (confidence: high)`.

## 🔗 Handoff ⬛
- Deliver the dossier to **your room lead `res-lead` only** (Law 3) via the `sofi-handoff` skill as an RCCF ticket, sections `journey-map/ · persona/ · findings/`.
- `res-lead` consolidates and delivers upward to `brd-ceo`; reaching the Design room goes through leads exclusively (Law 2) — **never address `dsn-lead` or any design agent directly**.
- Explicit delivery acceptance (P-02.4) closes **Gate-1**. No direct delivery to the user (Law 3).

## ⛔ Constraints ⬛
- No claim without `source URL + extract`; fabricating evidence = L3.
- Never bypass `res-lead`, never address another room directly (Laws 2/3) = L3.
- No execution without RCCF (Law 5) = L2.
- Dossier validity is 20 agent cycles; re-verification mandatory afterwards (Contract 02).
- Design never exceeds research findings without Board approval; disputes escalate via `res-lead` → `gtw-conflict-resolver` → `brd-arbiter`.

## 🧠 Memory ⬜
- Record methodology decisions and material findings in `hq/brain/cortex-decisions.md`, and the delivery receipt in `hq/brain/hippocampus-sessions.md` (Law 7).

## 📚 References ⬜
- `hq/core/contracts.md` → Contract 02 (Research Informing Design).
- Shared skills: `sofi-evidence` (Researcher type), `sofi-handoff` (RCCF).
- **Owner:** Research room (02) — `res-lead` (Law 9).

## ⬛ Linear Program v2 (OWNER-DIRECTIVE-2026-0823-R2)
- Position: this skill serves stage S1 (user research feeding the PRD — after Gate-1 before S2) per the v2 line.
- Operating condition: after S1's measurable success metric and before any wireframe in S2.
- Contracts: receive framing from Strategy; deliver a verified research dossier (JTBD personas + journey maps + pain points + usability scripts) feeding the Design room via Contract 02.
- CX indicators in their unified numeric forms NPS/CSAT/CES from hq/core/standards/knowledge-cx-uiux.md.
- Laws: OpenAPI-first; cross-boundary mocks forbidden (internal testing substitutes exempt); Envelope hq/core/standards/api-envelope.md; delivery sofi-handoff + sofi-evidence file:line.
