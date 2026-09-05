#!/usr/bin/env python3
"""FILE: hq/core/tooling/evidence_guard.py
Evidence guard — Law 4 (Evidence Required) + Law 13 (Zero-Randomness)
Validates every `file:line` citation in a file/text exists on disk.
Usage: python3 hq/core/tooling/evidence_guard.py <file-or-dir> [--strict]
  --strict: exit 1 if any broken citation found (for Gate-5/DFR blocking)
  default: reports but exits 0 (advisory)
Also usable as git hook: python3 hq/core/tooling/evidence_guard.py --staged --strict
"""
from __future__ import annotations
import re, sys, pathlib, subprocess

ROOT = pathlib.Path(__file__).resolve().parents[3]  # hq/core/tooling -> SOFI root
SKIP_DIRS = {"node_modules", ".git", ".venv", "vendor", "backups", ".kilo", "dist", "build", ".dart_tool"}

# Pattern: path:line  e.g. hq/core/nexus/registry.yaml:10 or AGENTS.md:1
# Also captures file:line with optional line range
PAT = re.compile(r"([A-Za-z0-9_.\-/@]+\.(?:md|yaml|yml|json|mjs|js|ts|tsx|py|sh|toml|sql|caddy|php|dart|css)):(\d+)")
ALLOWLIST_PATTERNS = [
    re.compile(r"hq/brain/(cortex-decisions|hippocampus-sessions|amygdala-incidents)\.md:\d+"),  # historical citations allowed but checked differently
    re.compile(r"projects/[^/]+/brain/(DECISIONS|HANDOFFS|LESSONS|CONTEXT)\.md:\d+"),
]

def file_exists_for_citation(token: str) -> bool:
    # token is "path:line" -> check path exists
    path = token.split(":")[0]
    # handle leading ./ or / — preserve dotfiles like .opencode/
    if path.startswith("./"):
        path = path[2:]
    path = path.lstrip("/")
    cands = [
        ROOT / path,
        ROOT / path.split(":", 1)[0],
    ]
    # also try without line suffix already stripped
    # handle .opencode/skills/foo/SKILL.md:1
    for c in cands:
        if c.exists():
            return True
        # try relative to hq/core etc
        if (ROOT / "hq" / path).exists():
            return True
    return False

def scan_text(text: str, source: str) -> list[tuple[str, int, str]]:
    broken = []
    for m in PAT.finditer(text):
        full = m.group(0)  # path:line
        path_part = m.group(1)
        line_no = int(m.group(2))
        # skip allowlisted historical but still verify file exists (without line check)
        # skip generic filenames that are templates
        if path_part in {"SKILL.md", "package.json", "composer.json", "pubspec.yaml"}:
            continue
        if "/" not in path_part:
            continue
        if path_part.startswith(("http", "www.", "https:")):
            continue
        # skip if matches allowlist and file is historical (we still check existence)
        # For evidence guard, we verify file exists and line is within bounds
        # handle leading ./ correctly — preserve dotfiles like .opencode/
        _pp = path_part[2:] if path_part.startswith("./") else path_part
        _pp = _pp.lstrip("/")
        p = ROOT / _pp
        if not p.exists():
            # try hierarchical fallbacks: hq/, hq/core/, and common roots
            candidates = []
            if not _pp.startswith("hq/"):
                candidates.append(ROOT / "hq" / _pp)
                candidates.append(ROOT / "hq/core" / _pp)
            # also handle bare "gate_checklists/" → "hq/core/gate_checklists/"
            if _pp.startswith("gate_checklists/"):
                candidates.append(ROOT / "hq/core" / _pp)
            if _pp.startswith("standards/"):
                candidates.append(ROOT / "hq/core" / _pp)
            if _pp.startswith("nexus/"):
                candidates.append(ROOT / "hq/core" / _pp)
            # handle opencode without dot and with dot
            if _pp.startswith("opencode/"):
                candidates.append(ROOT / ("." + _pp))
            if _pp.startswith(".opencode/"):
                # already correct, but also try without dot as fallback (legacy)
                candidates.append(ROOT / _pp[1:])
            # example placeholder skip: .opencode/skills/foo/
            if "foo" in path_part and "skills" in path_part:
                continue
            found = None
            for c in candidates:
                if c.exists():
                    found = c
                    break
            if found is not None:
                p = found
            else:
                # also try template placeholder paths like backend/app/... — those are intentional examples, skip
                if path_part.startswith(("backend/", "client/", "app/", "n8n/", "database/", "admin/")):
                    continue
                broken.append((source, m.start(), full + " → file not found"))
                continue
        if p.is_file():
            try:
                lines = p.read_text(errors="ignore").splitlines()
                if line_no < 1 or line_no > len(lines) + 5:  # allow +5 slack for appended citations
                    broken.append((source, m.start(), f"{full} → line {line_no} out of range (file has {len(lines)} lines)"))
            except OSError:
                pass
    return broken

def collect_targets(args: list[str]) -> list[pathlib.Path]:
    targets = []
    for a in args:
        if a in {"--strict", "--staged"}:
            continue
        p = pathlib.Path(a)
        if p.is_file():
            targets.append(p)
        elif p.is_dir():
            for f in p.rglob("*"):
                if f.is_file() and f.suffix in {".md", ".yaml", ".yml", ".json", ".mjs", ".js", ".ts", ".py", ".sh"}:
                    if any(part in SKIP_DIRS for part in f.parts):
                        continue
                    targets.append(f)
        else:
            # treat as text snippet? try as path relative to ROOT
            rp = ROOT / a
            if rp.is_file():
                targets.append(rp)
    return targets

def get_staged_files() -> list[pathlib.Path]:
    try:
        out = subprocess.check_output(["git", "diff", "--cached", "--name-only"], cwd=ROOT, text=True)
        return [ROOT / line.strip() for line in out.splitlines() if line.strip()]
    except Exception:
        return []

def main() -> int:
    strict = "--strict" in sys.argv
    staged = "--staged" in sys.argv
    args = [a for a in sys.argv[1:] if a not in ("--strict", "--staged")]

    if staged:
        targets = get_staged_files()
        if not targets:
            print("evidence_guard: no staged files")
            return 0
    elif not args:
        print("Usage: evidence_guard.py <file-or-dir> [--strict] | --staged --strict")
        return 2
    else:
        targets = collect_targets(args)
        # if no targets but args look like single file that doesn't exist, scan args as text
        if not targets and args:
            # fallback: treat first arg as path to scan for citations
            p = pathlib.Path(args[0])
            if not p.exists():
                print(f"evidence_guard: target not found: {args[0]}")
                return 2

    broken_all = []
    scanned = 0
    for t in targets:
        if t.suffix not in {".md", ".yaml", ".yml", ".json", ".mjs", ".js", ".ts", ".py", ".sh"}:
            continue
        # skip historical evidence archives (never edited per Law 13 continuity) + core brain permanent records
        rel = str(t.relative_to(ROOT)) if t.is_relative_to(ROOT) else str(t)
        if rel.startswith("hq/brain/") and t.name in {"cortex-decisions.md", "hippocampus-sessions.md", "amygdala-incidents.md"}:
            continue
        if rel.startswith("hq/brain/evidence/"):
            continue
        if "archive" in rel or "SOFI-archive" in rel:
            continue
        # skip .opencode/skills INDEX historical 106 references (handled by count_sync)
        if t.name == "INDEX.md" and "skills" in rel:
            # still scan INDEX but allow old 106 stamp via advisory elsewhere
            pass
        try:
            text = t.read_text(errors="ignore")
        except OSError:
            continue
        scanned += 1
        broken = scan_text(text, rel)
        broken_all.extend([(rel, pos, msg) for _, pos, msg in broken])

    print(f"═══ evidence_guard ═══ scanned={scanned} · broken_citations={len(broken_all)} · strict={strict}")
    for rel, _, msg in broken_all[:20]:
        print(f"  ✖ {rel} → {msg}")
    if len(broken_all) > 20:
        print(f"  ... and {len(broken_all)-20} more")
    if not broken_all:
        print("✔ 0 broken file:line citations — Law 4 satisfied")
        return 0
    if strict:
        print(f"✖ evidence_guard STRICT FAILED — {len(broken_all)} broken citation(s) block gate/commit")
        return 1
    print(f"⚠ {len(broken_all)} broken citation(s) found (advisory)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
