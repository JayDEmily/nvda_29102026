# Atlas Roadmap Schema Repair Receipt — Worker Gate 6A

## Scope

Gate 6A repairs only the roadmap ledger schema so a later Gate 6 rerun can record either candidate-only selection or a truthful blocked/no-selection outcome without modifying the existing Gate 5 ledger.

This gate does not modify the ledger, does not perform candidate selection, does not create roadmap closeout, does not open implementation, and does not change runtime, tests, vocabulary, generated Atlas slices, original Atlas/Bridge JSON, or planning-compiler code.

## Source ZIP lock

```text
path=/mnt/data/NVIDIA9_remotetest-main_gate5_roadmap_ledger_schema_applied_2026-05-01.zip
SHA256=2fdf3a4549e83535cfdafbffaf3e1386fd8e78b0940c8fdde80ec88914b81ba3
size_bytes=2863457
archive_integrity=PASS
unzip -tq output: No errors detected in compressed data of /mnt/data/NVIDIA9_remotetest-main_gate5_roadmap_ledger_schema_applied_2026-05-01.zip.
```

## Why Gate 6 stopped before Gate 6A

Gate 6 correctly stopped because the Gate 5 schema hard-coded the Gate 5 not-opened state and could not truthfully represent either:

1. a lawful Gate 6 candidate-only selection state; or
2. a truthful Gate 6 blocked/no-selection state.

## Exact schema blockers repaired

The repaired schema broadens only the blocked Gate 5 constants that prevented later truthful Gate 6 recording:

1. top-level `gate` changed from `const: "Worker Gate 5"` to enum permitting `"Worker Gate 5"` and `"Worker Gate 6"`;
2. top-level `status` changed from Gate-5-only constant to enum permitting Gate 5 not-opened, Gate 6 candidate-only selection completed, and Gate 6 blocked;
3. `candidate_selection.status` changed from Gate-5-only constant to enum permitting Gate 5 not-opened, Gate 6 candidate-only selection completed, and Gate 6 blocked;
4. `candidate_selection.selected_candidate` changed from `type: null` to `null` or a bounded object requiring:
   - `tranche_id`
   - `source_slice_path`
   - `blueprint_surface`
   - `selection_status`
   - `candidate_only`
   - `selection_reason`
5. `roadmap_tranches[].candidate_only_flag` changed from `const: false` to boolean;
6. `roadmap_tranches[].candidate_selection_status` changed from Gate-5-only constant to enum permitting Gate 5 not-opened, Gate 6 not-selected, Gate 6 candidate-only selected, and Gate 6 blocked;
7. `roadmap_tranches[].status` changed from Gate-5-only constant to enum permitting Gate 5 not-opened, Gate 6 not-selected, Gate 6 candidate-only selected, and Gate 6 blocked;
8. tranche-level conditional rules were added so each `candidate_selection_status` still forces the matching tranche `status` and `candidate_only_flag`;
9. top-level conditional rules were added so:
   - Gate 5 still requires the old not-opened state and forbids any selected tranche;
   - Gate 6 candidate-only completion requires `candidate_selection.selected_candidate` object plus exactly one selected tranche;
   - Gate 6 blocked state requires `selected_candidate = null` and forbids any selected tranche.

Implementation boundary state remains explicitly required and remains closed.

## Changed files

```text
var/audit/ledgers/atlas_tranche_roadmap_ledger.schema.json
var/audit/atlas_roadmap/2026-05-01_ATLAS_ROADMAP_SCHEMA_REPAIR_RECEIPT.md
```

## Temporary validation artefacts

Synthetic Gate 6 validation files were written outside the repo only:

```text
/mnt/data/gate6a_validation/gate6_candidate_only.synthetic.json
/mnt/data/gate6a_validation/gate6_blocked.synthetic.json
```

## Validation commands and results

### JSON parse validation

```text
PASS jq -e schema
PASS jq -e ledger
PASS jq -e synthetic_candidate
PASS jq -e synthetic_blocked
```

### Deterministic schema validation

```text
PASS gate5_current_ledger
PASS gate6_candidate_only_synthetic
PASS gate6_blocked_synthetic
```

## Proof that the existing Gate 5 ledger still validates and was not modified

Validation result:

```text
PASS gate5_current_ledger
```

Byte-for-byte ledger preservation proof:

```text
37807e2d7bc364f52f0f98087255917208adeda2ac946db3fe56dc28b8b4e5ed  /mnt/data/gate6a_work/original/NVIDIA9_remotetest-main/var/audit/ledgers/atlas_tranche_roadmap_ledger.json
37807e2d7bc364f52f0f98087255917208adeda2ac946db3fe56dc28b8b4e5ed  /mnt/data/gate6a_work/repo/NVIDIA9_remotetest-main/var/audit/ledgers/atlas_tranche_roadmap_ledger.json
PASS ledger unchanged byte-for-byte
```

## Proof that synthetic Gate 6 states validate

```text
PASS gate6_candidate_only_synthetic
PASS gate6_blocked_synthetic
```

## Candidate-selection boundary

Candidate selection was not performed in Gate 6A.

The repo ledger remains unchanged and still records:

```text
candidate_selection.status = not_opened_in_gate_5
candidate_selection.selected_candidate = null
```

## Implementation boundary

Implementation remains closed.

The repaired schema still requires explicit implementation-boundary objects and still keeps both top-level and tranche-level implementation status fixed at:

```text
implementation_closed
```

## Route-control confirmation

`READY_TO_CONSIDER_ATLAS = false` remains controlling.

Gate 6A is a schema-repair gate only and does not claim Atlas readiness, runtime readiness, repo-wide proof completion, or full semantic review of all 1,716 Atlas records.
