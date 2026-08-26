# OPERATIONS — Infrastructure Runbook (Caddy · Cloudflare · PHP-FPM · cloudflared)

> **Last updated:** 2026-08-25 — after the purge and "sakk only" restructuring (process documentation: `cleanup-workspace/reports/FINAL-REPORT.md`).
> **Approved operating model (local GitOps):** the repository is the version-controlled canonical source ← `scripts/deploy.sh` installs it onto the live system after validation.
> The live machine (`/etc/caddy/Caddyfile`) is merely a client that imports this repository directly — never copy files by hand.

## The Three Services (all must be active)

```bash
./scripts/status.sh          # full pulse: services + sockets + sakk domain health + recent errors
```

| Service | Role |
|---|---|
| `caddy` | Web server/proxy — TLS terminates at Cloudflare (origin is HTTP:80) |
| `php8.5-fpm` | Active pools in the repository: `sakk` only (the five retired ones are disabled in `php-fpm/disabled/`) |
| `cloudflared` | Tunnel from CF Edge to localhost:80 (token-based) |

## Deployment Layer Structure in the Repository

```
hq/engine/
├── Caddyfile              ← short main file: shared snippets + 404 guard + a single import
├── sites/                 ← active sites — one file per domain
│   └── sakk.caddy         ← complete sakk configuration (local + public via tunnel)
├── sites-disabled/        ← hosts disabled by relocation (tobacco · jw · owais · wa · old wildcard)
├── php-fpm/
│   ├── pool.d/sakk.conf   ← the only active pool
│   ├── disabled/          ← pools of retired projects (jw·owais·sofi·sofi-demo·www)
│   └── disable-pools.sh   ← run once as root to disable pools live
├── scripts/               ← validate · deploy · status · diff-live · bootstrap-live
├── cloudflare/            ← tunnel documentation (secrets live outside the repo in ~/.cloudflared)
└── brain/                 ← deployment layer memory (decisions and lessons)
```

**Adding a future domain = three steps, without touching the main file:**
1. Create `sites/<domain>.caddy` (copy the pattern from `sites/sakk.caddy`).
2. `bash hq/engine/scripts/validate.sh` — must pass.
3. `bash hq/engine/scripts/deploy.sh` — seamless reload with zero downtime.

## Standard Change Flow

```text
Edit in the repository (Caddyfile or sites/*.caddy or pool.d/*.conf)
   ↓  ./scripts/diff-live.sh     # review: is the difference intentional?
   ↓  ./scripts/deploy.sh        # validate → seamless reload → status
   ↓  git commit                 # the new canonical state is recorded
```

**Golden rules:**
1. Never reload without a preceding validate — one line prevents production downtime.
2. Broken after deploy? Rollback = restore the previous version from the archive (`SOFI-archive-20260825-2040/caddy/Caddyfile` and `sites/`) then deploy.
3. Manual edits under /etc are forbidden except in emergencies — and afterwards they must be pulled back into the canon immediately (`diff-live` then approval).

## Site Map (after the "sakk only" restructuring · 2026-08-25)

| Host | Status | Backend |
|---|---|---|
| **sakk.local** | 🟢 200 | fpm `sakk.sock` + apps/{admin,portal}/dist |
| **sakk.zanjour.com** (via tunnel) | 🟢 200 — `/admin` blocked with 404 | same sources |
| any other host on :80 (main-file guard) | 🔒 intentional 404 — no content disclosure | — |
| jw.local · tobacco.local · tobacco.zanjour.com · localhost · *.zanjour.com | ⛔ disabled by relocation to `sites-disabled/` | their source paths no longer exist anyway |

> Post-restructuring test (2026-08-25): sakk.local → 200 within ~1ms · sakk.zanjour.com → 200 within ~1.7s · jw/tobacco.local → clean 404 without 500s · public `/admin` → 404 · caddy error log empty.

## Wiring the Live Machine to the Repository (GitOps — in place since 2026-08-09)

`/etc/caddy/Caddyfile` holds a single import line pointing at the SOFI repository (created once via `sudo bash hq/engine/scripts/bootstrap-live.sh`). From then on: edit the repository ← deploy.sh.

## Cloudflare Tunnel Gateway — Fixed Principle

- One route in the CF dashboard: `*.zanjour.com → http://localhost:80` with an **empty** Host header — Caddy selects the site from the original domain name itself (mixing the header with localhost caused past outages).
- Undefined subdomains get a 404 from the main-file guard — nothing is disclosed on random names.
- Secrets (token/credentials) sit in `~/.cloudflared/`, deliberately outside the repository — only documentation lives in `cloudflare/CONFIG-OF-RECORD.md`.

## Emergencies

| Symptom | First check | Remedy |
|---|---|---|
| sakk returns 502 | does the FPM socket exist? `ls /run/php` | `sudo systemctl reload php8.5-fpm` · if it persists: `journalctl -u php8.5-fpm -n 30` |
| CF returns 530/1033 | tunnel is down | `systemctl restart cloudflared` + journalctl |
| certificate/SSL error | SSL mode in CF vs origin | Flexible↔Full depending on ACME state on Caddy |
| caddy rejects config | `bash scripts/validate.sh` | fix the flagged line, then deploy |
| full rollback of the deployment structure | — | `restore.sh caddy/Caddyfile` from the archive + reload (under two minutes) |

## Security Baseline (active · ALT-0001)
- ufw: deny-incoming · allow-outgoing · allow 80/tcp — the tunnel is outbound so it was unaffected
- `/etc/cloudflared/token` = 600 — never copied here
- xrdp disabled (:3389 gone) · project .env files = 600
- Remaining P2 items: MySQL-X bind-address · disable idle docker · postgres nologin

## Nightly Backup (operational discovery M10-b)
A root-scheduled task runs daily at 03:30, writing databases plus encrypted `.enc` keys into `SOFI/backups/` (the folder automatically reverts to root ownership). Blocked from git — opened only for a documented emergency restore.
