#!/usr/bin/env python3
"""
sofi-security-scanner — periodic security scan (audit suggestion)
Runs gitleaks + evidence_guard as a combined security surface check.
"""
import subprocess, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    print(r.stdout, end=""); return r.returncode
if __name__ == "__main__":
    c1 = run(["gitleaks", "detect", "--no-git", "-v"])
    c2 = run([sys.executable, str(ROOT/"hq/core/tooling/evidence_guard.py"), "hq/core", "--strict"])
    sys.exit(0 if c1==0 or c2==0 else 1)
