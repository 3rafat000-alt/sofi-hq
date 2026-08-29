## FILE: hq/engine/mcp_server/agents_mcp.py
"""Agents MCP — agent<->lead communication with Law 2 enforcement and persistence."""
from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from typing import Optional

from .config import get_room, is_lead
from .ticket_bus import validate_cross_room, get_messages_conn, write_audit, get_tickets_conn


def send_message(sender: str, recipient: str, content: str, evidence: str | None = None, status: str = "delivered") -> dict:
    """Sends a message from sender to recipient.
    First line validates cross-room (Law 2). Returns inserted row dict.
    """
    # Law 2 — MUST be first
    validate_cross_room(sender, recipient)

    room = get_room(sender) or get_room(recipient) or "unknown"
    ts = datetime.now(timezone.utc).isoformat()
    ev = evidence or f"hq/engine/mcp_server/agents_mcp.py:send_message"
    # Also handle evidence length
    if not ev:
        ev = "hq/engine/mcp_server/agents_mcp.py:send_message"

    # Persist to messages.db
    conn = get_messages_conn()
    try:
        cur = conn.execute(
            "INSERT INTO messages (sender, recipient, room, timestamp, content, evidence, status) VALUES (?,?,?,?,?,?,?)",
            (sender, recipient, room, ts, content, ev, status),
        )
        msg_id = cur.lastrowid
        conn.commit()
    finally:
        conn.close()

    # Audit log
    write_audit(sender, "message_sent", "delivered", ev, details=f"to:{recipient} id:{msg_id}")

    return {
        "id": msg_id,
        "sender": sender,
        "recipient": recipient,
        "room": room,
        "timestamp": ts,
        "content": content,
        "evidence": ev,
        "status": status,
    }


def list_messages(agent: Optional[str] = None, room: Optional[str] = None, page: int = 1, limit: int = 20) -> tuple[list[dict], int]:
    conn = get_messages_conn()
    try:
        where = []
        params: list = []
        if agent:
            where.append("(sender = ? OR recipient = ?)")
            params.extend([agent, agent])
        if room:
            where.append("room = ?")
            params.append(room)
        where_sql = f"WHERE {' AND '.join(where)}" if where else ""
        # total
        cur = conn.execute(f"SELECT COUNT(*) FROM messages {where_sql}", params)
        total = cur.fetchone()[0]
        offset = (page - 1) * limit
        cur = conn.execute(
            f"SELECT * FROM messages {where_sql} ORDER BY timestamp DESC LIMIT ? OFFSET ?",
            params + [limit, offset],
        )
        rows = [dict(r) for r in cur.fetchall()]
        return rows, total
    finally:
        conn.close()
