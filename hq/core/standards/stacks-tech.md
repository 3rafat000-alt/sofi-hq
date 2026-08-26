# SOFI — Tech Stack Standards (Stack Architecture Standards)
**Binding for every project using this stack under `projects/<name>/` (STRUCTURE.md §4). Source: study of real live code, not generic internet templates.**

> Purpose: one decisive structuring map for every tech stack SOFI builds — instead of each project inventing its own structure from scratch or imitating generic tutorials. One stack is documented here now: **Laravel + React + Flutter (monorepo)**. Future stacks are added as new sections in the same shape.

---

## | Laravel + React + Flutter — Monorepo

**Source:** study of an actual live folder structure (a real production project under development), from which the architectural pattern was extracted and generalized — real names (specific domains/features) were replaced with generic `<Placeholder>` names so the template fits any new project.

### 1) Overall Shape (4 layers + monorepo root)

```
<project>/
├── backend/          ← a single Laravel API serving all three clients (layer 1)
├── apps/
│   ├── web/          ← React (public/marketing, usually display-only) (layer 2)
│   └── admin/        ← React (control panel, full data layer) (layer 2)
├── packages/
│   └── ui/            ← design tokens package shared across apps (layer 3)
├── mobile/            ← Flutter (layer 4)
├── package.json        ← pnpm workspace root (for apps/ + packages/ only)
└── pnpm-workspace.yaml
```

**Governing rule:** three fully separate runtimes (pnpm/JS, composer/PHP, pub/Dart) — **never share a single runtime tool**. Coordination between them is structural only: same root folder, same API contract (versioned REST `/api/v1`), same design tokens where the language allows (JS/TS only), and the same "one folder per unit of work" logic (domain on the backend, feature in every client) — so the developer's mental model stays uniform across all four layers even though build tools differ.

---

### 2) Backend — Laravel (DDD-flavored)

```
backend/
├── app/
│   ├── Core/                          # Shared base — no business logic, no knowledge of any domain
│   │   ├── Base/                      # BaseService, Controller, Handler, Money…
│   │   ├── Exceptions/
│   │   ├── Interfaces/
│   │   └── Traits/
│   │
│   ├── Infrastructure/                # External integration adapters only (payment gateways, SMS, …) — one per external service
│   │
│   ├── Domains/                       # [Legacy of existing projects — the new canon: DDD-STANDARDS]
│   │   └── <DomainName>/              # Every domain folder follows this exact "stereotype":
│   │       ├── Actions/               #   one class = one operation/use-case
│   │       ├── DTOs/
│   │       ├── Enums/
│   │       ├── Exceptions/
│   │       ├── Http/
│   │       │   ├── Controllers/
│   │       │   ├── Requests/
│   │       │   └── Resources/
│   │       ├── Models/
│   │       ├── Providers/
│   │       │   └── <DomainName>ServiceProvider.php   # registers this domain's bindings only
│   │       ├── Routes/
│   │       │   └── api.php            # self-contained: its own use-statements + prefix + throttle
│   │       ├── Services/
│   │       └── Database/
│   │           ├── Factories/
│   │           └── Seeders/
│   │       # Optional depending solely on the domain's needs: Interfaces/ (ports for external services),
│   │       # Policies/, Console/, Mail/, Support/, Traits/, Casts/
│   │
│   ├── Http/Middleware/               # app-wide middleware
│   ├── Jobs/                          # queued jobs spanning more than one domain
│   ├── Providers/
│   │   ├── AppServiceProvider.php
│   │   └── DomainServiceProvider.php  # single control point for any old↔new compatibility during gradual migration
│   └── Services/                      # shared code not yet migrated to a domain (transitional only, not permanent)
│
├── bootstrap/providers.php            # explicit list: core providers + one provider per domain
├── config/
│   └── <app-namespace>/app.php        # optional custom namespace config (instead of polluting the root config)
├── database/
│   └── migrations/
│       └── NN_<group-name>/           # migrations grouped by number + group name, with squashed.sql as the schema snapshot
├── routes/domains.php                 # auto-collects every Domains/*/Routes/api.php — no manually-edited central registry
└── tests/{Feature/Api, Unit/Domain}/
```

**Rule for adding a new domain:** create `app/Domains/<Name>/` following exactly the stereotype above — do not touch `routes/domains.php` (it is discovered automatically); register the Provider manually in `bootstrap/providers.php`.

---

### 3) Frontend — React [Legacy section: existing projects only — new work is Flutter/Dart per R2]

(same shape for web and admin)

```
apps/<app-name>/                       # @<scope>/web and @<scope>/admin — same shape, different depth
├── src/
│   ├── app/                           # (usually admin only) app composition layer: providers/router/routes.tsx
│   │
│   ├── features/                      # one feature = one folder
│   │   └── <feature-name>/            # every feature folder follows this "stereotype":
│   │       ├── pages/                 #   route-level components
│   │       ├── services/              #   <feature>.api.ts — all axios calls for that feature only
│   │       ├── hooks/                 #   use<Feature>.ts — wraps services
│   │       ├── types/                 #   <feature>.types.ts
│   │       └── components/            #   UI local to the feature (optional)
│   │
│   ├── shared/                        # code spanning all features
│   │   ├── components/                #   one UI element = one folder (<Component>/<Component>.tsx + index.ts)
│   │   ├── hooks/                     #   general hooks (admin: some feature hooks repeat here if used in multiple places)
│   │   ├── layouts/                   #   Navbar/Footer or AdminLayout/Sidebar/Topbar
│   │   ├── services/                  #   api.ts — single axios instance + interceptors (the only network point)
│   │   ├── types/                     #   api.types.ts — shared API response shapes
│   │   └── utils/
│   │
│   ├── styles/                        # globals.css
│   ├── App.tsx · main.tsx · vite-env.d.ts
│
├── tailwind.config.ts                 # imports theme from @<scope>/ui/tailwind.config
├── tsconfig.json                      # paths: "@/*"→src, "@<scope>/ui/*"→../../packages/ui/*
└── vite.config.ts
```

**Rule:** no raw HTTP calls outside `shared/services/api.ts` — every feature consumes it only through its own `services/<feature>.api.ts`. web is usually display-only (simple axios), admin carries a full data layer (React Query) — do not force complete symmetry between the two if the project does not need it.

---

### 4) Shared Package — packages/ui

```
packages/ui/
├── src/
│   ├── index.ts        # re-exports tokens
│   └── tokens.ts        # raw design token values (colors, fonts)
├── tailwind.config.ts    # exports theme + factory function createTailwindConfig(contentGlobs)
└── package.json          # "@<scope>/ui" — apps consume it via "workspace:*"
```

It exports **tokens only, no components** — a deliberate simplification. It has no counterpart in Flutter (Dart cannot consume an npm package) — colors are rewritten manually in `mobile/lib/core/theme/`.

---

### 5) Mobile — Flutter (clean-architecture-lite)

```
mobile/
├── lib/
│   ├── core/                          # general infrastructure, no knowledge of any feature
│   │   ├── constants/api_constants.dart   # baseUrl + all endpoint paths in one place
│   │   ├── network/api_client.dart        # dio wrapper — the only network point
│   │   ├── router/app_router.dart         # go_router
│   │   ├── storage/                       # secure_token_storage.dart, hive_cache.dart
│   │   ├── theme/                         # colors/fonts/design tokens (copied manually from packages/ui)
│   │   ├── di/service_locator.dart
│   │   └── services/                      # biometric/device/fcm/location/permission…
│   │
│   ├── features/                      # one feature = one folder
│   │   └── <feature-name>/            # every feature folder follows this "stereotype":
│   │       ├── data/
│   │       │   ├── models/            #   <name>_model.dart (+ .g.dart if json_serializable)
│   │       │   └── repositories/      #   <name>_repository.dart — calls core/network only
│   │       ├── presentation/
│   │       │   ├── pages/
│   │       │   └── widgets/
│   │       └── providers/             #   <name>_provider.dart — state (Riverpod), if the feature needs state
│   │
│   ├── shared/                        # cross-feature domain code (not general UI — that lives in core/widgets)
│   │   ├── models/ · providers/ · repositories/ · services/
│   │
│   └── main.dart
└── pubspec.yaml
```

**baseUrl via `--dart-define` at build time** (`String.fromEnvironment`), not a `.env` file — different from the web/admin convention.

---

### 6) Wiring Between Layers (Wiring)

- **One API for all clients:** every backend domain registers its own route, and `routes/domains.php` collects them automatically under a versioned prefix (`/api/v1`). CORS allows only the two known web origins (`FRONTEND_URL`, `LOCAL_URL`) — mobile is a native client and therefore outside CORS.
- **One network point per client:** `shared/services/api.ts` (web/admin) or `core/network/api_client.dart` (mobile) — no exceptions.
- **The shared package:** `packages/ui` via `workspace:*` in pnpm — tokens only, consumed directly or through the Tailwind config.
- **Build tools fully separate:** pnpm (`--filter @scope/app`) for JS, composer scripts (`pint`, `phpstan`, `php artisan test`) for PHP, standalone scripts (`build_release.sh` and others) for Flutter — the monorepo root never touches backend or mobile.

---

### 7) Scaffolding Procedure — folders only, no files

When starting a new project on this stack:

1. Create the entire folder tree above — **`mkdir -p` only, zero files, not even a README inside the tree itself** (all explanation lives here in this file, not inside the scaffold).
2. **Only then** run each framework's native tooling in its place in the tree: `composer create-project laravel/laravel backend`, `npm create vite@latest apps/web` and `apps/admin`, `flutter create mobile` — these tools fill in their framework's standard files.
3. Add the first `Domains/<Name>/` or `features/<name>/` following exactly the "stereotype" documented above — do not invent a new shape.
4. Wire `packages/ui` via `workspace:*` from the first app — do not defer it.

**Rationale:** the scaffold (folders) permanently and clearly documents the architectural decision; files come from each framework's own tooling and stay current with every new framework release, instead of copying old files the tool may outdate.

---

*Last updated: 2026-07-24 — first documented stack (Laravel+React+Flutter), extracted from a real live-code study at the owner's request.*

---

## | Owner Decision R2 — Unified Flutter/Dart Interfaces (2026-08-23 · SOFI-HQ-INT-0003)

- **Every new project:** web and mobile share a single **Flutter/Dart** stack — `apps/web` and `mobile` come from the same code base, state logic, and design system (ThemeData receives design-tokens directly).
- **The Laravel + React stack above:** remains in force **non-retroactively** on existing projects (tobacco-center · sakk) for maintenance only — no application to new work. The earlier exception (sofi-shop by decision DEC-0009) was **revoked by owner order (INT-GTW-033)** — Next.js was removed from projects entirely and R2 was restored.
- **Laravel Boost is mandatory** for every new project's backend once it reaches S4: `composer require laravel/boost --dev && php artisan boost:install` — live documentation + MCP tools for schema and commands.
- The `dart-flutter` MCP server is centrally enabled in opencode.json for rooms 06/07.
- The template `hq/core/tech_templates/auth-rbac-stack/frontend-react` is marked **LEGACY** (see LEGACY-NOTE.md inside it) — a Flutter Web equivalent is to be derived at the first new project.
