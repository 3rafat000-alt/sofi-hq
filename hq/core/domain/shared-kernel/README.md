# `hq/core/domain/shared-kernel/` — The Shared Kernel

> The **shared kernel** is the only place in the domain layer where shared concepts live. Per
> Law 2, the shared kernel is the **lingua franca** of the organization — every bounded
> context depends on it. Modifying the shared kernel requires `brd-ceo` approval.

Per DDD convention, the shared kernel contains concepts that are too fundamental to live in any
single bounded context. The "user" concept, the "evidence rule", the "API envelope" — these
belong to the shared kernel.

---

## The 4 shared-kernel concepts

| Concept | File | Purpose |
|---------|------|---------|
| **Glossary** | `glossary.md` | The shared terms (DDD ubiquitous language) — every term used by 2+ contexts |
| **Identity** | `identity.md` | The shared identity types (User · Role · Permission · Tenant) |
| **Envelope** | `envelope.md` | The shared envelope (API response wrapper, per `standards/api-envelope.md`) |
| **Evidence rule** | `evidence-rule.md` | The shared evidence rule (Law 4 + `sofi-evidence` skill) |

---

## The glossary (`glossary.md`)

> The DDD ubiquitous language. Every term used by 2+ contexts is defined here **once**.

Examples:
- **RCCF** (Request → Clarify → Confirm → Fullfil) — work order
- **DFR** (Design-Freeze Review) — design gate co-signed by sec-lead + qa-lead
- **Bounded context** — a DDD boundary owned by a single room
- **Capsule** — the per-agent directory `domain/rooms/<room>/agents/<name>/`
- **Lane** — Fast / Standard / Fateful
- **CORTEX** / **HIPPOCAMPUS** / **AMYGDALA** — the 3 memory stores
- **T0..T4** — the 5 priority tiers
- **G0..G8 + DFR** — the 10 gates
- **CONDITION-FOLLOW-UP** — DEC-R3.4 binding rule for runtime artifacts
- **PENDING-PHASE-B** — temporary stopgap for the constitutional guards

The full glossary is in `glossary.md`.

---

## The identity types (`identity.md`)

> The shared identity types. Every bounded context that deals with "who is the user" must
> use these types (not its own).

- **User** — the human person (with KYC, Arabic name, contact)
- **Role** — the RBAC role (Admin · User · Guest · etc.)
- **Permission** — the granular authorization (`resource.action` pattern)
- **Tenant** — the multi-tenant boundary (org · project · workspace)

These are **owned by the shared kernel** (not by any single room). Per Law 2, the shared kernel
is the only place where shared concepts are defined.

---

## The envelope (`envelope.md`)

> The shared envelope — every API response wraps in this format. Per `standards/api-envelope.md`.

```json
{
  "data": <payload>,
  "meta": {
    "request_id": "<uuid>",
    "timestamp": "<iso8601>",
    "version": "1.0"
  },
  "errors": [<error objects>],
  "links": {
    "self": "<url>",
    "next": "<url>" | null,
    "prev": "<url>" | null
  }
}
```

Every API in SOFI HQ (Laravel · React Query · Flutter) uses this envelope. See
`standards/api-envelope.md` for the full spec.

---

## The evidence rule (`evidence-rule.md`)

> The shared evidence rule — every claim has a `file:line` proof. Per Law 4 + the
> `sofi-evidence` skill.

```yaml
# Every claim in a delivery
- file: path/to/file
- line: 42
- exit_code: 0  # for command outputs
- log_or_screenshot: <path>  # optional, for visual evidence
- source_url: <url>  # optional, for external claims
- confidence: high | medium | low
```

The `evidence_guard` (Law 4) automatically verifies every `file:line` citation in the codebase.
A broken citation = the commit is blocked.

---

## How to add a shared-kernel concept

1. Add the concept to the appropriate file (`glossary.md` / `identity.md` / `envelope.md` / `evidence-rule.md`)
2. If it's a new concept, add a new file (e.g. `audit-trail.md`) and reference it from
   `README.md` above
3. Commit atomically — pre-commit enforces all 4 guards
4. Record ADR in CORTEX (shared kernel changes are constitutional)
5. Notify all room leads (per `communication-matrix.md`)

**Forbidden:** adding a concept to the shared kernel without `brd-ceo` approval.

---

## See also

- [`../README.md`](../README.md) — `hq/core/domain/` parent
- [`../context-map.yaml`](../context-map.yaml) — the interface map
- [`../../standards/api-envelope.md`](../../standards/api-envelope.md) — envelope standard
- [`../../standards/ddd-capsule.md`](../../standards/ddd-capsule.md) — DDD capsule standard
- [Top-level README](../../../README.md)
- [`AGENTS.md`](../../../AGENTS.md) — Law 2
