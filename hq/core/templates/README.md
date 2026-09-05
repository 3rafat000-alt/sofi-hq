# `hq/core/templates/` — Operational Templates

> Templates for **operational artifacts** (not tech-specific). Currently houses the unified
> report template. The tech-specific templates live in `tech_templates/`.

Owned by `knw-doc-writer` (13-knowledge).

---

## Files

| File | Purpose | Used by |
|------|---------|---------|
| `report-template.md` | The unified 5-section report template (created in Audit-ALL) | every agent reporting |

---

## The unified report template (Audit-ALL standard)

> Source: `report-template.md` — every agent's delivery follows this 5-section structure.

```markdown
# 📋 Report — <ticket-id> — <date>
## FILE: <output-path>

### Executive Summary
<one-line — the real goal>

### Full Context
<all context gathered — sources file:line>

### Specific Request
<what was asked — zero ambiguity>

### Constraints & Considerations
<constraints — boundaries — priorities — risks — deadlines — resources>

### Expected Deliverables
<measurable outputs>

### Gate Check (if delivery)
PASS/FAIL per criterion with reason

### Budget (if delivery)
WITHIN/OVER with numbers

### Evidence (if delivery)
- Change: path/file:line — what changed
- Command: <cmd> → exit 0 — <last lines>
- Test: <suite> → N passed / M failed
- Source: <url> → "<extract>" (confidence: high)

### Handoff (if delivery)
- ticket_id
- from_agent → to_agent
- artifacts
- evidence_digest
- context_refs
- status
- note (≤280 chars)
```

This is the **Audit-ALL standard** for reporting. Any report that doesn't follow this structure
fails the constitutional review.

---

## Other templates (planned)

| Template | Purpose | Status |
|----------|---------|--------|
| `agent-prompt-template.md` | (lives in `tech_templates/`) | ✅ done |
| `mcp-agent-annex.md` | (lives in `tech_templates/`) | ✅ done |
| `rccf-template.md` | The standard RCCF work-order template | 📋 planned |
| `incident-postmortem.md` | The standard AMYGDALA postmortem template | 📋 planned |
| `adr-template.md` | The standard ADR template for CORTEX | 📋 planned |
| `meeting-minutes-template.md` | The standard board meeting minutes template | 📋 planned |

---

## How to add a new template

1. Create the `.md` file with the standard format (purpose + structure + usage)
2. Add a row to the table above (or to the "planned" list)
3. Reference from at least one protocol or standard
4. Commit atomically — pre-commit enforces all 4 guards
5. Record ADR in CORTEX if the new template changes constitutional behavior

---

## See also

- [`../README.md`](../README.md) — `hq/core/` parent
- [`../tech_templates/README.md`](../tech_templates/README.md) — tech-specific templates
- [Top-level README](../../../README.md)
- [`AGENTS.md`](../../../AGENTS.md) — Law 4
