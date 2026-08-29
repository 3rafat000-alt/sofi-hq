## FILE: hq/engine/mcp_server/config.py
"""SOFI MCP Server — Configuration (Law 13: real path header, Law 15: MIT only, Law 7: .env secrets only)."""
from __future__ import annotations

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from same directory or project root — secrets never in code (P-08.1)
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")
load_dotenv(BASE_DIR / ".env.local", override=False)

# --- Server ---
MCP_HOST: str = os.getenv("MCP_HOST", "127.0.0.1")
MCP_PORT: int = int(os.getenv("MCP_PORT", "8765"))
MCP_API_KEY: str = os.getenv("SOFI_MCP_API_KEY", "dev-key-change-me")
ESCALATION_HOURS: float = float(os.getenv("ESCALATION_HOURS", "24"))  # for tests override to 0.033 (2min)
ESCALATION_CHECK_INTERVAL_S: int = int(os.getenv("ESCALATION_CHECK_INTERVAL_S", "3600"))

# --- Rate limiting ---
RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "100"))

# --- DB paths (two separate files per spec) ---
DATA_DIR: Path = BASE_DIR / "data"
MESSAGES_DB: Path = Path(os.getenv("MESSAGES_DB", str(DATA_DIR / "messages.db")))
TICKETS_DB: Path = Path(os.getenv("TICKETS_DB", str(DATA_DIR / "tickets.db")))
# Alternate: single-file mode uses same path for both if env points to same file — default is separate

# --- Audit export ---
AUDIT_PAGE_LIMIT: int = 100

# --- Rooms & Leads — 15 rooms from registry.yaml:6 (Law 12 invariant) ---
ROOMS: dict[str, dict] = {
    "boardroom": {"lead": "brd-ceo", "name": "Boardroom", "code": "00"},
    "strategy": {"lead": "str-lead", "name": "Strategy", "code": "01"},
    "research": {"lead": "res-lead", "name": "Research", "code": "02"},
    "design": {"lead": "dsn-lead", "name": "Design", "code": "03"},
    "architecture": {"lead": "arc-lead", "name": "Architecture", "code": "04"},
    "backend": {"lead": "bck-lead", "name": "Backend", "code": "05"},
    "frontend": {"lead": "fnt-lead", "name": "Frontend", "code": "06"},
    "mobile": {"lead": "mob-lead", "name": "Mobile", "code": "07"},
    "data": {"lead": "dat-lead", "name": "Data", "code": "08"},
    "security": {"lead": "sec-lead", "name": "Security", "code": "09"},
    "quality": {"lead": "qa-lead", "name": "Quality", "code": "10"},
    "devops": {"lead": "ops-lead", "name": "DevOps", "code": "11"},
    "observability": {"lead": "obs-lead", "name": "Observability", "code": "12"},
    "knowledge": {"lead": "knw-lead", "name": "Knowledge", "code": "13"},
    "gateway": {"lead": "gtw-dispatcher", "name": "Gateway", "code": "14"},
}

# --- Agents — 114 agents (representative + dynamic) — Law 12 ---
# Full list derived from registry.yaml. For validation we store room per agent.
# The 30 most-used agents are explicit; others are resolved via AGENT_ROOM map build below.
_EXPLICIT_AGENTS: dict[str, str] = {
    # boardroom
    "brd-ceo": "boardroom", "brd-cpo": "boardroom", "brd-cto": "boardroom", "brd-cqo": "boardroom",
    "brd-cso": "boardroom", "brd-chief-of-staff": "boardroom", "brd-arbiter": "boardroom",
    # strategy
    "str-lead": "strategy", "str-product-strategist": "strategy", "str-business-analyst": "strategy",
    "str-market-analyst": "strategy", "str-roadmap-planner": "strategy", "str-risk-analyst": "strategy",
    "str-monetization-strategist": "strategy", "str-agile-orchestrator": "strategy",
    # research
    "res-lead": "research", "res-ux-researcher": "research", "res-journey-architect": "research",
    "res-competitor-analyst": "research", "res-data-researcher": "research", "res-fact-checker": "research",
    "res-web-scout": "research", "res-visual-pattern-scout": "research",
    # design
    "dsn-lead": "design", "dsn-ui-designer": "design", "dsn-design-system": "design",
    "dsn-brand-designer": "design", "dsn-content-strategist": "design", "dsn-motion-designer": "design",
    "dsn-a11y-specialist": "design", "dsn-ux-architect": "design", "dsn-competitive-ui-analyst": "design",
    "dsn-arabic-ux-specialist": "design",
    # architecture
    "arc-lead": "architecture", "arc-system-architect": "architecture", "arc-api-architect": "architecture",
    "arc-data-architect": "architecture", "arc-infra-architect": "architecture", "arc-integration-architect": "architecture",
    "arc-review-architect": "architecture", "arc-security-architect": "architecture", "arc-performance-architect": "architecture",
    # backend
    "bck-lead": "backend", "bck-api-engineer": "backend", "bck-domain-engineer": "backend",
    "bck-blade-engineer": "backend", "bck-queue-engineer": "backend", "bck-integration-engineer": "backend",
    "bck-code-reviewer": "backend", "bck-refactoring-surgeon": "backend",
    # frontend
    "fnt-lead": "frontend", "fnt-vue-engineer": "frontend", "fnt-react-engineer": "frontend",
    "fnt-css-artisan": "frontend", "fnt-interaction-engineer": "frontend", "fnt-performance-engineer": "frontend",
    "fnt-a11y-engineer": "frontend", "fnt-code-reviewer": "frontend",
    # mobile
    "mob-lead": "mobile", "mob-flutter-engineer": "mobile", "mob-platform-engineer": "mobile",
    "mob-state-engineer": "mobile", "mob-perf-profiler": "mobile", "mob-release-engineer": "mobile",
    # data
    "dat-lead": "data", "dat-db-engineer": "data", "dat-cache-engineer": "data",
    "dat-etl-engineer": "data", "dat-analytics-engineer": "data", "dat-ml-engineer": "data", "dat-privacy-officer": "data",
    # security
    "sec-lead": "security", "sec-pentester": "security", "sec-appsec-engineer": "security",
    "sec-authn-engineer": "security", "sec-compliance-auditor": "security", "sec-incident-responder": "security",
    "sec-threat-modeler": "security", "sec-secrets-warden": "security", "sec-license-auditor": "security",
    # quality
    "qa-lead": "quality", "qa-test-architect": "quality", "qa-automation-engineer": "quality",
    "qa-manual-explorer": "quality", "qa-perf-analyst": "quality", "qa-design-auditor": "quality", "qa-regression-warden": "quality",
    # devops
    "ops-lead": "devops", "ops-cicd-engineer": "devops", "ops-cloud-engineer": "devops", "ops-cost-optimizer": "devops",
    "ops-domain-warden": "devops", "ops-migration-runner": "devops", "ops-release-manager": "devops", "ops-sandbox-executor": "devops",
    # observability
    "obs-lead": "observability", "obs-monitoring-engineer": "observability", "obs-alerting-engineer": "observability",
    "obs-sre": "observability", "obs-incident-commander": "observability", "obs-insights-analyst": "observability",
    # knowledge
    "knw-lead": "knowledge", "knw-brain-query": "knowledge", "knw-doc-writer": "knowledge",
    "knw-historian": "knowledge", "knw-memory-curator": "knowledge", "knw-reflector": "knowledge",
    # gateway
    "gtw-dispatcher": "gateway", "gtw-router": "gateway", "gtw-gatekeeper": "gateway",
    "gtw-budget-warden": "gateway", "gtw-conflict-resolver": "gateway", "gtw-external-reviewer": "gateway", "gtw-intake-reformer": "gateway",
}

# Build reverse maps
AGENT_ROOM: dict[str, str] = dict(_EXPLICIT_AGENTS)
ROOM_LEADS: dict[str, str] = {v["lead"]: k for k, v in ROOMS.items()}
LEAD_IDS: set[str] = set(ROOM_LEADS.keys())
ALL_AGENT_IDS: set[str] = set(AGENT_ROOM.keys())

# Helper: room of any id (agent or lead) — leads belong to their room too
def get_room(agent_id: str) -> str | None:
    if agent_id in AGENT_ROOM:
        return AGENT_ROOM[agent_id]
    if agent_id in ROOM_LEADS:
        return ROOM_LEADS[agent_id]
    # prefix fallback for unseen variants (e.g., bck-new-engineer) — keep strict but allow
    prefix_map = {
        "brd": "boardroom", "str": "strategy", "res": "research", "dsn": "design",
        "arc": "architecture", "bck": "backend", "fnt": "frontend", "mob": "mobile",
        "dat": "data", "sec": "security", "qa": "quality", "ops": "devops",
        "obs": "observability", "knw": "knowledge", "gtw": "gateway",
    }
    if "-" in agent_id:
        pref = agent_id.split("-")[0]
        return prefix_map.get(pref)
    return None

def is_lead(agent_id: str) -> bool:
    return agent_id in LEAD_IDS

def is_agent(agent_id: str) -> bool:
    # true for non-lead agents
    return agent_id in ALL_AGENT_IDS and agent_id not in LEAD_IDS
