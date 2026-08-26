# Ubiquitous Language — single source of terminology
> Any document or contract using these terms means exactly what is written here — no free interpretation.

| Entity | Precise definition |
|--------|--------------------|
| Room | A bounded context owning exactly one organizational mission and one lead (aggregate root) |
| Agent | An executing entity inside exactly one room; crosses boundaries only via contracts |
| Skill | A knowledge capability owned by exactly one room, registered in capabilities/skills.yaml |
| Tool | An execution capability licensed to a room through the vetting gate, registered in tools.yaml |
| Ticket | The only permitted communication object between contexts, via the application bus |
| Gate | A domain service: a mandatory checkpoint before any state transition |
| Evidence | file:line · exit code · screenshot — no evidence, no delivery (Law 4) |
| RCCF | The formal work order that opens any execution (Law 5) |
| Capsule | The agent enclosure: agent.md + senses.yaml + memory.md + capabilities.yaml |
