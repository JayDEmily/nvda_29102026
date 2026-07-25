# Semantic receipt — `tests/tier_a/testing_harnesses/test_module_8_parallel_risk_workbook_specimen_surface.py`

## File evidence

- Sequence `093`, unit `PM-014`; test SHA-256 `dd4b6a269459b4a3f97e387c486006f723824f29484a0a9dbb265d8e3135a626`.
- Full reads: test `1-40`; complete harness `src/nvda_desk/testing/harnesses/module_8_parallel_risk_workbook_specimen.py`; workbook reference-ledger authority `docs/reference/SIGNAL_WORKBOOK_AUTHORITY.md:26-34,75-86`; DMP fixture, lineage and temporal law `docs/09.1_DMPV3_PROTOCOL_WORKING.md:25-79`.
- Raw test result: `1 passed in 0.20s`.

## G1 — `test_module_8_parallel_risk_workbook_mapping_surface_is_present`

- Test locator: `tests/tier_a/testing_harnesses/test_module_8_parallel_risk_workbook_specimen_surface.py:12-40`; assertions cover the mapping type, one hard-coded workbook path, selected temporal/regime/options values, selected cell references, one `derivedfrom` string and an `inputfingerprint` prefix.
- Authority locator: `docs/reference/SIGNAL_WORKBOOK_AUTHORITY.md:26-34,75-86` and `docs/09.1_DMPV3_PROTOCOL_WORKING.md:37,41-79`.
- Authority match: the authority permits a bounded test-owned workbook specimen to preserve field provenance and date-level temporal truth; it expressly withholds direct runtime authority from the workbook and requires an admitted semantic fingerprint rather than an unexplained hash.
- Behaviour proved: the builder returns the asserted specimen type and currently maps the selected reference cells to the asserted values, missing-field lists, provenance labels and date-only temporal fields.
- Limitation: the test does not authenticate the workbook bytes, reconcile the selected cells against a governed source, prove role-specific Stage Input Bundle admission, inspect the fingerprint value beyond its prefix, or exercise live/replay consumption.
- Adversarial challenge: substitute a different workbook with the same path and selected values, or hash an arbitrary serialisation while preserving the `sha256:` prefix; every assertion can remain green although source identity and semantic fingerprint authority are false.
- Exact-surface falsifier: change the mapped `temporal.source_date`, `regime.vix_level`, `options_flow.spot_price`, a named cell reference, `derivedfrom`, or remove the `sha256:` prefix; the corresponding assertion at lines `15-40` must fail.
- Assertion that must fail and why: at test lines `15-40`, changing the mapping type, workbook path, selected temporal/regime/options values, missing-field lists, named cell references, `derivedfrom` string, or removing the `sha256:` prefix breaks its corresponding assertion. A substituted workbook or meaningless hash with the same selected outputs and prefix remains undetected.
- Semantic relation: `bounded_separable_clause`.
- Proof strength: `specimen_only`.
- Disposition and return gate: `NON_AUTHORITATIVE_OBSERVATIONAL`; retain as a deterministic selected-cell mapping specimen, and return for promotion only after workbook-byte identity, governed source reconciliation, semantic-fingerprint verification and role-specific input admission are executable.

## File decision

- Groups/relationships: `1/1`.
- Final disposition: `NON_AUTHORITATIVE_OBSERVATIONAL`.
- Preserve as non-authoritative workbook-mapping observation evidence; do not represent it as Tier A runtime or source authority.
