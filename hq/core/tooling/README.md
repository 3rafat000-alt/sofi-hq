# `hq/core/tooling/` — The 4 Constitutional Guards + Pre-Commit

> The **machine-checked law enforcement layer** of SOFI HQ. These Python scripts run on every
> commit (via `hooks/pre-commit`) and block any change that violates a constitutional invariant.

If a guard fails → commit is blocked. If a guard warns (`PENDING`) → the commit is allowed but the
warning must be resolved before the next fateful change.

---

## Files

| File | Law | Purpose | Exit code |
|------|-----|---------|-----------|
| `registry_guard.py:1` | 12 | `registry.yaml` ↔ `.opencode/agent/*` ↔ `domain/rooms/*/agents/*` — 1:1 check | 0 on PASS |
| `count_sync.py:1` | 12/13 | derived vs declared (registry meta) vs textual claims (AGENTS.md) vs disk | 0 on PASS |
| `evidence_guard.py:1` | 4 | every `file:line` citation in the codebase resolves to a real file:line | 0 + 0 broken |
| `sofi-audit.py:1` | 12 | **Unified wrapper** — chains `registry_guard` + `count_sync` for pre-commit | 0 on PASS |
| `sofi-security-scanner.py:1` | 8/15 | Periodic security scan — `gitleaks` + `evidence_guard` combined | 0 on PASS |
| `law13_path_guard.py` | 13 | every cited path has a home (advisory) | advisory |
| `memory_summarizer.py:1` | P-06.7 | when `hippocampus >800` or `amygdala >600` — keep last 5 + summarize | n/a |
| `port-agents.mjs:6` | 12 | dynamic generation of `.opencode/agent/` from `registry.yaml` | n/a |
| `hooks/pre-commit:1` | 4/8/12 | the pre-commit chain (installed via `hooks/install.sh`) | 0 to commit |
| `hooks/install.sh` | — | installs the pre-commit hook into `.git/hooks/pre-commit` | 0 |
| `privileges-required.sh` | — | least-privilege guard for engine scripts | 0 |
| `__pycache__/` | — | Python bytecode (gitignored) | — |
| `docker/` (retired) | — | historical Docker config (removed in R6) | — |

---

## The pre-commit chain (5 stages)

Source: `hooks/pre-commit:1`. Run automatically on every `git commit` (after `install.sh`).

1. **gitleaks** — `gitleaks git --staged --pre-commit --config gitleaks.toml --no-banner --redact` →
   exit 0 + "no leaks found"
2. **sofi-audit** (unified wrapper) — chains `registry_guard --strict` + `count_sync` → exit 0 + zero pending
3. **evidence_guard --staged --strict** — every `file:line` in staged files resolves → exit 0 + 0 broken
4. **law13_path_guard** — every cited path has a home → advisory (prints top paths but does not block)
5. **License advisory** — if `composer.json` / `pubspec.yaml` / `package.json` / `*.lock` changed → reminds to
   fill `License-check: [allowed/rejected]` task-card field via `sec-license-auditor` (Law 15)

**Skip with:** `git commit --no-verify` (use sparingly — only in emergencies with CEO approval).

---

## The 3 baselines (in the guards)

> These constants are bumped +1 each time a new room / agent / skill is added. They're the
> machine-checked "ground truth" that the disk matches the constitution.

| Guard | Constant | Current value (2026-09-05) |
|-------|-----------|---------------------------|
| `registry_guard.py:20` | `SKILLS_BASELINE` | 116 (Audit-ALL-Phase3 — loc-rtl + inn-exp + war-runbook) |
| `count_sync.py:22` | `SKILLS_BASELINE` | 116 |
| `count_sync.py:23` | `AGENTS_HDR_REQUIRED` | `(17, 121)` |

When you add a new skill: bump `SKILLS_BASELINE` in **both** files. When you add a new agent: bump
`AGENTS_HDR_REQUIRED` in `count_sync.py` (17 rooms + new count) + `meta.total_agents` in
`registry.yaml` + `AGENTS.md:62,256` + `room-priority.yaml:11`.

---

## The PENDING-PHASE-B mechanism (what "zero pending" means)

Each guard maintains a **temporary stopgap** (PENDING-PHASE-B) that warns on:
- **Stale `system-state-current.md`** claims (mentions "15 rooms · 114 agents" without "historical" marker)
- **Stale `INDEX.md` skill stamp** (doesn't match `SKILLS_BASELINE`)
- **Extra capsule directories** in `domain/rooms/` not in `registry.yaml`
- **Missing capsules** for agents in `registry.yaml`

**Zero pending** = all of the above clean. After Audit-ALL-Phase3: **zero pending warnings**.
Any future drift that re-introduces a pending item = must be resolved before the next fateful change.

---

## How to run on demand

```bash
# Unified
python3 hq/core/tooling/sofi-audit.py

# Individually
python3 hq/core/tooling/registry_guard.py --strict
python3 hq/core/tooling/count_sync.py
python3 hq/core/tooling/evidence_guard.py hq/core --strict

# Security (advisory on every commit, strict on demand)
gitleaks detect --no-git -v
gitleaks git --staged --pre-commit --config gitleaks.toml

# Pre-commit
bash hq/core/tooling/hooks/pre-commit

# Memory summarizer (P-06.7 — every 10 turns)
python3 hq/core/tooling/memory_summarizer.py
```

---

## When a guard fails — what to do

**`registry_guard` FAIL** — `.opencode/agent/*` drift from `registry.yaml`:
- A new agent file exists in `.opencode/agent/` but isn't in `registry.yaml` → add it (or remove the file)
- An agent is in `registry.yaml` but has no `.opencode/agent/*.md` → create the file
- Capsule missing → create the 3 files in `domain/rooms/<room>/agents/<name>/`

**`count_sync` FAIL** — derived vs declared drift:
- Update `AGENTS.md:62,256` + `registry.yaml:3,11` + `room-priority.yaml:11` to match
- Or update `count_sync.py:23` `AGENTS_HDR_REQUIRED` constant

**`evidence_guard` FAIL** — broken `file:line` citation:
- The error tells you exactly which file:line is broken
- Either fix the citation or remove it
- Run again to verify

**`gitleaks` FAIL** — secret in code:
- **NEVER** commit the secret — remove it
- Use environment variable / vault instead
- Re-stage and commit

---

## See also

- [`hq/core/README.md`](../README.md) — parent
- [`hq/core/nexus/registry.yaml`](../nexus/registry.yaml) — the registry
- [`hq/core/protocols.md:P-11`](../protocols.md) — Tool Protocol
- [`AGENTS.md`](../../../AGENTS.md) — Law 12 + 13
- [Top-level README](../../../README.md)
