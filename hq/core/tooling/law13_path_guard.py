#!/usr/bin/env python3
"""law13_path_guard — guard of Law 13: every path cited in the living corpus has a real home.

Zero dependencies. Usage: python3 tooling/law13_path_guard.py [--fix-report FILE]
Scans path-like tokens in live files and reports every missing target,
excluding history records (cortex/hippocampus/amygdala + project logs)
and approved convention shortcuts (brain/X.md and sibling names).
"""
from __future__ import annotations
import re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
HIST = {"org_brain/cortex-decisions.md", "org_brain/hippocampus-sessions.md",
        "org_brain/amygdala-incidents.md", "org_brain/handoffs"}
SKIP_DIRS = {"node_modules", ".git", ".venv", "vendor"}
PAT = re.compile(r"(?:[\w@.-]+/)*[\w.-]+\.(?:md|yaml|mjs)\b")
GENERIC = {"SKILL.md", "package.json", "composer.json", "pubspec.yaml"}

def is_history(sp: str) -> bool:
    return sp in HIST or sp.startswith("org_brain/handoffs/") or bool(re.search(r"projects/[^/]+/brain/(DECISIONS|HANDOFFS|LESSONS)\.md$", sp))

def in_scope(p: pathlib.Path) -> bool:
    sp = str(p)
    if p.suffix not in {".md", ".yaml", ".mjs"} or not p.is_file():
        return False
    rel0 = p.relative_to(ROOT)
    rs = str(rel0)
    if any(s in rs for s in SKIP_DIRS) or rs.startswith("projects/sakk"):
        return False
    return not is_history(rs)

def exists_flex(tok: str, here: pathlib.Path) -> bool:
    cands = [ROOT / tok, here / tok, here.parent / tok]
    cands += [ROOT / ".opencode/skills" / tok, here.parent.parent / tok.lstrip('/')]
    if tok.startswith(".opencode/skills/") or (not tok.startswith("/") and (ROOT / ".opencode" / tok).exists()):
        cands.append(ROOT / ".opencode" / tok)
    if tok.startswith("opencode/"):
        cands.append(ROOT / ("." + tok))
    if tok.startswith(".opencode/skills/"):
        cands.append(ROOT / ".opencode/skills" / tok.split("/", 3)[-1])
    return any(c.exists() for c in cands)

def main() -> int:
    problems: dict[str, list[str]] = {}
    scanned = 0
    for p in ROOT.rglob("*"):
        if not in_scope(p):
            continue
        try:
            text = p.read_text(errors="ignore")
        except OSError:
            continue
        scanned += 1
        rel = str(p.relative_to(ROOT))
        for m in PAT.findall(text):
            tok = m.strip(".,;:`")
            if not tok or tok.startswith(("http", "www.", "/reference")) or "raw.githubusercontent" in tok or "/" not in tok:
                continue
            if tok.split("/")[-1] in GENERIC:
                continue
            # Approved convention shortcuts: brain sibling names, project brain/X, nexus/gates.yaml
            if re.fullmatch(r"(CORTEX|HIPPOCAMPUS|AMYGDALA|THALAMUS|BRAIN|PREFRONTAL|BASAL-GANGLIA|TOOLS)\.md", tok):
                continue
            if re.fullmatch(r"brain/(CONTEXT|DECISIONS|HANDOFFS|LESSONS)\.md", tok):
                continue
            if re.fullmatch(r"nexus/(gates|routing|pipeline|registry|models|personas)\.yaml", tok):
                continue
            if re.fullmatch(r"(\w+-skill)/(reference|docs)/[\w.-]+", tok):
                continue
            if re.fullmatch(r"flutter_lints/[\w.-]+", tok):
                continue
            if re.fullmatch(r"(docs|reference)/[\w.-]+", tok) and (p.parent / tok).exists():
                continue
            if not exists_flex(tok, p.parent):
                problems.setdefault(tok, []).append(str(rel))
    print(f"scanned={scanned} · broken_targets={len(problems)}")
    for tok, where in sorted(problems.items(), key=lambda x: -len(x[1]))[:20]:
        print(f"  {len(where):3d}x {tok}  <- {where[0]}")
    if "--fix-report" in sys.argv:
        out = ROOT / "tooling" / "path-guard-report.txt"
        out.write_text("\n".join(f"{tok}\t{','.join(w)}" for tok, w in problems.items()))
        print(f"report -> {out}")
    return 1 if problems else 0

if __name__ == "__main__":
    sys.exit(main())
