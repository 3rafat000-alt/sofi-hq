## FILE: hq/engine/mcp_server/tests/test_governance.py
"""Board consultation (Law 6) + room meetings (اجتماع الغرف) — endpoint tests against live-ish TestClient."""
import os
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import tempfile

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

from hq.engine.mcp_server.main import app  # noqa: E402

API_KEY = "test-integration-key"
client = TestClient(app)
H = {"X-API-Key": API_KEY}


def test_consult_opens_consultation_ticket():
    r = client.post("/api/v1/consult", headers=H, json={
        "requester": "brd-ceo", "consultee": "brd-cso",
        "subject": "استشارة: نشر البوابة للإنتاج",
        "description": "قرار مصيري — فتح البوابة للإنتاج",
        "decision_options": ["نشر مع ROLLBACK", "تأجيل أسبوع"],
        "priority": "critical",
    })
    assert r.status_code == 201, r.text
    data = r.json()["data"]
    assert data["type"] == "consultation_request"
    assert data["status"] == "open"
    assert data["consultee"] == "brd-cso"


def test_consult_self_rejected():
    r = client.post("/api/v1/consult", headers=H, json={
        "requester": "brd-ceo", "consultee": "brd-ceo",
        "subject": "خطأ", "description": "لا استشارة ذاتية",
    })
    assert r.status_code == 400


def test_meeting_lifecycle():
    r = client.post("/api/v1/meetings", headers=H, json={
        "organizer": "brd-ceo", "title": "تنسيق أسبوعي للغرف",
        "room": "boardroom", "agenda": "1) حالة المشاريع 2) العوائق 3) القرارات",
        "attendees": ["bck-lead", "sec-lead", "qa-lead"],
    })
    assert r.status_code == 201, r.text
    mid = r.json()["data"]["meeting_id"]

    r = client.get("/api/v1/meetings", headers=H, params={"status": "scheduled"})
    assert r.status_code == 200
    assert any(m["id"] == mid for m in r.json()["data"])

    r = client.post(f"/api/v1/meetings/{mid}/minutes", headers=H, json={
        "decisions": ["اعتماد تصميم الواجهة بعد مراجعة الأمان"],
        "actions": ["bck-lead: تنفيذ العقد المجمد"],
        "evidence": "contracts/openapi.yaml:26",
    })
    assert r.status_code == 200, r.text
    data = r.json()["data"]
    assert data["status"] == "closed"
    assert data["decisions"] == ["اعتماد تصميم الواجهة بعد مراجعة الأمان"]


def test_minutes_for_missing_meeting_404():
    r = client.post("/api/v1/meetings/999999/minutes", headers=H, json={"decisions": ["x"]})
    assert r.status_code == 404