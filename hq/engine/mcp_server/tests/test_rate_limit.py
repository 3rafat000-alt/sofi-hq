## FILE: hq/engine/mcp_server/tests/test_rate_limit.py
"""Rate limit test — 100/min per agent."""
from hq.engine.mcp_server.main import check_rate_limit, _rate_store

def test_rate_limit_enforced_at_101():
    _rate_store.clear()
    agent = "test-agent-rate"
    for i in range(100):
        assert check_rate_limit(agent) is True, f"should allow {i+1}"
    assert check_rate_limit(agent) is False, "101st should be blocked"
