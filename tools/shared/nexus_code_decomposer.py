#!/usr/bin/env python3
"""
sofi_code_decomposer.py — مفكك الكود المتقدم
============================================
يساعد الوكلاء على تحليل وفهم أي مشروع
"""

import ast
from pathlib import Path
from typing import Dict, List, Any


class CodeDecomposer:
    """تحليل بنية المشروع وفهم الكود المعقد"""
    
    def __init__(self, root: str = "."):
        self.root = Path(root)
    
    def analyze_file(self, filepath: Path) -> Dict[str, Any]:
        """تحليل ملف برمجي"""
        try:
            source = filepath.read_text(encoding="utf-8")
            tree = ast.parse(source)
        except (SyntaxError, UnicodeDecodeError) as e:
            return {"file": str(filepath), "error": str(e)}
        
        analysis = {
            "file": str(filepath),
            "lines": len(source.splitlines()),
            "classes": [],
            "functions": [],
            "imports": [],
            "complexity": 0
        }
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                analysis["classes"].append({
                    "name": node.name,
                    "methods": len([n for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]),
                    "line": node.lineno
                })
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                analysis["functions"].append({
                    "name": node.name,
                    "line": node.lineno,
                    "args": [a.arg for a in node.args.args]
                })
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                mod = node.module if isinstance(node, ast.ImportFrom) else ""
                names = [a.name for a in node.names]
                analysis["imports"].append(f"{mod}: {names}")
        
        analysis["complexity"] = len(analysis["functions"]) + len(analysis["classes"])
        return analysis
    
    def scan_project(self) -> List[Dict[str, Any]]:
        """مسح المشروع بالكامل"""
        results = []
        for py_file in sorted(self.root.rglob("*.py")):
            skip = {"node_modules", ".venv", "__pycache__", ".git", "venv"}
            if any(s in str(py_file) for s in skip):
                continue
            results.append(self.analyze_file(py_file))
        return results
    
    def project_summary(self) -> Dict[str, Any]:
        """ملخص المشروع"""
        files = self.scan_project()
        total_classes = sum(len(f.get("classes", [])) for f in files)
        total_functions = sum(len(f.get("functions", [])) for f in files)
        total_lines = sum(f.get("lines", 0) for f in files)
        
        return {
            "total_files": len(files),
            "total_classes": total_classes,
            "total_functions": total_functions,
            "total_lines": total_lines,
            "avg_complexity": total_functions / max(len(files), 1)
        }


if __name__ == "__main__":
    decomposer = CodeDecomposer()
    summary = decomposer.project_summary()
    print(f"📊 ملخص المشروع:")
    print(f"   الملفات: {summary['total_files']}")
    print(f"   الكلاسات: {summary['total_classes']}")
    print(f"   الدوال: {summary['total_functions']}")
    print(f"   إجمالي الأسطر: {summary['total_lines']}")