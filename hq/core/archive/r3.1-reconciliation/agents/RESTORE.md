# RESTORE — R3.1 Reconciliation Archive (agents)

**FILE: hq/core/archive/r3.1-reconciliation/agents/RESTORE.md**
**Purpose:** the exact reversal procedure for any archived agent (Law 14 / Phase-B un-archiving).
**Only brd-ceo (or the Phase-B releaser named in MANIFEST.md) may authorize restoration.**

## Restore a single agent (e.g. `dat-lead`)

```bash
# 1) move back into the live agent directory
mv hq/core/archive/r3.1-reconciliation/agents/dat-lead.md .opencode/agent/dat-lead.md
# 2) verify hash integrity against MANIFEST.md (must equal the recorded sha256)
sha256sum .opencode/agent/dat-lead.md
# 3) registry.yaml must regain the corresponding entry; meta.total_agents must be updated;
#    guards (registry_guard/count_sync) will then demand a matching disk file — run them:
python3 hq/core/tooling/registry_guard.py && python3 hq/core/tooling/count_sync.py
# 4) commit with evidence (sofi-handoff + sofi-evidence)
```

## Restore ALL 7 (rollback of Phase A archival)

```bash
for f in dat-lead dsn-content-strategist dsn-motion-designer fnt-vue-engineer \
         res-data-researcher res-web-scout qa-flutter-architect; do
  mv hq/core/archive/r3.1-reconciliation/agents/$f.md .opencode/agent/$f.md
done
# verify each sha256 against MANIFEST.md, then update registry.yaml (if the 6 dat→arc renames
# must also be undone: git mv .opencode/agent/arc-*.md back to dat-*.md + revert identity lines)
```

## Constraints
- **qa-flutter-architect** may never be restored without a registry entry added first (Law 12) and brd-ceo approval — currently it is an illegitimate record.
- **fnt-vue-engineer** cannot return while Stack Lock R3.1 bans Vue.js — a later owner order is required.
- Restored files count against `meta.total_agents`; guards fail loudly on any mismatch (Law 12).