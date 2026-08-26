#!/usr/bin/env python3
"""count_sync — guardian of the sacred counters: disk versus claims in governing documents.

Zero dependencies. Fails (exit 1) on any divergence between reality and the claim.
"""
from __future__ import annotations
import pathlib, re, sys, yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent

def disk_counts() -> dict[str, int]:
    agents = len(list((ROOT / ".opencode/agent").glob("*.md")))
    skills = sum(1 for d in (ROOT / ".opencode/skills").iterdir()
                 if d.is_dir() and (d / "SKILL.md").exists())
    charters = len(list((ROOT / "governance_law/room_charters").glob("*.md")))
    gates = len(list((ROOT / "governance_law/gate_checklists").glob("*.md")))
    articles = len(list((ROOT / "governance_law/constitution_articles").glob("*.md")))
    reg = yaml.safe_load((ROOT / "governance_law/nexus/registry.yaml").read_text())
    routes = yaml.safe_load((ROOT / "governance_law/nexus/routing.yaml").read_text())
    rooms = len(reg["rooms"])
    rts = len(set(routes["routes"]) - {"default"})
    return dict(agents=agents, skills=skills, charters=charters,
                gates=gates, articles=articles, registry_rooms=rooms, routing_routes=rts)

def claims() -> list[tuple[str, int, str]]:
    out = []
    agents_md = (ROOT / "AGENTS.md").read_text()
    m = re.search(r"\((\d+) Binding Laws\)", agents_md)
    if m: out.append(("laws", int(m.group(1)), "AGENTS.md"))
    for f, pat in [
        ("AGENTS.md", r"(\d{3}) skills"),
        ("identity/sofi-system-identity.md", r"(\d{3}) skills"),
        (".opencode/skills/INDEX.md", r"(\d{3})/(\d{3})"),
    ]:
        t = (ROOT / f).read_text()
        for mm in re.finditer(pat, t):
            val = int(mm.group(1)) if f != ".opencode/skills/INDEX.md" else int(mm.group(1))
            out.append(("skills", val, f))
            break
    return out

def main() -> int:
    d = disk_counts()
    print("DISK:", d)
    fails = []
    expect = {"agents": 106, "skills": 106, "charters": 15, "gates": 9,
              "articles": 11, "registry_rooms": 15, "routing_routes": 106}
    for k, v in expect.items():
        if d[k] != v:
            fails.append(f"disk {k}={d[k]} != {v}")
    for name, val, src in claims():
        target = d.get(name)
        if target is None:
            continue
        if name == "skills" and src.endswith("INDEX.md"):
            continue  # the 106/106 pattern is checked below
        if val != target:
            fails.append(f"{src}: {name} claim={val} != disk={target}")
    idx = (ROOT / ".opencode/skills/INDEX.md").read_text()
    if "106/106" not in idx:
        fails.append("INDEX.md missing '106/106' stamp")
    laws = (ROOT / "AGENTS.md").read_text()
    if "(13 Binding Laws)" not in laws:
        fails.append("AGENTS.md laws != 13")
    print("CLAIMS OK" if not fails else "FAILS:\n  " + "\n  ".join(fails))
    return 1 if fails else 0

if __name__ == "__main__":
    sys.exit(main())
