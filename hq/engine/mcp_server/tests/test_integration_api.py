## FILE: hq/engine/mcp_server/tests/test_integration_api.py
"""Integration tests via FastAPI TestClient — covers main.py endpoints + WS."""
import tempfile
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

# Setup temp DBs before importing app
import hq.engine.mcp_server.config as config
import hq.engine.mcp_server.ticket_bus as ticket_bus

tmp = tempfile.mkdtemp()
config.DATA_DIR = Path(tmp)
config.MESSAGES_DB = Path(tmp) / "messages.db"
config.TICKETS_DB = Path(tmp) / "tickets.db"
ticket_bus.DATA_DIR = Path(tmp)
ticket_bus.MESSAGES_DB = Path(tmp) / "messages.db"
ticket_bus.TICKETS_DB = Path(tmp) / "tickets.db"
config.MCP_API_KEY = "test-integration-key"
ticket_bus.init_db()

from hq.engine.mcp_server.main import app, _rate_store

KEY = "test-integration-key"
client = TestClient(app)

def headers(sender: str | None = None):
    h = {"X-API-Key": KEY}
    if sender:
        h["X-Sender"] = sender
    return h

def test_health():
    r = client.get("/health", headers=headers())
    assert r.status_code == 200
    assert r.json()["success"] is True

def test_health_no_key_allowed():
    r = client.get("/health")
    assert r.status_code in (200, 401)

def test_message_send_and_list():
    _rate_store.clear()
    r = client.post("/api/v1/message", headers=headers("bck-api-engineer"), json={"recipient":"bck-lead","content":"hello","evidence":"test:1"})
    assert r.status_code == 200, r.text
    assert r.json()["data"]["status"] == "delivered"
    r = client.get("/api/v1/messages", headers=headers(), params={"agent":"bck-api-engineer"})
    assert r.status_code == 200
    assert r.json()["data"][0]["content"] == "hello"

def test_cross_room_blocked():
    _rate_store.clear()
    r = client.post("/api/v1/message", headers=headers("bck-api-engineer"), json={"recipient":"fnt-react-engineer","content":"cross"})
    assert r.status_code == 403
    assert "ممنوع" in r.json()["message"]

def test_unauthorized():
    r = client.post("/api/v1/message", headers={"X-API-Key":"wrong"}, json={"recipient":"bck-lead","content":"x"})
    assert r.status_code == 401

def test_validation_empty():
    r = client.post("/api/v1/message", headers=headers("bck-api-engineer"), json={"recipient":"bck-lead","content":""})
    assert r.status_code == 422
    assert r.json()["error"]["code"] == "VALIDATION_ERROR"

def test_ticket_create_and_patch():
    _rate_store.clear()
    r = client.post("/api/v1/tickets", headers=headers("bck-lead"), json={"subject":"s","description":"d","priority":"high","type":"consultation_request","assignee":"arc-lead"})
    assert r.status_code == 201
    tid = r.json()["data"]["ticket_id"]
    r = client.get(f"/api/v1/tickets/{tid}", headers=headers())
    assert r.status_code == 200
    r = client.patch(f"/api/v1/tickets/{tid}", headers=headers("arc-lead"), json={"status":"in_progress"})
    assert r.status_code == 200
    assert r.json()["data"]["status"] == "in_progress"
    r2 = client.post("/api/v1/tickets", headers=headers("bck-lead"), json={"subject":"s2","description":"d","priority":"low","type":"task_assignment","assignee":"arc-lead"})
    tid2 = r2.json()["data"]["ticket_id"]
    r = client.patch(f"/api/v1/tickets/{tid2}", headers=headers(), json={"status":"closed"})
    assert r.status_code == 400

def test_tickets_list():
    r = client.get("/api/v1/tickets", headers=headers(), params={"status":"open"})
    assert r.status_code == 200

def test_memory_decision():
    r = client.post("/api/v1/memory/decision", headers=headers("bck-lead"), json={"content":"قرار اختبار","room":"bck-lead","evidence":"test"})
    assert r.status_code == 201
    assert "evidence" in r.json()["data"]["line"]

def test_audit_search_and_export():
    r = client.get("/api/v1/audit", headers=headers(), params={"agent":"bck-api-engineer"})
    assert r.status_code == 200
    r = client.get("/api/v1/audit/export", headers=headers(), params={"format":"json"})
    assert r.status_code == 200
    r = client.get("/api/v1/audit/export", headers=headers(), params={"format":"csv"})
    assert r.status_code == 200
    assert "id,timestamp" in r.text

def test_rate_limit_rest():
    _rate_store.clear()
    sender = "rate-limit-int-test"
    for i in range(100):
        r = client.post("/api/v1/message", headers=headers(sender), json={"recipient":"bck-lead","content":f"msg {i}"})
        assert r.status_code == 200, f"failed at {i} {r.text}"
    r = client.post("/api/v1/message", headers=headers(sender), json={"recipient":"bck-lead","content":"overflow"})
    assert r.status_code == 429
    assert r.headers.get("Retry-After") == "60"

def test_ws_agent_flow():
    _rate_store.clear()
    with client.websocket_connect(f"/ws/agent/bck-api-engineer?api_key={KEY}") as ws:
        ws.send_json({"content":"hello ws","evidence":"test_ws:1"})
        data = ws.receive_json()
        assert data["success"] is True
        assert data["status"] == "delivered"
        # cross-room blocked
        ws.send_json({"content":"cross","recipient":"fnt-react-engineer"})
        data2 = ws.receive_json()
        assert data2["success"] is False
        assert data2["error"]["code"] == "FORBIDDEN"
        # empty
        ws.send_json({"content":""})
        data3 = ws.receive_json()
        assert data3["error"]["code"] == "VALIDATION_ERROR"

def test_ws_lead_flow():
    _rate_store.clear()
    with client.websocket_connect(f"/ws/lead/bck-lead?api_key={KEY}") as ws:
        ws.send_json({"content":"lead msg","recipient":"bck-api-engineer"})
        data = ws.receive_json()
        assert data["success"] is True

def test_ws_unauthorized():
    # TestClient will raise if close code 4401 — we check via try
    try:
        with client.websocket_connect(f"/ws/agent/bck-api-engineer?api_key=wrong") as ws:
            ws.receive_json()
            assert False
    except Exception:
        pass
