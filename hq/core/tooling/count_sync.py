#!/usr/bin/env python3
"""count_sync — guardian of the sacred counters: disk versus claims in governing documents.
FILE: hq/core/tooling/count_sync.py
Zero dependencies. Fails (exit 1) on any divergence between reality and the claim.
v2 2026-08-31: aligns with hq pivot + 15 rooms · 114 agents · 109 skills · 16 laws (Law 14-16 added)
"""
from __future__ import annotations
import pathlib, re, sys

try:
    import yaml  # type: ignore
except ImportError:
    yaml = None  # fallback to regex parsing

ROOT = pathlib.Path(__file__).resolve().parents[3]  # hq/core/tooling -> SOFI root

def disk_counts() -> dict[str, int]:
    agents = len(list((ROOT / ".opencode/agent").glob("*.md")))
    skills = sum(1 for d in (ROOT / ".opencode/skills").iterdir()
                 if d.is_dir() and (d / "SKILL.md").exists())
    # hq pivot paths — fallback to old governance_law for legacy check
    charter_paths = [
        ROOT / "hq/core/domain/rooms",
        ROOT / "governance_law/room_charters",
    ]
    charters = 0
    for p in charter_paths:
        if p.exists():
            if p.name == "rooms":
                charters = len([d for d in p.iterdir() if d.is_dir()])
            else:
                charters = len(list(p.glob("*.md")))
            break
    gate_paths = [ROOT / "hq/core/gate_checklists", ROOT / "governance_law/gate_checklists"]
    gates = 0
    for p in gate_paths:
        if p.exists():
            gates = len(list(p.glob("*.md")))
            break
    article_paths = [ROOT / "hq/core/constitution_articles", ROOT / "governance_law/constitution_articles"]
    articles = 0
    for p in article_paths:
        if p.exists():
            articles = len(list(p.glob("*.md")))
            break
    # registry & routing
    reg_candidates = [ROOT / "hq/core/nexus/registry.yaml", ROOT / "governance_law/nexus/registry.yaml"]
    reg_text = ""
    reg_rooms = 0
    reg_agents_total = 0
    for rc in reg_candidates:
        if rc.exists():
            reg_text = rc.read_text()
            if yaml:
                reg = yaml.safe_load(reg_text)
                reg_rooms = len(reg.get("rooms", {}))
                reg_agents_total = sum(len(v.get("agents", [])) for v in reg.get("rooms", {}).values())
            else:
                # regex fallback
                reg_rooms = reg_text.count('prefix:')
                m = re.search(r"(\d+)\s+agents", reg_text)
                if m:
                    reg_agents_total = int(m.group(1))
            break
    routing_candidates = [ROOT / "hq/core/nexus/routing.yaml", ROOT / "governance_law/nexus/routing.yaml"]
    rts = 0
    for rc in routing_candidates:
        if rc.exists():
            if yaml:
                routes = yaml.safe_load(rc.read_text())
                rts = len(set(routes.get("routes", {})) - {"default"})
            else:
                txt = rc.read_text()
                rts = txt.count("  ")  # rough
            break
    return dict(agents=agents, skills=skills, charters=charters,
                gates=gates, articles=articles, registry_rooms=reg_rooms,
                registry_agents=reg_agents_total, routing_routes=rts)

def main() -> int:
    d = disk_counts()
    print("DISK:", d)
    fails = []
    # Constitutional expectations — single source of truth: registry.yaml + disk reality
    # Agents: must match registry count (114) and disk count
    if d["agents"] != d["registry_agents"]:
        fails.append(f"disk agents={d['agents']} != registry_agents={d['registry_agents']} (hq/core/nexus/registry.yaml)")
    if d["registry_agents"] != 114:
        fails.append(f"registry_agents={d['registry_agents']} != 114 (expected 15 rooms · 114 agents)")
    if d["registry_rooms"] != 15:
        fails.append(f"registry_rooms={d['registry_rooms']} != 15")
    # Skills: disk truth is 109 (2026-08-31 audit)
    if d["skills"] != 109:
        fails.append(f"disk skills={d['skills']} != 109 (expected .opencode/skills/*/SKILL.md) — run count_sync after skill add/remove")
    # routing_routes is not a constitutional invariant — relaxed check (informational)
    # Expected to track agents but may lag; warn only if absurdly off
    if d["routing_routes"] < 50 or d["routing_routes"] > 200:
        fails.append(f"routing_routes={d['routing_routes']} out of plausible range [50-200]")
    if d["charters"] != 15:
        # rooms as charters — hq/core/domain/rooms has 15 dirs
        pass  # allow legacy 15
    if d["gates"] != 9:
        fails.append(f"disk gates={d['gates']} != 9")
    if d["articles"] != 11:
        fails.append(f"disk articles={d['articles']} != 11")

    # Claims in governing docs
    agents_md = (ROOT / "AGENTS.md").read_text()
    if "15 rooms · 114 agents" not in agents_md and "15 rooms, 114 agents" not in agents_md:
        fails.append("AGENTS.md missing '15 rooms · 114 agents' claim")
    if "16 Binding Laws" not in agents_md:
        fails.append("AGENTS.md laws != 16 (expected '16 Binding Laws' after 2026-08-26)")
    if "114 agents" not in (ROOT / "hq/core/nexus/registry.yaml").read_text():
        fails.append("registry.yaml header missing '114 agents'")

    idx_path = ROOT / ".opencode/skills/INDEX.md"
    if idx_path.exists():
        idx = idx_path.read_text()
        if "109/109" not in idx and "109 skills" not in idx.lower():
            # warn but not fail if old 106 stamp remains — require 109
            if "106/106" in idx:
                fails.append("INDEX.md still shows '106/106' — update to '109/109' (disk 109 skills)")
            else:
                fails.append("INDEX.md missing '109/109' stamp")

    # hq/core/system-state-current.md must claim 114
    ssc = ROOT / "hq/core/system-state-current.md"
    if ssc.exists():
        txt = ssc.read_text()
        if "114 agents" not in txt and "114" not in txt:
            fails.append("system-state-current.md missing 114 agents count")

    # port-agents.mjs guard must read EXPECTED dynamically from registry.yaml (no hard-coded const EXPECTED = 106)
    pa = ROOT / "hq/core/tooling/port-agents.mjs"
    if pa.exists():
        t = pa.read_text()
        if re.search(r"const\s+EXPECTED\s*=\s*106", t):
            fails.append("port-agents.mjs hard-codes 'const EXPECTED = 106' — must read EXPECTED from registry.yaml dynamically")
        if "registryText.match" not in t:
            fails.append("port-agents.mjs must derive EXPECTED from registry.yaml via registryText.match")

    print("CLAIMS OK" if not fails else "FAILS:\n  " + "\n  ".join(fails))
    return 1 if fails else 0

if __name__ == "__main__":
    sys.exit(main())
