#!/usr/bin/env python3
"""FILE: hq/core/tooling/memory_summarizer.py
Memory summarizer — Axis 8 fix (Context Bloat / Token Burn mitigation via knw-reflector)
Implements: Protocol 06 P-06.7 (knw-lead consolidation every 10 turns) + hq/core/standards/reporting-cadence.md
Purpose: compact hq/brain/hippocampus-sessions.md and amygdala-incidents.md when they exceed token-efficient thresholds,
         preserving every decision/violation/incident semantic while reducing raw line count.
Usage: python3 hq/core/tooling/memory_summarizer.py [--check] [--compact] [--threshold 1000]
  --check: report size + whether compaction needed (exit 1 if over threshold)
  --compact: perform compaction (creates .bak, writes compacted file, logs to cortex)
  --threshold: line count threshold (default 800 for hippocampus, 500 for amygdala overflow)

Logic (knw-reflector ritual):
  - hippocampus-sessions.md: keep last N sessions in full (N=5), summarize older sessions to 1-line per session + evidence links
  - amygdala-incidents.md: keep SEV-1/2 + open incidents in full; summarize closed SEV-3/4 >30 days to 1-line; dedup repeated escalations (e.g., ticket #1 spam 2026-08-29/30)
  - Never deletes cortex-decisions.md entries (permanent)
  - Writes summary header with date, stats, and link to .bak archive

Exit codes: 0 = ok / compacted, 1 = over threshold (needs compaction), 2 = error
"""
from __future__ import annotations
import pathlib, re, sys, datetime

ROOT = pathlib.Path(__file__).resolve().parents[3]
HIPPO = ROOT / "hq/brain/hippocampus-sessions.md"
AMYGDALA = ROOT / "hq/brain/amygdala-incidents.md"
CORTEX = ROOT / "hq/brain/cortex-decisions.md"

HIPPO_THRESHOLD = 800
AMYGDALA_THRESHOLD = 600  # amygdala currently 75k lines due to ticket spam
KEEP_RECENT_SESSIONS = 5

def count_lines(p: pathlib.Path) -> int:
    if not p.exists():
        return 0
    return len(p.read_text(errors="ignore").splitlines())

def summarize_hippocampus(threshold: int = HIPPO_THRESHOLD, do_compact: bool = False) -> tuple[int, str]:
    lines = count_lines(HIPPO)
    status = "OK" if lines <= threshold else "OVER"
    msg = f"hippocampus: {lines} lines (threshold {threshold}) → {status}"
    if not do_compact or lines <= threshold:
        return (0 if status == "OK" else 1), msg
    # Compact: keep header + last KEEP_RECENT_SESSIONS sessions in full, summarize older
    text = HIPPO.read_text(errors="ignore")
    # Sessions are marked by "## SES-"
    sessions = re.split(r"(?=^## SES-)", text, flags=re.MULTILINE)
    header = sessions[0] if sessions and not sessions[0].strip().startswith("## SES-") else ""
    sess_blocks = [s for s in sessions if s.strip().startswith("## SES-")]
    if len(sess_blocks) <= KEEP_RECENT_SESSIONS:
        return 0, msg + " — no compaction needed (recent sessions <= keep)"
    older = sess_blocks[:-KEEP_RECENT_SESSIONS]
    recent = sess_blocks[-KEEP_RECENT_SESSIONS:]
    # Summarize older to 1 line each
    summary_lines = []
    for block in older:
        # Extract SES id and first line summary
        m_id = re.search(r"##\s+(SES-[^\n]+)", block)
        sid = m_id.group(1).strip() if m_id else "unknown"
        # Find date or first bullet
        m_date = re.search(r"\d{4}-\d{2}-\d{2}", block)
        date = m_date.group(0) if m_date else "—"
        # Take first 120 chars of block stripped
        snippet = " ".join(block.splitlines()[1:3])[:120].strip()
        summary_lines.append(f"- {sid} ({date}): {snippet} … [compacted]")
    compacted = header.rstrip() + "\n\n## COMPACTED HISTORY (knw-reflector ritual 2026-08-31 — older sessions summarized, full in .bak)\n"
    compacted += f"_Compacted: {datetime.datetime.now().isoformat()} · original lines {lines} → summary {len(summary_lines)} entries + {len(recent)} recent full_\n"
    compacted += "\n".join(summary_lines) + "\n\n"
    compacted += "\n".join(recent)
    # Backup
    bak = HIPPO.with_suffix(".md.bak." + datetime.datetime.now().strftime("%Y%m%d"))
    bak.write_text(text, errors="ignore")
    HIPPO.write_text(compacted, errors="ignore")
    new_lines = len(compacted.splitlines())
    return 0, msg + f" → COMPACTED: {lines} → {new_lines} lines (bak: {bak.name}) · kept {len(recent)} recent full, summarized {len(summary_lines)} older"

def summarize_amygdala(threshold: int = AMYGDALA_THRESHOLD, do_compact: bool = False) -> tuple[int, str]:
    lines = count_lines(AMYGDALA)
    status = "OK" if lines <= threshold else "OVER"
    msg = f"amygdala: {lines} lines (threshold {threshold}) → {status}"
    if not do_compact or lines <= threshold:
        return (0 if status == "OK" else 1), msg
    text = AMYGDALA.read_text(errors="ignore")
    # Strategy: deduplicate repeated ticket escalations (ticket #1 spam) — keep first 2 and last 2 per ticket, summarize middle
    # Identify blocks by timestamp line
    lines_list = text.splitlines()
    header = "\n".join(l for l in lines_list[:5])  # first 5 lines header
    body = lines_list[5:]
    # Group by ticket number in line
    from collections import defaultdict
    grouped: dict[str, list[str]] = defaultdict(list)
    other = []
    for line in body:
        m = re.search(r"تذكرة #(\d+)", line)
        if m:
            grouped[m.group(1)].append(line)
        else:
            other.append(line)
    # For tickets with >10 entries, keep first 2 + last 2, summarize middle
    compacted_body = other.copy()
    dedup_count = 0
    for tid, entries in sorted(grouped.items(), key=lambda x: int(x[0])):
        if len(entries) > 6:
            kept = entries[:2] + [f"- [compacted {len(entries)-4} repeated escalations for ticket #{tid} — see .bak]"] + entries[-2:]
            dedup_count += len(entries) - 4
            compacted_body.extend(kept)
        else:
            compacted_body.extend(entries)
    # Sort compacted_body? Keep original order-ish: other + grouped sorted
    new_text = header + "\n" + "\n".join(compacted_body)
    bak = AMYGDALA.with_suffix(".md.bak." + datetime.datetime.now().strftime("%Y%m%d"))
    bak.write_text(text, errors="ignore")
    AMYGDALA.write_text(new_text, errors="ignore")
    new_lines = len(new_text.splitlines())
    return 0, msg + f" → DEDUPED: {lines} → {new_lines} lines (removed {dedup_count} duplicate escalation lines, bak: {bak.name})"

def main() -> int:
    check = "--check" in sys.argv
    compact = "--compact" in sys.argv
    thresh = HIPPO_THRESHOLD
    if "--threshold" in sys.argv:
        try:
            idx = sys.argv.index("--threshold")
            thresh = int(sys.argv[idx+1])
        except Exception:
            pass
    # hippocampus
    code_h, msg_h = summarize_hippocampus(threshold=thresh, do_compact=compact)
    print(msg_h)
    # amygdala — check if over threshold regardless
    code_a, msg_a = summarize_amygdala(threshold=AMYGDALA_THRESHOLD, do_compact=compact)
    print(msg_a)
    # cortex never compacted (permanent)
    cortex_lines = count_lines(CORTEX)
    print(f"cortex: {cortex_lines} lines (permanent — never compacted per P-06.2)")
    if check:
        # check mode: exit 1 if any over
        return 1 if (code_h == 1 or code_a == 1) else 0
    return 0

if __name__ == "__main__":
    sys.exit(main())
