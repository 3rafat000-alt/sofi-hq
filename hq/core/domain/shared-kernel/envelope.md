# Unified Message & Delivery Envelope
- Detailed reference: `hq/core/standards/api-envelope.md` (APIs). General rule restated:
- Every cross-context message = { from-room, to-room, ticket, intent, payload, evidence[] }
- Every delivery to another room or to the owner goes through the room lead exclusively (Law 3). Exception: the ⚠️ ESCALATE emergency channel.
