# PHP-FPM 8.5 — Work Pools

> Live source: `/etc/php/8.5/fpm/pool.d/` · these are canonical, repository-managed copies.
> **After the "sakk only" restructuring (2026-08-25):** active pools in the repository = `sakk.conf` exclusively; all other pools moved to `php-fpm/disabled/`.

## Pool ↔ Project Map

### Active
| Pool | Socket | Serves | Note |
|---|---|---|---|
| `sakk.conf` | `/run/php/sakk.sock` | sakk project (Laravel) | its own standalone repository outside SOFI · user `es3dlll` |

### Disabled (in `php-fpm/disabled/` — restoring = move the file back to `pool.d/` + reload)
| Pool | Used to serve | Reason for disabling |
|---|---|---|
| `sofi.conf` | tobacco-center (production) | project path no longer exists |
| `sofi-demo.conf` | tobacco demo | same reason |
| `owais.conf` · `jw.conf` | side projects/experiments | outside the "sakk only" scope |
| `www.conf` | unused default for sites | no beneficiary |

> ⚠️ **The only remaining root step:** disabling the pools *live* on the system requires root privileges — run once:
> `sudo bash caddy/php-fpm/disable-pools.sh` (stops the five pools and reloads fpm seamlessly).

## Core Commands

```bash
# syntax check before any reload
php-fpm8.5 --test
# safe reload (zero downtime)
sudo systemctl reload php8.5-fpm
# process status per pool
sudo systemctl status php8.5-fpm
ps --ppid $(pgrep -o php-fpm) -o pid,cmd | head
```

## ⚠️ Institutional opcache Rule (lesson LES-022)

`validate_timestamps=Off` is enabled for production ⇒ **any edited PHP file only takes effect after a reload**:

```
Edited PHP?  →  sudo systemctl reload php8.5-fpm  →  verify via the endpoint
```

> **Note on validate without root:** the pool check may complain about `error_log (/var/log/php8.5-fpm.log): Permission denied` — that is a privilege limitation, not a syntax error; run `sudo ./scripts/validate.sh` for full confirmation.
