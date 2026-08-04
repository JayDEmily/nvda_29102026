# Chapter 8 — Execution Lifecycle, Carry, State and Persistence

## Chapter role

This chapter describes what happens after an execution expression has been formed, while preserving the design's strict distinction between preview state and booked reality. It then separates intraday lifecycle, carry horizons, schema migration and parallel-risk observation persistence.

**Primary propositions:** `P-EXE-002`, `P-STATE-001`, `P-EXE-003`, `P-CARRY-001`, `P-CARRY-002`, `P-PERSIST-001`, `P-PERSIST-002`, `P-PERSIST-003`.

## 1. Original execution model: a deterministic dry-run chain

Entry planning, position allocation, order simulation, broker adaptation, bot orchestration and execution tags may form one deterministic dry-run chain. (`P-EXE-002`)

The broker adapter remains fenced from:

- credentials;
- network execution;
- live acknowledgements;
- live-bridge claims;
- real placement behaviour.

Bot orchestration does not imply a daemon, scheduler or autonomous live loop. Execution tags explain the simulated or preview result; they do not prove that an order was sent or accepted.

The exact simulation fill model and adapter protocol remain unspecified. That incompleteness cannot be hidden by representing the dry-run adapter as a live broker integration.

## 2. Preview state is not booked state

The design allows execution logs, position books, trade logs and unrealised tracking, but their authority is preview-only. Missing-surface markers remain explicit. No preview surface may be described as live broker inventory, a booked ledger, settlement truth or booked P&L. (`P-STATE-001`)

Preview state may preserve local continuity and make later review possible. It does not acquire financial finality because it resembles a position ledger. Retention, transaction and reconciliation policies for any future booked system are not established by this proposition.

This distinction protects the rest of the lifecycle. A downstream exit marker cannot act on a booked position that the system never lawfully established.

## 3. Exit, re-entry and fill feedback remain advisory

The preview lifecycle then expands to partial exits, take-profit logic, trailing stops, re-entry markers, fill-feedback routing and ladder continuity. (`P-EXE-003`)

Each remains advisory. Missing live fills remain absent. The system cannot infer broker-side state from a simulated fill or present a preview ladder as live ladder management. Continuity may use a deterministic preview identity or hash so that a later step can refer to the same simulated plan without pretending it is broker inventory.

The source corpus does not state the complete exit thresholds or re-entry rules. It does establish that those rules, when later defined, cannot cross into live state without separately admitted broker and booked-state authority.

## 4. Carry becomes a separate horizon branch

Carry is not another intraday playbook. At the intraday close, the system hands state through a typed carry packet into three explicit branches: (`P-CARRY-001`)

- `overnight`;
- `weekend`;
- `event_carry`.

Friday-close and pre-event cases are named, not left to generic overnight logic. The lawful action set is:

- `flatten`;
- `hold_small`;
- `hold_baseline`;
- `add_carry`;
- `block_carry`.

Every action requires explicit legal conditions. Missing conditions cannot authorise carry, and mandatory-flatten policy remains binding. Carry cannot be disguised as intraday eligibility or supported with fabricated booked-position state.

## 5. Carry packets acquire inventory, lineage and deterministic ceilings

The later formalisation adds the context required to explain a carry decision. The close-state/carry packet includes held-position or inventory context and family/setup/playbook lineage. (`P-CARRY-002`)

Ordinary overnight, weekend and event carry remain separate states. Each branch has deterministic allowed-action ceilings, with bounded downgrade and override rules. The resulting explanation must show why an action was legal, downgraded or blocked.

A missing inventory surface cannot be replaced with a fictitious holding. A branch cannot silently widen its action ceiling or avoid a mandatory flatten. The detailed ceiling values and override precedence are not restated in the admitted corpus.

## 6. Migration lifecycle is not persistence business ownership

The successor corpus introduces an explicit schema-migration owner. That owner is separate from runtime persistence domains, repositories, models and sessions. A package-owned migration boundary may coexist with an external migration-tool root, but the relationship must be explicit and bounded. (`P-PERSIST-001`)

Migration authority governs schema lifecycle. It does not own the business meaning of:

- execution records;
- market observations;
- positions;
- capital state;
- review state;
- research logs;
- module-registry policy.

Moving those records under a migration package would not make the migration owner their semantic owner. Exact package paths and tool topology remain implementation-specific rather than canonical.

## 7. Parallel-risk observation persistence is write-only to live runtime

The parallel-risk lane may append observations for evidence, but the live runtime cannot read them back as a decision input. The store is write-only from the perspective of both the serial and parallel live paths. (`P-PERSIST-002`)

This protects the statelessness established in Chapter 4. An observation database may preserve history without turning that history into hidden serial or parallel state. Read-back, implicit feedback or an undeclared live analytics path would change the lane's semantics and is prohibited.

Retention, schema and offline-reader policy are not specified by this proposition.

## 8. The append-only record is narrowed to bounded audit lineage

The final persistence amendment makes the write-only record concrete. A receiptable parallel-risk observation may contain only: (`P-PERSIST-003`)

- admitted input packet IDs;
- emitted output packet IDs;
- a bounded observation payload;
- timestamps;
- trace ID;
- run ID;
- scenario ID;
- lineage references required for later audit.

Persistence occurs after the lane evaluation. The seam exposes no live reader, analytical reader, analytics table or live read-back path. It must not become a shared hidden-state store.

The authority admits persistence for evidence and later analysis. It does not yet admit runtime analytics, feedback, offline query policy, retention rules or a broader research database.

## 9. Current authoritative position

The lifecycle and persistence design is now:

1. execution remains deterministic dry-run and broker-fenced;
2. logs, books and unrealised state remain preview-only;
3. exits, re-entry and fill feedback remain advisory;
4. continuity may use deterministic preview identity, not broker state;
5. carry is a typed close-state branch separate from intraday eligibility;
6. overnight, weekend and event carry have explicit action sets and ceilings;
7. schema migration has its own lifecycle owner but no business-record ownership;
8. parallel-risk observations append after evaluation;
9. live serial and parallel paths have no read-back authority;
10. observation records carry bounded packet, time and trace lineage only.

## 10. Unresolved matters

The admitted corpus leaves open:

- the simulation fill model and broker-adapter protocol details;
- preview retention, transaction and reconciliation policy;
- exit and re-entry thresholds;
- the full carry legal-condition matrix, ceiling values and override precedence;
- exact migration topology;
- observation retention, schema evolution, offline querying and analysis policy.

These gaps do not permit live placement claims, fake booked positions, hidden runtime read-back or migration-driven relocation of business authority.

## Cross-references

- Advisory and non-live authority ceiling: [Chapter 1](01_SYSTEM_PURPOSE_AND_ADVISORY_LIMITS.md).
- Stateless serial cognition: [Chapter 4](04_SERIAL_COGNITION_AND_STAGE_OWNERSHIP.md).
- Execution geometry and modifier consequences: [Chapter 5](05_PLAYBOOKS_POSTURE_MODIFIERS_AND_EXECUTION_CHOICES.md).
- Parallel-risk Stage A and terminal risk: [Chapter 7](07_PARALLEL_RISK_TERMINAL_RISK_AND_CAPITAL.md).
- Review and replay of lifecycle evidence: [Chapter 9](09_REVIEW_TRACE_REPLAY_AND_ASSURANCE.md).
- Public broker boundary and compatibility law: [Chapter 10](10_GOVERNANCE_COMPATIBILITY_AND_PUBLIC_BOUNDARIES.md).
