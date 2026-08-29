## FILE: hq/engine/mcp_server/tests/test_agents_mcp.py
"""Unit tests for agents_mcp — persistence and isolation."""
import tempfile, sqlite3
from pathlib import Path
import hq.engine.mcp_server.config as config
import hq.engine.mcp_server.ticket_bus as ticket_bus
import hq.engine.mcp_server.agents_mcp as agents_mcp

def setup_temp_db():
    tmp = tempfile.mkdtemp()
    msg_db = Path(tmp) / "messages.db"
    tick_db = Path(tmp) / "tickets.db"
    config.DATA_DIR = Path(tmp)
    config.MESSAGES_DB = msg_db
    config.TICKETS_DB = tick_db
    ticket_bus.DATA_DIR = Path(tmp)
    ticket_bus.MESSAGES_DB = msg_db
    ticket_bus.TICKETS_DB = tick_db
    ticket_bus.init_db()
    return tmp

def test_send_to_lead_persists():
    tmp = setup_temp_db()
    result = agents_mcp.send_message("bck-api-engineer","bck-lead","تم إنجاز API","hq/engine/mcp_server/tests/test_agents_mcp.py:1")
    assert result["id"] == 1
    assert result["status"] == "delivered"
    conn = sqlite3.connect(str(config.MESSAGES_DB))
    cur = conn.execute("SELECT COUNT(*) FROM messages")
    assert cur.fetchone()[0] == 1
    rows,total = agents_mcp.list_messages(agent="bck-api-engineer")
    assert total == 1
    assert rows[0]["content"] == "تم إنجاز API"
    conn2 = sqlite3.connect(str(config.TICKETS_DB))
    cur = conn2.execute("SELECT COUNT(*) FROM audit_logs WHERE action='message_sent'")
    assert cur.fetchone()[0] >= 1

def test_cross_room_blocked_no_db_row():
    tmp = setup_temp_db()
    from hq.engine.mcp_server.ticket_bus import CrossRoomViolation
    try:
        agents_mcp.send_message("bck-api-engineer","fnt-react-engineer","محاولة")
        assert False
    except CrossRoomViolation:
        pass
    conn = sqlite3.connect(str(config.MESSAGES_DB))
    cur = conn.execute("SELECT COUNT(*) FROM messages")
    assert cur.fetchone()[0] == 0

def test_empty_content_blocked_by_constraint():
    tmp = setup_temp_db()
    conn = sqlite3.connect(str(config.MESSAGES_DB))
    try:
        conn.execute("INSERT INTO messages (sender,recipient,room,timestamp,content,evidence,status) VALUES (?,?,?,?,?,?,?)",
                     ("a","b","backend","2026-01-01T00:00:00Z","","ev","delivered"))
        assert False
    except sqlite3.IntegrityError:
        pass
