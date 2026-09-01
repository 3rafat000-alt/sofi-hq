#!/usr/bin/env python3
"""
Sofi MCP Broker — Tool Builder
=================================
باني الأدوات — كل قائد فريق يبني أدواته الخاصة ببايثون
"""

import ast
import importlib.util
import inspect
import uuid
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class BuiltTool:
    """أداة تم بناؤها بواسطة وكيل"""
    id: str = ""
    name: str = ""
    version: str = "1.0.0"
    description: str = ""
    author: str = ""
    author_office: str = ""
    agent_level: int = 3  # 3=Lead, 4=Micro
    filepath: str = ""
    source_code: str = ""
    dependencies: List[str] = field(default_factory=list)
    safety_score: float = 1.0  # 0.0 to 1.0
    usage_count: int = 0
    verified: bool = False
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    last_used: str = ""


class ToolBuilder:
    """مصنع الأدوات — كل Lead Agent يبني أدواته"""
    
    def __init__(self, base_dir: str = None):
        if base_dir is None:
            base_dir = str(Path(__file__).parent.parent / "agents")
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.built_tools: Dict[str, BuiltTool] = {}
        self._load_existing()
    
    def _load_existing(self):
        """تحميل الأدوات الموجودة"""
        for tool_file in self.base_dir.rglob("*.py"):
            if tool_file.stem.startswith("_"):
                continue
            rel_path = tool_file.relative_to(self.base_dir)
            tool = BuiltTool(
                id=str(uuid.uuid4())[:8],
                name=tool_file.stem,
                filepath=str(rel_path),
                source_code=tool_file.read_text(),
                author=str(rel_path.parent) if rel_path.parent else "shared",
                author_office=self._detect_office(str(rel_path)),
                agent_level=3
            )
            self.built_tools[tool.name] = tool
    
    def _detect_office(self, path: str) -> str:
        if "architect" in path or "builder" in path or "db_" in path or "devops" in path or "eng" in path:
            return "engineering"
        if "brand_designer" in path or "ui_" in path or "motion" in path or "ux_" in path or "a11y" in path:
            return "creative"
        if "security" in path or "tester" in path or "reviewer" in path or "hacker" in path or "recon" in path:
            return "quality"
        if "assistant" in path or "documenter" in path or "release" in path or "prompt" in path or "auto" in path:
            return "ai_data"
        return "unknown"
    
    def build_tool(self, name: str, author: str, author_office: str,
                    agent_level: int, code: str,
                    description: str = "") -> BuiltTool:
        """بناء أداة جديدة — مع فحص أمني وتجميع"""
        # 1. الفحص الأمني
        safety = self._safety_check(code)
        if safety < 0.3:
            return BuiltTool(
                name=name, description="❌ رفض الأمان: كود خطير",
                safety_score=safety
            )
        
        # 2. التحقق من الصحة النحوية
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return BuiltTool(
                name=name, description=f"❌ خطأ نحوي: {e}",
                safety_score=0.0
            )
        
        # 3. استخراج التبعيات
        dependencies = self._extract_dependencies(tree)
        
        # 4. حفظ الملف
        filepath = self.base_dir / author.replace(" ", "_").lower() / f"{name}.py"
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(code)
        
        # 5. تسجيل الأداة
        tool = BuiltTool(
            id=str(uuid.uuid4())[:8],
            name=name,
            description=description,
            author=author,
            author_office=author_office,
            agent_level=agent_level,
            filepath=str(filepath.relative_to(self.base_dir.parent.parent)),
            source_code=code,
            dependencies=dependencies,
            safety_score=safety,
            verified=safety >= 0.8
        )
        self.built_tools[name] = tool
        
        print(f"🔨  أداة جديدة: {name} بقلم {author} ({author_office})")
        print(f"   📁  {filepath}")
        print(f"   🛡️  الأمان: {safety:.0%}")
        
        return tool
    
    def _safety_check(self, code: str) -> float:
        """فحص أمني للكود — يمنع الأنماط الخطرة"""
        score = 1.0
        
        dangerous_patterns = {
            "eval(": -0.4, "exec(": -0.4, "__import__": -0.3,
            "os.system": -0.5, "subprocess.call": -0.3,
            "subprocess.Popen": -0.3, "pickle.loads": -0.3,
            "BaseException": -0.2, "compile(": -0.3
        }
        
        for pattern, penalty in dangerous_patterns.items():
            if pattern in code:
                score += penalty
        
        return max(0.0, min(1.0, score))
    
    def _extract_dependencies(self, tree: ast.AST) -> List[str]:
        """استخراج الـ imports من الكود"""
        deps = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                deps.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    deps.append(node.module.split('.')[0])
        return list(set(deps))
    
    def get_tool(self, name: str) -> Optional[BuiltTool]:
        return self.built_tools.get(name)
    
    def get_tools_by_author(self, author: str) -> List[BuiltTool]:
        return [t for t in self.built_tools.values() if t.author == author]
    
    def get_tools_by_office(self, office: str) -> List[BuiltTool]:
        return [t for t in self.built_tools.values() if t.author_office == office]
    
    def get_all_tools(self) -> Dict[str, BuiltTool]:
        return dict(self.built_tools)
    
    def run_tool(self, name: str, *args, **kwargs) -> Any:
        """تشغيل أداة مبنية"""
        tool = self.built_tools.get(name)
        if not tool:
            raise ValueError(f"الأداة '{name}' غير موجودة")
        
        filepath = self.base_dir.parent.parent / tool.filepath
        if not filepath.exists():
            raise FileNotFoundError(f"ملف الأداة غير موجود: {filepath}")
        
        # استيراد الوحدة
        spec = importlib.util.spec_from_file_location(tool.name, filepath)
        if not spec or not spec.loader:
            raise ImportError(f"لا يمكن تحميل الأداة: {name}")
        
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        tool.usage_count += 1
        tool.last_used = datetime.now().isoformat()
        
        # البحث عن الدالة الرئيسية
        for attr_name in dir(module):
            if not attr_name.startswith('_'):
                attr = getattr(module, attr_name)
                if callable(attr) and not isinstance(attr, type):
                    return attr(*args, **kwargs)
        
        raise AttributeError(f"لا توجد دالة قابلة للاستدعاء في الأداة: {name}")
    
    def get_stats(self) -> dict:
        return {
            "total_tools": len(self.built_tools),
            "by_office": {
                "engineering": len(self.get_tools_by_office("engineering")),
                "creative": len(self.get_tools_by_office("creative")),
                "quality": len(self.get_tools_by_office("quality")),
                "ai_data": len(self.get_tools_by_office("ai_data"))
            },
            "total_usage": sum(t.usage_count for t in self.built_tools.values()),
            "verified_tools": sum(1 for t in self.built_tools.values() if t.verified)
        }
