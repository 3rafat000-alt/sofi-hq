# SOFI — The Official Flexible Deployment Standard (DEPLOY-STANDARD)
**Status:** ratified by owner order 2026-08-24 (INT-EVOL-2) · binding on new production projects · flexibility lives inside this standard, never outside it.
**Philosophy:** thinking and planning before any deployment line — a documented deployment plan per project is approved within approval points (see gtw-intake-route §approval points).

---

## | 1) The Official Production Stack

| Layer | Technology | Role |
|--------|---------|-------|
| Shield & CDN | **Cloudflare** (proxy enabled) | secured DNS · edge certificate · managed WAF · asset caching |
| Reverse proxy | **Caddy v2** | automatic TLS (Let's Encrypt) · site routing · automatic compression · one readable Caddyfile |
| PHP runner | **PHP-FPM 8.3** (one pool per site) | running Laravel with isolated resources per project |
| Backend | **Laravel** (DDD-STANDARDS) | API + business logic + queues |
| Interfaces | **Unified Flutter/Dart** (R2) for new web+mobile · React SPA and Next.js for existing projects only | per the documented project decision |

> **Flexibility rule:** the choice of "React or Next.js or Flutter-web" for an existing project's interface is documented as an ADR decision in project memory at S1 — flexibility in the documented decision, not in silent improvisation.

## | 2) Reference Caddyfile Pattern (unified template)

```caddyfile
# ===== Project <name> — production =====
<domain>.com {
    # --- Interface (Flutter web / React SPA): static files ---
    root * /var/www/<name>/current/public-web
    encode zstd gzip
    try_files {path} /index.html          # SPA fallback
    file_server

    # --- API on a subpath: Laravel via PHP-FPM ---
    handle /api/* {
        root * /var/www/<name>/current/public
        php_fastcgi unix//run/php/php8.3-fpm-<name>.sock
        header Cache-Control "no-store"    # no caching for API responses
    }

    header {
        Strict-Transport-Security "max-age=31536000"
        X-Content-Type-Options "nosniff"
        X-Frame-Options "DENY"
        Referrer-Policy "strict-origin-when-cross-origin"
    }
    log { output file /var/log/caddy/<name>.log }
}

# Existing Next.js (legacy): route to a Node service instead of the static section
# legacy-<name>.com { reverse_proxy localhost:3000 }
```

## | 3) Binding PHP-FPM Rules
1. **A dedicated pool per project** (`php8.3-fpm-<name>.sock`) — no pool sharing between projects (fault and resource isolation).
2. `pm.max_children` sized to server RAM: the rule is `(available RAM × 1024) / average process consumption in MB` — the calculation is documented in the project runbook.
3. Queues: `queue:work` via **a systemd unit per project** (never manual screen/nohup).
4. `opcache` enabled + `APP_ENV=production` and `APP_DEBUG=false` mandatory before release (quality gate check Gate-5).

## | 4) Binding Cloudflare Rules
1. **Proxy enabled** (orange cloud) on every A/AAAA record — no gray DNS for production.
2. **Always Use HTTPS** + HSTS once certificates stabilize.
3. **Cache Rules:** cache for static assets (`/_flutter/*`, `/assets/*`, `*.js,*.css,*.png`) · **Bypass** for `/api/*` and authenticated paths.
4. **WAF Managed Rules** enabled + Rate Limiting on `/api/*` (starting value: 300 requests/min/IP — adjusted only by documented decision).
5. Secrets (API keys/Tokens) live in `.env` on the server only + project Secrets — **no secret in git nor exposed as text in Cloudflare Workers**.

## | 5) Zero-Downtime Release Pattern
```
/var/www/<name>/
├── releases/2026-08-24-a/     # every release is a dated folder
├── releases/2026-08-20-b/
└── current -> releases/2026-08-24-a   # instant symlink = immediate switch
```
1. Build into a new release folder → safe migrations (dat-schema-migration) → switch the symlink → health check (`/api/health` returns 200) → keep the last 5 releases for safe deletion.
2. **Rollback:** repoint the arrow to the previous release within seconds — the rollback plan is a condition for approving any deployment (ops-deploy-runbook).

## | 6) Pre-Deployment Checklist — Gate S6 / Gate-7 Production (INT-GTW-024)
- [ ] Approved deployment plan (approval point) + written rollback plan
- [ ] `APP_ENV=production` · `APP_DEBUG=false` · real keys, not test ones
- [ ] Migrations rehearsed on a mirror-image staging copy
- [ ] Flutter web built with the approved design system (Design Freeze Review (DFR) signature present)
- [ ] Caddyfile tested locally + green certificates
- [ ] Cloudflare: proxy/WAF/cache rules applied per §4
- [ ] Health check green + obs monitoring wired (Contract 08)
- [ ] Backup taken before deployment + release log in project HANDOFFS

---
*References: stacks-tech.md (stacks) · pipeline-production-line.md (S6) · ops-deploy-runbook (execution) · dat-schema-migration (databases). Last updated 2026-08-24.*

---
## | 7) Local Development Environment (annex amended 2026-08-24 — owner order INT-GTW-017)
> ⚠️ **This annex supersedes its old wording**, which placed the local Caddyfile outside the project (`~/caddy/Caddyfile.local`) — the later owner directive cancelled that: **all infrastructure files live inside the project folder exclusively** (`docker/caddy/Caddyfile`) with zero files at system roots.

**The rule now in force:** the local development environment is governed exclusively by `devops-standard.md` — Docker containers inside the project (Laravel · MySQL · Caddy) + `<project>.localhost` domains + a unified Makefile interface, with service-shape parity with this standard (production) and variables as the only difference. The "never touch production data or keys locally" rule remains verbatim.
