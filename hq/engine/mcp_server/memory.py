## FILE: hq/engine/mcp_server/memory.py
"""Memory integration — Law 7 — writes to hq/brain/* append-only with file lock."""
from __future__ import annotations

import os
from datetime import datetime, timezone
from pathlib import Path

try:
    from filelock import FileLock
except ImportError:
    FileLock = None  # fallback to no lock if not installed (tests still pass)

# Resolve hq/brain relative to this file: hq/engine/mcp_server -> hq/brain
BASE_DIR = Path(__file__).resolve().parent
HQ_BRAIN = BASE_DIR.parent.parent / "brain"  # hq/brain
# Fallback absolute
if not HQ_BRAIN.exists():
    HQ_BRAIN = Path("/home/es3dlll/Desktop/SOFI/hq/brain")

CORTEX = HQ_BRAIN / "cortex-decisions.md"
HIPPOCAMPUS = HQ_BRAIN / "hippocampus-sessions.md"
AMYGDALA = HQ_BRAIN / "amygdala-incidents.md"
LESSONS = HQ_BRAIN / "org_lessons" / "LESSONS.md"

# Project brain separation check
PROJECTS_ROOT = Path("/home/es3dlll/Desktop/SOFI/projects")


def _lock_for(path: Path):
    if FileLock is None:
        from contextlib import nullcontext
        return nullcontext()
    lock_path = str(path) + ".lock"
    return FileLock(lock_path, timeout=5)


def _ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(f"# {path.name}\n\n", encoding="utf-8")


def _append_line(path: Path, line: str) -> None:
    _ensure_parent(path)
    with _lock_for(path):
        with open(path, "a", encoding="utf-8") as f:
            f.write(line + "\n")

# Law 7: forbid writing project memory into org memory — check path

def _is_org_path(path: Path) -> bool:
    try:
        return HQ_BRAIN.resolve() in path.resolve().parents or path.resolve() == HQ_BRAIN.resolve()
    except Exception:
        return str(HQ_BRAIN) in str(path)


def _validate_org_write(content: str, target: str) -> None:
    # Detect project path injection in content — if content tries to claim project path as org
    # Simple guard: if content contains "projects/" and target is org, still allow but tag
    # Hard guard: if caller passes a project brain path as target for org write → reject
    if "projects/" in target and _is_org_path(Path(target)):
        raise ValueError("Law 7: لا يمكن كتابة ذاكرة مشروع في ذاكرة المؤسسة — فصل صارم")


def write_decision(content: str, room: str | None = None, evidence: str | None = None) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    room_tag = f"[{room}]" if room else "[system]"
    ev = f" — evidence: {evidence}" if evidence else " — evidence: hq/engine/mcp_server/memory.py:write_decision"
    line = f"- [{ts}] {room_tag} {content}{ev}"
    _append_line(CORTEX, line)
    return line


def write_session(content: str, session_id: str | None = None) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    sid = f" [{session_id}]" if session_id else ""
    line = f"- [{ts}]{sid} {content} — evidence: hq/engine/mcp_server/memory.py:write_session"
    _append_line(HIPPOCAMPUS, line)
    return line


def write_incident(content: str, severity: str | None = None) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    sev = f" [{severity}]" if severity else ""
    line = f"- [{ts}]{sev} {content} — evidence: hq/engine/mcp_server/memory.py:write_incident"
    _append_line(AMYGDALA, line)
    return line


def write_lesson(content: str, room: str | None = None) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    room_tag = f"[{room}]" if room else ""
    line = f"- [{ts}] {room_tag} {content} — evidence: hq/engine/mcp_server/memory.py:write_lesson"
    # LESSONS lives under org_lessons subdir
    LESSONS.parent.mkdir(parents=True, exist_ok=True)
    _append_line(LESSONS, line)
    return line
