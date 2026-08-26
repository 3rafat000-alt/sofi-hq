---
name: sec-mcp-vetting
description: >-
  Security vetting gate for any MCP server before enabling it in .mcp.json — source/permission assessment + supply-chain screening + risk classification + enable/reject/sandbox decision + brd-cso veto for sensitive cases. Triggers — "add an MCP server", "enable a server in .mcp.json", "is this server safe", "vet this Smithery/Glama server", "an MCP server wants an API key", "MCP gate", "third-party server", "vet this MCP", "is this MCP server safe", "MCP supply chain". Invoked before adding or enabling any MCP server, especially anything requesting keys, network connections, or file access.
---

# sec-mcp-vetting — The MCP Server Vetting Gate ⬛

> **Value:** every MCP server = third-party code running with your keys and files. This gate blocks any server from entering `.mcp.json` except by documented security decision — protecting SOFI's decision to strip down to the tools engine and preventing secret leakage.

## 🎯 When to invoke (When) ⬛
- Before adding/enabling any MCP server in `.mcp.json` — any `GATED` state in `references/FLEET.md`.
- For a server requesting an API key, token, connection string, or filesystem/network access.
- For any server from a third-party directory (Smithery / Glama / mcp.so / mcpservers.org).
- For periodic audits of the enabled fleet, or when an enabled server is suspected.

**Do not invoke** for: using an already-enabled approved server (ACTIVE without keys: playwright/context7/sequential-thinking/ddg-search), managed claude.ai connectors (CONNECTOR), or threat modeling an application feature (that's `sec-threat-model`).

> **Distinction:** the installed `mcp-builder` skill *builds* new MCP servers; this skill *security-checks them before enabling* — even a server built internally with `mcp-builder` passes through this gate before entering `.mcp.json`.

## 📥 Required inputs (Inputs) ⬛
- **A formal RCCF work order (Law 5)** — no vetting or enabling without it. Violation = L2.
- Server name + package (`npx`/command) + source (directory/repository) + requesting room and purpose.
- The requested permission list: filesystem (which paths?), network (which destinations?), secrets (which keys/tokens?).
- **SOFI precedent warning:** the system was deliberately stripped of a tools engine — every MCP addition contradicts the stripping decision by default; the burden of proof lies on the requester: only what is justified both security-wise and operationally gets enabled.

## 🔧 Steps (Steps) ⬛
1. **RCCF gate:** verify the work order and scope. Missing → halt and notify sec-lead (L2).
2. **Source & publisher assessment:** identify the publisher (official `modelcontextprotocol` vs third-party), package age, last publish, downloads/stars, whether the repository is open and audited. Unknown/new/sourceless = red flag.
3. **Permission inventory (least privilege):** extract what the server actually requests — filesystem (paths), network (egress destinations), secrets (keys). Any permission exceeding declared purpose = reject or sandbox. **Special warning:** a server asking for a key/connection = a secrets exfiltration surface → higher risk than keyless servers.
4. **Supply-chain scan (delegate `sec-secrets-warden` — Trivy owner):** scan the package with Trivy (CVE/config/exposed secrets), review its dependencies and install scripts (`postinstall`), verify reputation. Scanning is **read-only, offline, no auto-fix**. Evidence = Trivy report + exit code.
5. **Server threat modeling (mini-STRIDE):** what does it read/write/send? What if malicious or compromised (exfiltration of keys/files, RCE, poisoning the six-area brain)? Log scenarios and mitigations.
6. **Risk classification:** `LOW` (keyless, limited reads, official publisher) / `MEDIUM` (free-tier key or DB path, documented publisher) / `HIGH` (broad file/network access, third-party publisher, or touches sensitive secrets).
7. **Decision:** issue verdict — `ENABLE` (LOW and justified) / `SANDBOX` (MEDIUM: restricted permissions + monitoring) / `REJECT` (HIGH, unjustified, or unknown source). On enablement: **never write keys into `.mcp.json` — environment variables `${VAR}` only.**
8. **Security veto (Law 6):** any HIGH server or anything touching secrets/sensitive data → sec-lead escalates decision + evidence to **brd-ceo**, who consults **brd-cso**; brd-cso's veto is absolute and final. Never address the Board directly (Law 2).
9. **Documentation & fleet update:** after approval, update the server's state in `references/FLEET.md` (ACTIVE/GATED/REJECTED + reason) and log the decision in CORTEX.
10. **Emergency (Law 7):** malicious server discovered or exfiltration behavior observed → immediate emergency: disable in `.mcp.json`, record in `hq/brain/amygdala-incidents.md`, escalate to sec-lead then brd-ceo.
11. Produce the evidence block (below) via `sofi-evidence`.

## 📤 Outputs + evidence (Outputs & Evidence) ⬛
- **Output:** an MCP server vetting card = source/publisher + permission inventory + supply-chain report + risk classification + verdict (ENABLE/SANDBOX/REJECT) + brd-cso veto status, with `FLEET.md` updated.
- **Evidence (Law 4 — Security type)** via `sofi-evidence`:
  - **Server threat model:** mini-STRIDE scenarios + impact-if-malicious + mitigation controls.
  - **Permission list:** actual vs declared filesystem/network/secrets (least-privilege).
  - **Supply-chain scan:** Trivy report + `file:line` for any exposed secret/CVE + tool exit code.
  - **Decision:** verdict + justification + proposed `.mcp.json` line (with `${VAR}`, no keys) + updated `FLEET.md` row.

## 🔗 Handoff ⬛
- Deliver vetting card + evidence block to **sec-lead** only (Law 3) via `sofi-handoff`.
- Only sec-lead escalates to brd-ceo; enabling any sensitive server passes brd-cso's veto.
- No direct delivery to the user. No addressing another room directly (Law 2) — the requesting room is notified via leads.

## ⛔ Constraints ⬛
- No server enabled before a documented `ENABLE`/`SANDBOX` verdict — default is `REJECT`.
- **Writing a key/token/connection string into `.mcp.json` forbidden** — `${VAR}` from the environment only. Violation = L2.
- Supply-chain scanning = read-only, offline, no auto-fix (brd-cso binding limit).
- Automatic security veto list: known dangerous servers (write-capable architecture tokens / Desktop Commander / Composio / write-capable github-mcp / Shannon) = automatic `REJECT` — see `hq/brain/tools-capabilities.md`.
- brd-cso's veto is absolute: no enablement over their objection under any pressure.
- Never override any of the thirteen laws.

## 🧠 Memory ⬜
- Every enable/reject/sandbox decision + justification → `hq/brain/cortex-decisions.md` (Law 7); fleet state updated in `references/FLEET.md`.
- Malicious server/leak discovery → `hq/brain/amygdala-incidents.md` immediately.

## 📚 References ⬜
- `references/FLEET.md` — the complete fleet map (15 rooms, ACTIVE/GATED/CONNECTOR states, ready enablement commands).
- `hq/brain/tools-capabilities.md` — central tool registry and security veto list.
- `sofi-evidence` (Security evidence block) · `sofi-handoff` (RCCF ticket).
- Owner: Security room (09-security) — lead `sec-lead` (Law 9).
