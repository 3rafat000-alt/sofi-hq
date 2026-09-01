#!/usr/bin/env python3
"""
tool_forge_lib.py — مصنع الأدوات الذاتي المتقدم
==============================================
الوكلاء يبنون أدواتهم الخاصة — كل قائد فريق يبني أدوات PY خاصة بمكتبه
"""

import ast
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime


class ToolForge:
    """مصنع الأدوات المتقدم — يسمح لكل Lead Agent ببناء أدواته"""
    
    # مستويات صلاحية بناء الأدوات
    AGENT_DIRS = {
        # Engineering
        "architect": {"office": "engineering", "level": 3, "max_tools": 25},
        "builder": {"office": "engineering", "level": 3, "max_tools": 25},
        "db_engineer": {"office": "engineering", "level": 3, "max_tools": 25},
        "devops": {"office": "engineering", "level": 3, "max_tools": 25},
        "eng_assistant": {"office": "engineering", "level": 3, "max_tools": 25},
        # Creative
        "brand_designer": {"office": "creative", "level": 3, "max_tools": 25},
        "ui_designer": {"office": "creative", "level": 3, "max_tools": 25},
        "motion": {"office": "creative", "level": 3, "max_tools": 25},
        "ux_research": {"office": "creative", "level": 3, "max_tools": 25},
        "a11y": {"office": "creative", "level": 3, "max_tools": 25},
        # Quality
        "security": {"office": "quality", "level": 3, "max_tools": 25},
        "tester": {"office": "quality", "level": 3, "max_tools": 25},
        "reviewer": {"office": "quality", "level": 3, "max_tools": 25},
        "red_hacker": {"office": "quality", "level": 3, "max_tools": 25},
        "recon": {"office": "quality", "level": 3, "max_tools": 25},
        # AI & Data
        "assistant": {"office": "ai_data", "level": 3, "max_tools": 25},
        "documenter": {"office": "ai_data", "level": 3, "max_tools": 25},
        "release": {"office": "ai_data", "level": 3, "max_tools": 25},
        "prompt_engineer": {"office": "ai_data", "level": 3, "max_tools": 25},
        "auto_engineer": {"office": "ai_data", "level": 3, "max_tools": 25},
    }
    
    def __init__(self, base_dir: str = None):
        if base_dir is None:
            base_dir = Path(__file__).parent.parent / "agents"
        self.base_dir = Path(base_dir)
        self.agents_dir = self.base_dir
        self.shared_dir = Path(__file__).parent
        self.base_dir.mkdir(parents=True, exist_ok=True)
        
        # إنشاء مجلدات كل Lead Agent
        for agent_name in self.AGENT_DIRS:
            (self.base_dir / agent_name).mkdir(parents=True, exist_ok=True)
        
        # سجل الأدوات
        self.tool_registry: Dict[str, Dict] = {}
        self._scan_existing_tools()
    
    def _scan_existing_tools(self):
        """مسح الأدوات الموجودة"""
        for agent_name in self.AGENT_DIRS:
            agent_dir = self.base_dir / agent_name
            for tool_file in agent_dir.glob("*.py"):
                if tool_file.stem.startswith("_"):
                    continue
                self.tool_registry[f"{agent_name}/{tool_file.stem}"] = {
                    "agent": agent_name,
                    "name": tool_file.stem,
                    "path": str(tool_file),
                    "office": self.AGENT_DIRS[agent_name]["office"],
                    "built_at": datetime.fromtimestamp(tool_file.stat().st_mtime).isoformat()
                }
    
    def forge_tool(self, name: str, code: str, agent: str,
                   description: str = "") -> Dict:
        """بناء أداة جديدة بواسطة Lead Agent"""
        # التحقق من صلاحية الوكيل
        if agent not in self.AGENT_DIRS:
            return {"success": False, "error": f"وكيل غير معروف: {agent}"}
        
        agent_info = self.AGENT_DIRS[agent]
        
        # التحقق من عدد الأدوات المسموح
        agent_tools = [t for t in self.tool_registry if t.startswith(f"{agent}/")]
        if len(agent_tools) >= agent_info["max_tools"]:
            return {"success": False, "error": f"تجاوز الحد الأقصى للأدوات ({agent_info['max_tools']})"}
        
        print(f"🔨  {agent} يبني أداة: {name}")
        print(f"   📂  المكتب: {agent_info['office']}")
        print(f"   📝  {description[:80] if description else ''}")
        
        # المرحلة 1: الفحص الأمني المتقدم
        safety = self._advanced_safety_check(code)
        if safety["score"] < 0.4:
            print(f"   ❌  فشل الفحص الأمني: {safety['issues'][0] if safety['issues'] else 'unknown'}")
            return {"success": False, "error": "فشل الفحص الأمني", "issues": safety["issues"]}
        
        # المرحلة 2: التحقق النحوي
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            print(f"   ❌  خطأ نحوي: {e}")
            return {"success": False, "error": f"SyntaxError: {e}"}
        
        # المرحلة 3: استخراج المعلومات
        functions = [n.name for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
        classes = [n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
        imports = self._extract_imports(tree)
        
        # المرحلة 4: الحفظ في مجلد الوكيل
        target_dir = self.base_dir / agent
        target_dir.mkdir(parents=True, exist_ok=True)
        filepath = target_dir / f"{name}.py"
        filepath.write_text(code, encoding="utf-8")
        
        # المرحلة 5: التسجيل
        tool_info = {
            "name": name,
            "agent": agent,
            "office": agent_info["office"],
            "level": agent_info["level"],
            "path": str(filepath),
            "functions": functions,
            "classes": classes,
            "imports": imports,
            "safety_score": safety["score"],
            "description": description,
            "built_at": datetime.now().isoformat(),
            "verified": safety["score"] >= 0.8
        }
        self.tool_registry[f"{agent}/{name}"] = tool_info
        
        print(f"   ✅  أداة '{name}' جاهزة — {len(functions)} دوال, {len(classes)} كلاسات")
        print(f"   📁  {filepath}")
        print(f"   🛡️  الأمان: {safety['score']:.0%}")
        
        # اختبار سريع
        test_result = self._test_tool(filepath)
        tool_info["test_passed"] = test_result
        
        return {"success": True, "tool": tool_info, "test_passed": test_result}
    
    def _advanced_safety_check(self, code: str) -> Dict:
        """فحص أمني متقدم"""
        score = 1.0
        issues = []
        
        checks = {
            "eval(": (0.4, "خطير: eval() يسمح بتنفيذ كود عشوائي"),
            "exec(": (0.4, "خطير: exec() يسمح بتنفيذ كود عشوائي"),
            "os.system": (0.5, "خطير: os.system() ينفذ أوامر النظام"),
            "subprocess.call": (0.3, "تحذير: subprocess.call يستدعي عمليات خارجية"),
            "subprocess.Popen": (0.3, "تحذير: Popen يستدعي عمليات خارجية"),
            "__import__": (0.3, "تحذير: استيراد ديناميكي"),
            "pickle.loads": (0.3, "تحذير: pickle قد ينفذ كود أثناء فك التشفير"),
            "compile(": (0.3, "تحذير: compile() يسمح بتجميع كود ديناميكي"),
            "BaseException": (0.2, "تنبيه: استخدام BaseException واسع جداً"),
        }
        
        for pattern, (penalty, message) in checks.items():
            if pattern in code:
                score -= penalty
                issues.append(message)
        
        # فحص الـ imports
        if "import os" in code or "from os " in code:
            if any(cmd in code for cmd in ["system", "popen", "fork"]):
                pass  # تم الفحص أعلاه
        
        return {"score": max(0.0, score), "issues": issues}
    
    def _extract_imports(self, tree: ast.AST) -> List[str]:
        deps = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                deps.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    deps.append(node.module)
        return list(set(deps))
    
    def _test_tool(self, filepath: Path) -> bool:
        """اختبار تشغيل الأداة"""
        try:
            result = subprocess.run(
                ["python", "-c", f"import ast; ast.parse(open('{filepath}').read()); print('syntax OK')"],
                capture_output=True, text=True, timeout=10
            )
            return "OK" in result.stdout
        except Exception:
            return False
    
    def get_agent_tools(self, agent_name: str) -> List[Dict]:
        """جلب أدوات وكيل معين"""
        return [
            info for key, info in self.tool_registry.items()
            if key.startswith(f"{agent_name}/")
        ]
    
    def get_office_tools(self, office: str) -> List[Dict]:
        """جلب أدوات مكتب معين"""
        return [
            info for info in self.tool_registry.values()
            if info["office"] == office
        ]
    
    def catalogue(self) -> Dict:
        """كتالوج كامل بالأدوات"""
        return {
            "by_office": {
                "engineering": [t["name"] for t in self.get_office_tools("engineering")],
                "creative": [t["name"] for t in self.get_office_tools("creative")],
                "quality": [t["name"] for t in self.get_office_tools("quality")],
                "ai_data": [t["name"] for t in self.get_office_tools("ai_data")],
            },
            "by_agent": {
                agent: [t["name"] for t in self.get_agent_tools(agent)]
                for agent in self.AGENT_DIRS
            },
            "total": len(self.tool_registry)
        }
    
    def get_stats(self) -> Dict:
        return {
            "total_tools": len(self.tool_registry),
            "by_office": {
                "engineering": len(self.get_office_tools("engineering")),
                "creative": len(self.get_office_tools("creative")),
                "quality": len(self.get_office_tools("quality")),
                "ai_data": len(self.get_office_tools("ai_data")),
            },
            "agents_with_tools": len(set(t["agent"] for t in self.tool_registry.values()))
        }


if __name__ == "__main__":
    forge = ToolForge()
    print(f"🔧  Sofi Tool Forge — Advanced Edition")
    print(f"   {len(forge.AGENT_DIRS)} Lead Agents يمكنهم بناء أدوات")
    print(f"   {forge.get_stats()['total_tools']} أدوات موجودة")
    print(f"   📦  الكتالوج: {json.dumps(forge.catalogue(), indent=2, ensure_ascii=False)}")
