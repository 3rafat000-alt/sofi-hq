## FILE: hq/engine/mcp_server/tests/test_ticket_bus.py
"""Unit tests for ticket_bus — Law 2 enforcement."""
from hq.engine.mcp_server.config import get_room
from hq.engine.mcp_server.ticket_bus import validate_cross_room, CrossRoomViolation, validate_status_transition, InvalidTransition

def test_same_room_allowed():
    validate_cross_room("bck-api-engineer","bck-lead")

def test_cross_room_agent_to_agent_blocked():
    try:
        validate_cross_room("bck-api-engineer","fnt-react-engineer")
        assert False, "should have raised"
    except CrossRoomViolation as e:
        assert "Law 2" in str(e)

def test_cross_room_agent_to_lead_blocked():
    try:
        validate_cross_room("bck-api-engineer","fnt-lead")
        assert False
    except CrossRoomViolation:
        pass

def test_lead_to_lead_allowed():
    validate_cross_room("bck-lead","fnt-lead")

def test_lead_to_agent_cross_room_allowed():
    validate_cross_room("bck-lead","fnt-react-engineer")

def test_valid_transitions():
    validate_status_transition("open","in_progress")
    validate_status_transition("in_progress","resolved")
    validate_status_transition("resolved","closed")

def test_invalid_transitions():
    for cur,nxt in [("open","resolved"),("open","closed"),("in_progress","closed"),("closed","open")]:
        try:
            validate_status_transition(cur,nxt)
            assert False, f"should block {cur}->{nxt}"
        except InvalidTransition:
            pass
