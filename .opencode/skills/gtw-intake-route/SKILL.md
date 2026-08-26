---
name: gtw-intake-route
description: >-
  The mandatory flow entry point (Law 1) — invoked whenever raw user speech arrives before distribution: understanding intent, reformulating into a 5-section prompt, gate check, budget check, conflict resolution, then routing to brd-ceo. Triggers — "new request", "intake user input", "reform the prompt", "gate check", "route to CEO", "budget check", "resolve request conflict". Invoked by gtw-dispatcher on every user input before the flow starts.
---

# gtw-intake-route — The Gateway Playbook (Intake → Gate → Route) ⬛

> **Law 1:** every session, every request, every message starts at the gateway — no exceptions. This playbook converts raw speech into an ideal, checked, and routed prompt for brd-ceo. Skipping the gate = L4 (immediate halt, restart from intake).

## 🎯 When to invoke (When) ⬛
- Raw user speech arrives (Arabic/English/mixed) — the first entry point before any distribution (Law 1).
- A request needs reformulation into a 5-section prompt before handing it to the CEO.
- An acceptance gate before routing: completeness, authority, no constitutional violation.
- A budget/cost feasibility check before committing resources.
- Conflict or duplication between two requests needing settlement at the gate before escalation.

**Do not invoke** for: work in progress inside an executive room under a standing RCCF order (that room's own playbook, not the gateway), or a fateful Board decision (that's `brd-decision-gate`).

## 📥 Required inputs (Inputs) ⬛
- **The user's raw speech** — the only input that precedes RCCF (Law 1: the gate precedes the work order).
- Missing context from memory: `memory_index/memory-index.md`, `hq/brain/brain-index.md`, `hq/brain/cortex-decisions.md` (the living decisions log — read before drafting).
- The cost/resource baseline for feasibility checking.
- **RCCF (Law 5):** the gate prepares and routes; it never executes work on a project. Any subsequent execution in a room requires an RCCF work order issued by the CEO — block any work reaching a room without RCCF.

## 🔧 Steps (Steps) ⬛
1. **Receive and understand:** detect the language, grasp the real intent behind the raw request (delegate `gtw-intake-reformer` via Task — same-room peer, Law 2).
2. **🆕 The ten questions protocol (mandatory for project build/development requests):** before any drafting or routing, ask the owner **10 simple non-technical questions in Arabic, each with 5 ready-made numbered options to choose from** — the full official bank lives in agent `gtw-intake-reformer` §Bank. Binding rules:
   - Fully simplified Arabic language — not one technical term (no API, schema, or deploy).
   - «I don't know» is a legitimate answer ← pick the best fit from their previous answers' context and justify your pick in one plain sentence.
   - After the ten: a **confirmation summary** — "this is what I understood from you… right?" — no routing before they confirm.
   - Small edit or follow-up requests on existing work = exempt; the ten apply to new projects and substantial features.
3. **Search context:** read memory (MEMORY/BRAIN/DECISIONS) and fill gaps before drafting — never pass raw text through untouched.
4. **Reformulate** into a 5-section prompt: Executive Summary / Full Context / Specific Request / Constraints & Considerations / Expected Deliverables.
5. **Gate check** (`gtw-gatekeeper`): completeness + authority + no constitutional violation — a PASS/FAIL result per criterion.
6. **Budget check** (`gtw-budget-warden`): estimate cost/resources → a `WITHIN` or `OVER` verdict with numbers.
7. **Conflict check** (`gtw-conflict-resolver`): if a conflicting/duplicate request exists → settle it or raise it as an explicit flag.
8. **Classify the lane** (`gtw-router` + `str-gate0-classify`) — Law 1 (proportional flow). Determine type/risk/size, then choose:
   - 🟢 **Fast:** reading/check/query/documentation or a trivial reversible single-file fix — provided `risk ≤ low`, `size ≤ S`, and no money/security/privacy/schema/production. **The gate approves these itself** (no per-task CEO approval — this is the speed secret).
   - 🟡 **Standard:** a feature/change spanning 1–2 rooms → **brd-ceo**.
   - 🔴 **Fateful:** money/security/architecture/production/schema/irreversible → **brd-ceo + Board (brd-cso veto)**.
   **Guarding:** doubt escalates upward (fail-safe). Money/security/production/schema = always fateful however small (breach = L3). Discovering higher risk later → immediate promotion, never downgrade.
9. **Routing decision:** Fast → directly to the single competent room lead (delivery on completion via the lead). Standard/Fateful → **brd-ceo** exclusively.
10. Produce the evidence block (below) and deliver it to the destination per the lane.

## 📤 Outputs + evidence (Outputs & Evidence) ⬛
- **Output:** an Intake Report with 5 sections + gate verdict + budget verdict + routing decision → delivered to brd-ceo.
- **Evidence (Law 4) — Gateway/Routing type:** use the `sofi-evidence` skill:
  - Intake Report: the five sections + raw speech verbatim + context sources (`file:line` in MEMORY/BRAIN).
  - Gate checklist: PASS/FAIL per criterion + reason.
  - Budget verdict: estimated cost + `WITHIN`/`OVER` + figures.
  - Routing decision: destination (brd-ceo) + routing reason + any room-lead recommendation for the CEO.
  - Conflict record: discovered conflicts + resolution/flag.

```
### Gateway Intake-Route Record
- intake_id: <PRJ-ID>-INT-<seq>
- raw_input: <raw speech verbatim>
- intake_report: [Exec Summary | Full Context | Specific Request | Constraints | Deliverables]
- gate: PASS|FAIL — <criterion: reason>
- budget: WITHIN|OVER — <estimate + figures>
- conflict: none|resolved|FLAGGED — <detail>
- lane: FAST|STANDARD|FATEFUL — <type/risk/size + classification reason>
- route_to: <lead-name> (FAST) | brd-ceo (STANDARD/FATEFUL) — <reason + recommendation>
- evidence_refs: <memory_index/memory-index.md:line, BRAIN.md:line>
```

## 🔗 Handoff ⬛
- Deliver the Intake Report to **brd-ceo** only (Law 3 — hierarchical delivery: gate → CEO) via the `sofi-handoff` skill. The gateway's only functional output goes upward to the CEO.
- Gateway agents are coordinated inside the room via Task (Law 2 — same-room peers). No addressing executive rooms directly; the CEO distributes downward.
- No direct reply to the user — final delivery to the user stays a CEO step within the flow (P-01.2), never part of this verdict.

## ⛔ Constraints ⬛
- Bypassing the gate as entry point = **L4** (immediate halt, restart from intake — Law 1).
- Passing raw speech through as-is forbidden — cleaning, expansion, and reformulation are mandatory before the CEO.
- Skipping the CEO allowed **only within the fast track's limits** (self-approval by the gate, L1). In Standard/Fateful, skipping the CEO = L3. Skipping a room lead = L3 on all lanes. Classifying a fateful task as Fast = L3.
- No execution without RCCF (Law 5 = L2); the gate prepares and routes, never executes project work.
- Direct delivery to the user forbidden (Law 3 = L3/L4).
- No evidence block = delivery rejected (Law 4 = L2).
- Never override any of the thirteen laws.

## 🧠 Memory ⬜
- Record important routing/gate/budget decisions in `hq/brain/cortex-decisions.md` (Law 7), document sessions in `hq/brain/hippocampus-sessions.md`, and any budget block/emergency in `hq/brain/amygdala-incidents.md`.

## 📚 References ⬜
- Room agents: `gtw-intake-reformer`, `gtw-gatekeeper`, `gtw-budget-warden`, `gtw-conflict-resolver`, `gtw-router`.
- `hq/core/protocols.md` (P-01 mandatory flow), `hq/core/contracts.md`.
- The `sofi-evidence` and `sofi-handoff` skills for evidence and hierarchical delivery.

## ⬛ Linear Program v2 (OWNER-DIRECTIVE-2026-0823-R2)
- **Your position:** this skill executes stage S1 fully. The official v2 map (source: `hq/core/nexus/gates.yaml#stage_map`): S1 idea, strategy, research (PRD · 00·01·14·02) → S2 data and contracts on paper (ERD+frozen OpenAPI · 04·08·05) → S3 experience and visual system + DFR signature (03 with 09·10) → S4 live security-checked backend (08·05) → S5 unified Flutter/Dart dual interfaces (merged team 06·07) → S6 shield and production (09-13).
- **Add to its flow:** when reformulating, identify the stage owning the request and its expected output per `hq/core/nexus/pipeline.yaml`, and warn brd-ceo immediately if the user asks to skip a stage or start interfaces before the contract.
- **The four binding laws:** OpenAPI-first; no cross-boundary mocks (internal testing substitutes exempt); Envelope per `hq/core/standards/api-envelope.md`; DDD capsule per `hq/core/standards/ddd-capsule.md`.
- **Delivery:** via `sofi-handoff` + `sofi-evidence` evidence in file:line form for every change and reference.

---

## 🚦 Mandatory approval points for build projects (Approve/Reject Gates — INT-EVOL-2)

**The owner's governing rule:** thinking ← planning ← research and analysis ← plan ← routing ← design and wireframe ← architecture — **then his explicit approve or reject at each point, and before any line of code:**

| Point | When | What is presented to the owner to approve or reject |
|--------|-----|----------------------------------|
| ✋ **1 — Scope & plan** | after research and analysis (S1) | exactly what we will build and what we won't · the timeline · candidate technologies in plain language |
| ✋ **2 — Look & design** | after wireframes and mockups (S3) | screen shapes, colors, and fonts as understandable images without jargon |
| ✋ **3 — Technical plan** | after architecture and contract (S2/S3) | how it will work inside, explained by metaphor not jargon |
| ✋ **4 — DFR signature then production quality** | DFR = design freeze at end of S3 (security+quality signature before any code) · G5 = the quality gate inside S6 | rejecting designs returns to S3; rejecting code returns to the owning stage |

An owner rejection at any point = returning the owning stage for correction — **writing any code before all four points are approved is forbidden** (consistent with the design-first doctrine INT-0004 and the S1..S6 line).

## 🛰️ Related deployment standard
Deployment/hosting requests are routed per the official deployment standard `hq/core/standards/deploy-standard.md` (Caddy + PHP-FPM + Cloudflare + Laravel + Flutter/React&Next interfaces with documented flexibility) — the default deployment proposal for the owner is presented within the ten questions (question 9) in plain terms.
