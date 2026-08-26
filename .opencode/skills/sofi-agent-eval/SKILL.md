---
name: sofi-agent-eval
description: "Periodic agent evaluation on a weighted five-dimension rubric"
mode: subagent
---
# Skill: sofi-agent-eval — Periodic Agent Quality Evaluation

```yaml
name: sofi-agent-eval
version: 1.0
room: 13-knowledge + 00-boardroom
authority: OWNER-DIRECTIVE 2026-08-24 (comprehensive self-development) · built on Anthropic Engineering principles (evals + LLM-as-judge)
triggers_ar: ["evaluate agent", "agent review", "agent quality audit", "periodic evaluation", "rubric for an agent"]
triggers_en: ["evaluate agent", "agent quality review", "agent rubric", "periodic eval"]
```

## 🎯 Purpose
Measure **the quality of the working agents themselves** (not just the products) in a systematic, provable way — the P0 gap exposed by the gap analysis: we measure project outputs yet never measure the agents' own performance.

## ⬛ The Binding Standard — Five-Dimension Rubric (every agent, any room)

| Dimension | Governing question | Weight |
|-------|---------------|-------|
| **1. Constitutional compliance** | Did the agent honor the 13 laws and the hierarchy (no skips, no direct delivery)? | 30% |
| **2. Evidence quality** | Does every delivery carry file:line + exit code + live proof? (Law 4 enforced strictly) | 25% |
| **3. Technical accuracy** | Were its claims actually verified? (fingerprints, tests, independent checks) | 20% |
| **4. Token economy** | Was the task completed within its track's budget without context waste? (Fourth Education) | 15% |
| **5. Simplified-Arabic communication** | Addressing the user without unexplained jargon? (Law 11) | 10% |

**Score:** 5 dimensions × rating 0–2 (0=fail, 1=partial, 2=excellent) → weighted total out of 10.
**Thresholds:** 9–10 = excellent (recorded in CORTEX) · 7–8.9 = acceptable (improvement note) · <7 = retraining/prompt adjustment (escalated by the room lead).

## 🔄 Periodic Execution Mechanism
1. **Monthly:** each room lead evaluates their agents on the last 3 documented deliveries (using HANDOFFS records as evidence).
2. **Quarterly:** room 13 (`knw-reflector` + this skill) re-evaluates a cross-room sample (10% of agents) and reports to brd-ceo.
3. **After every L2+ incident:** immediate evaluation of the involved agent before closing the incident.
4. **The evaluator never evaluates themselves** — leads evaluate their agents, room 13 evaluates the leads, and the Board audits the methodology annually.

## 📊 Eval Output (documentation-mandated)
```
### Agent Eval Record — <agent-name> — YYYY-MM
- sample: <last N deliveries / TKT identifiers>
- scores: {constitution: X/6, evidence: Y/5, accuracy: Z/4, tokens: W/3, communication: V/2}
- weighted: N.N/10 → EXCELLENT|ACCEPT|RETRAIN
- evidence: <file:line of the evaluated deliveries>
- action: <none | note | specific prompt adjustment>
```
Recorded in `hq/brain/org_lessons/patterns/` or escalated according to the score.

## 🔗 Alignment with industry patterns
This skill applies principles from «Building Effective Agents» and «Multi-Agent Research System» from Anthropic Engineering (harvested in `hq/training/internet_knowledge/agents-anthropic-*.md`): evaluation against declared criteria (rubrics), periodic sampling, and separating evaluator from evaluated — matching the Evaluator–Optimizer patterns already applied intuitively at the DFR/G5 gates.
