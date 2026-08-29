## FILE: hq/engine/mcp_server/tests/test_leads_mcp.py
"""Leads/Ticket tests."""
import tempfile
from pathlib import Path
import hq.engine.mcp_server.config as config
import hq.engine.mcp_server.ticket_bus as ticket_bus
import hq.engine.mcp_server.leads_mcp as leads_mcp

def setup():
    tmp = tempfile.mkdtemp()
    config.DATA_DIR = Path(tmp)
    config.MESSAGES_DB = Path(tmp)/"messages.db"
    config.TICKETS_DB = Path(tmp)/"tickets.db"
    ticket_bus.DATA_DIR = Path(tmp)
    ticket_bus.MESSAGES_DB = Path(tmp)/"messages.db"
    ticket_bus.TICKETS_DB = Path(tmp)/"tickets.db"
    ticket_bus.init_db()
    return tmp

def test_create_and_update_ticket():
    setup()
    res = leads_mcp.create_ticket("bck-lead","arc-lead","مراجعة","هل نستخدم SQLite؟","high","consultation_request")
    assert res["status"] == "open"
    tid = res["ticket_id"]
    upd = leads_mcp.update_ticket(tid,"in_progress", actor="arc-lead")
    assert upd["status"] == "in_progress"
    upd = leads_mcp.update_ticket(tid,"resolved", actor="arc-lead")
    assert upd["status"] == "resolved"
    upd = leads_mcp.update_ticket(tid,"closed", actor="arc-lead")
    assert upd["status"] == "closed"

def test_invalid_transition():
    setup()
    res = leads_mcp.create_ticket("bck-lead","arc-lead","subj","desc","low","task_assignment")
    tid = res["ticket_id"]
    try:
        leads_mcp.update_ticket(tid,"closed", actor="bck-lead")
        assert False
    except Exception as e:
        assert "Invalid transition" in str(e)

def test_escalation():
    setup()
    import datetime
    old = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=25)).isoformat()
    conn = ticket_bus.get_tickets_conn()
    cur = conn.execute("INSERT INTO tickets (requester,assignee,subject,description,priority,type,status,created_at,updated_at,evidence) VALUES (?,?,?,?,?,?,?,?,?,?)",
                       ("bck-lead","arc-lead","old","desc","high","consultation_request","open",old,old,"ev"))
    tid = cur.lastrowid
    conn.commit()
    conn.close()
    stale = leads_mcp.escalate_stale_tickets(hours=24)
    assert tid in stale
    row = leads_mcp.get_ticket(tid)
    assert row["assignee"] == "brd-ceo"
