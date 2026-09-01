#!/usr/bin/env python3
"""
Sofi MCP Base — Shared MCP Protocol Handler
===============================================
قاعدة لكل خوادم MCP — تتعامل مع JSON-RPC 2.0 عبر stdio
كل خادم يمد كلاس `SofiBaseMCP` وينفذ `handle_tool_call()`
"""

import sys
import os
import json
import asyncio
import contextlib
from typing import Any, Dict, List, Optional, Callable

# تأكد من مسار المشروع
_project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)
os.chdir(_project_root)


class SofiBaseMCP:
    """قاعدة خوادم MCP — تدير بروتوكول JSON-RPC 2.0 عبر stdio"""
    
    def __init__(self, server_name: str, server_version: str = "1.0.0",
                 tools: List[Dict] = None):
        self.server_name = server_name
        self.server_version = server_version
        self.tools = tools or []
        self.initialized = False
    
    @contextlib.contextmanager
    def _silence_stdout(self):
        """تحويلة print() إلى stderr عشان JSON ما يتلخبط"""
        old_stdout = sys.stdout
        sys.stdout = sys.stderr
        try:
            yield
        finally:
            sys.stdout = old_stdout
    
    def _send(self, msg: Dict):
        line = json.dumps(msg, ensure_ascii=False)
        sys.stdout.write(line + "\n")
        sys.stdout.flush()
    
    def _log(self, msg: str):
        sys.stderr.write(f"[{self.server_name}] {msg}\n")
        sys.stderr.flush()
    
    def _text_result(self, text: str) -> Dict:
        return {"content": [{"type": "text", "text": text}]}
    
    def _text_error(self, text: str) -> Dict:
        return {"isError": True, "content": [{"type": "text", "text": text}]}
    
    async def handle_tool_call(self, name: str, arguments: Dict) -> Dict:
        """تجاوز هذه الدالة في الخادمات الفردية"""
        return self._text_error(f"أداة غير معروفة: {name}")
    
    async def _handle_initialize(self, params: Dict) -> Dict:
        self.initialized = True
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}},
            "serverInfo": {"name": self.server_name, "version": self.server_version}
        }
    
    async def _handle_tools_list(self, params: Dict) -> Dict:
        return {"tools": self.tools}
    
    async def handle_message(self, msg: Dict):
        method = msg.get("method", "")
        params = msg.get("params", {})
        msg_id = msg.get("id")
        
        try:
            if method == "initialize":
                result = await self._handle_initialize(params)
                if msg_id is not None:
                    self._send({"jsonrpc": "2.0", "id": msg_id, "result": result})
            
            elif method == "notifications/initialized":
                self._log("Client initialized")
            
            elif method == "tools/list":
                result = await self._handle_tools_list(params)
                if msg_id is not None:
                    self._send({"jsonrpc": "2.0", "id": msg_id, "result": result})
            
            elif method == "tools/call":
                name = params.get("name", "")
                arguments = params.get("arguments", {})
                result = await self.handle_tool_call(name, arguments)
                if msg_id is not None:
                    self._send({"jsonrpc": "2.0", "id": msg_id, "result": result})
            
            elif method == "notifications/cancelled":
                self._log(f"Cancelled: {params}")
            
            else:
                self._log(f"Unknown method: {method}")
                if msg_id is not None:
                    self._send({
                        "jsonrpc": "2.0", "id": msg_id,
                        "error": {"code": -32601, "message": f"Method not found: {method}"}
                    })
        except Exception as e:
            self._log(f"Error: {e}")
            if msg_id is not None:
                self._send({
                    "jsonrpc": "2.0", "id": msg_id,
                    "result": self._text_error(str(e))
                })
    
    async def run(self):
        self._log(f"Starting...")
        while True:
            line = sys.stdin.readline()
            if not line:
                break
            line = line.strip()
            if not line:
                continue
            try:
                msg = json.loads(line)
                await self.handle_message(msg)
            except json.JSONDecodeError as e:
                self._log(f"Invalid JSON: {e}")
