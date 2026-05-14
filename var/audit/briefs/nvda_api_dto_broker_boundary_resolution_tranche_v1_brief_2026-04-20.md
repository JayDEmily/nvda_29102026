# NVDA API DTO and broker-boundary resolution tranche v1 — executable brief

Date: 2026-04-20
Repo baseline used to write this brief: `work/replay-evaluation-specimen-tranche-v1-20260420` at `aa4bad4728a0ea1cfc72570337584f1c8cc11a42`
Current `main` observed while writing: `3556388e0b76bc90676a48a5539906b491aeeb7a`

---

## 1. Direct answer

Yes. The next bounded tranche is the API DTO and broker-boundary reservation-resolution tranche.

This tranche exists to close the next explicit reservation pair after the accepted replay/evaluation tranche:

- the API DTO boundary reservation
- the broker-boundary reservation

This tranche must resolve those reservations truthfully without pretending that live API expansion or live broker integration has been admitted.

This tranche must **not** promote:

- new API routes beyond the existing bounded shell
- live broker adapters or outbound integration
- `analysis.scenarios`
- `observability`
- `legacy.imported`
- broad entry / CLI widening
- full-system V&V inside this tranche

This brief is executable. It is not an audit-only brief.

---

## 2. Mandatory execution setup

### 2.1 Promotion precondition before the tranche branch exists

The repo supplied with this brief is expected to be the accepted replay/evaluation tranche state on:

- `work/replay-evaluation-specimen-tranche-v1-20260420`
- `HEAD = aa4bad4728a0ea1cfc72570337584f1c8cc11a42`
- `main = 3556388e0b76bc90676a48a5539906b491aeeb7a`

Before starting tranche work:

1. confirm the supplied repo still matches that accepted state
2. promote the accepted replay/evaluation tranche into `main`
3. confirm `main` now points to `aa4bad4728a0ea1cfc72570337584f1c8cc11a42`
4. only then create the new tranche branch from that promoted `main`

Do not start the next tranche from stale `main`.

### 2.2 Work branch for this tranche

Create and use exactly this work branch:

`work/api-dto-broker-boundary-resolution-tranche-v1-20260420`

All leaves in this brief belong on that one tranche branch.

### 2.3 Mandatory reread before touching code or tests

Read, in order:

1. `AGENTS.md`
2. `migration_prebuild/AGENTS.override.md`
3. the ordered `migration_prebuild/` pack through `14_frozen_authority_and_mutability_law_2026-04-20.md`
4. `var/audit/README.md`
5. `var/audit/nvda_running_audit_log.xlsx`
6. `var/audit/briefs/nvda_replay_evaluation_specimen_tranche_v1_brief_2026-04-20.md`
7. `var/audit/reports/nvda_replay_evaluation_specimen_tranche_v1_report_2026-04-20.md`
8. `config/retained_test_registry.yaml`

Do not rely on memory of the prior tranche.

### 2.4 Workbook basis for this tranche

This tranche is grounded on the locked workbook by lineage, specifically the reservation pair already carried forward into the master tranche map:

- API DTO boundary reservation
- broker protocol / broker-boundary reservation

Interpretation fixed for this tranche:

- `src/nvda_desk/adapters/egress/api_dto_adapter.py` already exists, but its reservation is not lawfully closed merely by existing
- `src/nvda_desk/adapters/egress/broker_protocol.py` already exists, but its reservation is not lawfully closed merely by existing
- this tranche resolves **ownership, placement, use, and proof** for those bounded surfaces
- this tranche does **not** admit live broker implementations unless the audit proves a bounded concrete implementation already exists and must be normalised to stay truthful

---

## 3. Tranche objective

Resolve the API DTO and broker-boundary reservations truthfully.

At tranche closeout, the repo should have:

- an explicit, truthful answer for where API DTO projection belongs in the current shell
- an explicit, truthful answer for whether the broker boundary remains protocol-only or admits a bounded concrete implementation set
- the minimum native proof mirror required to keep those resolutions visible
- no accidental feature expansion

This tranche is allowed to leave the truthful answer as:

- **DTO adapter retained and explicitly used at the boundary**, or
- **DTO projection relocated to route-local boundary code with the adapter retired or reduced to compatibility**,

provided the result is explicit and bounded.

This tranche is allowed to leave the truthful broker answer as:

- **protocol-only boundary retained**,

if the audit shows there is no admissible native concrete implementation yet.

---

## 4. Current repo facts that this tranche must respect

Observed directly while writing this brief:

- `PYTHONPATH=src pytest -q tests/tier_a tests/tier_b` is green at **96 passed**
- `python3 -m compileall src tests/tier_a tests/tier_b` is clean
- the accepted replay/evaluation tranche has **not yet** been promoted to `main` in the supplied repo state
- `src/nvda_desk/api/app.py` exists and exposes only `healthcheck` and `run_once`
- `src/nvda_desk/api/deps.py` exists
- `src/nvda_desk/api/http/app.py` remains a thin compatibility wrapper
- `src/nvda_desk/adapters/egress/api_dto_adapter.py` exists, but there are no observed native call sites at tranche start
- `src/nvda_desk/adapters/egress/broker_protocol.py` exists, but there are no observed native concrete broker implementations at tranche start
- there are no current Tier A native families specifically covering the API DTO or broker-boundary reservations
- `analysis.scenarios`, `observability`, and `legacy.imported` remain absent and out of scope here

---

## 5. Leaf queue

### Leaf 1 — reservation audit and admissibility decision

Produce a bounded audit note before changing runtime or proof surfaces.

Minimum required questions:

1. what are the actual current consumers and producers of API boundary outputs?
2. does the current API shell need an explicit DTO projection step to stay truthful, or is it already returning public-boundary-safe payloads?
3. if DTO projection is needed, should it remain in `adapters/egress/api_dto_adapter.py` or move to narrower route-local boundary code?
4. are there any native concrete broker implementations already present that make `broker_protocol.py` incomplete as a reservation answer?
5. if no concrete implementations exist, is the truthful closeout state protocol-only plus proof, rather than fabricated implementation code?

Required output:

- one admissibility / reservation-resolution note under `var/audit/reports/`

Stop rule:

- do **not** widen code in this leaf
- if the audit proves the reservation can be closed with proof plus explicit notes only, that is admissible
- if code changes are needed, they must be bounded by later leaves in this tranche

### Leaf 2 — API DTO boundary resolution

Truthfully resolve the API DTO reservation.

Admissible outcomes:

1. retain `src/nvda_desk/adapters/egress/api_dto_adapter.py` as the dedicated projection boundary and make its use explicit from the bounded API shell, or
2. relocate the projection to narrower API-boundary code and reduce the adapter to compatibility or retire it if that is the more truthful bounded shape

Constraints:

- do **not** add new routes
- do **not** widen `HttpApp` beyond the current shell shape
- do **not** introduce web-framework dependencies or real transport plumbing
- do **not** let DTO work bleed into runtime orchestration or entry shells

### Leaf 3 — broker-boundary resolution

Truthfully resolve the broker-boundary reservation.

Default expected outcome unless direct evidence disproves it:

- keep `src/nvda_desk/adapters/egress/broker_protocol.py` as a protocol-only boundary
- make that protocol-only status explicit and benchmark-reconciled through code shape and proof

Admissible exception:

- only if native code already contains a real bounded concrete broker implementation that is necessary to keep the current repo truthful may this tranche admit a concrete implementation surface

Constraints:

- do **not** create fake broker integrations
- do **not** add network, credentials, or external execution logic
- do **not** turn this into live trading enablement

### Leaf 4 — minimum truthful proof mirror

Add only the minimum truthful native proof needed to keep the reservation resolutions visible.

Expected proof shape:

- one Tier A family for API DTO boundary truth
- one Tier A family for broker-boundary truth
- retained registry entries for each family

The proof may check:

- presence and bounded placement of the DTO projection surface
- whether the bounded API shell uses the admitted DTO boundary truthfully
- presence and bounded shape of the broker protocol boundary
- absence of admitted concrete broker implementation surfaces if protocol-only is the truthful result

The proof must **not**:

- become a broad API behaviour suite
- assert live broker execution
- widen into end-to-end orchestration

### Leaf 5 — tranche closeout

Required outputs:

- tranche report under `var/audit/reports/`
- brief copy under `var/audit/briefs/`
- ledger update in `var/audit/nvda_running_audit_log.xlsx`

The tranche report must state clearly:

- whether the API DTO reservation closed as dedicated-adapter, route-local, or compatibility-only
- whether the broker reservation closed as protocol-only or bounded concrete implementation
- why that answer is truthful against the current repo state
- exact proof commands and outputs
- whether any reservation remains intentionally deferred

---

## 6. Allowed surfaces

### 6.1 Runtime/code surfaces allowed to change

Only these bounded surfaces may change if required by the audit:

- `src/nvda_desk/api/app.py`
- `src/nvda_desk/api/deps.py`
- `src/nvda_desk/api/http/app.py`
- `src/nvda_desk/adapters/egress/api_dto_adapter.py`
- `src/nvda_desk/adapters/egress/broker_protocol.py`
- narrowly adjacent package `__init__.py` files if required for truthful exports only

### 6.2 Proof surfaces allowed to change

Only these proof surfaces may change if needed:

- new bounded Tier A tests under `tests/tier_a/api/`
- or new bounded Tier A tests under `tests/tier_a/adapters_egress/` if that is the cleaner native home
- `config/retained_test_registry.yaml`

### 6.3 Audit/receipt surfaces allowed to change

- `var/audit/briefs/`
- `var/audit/reports/`
- `var/audit/nvda_running_audit_log.xlsx`

---

## 7. Prohibited surfaces

Do **not** touch:

- `src/nvda_desk/analysis/scenarios/**`
- `src/nvda_desk/observability/**`
- `src/nvda_desk/legacy/imported/**`
- `src/nvda_desk/entry/**`
- `src/nvda_desk/ingress/**`
- `src/nvda_desk/persistence/**` except if a bounded import path requires trivial compatibility adjustment directly caused by this tranche and documented in the report
- `src/nvda_desk/testing/harnesses/**`
- `src/nvda_desk/runtime/**`
- broad `contracts/**` redesign
- new third-party dependencies
- caches, venvs, or unrelated repository hygiene work

Do **not** change tests merely to fit current code if the hierarchy points the other way.

---

## 8. Proof commands required at closeout

Run and record at minimum:

### 8.1 Targeted tranche proof

Use the exact targeted paths that correspond to the admitted new or changed Tier A families.

### 8.2 Tranche proof floor

```bash
PYTHONPATH=src pytest -q tests/tier_a tests/tier_b
python3 -m compileall src tests/tier_a tests/tier_b
```

This tranche does **not** require a whole-repo end-to-end V&V programme. Full-system closeout belongs later unless a direct blocker proves otherwise.

---

## 9. Definition of done

This tranche is done only when all of the following are true:

1. the accepted replay/evaluation tranche has first been promoted to `main`
2. the tranche branch used is exactly `work/api-dto-broker-boundary-resolution-tranche-v1-20260420`
3. the reservation audit note exists and is truthful
4. the API DTO reservation has a truthful bounded resolution
5. the broker-boundary reservation has a truthful bounded resolution
6. the minimum proof mirror exists and is admitted in the retained registry
7. `PYTHONPATH=src pytest -q tests/tier_a tests/tier_b` passes
8. `python3 -m compileall src tests/tier_a tests/tier_b` is clean
9. the tranche report, brief copy, and live ledger are updated truthfully
10. no prohibited surface was widened

If the truthful outcome is that one of the two reservations remains partially deferred, that is only admissible if the report states exactly why the deferral is still benchmark-honest and why a fabricated closure would be worse.

---

## 10. Direct instruction to the execution thread

Execute this tranche exactly as written.

Use one tranche branch only.
Use one active leaf at a time.
Use one commit per closed leaf.
Do not start the next leaf before the current leaf is fully closed and recorded.
Do not widen scope for convenience.
Do not perform full-system V&V inside this tranche unless a direct blocker proves it is required.
When complete, return the updated repo zip and the tranche report.
