#!/usr/bin/env python3
"""FILE: hq/core/tooling/registry_guard.py
Registry guard — Gate-0 mandatory check (Law 12 + Law 13)
Verifies: .opencode/agent/* 1:1 matches hq/core/nexus/registry.yaml (R3.1 dynamic schema)
Core invariants (FAIL-hard): declared counters == derived structure == disk 1:1.
PENDING-PHASE-B group (WARN only): physical capsule migration 08->04 + skills/INDEX stamp.
   Baseline recorded 2026-09-05 (hq/core/archive/r3.1-reconciliation/FINDINGS.md).
   Gap INCREASE -> FAIL now; Phase-B completion (b_complete) -> group becomes FAIL-hard.
Usage: python3 hq/core/tooling/registry_guard.py [--strict]
Exit 1 on any core-invariant mismatch or PENDING-PHASE-B gap increase / post-B drift.
R3.1 (2026-09-05): rooms is a LIST (`- code: ...`) — parse replaced dict-style regex that
   returned 0 rooms; counters are derived (meta vs structure) not hard-coded (brd-ceo verdict ج-4).
"""
from __future__ import annotations
import pathlib, sys, re

ROOT = pathlib.Path(__file__).resolve().parents[3]  # hq/core/tooling -> SOFI root

# ── PENDING-PHASE-B baseline (temporary stopgap per brd-ceo A-verdict ج-1..ج-4; ends when Phase B = "zero WARN left") ──
SKILLS_BASELINE = 113   # observed .opencode/skills/*/SKILL.md at B (2026-09-05) — bumped by qa-laravel-architect
CAP_ROOM_DIRS_EXTRA = 1      # physical 08-data dir pending migration (Phase B)
CAP_MISSING_LEGAL = 6        # arc-* capsule dirs pending 08->04 migration (Phase B)
CAP_EXTRA_DIRS = 12          # dat-* 7 + retired 5 capsule dirs pending archiving (Phase B)

def parse_registry() -> tuple[dict[str, list[str]], dict[str, str], dict[str, int]]:
    """Parse R3.1 list schema (no yaml dep): rooms = list of `- code:` blocks with prefix + `- { name: ... }` entries."""
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

def count_skills() -> int:
    skills_dir = ROOT / ".opencode/skills"
    return sum(1 for d in skills_dir.iterdir() if d.is_dir() and (d / "SKILL.md").exists()) if skills_dir.exists() else 0

def b_complete(legal_rooms: set[str]) -> bool:
    """Phase-B completion probe (Event-Driven per ج-3): zero pending items left.
    True only when 08-data dir gone AND system-state updated to derived counts AND INDEX stamp == disk skills."""
    data_dir_gone = not (ROOT / "hq/core/domain/rooms" / "08-data").exists()
    ssc = ROOT / "hq/core/system-state-current.md"
    ssc_fixed = ssc.exists() and "114 agents" not in ssc.read_text() and "15 rooms" not in ssc.read_text()
    idx = ROOT / ".opencode/skills/INDEX.md"
    idx_fixed = idx.exists() and f"{SKILLS_BASELINE}/{SKILLS_BASELINE}" in idx.read_text()
    return data_dir_gone and ssc_fixed and idx_fixed

def main() -> int:
    strict = "--strict" in sys.argv
    agents_dir = ROOT / ".opencode/agent"
    rooms, prefix_by_room, meta = parse_registry()

    derived_rooms = len(rooms)
    derived_agents = sum(len(a) for a in rooms.values())
    declared_rooms = meta.get("total_rooms")
    declared_agents = meta.get("total_agents")

    expected = set()
    for room, agents in rooms.items():
        prefix = prefix_by_room.get(room, room.split("-", 1)[0])
        for a in agents:
            expected.add(f"{prefix}-{a}.md")
    disk = set(p.name for p in agents_dir.glob("*.md")) if agents_dir.exists() else set()
    missing = sorted(expected - disk)
    extra = sorted(disk - expected)

    print(f"═══ registry_guard ═══")
    print(f"declared: rooms={declared_rooms} agents={declared_agents} · derived: rooms={derived_rooms} agents={derived_agents} · disk agents={len(disk)}")

    fails: list[str] = []
    if declared_rooms != derived_rooms:
        fails.append(f"meta.total_rooms={declared_rooms} != derived rooms={derived_rooms} (structure mismatch)")
    if declared_agents != derived_agents:
        fails.append(f"meta.total_agents={declared_agents} != derived agents={derived_agents} (structure mismatch)")
    if missing:
        fails.append(f"MISSING {len(missing)} agent file(s) vs registry:")
        for f in missing:
            fails.append(f"  - {f}")
    if extra:
        fails.append(f"EXTRA {len(extra)} agent file(s) not in registry:")
        for f in extra:
            fails.append(f"  - {f}")

    # ── PENDING-PHASE-B group (WARN unless gap grew or Phase B complete) ──
    done = b_complete(set(rooms))
    capsule_root = ROOT / "hq/core/domain/rooms"
    room_dirs = sorted(d.name for d in capsule_root.iterdir() if d.is_dir()) if capsule_root.exists() else []
    legal_room_set = set(rooms)
    extra_rooms = sorted(set(room_dirs) - legal_room_set)
    legal_caps = set()
    for r, agents in rooms.items():
        prefix = prefix_by_room.get(r, r.split("-", 1)[0])
        for a in agents:
            legal_caps.add(f"{r}/{prefix}-{a}")
    present_caps: set[str] = set()
    for r in room_dirs:
        ad = capsule_root / r / "agents"
        if not ad.is_dir():
            continue
        for c in ad.iterdir():
            if c.is_dir():
                present_caps.add(f"{r}/{c.name}")
    capsule_missing = sorted(legal_caps - present_caps)
    capsule_extra = sorted(present_caps - legal_caps)
    disk_skills = count_skills()

    cap_grow = (len(extra_rooms) > CAP_ROOM_DIRS_EXTRA or len(capsule_missing) > CAP_MISSING_LEGAL
                or len(capsule_extra) > CAP_EXTRA_DIRS)
    skill_grow = disk_skills > SKILLS_BASELINE
    pending: list[str] = []
    if extra_rooms or capsule_missing or capsule_extra or disk_skills != SKILLS_BASELINE:
        pending.append(
            f"PENDING-PHASE-B [capsules] rooms-extra={len(extra_rooms)}/{CAP_ROOM_DIRS_EXTRA} · missing-legal={len(capsule_missing)}/{CAP_MISSING_LEGAL}"
            f" · extra-dirs={len(capsule_extra)}/{CAP_EXTRA_DIRS}"
        )
        pending.append(f"PENDING-PHASE-B [skills] disk={disk_skills} baseline={SKILLS_BASELINE} (INDEX.md stamp 109 stale — Phase B)")
    if done:
        if extra_rooms or capsule_missing or capsule_extra:
            fails.append(f"Phase B complete — capsule drift must be zero (rooms-extra={len(extra_rooms)} · missing={len(capsule_missing)} · extra={len(capsule_extra)})")
        if disk_skills != SKILLS_BASELINE:
            fails.append(f"Phase B complete — skills must match baseline ({disk_skills} != {SKILLS_BASELINE})")
    elif cap_grow:
        fails.append(f"PENDING-PHASE-B gap increased (capsules) — rooms-extra={len(extra_rooms)} · missing={len(capsule_missing)} · extra={len(capsule_extra)} > baseline")
    elif skill_grow:
        fails.append(f"PENDING-PHASE-B gap increased (skills) — disk={disk_skills} > baseline {SKILLS_BASELINE}")

    if pending and not fails:
        for p in pending:
            print(f"⚠ {p}")

    if fails:
        print("\n".join(fails))
        print(f"\n✖ registry_guard FAILED — Gate-0 blocked (strict={strict})")
        return 1
    print(f"✔ registry_guard PASS — registry {declared_rooms} rooms · {declared_agents} agents · .opencode/agent {len(disk)}/{len(expected)} 1:1"
          + (" · PENDING-PHASE-B WARN active" if pending else " · zero pending"))
    return 0

if __name__ == "__main__":
    sys.exit(main())