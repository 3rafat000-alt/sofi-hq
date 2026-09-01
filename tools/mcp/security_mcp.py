#!/usr/bin/env python3
"""
🛡️ Sofi Security MCP Server — أدوات الأمن السيبراني المتقدمة
===============================================================
JSON-RPC 2.0 stdio MCP server for security scanning, dependency audit, config checks
"""

import sys
import os
import asyncio
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tools.mcp.base import SofiBaseMCP
import json
import re
import subprocess
from typing import Dict, List
from pathlib import Path


TOOLS = [
    {
        "name": "scan_security",
        "description": "فحص أمني للملفات — Scan files for security vulnerabilities",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "File or directory to scan", "default": "."},
                "recursive": {"type": "boolean", "description": "Scan recursively", "default": True}
            }
        }
    },
    {
        "name": "check_dependencies",
        "description": "فحص التبعيات — Check dependencies for known vulnerabilities",
        "inputSchema": {
            "type": "object",
            "properties": {
                "file": {"type": "string", "description": "Path to requirements.txt or package.json"}
            }
        }
    },
    {
        "name": "audit_config",
        "description": "تدقيق الإعدادات — Audit configuration files for security issues",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Directory to audit", "default": "."}
            }
        }
    },
    {
        "name": "sast_scan",
        "description": "تحليل ثابت SAST — Static Application Security Testing",
        "inputSchema": {
            "type": "object",
            "properties": {
                "file": {"type": "string", "description": "Python file to analyze"},
                "severity": {
                    "type": "string",
                    "description": "Minimum severity level",
                    "enum": ["low", "medium", "high", "critical"],
                    "default": "medium"
                }
            },
            "required": ["file"]
        }
    }
]

DANGEROUS_PATTERNS = {
    "critical": [
        (r"os\.system\s*\(", "تنفيذ أوامر النظام (os.system)"),
        (r"subprocess\.[a-z]+\s*\(", "تنفيذ أوامر فرعية (subprocess)"),
        (r"eval\s*\(", "تقييم كود ديناميكي (eval)"),
        (r"exec\s*\(", "تنفيذ كود ديناميكي (exec)"),
        (r"pickle\.loads?\s*\(", "إلغاء تسلسل غير آمن (pickle)"),
        (r"__import__\s*\(", "استيراد ديناميكي (__import__)"),
    ],
    "high": [
        (r"sqlite3\.execute\s*\([^)]*%", "حقن SQL محتمل (format string)"),
        (r"cursor\.execute\s*\([^)]*\+", "حقن SQL محتمل (concatenation)"),
        (r"request\.(get|post|put|delete)\s*\(", "طلب ويب خارجي"),
        (r"base64\.(b64decode|b64encode)\s*\(", "ترميز Base64"),
    ],
    "medium": [
        (r"tempfile\.", "استخدام الملفات المؤقتة"),
        (r"open\s*\([^)]*['\"]w['\"]", "فتح ملف للكتابة"),
        (r"shutil\.rmtree\s*\(", "حذف مجلدات (rmtree)"),
        (r"marshal\.", "استخدام marshal"),
    ],
}


def _scan_file(filepath: str) -> List[Dict]:
    findings = []
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        for severity, patterns in DANGEROUS_PATTERNS.items():
            for pattern, desc in patterns:
                for match in re.finditer(pattern, content):
                    line_num = content[:match.start()].count("\n") + 1
                    findings.append({
                        "file": filepath,
                        "line": line_num,
                        "severity": severity,
                        "description": desc,
                        "match": match.group()[:60]
                    })
    except Exception as e:
        findings.append({"file": filepath, "severity": "low", "description": f"Cannot read: {e}", "line": 0})
    return findings


def _audit_python_deps(filepath: str) -> List[Dict]:
    issues = []
    try:
        with open(filepath) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    pkg = re.split(r"[=<>~!]", line)[0].strip()
                    if pkg:
                        try:
                            r = subprocess.run(
                                ["pip", "audit", pkg, "--output-format=json"],
                                capture_output=True, text=True, timeout=15
                            )
                            if r.returncode == 0 and r.stdout.strip():
                                issues.extend(json.loads(r.stdout))
                        except:
                            pass
    except:
        pass
    return issues


class SecurityMCPServer(SofiBaseMCP):
    def __init__(self):
        super().__init__("🛡️ Security MCP", "1.0.0", TOOLS)

    async def handle_tool_call(self, name: str, arguments: Dict) -> Dict:
        if name == "scan_security":
            return await self._scan_security(arguments)
        elif name == "check_dependencies":
            return await self._check_dependencies(arguments)
        elif name == "audit_config":
            return await self._audit_config(arguments)
        elif name == "sast_scan":
            return await self._sast_scan(arguments)
        return self._text_error(f"Unknown tool: {name}")

    async def _scan_security(self, args: Dict) -> Dict:
        scan_path = args.get("path", ".")
        recursive = args.get("recursive", True)
        path = Path(scan_path).resolve()
        all_findings = []
        if path.is_file():
            all_findings.extend(_scan_file(str(path)))
        elif path.is_dir():
            glob = "**/*.py" if recursive else "*.py"
            for f in path.glob(glob):
                all_findings.extend(_scan_file(str(f)))
        critical = [f for f in all_findings if f["severity"] == "critical"]
        high = [f for f in all_findings if f["severity"] == "high"]
        medium = [f for f in all_findings if f["severity"] == "medium"]
        low = [f for f in all_findings if f["severity"] == "low"]
        summary = {
            "total": len(all_findings),
            "critical": len(critical),
            "high": len(high),
            "medium": len(medium),
            "low": len(low),
            "findings": all_findings[:50]
        }
        return self._text_result(json.dumps(summary, ensure_ascii=False, indent=2))

    async def _check_dependencies(self, args: Dict) -> Dict:
        filepath = args.get("file", "")
        if not filepath:
            return self._text_result("⚠️ يرجى تحديد ملف requirements.txt أو package.json")
        p = Path(filepath)
        if not p.exists():
            return self._text_error(f"الملف غير موجود: {filepath}")
        if p.name == "requirements.txt":
            issues = _audit_python_deps(str(p))
            if not issues:
                return self._text_result("✅ لم يتم العثور على ثغرات معروفة")
            return self._text_result(json.dumps(issues, ensure_ascii=False, indent=2))
        elif p.name == "package.json":
            try:
                r = subprocess.run(["npm", "audit", "--json"], cwd=str(p.parent),
                                   capture_output=True, text=True, timeout=30)
                if r.returncode == 0:
                    data = json.loads(r.stdout) if r.stdout.strip() else {}
                    return self._text_result(json.dumps(data, ensure_ascii=False, indent=2)[:5000])
                return self._text_error(f"npm audit failed: {r.stderr[:500]}")
            except Exception as e:
                return self._text_error(f"npm audit error: {e}")
        return self._text_error("الملف غير معروف. استخدم requirements.txt أو package.json")

    async def _audit_config(self, args: Dict) -> Dict:
        audit_path = args.get("path", ".")
        path = Path(audit_path).resolve()
        issues = []
        config_files = [
            ("*.env", "ملف بيئة يحتوي على secrets محتملة", "high"),
            ("*.pem", "مفتاح خاص (private key)", "critical"),
            ("*.key", "مفتاح خاص (private key)", "critical"),
            (".gitignore", "Git ignore file", "low"),
            ("Dockerfile", "Dockerfile — تحقق من USER root", "medium"),
            ("docker-compose*.yml", "Docker Compose", "low"),
        ]
        for glob_pattern, desc, severity in config_files:
            for f in path.glob(glob_pattern):
                rel = f.relative_to(path)
                issues.append({"file": str(rel), "severity": severity, "description": desc, "line": 0})
        return self._text_result(json.dumps({
            "total_configs": len(issues),
            "issues": issues
        }, ensure_ascii=False, indent=2))

    async def _sast_scan(self, args: Dict) -> Dict:
        filepath = args.get("file", "")
        severity = args.get("severity", "medium")
        p = Path(filepath)
        if not p.exists():
            return self._text_error(f"الملف غير موجود: {filepath}")
        findings = _scan_file(str(p))
        levels = {"low": 0, "medium": 1, "high": 2, "critical": 3}
        min_level = levels.get(severity, 1)
        filtered = [f for f in findings if levels.get(f["severity"], 0) >= min_level]
        scores = {"critical": 10, "high": 7, "medium": 4, "low": 1}
        score = sum(scores.get(f["severity"], 0) for f in filtered)
        return self._text_result(json.dumps({
            "file": str(p),
            "total": len(filtered),
            "score": min(score, 100),
            "risk": "high" if score > 20 else "medium" if score > 10 else "low",
            "findings": filtered
        }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    server = SecurityMCPServer()
    asyncio.run(server.run())
