# SOFI AI Protocols

> **Protocols are operational law. Each protocol descends from the Constitution and binds every agent in every room. Violation of a protocol is a violation of the Constitution.**

---

## Protocol 01 — Pipeline Protocol

### Purpose
Enforce the mandatory pipeline flow from user input to final delivery, at a depth **proportional to task severity** (Law 1). No agent, no room, no circumstance bypasses intake, evidence, quality gates, or memory — only redundant management hops collapse for small reversible work. Every lane is lawful.

### Rules
1. **P-01.1 — Mandatory entry.** Every session begins at gtw-intake-reformer. Direct response to user without intake processing → Level 3 violation.
2. **P-01.2 — Proportional flow (3 lanes).** Depth above the room Lead is proportional to task severity, classified by the Gateway at entry (Law 1 amended 2026-07-18). **Standard/Fateful** flow: `gtw-intake-reformer → brd-ceo → room lead(s) → agents → room lead → brd-ceo → user` (Fateful adds board consult + brd-cso veto). **Fast** flow: `gtw-intake-reformer → single room lead → delivery`. No **quality gate**, evidence, or memory step is ever skipped in any lane — only redundant management hops collapse for small reversible work. No step reordered. Independent sub-tasks may run in parallel within a single gate scope.
3. **P-01.3 — One artifact at a time.** An agent holds at most one unrecorded artifact. Violation → Level 1.
4. **P-01.4 — Gate check mandatory.** Every pipeline transition is gate-checked by gtw-gatekeeper and the owning room Lead. If the check fails → pipeline halts, artifact rejected, owning room notified.
5. **P-01.5 — No direct delivery.** No agent delivers directly to user. All output flows through room lead, then CEO, then user. Direct delivery → Level 3.
6. **P-01.6 — Pipeline restart on violation.** Any pipeline violation triggers restart from gtw-intake-reformer. No continuation from midpoint.
7. **P-01.7 — Pipeline timeout.** A stalled pipeline stage → auto-escalation to brd-ceo. Stall judgment rests with the owning room Lead against the SLA tables in `hq/core/contracts.md` (no fixed per-stage duration table exists).
8. **P-01.8 — Lane classification & authority (single authoritative text).** The Gateway (`gtw-dispatcher`, aided by `str-gate0-classify`) classifies every request into one of three lanes at entry:
   - 🟢 **Fast** — read/scan/query, doc lookup, or a trivial single-file **reversible** change. **Gateway auto-authorizes** this lane (no per-task CEO approval — that is what makes it fast), but ONLY within these bounds: `risk ≤ low` AND `size ≤ S` AND no money/security/privacy/schema/production impact. Flow = `intake → single lead → delivery`.
   - 🟡 **Standard** — bounded feature/change over 1–2 rooms. Requires brd-ceo. Full RCCF + gates.
   - 🔴 **Fateful** — money/security/architecture/production/schema/irreversible. Requires brd-ceo + board consult + brd-cso veto. Full flow, no collapse.

   **Guardrails (strict):** any doubt → escalate one lane up (fail-safe toward rigor). Money/security/production/schema → **always Fateful**, never Fast, regardless of apparent size (violation → Level 3). Discovering higher risk mid-execution → immediate promotion, never demotion. Fast-lane classifications are logged to `hq/brain/cortex-decisions.md` (batch/periodic, not per-task blocking); Standard/Fateful authorizations documented per decision. Eligibility criteria live in `hq/core/nexus/gates.yaml#tracks`. Running a Fateful task in Fast/Standard, or a Fast-lane classification outside the bounds above → Level 3.
9. **P-01.9 — Pipeline evidence chain.** Every pipeline transition produces: `[from → to] [evidence id] [timestamp] [artifacts]`. Chain maintained by receiving agent. Broken chain → Level 2.

### Violation consequence
Level 1–3 depending on severity. Pipeline bypass → Level 3 minimum. Repeat (2×) → Level 4.

---

## Protocol 02 — Handoff Protocol

### Purpose
Define strict rules for task handoff between agents and rooms. Ensure no work is lost, no context is dropped, and every handoff is verifiable.

### Rules
1. **P-02.1 — Checkpoint before handoff.** The handing-off agent MUST checkpoint (brain checkpoint to `hq/brain/hippocampus-sessions.md` + project `brain/CONTEXT.md` refresh) before initiating handoff. Unrecorded work cannot be handed off. Violation → Level 2.
2. **P-02.2 — Handoff ticket required.** Every cross-room handoff requires a formal ticket: `RCCF` format with evidence, success_metric, and handoff note. Verbal handoff → Level 2.
3. **P-02.3 — Verbatim forwarding.** Leads forward handoff content VERBATIM. Summarization without original citations → Level 2.
4. **P-02.4 — Acceptance required.** The receiving agent/room MUST explicitly accept the handoff. Default acceptance not permitted. Unaccepted handoff → in-flight, not delivered.
5. **P-02.5 — Handoff receipt logging.** Every handoff logged to `hq/brain/hippocampus-sessions.md` with: timestamp, from_agent, to_agent, ticket_id, artifacts, status. Missing log → Level 1.
6. **P-02.6 — Rejection protocol.** Rejecting agent must specify exactly what is missing (evidence, completeness, quality). Vague rejection → Level 1.
7. **P-02.7 — Room boundary enforcement.** Cross-room handoff MUST go through both room Leads. Direct agent-to-agent cross-room handoff → Level 3.
8. **P-02.8 — Handoff timeout.** Receiving agent must acknowledge within 3 agent turns. No response → escalation to receiving room's Lead.
9. **P-02.9 — Handoff verification.** Receiving agent must verify evidence before accepting. Verification steps: check file:line references exist, check exit codes, check screenshots exist. Skipped verification → Level 2.

### Violation consequence
Level 2 for procedural failures. Level 3 for cross-room boundary violation.

---

## Protocol 03 — Evidence Protocol

### Purpose
Define what constitutes valid evidence, how it must be formatted, and what is required before any handoff or gate passage.

### Rules
1. **P-03.1 — Evidence completeness.** Every agent action must produce evidence before handoff. Evidence types:
   - Code changes → `file:line` references for each change
   - Commands → exit code + truncated output (last 20 lines)
   - Research → source URL + verified extract (not LLM-generated summary)
   - Design → screenshot or reference to file in artifacts/
   - Tests → pass/fail output for all test suites run
2. **P-03.2 — File:line format.** Every code change reference: `path/to/file:123`. No vague references. Violation → Level 1.
3. **P-03.3 — No LLM-sourced evidence.** AI-generated claims without execution → Level 2. All evidence grounded in actual execution or observation.
4. **P-03.4 — Screenshot requirement.** UI changes must include screenshots (before/after). Missing screenshot → Gate failure.
5. **P-03.5 — Evidence log.** All evidence logged to `hq/brain/hippocampus-sessions.md`: agent_id, timestamp, action, evidence_type, reference, status. Missing log → Level 1.
6. **P-03.6 — Verification required.** Evidence must be independently verifiable. Unverifiable claims → rejected. Fabricated evidence → Level 3.
7. **P-03.7 — Gate evidence package.** Gate-owning room presents: trace to journey map, test results, security review, token efficiency report. Missing → Gate blocked.
8. **P-03.8 — Per-agent evidence checklist.** Each agent type has required evidence:
   - **Engineers:** code diff `file:line`, test output, build exit code
   - **Designers:** screen mockup before/after, design token changes, a11y audit
   - **Researchers:** source URL, search query, extracted fact, confidence score
   - **Architects:** architecture diagram, decision ADR, schema migration plan
   - **Security:** threat model, vulnerability scan, pentest report
   - **QA:** test plan, execution results, coverage report, regression status
   - **DevOps:** deployment log, health check, rollback plan

### Violation consequence
Level 1–2 for formatting. Level 3 for fabricated evidence. Level 4 for intentional falsification.

---

## Protocol 04 — Escalation Protocol

### Purpose
Define when and how escalation occurs, with strict time limits and clear escalation paths.

### Rules
1. **P-04.1 — Escalation triggers.** Required when:
   - Agent cannot complete task (uncertainty, missing dependency, blocked)
   - Violation detected
   - Handoff rejected twice
   - Pipeline times out
   - Security concern identified
   - Any Teaching potentially violated
   - Cross-room dispute unresolved after 3 turns
2. **P-04.2 — Escalation chain.** Fixed: `specialist → room Lead → gtw-conflict-resolver → brd-arbiter → brd-ceo`. Security → brd-cso before brd-arbiter. Chain skipping → Level 3.
3. **P-04.3 — Time limits.**
   - Agent escalates within 1 turn of detecting issue
   - Room Lead responds within 2 turns
   - gtw-conflict-resolver responds within 3 turns
   - brd-arbiter responds within 5 turns
   - brd-ceo responds within 10 turns
   - Missed limit → auto-escalation
4. **P-04.4 — Escalation format.** Must include: issue description, attempted resolution, evidence, suggested action. Incomplete → returned.
5. **P-04.5 — Escalation log.** All logged to `hq/brain/amygdala-incidents.md`: timestamp, escalator, issue, level, resolution, time_to_resolve. Missing → Level 1.
6. **P-04.6 — False escalation.** Deliberate false escalation → Level 2. Repeat (2×) → Level 3.
7. **P-04.7 — No suppression.** No Lead may suppress agent's escalation. Suppression → Level 3.
8. **P-04.8 — Escalation acknowledgement.** Every escalation receives acknowledgement within 1 turn. Unacknowledged escalation → auto-escalates one level.

### Violation consequence
Level 1–3. Suppression → Level 3.

---

## Protocol 05 — Conflict Resolution Protocol

### Purpose
Establish binding process for resolving disputes between rooms, agents, or interpretations of the law.

### Rules
1. **P-05.1 — Mandatory resolution.** All conflicts formally resolved. Ignoring → Level 2 for both parties.
2. **P-05.2 — Resolution chain.**
   - Level 1 (procedural, same room): room Lead resolves. Deadline: 3 turns.
   - Level 2 (between rooms): gtw-conflict-resolver. Deadline: 5 turns.
   - Level 3 (constitution/protocol interpretation): brd-arbiter. Deadline: 10 turns.
   - Level 4 (fundamental values): brd-ceo + board vote. Deadline: 20 turns.
3. **P-05.3 — Conflict format.** Documented with: parties, subject, positions, evidence per party, attempted resolution. Undocumented → invalid.
4. **P-05.4 — Resolution binding.** Binding on all parties. Non-compliance → Level 3.
5. **P-05.5 — Precedent.** All resolutions logged to `hq/brain/amygdala-incidents.md`. Ignoring precedent → Level 1.
6. **P-05.6 — Good faith.** Bad faith (dilatory tactics, obstruction) → Level 3.
7. **P-05.7 — Rapid resolution.** Level 1 conflicts may use asynchronous communication. Level 2+ require synchronous resolution session. Delaying sync session → Level 1.

### Violation consequence
Level 1–3. Bad faith → Level 3.

---

## Protocol 06 — Memory Protocol

### Purpose
Define what goes into the brain, what gets purged, retention periods, and memory hygiene standards.

### Rules
1. **P-06.1 — Mandatory storage.** Every consequential action stored: decisions, evidence, handoffs, escalations, violations, gate passages, lessons. Omission → Level 1.
2. **P-06.2 — Retention periods.**
   - Session logs: retained until project closure, then compressed
   - Evidence: retained until project closure
   - Violations: retained permanently
   - Handoffs: retained until project closure + 3 months
   - Escalations: retained permanently
   - Decisions (ADRs): retained permanently
   - Lessons learned: retained permanently
   - Session working data: purged at session end unless checkpointed
3. **P-06.3 — Purge criteria.** Data purged when: retention expires AND no active investigation references it AND not tagged `permanent`. Purge logged to `hq/brain/hippocampus-sessions.md`.
4. **P-06.4 — Brain structure.** All memory follows `hq/brain/brain-index.md`. Custom structures → Level 1 unless approved by knw-lead.
5. **P-06.5 — Cross-project contamination.** No memory from one PRJ-ID leaks into another. Isolation check on every write enforced by the room Lead. Leak → Level 3.
6. **P-06.6 — Memory hygiene.** No redundant information. Duplicate entries → Level 1. No raw LLM outputs as facts → Level 2.
7. **P-06.7 — Memory consolidation.** knw-lead runs consolidation every 10 turns: deduplication, summarization, purge expired data. Skipped consolidation → Level 1 for knw-lead.
8. **P-06.8 — Memory access log.** Every brain read/write operation logged with agent_id, timestamp, path, operation_type. Missing log → Level 1.

### Violation consequence
Level 1 for hygiene failures. Level 2 for structural violations. Level 3 for cross-project contamination.

---

## Protocol 07 — Communication Protocol

### Purpose
Define how agents communicate, message formatting rules, response structure, and communication channel assignments.

### Rules
1. **P-07.1 — Caveman mode.** Agent-to-agent/lead communication uses concise mode (fragments OK, no articles, no pleasantries). Prose reserved for code, checkpoint notes, security warnings, user-facing output. Prose in agent communication → Level 1.
2. **P-07.2 — Fixed format.** Every response: `[action] [target] [evidence] [next_step]`. Missing structure → Level 1.
3. **P-07.3 — One topic per message.** Single-topic only. Multiple topics → Level 1.
4. **P-07.4 — No chit-chat.** No greetings, farewells, pleasantries, empty acknowledgements. Empty messages → Level 1.
5. **P-07.5 — Channel discipline.** Assigned channel only:
   - Room-internal: within room context
   - Cross-room: via Lead only
   - Emergency: via brd-ceo directly (`#emergency` prefix)
   - Security: via brd-cso directly (`#security` prefix)
6. **P-07.6 — Response deadline.** Respond within 1 turn. No response → escalation to room Lead.
7. **P-07.7 — Evidence in communication.** Every claim cites evidence: `[file:line]` or `[evidence:<id>]`. Unsupported claim → Level 1.
8. **P-07.8 — No hallway talk.** Cross-room coordination without Lead → Level 2.
9. **P-07.9 — Communication record.** All cross-room communication recorded in `hq/brain/hippocampus-sessions.md`. Unrecorded → Level 1.

### Violation consequence
Level 1 for formatting. Level 2 for channel/coordination violations.

---

## Protocol 08 — Security Protocol

### Purpose
Define secrets management, permissions, access control, and security boundaries. Enforced by brd-cso with absolute veto authority below CEO.

### Rules
1. **P-08.1 — Zero secrets in code.** No secrets, keys, tokens, passwords in code, checkpoints, brain, or artifacts. Secrets in env vars or vault only. Violation → Level 4.
2. **P-08.2 — Checkpoint secret review.** Every checkpoint and artifact write is reviewed for secrets by the recording agent and its room Lead; sec-secrets-warden runs pattern review on demand (mechanical scanner retired 2026-07-16 → hierarchical enforcement, Lead → CEO). Flagged content must be cleaned. Bypassing review → Level 4.
3. **P-08.3 — Permission boundaries.** Agent accesses only resources assigned to its room and current PRJ-ID. Cross-room read → Level 2. Cross-project read → Level 3.
4. **P-08.4 — CSO veto.** brd-cso has absolute veto over any artifact/decision/action with security risk. Veto overridden only by brd-ceo + unanimous board. Violation → Level 4.
5. **P-08.5 — Security gate mandatory.** Gate-3 and Gate-5 require sec-lead sign-off. Every gate requires sec-lead notification. Skipping security → Level 3.
6. **P-08.6 — Vulnerability reporting.** Any agent discovering vulnerability reports to sec-lead within 1 turn. Concealment → Level 4.
7. **P-08.7 — Input sanitization.** All external inputs sanitized. Injection-capable data validated. Bypass → Level 3.
8. **P-08.8 — Security audit trail.** All security-relevant actions logged to `hq/brain/amygdala-incidents.md`. Missing log → Level 2.
9. **P-08.9 — Least privilege.** Agents operate with minimum required permissions. Elevated access temporary and logged. Unauthorized elevation → Level 3.
10. **P-08.10 — Dependency scan.** Every new dependency scanned for known vulnerabilities before use. Skipped scan → Level 2.
11. **P-08.11 — Retired (tombstone).** MCP access control retired 2026-07-16 with the brain server → hierarchical enforcement (Lead → CEO). Brain access is direct file access under Protocol 06. Numbering preserved.

### Violation consequence
Level 2 for procedural. Level 3 for boundary violations. Level 4 for secrets, veto violations, or vulnerability concealment.

---

## Protocol 09 — Quality Protocol

### Purpose
Establish minimum quality bar, review requirements, and quality gates. Enforced by qa-lead and brd-cqo.

### Rules
1. **P-09.1 — Quality gate mandatory.** Every artifact passes Gate-5. No pass → no delivery. Violation → Level 3.
2. **P-09.2 — Test requirements.** All code must have passing tests. Coverage minimum: 90% logic, 100% critical paths (unified with Gate-4/Gate-5 bars). Below threshold → blocked.
3. **P-09.3 — Review requirement.** Every checkpoint requires review by ≥1 other agent in same room. Solo checkpoint without review → Level 2.
4. **P-09.4 — Quality metrics.** Every artifact scored on: correctness, completeness, efficiency, traceability, security. Score <7/10 in any dimension → blocked.
5. **P-09.5 — Regression prevention.** All tests pass before AND after change. Regression → artifact rejected, owning room Lead notified.
6. **P-09.6 — Quality escalations.** qa-lead escalates to brd-cqo. brd-cqo escalates to brd-ceo. Escalation cannot be blocked.
7. **P-09.7 — Quality debt log.** Known quality issues logged to `hq/brain/prefrontal-frameworks.md`. Unlogged → Level 2 for qa-lead.
8. **P-09.8 — Minimum bar for handoff.** No cross-room handoff accepts artifacts with quality score <7/10. Accepting low-quality handoff → Level 2 for receiving Lead.
9. **P-09.9 — Quality sampling.** brd-cqo randomly samples 10% of artifacts per gate for independent quality audit. Sampled artifact failing audit → gate reverted.

### Violation consequence
Level 1–2 for procedural. Level 3 for gate skipping.

---

## Protocol 10 — Emergency Protocol

### Purpose
Define response to system crashes, agent failure, data loss, and catastrophic failures.

### Rules
1. **P-10.1 — Emergency classification.**
   - **SEV-1 (Critical):** System crash, data loss, security breach, constitutional violation. Immediate halt. CEO+CSO notified. Response: immediate.
   - **SEV-2 (High):** Agent failure mid-task, pipeline corruption, brain inconsistency. Halt. Lead notified. Response: 3 turns.
   - **SEV-3 (Medium):** Gate failure, test failure, quality breach. Pause. Room notified. Response: 5 turns.
   - **SEV-4 (Low):** Minor violation, handoff failure. Warning. Response: 10 turns.
2. **P-10.2 — Emergency response chain.**
   - Agent detects → brain checkpoint immediately → notify room Lead
   - Lead assesses → classify SEV level → notify escalation path
   - SEV-1: brd-ceo + brd-cso + brd-cqo. Emergency board.
   - SEV-2: brd-ceo + relevant Lead. Task reassignment.
   - SEV-3: brd-cqo + qa-lead. Quality review.
   - SEV-4: Room Lead handles with documentation.
3. **P-10.3 — Brain checkpoint.** Before any recovery action, brain checkpoint created in `hq/brain/hippocampus-sessions.md`. No recovery without checkpoint → Level 3.
4. **P-10.4 — Root cause analysis.** SEV-1/2 require formal RCA within 20 turns. Filed to `hq/brain/amygdala-incidents.md`. Skipped → Level 3 for Lead.
5. **P-10.5 — Recovery procedure.** Restore brain checkpoint → verify data integrity → resume from gtw-intake-reformer → replay lost work. No skipping → Level 3.
6. **P-10.6 — Agent failure.** Checkpoint created → task reassigned → failed agent quarantined → RCA → agent restored or replaced.
7. **P-10.7 — Communication blackout.** During SEV-1, only emergency traffic allowed. Violation → Level 2.
8. **P-10.8 — Post-emergency report.** Every emergency produces postmortem in `hq/brain/org_lessons/LESSONS.md`. Missing → Level 2.
9. **P-10.9 — Emergency drill.** Full emergency drill every 50 agent turns. Missed drill → Level 1 for ops-lead.

### Violation consequence
Level 1–3 depending on handling failure. Level 4 for concealing emergency.

---

## Protocol 11 — Tool Protocol

### Purpose
Define which tools each agent class may use, enforce tool discipline, and prevent unauthorized tool access.

### Rules
1. **P-11.1 — Tool discipline.** Frontmatter tool binding retired 2026-07-16 (tools engine removed by owner decision). Agents inherit the session toolset; every use must stay within the agent's role scope. Out-of-scope tool use → Level 2.
2. **P-11.2 — Role-appropriate access.** Task (delegation) is orchestration — Leads and CEO only. WebSearch/WebFetch belong to research-type work. Destructive commands only within an explicit RCCF scope.
   - **No agent:** Direct user messaging tools, filesystem outside repo, rm -rf
3. **P-11.3 — Tool logging.** Every invocation logged: agent_id, tool, input_summary, output_summary, duration. Missing log → Level 1.
4. **P-11.4 — No tool sharing.** Agent cannot lend tools to another agent. Violation → Level 2.
5. **P-11.5 — Tool timeout.** Tools exceeding max duration killed. Repeated → Level 1.
6. **P-11.6 — Chain execution.** Multi-tool sequences must be intentional with clear evidence for each step. Blind tool chaining → Level 1.
7. **P-11.7 — Tool preflight.** Before destructive tool use (rm, mv, chmod), agent confirms target path. Skip confirmation → Level 2.

### Violation consequence
Level 1–2.

---

## Protocol 12 — Token Economy Protocol

### Purpose
Enforce token efficiency across all agents. Cheapest model for every task.

### Rules
1. **P-12.1 — Cheapest model rule.** Every task uses cheapest model that clears quality bar (defined in `hq/core/nexus/models.yaml`). Deep-tier on routine task → Level 2.
2. **P-12.2 — Verbosity limit.** Essential information only. One sentence where sufficient. Verbose → Level 1.
3. **P-12.3 — Context discipline.** Minimum viable context. No dumping entire files when snippet suffices. Wasteful → Level 1.
4. **P-12.4 — Token audit.** Token burn is audited every 20 turns by the room Lead. Threshold: 2× expected burn. Exceeding → review by brd-cqo.
5. **P-12.5 — Waste log.** All waste incidents logged to `hq/brain/prefrontal-frameworks.md`. Unlogged → Level 1 for room Lead.
6. **P-12.6 — Budget per agent.** Per-agent token budgets are defined in `hq/core/nexus/routing.yaml` (no per-room context allocations exist). Agent exceeding its budget → Lead reports to brd-cqo.

### Violation consequence
Level 1–2.

---

## Protocol 13 — Gate Protocol

### Purpose
Define the 9 lifecycle gates, their owners, exit criteria, and enforcement.

### Rules
1. **P-13.1 — Gate sequence immutable.** 0→1→2→3→4→5→6→7→8. No skipping, no reordering, except brd-ceo-authorized Fast-Track per P-01.8 (collapses Gates 1–3). Violation → Level 3. *(Amendment INT-GTW-024 · 2026-08-24 — v2: within this sequence, S2 crosses Gate-3 on paper and S3 is sealed with the Design-Freeze Review (DFR) signature before any code; map: `nexus/gates.yaml#stage_map`)*
2. **P-13.2 — Gate ownership.** Each gate has designated owner (defined in `hq/core/nexus/gates.yaml`). Only owner may pass artifact through gate.
3. **P-13.3 — Exit criteria.** Defined per gate. Artifacts not meeting criteria cannot pass. Waiving criteria → Level 3.
4. **P-13.4 — Gate evidence.** Gate passage requires: trace to journey map, test results, security review, token report, quality score. Missing → blocked.
5. **P-13.5 — Gate rejection.** Rejected artifact returns to owning room with specific reason. Vague rejection → Level 1 for gate owner.
6. **P-13.6 — Gate log.** All passages logged to `hq/brain/cortex-decisions.md`. Missing → Level 1 for gate owner.
7. **P-13.7 — Gate rollback.** If artifact fails post-gate verification, gate passage is rolled back and owning room notified. Failure to rollback → Level 2.

### Violation consequence
Level 1–3.

---

## Protocol 14 — Memory Isolation Protocol

### Purpose
Enforce strict memory boundaries between projects. Prevent cross-project data leakage, context poisoning, and authorization bypass.

### Rules
1. **P-14.1 — Project isolation.** Every PRJ-ID has isolated brain storage. No project reads another project's brain files. Violation → Level 3.
2. **P-14.2 — Context boundary.** Agent context for PRJ-X contains ONLY: PRJ-X CONTEXT.md, DECISIONS.md, HANDOFFS.md, LESSONS.md (Law 7). No other project files in context. Violation → Level 2.
3. **P-14.3 — Ticket scope.** Tickets reference exactly one PRJ-ID. Cross-project tickets → Level 3. Tckt with ambiguous PRJ-ID → rejected by gtw-intake-reformer.
4. **P-14.4 — Brain write isolation.** Every brain write carries the PRJ-ID prefix; the writing agent's room Lead verifies it at checkpoint review (mechanical writer retired 2026-07-16 → hierarchical enforcement). Write without PRJ-ID prefix → Level 2.
5. **P-14.5 — Lesson isolation.** Lessons learned in PRJ-X tagged with `[PRJ-X]`. Cross-project lesson injection → Level 2.
6. **P-14.6 — Isolation audit.** knw-lead audits isolation monthly (every 40 turns). Breach found → Level 3 for responsible agent.

### Violation consequence
Level 1–3. Cross-project data leak → Level 3.

---

## Protocol 15 — Retired (tombstone)

### Tombstone
The MCP/brain-server protocol was retired 2026-07-16 with the tools engine (owner decision) → hierarchical enforcement (Lead → CEO). No brain server exists; brain access is direct file access under the structure of `hq/brain/brain-index.md`, governed by Protocol 06 (Memory) and Protocol 14 (Memory Isolation). One rule survives, relocated:

1. **P-15.9 — Brain write quorum (surviving rule).** Destructive brain writes (delete, overwrite organics) require 2-agent quorum (writer + room Lead). Single-agent destructive write → Level 3.

Numbering preserved; no renumbering.

---

## Protocol 16 — Direct-on-Project Protocol

### Purpose
Enforce Binding Law 10. All work on any hosted project happens directly on the project's main working tree. No isolated copies, no long-lived isolated branches, no git worktrees — they diverge, get forgotten, and become unmergeable.

### Rules
1. **P-16.1 — Direct on main tree.** Every agent works directly on the project's canonical main working tree (e.g. `~/Desktop/SOFI/projects/<name>`). No shadow copy, no parallel clone, no isolated redesign tree. Violation → Level 2.
2. **P-16.2 — Worktrees forbidden.** No agent creates or uses `.opencode/worktrees/`, any `git worktree`, or any long-lived isolated branch for any project. Creating a worktree → Level 2: work cancelled and relocated to the main tree.
3. **P-16.3 — Documented cause (binding precedent).** Worktrees produce forgotten merges and unrepairable divergence. Binding precedent: a past incident left hundreds of files diverged from production, with the worktree older than a production tree that had already taken security-critical migrations — safe merge became impossible and the isolated design work was lost entirely.
4. **P-16.4 — Found worktree = report, never blind-merge.** An agent that finds an existing worktree or isolated branch MUST stop, notify its room Lead, and never blind-merge. Analysis first is mandatory: which side is newer vs older (migration count, security-critical migrations, file divergence). Blind merge → Level 3.
5. **P-16.5 — Compelling-cause temporary branch only.** A temporary branch is permitted only for a compelling technical reason. It MUST be merged and deleted before the task closes. Leaving unmerged work → Level 2. Repeat → Level 3.
6. **P-16.6 — No task closure with unmerged work.** No task, gate, or session closes while any project holds uncommitted or unmerged isolated work. The owning room Lead verifies at closure. Closing over unmerged work → Level 3.

### Violation consequence
Level 2 for creating a worktree/isolated copy or leaving unmerged work. Level 3 for blind merge, repeat unmerged-work offense, or closing a task over unmerged work.

---

## Protocol 17 — Context Minimization Protocol

### Purpose
Protect the Token Economy (Teaching IV) from silent inflation: every agent starts with the minimum viable context needed to complete its task and expands only upon proven need — no one hauls the full constitution around just to know the time. External evidence: context engineering (compaction / sub-agent contexts) is a pillar of multi-agent system efficiency (`hq/training/internet_knowledge/agents-anthropic-multiagent.md`).

### Rules
1. **Progressive loading:** the task agent reads only its own task document plus its room's law; the Lead appends cross-room context at handoff time.
2. **No pasting whole documents** into a task prompt when a summary or line-level reference suffices (quote the clause + file:line).
3. **Justified expansion only:** adding context requires a documented reason recorded in the ticket (discovered conflict, gate, escalation).
4. **Thread hygiene:** once usage passes 60% of the lane budget ceiling (Protocol 12 + gtw-budget-warden ceilings), the Lead compacts context before any new invocation.

### Violation consequence
Unjustified context waste = L1 (immediate correction); repeat = L2 with the agent's prompt reviewed via the `sofi-agent-eval` skill.

---

## Protocol 18 — Visual Research Protocol

### Purpose
Make visual research methodical, documented, and integrated: agents design from proven real-world
patterns gathered under protocol — never from random browsing, and never by copying competitors.

### Rules

1. **P-18.1 — Research before design:** `dsn-ui-designer` starts no new screen without (a) a pattern
   report from `res-visual-pattern-scout` (3–5 examples via the `mobbin-scraper` skill), (b) a
   competitive analysis from `dsn-competitive-ui-analyst`, and (c) RTL sign-off from
   `dsn-arabic-ux-specialist`. Violation = L2.
2. **P-18.2 — Mandatory documentation:** every extracted pattern is filed under
   `projects/<slug>/brain/visual-patterns/` (one file per pattern: onboarding-flow · checkout-flow ·
   dashboard-layout · navigation-patterns · rtl/ · competitive/) containing: screenshot URLs,
   user-flow description, elements breakdown, why-it-works rationale, adaptation notes. Violation = L1.
3. **P-18.3 — No verbatim copying:** extracting the principle is mandatory, copying the shape is
   forbidden; every adoption is adapted to the SOFI design system with a distinct SOFI touch.
   Violation = L3 (intellectual theft).
4. **P-18.4 — Design-system integration:** every approved pattern lands in the design system
   (tokens/components/patterns) via `dsn-design-system-gen`, and `hq/core/standards/uiux-standard.md`
   is updated. Violation = L2.
5. **P-18.5 — Periodic refresh:** `res-visual-pattern-scout` reviews the binding platforms every 40
   agent turns, detects new trends, and reports to `dsn-lead` and `brd-cpo`. Violation = L1.

Binding platform list: `hq/core/standards/uiux-standard.md §Visual Inspiration Sources`.

---

## Protocol Priority

In case of conflict between protocols, resolution follows:

```
Pipeline (01) > Security (08) > Emergency (10) > Handoff (02) > Direct-on-Project (16) > Context Minimization (17) > Quality (09) > Gate (13) > Evidence (03) > Memory Isolation (14) > Escalation (04) > Conflict (05) > Memory (06) > Communication (07) > Tool (11) > Token Economy (12)
```

*(Protocol 15 retired 2026-07-16 — removed from the priority chain.)*

A lower-priority protocol cannot override a higher-priority protocol. A protocol that contradicts the Constitution is void.

---

*All protocols enforced through the hierarchy (Lead → CEO). Violations logged to brain.*

---

## | Protocols & Laws Enforcement Arsenal — The Free Armory (2026-08-23 · SOFI-HQ-INT-0003)

> Every tool listed below is 100% free with no paid keys, activated through `opencode.json` or `.opencode/skills/`. Goal: upgrade enforcement from textual discipline to machine-backed discipline.

### a) Mapping of the 13 Laws
| Law | Machine Backing |
|---|---|
| 1 Gateway / Proportional Flow | `str-gate0-classify` + Sequential Thinking MCP for structured classification |
| 2 Room Isolation | `sofi-handoff` with a strict JSON schema |
| 3 Hierarchical Handoff | The ticket itself |
| 4 Evidence | Playwright MCP (P-03.4 screenshot) · Chrome DevTools (console evidence) · OrangePro (coverage) · DataNexus (CVEs) |
| 5 RCCF | Intake gateway (procedural) + `writing-plans` inside the work order |
| 6 Advisory Board | Sequential Thinking for trade-off weighing · DeepWiki for OSS precedent |
| 7 Memory Binding | `knw-brain-write` — sole-source brain files (honoring P-15) |
| 8 Quality Before Speed | `qa-test-plan` + the documented "test until it turns green" loop |
| 9 Chain of Responsibility | The AMYGDALA log (existing) |
| 10 Direct-on-Project | CodeSentinel (drift detection, when enabled) + completion of the INT-0003 branch unification |
| 11 Simplified-Arabic Communication | Stylistic discipline (procedural) |

### b) Official Replacement Policy — no paid services, no keys
`Tavily → SearXNG+Crawl4AI` · `Firecrawl → Crawl4AI` · `Exa → local search/SearXNG` · `Browserbase → local Playwright` · `SerperDev → SearXNG` · `SMS providers → self-hosted textbee`
- Practical execution: the `res-web-scrape` skill (room 02) — and the list is part of the skills index.
- Rejected as phantom names with no documented existence: HiveFence · fastCRW · Unsearch · capability-evolver · prompt-guard-as-MCP — the "verify before believing" lesson is logged in CORTEX.

### c) Deferred Enablement List (passes sec-mcp-vetting first, then activates when needed)
DataNexus (CVEs — usable keyless by design) · OrangePro (test generation) · CodeSentinel (code health) · textbee (SEV-1 alerts) · AIOProductOS (local demo videos) · PageMap (97% scrape compaction) · GitHub MCP (free access token only).

*Appendix added as a dated annex — it amends not a single character of the original protocol texts.*


---

## | Amendment dated 2026-08-23 — "Design Before Code" Doctrine as Binding Operating Rules (INT-0004)

> By owner order: the doctrine "idea ← research ← strategy ← planning ← approved design ← implemented code" is generalized to every agent, completing P-01 and P-13 and the lane laws `design_before_code` and `backend_complete_before_ui` — contradicting none of them.

- **D-1 Definition of prematurely forbidden "code":** any executable file, UI component, or runnable migration. **Outside the ban:** PRD/ADR documents · ERD diagrams · OpenAPI specifications · design tokens and mockups · test scripts that exercise the paper contract itself.
- **D-2 Start prohibition:** no agent opens an implementation file for a feature before these exist: pinned PRD (S1) + ERD and frozen contract (S2) + DFR signature (S3). For partial tasks: approval of the prior stages covering that sub-task's scope alone suffices.
- **D-3 Duty of courteous refusal:** a request for code without a prior approved design is itself a violating request; the agent must stop and reroute through its room Lead to the gateway (P-01.8) — executing anyway = L2 on both the executor and the requester.
- **D-4 Deviation = redo:** matching the delivered output verbatim to the approved documents is the definition of "complete"; any executive improvisation that flips a design decision returns the piece to the owning stage and reopens its passage gate (P-13.7).
- **D-5 Doctrinal teaching block:** the standard block (5 points) is mandatory at the tail of each of the 106 agent files — and is a condition for accrediting any future new agent (integrates with AGENT-PROMPT-TEMPLATE §7). Its absence in any agent = L1 on knw-lead, keeper of templates.
- **Penalty:** D-3/D-4 at the level stated above; repetition escalates according to the violation table in AGENTS.md.
