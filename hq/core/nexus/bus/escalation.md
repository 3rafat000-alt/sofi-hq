# Escalation Chain

## Path

```
specialist → room Lead → gtw-conflict-resolver → brd-arbiter → brd-ceo
```

Security:
```
specialist → sec-lead → brd-cso (absolute veto below CEO)
```

## Circuit breaker (3-attempt ceiling)

1. Halt immediately.
2. Crash-dump JSON: `{ "checkpoint": "<id>", "loop_count": 4, "failed_context": "...", "last_command": "...", "error_delta": "...", "escalation_token": "<TKT>" }`
3. Escalate up the chain (specialist → room Lead → …) with the crash-dump JSON attached; log the escalation to `hq/brain/amygdala-incidents.md` (escalate tooling retired 2026-07-16 → hierarchical enforcement).
4. Set ticket status to `blocked` (escalation in flight — status vocabulary of `bus/ticket-schema.md`)
5. Await decision; resume only after ADR recorded.

## When to escalate

- Decision above your authority (arbitration, contradictory constraints, security surface)
- 3 failed attempts on same sub-task
- Contradicting sources that can't be resolved (G5)
- SLO breach requiring formal Gate-1 reopen
