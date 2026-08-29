## FILE: hq/engine/mcp_server/leads_mcp.py
"""Leads MCP — Ticket Bus operations + escalation."""
from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from typing import Optional

from .config import ESCALATION_HOURS
from .ticket_bus import get_tickets_conn, write_audit, validate_status_transition, check_escalation_needed
from . import memory as mem


def create_ticket(requester: str, assignee: str, subject: str, description: str, priority: str, type_: str, evidence: str | None = None) -> dict:
    conn = get_tickets_conn()
    try:
        now = datetime.now(timezone.utc).isoformat()
        ev = evidence or f"hq/engine/mcp_server/leads_mcp.py:create_ticket"
        cur = conn.execute(
            "INSERT INTO tickets (requester, assignee, subject, description, priority, type, status, created_at, updated_at, evidence) VALUES (?,?,?,?,?,?,?,?,?,?)",
            (requester, assignee, subject, description, priority, type_, "open", now, now, ev),
        )
        tid = cur.lastrowid
        conn.commit()
    finally:
        conn.close()

    write_audit(requester, "ticket_created", "open", ev, details=f"ticket:{tid} assignee:{assignee} priority:{priority}")

    # Critical → immediate incident log
    if priority == "critical":
        try:
            mem.write_incident(f"تذكرة حرجة #{tid}: {subject} — من {requester} إلى {assignee}", severity="critical")
        except Exception:
            pass

    return {"ticket_id": tid, "status": "open", "assignee": assignee, "created_at": now}


def get_ticket(tid: int) -> Optional[dict]:
    conn = get_tickets_conn()
    try:
        cur = conn.execute("SELECT * FROM tickets WHERE id = ?", (tid,))
        row = cur.fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def update_ticket(tid: int, new_status: str, assignee: Optional[str] = None, actor: str = "system") -> dict:
    conn = get_tickets_conn()
    try:
        cur = conn.execute("SELECT status FROM tickets WHERE id = ?", (tid,))
        row = cur.fetchone()
        if not row:
            raise ValueError("Ticket not found")
        current = row["status"]
        validate_status_transition(current, new_status)
        now = datetime.now(timezone.utc).isoformat()
        if assignee:
            conn.execute("UPDATE tickets SET status=?, assignee=?, updated_at=? WHERE id=?", (new_status, assignee, now, tid))
        else:
            conn.execute("UPDATE tickets SET status=?, updated_at=? WHERE id=?", (new_status, now, tid))
        conn.commit()
        cur = conn.execute("SELECT * FROM tickets WHERE id=?", (tid,))
        updated = dict(cur.fetchone())
    finally:
        conn.close()

    write_audit(actor, "ticket_updated", new_status, f"hq/engine/mcp_server/leads_mcp.py:update_ticket", details=f"ticket:{tid} {current}->{new_status}")

    return updated


def list_tickets(status: Optional[str] = None, priority: Optional[str] = None, assignee: Optional[str] = None, room: Optional[str] = None, page: int = 1, limit: int = 20) -> tuple[list[dict], int]:
    conn = get_tickets_conn()
    try:
        where = []
        params: list = []
        if status:
            where.append("status = ?")
            params.append(status)
        if priority:
            where.append("priority = ?")
            params.append(priority)
        if assignee:
            where.append("assignee = ?")
            params.append(assignee)
        # room filter: we don't have room column; skip or map via agent room
        where_sql = f"WHERE {' AND '.join(where)}" if where else ""
        cur = conn.execute(f"SELECT COUNT(*) FROM tickets {where_sql}", params)
        total = cur.fetchone()[0]
        offset = (page - 1) * limit
        cur = conn.execute(f"SELECT * FROM tickets {where_sql} ORDER BY created_at DESC LIMIT ? OFFSET ?", params + [limit, offset])
        rows = [dict(r) for r in cur.fetchall()]
        # post-filter by room if needed (lookup assignee room)
        if room:
            from .config import get_room as gr
            rows = [r for r in rows if gr(r["assignee"]) == room or gr(r["requester"]) == room]
        return rows, total
    finally:
        conn.close()


def escalate_stale_tickets(hours: float | None = None) -> list[int]:
    """Scan open tickets and escalate to brd-ceo if older than hours."""
    h = hours if hours is not None else ESCALATION_HOURS
    conn = get_tickets_conn()
    try:
        cur = conn.execute("SELECT id, created_at, assignee FROM tickets WHERE status = 'open'")
        stale = []
        rows = cur.fetchall()
        for row in rows:
            if check_escalation_needed(row["created_at"], h):
                stale.append(row["id"])
        for tid in stale:
            now = datetime.now(timezone.utc).isoformat()
            conn.execute("UPDATE tickets SET assignee=?, updated_at=?, type=? WHERE id=?", ("brd-ceo", now, "escalation", tid))
            ts = datetime.now(timezone.utc).isoformat()
            # Use same conn for audit to avoid database locked
            conn.execute(
                "INSERT INTO audit_logs (timestamp, agent_id, action, result, evidence, details) VALUES (?,?,?,?,?,?)",
                (ts, "system", "escalation", "escalated_to_brd-ceo", "hq/engine/mcp_server/leads_mcp.py:escalate_stale_tickets", f"ticket:{tid}"),
            )
            try:
                mem.write_incident(f"تصعيد تذكرة #{tid} إلى brd-ceo — تجاوزت {h} ساعة", severity="high")
            except Exception:
                pass
        conn.commit()
        return stale
    finally:
        conn.close()


def create_consultation(requester: str, consultee: str, subject: str, description: str,
                        decision_options: list[str] | None = None, priority: str = "high",
                        evidence: str | None = None) -> dict:
    """Board consultation (Law 6): lead/CEO consults a board advisor or another lead.

    Creates a consultation_request ticket addressed to the consultee with decision
    options attached — every consult is a recorded, auditable step after gateway delivery.
    """
    from .ticket_bus import write_audit, get_tickets_conn
    if requester == consultee:
        raise ValueError("لا يمكنك استشارة نفسك")
    conn = get_tickets_conn()
    try:
        now = datetime.now(timezone.utc).isoformat()
        payload = {
            "description": description,
            "decision_options": decision_options or [],
            "flow": "gateway-delivery → brd-ceo → board consultation (Law 6)",
        }
        import json as _json
        ev = evidence or "hq/engine/mcp_server/leads_mcp.py:create_consultation"
        cur = conn.execute(
            "INSERT INTO tickets (requester, assignee, subject, description, priority, type, status, created_at, updated_at, evidence) "
            "VALUES (?,?,?,?,?,?,?,?,?,?)",
            (requester, consultee, subject, _json.dumps(payload, ensure_ascii=False),
             priority, "consultation_request", "open", now, now, ev),
        )
        tid = cur.lastrowid
        conn.commit()
    finally:
        conn.close()
    write_audit(requester, "consult_opened", "open",
                evidence or "hq/engine/mcp_server/leads_mcp.py:create_consultation",
                details=f"ticket:{tid} consultee:{consultee} priority:{priority}")
    return {"ticket_id": tid, "type": "consultation_request", "status": "open",
            "consultee": consultee, "created_at": now}
