---
name: sec-threat-model
description: >-
  Threat modeling and security gate playbook — STRIDE + vulnerability scanning + penetration testing + secrets audit + security veto decision (brd-cso holds absolute veto). Triggers — "threat model this", "security gate", "STRIDE analysis", "is this secure", "pre-launch security review", "attack surface", "security sign-off", "model the threat", "what are this feature's risks", "scan for vulnerabilities". Invoked before launching/merging any feature touching authentication, sensitive data, or a new attack surface — **and before signing DFR for any ERD/contract/designs touching sensitive data (DFR mode: mandatory paper review)**.
---

# sec-threat-model — Threat Model & Security Gate ⬛

> **Value:** one unified security gate before launch — turning "we think it's safe" into an evidence-based decision while preserving brd-cso's absolute security veto.

## 🎯 When to invoke (When) ⬛
- Before launching/merging a feature touching authentication, permissions, payments, or KYC/PII data.
- When introducing a new attack surface: endpoint, external integration, file upload, webhook.
- When brd-ceo/sec-lead request a "security gate" or "security sign-off" before the launch gate.
- After a security incident — to re-assess the model before resuming work.

**Do not invoke** for: general code review with no security dimension (that's qa/bck), nor fixing a single known vulnerability without modeling (that's direct execution via sec-appsec-engineer).

## 📥 Required inputs (Inputs) ⬛
- **A formal RCCF work order (Law 5)** — no execution without it. Violation = L2.
- The scope of the asset being modeled: feature/service, data flow diagram (DFD), trust boundaries.
- The sensitive assets involved (PII/KYC/secrets/keys) and their classification level.
- The authorized testing environment (staging) — no penetration testing on production without CEO authorization.

## 🔧 Steps (Steps) ⬛
1. **RCCF gate:** verify the work order exists and read its scope. Missing → halt and notify sec-lead (L2).
2. **STRIDE modeling** (delegate `sec-threat-modeler` via sec-lead): for every DFD element classify the threat — Spoofing / Tampering / Repudiation / Information disclosure / Denial of service / Elevation of privilege — with a risk rating (likelihood × impact) per item.
3. **Vulnerability scan** (delegate `sec-appsec-engineer`): SAST/DAST/dependencies (CVE); log every finding with `file:line` + CVE id + severity.
4. **Penetration testing** (delegate `sec-pentester`): on authorized staging only; prove exploitation with a PoC + reproduction steps, never theoretical claims.
5. **Secrets audit** (delegate `sec-secrets-warden`): check exposed secrets, key rotation, encryption at rest; log path:line for any leak.
6. **Review & consolidation (Law 8):** sec-lead unifies findings, deduplicates, links each STRIDE item to a mitigation control with status (fixed/accepted-with-justification/open).
7. **Security gate decision:** issue the verdict — `PASS` / `PASS-WITH-CONDITIONS` / `FAIL`. Any open Critical/High item = `FAIL`.
8. **Security veto (Law 6):** sec-lead escalates the decision + evidence block to **brd-ceo**, who consults **brd-cso**; brd-cso's veto on any launch is absolute and final. Never address the Board directly (Law 2).
9. **Emergencies:** any actively exploited vulnerability or secrets leak = an emergency — record it immediately in `hq/brain/amygdala-incidents.md` (Law 7) and escalate to sec-lead then brd-ceo.
10. Produce the evidence block (below) via `sofi-evidence`.

## 📤 Outputs + evidence (Outputs & Evidence) ⬛
- **Output:** one unified security gate report = STRIDE matrix + vulnerability log + pentest report + secrets audit + gate verdict (PASS/CONDITIONS/FAIL) + brd-cso veto status.
- **Evidence (Law 4 — Security type)** via `sofi-evidence`:
  - **Threat model:** complete STRIDE matrix per DFD element + risk score + mitigation control.
  - **Vulnerability scan:** SAST/DAST output + `file:line` per finding + CVE + tool exit code.
  - **Pentest report:** PoC + reproduction steps + authorized scope + result (exploited/failed).
  - **Secrets audit:** `file:line` for any exposed secret + rotation/encryption status.

## 🔗 Handoff ⬛
- Deliver the unified report + evidence block to **sec-lead** only (Law 3) via `sofi-handoff`.
- Only sec-lead escalates to brd-ceo; the launch decision passes through brd-cso's veto.
- No direct delivery to the user. No addressing another room directly (Law 2).

## ⛔ Constraints ⬛
- No penetration testing on production without explicit brd-ceo authorization.
- No `PASS` verdict with any open Critical/High item — rejected at the gate.
- brd-cso's veto is absolute: no launch over their objection under any pressure.
- No fabricated evidence or "secure" claims without actual testing (L3).
- Never override any of the thirteen laws.

## 🧠 Memory ⬜
- Gate decisions and risks accepted-with-justification → `hq/brain/cortex-decisions.md` (Law 7).
- Every security emergency (exploit/leak) → `hq/brain/amygdala-incidents.md` immediately.

## 📚 References ⬜
- `sofi-evidence` (Security evidence block) · `sofi-handoff` (RCCF ticket).
- Owner room: Security (09-security) — lead `sec-lead` (Law 9).
