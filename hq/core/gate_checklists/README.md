# `hq/core/gate_checklists/` — Per-Gate Criteria

> The 9 gates (G0..G8) + DFR (Design-Freeze Review) each have a checklist file in this directory.
> A gate's checklist enumerates the **binding criteria** that must be met before the next stage can
> begin. The checklists are referenced by `nexus/gates.yaml` and `nexus/pipeline.yaml`.

Owned by `qa-lead` (10-quality) + `arc-lead` (04-architecture) + the relevant gate owner.

---

## The 9 gates + DFR (10 files)

| Gate | Owner | Triggers | What it checks |
|------|-------|---------|----------------|
| **G0** | `14-gateway` + `01-strategy` | every intake | ambiguity ≤ 20% · scope classification · fast-track eligibility |
| **G1** | `02-research` | S1 → S2 | research dossier signed (JTBD + personas + pain points) |
| **G2** | `01-strategy` | S1 → S2 | PRD approved · MVP scope locked |
| **G3** | `04-architecture` | S2 → S3 | ERD + schema-contract (paper) + OpenAPI frozen |
| **DFR** | `03-design` + `09-security` + `10-quality` | S3 → S4 | **Design-Freeze Review signed by sec-lead + qa-lead** — zero code before this |
| **G4** | `05-backend` | S4 → S5 | live API + migrations + security-checked |
| **G4b** | `06-frontend` + `07-mobile` | S5 → S6 | both interfaces on frozen contract |
| **G5** | `10-quality` | S6 end | test plan + execution + coverage + design audit (PASS/REJECT) |
| **G6** | `11-devops` | G5 → S7 | deploy + rollback plan + health check |
| **G7** | `12-observability` | G6 → S8 | tracing + SLOs + alerts live |
| **G8** | `13-knowledge` | S6 final | documentation in CORTEX + skills indexed |

---

## The 4 owner approval points (per `INT-EVOL-2`)

1. **Scope & plan** (after S1) — what we build, what we don't, timeline, technology
2. **Look & design** (after S3) — shapes, colors, fonts as images, no jargon
3. **Technical plan** (after S2/S3) — how it works inside, explained by metaphor
4. **DFR signature + production quality** (G5) — design freeze + test report

Rejecting at any point = return to the owning stage. Writing code before all 4 points approved is
forbidden (Design-First doctrine INT-0004).

---

## The K1–K17 thresholds (per `standards/kpi-thresholds.md`)

**Hard rules (block Gate-8 if violated):**
- **K6** — Test coverage ≥ 85% on critical paths
- **K11** — Zero P0 bugs at release
- **K14** — No task may be rejected twice for the same reason (Law 14 freeze)
- **K16** — Ambiguity score ≤ 20% for any request (Law 16)
- **K17** — Every `file:line` must resolve to a real file (Law 4)

Other K1–K17 are advisory and feed into Gate-5's verdict.

---

## The P-13 Gate Protocol

> Source: `protocols.md:P-13`.

Gate sequence is **immutable**: `0 → 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8`. No skipping, no reordering.
Fast-Track may collapse gates 1-3 with `brd-ceo` authorization (P-01.8).

---

## The gate checklist format

```markdown
# Gate X — <name>
- **Owner:** <room> (lead: <agent>)
- **Stage:** S1..S6
- **Entry:** what triggers the gate
- **Exit:** what must be true to pass

## Criteria (per `kpi-thresholds.md`)
- [ ] criterion 1 (with file:line source)
- [ ] criterion 2
- [ ] ...

## Evidence Required
- file:line per claim
- exit code per command
- log/screenshot per result

## Approval
- Signed by: <owner>
- Co-signed by: <co-signer>
- Date: YYYY-MM-DD
```

---

## How to update a gate checklist

1. Edit the relevant `gate-X.md` (or `dfr.md`)
2. Update `nexus/gates.yaml` to reference the new criteria
3. Bump `standards/kpi-thresholds.md` if K-rules change
4. Commit atomically — pre-commit enforces all 4 guards
5. Record ADR in CORTEX if the change affects gate semantics

---

## See also

- [`../README.md`](../README.md) — `hq/core/` parent
- [`../nexus/gates.yaml`](../nexus/gates.yaml) — gates registry
- [`../standards/kpi-thresholds.md`](../standards/kpi-thresholds.md) — K1–K17
- [`../protocols.md:P-13`](../protocols.md) — Gate Protocol
- [Top-level README](../../../README.md)
- [`AGENTS.md`](../../../AGENTS.md) — Law 1 + 11
