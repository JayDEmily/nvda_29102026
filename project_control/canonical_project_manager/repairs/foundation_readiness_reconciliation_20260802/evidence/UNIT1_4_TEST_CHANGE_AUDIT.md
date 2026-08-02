# Units 1–4 retrospective test-preservation audit

## Authority and scope

This audit applies the repository-wide rule in `AGENTS.md` to every test or test-support surface changed between accepted base `3876f17108b5c2e42510dff66e7248d622c10e47` and Unit 4 checkpoint `11699fed3838049722a16eedeb68a3ebe5f94b49`.

The inventory contains 20 changed test/support files and 47 changed top-level functions. No physical test file was deleted or renamed. The two renamed test nodes are mapped one-to-one in `UNIT1_4_TEST_CHANGE_AUTHORITY_REGISTER.tsv`; neither is treated as silent retirement.

## Findings

Four prior replacements did not fully preserve their predecessor propositions:

1. FWD-004 `default_degradation` retained fail-closed identity rejection but had dropped the original explicit trace/run, validation and summary checks.
2. FWD-004 `builder_default_surface` retained fail-closed scenario rejection but had dropped module-version, module-instance and summary checks.
3. FWD-009 `prepared_context_packet_trace_review` proved that a raw compatibility snapshot was rejected but had dropped the original packet fingerprint, role/schema, producer, trace, review-trace and payload-identity checks.
4. FWD-005’s renamed compatibility-API test proved route absence but did not also prove absence of the corresponding methods and process-local collections.

Those propositions were restored under the existing Unit 2 and Unit 4D authority. No production compatibility shim, packet-identity default, route, method or process-local state was reintroduced.

## Dispositions

Every changed surface is recorded in `UNIT1_4_TEST_CHANGE_AUTHORITY_REGISTER.tsv` with:

- old and replacement node or helper;
- governing authority;
- original behavioural proposition;
- replacement assertion or fixture;
- preservation disposition; and
- executable evidence.

The permitted dispositions are limited to added current-law proof/support, fixture authority completion, assertion strengthening, temporal control-state transition, or explicit normative supersession of only the obsolete seam while retaining the underlying behavioural proposition.

## Executable evidence

| Gate | Result |
|---|---:|
| Changed-file affected cone | 439 passed; 0 failed; 0 skipped |
| Physical Tier A | 1,990 passed; 0 failed; 0 skipped |
| Physical Tier B | 91 passed; 0 failed; 0 skipped |
| Physical Tier C | 5 passed; 0 failed; 0 skipped |
| Proof authority | 201 families; 203 paths; 73 blocks |
| Proof-block definitions | 73/73 valid |
| Vocabulary | 13/13 namespaces clean; 6 exact occurrence renewals |
| Added skip/xfail/equivalent mechanisms | 0 |
| Deleted or renamed physical test files | 0 |

The six vocabulary renewals are exact line/context shifts caused by restored FWD-009 assertions. They reuse the prior occurrence-specific semantic disposition; no canonical label, alias or broad suppression changed.

## Verdict

**PASS.** Units 1–4 contain no unrecorded test retirement. The four under-preserved replacements have been repaired, all 47 changed surfaces are authority-mapped, and the current physical proof universe remains fully green.
