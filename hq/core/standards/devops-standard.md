# SOFI — Unified Engineering Workflow Standard (DEVOPS-STANDARD)
**Status:** ratified by direct owner order 2026-08-24 (INT-GTW-017) · binding on every team member on every project.
**Purpose:** full institutional mastery of Git · GitHub · Docker — so that any project can be launched from scratch on any machine and any operating system (Linux/macOS/Windows) within minutes, with zero dependence on machine-specific installations.
**Relation to standards:** complements `deploy-standard.md` (production) and supersedes its former §7 annex (which placed Caddy outside the project) — the development environment now lives **isolated inside the project folder exclusively**. Subject to the eleven laws of AGENTS.md and never above them.

---

## | 0) The Five Governing Principles (Non-Negotiable)

| # | Principle | Practical Meaning |
|---|--------|----------------|
| P-1 | **Portability-First** | Machine requirements: Docker + Git + Make only. Installing PHP, MySQL, Composer, or Caddy on the host OS is forbidden — everything runs inside containers |
| P-2 | **Project Isolation** | All infrastructure files (`compose.yml`, `Caddyfile`, `Dockerfile`, init scripts, Makefile) live inside `<project>/docker/` and project folders — **zero files at system roots** (`/etc`, `~/`) |
| P-3 | **Reproducibility** | Same command = same result on any machine. Versions are pinned by number; structural data (migrations+seeders) is the source of truth |
| P-4 | **Environment Parity** | Development and production share the same service shape and the same routing logic; the only difference between them is environment variables (12-Factor) |
| P-5 | **Mandatory Evidence** | Every infrastructure change = ADR + documented commit (Law 4) — verbal infrastructure changes are never accepted |

---

## | 1) Standard Docker Architecture (Laravel · MySQL · Caddy)

### 1.1 The Mandatory Tree Inside Every Project

```
projects/<name>/
├── docker/
│   ├── compose.yml              # the single source of assembly
│   ├── caddy/
│   │   └── Caddyfile            # local routing — inside the project, not /etc nor ~/caddy
│   ├── app/
│   │   └── Dockerfile           # multi-stage PHP-FPM
│   └── mysql/
│       └── init/                # one-time bootstrap scripts (run once on first volume creation)
├── Makefile                     # the mandatory interface for all commands (§2)
├── .env.example                 # variable template — the only tracked copy in git
└── .env                         # local only — blocked by the secrets safety net (gitignore)
```

> **Strict isolation rule:** if the project needs to alter Caddy or PHP behavior, that happens by editing the project's `docker/` files and syncing through the container — never by touching a host service. Any solution requiring `/etc/...` or `~/...` is wrong design and is sent back.

### 1.2 Reference compose Pattern (`docker/compose.yml`)

```yaml
name: <project>                      # fixed name = automatic isolation of containers, networks, and volumes

services:
  app:                               # Laravel via PHP-FPM 8.3
    build:
      context: ..
      dockerfile: docker/app/Dockerfile
    restart: unless-stopped
    env_file: ../.env
    volumes:
      - ..:/var/www/html:cached      # on macOS, :cached guarantees code consistency without slowdown
    depends_on:
      db:
        condition: service_healthy   # no migrate before a real database is ready
    networks: [net]

  web:                               # Caddy — routing and local certificates
    image: caddy:2.8-alpine
    restart: unless-stopped
    ports:
      - "${HTTP_PORT:-8080}:80"      # ports come from the central registry (§1.5) — no local 80/443
      - "${HTTPS_PORT:-8443}:443"
    volumes:
      - ./caddy/Caddyfile:/etc/caddy/Caddyfile:ro
      - caddy_data:/data             # local certificates managed inside an isolated volume
      - caddy_config:/config
    depends_on: [app]
    networks: [net]

  db:                                # MySQL 8 — data in a named volume, not a bind mount
    image: mysql:8.4
    restart: unless-stopped
    environment:
      MYSQL_DATABASE: ${DB_DATABASE}
      MYSQL_USER: ${DB_USERNAME}
      MYSQL_PASSWORD: ${DB_PASSWORD}
      MYSQL_ROOT_PASSWORD: ${DB_PASSWORD_ROOT}
    volumes:
      - db_data:/var/lib/mysql
      - ./mysql/init:/docker-entrypoint-initdb.d:ro
    healthcheck:                     # the gate every later step waits on
      test: ["CMD-SHELL", "mysqladmin ping -h127.0.0.0 -u$${MYSQL_USER} -p$${MYSQL_PASSWORD} --silent"]
      interval: 5s
      timeout: 3s
      retries: 20
    networks: [net]

volumes:
  db_data:
  caddy_data:
  caddy_config:

networks:
  net:
    driver: bridge
```

**Binding compose rules:**
1. A fixed `name:` per project — prevents container/volume mixing between concurrent projects.
2. Every image pinned to a numeric version (`caddy:2.8-alpine`, not `latest`) — `latest` is forbidden in all tracked files.
3. A `healthcheck` is mandatory for db (and app when adding a queue) — dependencies wait for `service_healthy`, not merely container start.
4. Development database data lives in a **named volume** (`db_data`) — no bind mount of the MySQL data directory onto the host (macOS permission breakage is guaranteed).
5. The network is private to the project name — no project sees another project's containers.
6. Validate any edit before committing: `docker compose -f docker/compose.yml config -q` must return silent (exit 0).

### 1.3 Local Caddyfile Template (`docker/caddy/Caddyfile`)

```caddyfile
# Local development — inside the project exclusively. No external TLS or DNS here (that is DEPLOY-STANDARD).
<project>.localhost {
	encode zstd gzip
	root * /var/www/html/public
	php_fastcgi app:9000
	file_server

	handle /api/* {
		header Cache-Control "no-store"
	}

	log { output stdout }
}
```

**Why `*.localhost`?** Browsers resolve `.localhost` domains to the local machine themselves (RFC 6761) — it works on Linux/macOS/Windows **with no hosts edits, no root privileges, and no collision with other projects' domains**. Caddy issues a local certificate automatically when using the defined port 443.

### 1.4 Multi-stage Dockerfile Pattern (`docker/app/Dockerfile`)

```dockerfile
# Stage 1: install PHP dependencies in a cacheable way
FROM composer:2 AS vendor
WORKDIR /app
COPY composer.json composer.lock ./
RUN composer install --no-dev --no-scripts --prefer-dist --no-interaction

# Stage 2: runtime image
FROM php:8.3-fpm-alpine
RUN docker-php-ext-install pdo_mysql opcache \
 && apk add --no-cache icu-dev libzip-dev zip \
 && docker-php-ext-install intl zip bcmath
WORKDIR /var/www/html
COPY --from=vendor /app/vendor ./vendor
COPY . .
RUN chown -R www-data:www-data storage bootstrap/cache
USER www-data                          # never run as root inside the container
EXPOSE 9000
CMD ["php-fpm"]
```

**Binding Dockerfile rules:** multi-stage (dependencies then runtime) · dependency layers before copying code (fast build cache) · non-root `USER` · never bake secrets into the image (passed at runtime via env_file).

### 1.5 Central Port Registry (prevents collisions between concurrent projects)

Each project owns its own range of ten ports. **Adding a new row = an ADR decision documented in this file** (no silent improvisation):

| Project | HTTP | HTTPS | Additional services |
|---------|------|-------|---------------|
| Default for any new project | 8080–8089 | 8443–8449 | — |
| tobacco-center | (currently live production on 80/443 via DEPLOY-STANDARD — container migration via ADR) | | |
| sofi-shop | 3105 (Next.js) | — | API 8123 |
| spirit-lp | 3020 | 3443 | Node 22 |

The rule: the first port of the range is defined in `.env.example` (`HTTP_PORT`, `HTTPS_PORT`) — no hard-coded numbers inside compose.

### 1.6 macOS and Apple Silicon Specifics

1. **Processor architecture:** the base images used are all official multi-arch (php/alpine · mysql · caddy) — they run on M-series and Intel with no special setup. Manual image builds with `platform:` are forbidden except for a documented defect.
2. **File performance:** bind mounts always use `:cached` (macOS) — if intensive tests feel slow, enable VirtioFS from Docker Desktop settings (default in recent versions) before any external workaround.
3. **MySQL memory:** a Docker Desktop memory limit ≥ 4GB is a condition for comfortable operation — noted in the project runbook.
4. **Line endings:** `.gitattributes` enforces `* text=auto eol=lf` — Windows line endings are the classic cause of broken entrypoint scripts.

---

## | 2) Lifecycle & Build — the "From Zero" Protocol (Build & Setup)

### 2.1 The Mandatory Interface: Makefile

**Memorizing long compose commands from headers or docs is forbidden** — everything goes through standard make targets, uniform across all projects:

```makefile
COMPOSE := docker compose -f docker/compose.yml

setup:        ## first boot from zero (build + up + install + seed)
	$(COMPOSE) up -d db
	$(COMPOSE) up -d --build app web
	$(COMPOSE) exec -T app composer install --no-interaction
	$(COMPOSE) exec -T app php artisan key:generate
	$(COMPOSE) exec -T app php artisan migrate --seed
up:       ; $(COMPOSE) up -d --build
down:     ; $(COMPOSE) down
stop:     ; $(COMPOSE) stop
logs:     ; $(COMPOSE) logs -f --tail=100
shell:    ; $(COMPOSE) exec app bash
test:     ; $(COMPOSE) exec -T app php artisan test
lint:     ; $(COMPOSE) exec -T app ./vendor/bin/pint --test
fresh:    ; $(COMPOSE) exec -T app php artisan migrate:fresh --seed
dump:     ; mkdir -p backups && $(COMPOSE) exec -T db sh -c 'exec mysqldump -u$$MYSQL_USER -p"$$MYSQL_PASSWORD" $$MYSQL_DATABASE' > backups/db-$$(date +%Y%m%d-%H%M%S).sql
nuke:     ## full reset — containers and data (migrations+seeders are the source of truth)
	$(COMPOSE) down -v --remove-orphans
	$(MAKE) setup

.PHONY: setup up down stop logs shell test lint fresh dump nuke
```

### 2.2 Boot Protocol on a New Machine (step by step — target ≤ 15 minutes)

| # | Step | Command | Verification |
|---|--------|-------|--------|
| 0 | Only three prerequisites | Install Docker Desktop + Git + Make | `docker --version` · `git --version` · `make --version` |
| 1 | Clone the project | `git clone <repo-url> && cd <project>` | `docker/compose.yml` exists |
| 2 | Prepare the local environment | `cp .env.example .env` then fill values from the team vault (**copying production keys locally is forbidden**) | `.env` exists and is untracked (`git status` clean of it) |
| 3 | Full boot | `make setup` | finishes without error — the db healthcheck is what opens the door to migrate |
| 4 | Live verification | open `http://localhost:8080` and `/api/health` | page renders + success JSON |
| 5 | Tests | `make test` | fully green |
| 6 | Record elapsed time | log actual minutes in the project runbook | exceeding 15 minutes = an infrastructure defect gets a ticket |

### 2.3 Binding Build Rules

1. **Order is not reversible:** db (until healthy) ← app/web ← composer ← key ← migrate ← seed. Jumping the order causes 90% of "first run" failures.
2. **Reset is safe by design:** `make nuke` wipes everything and rebuilds it — because migrations and seeders are the source of truth (P-3). Fearing nuke means data without a migration — a defect fixed immediately.
3. **Local backup through the container:** `make dump` writes SQL into `backups/` inside the project (blocked from git) — no reliance on a mysqldump installed on the host.
4. **Periodic clean build:** before every large merge, run `docker compose build --no-cache app` once to verify no reliance on stale cache.

---

## | 3) Git & GitHub Protocol (code integrity and team synchronization)

### 3.1 Branching Pattern — compliant with Law 10 (the main tree)

> **Constitutional balance:** Law 10 forbids long-lived isolated branches and worktrees. Our pattern is therefore **diluted trunk-based**: one branch per task, short-lived, merged before ticket closure — no long-lived develop/staging branches and no work sleeping overnight locally.

| Branch | Purpose | Lifetime |
|-------|-------|------|
| `main` | the single truth — deployable at any moment, protected | permanent |
| `task/<ticket>-<slug>` | one task branch (example: `task/SHP-042-vendor-profile`) | **≤ 48 hours** — merged before ticket closure (Law 10 exception condition) |

**Forbidden:** permanent personal branches · long-lived `dev`/`test` · worktrees · pushing a task branch whose owner has not merged it within two days without escalation.

### 3.2 Commit Convention (Conventional Commits)

```
<type>(<scope>): <summary ≤ 72 characters>

[optional body — why, not what]
Refs: <TICKET>
Evidence: <file:line of evidence — Law 4>
```

- **Locked types:** `feat · fix · chore · docs · refactor · test · perf · ci · infra`
- **Rules:** one atomic commit per logical change · secrets are forbidden in any commit body even if the file is later deleted (history is eternal) · `--no-verify` to bypass checks is forbidden.

Examples from real institutional practice (matching our actual log):
```
feat(shop): W2 — landing v2 complete + axe AA zero violations
chore(git): sakk nested boundaries + block encrypted backups and keys (INT-GTW-016)
```

### 3.3 Pull Request Protocol (mandatory even for solo work)

1. **Never push directly to `main`** — protection is enabled on GitHub (Require PR + Require checks pass).
2. **The mandatory description template:**
   ```markdown
   ## What
   ## Why (ticket/context)
   ## How tested (commands + results + UI screenshots)
   ## Risks and rollback
   ```
3. **CI gates before merge** (GitHub Actions inside the project's own container — same dev image):
   - `composer lint` (Pint) · `php artisan test` · `docker compose -f docker/compose.yml config -q`
   - one red = no merge (Law 8: quality before speed).
4. **Mandatory self-review:** the PR author reviews the diff line by line personally before requesting merge — a second reviewer (a peer or room lead) for touchpoints: schema · security · infrastructure · financial operations.
5. **Squash merges only** — linear history: every task = one clean commit on main, and the branch is deleted immediately after merging.
6. **Force-push is forbidden** except for a documented emergency recovery backed by a report (a brief ADR) — that alone is the exception.

### 3.4 Daily Sync Ritual (the documented INT-GTW-016 lesson)

| Moment | Ritual | Reason |
|--------|-------|-------|
| Session start | `git pull --rebase origin main` | start from the latest truth, not a stale copy |
| During work | atomic commits at every completed step | divide risk |
| **Session end — mandatory** | `git push` — **unpushed work or dirty files must never sleep overnight** | the 2026-08-24 session found 135 exposed files unprotected — never again |

### 3.5 Releases (Tags)

On every approved release (S6 gate / Gate-7 Production): `git tag -a vX.Y.Z -m "release notes"` + push the tag. MAJOR breaks compatibility, MINOR adds a feature, PATCH fixes. The tag is the reference the production symlink points to in DEPLOY-STANDARD §5.

---

## | 4) Environment Consistency — "works on my machine" has no place here

1. **One home per version:** PHP/MySQL/Caddy versions are pinned in three literally synchronized locations: `docker/*.Dockerfile` + `docker/compose.yml` + `composer.json`/`platform` requirements. Changing a version without changing all three = rejected commit.
2. **The difference between environments = variables only:** the same app image in development and production; what changes is `.env` (APP_ENV, DEBUG, keys). Any `if (env('APP_ENV') === 'local')` inside business logic = design smell rejected in review.
3. **Secrets:** `.env` is blocked by the secrets safety net (activated 2026-08-24) — `.env.example` with placeholder values is the only tracked file. A leaked key in a commit = immediate key rotation + history scrubbing by documented decision.
4. **Periodic "new machine" drill (The New-Machine Drill):** once a month (and whenever any member joins), the entire project is launched on a clean machine/VM following §2.2 verbatim. Time is measured and compared to target; every obstacle = a fix ticket. **The golden criterion: anyone who can read this standard alone can run the project — without asking anyone.**
5. **Moving the database between machines:** exclusively via `make dump` / import inside the db container — sharing raw MySQL data directories across systems is forbidden (inode/permission differences corrupt them).

---

## | 5) Team Governance — Professional Engagement Rules

| # | Rule | Detail |
|---|---------|---------|
| R-1 | **Infrastructure change = documented decision** | any edit to `docker/`, CI, or the port registry (§1.5) goes through a brief ADR in project memory + ops-lead review — no silent touches |
| R-2 | **Infrastructure as code** | no manual setup on any machine counts as "done" unless written into tracked files — what cannot be reproduced from a clean clone does not exist |
| R-3 | **Broken main = absolute top priority** | red CI checks on main: stop all merging and either fix within 60 minutes or revert immediately — then investigate calmly |
| R-4 | **Evidence in every delivery** (L4) | a PR without a "how tested" section is auto-rejected — screenshots are mandatory for interface changes |
| R-5 | **Chain of responsibility** (L9) | branch owner answers for merge integrity; the lead answers for the review gate; violations escalate as in AGENTS.md |
| R-6 | **Document deviations** | could not follow this standard for a specific case? Document the deviation with reasons in an ADR — silent deviation is an L2 violation |
| R-7 | **Onboarding path for a new member** | (1) read this standard fully → (2) execute the New-Machine Drill successfully ≤15 minutes → (3) first simple PR passing the full protocol — only then may production work be assigned |

---

## | 6) Reference Annexes

### 6.1 PR Description Template (copy into the project's `.github/pull_request_template.md`)
```markdown
## What
## Why (Refs: <TICKET>)
## How tested
- [ ] make lint ✓ (exit=__)
- [ ] make test ✓ (__ passed)
- [ ] compose config valid ✓
- [ ] screenshots (if interfaces changed)
## Risks and rollback plan
```

### 6.2 Smallest CI Workflow (`.github/workflows/ci.yml`)
```yaml
name: ci
on: [pull_request]
jobs:
  checks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - name: Validate compose
        run: docker compose -f docker/compose.yml config -q
      - name: Build & test inside container
        run: |
          cp .env.example .env
          docker compose -f docker/compose.yml up -d --build db app
          docker compose -f docker/compose.yml exec -T app composer install --no-interaction
          docker compose -f docker/compose.yml exec -T app php artisan test
```

### 6.3 Constitutional Compliance Table
| Law | Applied here |
|---------|------------|
| L4 Evidence | "how tested" section + mandatory Evidence footers |
| L8 Quality | red CI gates block merging regardless of deadlines |
| L9 Responsibility | branch owner ← lead ← CEO escalation on main breakage |
| L10 Main tree | task branches ≤48h merged before ticket closure — no long silos |
| L7 Memory | every infrastructure change = an ADR in project brain or CORTEX |

---
*References: deploy-standard.md (production and the releases/current pattern) · stacks-tech.md · dat-schema-migration (migrations as source of truth) · ops-deploy-runbook (release execution).*
*Enacted by gtw-intake-reformer under direct owner order — 2026-08-24 · last updated: 2026-08-24.*
