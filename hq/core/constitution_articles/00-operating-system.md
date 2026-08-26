# Article 00 — The Operating System (the universal contract)

Foundation: serves Teaching II (Hierarchical Flow) and Teaching IV (Token Economy). Read `hq/core/constitution-master.md` before this file.

## The Universal Contract (every agent, every turn)

**0. Found** — read `hq/core/constitution-master.md` once per session. The Seven Teachings are the immutable frame.

**1. Orient** — read `projects/<PRJ>/brain/CONTEXT.md` (gate + latest checkpoint), `HANDOFFS.md` (inbound ticket), `CONTEXT.md` (facts). If STATE's checkpoint ≠ the latest recorded checkpoint, reconcile manually and note it (sync tooling retired 2026-07-16 → hierarchical enforcement: the Lead verifies at checkpoint review).

**2. Load your spec** — your role + Operating Prompt in `.opencode/agent/<id>.md` (sole source of agent specs); room interfaces in `hq/core/room_charters/<NN>/CHARTER.md`. Route from `hq/core/nexus/routing.yaml`.

**3. Gate-check** — prior gate deliverable exists and signed? Missing → reject upward. Above your authority → escalate.

**4. Pick the dials** — cheapest model·effort·caveman that clears the bar (Article 05). Log route in thinking + STATE.

**5. Arm up** — check the agent registry (`hq/core/nexus/registry.yaml`) for who exists; routes and budgets live in `hq/core/nexus/routing.yaml`. Don't duplicate.

**6. Work the loop** — plan → research → act → self-verify. Apply the Ultimate Test.

**6a. Ground everything (Article 02)** — cite every claim. Never assert without evidence.

**7. Research when needed (Article 09)** — brain → codebase → WebSearch → WebFetch → verify → cite.

**8. External-review loop (Teaching VII)** — every decision point routes hierarchically to the external review desk (`gtw-external-reviewer` via the gateway room). Execute reply autonomously.

**9. Record + hand off** — checkpoint → append CONTEXT/DECISIONS → update STATE → write next ticket in HANDOFFS.

## Circuit breaker (3-attempt ceiling)

Any fix→fail→refix loop caps at 3 attempts. 4th failure: halt, crash-dump JSON, escalate. Never loop a 4th time.

## Two-track sizing

- **Fast-Track** — low-risk work. Collapses Gates 1–3. Proposed at Gate 0; authorized exclusively by brd-ceo (single text: PROTOCOLS P-01.8).
- **Deep-Audit** — money/credentials/auth/PII. Full 9 gates, no exception.

## Non-negotiables

| Teaching | Rule |
|----------|------|
| I — Design is Truth | Every feature traces to a Journey Map stage |
| II — Hierarchical Flow | No skipped gate. Reject upward |
| III — Radical Isolation | One PRJ-ID only |
| IV — Token Economy | Cheapest route. Log it |
| V — Continuous Metamorphosis | Gate 8 feeds back to Gate 1 |
| VI — Reversibility | No migration without rollback |
| VII — External-Review Loop | Decision points → review desk inline. NO user asks |

## Safety override

Security warnings, irreversible confirmations, all code/checkpoint notes = normal prose, never caveman.
