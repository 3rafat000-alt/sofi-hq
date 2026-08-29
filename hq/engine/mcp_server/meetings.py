## FILE: hq/engine/mcp_server/meetings.py
"""Room meetings bus — اجتماع الغرف: agenda, attendance, minutes → decisions go to CORTEX (Law 7)."""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from .config import DATA_DIR
from .ticket_bus import write_audit
from . import memory as mem


def get_meetings_conn() -> sqlite3.Connection:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DATA_DIR / "meetings.db")
    conn.row_factory = sqlite3.Row
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS meetings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            organizer TEXT NOT NULL,
            title TEXT NOT NULL,
            room TEXT NOT NULL,
            agenda TEXT NOT NULL,
            attendees TEXT NOT NULL DEFAULT '[]',
            scheduled_at TEXT,
            status TEXT NOT NULL DEFAULT 'scheduled',
            minutes TEXT,
            decisions TEXT NOT NULL DEFAULT '[]',
            actions TEXT NOT NULL DEFAULT '[]',
            minutes_version INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL,
            closed_at TEXT
        )
        """
    )
    conn.commit()
    return conn


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def create_meeting(organizer: str, title: str, room: str, agenda: str,
                   scheduled_at: Optional[str] = None, attendees: Optional[list[str]] = None) -> dict:
    conn = get_meetings_conn()
    try:
        now = _now()
        attendees_json = json.dumps(attendees or [], ensure_ascii=False)
        cur = conn.execute(
            "INSERT INTO meetings (organizer, title, room, agenda, attendees, scheduled_at, status, created_at) "
            "VALUES (?,?,?,?,?,?,?,?)",
            (organizer, title, room, agenda, attendees_json, scheduled_at or now, "scheduled", now),
        )
        mid = cur.lastrowid
        conn.commit()
    finally:
        conn.close()
    write_audit(organizer, "meeting_created", "scheduled",
                f"hq/engine/mcp_server/meetings.py:create_meeting",
                details=f"meeting:{mid} room:{room} attendees:{len(attendees or [])}")
    return {"meeting_id": mid, "title": title, "room": room, "status": "scheduled", "created_at": now}


def list_meetings(status: Optional[str] = None, room: Optional[str] = None, limit: int = 20) -> tuple[list[dict], int]:
    conn = get_meetings_conn()
    try:
        where, params = [], []
        if status:
            where.append("status = ?")
            params.append(status)
        if room:
            where.append("room = ?")
            params.append(room)
        sql = "SELECT * FROM meetings"
        if where:
            sql += " WHERE " + " AND ".join(where)
        sql += " ORDER BY id DESC LIMIT ?"
        params.append(int(limit))
        rows = [dict(r) for r in conn.execute(sql, params).fetchall()]
        count_sql = "SELECT COUNT(*) AS c FROM meetings" + (" WHERE " + " AND ".join(where) if where else "")
        total = conn.execute(count_sql, params[:-1]).fetchone()["c"]
    finally:
        conn.close()
    return rows, total


def close_meeting_with_minutes(mid: int, actor: str, attendees: Optional[list[str]] = None,
                               decisions: Optional[list[str]] = None, actions: Optional[list[str]] = None,
                               evidence: Optional[str] = None) -> dict:
    conn = get_meetings_conn()
    try:
        row = conn.execute("SELECT * FROM meetings WHERE id = ?", (mid,)).fetchone()
        if not row:
            raise ValueError("Meeting not found")
        if row["status"] == "closed":
            raise ValueError("Meeting already closed")
        now = _now()
        current = json.loads(row["attendees"] or "[]")
        if attendees:
            current = list(dict.fromkeys(current + attendees))
        decisions_list = decisions or []
        actions_list = actions or []
        minutes_text = json.dumps({
            "attendees": current,
            "decisions": decisions_list,
            "actions": actions_list,
            "evidence": evidence or f"hq/engine/mcp_server/meetings.py:close_meeting_with_minutes",
        }, ensure_ascii=False)
        conn.execute(
            "UPDATE meetings SET status='closed', attendees=?, minutes=?, decisions=?, actions=?, closed_at=?, minutes_version=? WHERE id=?",
            (json.dumps(current, ensure_ascii=False), minutes_text,
             json.dumps(decisions_list, ensure_ascii=False), json.dumps(actions_list, ensure_ascii=False),
             now, 1, mid),
        )
        conn.commit()
    finally:
        conn.close()

    write_audit(actor, "meeting_minutes", "closed",
                evidence or f"hq/engine/mcp_server/meetings.py:close_meeting_with_minutes",
                details=f"meeting:{mid} decisions:{len(decisions_list)} actions:{len(actions_list)}")

    # Decisions → CORTEX (Law 7 — every major decision logs)
    for d in decisions_list:
        try:
            mem.write_decision(f"[اجتماع] {row['title']} — {d}", room=row["room"],
                               evidence=evidence or f"hq/engine/mcp_server/meetings.py:{mid}")
        except Exception:
            pass

    return {"meeting_id": mid, "status": "closed", "decisions": decisions_list,
            "actions": actions_list, "attendees": current, "closed_at": now}