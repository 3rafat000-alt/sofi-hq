# CADDY-CHANGE — Deployment Layer Change Summary

> Purpose: before/after of the deployment restructuring, plus actual check and test results.
> Created: 2026-08-25 · Team: Wave 5a · Risk level: live production — executed under a documented security gate.

## Before (unified Caddyfile · 405 lines)

- A 410 block for dead hosts (jw·owais·wa·wa-track)
- A full tobacco setup (snippets + 4 hosts) pointing at the `projects/tobacco-center` path **which does not exist on disk at all**
- wildcard `*.zanjour.com → 404` · localhost serving tobacco
- sakk local and public in the same file (229 of the 405 lines)
- /etc/caddy/Caddyfile a thin file importing this one directly (GitOps — unchanged)

## After

```
Caddyfile            43 lines: shared snippets (block_sensitive · security_headers · csp_sakk)
                               + http://:80 guard → 404 for any unknown host
                               + import sites/*.caddy
sites/sakk.caddy     full sakk config carried verbatim (no functional change — confirmed by visual fingerprint of blocks)
sites-disabled/      jw-owais-wa-410.caddy · wildcard-zanjour.caddy · tobacco.caddy (text as it was)
php-fpm/pool.d/      sakk.conf only
php-fpm/disabled/    jw · owais · sofi · sofi-demo · www (+ root script disable-pools.sh to stop them live)
```

**Adding a future domain:** a `sites/<domain>.caddy` file → `validate.sh` → `deploy.sh`. The main file untouched.

## Actual Check & Test Results (2026-08-25)

| Check | Result |
|-------|---------|
| `validate.sh` on the new canon | ✓ Valid configuration — exit 0 |
| negative test (config with a deliberate error) | ✓ validation rejected it — the barrier works; live untouched |
| reload | ✓ graceful via admin API (`caddy reload`) — no sudo and no dropped connections |
| `http://sakk.local/` | ✓ **200** in 0.001s |
| `https://sakk.zanjour.com/` (through tunnel) | ✓ **200** in 1.68s |
| `/admin` from outside | ✓ blocked **404** (as planned) |
| `/admin` locally | ✓ 301 to /admin/ (normal behavior) |
| `http://jw.local/` and `tobacco.local/` | ✓ clean disable **404** — no 500 page |
| `GET /api/` via sakk.sock socket | ✓ HTTP response in 0.12s — FastCGI alive |
| caddy error log after reload | ✓ zero entries |
| php8.5-fpm | ✓ active — sakk pool running; stopping the five live = one documented root step in BLOCKED.md |

## Full Rollback (if needed — under two minutes)

```bash
bash ../SOFI-archive-20260825-2040/restore.sh caddy/Caddyfile
rm -rf sites sites-disabled && mkdir sites   # then rebuild from the archive when needed
bash scripts/validate.sh && caddy reload --config /etc/caddy/Caddyfile
```
