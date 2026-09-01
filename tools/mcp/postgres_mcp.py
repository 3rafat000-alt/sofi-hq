#!/usr/bin/env python3
"""
🐘 Sofi PostgreSQL MCP Server — قاعدة البيانات العلائقية
==========================================================
JSON-RPC 2.0 stdio MCP server for PostgreSQL operations
"""

import sys
import os
import asyncio
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tools.mcp.base import SofiBaseMCP
import json
from typing import Dict


TOOLS = [
    {
        "name": "pg_query",
        "description": "تنفيذ استعلام SQL — Execute SQL query on PostgreSQL",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "SQL query to execute"},
                "params": {"type": "array", "description": "Query parameters", "items": {"type": "string"}}
            },
            "required": ["query"]
        }
    },
    {
        "name": "pg_tables",
        "description": "عرض الجداول — List all tables in the database",
        "inputSchema": {
            "type": "object",
            "properties": {
                "schema": {"type": "string", "description": "Schema name", "default": "public"}
            }
        }
    },
    {
        "name": "pg_describe",
        "description": "وصف جدول — Describe table structure",
        "inputSchema": {
            "type": "object",
            "properties": {
                "table": {"type": "string", "description": "Table name"}
            },
            "required": ["table"]
        }
    }
]


POSTGRES_AVAILABLE = False
PG_CONNECTION = None


def _get_connection():
    global PG_CONNECTION, POSTGRES_AVAILABLE
    if PG_CONNECTION is not None:
        return PG_CONNECTION
    conn_str = os.environ.get(
        "POSTGRES_CONNECTION_STRING",
        "postgresql://sofi:sofi@localhost:5432/sofi_enterprise"
    )
    try:
        import psycopg2
        PG_CONNECTION = psycopg2.connect(conn_str)
        POSTGRES_AVAILABLE = True
        return PG_CONNECTION
    except Exception:
        POSTGRES_AVAILABLE = False
        return None


class PostgresMCPServer(SofiBaseMCP):
    def __init__(self):
        super().__init__("🐘 PostgreSQL MCP", "1.0.0", TOOLS)

    async def handle_tool_call(self, name: str, arguments: Dict) -> Dict:
        conn = _get_connection()
        if not POSTGRES_AVAILABLE:
            return self._text_result(
                "⚠️ PostgreSQL غير متاح. PostgreSQL server غير مشغل أو psycopg2 غير مثبت.\n"
                "للتفعيل: ثبت psycopg2 وشغل PostgreSQL محلياً.\n"
                "الاتصال الافتراضي: postgresql://sofi:sofi@localhost:5432/sofi_enterprise"
            )

        if name == "pg_query":
            return await self._pg_query(conn, arguments)
        elif name == "pg_tables":
            return await self._pg_tables(conn, arguments)
        elif name == "pg_describe":
            return await self._pg_describe(conn, arguments)
        return self._text_error(f"Unknown tool: {name}")

    async def _pg_query(self, conn, args: Dict) -> Dict:
        query = args.get("query", "")
        params = args.get("params", [])
        cur = conn.cursor()
        try:
            cur.execute(query, params if params else None)
            if query.strip().upper().startswith("SELECT"):
                rows = cur.fetchall()
                cols = [desc[0] for desc in cur.description] if cur.description else []
                result = [dict(zip(cols, row)) for row in rows]
                return self._text_result(json.dumps(result, ensure_ascii=False, default=str, indent=2))
            else:
                conn.commit()
                return self._text_result(f"✅ {cur.rowcount} rows affected")
        except Exception as e:
            conn.rollback()
            return self._text_error(f"Query error: {e}")
        finally:
            cur.close()

    async def _pg_tables(self, conn, args: Dict) -> Dict:
        schema = args.get("schema", "public")
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT table_name, table_type, pg_size_pretty(pg_total_relation_size(quote_ident(table_name)))
                FROM information_schema.tables
                WHERE table_schema = %s
                ORDER BY table_name
            """, [schema])
            rows = cur.fetchall()
            result = [{"table": r[0], "type": r[1], "size": r[2]} for r in rows]
            return self._text_result(json.dumps(result, ensure_ascii=False, indent=2))
        finally:
            cur.close()

    async def _pg_describe(self, conn, args: Dict) -> Dict:
        table = args.get("table", "")
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns
                WHERE table_name = %s
                ORDER BY ordinal_position
            """, [table])
            rows = cur.fetchall()
            result = [{"column": r[0], "type": r[1], "nullable": r[2], "default": r[3]} for r in rows]
            return self._text_result(json.dumps(result, ensure_ascii=False, indent=2))
        finally:
            cur.close()


if __name__ == "__main__":
    server = PostgresMCPServer()
    asyncio.run(server.run())
