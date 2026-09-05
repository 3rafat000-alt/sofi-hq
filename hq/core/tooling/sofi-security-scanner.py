#!/usr/bin/env python3
"""FILE: hq/core/tooling/sofi-security-scanner.py
sofi-security-scanner — periodic security scan (audit suggestion Phase 3)
Runs gitleaks + evidence_guard as a combined security surface check.
"""
import subprocess, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[3]
def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    print(r.stdout, end=""); return r.returncode
if __name__ == "__main__":
    c1 = run(["gitleaks", "detect", "--no-git", "-v"])
    c2 = run([sys.executable, str(ROOT/"hq/core/tooling/evidence_guard.py"), "hq/core", "--strict"])
    sys.exit(0 if c1==0 or c2==0 else 1)
