#!/usr/bin/env bash
# FILE: hq/core/tooling/hooks/install.sh
# Installs SOFI pre-commit hook to .git/hooks/pre-commit (versioned source: hq/core/tooling/hooks/pre-commit)
set -e
ROOT="$(git rev-parse --show-toplevel 2>/dev/null)"
if [ -z "$ROOT" ]; then
  ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
fi
SRC="$ROOT/hq/core/tooling/hooks/pre-commit"
DST="$ROOT/.git/hooks/pre-commit"
if [[ ! -f "$SRC" ]]; then echo "✗ source hook not found: $SRC"; exit 1; fi
cp "$SRC" "$DST"
chmod +x "$DST"
echo "✓ installed: $SRC → $DST (executable)"
echo "  Verify: bash .git/hooks/pre-commit (dry run) or git commit --dry-run if supported"
# Also ensure gitleaks.toml exists at root
if [[ ! -f "$ROOT/gitleaks.toml" ]]; then echo "⚠ gitleaks.toml missing at root"; else echo "✓ gitleaks.toml present"; fi
# Sanity run (non-blocking advisory)
bash "$DST" 2>&1 | tail -30 || echo "⚠ hook dry run found issues (see above) — fix before next commit"
