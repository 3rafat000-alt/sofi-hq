#!/usr/bin/env python3
"""
🔧 Sofi Chrome DevTools MCP Server — تحليل أداء الواجهات وفحص الكود
====================================================================
JSON-RPC 2.0 stdio MCP server for web performance, accessibility, SEO analysis
"""

import sys
import os
import asyncio
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tools.mcp.base import SofiBaseMCP
import json
import re
from typing import Dict
from pathlib import Path
from urllib.parse import urlparse


TOOLS = [
    {
        "name": "analyze_html",
        "description": "تحليل HTML — Analyze HTML for performance, a11y, SEO issues",
        "inputSchema": {
            "type": "object",
            "properties": {
                "file": {"type": "string", "description": "HTML file path or URL to analyze"},
                "checks": {
                    "type": "array",
                    "description": "Checks to run: performance, accessibility, seo, all",
                    "items": {"type": "string"},
                    "default": ["all"]
                }
            },
            "required": ["file"]
        }
    },
    {
        "name": "audit_css",
        "description": "تدقيق CSS — Audit CSS for unused styles, performance",
        "inputSchema": {
            "type": "object",
            "properties": {
                "file": {"type": "string", "description": "CSS file path"}
            },
            "required": ["file"]
        }
    },
    {
        "name": "check_js",
        "description": "فحص JS — Check JavaScript for console.log, errors, best practices",
        "inputSchema": {
            "type": "object",
            "properties": {
                "file": {"type": "string", "description": "JavaScript file path"}
            },
            "required": ["file"]
        }
    },
    {
        "name": "analyze_page_size",
        "description": "تحليل حجم الصفحة — Analyze page resources and sizes",
        "inputSchema": {
            "type": "object",
            "properties": {
                "directory": {"type": "string", "description": "Project directory", "default": "."}
            }
        }
    }
]


class ChromeDevToolsMCPServer(SofiBaseMCP):
    def __init__(self):
        super().__init__("🔧 Chrome DevTools MCP", "1.0.0", TOOLS)

    async def handle_tool_call(self, name: str, arguments: Dict) -> Dict:
        if name == "analyze_html":
            return await self._analyze_html(arguments)
        elif name == "audit_css":
            return await self._audit_css(arguments)
        elif name == "check_js":
            return await self._check_js(arguments)
        elif name == "analyze_page_size":
            return await self._analyze_page_size(arguments)
        return self._text_error(f"Unknown tool: {name}")

    async def _analyze_html(self, args: Dict) -> Dict:
        filepath = args.get("file", "")
        checks = args.get("checks", ["all"])
        p = Path(filepath)
        if not p.exists():
            return self._text_error(f"الملف غير موجود: {filepath}")
        content = p.read_text(encoding="utf-8", errors="ignore")
        results = {"html_file": str(p), "issues": [], "score": 100}

        if "all" in checks or "seo" in checks:
            if not re.search(r'<title>', content, re.I):
                results["issues"].append({"type": "seo", "severity": "high", "msg": "🚫 لا يوجد وسم <title>"})
                results["score"] -= 15
            if not re.search(r'<meta\s+[^>]*name=["\']description["\']', content, re.I):
                results["issues"].append({"type": "seo", "severity": "medium", "msg": "⚠️ لا يوجد meta description"})
                results["score"] -= 10
            if not re.search(r'<h1>', content, re.I):
                results["issues"].append({"type": "seo", "severity": "medium", "msg": "⚠️ لا يوجد <h1>"})
                results["score"] -= 8
            if not re.search(r'<html[^>]*lang=',
                             content, re.I):
                results["issues"].append({"type": "seo", "severity": "low", "msg": "📝 لا يوجد lang attribute"})
                results["score"] -= 3

        if "all" in checks or "accessibility" in checks:
            imgs = re.findall(r'<img\s+[^>]*>', content, re.I)
            for img in imgs:
                if not re.search(r'alt\s*=', img, re.I):
                    results["issues"].append({"type": "a11y", "severity": "high",
                                              "msg": f"🚫 صورة بدون alt: {img[:50]}..."})
                    results["score"] -= 5
            if not re.search(r'role\s*=', content, re.I):
                results["issues"].append({"type": "a11y", "severity": "medium",
                                          "msg": "📝 لا يوجد ARIA roles"})
                results["score"] -= 5
            if not re.search(r'aria-', content, re.I):
                results["issues"].append({"type": "a11y", "severity": "low",
                                          "msg": "📝 لا يوجد ARIA attributes"})
                results["score"] -= 3

        if "all" in checks or "performance" in checks:
            scripts = re.findall(r'<script\s+[^>]*src=["\']([^"\']+)["\']', content, re.I)
            styles = re.findall(r'<link\s+[^>]*href=["\']([^"\']+)["\']', content, re.I)
            results["resources"] = {
                "scripts": len(scripts),
                "stylesheets": len(styles),
                "script_files": scripts[:10],
                "css_files": styles[:10]
            }
            if len(scripts) > 10:
                results["issues"].append({"type": "performance", "severity": "medium",
                                           "msg": f"⚠️ {len(scripts)} سكريبت — قد يبطئ التحميل"})
                results["score"] -= 5
            if not re.search(r'<link[^>]*rel=["\']preload["\']', content, re.I):
                results["issues"].append({"type": "performance", "severity": "low",
                                           "msg": "📝 لا يوجد preload hints"})
                results["score"] -= 3

        results["score"] = max(0, results["score"])
        results["grade"] = "A" if results["score"] >= 90 else "B" if results["score"] >= 75 else "C" if results["score"] >= 50 else "F"
        return self._text_result(json.dumps(results, ensure_ascii=False, indent=2))

    async def _audit_css(self, args: Dict) -> Dict:
        filepath = args.get("file", "")
        p = Path(filepath)
        if not p.exists():
            return self._text_error(f"الملف غير موجود: {filepath}")
        content = p.read_text(encoding="utf-8", errors="ignore")
        results = {"file": str(p), "size_bytes": len(content), "issues": []}
        lines = content.split("\n")
        selector_count = len(re.findall(r'\{', content))
        results["selectors"] = selector_count
        if selector_count > 1000:
            results["issues"].append(f"⚠️ {selector_count} منتقى — كثير جداً")
        important_count = content.count("!important")
        if important_count > 10:
            results["issues"].append(f"⚠️ {important_count} !important — مشكلة في الخصوصية")
        vendor_prefixes = len(re.findall(r'-\w+-\w+:', content))
        if vendor_prefixes > 50:
            results["issues"].append(f"⚠️ {vendor_prefixes} بادئة متصفح — استخدم Autoprefixer")
        return self._text_result(json.dumps(results, ensure_ascii=False, indent=2))

    async def _check_js(self, args: Dict) -> Dict:
        filepath = args.get("file", "")
        p = Path(filepath)
        if not p.exists():
            return self._text_error(f"الملف غير موجود: {filepath}")
        content = p.read_text(encoding="utf-8", errors="ignore")
        results = {"file": str(p), "lines": len(content.split("\n")), "warnings": []}
        if re.search(r'console\.(log|debug|info)\s*\(', content):
            results["warnings"].append("📝 console.log موجود — ازله للإنتاج")
        if re.search(r'alert\s*\(', content):
            results["warnings"].append("⚠️ alert() موجود — ضار أو خطأ")
        if re.search(r'debugger;', content):
            results["warnings"].append("🚫 debugger موجود — أزله فوراً")
        if re.search(r'document\.write\s*\(', content):
            results["warnings"].append("🚫 document.write() — ضار بالأداء")
        if re.search(r'innerHTML\s*=', content):
            results["warnings"].append("⚠️ innerHTML — عرضة لـ XSS، استخدم textContent")
        if re.search(r'eval\s*\(', content):
            results["warnings"].append("🚫 eval() — خطر أمني")
        func_count = len(re.findall(r'function\s+\w+\s*\(', content))
        arrow_count = len(re.findall(r'=\s*\(?\w*\)?\s*=>', content))
        results["functions"] = func_count + arrow_count
        return self._text_result(json.dumps(results, ensure_ascii=False, indent=2))

    async def _analyze_page_size(self, args: Dict) -> Dict:
        directory = args.get("directory", ".")
        path = Path(directory).resolve()
        if not path.is_dir():
            return self._text_error(f"المجلد غير موجود: {directory}")
        sizes = {}
        for ext in ["*.html", "*.css", "*.js", "*.png", "*.jpg", "*.svg", "*.json"]:
            total = sum(f.stat().st_size for f in path.rglob(ext))
            count = len(list(path.rglob(ext)))
            sizes[ext.replace("*", "")] = {"count": count, "total_bytes": total, "total_kb": round(total / 1024, 1)}
        total = sum(v["total_bytes"] for v in sizes.values())
        return self._text_result(json.dumps({
            "resources": sizes,
            "total_kb": round(total / 1024, 1),
            "total_mb": round(total / 1024 / 1024, 2)
        }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    server = ChromeDevToolsMCPServer()
    asyncio.run(server.run())
