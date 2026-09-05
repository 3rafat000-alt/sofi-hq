# `hq/engine/brain/` — Live Engine CORTEX Mirror

> A **mirror** of `hq/brain/` (CORTEX + HIPPOCAMPUS + AMYGDALA) for the **live engine**. This
> is the operational brain — the org memory at `hq/brain/` is the **source of truth**, this is the
> runtime cache.

Per Law 7, the two memories are **strictly separate**. The engine brain is read-mostly at runtime
(updated on a schedule, not on every commit). The org brain is the constitutional log.

---

## Files

| File | Mirror of | Purpose | Update frequency |
|------|-----------|---------|------------------|
| `CONTEXT.md` | `hq/brain/cortex-decisions.md` (summary) | What the engine needs to know about the current state | on-merge |
| `DECISIONS.md` | `hq/brain/cortex-decisions.md` (selected ADRs) | The ADRs that affect the engine | on-merge |
| `HANDOFFS.md` | `hq/brain/hippocampus-sessions.md` (selected SES) | The sessions that involve the engine | on-incident-close |
| `LESSONS.md` | `hq/brain/amygdala-incidents.md` (selected) | The lessons that the engine must learn | on-incident-close |
| `verified/` | `hq/brain/evidence/` (snapshot) | The verified artifacts (e.g. signed ADRs) | on-merge |

---

## The flow (per Law 7)

```
happen in org memory (hq/brain/)           mirror in engine (hq/engine/brain/)
─────────────────────────────────           ─────────────────────────────────────
ADR committed to CORTEX          ──mirror──> CONTEXT.md + DECISIONS.md updated
SES entry to HIPPOCAMPUS         ──mirror──> HANDOFFS.md updated (selected)
Incident logged in AMYGDALA      ──mirror──> LESSONS.md updated
Evidence file in evidence/       ──mirror──> verified/ updated
```

The mirror is **one-way** (org → engine). The engine never writes back to the org memory (that
requires `brd-ceo` promotion).

---

## The verification protocol

Every file in `verified/` must be:
- `file:line`-cited (Law 4)
- A snapshot of the org source (not a copy with modifications)
- Updated only via `knw-lead` or `ops-release-manager`

**Forbidden:**
- Direct edits to the engine brain (must update org first, then mirror)
- Modifications to verified artifacts (must re-mirror from org source)
- Cross-linking to other engines (each engine has its own brain)

---

## The CONDITION-FOLLOW-UP (DEC-R3.4)

> The engine brain files are **never** truncated in delivery handoffs. They are part of the
> operational canon. They live in git and are versioned.

---

## How to update the engine brain

1. Update the **org source** (`hq/brain/cortex-decisions.md` or `hippocampus-sessions.md` or `amygdala-incidents.md`)
2. Wait for the commit to land (pre-commit enforces 4 guards)
3. Update the **engine mirror** (`hq/engine/brain/CONTEXT.md` etc.) — only the relevant section
4. If the change involves a verification artifact, add to `verified/`
5. Commit atomically — pre-commit enforces all 4 guards

**Forbidden:** updating the engine brain without first updating the org source. This creates
divergence between the two and violates Law 7.

---

## See also

- [`../README.md`](../README.md) — `hq/engine/` parent
- [`../../brain/README.md`](../../brain/README.md) — org memory (sister — source of truth)
- [Top-level README](../../../README.md)
- [`AGENTS.md`](../../../AGENTS.md) — Law 7
