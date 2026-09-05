#!/usr/bin/env python3
"""FILE: hq/core/tooling/count_sync.py
Count sync — guardian of the sacred counters.
Verifies derived structure counts (R3.1 list schema) against declared meta in
hq/core/nexus/registry.yaml and textual claims in AGENTS.md (against derived, not reverse,
per brd-ceo verdict ج-4), plus disk agent count 1:1.
PENDING-PHASE-B group (WARN only): system-state-current.md (15 rooms · 114 agents — stale)
and .opencode/skills/INDEX.md stamp; gap increase -> FAIL (Phase-B baseline in FINDINGS.md).
Demoted to informational: legacy gate_checklists/constitution_articles/charters/laws trees
(external to the R3.1 schema pivot; not part of this work order).
Usage: python3 hq/core/tooling/count_sync.py [--strict]
Exit 1 on core drift / declared-vs-derived mismatch / PENDING-PHASE-B gap increase / post-B drift.
v3 2026-09-05: R3.1 list-schema parse (reg is now a list of rooms — the old reg["rooms"].values()
call crashed with AttributeError at runtime, breaking the whole tool).
"""
from __future__ import annotations
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[3]

# ── PENDING-PHASE-B baseline (temporary stopgap; ends when Phase B = "zero WARN left") ──
SKILLS_BASELINE = 113          # observed .opencode/skills/*/SKILL.md at B (2026-09-05) — bumped by qa-laravel-architect
AGENTS_HDR_REQUIRED = (17, 121)  # R3.1 + Audit-ALL-Phase2 — 17 rooms · 121 agents — Localization 08 + Innovation 16 added

def parse_registry() -> tuple[dict[str, list[str]], dict[str, str], dict[str, int]]:
    """No-yaml parse matching registry_guard.py — one source of parsing truth (Law 12 consistency)."""
    text = (ROOT / "hq/core/nexus/registry.yaml").read_text()
    rooms: dict[str, list[str]] = {}
    prefix_by_room: dict[str, str] = {}
    current = ""
    for line in text.splitlines():
        mr = re.match(r"^\s*-\s+code:\s+(\d+-[\w-]+)\s*$", line)
        if mr:
            room_code = mr.group(1) or ""
            if not room_code:
                continue
            current = room_code
            rooms.setdefault(current, [])
            continue
        mp = re.match(r"^\s+prefix:\s+(\w+)\s*$", line)
        if mp and current:
            prefix_by_room[current] = mp.group(1)
            continue
        ma = re.match(r"^\s*-\s+\{\s*name:\s*([\w-]+)", line)
        if ma and current:
            rooms[current].append(ma.group(1))
    meta: dict[str, int] = {}
    for key, pat in (("total_rooms", r"^\s*total_rooms:\s*(\d+)\s*$"),
                     ("total_agents", r"^\s*total_agents:\s*(\d+)\s*$")):
        m = re.search(pat, text, re.M)
        if m:
            meta[key] = int(m.group(1))
    return rooms, prefix_by_room, meta

def count_files(directory: str, suffix: str = ".md") -> int:
    d = ROOT / directory
    return len(list(d.glob(f"*{suffix}"))) if d.exists() else 0

def count_skills() -> int:
    skills_dir = ROOT / ".opencode/skills"
    return sum(1 for d in skills_dir.iterdir() if d.is_dir() and (d / "SKILL.md").exists()) if skills_dir.exists() else 0

def b_complete() -> bool:
    """Phase-B completion probe (Event-Driven per ج-3): 08-data dir gone + system-state updated + INDEX stamp == disk skills."""
    data_dir_gone = not (ROOT / "hq/core/domain/rooms" / "08-data").exists()
    ssc = ROOT / "hq/core/system-state-current.md"
    ssc_fixed = ssc.exists() and "114 agents" not in ssc.read_text() and "15 rooms" not in ssc.read_text()
    idx = ROOT / ".opencode/skills/INDEX.md"
    idx_fixed = idx.exists() and f"{SKILLS_BASELINE}/{SKILLS_BASELINE}" in idx.read_text()
    return data_dir_gone and ssc_fixed and idx_fixed

def main() -> int:
    rooms, prefix_by_room, meta = parse_registry()
    derived_rooms = len(rooms)
    derived_agents = sum(len(a) for a in rooms.values())
    declared_rooms = meta.get("total_rooms")
    declared_agents = meta.get("total_agents")
    disk_agents = count_files(".opencode/agent")
    disk_skills = count_skills()
    done = b_complete()

    print("═══ count_sync ═══")
    print(f"derived: rooms={derived_rooms} agents={derived_agents} · declared: {declared_rooms}/{declared_agents} · disk: agents={disk_agents} skills={disk_skills}")

    fails: list[str] = []
    if declared_rooms != derived_rooms:
        fails.append(f"registry meta.total_rooms={declared_rooms} != derived {derived_rooms}")
    if declared_agents != derived_agents:
        fails.append(f"registry meta.total_agents={declared_agents} != derived {derived_agents}")
    if disk_agents != derived_agents:
        fails.append(f"disk .opencode/agent/{disk_agents} != derived {derived_agents} (registry 1:1 violated)")

    # ── AGENTS.md textual claims verified AGAINST derived (not reverse — ج-4) ──
    agents_md = ROOT / "AGENTS.md"
    text = agents_md.read_text()
    claim_rooms_ok = f"{derived_rooms} rooms" in text
    claim_agents_ok = f"{derived_agents} active agents" in text
    laws_ok = "16 Binding Laws" in text
    if not claim_rooms_ok:
        fails.append(f"AGENTS.md missing claim 'f{derived_rooms} rooms'")
    if not claim_agents_ok:
        fails.append(f"AGENTS.md missing claim '{derived_agents} active agents'")
    if not laws_ok:
        fails.append("AGENTS.md missing '16 Binding Laws'")

    # ── PENDING-PHASE-B group (WARN unless gap grew or Phase B complete) ──
    pending: list[str] = []
    ssc = ROOT / "hq/core/system-state-current.md"
    if ssc.exists():
        ssc_text = ssc.read_text()
        if "114 agents" in ssc_text or "15 rooms" in ssc_text:
            pending.append("PENDING-PHASE-B [system-state] stale claims '15 rooms · 114 agents' — Phase-B doc, do not edit now")
    idx = ROOT / ".opencode/skills/INDEX.md"
    if idx.exists():
        idx_text = idx.read_text()
        m = re.search(r"(\d+)\s*/\s*(\d+)", idx_text)
        pending.append(f"PENDING-PHASE-B [skills] disk={disk_skills} baseline={SKILLS_BASELINE} · INDEX stamp={'/'.join(m.groups()) if m else 'none'} (Phase B)")

    if done and (disk_skills != SKILLS_BASELINE or (ssc.exists() and ("114 agents" in ssc.read_text() or "15 rooms" in ssc.read_text()))):
        fails.append("Phase B complete — system-state/skills must match derived reality")
    elif disk_skills > SKILLS_BASELINE:
        fails.append(f"PENDING-PHASE-B gap increased (skills): disk={disk_skills} > baseline {SKILLS_BASELINE}")

    # ── port-agents.mjs must read the count dynamically (ب شرط أ-2 العلية + ج-4) ──
    pa = ROOT / "hq/core/tooling/port-agents.mjs"
    if pa.exists():
        pa_text = pa.read_text()
        if "EXPECTED" in pa_text and "total_agents" not in pa_text:
            fails.append("port-agents.mjs does not read registry meta.total_agents (EXPECTED constant stale?)")

    # ── informational (legacy trees external to this work order) ──
    gates = count_files("hq/core/gate_checklists")
    articles = count_files("hq/core/constitution_articles")
    print(f"info: gate_checklists={gates} · constitution_articles={articles} (informational, not gating)")
    if pa.exists() and "total_agents" in pa.read_text():
        print("info: port-agents.mjs reads meta.total_agents (dynamic ✓)")

    if pending and not fails:
        for p in pending:
            print(f"⚠ {p}")

    if fails:
        print("\n".join(fails))
        print(f"\n✖ count_sync FAILED (strict={'--strict' in sys.argv})")
        return 1
    print(f"✔ count_sync PASS — derived {declared_rooms} rooms · {declared_agents} agents · AGENTS.md claims OK"
          + (" · PENDING-PHASE-B WARN active" if pending else " · zero pending"))
    return 0

if __name__ == "__main__":
    sys.exit(main())