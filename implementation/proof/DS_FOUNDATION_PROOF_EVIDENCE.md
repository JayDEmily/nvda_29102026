# DS-T01 — foundation proof boundary evidence

## Status and claim boundary

**AUTONOMOUS WORKER CANDIDATE EVIDENCE — foundation proof authored before DS-I01 production implementation; foundation implementation PASS is not claimed.**

DS-T01 establishes executable proof for the already-admitted foundation boundary required by REQ-003, REQ-004, REQ-005, REQ-008 and REQ-010. The proof is intentionally expected-red where DS-I01 production behaviour or the mandatory PostgreSQL proof environment does not yet exist. It does not implement M00 projection behaviour, create the M01 source package, establish database roles/schemas, calculate any `Dxxx`, or claim DS-I01 acceptance.

## Accepted predecessor and execution state

DS-A04 independent review was admitted before DS-T01 entry:

- reviewed repair commit/tree: `7fff5cec71f6a1635ec9771ddbc225c391683cf9` / `59a73a0cb4f25bb58d6241a393a3a1cea55f881e`;
- review packet SHA-256: `0b300704527a2cc74a035dd1b4e221e33a726e0509f18721e33d04a35d2f201d`;
- reviewer result internal SHA-256: `449e85697b9cdc7c6c2ebd5f3281b5ad36abc61313ece5afe16178843cbfd706`;
- preserved reviewer-result file SHA-256: `65272d69c5b8c18a5eff22ea35193ef8bdfa4b2186412c6e63b666d9532d389a`;
- reviewer actor instance: `90a693b05a379582a3d4b5b77158b636`;
- verdict/route: `pass` / `PASS`;
- acceptance commit/tag: `ad5508f65760dc1b1949f067223f35cdc3e46cfb`, `accepted/DS-A04`;
- post-admission controller checkpoint: `cfec16ba3cb79e526558a76466fe03803e2f83a7` / tree `364901195b96171e176ae7389a760c2d447332e7`.

At that admitted state `projectctl ready` routed `DS-T01`, actor class `AUTONOMOUS`.

DS-T01 execution branch:

- branch: `work/ds-t01-foundation-proof-v2`;
- source HEAD/tree: `cfec16ba3cb79e526558a76466fe03803e2f83a7` / `364901195b96171e176ae7389a760c2d447332e7`;
- worker session actor instance: `92d8552e11233094bd4348f4ccab41b7`;
- generated context size: 44,657 bytes.

A first branch-entry attempt created historical commit `629d3bfd...` containing only an LCR branch transition. `projectctl check` rejected that shape because the LCR checkpoint source no longer matched the immediate first parent. No proof or production bytes were changed in that failed branch. The current branch uses the repository-prescribed coalesced pattern: branch admission and first lawful DS-T01 work are committed together with the regenerated LCR rather than rewriting history or bypassing the invariant.

## Authority-derived proof surface

The accepted brief and work order require foundation proof for six bounded areas. DS-T01 maps those obligations to physical proof as follows.

| Authority proposition | Physical proof |
|---|---|
| M00 field-level projection requires one exact `RawSignalProjectionMapping`; missing/ambiguous mappings or missing field/units refuse output | `tests/product/derived_signal/test_ds_t01_m00_projection.py` |
| Projected raw values preserve native value/units and source/mapping/temporal/receipt/subject/revision lineage; raw history is bounded, deterministic and paginated without duplication | `tests/product/derived_signal/test_ds_t01_m00_projection.py` |
| Required non-signal contexts are immutable/version-identified; unit conversion is explicit and rejects unit mismatch/magnitude heuristics | `tests/product/derived_signal/test_ds_t01_foundation_contract.py` |
| Derived occurrence carrier exposes exact identity, version, time, result shape and raw/predecessor/convention lineage; public reads distinguish absence from a value | `tests/product/derived_signal/test_ds_t01_foundation_contract.py` |
| M00 and M01 use distinct PostgreSQL user/schema boundaries and M01 lacks read/write privilege on M00-owned relations; M01 persistence factory remains private mechanism | `tests/implementation/derived_signal/test_ds_t01_persistence_isolation.py` |
| M01 never imports M00 private persistence/raw occurrence carrier, references M00 private table names directly, or introduces external-effect client/command surfaces | `tests/implementation/derived_signal/test_ds_t01_source_boundaries.py` |

The public-symbol spellings used by these tests are executable mechanism contracts for DS-I01, not changes to accepted Derived Signal mathematics, package/distribution identity or downstream effect authority. The architecture-admitted Python owner/public seam remains `nvda_desk.derived_signal_calculation_truth` / `nvda_desk.derived_signal_calculation_truth.api`.

## Collected proof

Command:

```text
PYTHONPATH=src /mnt/data/ds_a03_proof_env/venv/bin/python -m pytest --collect-only -q \
  tests/product/derived_signal tests/implementation/derived_signal
```

Observed:

```text
27 tests collected in 0.03s
```

Collected cases comprise:

- 4 M00 projection/history tests;
- 15 immutable/version-identified context-type instances;
- 4 additional M01 public-contract tests (unit conversion, occurrence carrier, absence semantics, no external-effect commands);
- 2 PostgreSQL persistence/isolation tests;
- 2 source-boundary tests.

No test skips missing production implementation, a missing required mapping or an absent PostgreSQL proof boundary.

## Expected-red pre-implementation execution

Command:

```text
PYTHONPATH=src /mnt/data/ds_a03_proof_env/venv/bin/python -m pytest -q \
  tests/product/derived_signal tests/implementation/derived_signal
```

Observed:

```text
27 failed in 0.06s
```

The failures are attributable to the intended pre-implementation/proof-environment boundary:

- 19 tests require the not-yet-created `nvda_desk.derived_signal_calculation_truth.api` public seam/types;
- 4 tests require the not-yet-implemented M00 typed raw projection symbols/read methods;
- 1 PostgreSQL boundary test fails closed because `NVDA_TEST_M00_POSTGRES_DSN` (and therefore the paired M01 proof boundary) is not configured in this Worker execution;
- 1 test requires the not-yet-created M01 private PostgreSQL persistence mechanism;
- 2 source-boundary tests require the not-yet-created M01 source package.

The PostgreSQL test does not substitute SQLite, an in-memory persistence fixture or a shared writer identity for the absent real proof DSNs. The implementation task must provide/exercise the real separated roles/schemas before this proposition can become green.

This expected-red disposition is proof-first evidence only. It is not a semantic or implementation PASS.

## Existing architecture regression proof

DS-T01 does not modify architecture registry/allocation/dependency/public-seam state. The current architecture/bootstrap proof was re-run with the preserved Python 3.13/PostgreSQL proof environment, the existing host PyYAML dependency, and a process-local Git `safe.directory` setting required only because the extracted handoff ownership differs from the runtime user.

Observed:

```text
python -m pytest tests/architecture tests/bootstrap -q
74 passed in 2.09s

python tools/validate_architecture.py
architecture objects: 6
active runtime modules: 1
implementation allocations: 2
admitted test families: 11
promotion sets: 1
dependency/public-seam violations: 0
PASS: structural architecture validation

python tools/check_dependencies.py
PASS: dependency direction and cycle validation

python tools/check_public_seams.py
PASS: public-seam validation
```

An earlier run without the process-local Git safety setting produced `73 passed, 1 failed`; the sole failure was Git's extracted-directory ownership refusal inside `validate_implementation_authority.py`, not an architecture assertion. No repository/global Git configuration was changed to obtain the clean rerun.

## Change boundary

DS-T01 changes only its authorised proof surfaces:

- `tests/product/derived_signal/__init__.py`;
- `tests/product/derived_signal/_support.py`;
- `tests/product/derived_signal/test_ds_t01_m00_projection.py`;
- `tests/product/derived_signal/test_ds_t01_foundation_contract.py`;
- `tests/implementation/derived_signal/test_ds_t01_persistence_isolation.py`;
- `tests/implementation/derived_signal/test_ds_t01_source_boundaries.py`;
- this `implementation/proof/DS_FOUNDATION_PROOF_EVIDENCE.md`.

No `src/**`, architecture registry/allocation, package metadata, schema, accepted brief, requirement, task/delegation or governance meaning is changed by the proof authoring itself.

## Clean committed proof candidate

The first coalesced DS-T01 proof commit is:

- commit: `ee9068dac291b55b085b0d23c72404d0d782bcab`;
- tree: `be927ff9203a218712a25eb32fbd4c43ce01a80d`;
- controller `check`: PASS;
- routed leaf after commit: `DS-T01`;
- worktree before committed-state execution: clean.

From that exact committed proof candidate, observed:

```text
ruff check tests/product/derived_signal tests/implementation/derived_signal
All checks passed!

python -m pytest --collect-only -q tests/product/derived_signal tests/implementation/derived_signal
27 tests collected in 0.04s

python -m pytest -q tests/product/derived_signal tests/implementation/derived_signal
27 failed in 0.09s
```

The 27 failures retain the same expected-red classification recorded above: missing DS-I01 M01 seam/types/source/persistence, missing M00 projection behaviour, and absent mandatory PostgreSQL proof DSNs. No test became unexpectedly green and no new failure class appeared.

The inherited architecture state remained green from the same committed candidate:

```text
python -m pytest tests/architecture tests/bootstrap -q
74 passed in 2.07s

python tools/validate_architecture.py
PASS: structural architecture validation

python tools/check_dependencies.py
PASS: dependency direction and cycle validation

python tools/check_public_seams.py
PASS: public-seam validation
```

This successor evidence update changes this evidence record and generated controller state only; the physical DS-T01 test bytes are unchanged from `ee9068d...`.

## Claim boundary

This evidence establishes only that the DS-T01 foundation proof boundary has been physically authored, collected and exercised expected-red before production implementation, while the inherited architecture proof remains green.

It does **not** establish that M00 projection or M01 foundation behaviour is implemented, that PostgreSQL role/schema isolation has passed, that any `Dxxx` is calculable, that DS-I01 is accepted, or that later kernel/integration/package proof has been reached.

---

# DS-I01 — foundation implementation evidence

## Scope and claim boundary

This section records DS-I01 implementation evidence against the already-accepted DS-T01 proof boundary. It does not claim DS-R01 independent-review PASS, any D-kernel implementation, M01 activation/composability, final package authority or downstream external-effect authority.

## Programme Owner bounded write-scope decisions

During DS-I01, two lifecycle-proof fixtures became stale only because the lawfully admitted implementation shell changes M01's truthful lifecycle from `placeholder` to `bootstrap`:

1. `tests/architecture/test_object_lifecycle.py` — authorised as an additional DS-I01 write path and recorded by governance commit `de1d6a3d3b54fd0cecaf803471ecd420a7236fe7`;
2. `tests/bootstrap/test_minimal_imports.py` — authorised as an additional DS-I01 write path and recorded by governance commit `4fb75554e518e94616ef89052936bd885eba4158`.

Neither decision changes calculation meaning, M01 identity/allocation, owner dependency direction, public-seam authority or review law.

## Implemented foundation surfaces

DS-I01 changes only the authorised foundation surfaces:

- `src/nvda_desk/raw_signal_occurrence_truth/api.py` — additive typed M00 raw-value/history projection;
- `src/nvda_desk/derived_signal_calculation_truth/__init__.py` — owner package shell;
- `src/nvda_desk/derived_signal_calculation_truth/api.py` — typed/versioned contexts, request/occurrence/lineage carriers, absence-preserving calculation/read foundation;
- `src/nvda_desk/derived_signal_calculation_truth/_postgres.py` — private M01 PostgreSQL occurrence persistence mechanism;
- `config/architecture/modules.yaml` — M01 lifecycle `placeholder -> bootstrap` with semantic ownership/dependency unchanged;
- `implementation/work_order/DS_IMPLEMENTATION_WORK_ORDER.md` — current lifecycle wording aligned to the admitted implementation shell;
- `tests/architecture/test_object_lifecycle.py` — M01 lifecycle assertion aligned to `bootstrap` while retaining non-composability proof;
- `tests/bootstrap/test_minimal_imports.py` — admitted source-package census accepts both `bootstrap` and `active` owners;
- `implementation/review/DS_FOUNDATION_CANDIDATE.md` — exact DS-R01 candidate narrative;
- this evidence record.

No D-kernel source, catalogue/dependency meaning, package metadata, provider integration or external-effect implementation is added.

## Pre-freeze implementation proof

A fresh PostgreSQL 17.9 proof cluster was used under `/mnt/data/ds_i01_pgproof`. The proof roles/schemas were temporary mechanism identities only:

- M00 proof role/schema: `nvda_m00_proof` / `m00_proof`;
- M01 proof role/schema: `nvda_m01_proof` / `m01_proof`.

The roles are distinct, the schemas are distinct, and the M01 proof role has neither SELECT nor INSERT/UPDATE/DELETE privilege on the M00 proof relations exercised by the DS-T01 boundary test.

Using the preserved Python 3.13 proof environment, psycopg 3.3.4, the repository source tree and the host PyYAML dependency, observed before candidate freeze:

```text
python -m pytest tests/product/derived_signal tests/implementation/derived_signal \
  tests/architecture/test_object_lifecycle.py tests/bootstrap/test_minimal_imports.py -q
32 passed in 0.19s

python -m pytest tests/architecture tests/bootstrap -q
74 passed in 2.18s

python tools/validate_architecture.py
architecture objects: 6
active runtime modules: 1
implementation allocations: 2
admitted test families: 11
promotion sets: 1
dependency/public-seam violations: 0
PASS: structural architecture validation

python tools/check_dependencies.py
PASS: dependency direction and cycle validation

python tools/check_public_seams.py
PASS: public-seam validation

python -m mypy src --show-error-codes
Success: no issues found in 19 source files

python -m ruff check src tests tools
All checks passed!

git diff --check
PASS (no output)
```

The 32-test bounded set includes the 27 accepted DS-T01 product/implementation proofs plus the M01 lifecycle and bootstrap source-tree regression assertions required by the two authorised lifecycle transitions.

## PostgreSQL mechanism observation

The DS-T01 PostgreSQL tests exercise a real local PostgreSQL 17.9 server, not SQLite or an in-memory substitute. The private M01 persistence factory creates its table through the M01 proof role/current schema, while the public M01 API does not export that factory.

The proof environment names do not resolve the accepted brief's deliberately deferred production role/schema names.

## First committed candidate and direct persistence defect discovery

The first substantive DS-I01 candidate was frozen at:

- commit `79652dfefdb73d1b223065d29adb5550c5abe3c4`;
- tree `1a8c0e264900b142e370b1168384276edb599e4f`;
- `projectctl check`: PASS;
- routed leaf: `DS-I01`;
- worktree: clean.

From that exact commit the bounded 32-test foundation/lifecycle surface passed, architecture/bootstrap passed 74/74, structural/dependency/public-seam validation passed, mypy passed for 19 source files and Ruff passed. The repository-configured aggregate `pytest -q` also passed 74/74 architecture/bootstrap tests.

A separate direct PostgreSQL occurrence round-trip was then executed because durable occurrence persistence is a load-bearing DS-I01 proposition and the accepted DS-T01 tests did not exercise read-back of a persisted nullable universe. That direct probe found the first unmet invariant: PostgreSQL JSONB `null` for `universe` is returned by psycopg as Python `None`, but `_PostgresPersistenceV1._from_row` attempted `json.loads(str(None))`, causing `JSONDecodeError` on read-back.

Observed failure class:

```text
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

This was a DS-I01 persistence decoder defect, not a test-environment failure. Downstream close/review was stopped at that point.

The bounded repair changes only `src/nvda_desk/derived_signal_calculation_truth/_postgres.py`: nullable JSONB `universe` is now decoded as `None`; list-valued JSONB continues to decode as an immutable tuple in the public occurrence carrier. No authority, schema name, dependency, public seam or calculation meaning changes.

## Repaired-state direct PostgreSQL proof before second freeze

Against the same PostgreSQL 17.9 proof cluster, direct observation established:

```text
M00_IDENTITY ('nvda_m00_proof', 'm00_proof')
M01_IDENTITY ('nvda_m01_proof', 'm01_proof')
M01_ON_M00_PRIVILEGES ... (False, False) for SELECT and INSERT/UPDATE/DELETE on all four exercised M00 relations

ds-i01-proof-roundtrip-none-v2 ROUNDTRIP_IDENTICAL True
ds-i01-proof-roundtrip-none-v2 CONFLICT_REFUSAL derived occurrence identity already has different content
ds-i01-proof-roundtrip-universe-v2 ROUNDTRIP_IDENTICAL True
ds-i01-proof-roundtrip-universe-v2 CONFLICT_REFUSAL derived occurrence identity already has different content
HISTORY_CONTAINS_BOTH True
```

Thus the repaired private persistence mechanism round-trips both absent and non-empty universe values, is idempotent for identical content, refuses conflicting content under one occurrence ID, and returns the persisted occurrences through bounded history.

After that bounded repair, the prior proof surfaces remained green:

```text
32 passed in 0.18s
74 passed in 2.17s
PASS: structural architecture validation
PASS: dependency direction and cycle validation
PASS: public-seam validation
Success: no issues found in 19 source files
All checks passed!
git diff --check: PASS
```

## Remaining verification before DS-I01 close

The repaired source/evidence bytes must now be committed and the same proof re-run from that exact clean commit. Those committed-state results are recorded in a successor evidence-only update before DS-I01 is closed and DS-R01 becomes reviewable.

## Clean committed repaired-candidate proof

The bounded persistence repair was committed at:

- commit: `b099fbc1ddb277e9faba28bfec3d2b71d2b66c71`;
- tree: `a974c5039819f8a4034529ee365cb433fb2eec69`;
- branch: `work/ds-i01-foundation-implementation`;
- `projectctl check`: PASS;
- routed leaf: `DS-I01`;
- worktree before verification: clean.

From that exact committed state, direct PostgreSQL 17.9 proof established distinct M00/M01 role/schema identities and no M01 SELECT or INSERT/UPDATE/DELETE privilege on the four exercised M00-owned relations. Two committed-state occurrence probes then passed for both `universe=None` and `universe=('NVDA', 'AMD')`:

```text
M00_IDENTITY ('nvda_m00_proof', 'm00_proof')
M01_IDENTITY ('nvda_m01_proof', 'm01_proof')
M01_ON_M00_PRIVILEGES ... (False, False) for every exercised relation

ds-i01-committed-none-v1 ROUNDTRIP_IDENTICAL True
ds-i01-committed-none-v1 CONFLICT_REFUSAL derived occurrence identity already has different content
ds-i01-committed-universe-v1 ROUNDTRIP_IDENTICAL True
ds-i01-committed-universe-v1 CONFLICT_REFUSAL derived occurrence identity already has different content
HISTORY_CONTAINS_BOTH True
```

The same committed state produced:

```text
projectctl check
CHECK: PASS
ready=DS-I01

pytest tests/product/derived_signal tests/implementation/derived_signal \
  tests/architecture/test_object_lifecycle.py tests/bootstrap/test_minimal_imports.py -q
32 passed in 0.18s

pytest tests/architecture tests/bootstrap -q
74 passed in 2.07s

python tools/validate_architecture.py
architecture objects: 6
active runtime modules: 1
implementation allocations: 2
admitted test families: 11
promotion sets: 1
dependency/public-seam violations: 0
PASS: structural architecture validation

python tools/check_dependencies.py
PASS: dependency direction and cycle validation

python tools/check_public_seams.py
PASS: public-seam validation

python -m mypy src --show-error-codes
Success: no issues found in 19 source files

python -m ruff check src tests tools
All checks passed!

pytest -q
74 passed in 2.09s

git diff --check
PASS (no output)

git status --short
<empty>
```

The configured aggregate `pytest -q` remains the architecture/bootstrap aggregate; the 32-test foundation set is therefore recorded separately rather than being silently conflated with that aggregate.

This successor evidence update changes evidence/control bytes only. The substantive source/config/test/candidate bytes under review are unchanged from the repaired commit above.

## DS-R01 isolated context-contract repair

The first DS-R01 independent review of packet `bea78686264bab3e53f24223474b752613d4a90feaa8f52441d41f013bec71d8` returned `REPAIR -> DS-I01` with internal result SHA-256 `7e7145c3c8a84907473e620fcfad520348f8b03b5257b7abc9abac6fc69fd86b` and reviewer actor instance `c17e46d069bc2a7ec3b0070569228e79`. The externally supplied result file SHA-256 is `bce5622b5d57d4ab8b3c20f4db0666b5c5f401c2c1a89fa8bc733ea04e2a54f4`.

The reviewer classified one isolated foundation-contract defect: fourteen of the fifteen admitted clause-6 context types were frozen/versioned identity shells only, so the public seam could not represent the context-specific immutable inputs required by REQ-004. The reviewer explicitly authorised return to DS-I01 to implement context-specific fields/validation without adding kernel semantics, concrete production instances, architecture ownership changes or review-law changes.

The bounded repair changes:

- `src/nvda_desk/derived_signal_calculation_truth/api.py` — replaces the fourteen identity/version-only context subclasses with context-specific immutable fields and fail-closed validation derived from accepted brief clause 6;
- `implementation/review/DS_FOUNDATION_CANDIDATE.md` — records the repaired context contract and its non-claims;
- this evidence record.

No DS-T01 test, M00 projection implementation, PostgreSQL mechanism, architecture registry, dependency/public-seam declaration, package metadata, accepted brief, requirement or calculation-kernel source is changed.

The repaired context carriers represent the accepted clause-6 content as follows:

- `CalculationParameterSetV1`: named profile plus immutable named configured parameter values;
- `RequiredFieldPolicyV1`: non-empty distinct D007 requirements;
- `CandidateStructureContextV1`: candidate identity, aligned leg contract/side/quantity tuples, positive candidate quantity, explicit premium/entry assumptions and positive risk capital;
- `CandidateSetContextV1`: immutable ordered distinct candidate identities, exact eligibility-class mapping and explicit directed neighbour relations;
- `LivePositionContextV1`: position identity, aligned leg contracts/signed quantities/multipliers and exact M00/current-state occurrence references;
- `OrderIntentContextV1`: side, positive intended size and urgency;
- `EntryStateContextV1`: exact stored D155 occurrence reference;
- `EvaluationSetV1`: forecast occurrence identities, realised-outcome definition, UTC evaluation window, comparator/baseline and locked model/version;
- `RecalculationScheduleV1`: explicit scheduled trigger rules;
- `PnLConventionVersionV1`: provider P&L inclusion/exclusion components, explicit gross-of-execution-cost treatment and attribution units;
- `OptionRevaluationConventionVersionV1`: model family, exercise treatment, discount/carry references, time convention, IV/skew interpretation, numerical method/tolerance and Greek scaling;
- `ExecutionCostScheduleVersionV1`: explicit non-negative commission, fee and multi-leg incremental-cost rules plus cost units;
- `AttributionPathContextV1`: exact aligned underlying/IV/position/quantity path occurrence references;
- `InputSelectionPolicyVersionV1`: exact join keys, non-negative maximum staleness/skew, admitted temporal-basis permissions and immutable basket membership.

`UnitConventionVersionV1` already carried its accepted conversion-law content and remains unchanged.

### Direct public-seam repair probes before freeze

A direct construction probe instantiated all fifteen admitted context types with context-specific content. The two reviewer-described construction failures now succeed:

```text
CONTEXT_COUNT 15
REVIEWER_PROBES PASS
```

The same direct probe exercised fail-closed validation of representative load-bearing constraints:

```text
empty_required_policy REFUSED ValueError requirements must not be empty
zero_risk_capital REFUSED ValueError risk_capital_currency must be positive
negative_staleness REFUSED ValueError maximum_staleness must be non-negative
misaligned_attribution REFUSED ValueError attribution path occurrence reference tuples must be exactly aligned
```

These probes exercise the declared public constructors directly; they do not rely on the pre-existing DS-T01 helper that checked only frozen/version identity.

### Pre-freeze regression proof

Using a freshly reconstructed Python 3.13.5 proof environment with pytest 9.0.3, Ruff 0.15.11, mypy 1.20.1 and psycopg 3.3.4, plus a fresh PostgreSQL 17.9 proof cluster and temporary distinct proof identities `nvda_m00_r01_repair` / `m00_r01_repair` and `nvda_m01_r01_repair` / `m01_r01_repair`, observed:

```text
pytest tests/product/derived_signal tests/implementation/derived_signal \
  tests/architecture/test_object_lifecycle.py tests/bootstrap/test_minimal_imports.py -q
32 passed in 0.26s

pytest tests/architecture tests/bootstrap -q
74 passed in 2.34s

python tools/validate_architecture.py
PASS: structural architecture validation

python tools/check_dependencies.py
PASS: dependency direction and cycle validation

python tools/check_public_seams.py
PASS: public-seam validation

ruff check src tests tools
All checks passed!

mypy src/nvda_desk/derived_signal_calculation_truth/api.py --show-error-codes
Success: no issues found in 1 source file

git diff --check
PASS (no output)
```

The PostgreSQL DS-T01 isolation test therefore remained green across the context-only repair. The temporary proof role/schema names remain test-environment mechanics and do not resolve production database identity. Full-source mypy was not substituted for the recorded historical full-source proof in this pre-freeze run because the freshly reconstructed offline wheelhouse does not include PyYAML type stubs; the changed M01 public-seam file itself type-checks cleanly.

The repaired source/candidate/evidence bytes must now be committed and the direct context probes plus the same applicable regression proof re-run from that exact clean commit before a fresh DS-R01 packet is exported.

### Clean committed context-contract repair proof

The substantive context-contract repair was frozen at:

- branch: `work/ds-i01-context-contract-repair`;
- commit: `005fc799bc85c822486b09d0ac50da960984a15d`;
- tree: `0410ef0bc25d74a01dc978a3ecb5816c304cd132`;
- M01 public-seam file SHA-256: `e396dfd74874d9d81f31297f523ffaf95ba008cb4e6f56ede9780a4c1b21426e`;
- DS-R01 candidate SHA-256: `148e8d84b76dcd2cc4f8d2126e6d50272016b73c18e9ecd0c4f2304dd198d587`;
- worktree before committed-state verification: clean.

From that exact committed state, the direct public-seam construction/refusal probe produced:

```text
CONTEXT_COUNT 15
CONTEXT_SPECIFIC_FIELDS PASS
REVIEWER_PROBES PASS
empty_required_policy REFUSED ValueError requirements must not be empty
zero_risk_capital REFUSED ValueError risk_capital_currency must be positive
negative_staleness REFUSED ValueError maximum_staleness must be non-negative
misaligned_attribution REFUSED ValueError attribution path occurrence reference tuples must be exactly aligned
```

The same committed state, using a freshly recreated PostgreSQL 17.9 proof boundary with distinct M00/M01 proof users and schemas, produced:

```text
projectctl check
CHECK: PASS
ready=DS-R01

pytest tests/product/derived_signal tests/implementation/derived_signal \
  tests/architecture/test_object_lifecycle.py tests/bootstrap/test_minimal_imports.py -q
32 passed in 0.19s

pytest tests/architecture tests/bootstrap -q
74 passed in 2.22s

python tools/validate_architecture.py
PASS: structural architecture validation

python tools/check_dependencies.py
PASS: dependency direction and cycle validation

python tools/check_public_seams.py
PASS: public-seam validation

ruff check src tests tools
All checks passed!

mypy src/nvda_desk/derived_signal_calculation_truth/api.py --show-error-codes
Success: no issues found in 1 source file

pytest -q
74 passed in 2.13s

git diff --check
PASS (no output)

git status --short
<empty>
```

No production source, candidate, test, architecture, persistence or authority bytes changed after `005fc799...` during this committed-state verification. This successor update records evidence/control bytes only so a fresh DS-R01 packet can bind the exact repaired candidate and its committed-state proof.


---

# DS-T01-R01 — recurrent foundation-contract proof refinement

## Authority and recurrence boundary

The second independent DS-R01 review of packet `2f5c2232394921bf2e5098afc633fc68ce2e6adc4e0a048cc847df5d6cb69536` returned `REPAIR -> DS-I01` with internal result SHA-256 `c409fe3be22c0609100d1ee4980668650198d43b4ba5befc45a29ffd5633aadc` and classified the defect mechanism as `RECURRENT_CLASS foundation-contract/proof-boundary drift`.

The reviewer established that the prior clause-6 context repair fixed one witness but that the same mechanism remained elsewhere: accepted semantic requirements were stronger than the inherited DS-T01 green/shape proof. The named witnesses were lack of event-time filtering on the M00 projected-history seam and non-canonical `RawInputLineageV1.raw_signal_id` acceptance. The reviewer required class-level closure across the complete DS-I01 foundation contract and required a lawful proof/governance refinement before any further production repair where accepted DS-T01 proof bytes were insufficient.

The Programme Owner explicitly authorised that bounded proof-refinement route on 2026-10-04. Governance commit `9af612d` appends `DS-T01-R01` and `DS-I01-R01` as same-actor bounded refinements, keeps the original requirements/write scopes/acceptance law, routes DS-R01 behind the implementation refinement, and leaves kernel semantics, architecture ownership and external-effect authority unchanged.

## Authority-derived class-level proof surface

`tests/product/derived_signal/test_ds_t01_r01_foundation_contract_refinement.py` strengthens the Gate-2 proof without changing accepted semantics. It directly discriminates:

- M00 projected-history receipt-time and true-event-time criteria as separate public-seam dimensions;
- refusal to fabricate event instants for receipt-only observations;
- canonical admitted `R001-R323` identity on exact raw-input lineage;
- exact `VersionRefV1` typing and duplicate-ref refusal for request/context lineage;
- exact `RawInputLineageV1` typing for persisted raw lineage;
- non-empty/distinct predecessor occurrence identity and universe membership;
- persisted value versus absence separation (`result=None` is not a persisted occurrence value);
- rejection of unadmitted mutable/float/object result carriers and acceptance of the admitted recursive immutable result carrier; and
- continued constructibility of the repaired clause-6 context-specific contracts.

The refinement intentionally does not add any D-kernel mathematics, concrete production mappings/context instances, provider parsing fallback, architecture expansion or external effects.

## Expected-red execution against the reviewed DS-I01 candidate

Against repository state immediately after the governance refinement and before any production repair, the refined test produced:

```text
18 failed, 4 passed
```

The failures are semantic witnesses of the reviewed recurrent class:

- 2 failures: `list_projected_raw_history` has no `event_at_or_before_utc` criterion;
- 3 failures: `RawInputLineageV1` accepts invalid four-character/out-of-range raw IDs (`ABCD`, `R000`, `R324`);
- 2 failures: `CalculationRequestV1.context_refs` accepts untyped and duplicate version references;
- 3 failures: `DerivedSignalOccurrenceV1` accepts untyped parameter-context, raw-lineage and convention collections;
- 1 failure: duplicate occurrence version references are accepted;
- 1 failure: empty/duplicate predecessor occurrence IDs are accepted;
- 1 failure: empty/duplicate universe members are accepted;
- 1 failure: `result=None` is accepted as persisted value although public absence is a separate state;
- 4 failures: list/dict/float/arbitrary-object result carriers are accepted despite being outside `DerivedResultV1`.

The four passing propositions show that the refined proof itself is not merely globally red: malformed-length raw IDs already fail, the admitted recursive immutable structured result carrier is accepted, and the previously repaired clause-6 context-specific contracts remain constructible.

This is proof-first evidence only. No production source is changed by DS-T01-R01. DS-I01-R01 must remain blocked until this refined proof is durably accepted.

## DS-I01-R01 — production repair against accepted recurrent-class proof

`DS-T01-R01` is durably accepted at tag `accepted/DS-T01-R01` targeting commit `de61f260bc72446995d2d1f8806ea8a281e8e50a` / tree `263fd13d6455755a65db1183be09f45e87a366e1`. The post-tag controller state routes `DS-I01-R01` as the only ready autonomous leaf.

The production repair is bounded to two already-admitted foundation source surfaces plus candidate/evidence text:

- `src/nvda_desk/raw_signal_occurrence_truth/api.py`: add explicit `event_at_or_before_utc` selection to projected raw history and establish true-event UTC only from an admitted `true_instant`; receipt/date-only or unestablished source instants fail closed under event-time filtering;
- `src/nvda_desk/derived_signal_calculation_truth/api.py`: enforce canonical `R001-R323` raw lineage identity, exact typed/duplicate-safe version references and raw-lineage collections, non-empty/distinct predecessor/universe identities, and runtime validation of the admitted persisted `DerivedResultV1` carrier with `None` reserved for public absence rather than persisted value;
- `implementation/review/DS_FOUNDATION_CANDIDATE.md`: update the exact DS-R01 candidate narrative;
- this evidence record.

No accepted DS-T01/DS-T01-R01 test bytes, PostgreSQL mechanism, architecture state, dependency/public-seam declaration, package metadata, kernel semantics, concrete production mapping/context instance or external-effect surface is changed by DS-I01-R01.

### Pre-freeze refined proof and regression evidence

Against the repaired working candidate, the accepted recurrent-class proof transitions from `18 failed, 4 passed` to:

```text
pytest -q tests/product/derived_signal/test_ds_t01_r01_foundation_contract_refinement.py
22 passed
```

A fresh preserved Python 3.13.5 / PostgreSQL 17.9 proof environment was reconstructed from the hash-verified offline bootstrap/runtime assets. Temporary proof-only database identities were created as `nvda_m00_r01` / `m00_r01` and `nvda_m01_r01` / `m01_r01`; those names remain proof mechanics and do not resolve production schema/role identity.

Using that environment, observed before candidate freeze:

```text
pytest -q tests/product/derived_signal tests/implementation/derived_signal \
  tests/architecture/test_object_lifecycle.py tests/bootstrap/test_minimal_imports.py
54 passed

pytest -q tests/architecture tests/bootstrap
74 passed

python tools/validate_architecture.py
PASS: structural architecture validation

python tools/check_dependencies.py
PASS: dependency direction and cycle validation

python tools/check_public_seams.py
PASS: public-seam validation

mypy src/nvda_desk/derived_signal_calculation_truth/api.py \
  src/nvda_desk/raw_signal_occurrence_truth/api.py --show-error-codes
Success: no issues found in 2 source files

ruff check src/nvda_desk/derived_signal_calculation_truth/api.py \
  src/nvda_desk/raw_signal_occurrence_truth/api.py \
  tests/product/derived_signal/test_ds_t01_r01_foundation_contract_refinement.py
All checks passed!

git diff --check
PASS (no output)
```

A direct real-PostgreSQL structured-occurrence probe through the private M01 persistence mechanism also established:

```text
ROUNDTRIP_IDENTICAL True
IDEMPOTENT_IDENTICAL True
UNKNOWN_ABSENCE True
```

That probe persisted non-empty parameter/context refs, canonical raw lineage, predecessor lineage, convention refs, a non-empty universe and a nested immutable result containing `Decimal`, category/boolean and UTC `datetime`, then read the exact occurrence back. This confirms the stricter public carrier contract remains compatible with durable structured-result persistence.

The substantive repaired source/candidate/evidence bytes must now be frozen in Git and the same proof rerun from that exact clean commit before a fresh DS-R01 packet is exported.

### Clean committed DS-I01-R01 proof

The substantive recurrent-class production repair was frozen at:

- branch: `work/ds-i01-r01-foundation-contract-repair`;
- commit: `d9aa11c18cd949eced71aff4179a76aa7525b276`;
- tree: `ef4332c75cdb8db4e00462ff86199e53dabf756d`;
- candidate SHA-256: `0496e296610af76b52b0960db390c150755f637f5cef2ac69023695e2c43bb64`;
- M00 public API SHA-256: `74f13b23fc813f64805dec7c1467471de934fc00b16a72b792bee91bd61a5216`;
- M01 public API SHA-256: `1c76c6620d3f1e494a78a1a40022e1fa9a07677f21b3483b2151c307a7e243f4`;
- worktree before committed-state verification: clean.

From that exact commit, the accepted recurrent-class proof and inherited Gate-2/architecture proof surfaces produced:

```text
pytest -q tests/product/derived_signal/test_ds_t01_r01_foundation_contract_refinement.py
22 passed

pytest -q tests/product/derived_signal tests/implementation/derived_signal \
  tests/architecture/test_object_lifecycle.py tests/bootstrap/test_minimal_imports.py
54 passed

pytest -q tests/architecture tests/bootstrap
74 passed

python tools/validate_architecture.py
PASS: structural architecture validation

python tools/check_dependencies.py
PASS: dependency direction and cycle validation

python tools/check_public_seams.py
PASS: public-seam validation

mypy src/nvda_desk/derived_signal_calculation_truth/api.py \
  src/nvda_desk/raw_signal_occurrence_truth/api.py --show-error-codes
Success: no issues found in 2 source files

ruff check src/nvda_desk/derived_signal_calculation_truth/api.py \
  src/nvda_desk/raw_signal_occurrence_truth/api.py \
  tests/product/derived_signal/test_ds_t01_r01_foundation_contract_refinement.py
All checks passed!

projectctl check
CHECK: PASS
ready=DS-I01-R01

git diff --check
PASS (no output)

git status --short
<empty>
```

The same committed state passed a real PostgreSQL 17.9 structured occurrence round-trip using the temporary M01 proof schema/role:

```text
ROUNDTRIP_IDENTICAL True
IDEMPOTENT_IDENTICAL True
UNKNOWN_ABSENCE True
```

No substantive source/candidate/test/architecture/persistence bytes were changed after `d9aa11c...` during committed-state verification. This successor evidence update changes evidence/control bytes only so DS-I01-R01 can be closed and a fresh DS-R01 packet can bind the exact repaired candidate plus committed-state proof.

---

# DS-T01-R02 — PostgreSQL persistence-boundary proof refinement

## Authority and recurrence boundary

The third independent DS-R01 review of packet `aae2f5e40ee61ba1ecdc098aa385ff592ba9f220b3900755a33753c727c3071d` returned `REPAIR -> DS-I01-R01` with internal result SHA-256 `6e2846855688345776ccee06d49049c0a6fe38fba039b4e5e1812161cdafb169` and retained the `RECURRENT_CLASS foundation-contract/proof-boundary drift` classification.

The reviewer established that DS-T01-R01/DS-I01-R01 closed the prior public-contract witnesses but that the same proof weakness remained at the PostgreSQL persistence boundary: a lawful separated role/schema configuration was proved, while an adverse shared M00 writer/schema configuration was not required to fail closed. The accepted brief clause 10 and REQ-005 require both the calculation-owner schema and write role to remain separate from M00.

Under the existing same-actor bounded-refinement contract for `FOUNDATION-CONTRACT-PROOF-DRIFT`, DS-T01-R02 strengthens proof before any further persistence behaviour change. No concrete production role/schema name is selected by this proof.

## Authority-derived adverse persistence proof

`tests/implementation/derived_signal/test_ds_t01_r02_persistence_boundary_refinement.py` directly exercises four database-boundary propositions against real PostgreSQL:

1. a lawfully separate M01 writer and schema may construct the private persistence mechanism;
2. the exact M00 writer/schema boundary is refused before the M01 derived-occurrence table is created;
3. the M00 writer remains refused even when pointed at a different schema; and
4. a different writer remains refused when pointed at M00's schema, even when proof-only privileges make that adverse configuration technically possible.

The proof obtains current role/schema identities from PostgreSQL at runtime. It therefore discriminates the semantic boundary without fixing production role/schema names. The temporary grant used for the fourth adverse probe is proof-environment-only and is revoked in the test cleanup path.

## Expected-red execution before DS-I01-R02

Using the preserved Python 3.13.5 / psycopg 3.3.4 / PostgreSQL 17.9 proof environment with existing temporary proof identities `nvda_m00_r01` / `m00_r01` and `nvda_m01_r01` / `m01_r01`, observed before any production repair:

```text
pytest -q tests/implementation/derived_signal/test_ds_t01_r02_persistence_boundary_refinement.py
4 failed
```

All four failures stop at the same first unmet contract:

```text
DS-T01-R02 requires an explicit private M00 persistence-boundary identity contract
```

This is the intended proof-first red state. The test module itself passes Ruff. No source, architecture, schema, package metadata or accepted DS-T01/DS-T01-R01 proof bytes were changed to obtain this result.

DS-I01-R02 remains blocked until this proof refinement is durably accepted.

## DS-I01-R02 — PostgreSQL persistence-boundary production repair

`DS-T01-R02` is durably accepted at tag `accepted/DS-T01-R02`, targeting commit `59c796e072ecc7a0344c0ee45d78c1d6a62b6f46`. DS-I01-R02 is the same-actor implementation refinement under the already-admitted DS-I01 envelope and changes no requirement, semantic route, write scope, actor class or review contract.

### Bounded implementation mechanism

The repair changes only the private M01 PostgreSQL mechanism plus candidate/evidence text. `src/nvda_desk/derived_signal_calculation_truth/_postgres.py` now defines an immutable private `PostgresBoundaryIdentityV1` carrying runtime `writer_role` and `schema` identity. `create_postgres_persistence(...)` requires the observed M00 boundary identity as a private mechanism input, introspects its own `current_user/current_schema()`, and refuses construction if either writer role or schema is shared with M00.

The constructed persistence object stores both the accepted M00 boundary and its own observed M01 boundary and revalidates both on every new PostgreSQL connection. A later role/search-path change therefore fails closed rather than redirecting unqualified persistence onto an M00-owned boundary. The repair does not hard-code, select or grant production role/schema names, does not receive an M00 DSN, and does not read or write M00-owned relations.

### Pre-freeze proof

Using the preserved PostgreSQL 17.9 proof environment with temporary identities `nvda_m00_r01` / `m00_r01` and `nvda_m01_r01` / `m01_r01`, the accepted DS-T01-R02 proof produced:

```text
pytest -q tests/implementation/derived_signal/test_ds_t01_r02_persistence_boundary_refinement.py
4 passed
```

The proof establishes lawful separate construction, exact shared-boundary refusal, same-writer/different-schema refusal and different-writer/same-schema refusal. The proof-only M00 role was granted database `CREATE` solely so the alternate-schema adversary could be constructed; this does not alter production authority.

The complete Gate-2 and architecture regressions then produced:

```text
pytest -q tests/product/derived_signal tests/implementation/derived_signal \
  tests/architecture/test_object_lifecycle.py tests/bootstrap/test_minimal_imports.py
58 passed

pytest -q tests/architecture tests/bootstrap
74 passed

python tools/validate_architecture.py
PASS: structural architecture validation

python tools/check_dependencies.py
PASS: dependency direction and cycle validation

python tools/check_public_seams.py
PASS: public-seam validation

mypy src/nvda_desk/derived_signal_calculation_truth/_postgres.py --show-error-codes
Success: no issues found in 1 source file

ruff check src/nvda_desk/derived_signal_calculation_truth/_postgres.py \
  tests/implementation/derived_signal/test_ds_t01_r02_persistence_boundary_refinement.py
All checks passed!
```

A separate direct real-PostgreSQL operation-drift probe constructed M01 lawfully, then changed the proof M01 role's default search path onto M00's schema after construction. The next persistence read was refused before querying the derived table:

```text
OPERATION_DRIFT_REFUSED M01 persistence schema must be separate from M00 schema
POST_RESET_IDENTITY ('nvda_m01_r01', 'm01_r01')
```

The proof role configuration and schema privilege were reset after the probe. The substantive repaired source/candidate/evidence bytes must now be committed and the same proof rerun from that exact clean commit before DS-I01-R02 can be accepted and a fresh DS-R01 packet exported.

### Clean committed DS-I01-R02 proof

The substantive PostgreSQL boundary repair was frozen at:

- branch: `work/ds-i01-r02-persistence-boundary-repair`;
- commit: `b4d2bf3cd4d3a9683768bfc1b59a62753ccd5e62`;
- tree: `a8132286de20d3210d0f206c91fc5b99b3375fd7`;
- private M01 PostgreSQL mechanism SHA-256: `96b84b2e4406041546db2e15f3f81f217426878af59a5153c317ea0961d532a6`;
- DS-R01 candidate SHA-256: `9ed74a4cf5dedf1e04cd61daafd4141105cec5eb4c2f00b9c3398d5579aea606`;
- worktree before committed-state verification: clean.

From that exact commit, the accepted adverse persistence proof produced:

```text
pytest -q tests/implementation/derived_signal/test_ds_t01_r02_persistence_boundary_refinement.py
4 passed
```

The complete Gate-2 and architecture surfaces from the same clean commit produced:

```text
pytest -q tests/product/derived_signal tests/implementation/derived_signal \
  tests/architecture/test_object_lifecycle.py tests/bootstrap/test_minimal_imports.py
58 passed

pytest -q tests/architecture tests/bootstrap
74 passed

python tools/validate_architecture.py
PASS: structural architecture validation

python tools/check_dependencies.py
PASS: dependency direction and cycle validation

python tools/check_public_seams.py
PASS: public-seam validation

mypy src/nvda_desk/derived_signal_calculation_truth/_postgres.py --show-error-codes
Success: no issues found in 1 source file

ruff check src/nvda_desk/derived_signal_calculation_truth/_postgres.py \
  tests/implementation/derived_signal/test_ds_t01_r02_persistence_boundary_refinement.py
All checks passed!

git diff --check
PASS (no output)

git status --short
<empty>
```

A direct structured-occurrence probe through the repaired private factory also established:

```text
ROUNDTRIP_IDENTICAL True
IDEMPOTENT_IDENTICAL True
UNKNOWN_ABSENCE True
OPERATION_DRIFT_REFUSED M01 persistence schema must be separate from M00 schema
POST_RESET_IDENTITY ('nvda_m01_r01', 'm01_r01')
```

The operation-drift probe granted only temporary proof-environment schema visibility, reset the M01 role's search path to its own schema and revoked that visibility afterwards. No production database identity or privilege was selected or changed.

No substantive source/candidate/test/architecture bytes changed after `b4d2bf3...` during committed-state verification. This successor evidence update changes evidence/control bytes only so DS-I01-R02 can be accepted and a fresh DS-R01 packet can bind the exact repaired candidate and committed-state proof.

---

# DS-T01-R03 — PostgreSQL privilege-boundary proof refinement

## Authority and recurrence boundary

The fourth independent DS-R01 review of packet `5742c502855a2f9d95cec5f2df02c40296d12021bf60119af95567c788176e43` returned `REPAIR -> DS-I01-R01` with internal result SHA-256 `6dbc7d314e9631d808ebab62c8847d3ee3edd24b7b7f0fee18b7c9aa78f49a32`, reviewer actor instance `24b174ae65e2939a776bf696358fbd19`, and externally supplied result-file SHA-256 `fa07fef62b41b9ee0c6ff3e736c6549f3338bd95bfd42dcb8cf3d37b219a1083`.

The reviewer confirmed that DS-T01-R02/DS-I01-R02 correctly enforce distinct writer/schema identity, but retained the `RECURRENT_CLASS foundation-contract/proof-boundary drift` classification because the calculation-owner role can still hold direct read/write privilege on M00-owned relations. The accepted brief clause 10 and REQ-005 require both boundary separation and no calculation-owner database-role privilege to read or write M00-owned tables.

Under the existing same-actor bounded-refinement contract for `FOUNDATION-CONTRACT-PROOF-DRIFT`, DS-T01-R03 strengthens proof before any further persistence behaviour change. It does not select concrete production role/schema names, grant production privilege, or authorise M01 to read M00 row content.

## Authority-derived adverse privilege proof

`tests/implementation/derived_signal/test_ds_t01_r03_postgres_privilege_boundary_refinement.py` directly exercises five propositions against real PostgreSQL 17.9:

1. a distinct M01 writer/schema holding effective `SELECT` on an M00-owned relation must be refused by persistence construction;
2. effective `INSERT` privilege on that M00 relation must be refused;
3. effective `UPDATE` privilege on that M00 relation must be refused;
4. effective `DELETE` privilege on that M00 relation must be refused; and
5. a lawfully constructed persistence object must fail closed if M01 later gains effective `SELECT` privilege on the M00 relation before an operation.

The proof derives the M00/M01 role and schema identities from the live database. It grants only temporary proof-environment schema usage and table privilege, verifies that the adverse privilege is actually effective through the M01 role, and revokes it in cleanup. The proof never reads M00 row content as part of the product mechanism and does not fix production role/schema names.

## Expected-red execution before DS-I01-R03

A fresh hash-verified Python 3.13.5 / psycopg 3.3.4 / PostgreSQL 17.9 proof environment was reconstructed from the preserved offline bootstrap/runtime assets. Temporary proof-only database identities are `nvda_m00_r03` / `m00_r03` and `nvda_m01_r03` / `m01_r03`.

Against the current reviewed candidate, before any production repair, observed:

```text
pytest -q tests/implementation/derived_signal/test_ds_t01_r03_postgres_privilege_boundary_refinement.py
5 failed
```

Each failure occurs because a `ValueError` is required but the existing persistence mechanism constructs or operates successfully while the M01 role has the adverse effective M00-table privilege. The test file itself passes Ruff:

```text
ruff check tests/implementation/derived_signal/test_ds_t01_r03_postgres_privilege_boundary_refinement.py
All checks passed!
```

This is the intended proof-first red state. No production source, architecture, package metadata, schema definition or previously accepted proof byte was changed to obtain it. DS-I01-R03 remains blocked until this proof refinement is durably accepted.
