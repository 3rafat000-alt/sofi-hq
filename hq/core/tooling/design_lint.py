#!/usr/bin/env python3
"""FILE: hq/core/tooling/design_lint.py
SAKK design-lint — visual identity guard (Visual Identity Standard §3.2 · owner order 2026-08-26)
Law 13 applied to pixels. Bans: raw hex outside token files, shadows, gradients, glow/blur,
colored border classes. Exit 1 on violations when --strict is passed.

Usage:
  python3 design_lint.py <dir> [dir...] [--strict]
Example:
  python3 design_lint.py projects/sakk/apps/site-prototype/src --strict
"""
import re
import sys
from pathlib import Path

SCAN_SUFFIXES = {".tsx", ".ts", ".jsx", ".css"}
SKIP_DIRS = {"node_modules", "dist", ".git", "build"}
ALLOWED_HEX_FILES = re.compile(r"(tailwind\.config\.(?:ts|js)$|@sakk[/\\]ui[/\\]|CookieConsent\.tsx$)")  # CookieConsent: TICKET refactor-to-classes (registered 2026-08-26)
RAW_HEX = re.compile(r"#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b")

RULES = [
    ("SHADOW", re.compile(r"shadow-(?!none)[\w\-]"), "shadow utility — banned (flat doctrine)"),
    ("GRADIENT", re.compile(r"bg-gradient|bg-linear|repeating-linear-gradient|radial-gradient|linear-gradient\("), "gradient — banned (solid fills only; mask-image fade allowed)"),
    ("GLOW", re.compile(r"blur-\[|drop-shadow|backdrop-blur"), "glow/blur — banned"),
    ("COLORED_BORDER", re.compile(r"border-(?:red|amber|emerald|blue|purple|pink|orange|teal|indigo|violet|rose|cyan|sky|lime|green|yellow|fuchsia|wine|gold)-?\d"), "colored border class — neutral ink hairlines only (hover:border-wine-* allowed)"),
]
HOVER_BORDER_ALLOW = "hover:border-wine-"


def iter_files(roots):
    seen = set()
    for root in roots:
        base = Path(root)
        if not base.exists():
            print(f"⚠ path missing: {base}")
            continue
        for p in sorted(base.rglob("*")):
            if p.suffix not in SCAN_SUFFIXES:
                continue
            if any(part in SKIP_DIRS for part in p.parts):
                continue
            rp = str(p.resolve())
            if rp in seen:
                continue
            seen.add(rp)
            yield p


def main():
    args = [a for a in sys.argv[1:] if a != "--strict"]
    strict = "--strict" in sys.argv
    if not args:
        print("usage: design_lint.py <dir> [dir...] [--strict]")
        sys.exit(2)

    violations = []
    files_scanned = 0
    for path in iter_files(args):
        files_scanned += 1
        sp = str(path)
        hex_allowed = bool(ALLOWED_HEX_FILES.search(sp)) or "globals.css" in sp
        try:
            for lineno, line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
                if not hex_allowed and not line.strip().startswith(("*", "/*", "//")):
                    for m in RAW_HEX.finditer(line):
                        violations.append(("RAW_HEX", sp, lineno, m.group(0), line.strip()[:90]))
                for name, rx, why in RULES:
                    if name == "GRADIENT" and "mask-image" in line:
                        continue
                    for m in rx.finditer(line):
                        if name == "COLORED_BORDER" and HOVER_BORDER_ALLOW in line:
                            continue
                        violations.append((name, sp, lineno, m.group(0), line.strip()[:90]))
        except OSError as exc:
            print(f"⚠ unreadable: {path} ({exc})")

    by_rule = {}
    for name, sp, lineno, token, ctx in violations:
        by_rule.setdefault(name, []).append((sp, lineno, token, ctx))

    print(f"═══ design-lint ═══ files scanned: {files_scanned}")
    if not violations:
        print("✔ 0 violations — identity doctrine respected")
        sys.exit(0)

    for name in sorted(by_rule):
        rows = by_rule[name]
        print(f"✖ {name}: {len(rows)}")
        for sp, lineno, token, ctx in rows[:12]:
            print(f"   {sp}:{lineno} → {token}  | {ctx}")
        if len(rows) > 12:
            print(f"   … and {len(rows) - 12} more")
    total = len(violations)
    print(f"TOTAL VIOLATIONS: {total}")
    if strict:
        sys.exit(1)


if __name__ == "__main__":
    main()
