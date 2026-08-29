## FILE: hq/engine/mcp_server/mcp_bridge/server.py
"""SOFI bus MCP gateway — opencode agents talk to SOFI's own bus (Law 2/3/4/6/7).
- Org knowledge: sofi_org_structure / sofi_who_is (ground truth = hq/core/nexus/registry.yaml — Law 12)
- Bus ops: sofi_send / sofi_ticket / sofi_clarify / sofi_escalate / sofi_tickets / sofi_audit / sofi_health
- Governance: sofi_consult (Board consultation after gateway delivery — Law 6) / sofi_meeting_* (اجتماع الغرف)
Rules: no blind work (task_id+context+evidence) · clarify not guess · escalate upward · wall enforced by bus.
"""
import json
import os
from typing import Optional

import httpx
import yaml
from mcp.server.fastmcp import FastMCP

_BRIDGE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(_BRIDGE_DIR)          # hq/engine/mcp_server (مجلد الحزمة — داخل المحرك)
# جذر SOFI محسوب بالصعود حتى نجد hq/core/nexus/registry.yaml — يتحمل أي نقل مستقبلي (Law 13: بلا مسارات وهمية)
def _find_sofi_root(start: str) -> str:
    d = start
    while True:
        if os.path.isfile(os.path.join(d, "hq/core/nexus/registry.yaml")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            raise RuntimeError("SOFI_ROOT not found — خذ جذر المشروع من متغير البيئة SOFI_ROOT")
        d = parent

SOFI_ROOT = os.environ.get("SOFI_ROOT") or _find_sofi_root(_BRIDGE_DIR)
REGISTRY = os.path.join(SOFI_ROOT, "hq/core/nexus/registry.yaml")
ENV_FILE = os.path.join(ROOT, ".env")

BASE_URL = os.environ.get("SOFI_BUS_URL", "http://127.0.0.1:8765")


def _api_key() -> str:
    if os.environ.get("SOFI_API_KEY"):
        return os.environ["SOFI_API_KEY"]
    try:
        for line in open(ENV_FILE, encoding="utf-8"):
            line = line.strip()
            if line.startswith("API_KEY=") or line.startswith("MCP_API_KEY=") or line.startswith("SOFI_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    except FileNotFoundError:
        pass
    return "dev-key-change-me"


KEY = _api_key()
_HEADERS = {"X-API-Key": KEY, "X-Sender": "mcp-bridge"}


def _load_registry() -> dict:
    with open(REGISTRY, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _room_id(agent_id: str) -> Optional[str]:
    for key, info in _load_registry()["rooms"].items():
        prefix = info["prefix"]
        if agent_id.startswith(prefix + "-") or agent_id in info.get("aliases", []):
            return key
    return None


def _room_lead(room_key: str, prefix: str) -> str:
    """Lead of a room per constitution: boardroom lead IS brd-ceo; gateway lead IS gtw-dispatcher (registry)."""
    if room_key.startswith("00"):
        return "brd-ceo"
    if room_key == "14":
        return "gtw-dispatcher"
    return f"{prefix}-lead"


mcp = FastMCP(
    "sofi",
    instructions=(
        "SOFI bus MCP — you are inside SOFI's own company bus (mcp.local:8765). "
        "Before cross-room work: know your room/lead/teammates via sofi_who_is; "
        "send only with task_id+context+evidence (no blind work); "
        "if information is missing → sofi_clarify (1-3 sharp questions) then escalate after silence; "
        "the Law-2 wall (agent→agent across rooms = 403) is enforced by the bus. "
        "Records: sofi_tickets / sofi_audit."
    ),
)


@mcp.tool()
def sofi_org_structure() -> str:
    """Full SOFI org: 15 rooms — code, name, lead, agent list (ground truth registry.yaml)."""
    reg = _load_registry()
    lines = []
    for key, info in reg["rooms"].items():
        prefix = info["prefix"]
        lead = _room_lead(key, prefix)
        others = ", ".join(f"{prefix}-{a}" for a in info["agents"])
        lines.append(f"{key} [{info['name_en']}] lead={lead} agents=({others})")
    return "\n".join(lines)


@mcp.tool()
def sofi_who_is(agent_id: str) -> str:
    """Who is this agent? Returns their room, lead, teammates, and whether they are a lead."""
    reg = _load_registry()
    for key, info in reg["rooms"].items():
        prefix = info["prefix"]
        if not agent_id.startswith(prefix + "-"):
            continue
        lead = _room_lead(key, prefix)
        is_lead = agent_id == lead
        teammates = [f"{prefix}-{a}" for a in info["agents"] if f"{prefix}-{a}" != agent_id]
        return json.dumps(
            {"agent": agent_id, "room": key, "room_name": info["name_en"], "lead": lead,
             "teammates": teammates, "is_lead": is_lead, "is_board_advisor": key.startswith("00") and agent_id != "brd-ceo"},
            ensure_ascii=False, indent=2)
    return f"UNKNOWN agent: {agent_id} — لا يوجد في السجل الرسمي (registry.yaml)"


@mcp.tool()
async def sofi_health() -> str:
    """Check SOFI bus health (server reachable, version)."""
    async with httpx.AsyncClient(timeout=5) as client:
        r = await client.get(f"{BASE_URL}/health", headers=_HEADERS)
        return json.dumps(r.json()["data"], ensure_ascii=False)


@mcp.tool()
async def sofi_send(sender: str, recipient: str, content: str, task_id: str, context: str, evidence: str) -> str:
    """Send a message to one agent/lead through the bus (Law 2/3). Guarded: task_id+context+evidence required."""
    if not (task_id and context and evidence):
        raise ValueError("عمل أعمى مرفوض: task_id + context + evidence مطلوبة")
    if _room_id(sender) is None:
        raise ValueError(f"المرسل {sender} غير معروف في السجل")
    if _room_id(recipient) is None:
        raise ValueError(f"المستلم {recipient} غير معروف في السجل")
    payload = {"sender": sender, "recipient": recipient, "content": content,
               "task_id": task_id, "context": context, "evidence": evidence}
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.post(f"{BASE_URL}/api/v1/message", headers=_HEADERS, json=payload)
    body = r.json()
    if r.status_code >= 400:
        raise RuntimeError(f"bus: {r.status_code} — {body.get('message')}")
    return json.dumps(body["data"], ensure_ascii=False)


@mcp.tool()
async def sofi_ticket(requester: str, assignee: str, subject: str, description: str, priority: str = "medium",
                      type: str = "task_assignment") -> str:
    """Create a ticket on the bus (task_assignment / consultation_request / escalation / gate_check / clarification_request)."""
    payload = {"requester": requester, "assignee": assignee, "subject": subject,
               "description": description, "priority": priority, "type": type}
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.post(f"{BASE_URL}/api/v1/tickets", headers=_HEADERS, json=payload)
    body = r.json()
    if r.status_code >= 400:
        raise RuntimeError(f"bus: {r.status_code} — {body.get('message')}")
    return json.dumps(body["data"], ensure_ascii=False)


@mcp.tool()
async def sofi_clarify(requester: str, questions: list[str], missing: str, assignee: Optional[str] = None) -> str:
    """Missing information → stop and ask 1-3 sharp questions (clarification_request ticket). No guessing."""
    if not 1 <= len(questions) <= 3:
        raise ValueError("اسأل حاداً: 1 إلى 3 أسئلة فقط")
    if assignee is None:
        room = _room_id(requester)
        reg = _load_registry()
        assignee = f"{reg['rooms'][room]['prefix']}-lead" if room else requester
    description = json.dumps({"questions": questions, "missing": missing,
                              "thinking": "Sequential-Thinking §15 — عائق في الفحص/الفهم"}, ensure_ascii=False)
    return await sofi_ticket(requester=requester, assignee=assignee, subject=f"[نقص] {missing[:80]}",
                             description=description, priority="high", type="clarification_request")


@mcp.tool()
async def sofi_escalate(requester: str, subject: str, description: str) -> str:
    """Escalate immediately to brd-ceo (critical/silent lead) — escalation is professionalism, not failure."""
    return await sofi_ticket(requester=requester, assignee="brd-ceo", subject=f"[تصعيد] {subject[:80]}",
                             description=description, priority="critical", type="escalation")


@mcp.tool()
async def sofi_tickets(status: Optional[str] = None, limit: int = 20) -> str:
    """List tickets (optionally filter by status: open/in_progress/resolved/closed)."""
    query: dict[str, str | int] = {"limit": limit}
    if status:
        query["status"] = status
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(f"{BASE_URL}/api/v1/tickets", headers=_HEADERS, params=query)
    body = r.json()
    if r.status_code >= 400:
        raise RuntimeError(f"bus: {r.status_code} — {body.get('message')}")
    return json.dumps(body.get("data", []), ensure_ascii=False)


@mcp.tool()
async def sofi_audit(agent: Optional[str] = None, action: Optional[str] = None, limit: int = 20) -> str:
    """Query the immutable audit log (Law 4 — every step recorded)."""
    params: dict[str, str | int] = {"limit": limit}
    if agent:
        params["agent"] = agent
    if action:
        params["action"] = action
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(f"{BASE_URL}/api/v1/audit", headers=_HEADERS, params=params)
    body = r.json()
    if r.status_code >= 400:
        raise RuntimeError(f"bus: {r.status_code} — {body.get('message')}")
    return json.dumps(body.get("data", []), ensure_ascii=False)


@mcp.tool()
async def sofi_consult(requester: str, consultee: str, subject: str, description: str,
                       decision_options: list[str] | None = None, priority: str = "high") -> str:
    """Board consultation (Law 6) — a lead/CEO consults a board advisor or fellow lead; decision options attached; audited."""
    payload = {"requester": requester, "consultee": consultee, "subject": subject,
               "description": description, "decision_options": decision_options or [], "priority": priority}
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.post(f"{BASE_URL}/api/v1/consult", headers=_HEADERS, json=payload)
    body = r.json()
    if r.status_code >= 400:
        raise RuntimeError(f"bus: {r.status_code} — {body.get('message')}")
    return json.dumps(body["data"], ensure_ascii=False)


@mcp.tool()
async def sofi_meeting_new(organizer: str, title: str, agenda: str, room: str = "boardroom",
                           attendees: list[str] | None = None) -> str:
    """Schedule a room meeting (اجتماع الغرف) — agenda + attendees; minutes follow via sofi_meeting_minutes."""
    payload = {"organizer": organizer, "title": title, "agenda": agenda,
               "room": room, "attendees": attendees or []}
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.post(f"{BASE_URL}/api/v1/meetings", headers=_HEADERS, json=payload)
    body = r.json()
    if r.status_code >= 400:
        raise RuntimeError(f"bus: {r.status_code} — {body.get('message')}")
    return json.dumps(body["data"], ensure_ascii=False)


@mcp.tool()
async def sofi_meetings(status: Optional[str] = None, room: Optional[str] = None, limit: int = 20) -> str:
    """List room meetings (optionally by status: scheduled/closed — or by room)."""
    params: dict[str, str | int] = {"limit": limit}
    if status:
        params["status"] = status
    if room:
        params["room"] = room
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(f"{BASE_URL}/api/v1/meetings", headers=_HEADERS, params=params)
    body = r.json()
    if r.status_code >= 400:
        raise RuntimeError(f"bus: {r.status_code} — {body.get('message')}")
    return json.dumps(body.get("data", []), ensure_ascii=False)


@mcp.tool()
async def sofi_meeting_minutes(meeting_id: int, decisions: list[str], actions: list[str],
                               attendees: list[str] | None = None, evidence: str = "") -> str:
    """Close a meeting with minutes — decisions go to CORTEX (Law 7). Evidence optional but preferred."""
    payload = {"decisions": decisions, "actions": actions, "attendees": attendees or [], "evidence": evidence}
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.post(f"{BASE_URL}/api/v1/meetings/{meeting_id}/minutes", headers=_HEADERS, json=payload)
    body = r.json()
    if r.status_code >= 400:
        raise RuntimeError(f"bus: {r.status_code} — {body.get('message')}")
    return json.dumps(body["data"], ensure_ascii=False)


if __name__ == "__main__":
    mcp.run(transport="stdio")