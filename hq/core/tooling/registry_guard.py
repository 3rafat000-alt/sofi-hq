#!/usr/bin/env python3
"""FILE: hq/core/tooling/registry_guard.py
Registry guard — Gate-0 mandatory check (Law 12 + Law 13)
Verifies: .opencode/agent/* 1:1 matches hq/core/nexus/registry.yaml (15 rooms · 114 agents)
         + .opencode/skills/*/SKILL.md matches SKILLS-ASSIGNMENT.md
Usage: python3 hq/core/tooling/registry_guard.py [--strict]
Exit 1 on any mismatch — blocks Gate-0 (and any gate that includes it).
"""
from __future__ import annotations
import pathlib, sys, re

ROOT = pathlib.Path(__file__).resolve().parents[3]  # hq/core/tooling -> SOFI root

def load_registry_agents() -> tuple[set[str], dict[str, list[str]]]:
    text = (ROOT / "hq/core/nexus/registry.yaml").read_text()
    # Extract rooms -> agents via simple parse (no yaml dep)
    rooms: dict[str, list[str]] = {}
    current = None
    for line in text.splitlines():
        m_room = re.match(r'\s+"(\d+-.+?)":', line)
        if m_room:
            current = m_room.group(1)
            rooms[current] = []
        m_agents = re.search(r'agents:\s*\[(.+?)\]', line)
        if m_agents and current:
            agents = [a.strip() for a in m_agents.group(1).split(",") if a.strip()]
            rooms[current] = agents
    # Build expected filenames: <prefix>-<agent>.md
    # prefix map from registry header
    prefix_map = {}
    for room_key, agents in rooms.items():
        # room_key like "00-boardroom" -> prefix via registry explicit block
        pass
    # Simpler: actual disk names are <prefix>-<agent>.md where prefix derived from registry "prefix:" lines
    # Parse prefix per room
    prefix_by_room = {}
    cur = None
    for line in text.splitlines():
        mr = re.match(r'\s+"(\d+-.+?)":', line)
        if mr:
            cur = mr.group(1)
        mp = re.match(r'\s+prefix:\s+(\w+)', line)
        if mp and cur:
            prefix_by_room[cur] = mp.group(1)
    expected = set()
    for room, agents in rooms.items():
        prefix = prefix_by_room.get(room, "")
        for a in agents:
            expected.add(f"{prefix}-{a}.md")
    return expected, rooms

def main() -> int:
    strict = "--strict" in sys.argv
    agents_dir = ROOT / ".opencode/agent"
    expected, rooms = load_registry_agents()
    disk = set(p.name for p in agents_dir.glob("*.md")) if agents_dir.exists() else set()

    print(f"═══ registry_guard ═══")
    print(f"registry rooms: {len(rooms)} · expected agents: {len(expected)} · disk agents: {len(disk)}")

    missing = sorted(expected - disk)
    extra = sorted(disk - expected)

    fails = []
    if missing:
        fails.append(f"MISSING {len(missing)} agent file(s) vs registry:")
        for f in missing:
            fails.append(f"  - {f}")
    if extra:
        fails.append(f"EXTRA {len(extra)} agent file(s) not in registry:")
        for f in extra:
            fails.append(f"  - {f}")
    if len(expected) != 114:
        fails.append(f"registry total {len(expected)} != 114 (AGENTS.md:15 rooms · 114 agents)")

    # Skill check: SKILLS-ASSIGNMENT vs disk
    skills_dir = ROOT / ".opencode/skills"
    disk_skills = set(d.name for d in skills_dir.iterdir() if d.is_dir() and (d / "SKILL.md").exists()) if skills_dir.exists() else set()
    assignment = ROOT / "hq/core/domain/SKILLS-ASSIGNMENT.md"
    if assignment.exists():
        assigned = set()
        for line in assignment.read_text().splitlines():
            if not line.startswith("|"):
                continue
            if "SKILL.md" in line or "derived" in line.lower():
                continue
            parts = [p.strip() for p in line.split("|")]
            if len(parts) < 2 or not parts[1]:
                continue
            skill = parts[1].strip()
            if not skill or skill == "---" or set(skill) <= {"-", " "}:
                continue
            if skill.startswith("derived") or skill.startswith("---"):
                continue
            assigned.add(skill)
        # assigned currently only ~50 explicit — full list is in .opencode/skills itself
        # So we check that every assigned skill exists on disk
        missing_skills = sorted(assigned - disk_skills)
        if missing_skills:
            fails.append(f"SKILLS-ASSIGNMENT entries missing on disk ({len(missing_skills)}): {', '.join(missing_skills[:10])}")

    # Capsule check: every registry agent must have a capsule dir
    capsule_root = ROOT / "hq/core/domain/rooms"
    capsule_missing = []
    for room_key, agents in rooms.items():
        for a in agents:
            prefix = ""
            # find prefix for room
            txt = (ROOT / "hq/core/nexus/registry.yaml").read_text()
            cur = None
            for line in txt.splitlines():
                if f'"{room_key}"' in line:
                    cur = room_key
                if cur == room_key:
                    m = re.match(r'\s+prefix:\s+(\w+)', line)
                    if m:
                        prefix = m.group(1)
                        break
            agent_id = f"{prefix}-{a}"
            capsule = capsule_root / room_key / "agents" / agent_id
            if not capsule.exists():
                capsule_missing.append(str(capsule.relative_to(ROOT)))
    if capsule_missing:
        fails.append(f"CAPSULE missing {len(capsule_missing)} agent capsule(s):")
        for c in capsule_missing[:10]:
            fails.append(f"  - {c}")
        if len(capsule_missing) > 10:
            fails.append(f"  ... and {len(capsule_missing)-10} more")

    print(f"capsules checked: {114 - len(capsule_missing)}/{114} present")

    if fails:
        print("\n".join(fails))
        print(f"\n✖ registry_guard FAILED — Gate-0 blocked (strict={strict})")
        return 1
    else:
        print("✔ registry_guard PASS — .opencode/agent ↔ registry.yaml 114/114 · capsules OK · skills OK")
        return 0

if __name__ == "__main__":
    sys.exit(main())
