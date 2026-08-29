## FILE: hq/engine/mcp_server/ticket_bus.py
"""Ticket Bus — enforces Law 2 (Room Isolation) — validates every cross-room attempt."""
from __future__ import annotations

import sqlite3
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from .config import get_room, is_lead, LEAD_IDS, MESSAGES_DB, TICKETS_DB, DATA_DIR
from .models import ALLOWED_TRANSITIONS, TicketStatus


# --- Exceptions ---

class CrossRoomViolation(Exception):
    """Raised when agent→agent cross-room is blocked by Law 2."""
    def __init__(self, sender: str, recipient: str):
        self.sender = sender
        self.recipient = recipient
        super().__init__(f"cross-room agent-to-agent blocked by Law 2: {sender} -> {recipient}")


class InvalidTransition(Exception):
    pass


# --- Core validation (Law 2) — MUST be first line in every send path ---

def validate_cross_room(sender: str, recipient: str) -> None:
    """Enforces Law 2: agent→agent across rooms is forbidden.
    Lead→lead and agent→lead (same room) and lead→agent (same room) are allowed.
    Raises CrossRoomViolation if blocked.
    File:Line: hq/engine/mcp_server/ticket_bus.py:validate_cross_room
    """
    s_room = get_room(sender)
    r_room = get_room(recipient)
    if s_room is None or r_room is None:
        # unknown ids — let caller handle 404, but don't bypass isolation
        return
    if s_room == r_room:
        return  # same room → allowed
    # Different rooms
    s_is_lead = is_lead(sender)
    r_is_lead = is_lead(recipient)
    # Only lead<->lead cross-room is allowed (via Ticket Bus)
    # agent->agent cross-room → blocked
    # agent->lead cross-room → blocked (must go via own lead first)
    if not s_is_lead and not r_is_lead:
        raise CrossRoomViolation(sender, recipient)
    if not s_is_lead and r_is_lead:
        # Agent trying to reach a lead of another room directly — blocked
        # Must go agent->own-lead->target-lead
        raise CrossRoomViolation(sender, recipient)
    # lead->agent cross-room and lead->lead cross-room are allowed (lead→lead is ticket_bus, lead→agent cross-room is rare but allowed for escalation)
    return


def validate_status_transition(current: str, nxt: str) -> None:
    """Validates Ticket status transition — only open→in_progress→resolved→closed."""
    try:
        cur = TicketStatus(current)
        nxt_s = TicketStatus(nxt)
    except ValueError:
        raise InvalidTransition(f"Invalid status value: {current}->{nxt}")
    allowed = ALLOWED_TRANSITIONS.get(cur, set())
    if nxt_s not in allowed:
        raise InvalidTransition(f"Invalid transition {current}->{nxt}. Allowed: open→in_progress→resolved→closed")


# --- DB helpers ---

def _ensure_dirs() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

def get_messages_conn() -> sqlite3.Connection:
    _ensure_dirs()
    conn = sqlite3.connect(str(MESSAGES_DB), check_same_thread=False, timeout=10.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    return conn

def get_tickets_conn() -> sqlite3.Connection:
    _ensure_dirs()
    # tickets and audit share same DB file by default if MESSAGES_DB == TICKETS_DB; we use TICKETS_DB
    conn = sqlite3.connect(str(TICKETS_DB), check_same_thread=False, timeout=10.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    return conn

def init_db() -> None:
    """Create tables from schema.sql idempotently."""
    schema_path = Path(__file__).parent / "contracts" / "schema.sql"
    # fallback: sibling contracts (أي بنية قديمة)
    if not schema_path.exists():
        schema_path = Path(__file__).parent / "schema.sql"
    # Also try reading the shipped schema from file tree
    import pathlib
    # Direct SQL if file not found (fallback inline)
    sql_fallback = """
    PRAGMA journal_mode=WAL;
    PRAGMA synchronous=NORMAL;
    PRAGMA foreign_keys=ON;
    CREATE TABLE IF NOT EXISTS rooms (id TEXT PRIMARY KEY, name TEXT NOT NULL, lead_id TEXT NOT NULL UNIQUE);
    CREATE TABLE IF NOT EXISTS agents (id TEXT PRIMARY KEY, name TEXT NOT NULL, room TEXT NOT NULL, lead_id TEXT NOT NULL);
    CREATE INDEX IF NOT EXISTS idx_agents_room ON agents(room);
    CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, sender TEXT NOT NULL, recipient TEXT NOT NULL, room TEXT NOT NULL, timestamp TEXT NOT NULL, content TEXT NOT NULL CHECK(length(content) >= 1 AND length(content) <= 4096), evidence TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'delivered' CHECK(status IN ('delivered','pending','failed')));
    CREATE INDEX IF NOT EXISTS idx_messages_sender ON messages(sender);
    CREATE INDEX IF NOT EXISTS idx_messages_recipient ON messages(recipient);
    CREATE INDEX IF NOT EXISTS idx_messages_timestamp ON messages(timestamp);
    CREATE TABLE IF NOT EXISTS tickets (id INTEGER PRIMARY KEY AUTOINCREMENT, requester TEXT NOT NULL, assignee TEXT NOT NULL, subject TEXT NOT NULL CHECK(length(subject) >= 1 AND length(subject) <= 256), description TEXT NOT NULL CHECK(length(description) >= 1 AND length(description) <= 4096), priority TEXT NOT NULL CHECK(priority IN ('low','medium','high','critical')), type TEXT NOT NULL CHECK(type IN ('task_assignment','consultation_request','escalation','gate_check')), status TEXT NOT NULL DEFAULT 'open' CHECK(status IN ('open','in_progress','resolved','closed')), created_at TEXT NOT NULL, updated_at TEXT NOT NULL, evidence TEXT NOT NULL);
    CREATE INDEX IF NOT EXISTS idx_tickets_status ON tickets(status);
    CREATE INDEX IF NOT EXISTS idx_tickets_priority ON tickets(priority);
    CREATE INDEX IF NOT EXISTS idx_tickets_assignee ON tickets(assignee);
    CREATE TABLE IF NOT EXISTS audit_logs (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT NOT NULL, agent_id TEXT NOT NULL, action TEXT NOT NULL, result TEXT NOT NULL, evidence TEXT NOT NULL, details TEXT);
    CREATE INDEX IF NOT EXISTS idx_audit_agent ON audit_logs(agent_id);
    CREATE INDEX IF NOT EXISTS idx_audit_action ON audit_logs(action);
    CREATE TRIGGER IF NOT EXISTS no_update_messages BEFORE UPDATE ON messages BEGIN SELECT RAISE(ABORT, 'messages is append-only — UPDATE forbidden'); END;
    CREATE TRIGGER IF NOT EXISTS no_delete_messages BEFORE DELETE ON messages BEGIN SELECT RAISE(ABORT, 'messages is append-only — DELETE forbidden'); END;
    CREATE TRIGGER IF NOT EXISTS no_update_audit_logs BEFORE UPDATE ON audit_logs BEGIN SELECT RAISE(ABORT, 'audit_logs is append-only — UPDATE forbidden'); END;
    CREATE TRIGGER IF NOT EXISTS no_delete_audit_logs BEFORE DELETE ON audit_logs BEGIN SELECT RAISE(ABORT, 'audit_logs is append-only — DELETE forbidden'); END;
    """
    sql = sql_fallback
    if schema_path.exists():
        try:
            sql = schema_path.read_text(encoding="utf-8")
            # strip first line ## FILE:
            if sql.startswith("## FILE:"):
                sql = "\n".join(sql.splitlines()[1:])
        except Exception:
            sql = sql_fallback
    # Execute on both DBs (they may be same file — double exec is idempotent)
    for db_path in {str(MESSAGES_DB), str(TICKETS_DB)}:
        conn = sqlite3.connect(db_path, timeout=10.0)
        try:
            conn.executescript(sql)
            # seed rooms if empty
            cur = conn.execute("SELECT COUNT(*) FROM rooms")
            if cur.fetchone()[0] == 0:
                conn.executescript("""
                INSERT OR IGNORE INTO rooms (id,name,lead_id) VALUES
                ('boardroom','Boardroom','brd-ceo'),
                ('strategy','Strategy','str-lead'),
                ('research','Research','res-lead'),
                ('design','Design','dsn-lead'),
                ('architecture','Architecture','arc-lead'),
                ('backend','Backend','bck-lead'),
                ('frontend','Frontend','fnt-lead'),
                ('mobile','Mobile','mob-lead'),
                ('data','Data','dat-lead'),
                ('security','Security','sec-lead'),
                ('quality','Quality','qa-lead'),
                ('devops','DevOps','ops-lead'),
                ('observability','Observability','obs-lead'),
                ('knowledge','Knowledge','knw-lead'),
                ('gateway','Gateway','gtw-dispatcher');
                """)
            conn.commit()
        finally:
            conn.close()

def write_audit(agent_id: str, action: str, result: str, evidence: str, details: str | None = None) -> int:
    """Append-only audit log — never update/delete."""
    conn = get_tickets_conn()
    try:
        ts = datetime.now(timezone.utc).isoformat()
        cur = conn.execute(
            "INSERT INTO audit_logs (timestamp, agent_id, action, result, evidence, details) VALUES (?,?,?,?,?,?)",
            (ts, agent_id, action, result, evidence, details),
        )
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()

def check_escalation_needed(created_at_iso: str, hours: float) -> bool:
    try:
        created = datetime.fromisoformat(created_at_iso)
        if created.tzinfo is None:
            created = created.replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        elapsed_h = (now - created).total_seconds() / 3600.0
        return elapsed_h >= hours
    except Exception:
        return False
