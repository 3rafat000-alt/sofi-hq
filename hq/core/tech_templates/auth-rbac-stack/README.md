# auth-rbac-stack — The Unified Authentication & RBAC Template

A contract-first template for authentication and RBAC across SOFI's three stacks.

| Component | Status | Entry Point |
|---|---|---|
| `backend-laravel/` | **the contract's reference source** | `docs/openapi-auth.md` — the five routes + the v1 envelope |
| `frontend-react/` | ⛔ **legacy — retired by decision R2** (2026-08-23) | `LEGACY-NOTE.md` — new work is Flutter/Dart |
| `mobile-flutter/` | dependency snippet only | `PUBSPEC-SNIPPET.md` |

**Consumption rule:** every stack consumes the OpenAPI contract verbatim — no improvisation. Framework tooling fills its own standard files (no pre-made package.json/pubspec).
