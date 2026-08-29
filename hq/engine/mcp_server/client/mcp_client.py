## FILE: hq/engine/mcp_server/client/mcp_client.py
"""SOFI MCP Client SDK — Python — احترافي مرن — يمنع العمل الأعمى."""
from __future__ import annotations
import asyncio, json, os, time
from pathlib import Path
from typing import Optional

import httpx
try:
    import websockets
    HAS_WS = True
except ImportError:
    HAS_WS = False

# Config — from .env or default
BASE_HOST = os.getenv("MCP_HOST", "127.0.0.1")
BASE_PORT = os.getenv("MCP_PORT", "8765")
API_KEY = os.getenv("SOFI_MCP_API_KEY", "dev-key-change-me")
BASE_REST = f"http://{BASE_HOST}:{BASE_PORT}"
BASE_WS = f"ws://{BASE_HOST}:{BASE_PORT}"

class MCPClient:
    """عميل مرن: يحاول WS أولاً، يتحول تلقائياً لـ REST إن انقطع — لا عمل أعمى."""

    def __init__(self, agent_id: str, api_key: Optional[str] = None, base_rest: Optional[str] = None, base_ws: Optional[str] = None):
        self.agent_id = agent_id
        self.api_key = api_key or API_KEY
        self.base_rest = base_rest or BASE_REST
        self.base_ws = base_ws or BASE_WS
        self._ws: Optional[object] = None
        self._rest = httpx.AsyncClient(timeout=5.0)

    # --- REST helpers ---
    async def send_to_lead_rest(self, content: str, evidence: str = "client/mcp_client.py:send", recipient: Optional[str] = None, task_id: Optional[str] = None, context: Optional[str] = None) -> dict:
        """إرسال عبر REST — مرن — مع كل الحقول المضادة للعمى."""
        # auto-resolve recipient = lead of own room if not given
        if not recipient:
            from hq.engine.mcp_server.config import get_room, ROOMS
            room = get_room(self.agent_id)
            recipient = next((v["lead"] for k, v in ROOMS.items() if k == room), self.agent_id)

        payload = {"recipient": recipient, "content": content, "evidence": evidence, "sender": self.agent_id}
        # task_id/context are logged in audit details via evidence string — keep payload minimal per openapi
        headers = {"X-API-Key": self.api_key, "X-Sender": self.agent_id}
        r = await self._rest.post(f"{self.base_rest}/api/v1/message", headers=headers, json=payload)
        if r.status_code == 429:
            retry = int(r.headers.get("Retry-After", "60"))
            raise RuntimeError(f"RATE_LIMITED — انتظر {retry}ث — {r.json().get('message')}")
        if r.status_code == 403:
            raise PermissionError(f"FORBIDDEN Law 2 — {r.json().get('message')}")
        r.raise_for_status()
        return r.json()["data"]

    async def consult_lead(self, subject: str, description: str, assignee: str, priority: str = "medium", type_: str = "consultation_request") -> dict:
        """استشارة بين قادة عبر Ticket Bus — لا عمل أعمى."""
        headers = {"X-API-Key": self.api_key, "X-Sender": self.agent_id}
        payload = {"subject": subject, "description": description, "priority": priority, "type": type_, "assignee": assignee, "requester": self.agent_id}
        r = await self._rest.post(f"{self.base_rest}/api/v1/tickets", headers=headers, json=payload)
        r.raise_for_status()
        return r.json()["data"]

    async def clarify(self, questions: list[str], missing: str, thinking: str = "", assignee: str | None = None, priority: str = "high") -> dict:
        """حلقة الأسئلة (§16): نقص/غموض → 1-3 أسئلة حادة — لا تخمين.
        توقف فوراً، اسأل حاداً، انتظر الجواب — التخمين = عمل أعمى = L2."""
        if not 1 <= len(questions) <= 3:
            raise ValueError("اسأل حاداً: 1 إلى 3 أسئلة فقط — لا أسئلة مفتوحة عريضة")
        import json as _json
        description = _json.dumps({"questions": questions, "missing": missing, "thinking": thinking or "Sequential-Thinking §15 — عائق في الخطوة 2/3"})
        # المرسل: الوكيل → قائده تلقائياً، أو القائد → من يملك القرار
        if not assignee:
            from hq.engine.mcp_server.config import get_room, ROOMS
            room = get_room(self.agent_id)
            assignee = next((v["lead"] for k, v in ROOMS.items() if k == room), None) or self.agent_id
        return await self.consult_lead(subject=f"[نقص] {missing[:80]}", description=description, assignee=assignee, priority=priority, type_="clarification_request")

    async def escalate(self, subject: str, description: str, priority: str = "critical", assignee: str = "brd-ceo") -> dict:
        """تصعيد فوري (§16): لا انتظار — صعّد للأعلى بأسئلتك وسياقك — التصعيد احترافية لا فشل."""
        return await self.consult_lead(subject=f"[تصعيد] {subject[:80]}", description=description, assignee=assignee, priority=priority, type_="escalation")

    async def write_decision(self, content: str, room: Optional[str] = None, evidence: str = "client/mcp_client.py:write_decision") -> dict:
        headers = {"X-API-Key": self.api_key}
        payload = {"content": content, "room": room or self.agent_id, "evidence": evidence}
        r = await self._rest.post(f"{self.base_rest}/api/v1/memory/decision", headers=headers, json=payload)
        r.raise_for_status()
        return r.json()["data"]

    # --- WebSocket helpers (فوري) ---
    async def connect_ws(self) -> None:
        if not HAS_WS:
            raise RuntimeError("websockets not installed — pip install websockets")
        # Determine WS path by role
        from hq.engine.mcp_server.config import is_lead
        path = "lead" if is_lead(self.agent_id) else "agent"
        uri = f"{self.base_ws}/ws/{path}/{self.agent_id}?api_key={self.api_key}"
        self._ws = await websockets.connect(uri)

    async def send_to_lead_ws(self, content: str, evidence: str = "client/mcp_client.py:ws", recipient: Optional[str] = None, retries: int = 3) -> dict:
        """إرسال عبر WS مع إعادة محاولة 3 مرات ثم fallback REST."""
        for attempt in range(retries):
            try:
                if self._ws is None:
                    await self.connect_ws()
                payload = {"content": content, "evidence": evidence}
                if recipient:
                    payload["recipient"] = recipient
                await self._ws.send(json.dumps(payload))
                raw = await asyncio.wait_for(self._ws.recv(), timeout=3)
                data = json.loads(raw)
                if data.get("success") is False:
                    # Law 2 etc — لا تحاول REST، ارفع فوراً
                    if data.get("error", {}).get("code") == "FORBIDDEN":
                        raise PermissionError(data.get("message"))
                    raise RuntimeError(data.get("message"))
                return data
            except (websockets.ConnectionClosed, asyncio.TimeoutError, OSError) as e:
                self._ws = None
                if attempt == retries - 1:
                    # Fallback REST — مرونة
                    return await self.send_to_lead_rest(content, evidence, recipient)
                await asyncio.sleep(1)
        # Should not reach
        return await self.send_to_lead_rest(content, evidence, recipient)

    async def close(self):
        if self._ws:
            try:
                await self._ws.close()
            except Exception:
                pass
        await self._rest.aclose()

    # --- Convenience: send with anti-blind guard ---
    async def send_guarded(self, content: str, evidence: str, task_id: str, context: str, recipient: Optional[str] = None) -> dict:
        """لا ترسل بدون task_id+context+evidence — يمنع العمل الأعمى."""
        if not task_id or not context or not evidence:
            raise ValueError("لا ترسل بدون task_id و context و evidence — هذا عمل أعمى مرفوض")
        # Prefer WS, fallback REST automatically
        try:
            return await self.send_to_lead_ws(content, evidence, recipient)
        except PermissionError:
            raise
        except Exception:
            return await self.send_to_lead_rest(content, evidence, recipient)
