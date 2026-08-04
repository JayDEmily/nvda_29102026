# Execution Lifecycle, Carry, State and Persistence

## Authority propositions

`P-EXE-002`, `P-STATE-001`, `P-EXE-003`, `P-CARRY-001`, `P-CARRY-002`, `P-PERSIST-001`, `P-PERSIST-002`, `P-PERSIST-003`.

Exact lineage is retained in [`../propositions/A02.md`](../propositions/A02.md), [`../propositions/A03.md`](../propositions/A03.md), [`../propositions/A05.md`](../propositions/A05.md), [`../propositions/A06.md`](../propositions/A06.md), [`../propositions/B03.md`](../propositions/B03.md), [`../propositions/B08.md`](../propositions/B08.md) and [`../propositions/B10.md`](../propositions/B10.md).

## 1. Execution remains deterministic preview

Entry planning, position allocation, order simulation, broker adaptation, bot orchestration and execution tags may form a deterministic dry-run chain. The broker boundary remains fenced from credentials, live acknowledgements and live-bridge claims. Bot orchestration does not imply a daemon, scheduler or live loop. Execution tags explain the preview only.

Execution logs, position books, trade logs and unrealised tracking are preview state. Missing-surface markers remain explicit. None may be represented as broker inventory, a booked ledger or settlement truth.

Partial exits, take-profit logic, trailing stops, re-entry markers, fill-feedback routing and ladder continuity remain advisory. Continuity may use deterministic preview identity or a hash, but cannot claim broker-side ladder or fill state.

## 2. Carry is a separate horizon branch

Intraday close state hands off through a typed carry packet into three distinct branches:

- `overnight`;
- `weekend`;
- `event_carry`.

Friday-close and pre-event cases are explicit. The packet includes held-position or inventory context and family/setup/playbook lineage.

Allowed carry actions are:

- `flatten`;
- `hold_small`;
- `hold_baseline`;
- `add_carry`;
- `block_carry`.

Each action has explicit legal conditions and a deterministic ceiling. Downgrade and override rules remain explanation-safe. Carry cannot be disguised as an intraday playbook, fabricate booked positions or silently change mandatory-flatten policy.

## 3. Migration lifecycle versus persistence meaning

Schema-migration lifecycle has an explicit owner distinct from business persistence domains, repositories, models and sessions. A package-owned migration boundary may coexist with an external migration-tool root only when the relationship is explicit.

Migration ownership does not authorise relocation of execution records, market observations, positions, capital state, review state, research logs or registry policy. It governs schema lifecycle, not the business meaning of stored records.

## 4. Parallel-risk observation persistence

The parallel-risk observation store is write-only from the live runtime's perspective. It cannot feed hidden state back into parallel risk or the serial spine.

Each append-only observation record is bounded to:

- admitted input packet IDs;
- emitted output packet IDs;
- a bounded observation payload;
- timestamps;
- trace, run and scenario IDs;
- lineage required for later audit.

The seam exposes no live reader, analytical reader, analytics table or live read-back path. Persistence is admitted for evidence and later analysis, not for runtime feedback or a shared hidden-state store.
