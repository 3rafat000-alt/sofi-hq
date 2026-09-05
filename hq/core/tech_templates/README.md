# `hq/core/tech_templates/` — Technology-Specific Templates

> Templates for technology-specific artifacts (Laravel Eloquent RBAC stack, DDD capsule protocol,
> etc.). These are the **technology-binding** layer of the standards — they take an abstract
> standard (e.g. `identity-handbook.md`) and ground it in a specific technology (e.g. Laravel).

Owned by `knw-doc-writer` (13-knowledge) + the relevant technology room leads.

---

## Files

| File | Technology | Purpose |
|------|------------|---------|
| `auth-rbac-stack/` | **Laravel 11+** | The auth + RBAC (Role-Based Access Control) stack — Spatie/laravel-permission + Sanctum + policies |
| `ddd-capsule-protocol.md` | **DDD** | The DDD capsule template — what every bounded context must include (entity / value object / aggregate / repository contract / event) |

---

## The auth-rbac-stack (`auth-rbac-stack/`)

> Source: `auth-rbac-stack/` (Laravel-specific)

The full authentication + authorization stack for Laravel 11+:

- **Auth driver:** Sanctum (SPA + token) or Passport (OAuth2) — depending on app profile
- **RBAC engine:** `spatie/laravel-permission` (roles + permissions)
- **Authorization:** Policies per Model + Gates per Role
- **Multi-factor:** TOTP via `pragmarx/google2fa`
- **Sessions:** Redis-backed (`config/session.php` → `connection: 'redis'`)
- **API rate limit:** `throttle:api` middleware on all auth + sensitive routes

**Stack-lock compliance:** this stack is mandatory for all Laravel projects in SOFI HQ
(per `deploy-standard.md` + `stacks-tech.md`).

---

## The ddd-capsule-protocol (`ddd-capsule-protocol.md`)

> Source: `ddd-capsule-protocol.md` — extends `standards/ddd-capsule.md` with a concrete template.

Every bounded context in SOFI HQ must include:

```php
app/Domain/<ContextName>/
├── Entities/             # Aggregate roots + their state
├── ValueObjects/         # Immutable types (Money, EmailAddress, etc.)
├── Aggregates/           # Aggregate root + its entities
├── Repositories/         # Interfaces (contracts) only — implementations in Infrastructure
└── Events/               # Domain events (DomainEvent trait)
```

Plus: `app/Application/<ContextName>/{DTOs,Services,Actions}` and
`app/Infrastructure/<ContextName>/{Database,Repositories,Api,Queue}`.

**DO/DON'T table:** see `standards/ddd-capsule.md` for the binding rules.

---

## How to add a new technology template

1. Create the template file/directory under this directory
2. Reference the relevant standard (in `standards/`)
3. Add a row to the table above
4. Update `standards/stacks-tech.md` to reference the template
5. Commit atomically — pre-commit enforces all 4 guards
6. Record ADR in CORTEX if the template changes constitutional behavior

**Forbidden:** adding a new technology that's not in Stack Lock R3 (React / Laravel / Flutter
exclusively). The exception is a `brd-ceo` decision (owner order).

---

## See also

- [`../README.md`](../README.md) — `hq/core/` parent
- [`../standards/stacks-tech.md`](../standards/stacks-tech.md) — R2 legacy stacks
- [`../standards/ddd-capsule.md`](../standards/ddd-capsule.md) — DDD capsule standard
- [`../standards/identity-handbook.md`](../standards/identity-handbook.md) — auth standard
- [Top-level README](../../../README.md)
- [`AGENTS.md`](../../../AGENTS.md) — Law 15 (License)
