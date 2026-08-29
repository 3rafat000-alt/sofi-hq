## FILE: hq/engine/mcp_server/tests/test_memory.py
"""Memory tests — Law 7 separation and append."""
import tempfile
from pathlib import Path
import hq.engine.mcp_server.memory as memory

def test_write_decision_appends():
    tmp = tempfile.mkdtemp()
    orig_cortex = memory.CORTEX
    memory.CORTEX = Path(tmp) / "cortex-decisions.md"
    line = memory.write_decision("اعتمدنا SQLite", room="bck-lead", evidence="hq/engine/mcp_server/memory.py:1")
    assert "اعتمدنا SQLite" in line
    assert "evidence:" in line
    assert Path(tmp, "cortex-decisions.md").read_text(encoding="utf-8").count("اعتمدنا SQLite") == 1
    memory.write_decision("قرار ثاني", room="arc-lead")
    text = Path(tmp, "cortex-decisions.md").read_text(encoding="utf-8")
    assert "قرار ثاني" in text
    assert text.count("- [") == 2
    memory.CORTEX = orig_cortex

def test_write_incident():
    tmp = tempfile.mkdtemp()
    orig = memory.AMYGDALA
    memory.AMYGDALA = Path(tmp) / "amygdala.md"
    line = memory.write_incident("حادث اختبار", severity="high")
    assert "حادث اختبار" in line
    memory.AMYGDALA = orig
