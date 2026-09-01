#!/usr/bin/env python3
"""
Episodic Memory MCP Server — Event Recording & Lessons Learned
================================================================
Records events with timestamps, extracts lessons from outcomes,
and provides recall of past events with similarity matching.
"""

import sys
import os
import asyncio
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tools.mcp.base import SofiBaseMCP
from tools.shared.memory_core import MemoryCore
import json
from typing import Dict


TOOLS = [
    {
        "name": "record_event",
        "description": "Record an event in episodic memory with automatic lesson extraction",
        "inputSchema": {
            "type": "object",
            "properties": {
                "event_type": {"type": "string", "description": "Type of event (e.g. deploy, error, milestone, review)"},
                "data": {"type": "object", "description": "Event data including summary, status, error, action taken"},
                "agent": {"type": "string", "description": "Agent that performed the action (default: system)"},
                "tags": {"type": "array", "items": {"type": "string"}, "description": "Tags for categorization"}
            },
            "required": ["event_type", "data"]
        }
    },
    {
        "name": "recall_events",
        "description": "Recall past events from episodic memory, optionally filtered by type or agent",
        "inputSchema": {
            "type": "object",
            "properties": {
                "event_type": {"type": "string", "description": "Filter by event type (e.g. error, deploy, milestone)"},
                "agent": {"type": "string", "description": "Filter by agent name"},
                "n": {"type": "integer", "description": "Number of events to return (max 50)", "default": 10},
                "include_lessons": {"type": "boolean", "description": "Only return events with lessons", "default": False}
            }
        }
    },
    {
        "name": "learn_from_mistakes",
        "description": "Explicitly record a lesson learned from an outcome (error or success)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "outcome": {"type": "object", "description": "Outcome data: error/summary/action taken. If contains 'error', it's extracted as a lesson"},
                "agent": {"type": "string", "description": "Agent name"}
            },
            "required": ["outcome"]
        }
    },
    {
        "name": "get_lessons",
        "description": "Retrieve all lessons learned, optionally filtered by applied status",
        "inputSchema": {
            "type": "object",
            "properties": {
                "applied": {"type": "boolean", "description": "Filter by whether the lesson has been applied"},
                "n": {"type": "integer", "description": "Number of lessons to return (max 50)", "default": 20}
            }
        }
    },
    {
        "name": "mark_lesson_applied",
        "description": "Mark a lesson as having been applied",
        "inputSchema": {
            "type": "object",
            "properties": {
                "episode_id": {"type": "integer", "description": "Episode/event ID containing the lesson"}
            },
            "required": ["episode_id"]
        }
    }
]


class EpisodicMemoryMCP(SofiBaseMCP):
    def __init__(self):
        super().__init__("Episodic Memory MCP", "1.0.0", TOOLS)
        self.memory = MemoryCore()

    async def handle_tool_call(self, name: str, arguments: Dict) -> Dict:
        if name == "record_event":
            return self._record_event(arguments)
        elif name == "recall_events":
            return self._recall_events(arguments)
        elif name == "learn_from_mistakes":
            return self._learn_from_mistakes(arguments)
        elif name == "get_lessons":
            return self._get_lessons(arguments)
        elif name == "mark_lesson_applied":
            return self._mark_lesson_applied(arguments)
        return self._text_error(f"Unknown tool: {name}")

    def _record_event(self, args: Dict) -> Dict:
        event_type = args.get("event_type", "")
        data = args.get("data", {})
        agent = args.get("agent", "system")
        tags = args.get("tags", [])
        if not event_type or not data:
            return self._text_error("event_type and data are required")
        ep_id = self.memory.record_event(event_type, data, agent=agent)
        lesson = data.get("lesson", "")
        return self._text_result(json.dumps({
            "status": "recorded",
            "episode_id": ep_id,
            "event_type": event_type,
            "agent": agent,
            "lesson_extracted": bool(lesson),
            "total_events": self.memory.episodic.count()
        }, ensure_ascii=False, indent=2))

    def _recall_events(self, args: Dict) -> Dict:
        event_type = args.get("event_type")
        agent = args.get("agent")
        n = min(args.get("n", 10), 50)
        include_lessons = args.get("include_lessons", False)
        events = self.memory.recall_events(event_type, agent=agent, n=n)
        if not include_lessons:
            events = [e for e in events if not e.get("lesson")]
        return self._text_result(json.dumps({
            "count": len(events),
            "events": events
        }, ensure_ascii=False, indent=2, default=str))

    def _learn_from_mistakes(self, args: Dict) -> Dict:
        outcome = args.get("outcome", {})
        agent = args.get("agent", "system")
        if not outcome:
            return self._text_error("outcome is required")
        ep_id = self.memory.learn_from_mistakes(outcome, agent=agent)
        return self._text_result(json.dumps({
            "status": "lesson_recorded",
            "episode_id": ep_id,
            "lesson": outcome.get("error", outcome.get("summary", "recorded")),
            "agent": agent
        }, ensure_ascii=False, indent=2))

    def _get_lessons(self, args: Dict) -> Dict:
        applied = args.get("applied")
        n = min(args.get("n", 20), 50)
        lessons = self.memory.episodic.get_lessons(applied=applied, n=n)
        return self._text_result(json.dumps({
            "count": len(lessons),
            "lessons": lessons
        }, ensure_ascii=False, indent=2, default=str))

    def _mark_lesson_applied(self, args: Dict) -> Dict:
        ep_id = args.get("episode_id")
        if not ep_id:
            return self._text_error("episode_id is required")
        success = self.memory.episodic.mark_lesson_applied(ep_id)
        return self._text_result(json.dumps({
            "status": "applied" if success else "failed",
            "episode_id": ep_id
        }))


if __name__ == "__main__":
    server = EpisodicMemoryMCP()
    asyncio.run(server.run())
