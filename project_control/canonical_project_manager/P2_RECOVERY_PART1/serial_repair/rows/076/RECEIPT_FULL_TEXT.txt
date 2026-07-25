# Semantic receipt — `tests/tier_a/parallel_risk/test_parallel_risk_missing_signal_register.py`

## File evidence

- Sequence `076`, unit `PM-014`; test SHA-256 `c9e3aeec29f40d43f487f42acf459793679f1fcee402683e5a59c97c6a94fecc`.
- Full reads: test `1-70`; missing-signal helper `src/nvda_desk/domain/parallel_risk/missing_signals.py:1-74`; raw ingress `src/nvda_desk/upstream/raw_signal_ingress.py:1-93`; upstream-signal contracts `src/nvda_desk/contracts/upstream_signal.py:1-87`; prepared-data law `docs/04.2_PREPARED_DATA_CONTRACTS_WORKING.md:17-25,48-83`; native preparation and Parallel Risk seams `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:203-218,254-269`.
- Raw test result: `3 passed in 0.14s`.

## G1 — `test_missing_signal_register_entry_is_metadata_only_and_lowers_confidence`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_missing_signal_register.py:11-25`; assertions cover references, default impact and absence of two literal substrings.
- Authority locator: `NO_VALID_AUTHORITY_RELATIONSHIP` for the Missing Signal Register taxonomy, workbook-reference fields or default confidence consequence.
- Authority match: explicit no-value metadata is compatible with preparation law, but this carrier and consequence are not proposition-level admitted.
- Behaviour proved: one fixture retains references, defaults to `lowers_confidence`, and omits the two selected strings.
- Limitation: token absence does not prove metadata-only behaviour, and no consumer consequence is tested.
- Adversarial challenge: add a differently named execution instruction or side effect while preserving all assertions.
- Exact-surface falsifier: change the asserted default or reference so an assertion in lines `19-23` fails.
- Assertion that must fail and why: line `19` fails if the helper no longer defaults the impact to `lowers_confidence`; lines `20-21` fail if either supplied inventory/workbook reference is lost; and lines `22-23` fail only if the exact words `trade` or `order` appear. Those token checks cannot detect differently named execution authority or a side effect outside the model.
- Semantic relation: `authority_missing`.
- Proof strength: `presence_only`.
- Disposition and return gate: `BLOCKED_P3_REPAIR`; retain only as repair evidence pending an admitted missing-signal carrier and consequence law.

## G2 — `test_quarantined_upstream_signal_becomes_snapshot_absence_not_runtime_signal_value`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_missing_signal_register.py:28-48`; assertions follow a raw-ingress quarantine result directly into a Parallel Risk snapshot absence.
- Authority locator: `docs/04.2_PREPARED_DATA_CONTRACTS_WORKING.md:48-83` and `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:203-218,254-269`.
- Authority match: the governing seam requires typed preparation between upstream evidence and Parallel Risk; this test endorses direct consumption of a raw-ingress result instead.
- Behaviour proved: for the fixture, a caller-controlled family set marks the signal quarantined and the helper emits a no-value snapshot entry.
- Limitation: the path bypasses prepared-substrate identity, schema/version, validation and source-preserving transformation authority.
- Adversarial challenge: a caller can alter the admitted-family set and thereby decide semantic admission without governed coverage/config authority.
- Exact-surface falsifier: change the quarantined result to lawful or emit a runtime signal value; an assertion at lines `42-48` must fail. Routing through an admitted prepared carrier would require a replacement assertion at the `BLOCKED_P3_REPAIR` gate.
- Assertion that must fail and why: line `42` fails if the raw ingress is not quarantined; lines `43-48` fail if its family identity, absent value, rejection reason or false lawful-use flag changes. Every assertion can remain green while the helper still consumes a raw-ingress result directly instead of an admitted prepared carrier, which is the architectural defect requiring P3 repair.
- Semantic relation: `authority_contradictory`.
- Proof strength: `boundary`.
- Disposition and return gate: `BLOCKED_P3_REPAIR`; repair by moving quarantine/admission upstream under governed configuration and consuming only a typed prepared carrier.

## G3 — `test_admitted_trace_only_signal_snapshot_does_not_strip_trace_lineage`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_missing_signal_register.py:51-70`; assertions expect an admitted raw payload to become a snapshot after recursive removal of named fields while retaining trace references.
- Authority locator: `docs/04.2_PREPARED_DATA_CONTRACTS_WORKING.md:58-83`.
- Authority match: source truth remains owned upstream and preparation must project a separately governed value with explicit identity; destructive rewriting of the raw payload and caller-set admission conflict with that law.
- Behaviour proved: the fixture retains selected trace references after the helper strips prohibited keys from the payload.
- Limitation: preserved trace strings do not restore the original source bytes, governed projection version or lawful admission decision.
- Adversarial challenge: stripping can silently remove material source evidence or miss synonymous authority keys while all assertions remain green.
- Exact-surface falsifier: retain `trade_allowed` in the projected value, strip `source-2`, or mark the admitted signal unavailable; an assertion at lines `65-70` must fail. Preserving immutable raw input separately requires a new assertion at `BLOCKED_P3_REPAIR`.
- Assertion that must fail and why: lines `65-69` fail if the admitted fixture loses its present state, projected payload, source identity or true use flag, and line `70` fails if the exact key `trade_allowed` survives. The group does not retain or compare immutable raw bytes, so destructive source rewriting and missed authority aliases are not falsified by these assertions.
- Semantic relation: `authority_contradictory`.
- Proof strength: `behavioural`.
- Disposition and return gate: `BLOCKED_P3_REPAIR`; repair requires source-preserving lineage, typed preparation and non-caller-owned admission.

## File decision

- Groups/relationships: `3/3`.
- Final disposition: `BLOCKED_P3_REPAIR`.
- The file demonstrates current behaviour but endorses a prohibited raw-ingress-to-Parallel-Risk path and destructive source rewriting. Repair must precede any Tier A admission.
