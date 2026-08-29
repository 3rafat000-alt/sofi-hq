## FILE: hq/engine/mcp_server/models.py
"""Pydantic models — strict validation (F6) — bilingual errors."""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator


class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class TicketType(str, Enum):
    task_assignment = "task_assignment"
    consultation_request = "consultation_request"
    escalation = "escalation"
    gate_check = "gate_check"
    clarification_request = "clarification_request"


class TicketStatus(str, Enum):
    open = "open"
    in_progress = "in_progress"
    resolved = "resolved"
    closed = "closed"


# Allowed transitions: open -> in_progress -> resolved -> closed
ALLOWED_TRANSITIONS: dict[TicketStatus, set[TicketStatus]] = {
    TicketStatus.open: {TicketStatus.in_progress},
    TicketStatus.in_progress: {TicketStatus.resolved},
    TicketStatus.resolved: {TicketStatus.closed},
    TicketStatus.closed: set(),
}

# --- Envelope (api-envelope.md v1) ---

class EnvelopeMeta(BaseModel):
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    envelope_version: str = "v1"
    pagination: Optional[dict] = None


class EnvelopeError(BaseModel):
    code: str
    message: str
    details: list[dict] = []


class Envelope(BaseModel):
    success: bool
    message: str
    data: Any = None
    error: Optional[EnvelopeError] = None
    meta: EnvelopeMeta = Field(default_factory=EnvelopeMeta)


def success_envelope(data: Any = None, message: str = "Done successfully", pagination: Optional[dict] = None) -> dict:
    meta = EnvelopeMeta(pagination=pagination)
    return Envelope(success=True, message=message, data=data, error=None, meta=meta).model_dump()


def error_envelope(code: str, message: str, status: int = 500, details: Optional[list[dict]] = None, request_id: Optional[str] = None) -> dict:
    meta = EnvelopeMeta(request_id=request_id or str(uuid.uuid4()))
    return Envelope(success=False, message=message, data=None, error=EnvelopeError(code=code, message=message, details=details or []), meta=meta).model_dump()


# --- Message ---

class MessageCreate(BaseModel):
    recipient: str = Field(..., min_length=1, max_length=128, description="recipient id")
    content: str = Field(..., min_length=1, max_length=4096, description="1-4096 chars")
    sender: Optional[str] = Field(None, description="filled from auth if missing")
    evidence: Optional[str] = Field(None, max_length=512)

    @field_validator("content")
    @classmethod
    def content_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("المحتوى فارغ — أرسل نصًا بين 1 و4096 حرف")
        return v

    @field_validator("recipient")
    @classmethod
    def recipient_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("المستقبل فارغ")
        return v.strip()


class MessageOut(BaseModel):
    id: int
    sender: str
    recipient: str
    room: str
    timestamp: str
    content: str
    evidence: str
    status: str


# --- Ticket ---

class TicketCreate(BaseModel):
    subject: str = Field(..., min_length=1, max_length=256)
    description: str = Field(..., min_length=1, max_length=4096)
    priority: Priority
    type: TicketType
    assignee: str = Field(..., min_length=1)
    requester: Optional[str] = None
    evidence: Optional[str] = None

    @field_validator("subject", "description")
    @classmethod
    def not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("الحقل فارغ")
        return v


class TicketUpdate(BaseModel):
    status: TicketStatus
    assignee: Optional[str] = None


# --- Memory ---

class MemoryDecisionCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=4096)
    room: Optional[str] = None
    evidence: Optional[str] = None

    @field_validator("content")
    @classmethod
    def not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("المحتوى فارغ")
        return v


class MemorySessionCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=4096)
    session_id: Optional[str] = None


class MemoryIncidentCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=4096)
    severity: Optional[str] = Field(None, pattern="^(low|medium|high|critical)$")


# --- Board consultation (Law 6 — CEO consults the Board after gateway delivery) ---

class ConsultCreate(BaseModel):
    requester: str = Field(..., min_length=2, max_length=64)
    consultee: str = Field(..., min_length=2, max_length=64)
    subject: str = Field(..., min_length=3, max_length=160)
    description: str = Field(..., min_length=3, max_length=4096)
    decision_options: list[str] = Field(default_factory=list)
    priority: str = Field("high", pattern="^(low|medium|high|critical)$")


# --- Room meetings (اجتماع الغرف) ---

class MeetingCreate(BaseModel):
    organizer: str = Field(..., min_length=2, max_length=64)
    title: str = Field(..., min_length=3, max_length=200)
    room: str = Field("boardroom", min_length=2, max_length=64)
    agenda: str = Field(..., min_length=3, max_length=4096)
    scheduled_at: Optional[str] = None
    attendees: list[str] = Field(default_factory=list)


class MeetingMinutes(BaseModel):
    attendees: list[str] = Field(default_factory=list)
    decisions: list[str] = Field(default_factory=list)
    actions: list[str] = Field(default_factory=list)
    evidence: Optional[str] = None


# --- Pagination helper ---

def paginate(total: int, page: int, limit: int) -> dict:
    return {"page": page, "per_page": limit, "total": total}
