#!/usr/bin/env python3
"""
sofi-audit — unified wrapper for registry_guard + count_sync
Audit gap: "دمج الأدوات المتشابهة" — audit 2026-09-05 recommended merging.
This wrapper runs both guards sequentially and reports unified PASS/FAIL.
Law 12 + 13 — does not replace the individual guards, only wraps them.
"""
import subprocess, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    print(r.stdout, end=""); print(r.stderr, end="", file=sys.stderr); return r.returncode
if __name__ == "__main__":
    c1 = run([sys.executable, str(ROOT/"hq/core/tooling/registry_guard.py"), "--strict"])
    c2 = run([sys.executable, str(ROOT/"hq/core/tooling/count_sync.py")])
    sys.exit(0 if c1==0 and c2==0 else 1)
