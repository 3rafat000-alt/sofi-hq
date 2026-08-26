---
name: sofi-project-spawn
description: >-
  SOFI's automated project-spawning engine — turns a new application request into a complete isolated
  project tree under projects/ with template stack scaffolding and project-memory initialization. Triggers — "spawn a new project", "create app X",
  "generate a project", "start a platform", "new client project", "initialize project",
  "new standalone application".
---

# sofi-project-spawn — The Project Spawning Engine

> **Purpose:** converting a standalone application request («build a real-estate platform named Aqari») into an isolated, build-ready project tree within seconds — no manual copying, no forgotten project memory.

## 🎯 When to invoke (When)
- An owner/user request for a new standalone application unrelated to the SOFI framework itself.
- After the gateway classifies the lane (usually standard — creating reversible structure).
- **Do not invoke** for work inside hq/ or changes to the framework itself.

## 📥 Inputs — mandatory before execution
| Field | Example | Note |
|-------|------|--------|
| `project_name` | `aqari` | Latin kebab-case only — becomes the folder name |
| `business_scope` | «real-estate platform for agents» | one line living in CONTEXT.md |
| `stacks` | laravel,react,flutter | any subset available in templates/ |

## 🔧 Steps

### 1) Pre-flight
- `<name>` does not already exist in `projects/` (otherwise = halt and reject L1 — never replace projects).
- The requested template exists in `templates/<template>/`.
- A formal RCCF work order is logged (L5).

### 2) Spawn
```bash
mkdir -p projects/<name>
cp -r templates/<template>/. projects/<name>/          # stack scaffold
mkdir -p projects/<name>/docs projects/<name>/brain    # contracts + memory
```

### 3) Brain Init — mandatory (L7)
Copy official templates and substitute `PRJ-XXXX` with the project name:
```bash
for f in CONTEXT DECISIONS HANDOFFS LESSONS; do
  cp "hq/brain/brain_templates/$f.md" "projects/<name>/brain/$f.md"
done
```
Then fill `CONTEXT.md`: identity, scope, involved rooms, current pipeline stage, source template used.

### 4) Registration & delivery
- Log the project's birth in `projects/<name>/brain/HANDOFFS.md` (first TKT ticket).
- Deliver to the next room lead in the chain (usually 08-data).

## 📤 Output
```
projects/<name>/
├── backend-laravel/     ← from template: v1 Envelope + Sanctum + ready RBAC
├── app-flutter/         ← one Flutter/Dart app for web and mobile (R2): Envelope<T> + Provider + theme from design-tokens
├── docs/                ← contracts (openapi-v*.json/md)
└── brain/               ← the project's separate memory (CONTEXT/DECISIONS/HANDOFFS/LESSONS)
```

## ⛔ Constraints
- **Strict isolation (L10):** all project work stays inside its folder — touching hq/ or other projects forbidden.
- **Publishing:** projects are not pushed to public repositories except by explicit documented owner exception (SOFI's own products) — client projects stay local forever.
- **Memory:** project decisions live only in their own brain/ — promotion to organization memory requires a CEO decision (L7).
- **Duplication:** a reserved name = rejection; never delete or implicitly overwrite.

## ⬛ Linear Program v2 (OWNER-DIRECTIVE-2026-0823-R2)
- **Position:** generates every new project's tree literally compliant with the v2 line.
- **Mandatory outputs at generation:**
  1) Laravel structure with DDD capsules per `hq/core/standards/ddd-capsule.md` (the canon for new projects — INT-GTW-024)
  2) **One Flutter/Dart application** serving web and mobile (R2) — no React/Next.js tree for new projects at all
  3) Full `/install` installer per `hq/core/standards/installer-standard.md` (requirements check, project name, admin email, lock)
  4) OpenAPI contract placeholder **filled in S2 on paper** (openapi_first — the contract before any code)
  5) `.env.example` never holding real secrets — secrets stay outside the tree
  6) `design-tokens/` empty folder awaiting S3 output (no invented tokens at generation)
- **The four laws:** OpenAPI-first, cross-boundary mocks forbidden (internal testing substitutes exempt), Envelope `hq/core/standards/api-envelope.md`, capsule `hq/core/standards/ddd-capsule.md`.
- **Delivery:** sofi-evidence file:line with the generated file tree.
