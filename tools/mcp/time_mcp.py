#!/usr/bin/env python3
"""
⏰ Sofi Time MCP Server — إدارة الوقت والتوقيتات
=================================================
JSON-RPC 2.0 stdio MCP server for time, timezone, date operations
"""

import sys
import os
import asyncio
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tools.mcp.base import SofiBaseMCP
from datetime import datetime, timedelta, timezone
import json
from typing import Dict, List, Optional


TOOLS = [
    {
        "name": "current_time",
        "description": "الوقت الحالي بتوقيت محدد — Current time in specified timezone (UTC default)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "timezone": {
                    "type": "string",
                    "description": "IANA timezone like UTC, Asia/Riyadh, America/New_York",
                    "default": "UTC"
                },
                "format": {
                    "type": "string",
                    "description": "Output format: iso, unix, readable",
                    "default": "readable"
                }
            }
        }
    },
    {
        "name": "timezone_convert",
        "description": "تحويل وقت بين توقيتين — Convert time between timezones",
        "inputSchema": {
            "type": "object",
            "properties": {
                "time_str": {"type": "string", "description": "Time string like 2026-06-06T12:00:00 or HH:MM"},
                "from_tz": {"type": "string", "description": "Source timezone (e.g. America/New_York)"},
                "to_tz": {"type": "string", "description": "Target timezone (e.g. Asia/Riyadh)"}
            },
            "required": ["time_str", "from_tz", "to_tz"]
        }
    },
    {
        "name": "date_math",
        "description": "عمليات حسابية على التواريخ — Add/subtract time from a date",
        "inputSchema": {
            "type": "object",
            "properties": {
                "date": {"type": "string", "description": "Base date (YYYY-MM-DD or now)"},
                "days": {"type": "integer", "description": "Days to add (negative = subtract)"},
                "months": {"type": "integer", "description": "Months to add"},
                "years": {"type": "integer", "description": "Years to add"}
            },
            "required": ["date"]
        }
    },
    {
        "name": "date_diff",
        "description": "الفرق بين تاريخين — Calculate difference between two dates",
        "inputSchema": {
            "type": "object",
            "properties": {
                "date1": {"type": "string", "description": "First date (YYYY-MM-DD or ISO datetime)"},
                "date2": {"type": "string", "description": "Second date"}
            },
            "required": ["date1", "date2"]
        }
    },
    {
        "name": "format_date",
        "description": "تنسيق تاريخ بصيغة مخصصة — Format date with custom pattern",
        "inputSchema": {
            "type": "object",
            "properties": {
                "date": {"type": "string", "description": "Date string or 'now'"},
                "pattern": {
                    "type": "string",
                    "description": "strftime pattern (e.g. %A, %B %d, %Y)",
                    "default": "%Y-%m-%d %H:%M:%S %Z"
                },
                "locale": {
                    "type": "string",
                    "description": "Language (ar for Arabic, en for English)",
                    "default": "en"
                }
            },
            "required": ["date"]
        }
    }
]


OFFSET_MAP = {}
for tz_offset in range(-12, 13):
    label = f"UTC{tz_offset:+d}" if tz_offset != 0 else "UTC"
    OFFSET_MAP[label] = tz_offset


OFFSET_MAP.update({
    "ECT": 1, "EET": 2, "ART": 2, "EAT": 3, "MET": 3.5, "NET": 4,
    "PLT": 5, "BST": 6, "VST": 7, "CTT": 8, "JST": 9, "ACT": 9.5,
    "AET": 10, "SST": 11, "NST": 12,
    "MIT": -11, "HST": -10, "AST": -9, "PST": -8, "PNT": -7,
    "MST": -7, "CST": -6, "EST": -5, "IET": -5, "PRT": -4,
    "CNT": -3.5, "BRT": -3, "CAT": -1, "GMT": 0,
})


def _parse_tz(tz_name: str) -> timezone:
    tz_upper = tz_name.upper().replace(" ", "_")
    if tz_upper in OFFSET_MAP:
        hours = OFFSET_MAP[tz_upper]
        return timezone(timedelta(hours=hours))
    return timezone.utc


def _parse_datetime(s: str) -> datetime:
    s = s.strip()
    if s.lower() == "now":
        return datetime.now(timezone.utc)
    for fmt in [
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
        "%H:%M:%S",
        "%H:%M",
    ]:
        try:
            dt = datetime.strptime(s, fmt)
            return dt.replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    raise ValueError(f"تعذر تحليل التاريخ: {s}")


class TimeMCPServer(SofiBaseMCP):
    def __init__(self):
        super().__init__("⏰ Time MCP", "1.0.0", TOOLS)

    async def handle_tool_call(self, name: str, arguments: Dict) -> Dict:
        if name == "current_time":
            return await self._current_time(arguments)
        elif name == "timezone_convert":
            return await self._timezone_convert(arguments)
        elif name == "date_math":
            return await self._date_math(arguments)
        elif name == "date_diff":
            return await self._date_diff(arguments)
        elif name == "format_date":
            return await self._format_date(arguments)
        return self._text_error(f"أداة غير معروفة: {name}")

    async def _current_time(self, args: Dict) -> Dict:
        tz_name = args.get("timezone", "UTC")
        fmt = args.get("format", "readable")
        tz = _parse_tz(tz_name)
        now = datetime.now(tz)
        if fmt == "iso":
            return self._text_result(now.isoformat())
        elif fmt == "unix":
            return self._text_result(str(int(now.timestamp())))
        else:
            return self._text_result(now.strftime("%Y-%m-%d %H:%M:%S %Z"))

    async def _timezone_convert(self, args: Dict) -> Dict:
        time_str = args.get("time_str", "")
        from_tz = args.get("from_tz", "UTC")
        to_tz = args.get("to_tz", "UTC")
        dt = _parse_datetime(time_str)
        dt_from = dt.replace(tzinfo=_parse_tz(from_tz))
        dt_to = dt_from.astimezone(_parse_tz(to_tz))
        return self._text_result(dt_to.strftime("%Y-%m-%d %H:%M:%S %Z"))

    async def _date_math(self, args: Dict) -> Dict:
        date_str = args.get("date", "now")
        days = args.get("days", 0)
        months = args.get("months", 0)
        years = args.get("years", 0)
        dt = _parse_datetime(date_str)
        if years:
            try:
                dt = dt.replace(year=dt.year + years)
            except ValueError:
                dt = dt + timedelta(days=365 * years)
        if months:
            new_month = dt.month + months
            year_shift = (new_month - 1) // 12
            dt = dt.replace(year=dt.year + year_shift, month=((new_month - 1) % 12) + 1)
        if days:
            dt = dt + timedelta(days=days)
        return self._text_result(dt.strftime("%Y-%m-%d %H:%M:%S %Z"))

    async def _date_diff(self, args: Dict) -> Dict:
        d1 = _parse_datetime(args.get("date1", ""))
        d2 = _parse_datetime(args.get("date2", ""))
        diff = abs(d2 - d1)
        days = diff.days
        hours = diff.seconds // 3600
        minutes = (diff.seconds % 3600) // 60
        result = {
            "days": days,
            "hours": hours + days * 24,
            "minutes": minutes + (hours + days * 24) * 60,
            "seconds": int(diff.total_seconds()),
            "total_days": round(diff.total_seconds() / 86400, 2)
        }
        return self._text_result(json.dumps(result, ensure_ascii=False, indent=2))

    async def _format_date(self, args: Dict) -> Dict:
        date_str = args.get("date", "now")
        pattern = args.get("pattern", "%Y-%m-%d %H:%M:%S %Z")
        locale = args.get("locale", "en")
        dt = _parse_datetime(date_str)
        if locale == "ar":
            import locale as lc
            try:
                lc.setlocale(lc.LC_TIME, "ar_SA.UTF-8")
            except:
                pass
        return self._text_result(dt.strftime(pattern))


if __name__ == "__main__":
    server = TimeMCPServer()
    asyncio.run(server.run())
