# `hq/engine/php-fpm/` — PHP-FPM Pools

> One PHP-FPM pool per Laravel application. Each pool is a **systemd service** that listens on a
> unique TCP port (9001, 9002, ...) and serves one Laravel codebase. Managed by room 11 (DevOps).

Per the deploy standard, each Laravel app = one FPM pool. No sharing of pools between apps
(strict isolation — see `deploy-standard.md`).

---

## Layout

```
php-fpm/
├── README.md                       ← you are here
├── pool.d/                         ← live pools (systemd services)
│   ├── sakk.conf                   ← sakk Laravel pool
│   └── ...
├── disabled/                       ← archived pools (no longer used)
└── disable-pools.sh                ← utility to disable a pool
```

---

## The pool config schema (per `pool.d/*.conf`)

```ini
[pool-name]                         # e.g. sakk
user = www-data
group = www-data
listen = 127.0.0.1:9001             # unique port per pool
pm = dynamic
pm.max_children = 20
pm.start_servers = 4
pm.min_spare_servers = 2
pm.max_spare_servers = 6
pm.max_requests = 1000
chdir = /var/www/sakk
php_admin_value[memory_limit] = 256M
php_admin_value[upload_max_filesize] = 32M
clear_env = no
env[PATH] = /usr/local/bin:/usr/bin:/bin
env[APP_ENV] = production
env[APP_KEY] = base64:...           # loaded from env / vault
catch_workers_output = yes
decorate_workers_output = yes
```

---

## The live pool (sakk)

> Source: `pool.d/sakk.conf` — the sakk Laravel pool.

| Field | Value | Notes |
|-------|-------|-------|
| `listen` | `127.0.0.1:9001` | only localhost, no public access |
| `pm.max_children` | 20 | tune to traffic (4× CPU cores) |
| `pm.max_requests` | 1000 | recycle workers to prevent memory leaks |
| `memory_limit` | 256M | per PHP worker |
| `chdir` | `/var/www/sakk` | project root (per `deploy-standard.md`) |
| `APP_ENV` | `production` | per `deploy-standard.md` |

**Managed by:** `ops-migration-runner` (migrations) + `ops-release-manager` (releases) +
`ops-cicd-engineer` (CI/CD).

---

## Adding a new pool

1. Copy `pool.d/sakk.conf` to `pool.d/<new-app>.conf`
2. Change `listen` to a unique port (next: 9002)
3. Change `chdir` to the new app's path
4. Update `env[APP_ENV]` and `env[APP_KEY]` (load from vault, not from git)
5. Enable the systemd service: `sudo systemctl enable php8.3-fpm@<new-app>`
6. Run `bash hq/engine/scripts/validate.sh` — must exit 0
7. Add a `sites/<new-app>.caddy` to reverse-proxy to the new port
8. Commit atomically — pre-commit enforces all 4 guards
9. Update `OPERATIONS.md` with the new pool

---

## Disabling a pool

```bash
sudo bash hq/engine/php-fpm/disable-pools.sh <pool-name>
```

This moves the pool config from `pool.d/` to `disabled/`, restarts PHP-FPM, and verifies the
disable. Per Law 10 (Direct-on-Project), disabled pools are kept in `disabled/` for audit
(not deleted — for traceability).

---

## The CONDITION-FOLLOW-UP (DEC-R3.4)

> PHP-FPM pool configs in `pool.d/` are **never** truncated in delivery handoffs. They are part
> of the canon and are versioned in git.

---

## See also

- [`../README.md`](../README.md) — `hq/engine/` parent
- [`../sites/README.md`](../sites/README.md) — per-domain Caddy sites
- [`../scripts/README.md`](../scripts/README.md) — operational scripts
- [`../../core/standards/deploy-standard.md`](../../core/standards/deploy-standard.md) — binding standard
- [Top-level README](../../../README.md)
- [`AGENTS.md`](../../../AGENTS.md) — Law 10
