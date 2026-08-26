---
name: sofi-evidence
description: >-
  Builds the official SOFI evidence block (Law 4 / Protocol 03) before any delivery or gate. Triggers — "build evidence", "evidence package", "prove this change", "before handoff", "gate evidence", "prepare the evidence", "evidence block", "before delivery", "document the proof". Invoked by any agent in any room before handing output to its lead.
---

# sofi-evidence — Evidence Block Builder

> **Law 4:** no evidence = delivery rejected (L2). Every output independently verifiable, never LLM claims.

## 🎯 When to invoke (When)
- Before any delivery to a room lead.
- Before crossing any gate — a gate demands an evidence package.
- When a delivery was rejected for missing evidence (correction).

**Do not invoke** to fabricate evidence or LLM summaries — fabricated proof = L3.

## 📥 Inputs
- Agent type (Engineer / Designer / Researcher / Architect / Security / QA / DevOps).
- Actual execution results (never guesses): command outputs, files, screenshots.

## 🔧 Steps
1. Identify your agent type → pick the matching evidence checklist (below).
2. Collect every element from its real source (run the command, open the file, take the screenshot).
3. Format every element per the binding format:
   - Code: `path/to/file:123` for every change (P-03.2). No vague references.
   - Commands: exit code + last 20 lines of output.
   - Research: source URL + verified extract (no generated summary).
   - Design: before/after screenshot in `artifacts/`.
   - Testing: pass/fail for every executed suite.
4. Verify every element is **independently reproducible** (P-03.6).

## 📤 Output + evidence
An evidence block ready for delivery/gates:

```
### Evidence — <agent_id> — <timestamp>
- Change: path/file:line — <what changed>
- Command: <cmd> → exit 0 — <last lines>
- Test: <suite> → 12 passed / 0 failed
- Source: <url> → "<extract>" (confidence: high)
- Screenshot: artifacts/<name>.png (before/after)
```

## Per-agent checklists (P-03.8)
| Agent | Required elements |
|--------|------------------|
| Engineer | code diff `file:line` + test output + build exit code |
| Designer | mockup before/after + design token changes + a11y audit |
| Researcher | source URL + search query + extracted fact + confidence |
| Architect | architecture diagram + ADR + schema migration plan |
| Security | threat model + vulnerability scan + pentest report |
| QA | test plan + execution results + coverage + regression status |
| DevOps | deployment log + health check + rollback plan |

## 🔗 Handoff
The evidence block is part of delivery via `sofi-handoff` → room lead (Law 3). Never hand evidence to the user directly.

## ⛔ Constraints
- Evidence generated without execution is forbidden (P-03.3). Every element from real execution/observation.
- Unverifiable evidence = rejected. Fabricated = L3.
- Log the evidence in `hq/brain/hippocampus-sessions.md` (P-03.5).
