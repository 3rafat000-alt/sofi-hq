## FILE: hq/engine/mcp_server/contracts/schema.sql
-- SOFI MCP Server — SQLite Schema (WAL + Append-Only)
-- Evidence: hq/core/standards/pipeline-production-line.md S2 — paper before code
-- License: MIT — no GPL

PRAGMA journal_mode=WAL;
PRAGMA synchronous=NORMAL;
PRAGMA foreign_keys=ON;

-- Rooms — 15 fixed from registry.yaml
CREATE TABLE IF NOT EXISTS rooms (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    lead_id TEXT NOT NULL UNIQUE
);

-- Agents — 114 fixed from registry.yaml:6
CREATE TABLE IF NOT EXISTS agents (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    room TEXT NOT NULL REFERENCES rooms(id),
    lead_id TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_agents_room ON agents(room);
CREATE INDEX IF NOT EXISTS idx_agents_lead ON agents(lead_id);

-- Messages — agent<->lead communication
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender TEXT NOT NULL,
    recipient TEXT NOT NULL,
    room TEXT NOT NULL,
    timestamp TEXT NOT NULL, -- ISO-8601 UTC
    content TEXT NOT NULL CHECK(length(content) >= 1 AND length(content) <= 4096),
    evidence TEXT NOT NULL, -- file:line
    status TEXT NOT NULL DEFAULT 'delivered' CHECK(status IN ('delivered','pending','failed'))
);
CREATE INDEX IF NOT EXISTS idx_messages_sender ON messages(sender);
CREATE INDEX IF NOT EXISTS idx_messages_recipient ON messages(recipient);
CREATE INDEX IF NOT EXISTS idx_messages_timestamp ON messages(timestamp);
CREATE INDEX IF NOT EXISTS idx_messages_room ON messages(room);

-- Tickets — lead<->lead via Ticket Bus
CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    requester TEXT NOT NULL,
    assignee TEXT NOT NULL,
    subject TEXT NOT NULL CHECK(length(subject) >= 1 AND length(subject) <= 256),
    description TEXT NOT NULL CHECK(length(description) >= 1 AND length(description) <= 4096),
    priority TEXT NOT NULL CHECK(priority IN ('low','medium','high','critical')),
    type TEXT NOT NULL CHECK(type IN ('task_assignment','consultation_request','escalation','gate_check','clarification_request')),
    status TEXT NOT NULL DEFAULT 'open' CHECK(status IN ('open','in_progress','resolved','closed')),
    created_at TEXT NOT NULL, -- ISO-8601 UTC
    updated_at TEXT NOT NULL,
    evidence TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_tickets_status ON tickets(status);
CREATE INDEX IF NOT EXISTS idx_tickets_priority ON tickets(priority);
CREATE INDEX IF NOT EXISTS idx_tickets_assignee ON tickets(assignee);
CREATE INDEX IF NOT EXISTS idx_tickets_created ON tickets(created_at);

-- Audit Logs — append-only, never update/delete
CREATE TABLE IF NOT EXISTS audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    agent_id TEXT NOT NULL,
    action TEXT NOT NULL,
    result TEXT NOT NULL,
    evidence TEXT NOT NULL,
    details TEXT
);
CREATE INDEX IF NOT EXISTS idx_audit_agent ON audit_logs(agent_id);
CREATE INDEX IF NOT EXISTS idx_audit_action ON audit_logs(action);
CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_logs(timestamp);

-- Triggers — enforce append-only (Law 4)
CREATE TRIGGER IF NOT EXISTS no_update_messages
BEFORE UPDATE ON messages
BEGIN
    SELECT RAISE(ABORT, 'messages is append-only — UPDATE forbidden');
END;

CREATE TRIGGER IF NOT EXISTS no_delete_messages
BEFORE DELETE ON messages
BEGIN
    SELECT RAISE(ABORT, 'messages is append-only — DELETE forbidden');
END;

CREATE TRIGGER IF NOT EXISTS no_update_audit_logs
BEFORE UPDATE ON audit_logs
BEGIN
    SELECT RAISE(ABORT, 'audit_logs is append-only — UPDATE forbidden');
END;

CREATE TRIGGER IF NOT EXISTS no_delete_audit_logs
BEFORE DELETE ON audit_logs
BEGIN
    SELECT RAISE(ABORT, 'audit_logs is append-only — DELETE forbidden');
END;

-- Seed rooms (15)
INSERT OR IGNORE INTO rooms (id, name, lead_id) VALUES
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

-- --- Meetings (اجتماع الغرف) — separate DB meetings.db ---
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
);
