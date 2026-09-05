# `hq/core/archive/` — Historical Archive (Law 13.5)

> The **archive** preserves historical artifacts that are no longer in active use but are kept
> for traceability + old←new maps. Every archived file has a `MANIFEST.md` + a `RESTORE.md`
> + sha256 fingerprints (before == after).

Per **Law 13.5** (zero-randomness), any structural change produces a permanent `old ← new` map
in this directory. The archive is **immutable** — files are added, never modified.

---

## The 3 archive subdirectories

| Subdirectory | Content | Source | Restore via |
|--------------|---------|--------|-------------|
| `legacy-hq-core-agents/` | 108 files — the legacy `hq/core/agents/` tree (R6 archive) | pre-R3.1 duplicate of `.opencode/agent/` | `bash <legacy>/RESTORE.md` |
| `r3.1-reconciliation/` | The R3.1 reconciliation artifacts (Phase A + B closure) | pre-Phase-B | `bash <r3.1>/RESTORE.md` |
| `audit-all-phase3/` | The Audit-ALL-Phase3 archived sources (arc-ml-engineer + arc-privacy-officer) | pre-Phase3 redistribution | `bash <phase3>/RESTORE.md` |

> **Note:** each archived subdirectory has a `MANIFEST.md` (list of files + classification) +
> a `RESTORE.md` (how to restore) + `sha256-before.txt` + `sha256-after.txt` (proving byte-identity).

---

## The restore protocol

To restore an archived file or directory:

```bash
# 1. Read the manifest
cat hq/core/archive/<subdir>/MANIFEST.md

# 2. Verify integrity (sha256 before == after)
diff hq/core/archive/<subdir>/sha256-before.txt hq/core/archive/<subdir>/sha256-after.txt
# Expected: no diff (byte-identity)

# 3. Restore per RESTORE.md
bash hq/core/archive/<subdir>/RESTORE.md

# 4. Update the registry if the restored file adds agents
# (or remove if the restored file removes them)

# 5. Commit atomically — pre-commit enforces all 4 guards
```

**Forbidden:** modifying files inside `archive/` — the archive is **immutable** (Law 13.5).

---

## The R6 archive (legacy-hq-core-agents/)

> Source: `DEC-R6-20260905-ARCHIVE-LEGACY-AGENTS` — 108 files archived from `hq/core/agents/`.

The `hq/core/agents/` tree was a **legacy duplicate** of `.opencode/agent/` (per the registry
invariant — `.opencode/agent/` is the sole source of truth). It was archived to keep the
`hq/core/agents/` directory empty. Restoring would re-introduce the duplication.

**Restore is NOT recommended** — if you need a specific agent, copy it from `.opencode/agent/`.

---

## The R3.1 archive (r3.1-reconciliation/)

> Source: `DEC-R3.3-PHASEB-20260905` — R3.1 reconciliation Phase A + B closure.

This archive contains the reconciliation artifacts from the R3.1 data room merge (08-Data
into 04-Architecture). It includes the dat-* → arc-* rename manifest, the AGENTS.md claim
corrections, and the Phase B acceptance. Restoring would re-introduce the old R3.1 state.

---

## The Audit-ALL-Phase3 archive (audit-all-phase3/)

> Source: `ADR-20260905-AUDIT-ALL-Phase3` — redistribution of arc-ml-engineer + arc-privacy-officer.

This archive contains the **source files** of the 2 agents that were renamed and redistributed
in Phase 3 (ml → inn-ml-engineer, privacy → loc-privacy-officer). The `arc-ml-engineer.md` and
`arc-privacy-officer.md` files are preserved here for traceability (in case of future re-merge).

The corresponding capsule directories were removed from `domain/rooms/04-architecture/agents/`.

---

## The audit (per `DEC-R6-20260905-ARCHIVE-LEGACY-AGENTS`)

> Source: `archive/legacy-hq-core-agents/MANIFEST.md` + `RESTORE.md` + `sha256-before.txt` +
> `sha256-after.txt`.

- **108 files** archived (legacy `hq/core/agents/<room>/<agent>.md`)
- **sha256 before == after** — byte-identity verified
- **15 broken file:line citations** resolved after archive (`evidence_guard hq/core --strict` → 0 broken)

---

## How to add to the archive

1. Create a new subdirectory: `archive/<name>-<date>/`
2. Create the manifest: `MANIFEST.md` (list of files + classification + sha256)
3. Create the restore procedure: `RESTORE.md` (step-by-step)
4. Compute `sha256-before.txt` + `sha256-after.txt` (must be byte-identical)
5. Commit atomically — pre-commit enforces all 4 guards
6. Record ADR in CORTEX

**Forbidden:** modifying files inside `archive/` (immutable — Law 13.5).

---

## See also

- [`../README.md`](../README.md) — `hq/core/` parent
- [`../structure-standard.md`](../structure-standard.md) — naming + old←new map
- [Top-level README](../../../README.md)
- [`AGENTS.md`](../../../AGENTS.md) — Law 13.5
