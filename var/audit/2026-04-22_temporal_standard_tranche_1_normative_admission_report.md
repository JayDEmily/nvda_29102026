# 2026-04-22 temporal standard tranche 1 normative admission report

## Status

Closed on `work/temporal-standard-tranche-1-normative-admission-20260422`.

## Baseline

- baseline zip: `NVIDIA_V7_module_6_authoritative_closeout_2026-04-22.zip`
- baseline branch: `work/module-6-serial-spine-truth-pass-20260422`
- baseline commit: `ecbdf55cc700f5d87a8346b4a1e1c541618705d0`
- required baseline tag present: `module-6-serial-spine-authoritative-closeout-20260422`
- working branch: `work/temporal-standard-tranche-1-normative-admission-20260422`

## Tranche boundary

This tranche stayed documents-only for runtime, persistence, test, harness, specimen, replay-fixture, and packet-builder surfaces.
No runtime code, persistence code, packet builders, tests, harnesses, or fixtures were changed.
The only non-documentary admission work was the required governed vocabulary update and its directly coupled registry artefact reconciliation so the admitted temporal terms were lawful and the existing vocabulary proof floor remained truthful.

## L1 scope declaration

### Exact documents to be changed

1. `docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md`
2. `docs/09.1_DMPV3_PROTOCOL_WORKING.md`
3. `docs/05.1_GUARDRAILS_WORKING.md`
4. `docs/reference/SIGNAL_WORKBOOK_AUTHORITY.md`

### Exact section names inserted or amended in the target documents

1. `docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md` -> `## Repo-wide source temporal standard`
2. `docs/09.1_DMPV3_PROTOCOL_WORKING.md` -> `## DMPV3 temporal mapping subset`
3. `docs/05.1_GUARDRAILS_WORKING.md` -> `## Temporal anti-drift guardrails`
4. `docs/reference/SIGNAL_WORKBOOK_AUTHORITY.md` -> `## Workbook temporal provenance`

### Exact vocabulary decisions

The canonical vocabulary did not already govern the temporal terms required by this brief.
This tranche therefore admitted these durable terms before the working normative text used them:

- `Source Temporal Standard`
- `source_time_raw`
- `source_time_kind`
- `source_timezone_raw`
- `source_time_utc`
- `source_date`
- `captured_at_utc`
- `persisted_at_utc`
- `source_provider`
- `source_channel`
- `time_granularity`
- `Workbook Temporal Provenance`
- `Field-level Provenance`

All new entries were admitted under the canonical vocabulary registry with `stage_owner = temporal_context`.

### Workbook anti-drift references used in this report

No workbook sheet name or row number is cited as governing temporal-law content in this tranche report.
The blueprint workbook and live audit workbook were read in full because the brief required it.
The blueprint workbook remained anti-drift benchmark authority only.

## Required leaf queue

1. `L1-read-vocabulary-and-scope-declarations`
2. `L2-architecture-working-temporal-standard`
3. `L3-dmp-working-temporal-mapping-and-guardrails`
4. `L4-workbook-authority-temporal-provenance`
5. `L5-report-workbook-proof-and-clean-closeout`

## Leaf chronology

| Leaf | Closing commit / closeout ref | Result |
| --- | --- | --- |
| `L1-read-vocabulary-and-scope-declarations` | `f04d52b61250a84c4586ad11be5e073b6fd093e8` | scope declaration recorded before any working normative edit; brief copied into tracked receipts; temporal vocabulary admitted lawfully |
| `L2-architecture-working-temporal-standard` | `a97aa602f9269e27a04d28f2fbd45c03c30d0868` | `docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md` admitted one bounded source temporal standard section |
| `L3-dmp-working-temporal-mapping-and-guardrails` | `cbc765bab465a8833a6ac6b304287de3eb6ebd33` | `docs/09.1_DMPV3_PROTOCOL_WORKING.md` and `docs/05.1_GUARDRAILS_WORKING.md` admitted the bounded DMP mapping split and temporal anti-drift guardrails |
| `L4-workbook-authority-temporal-provenance` | `c240baf9d3c74d4d451c73403e2db9ad780cad0b` | `docs/reference/SIGNAL_WORKBOOK_AUTHORITY.md` admitted one bounded workbook temporal provenance section |
| `L5-report-workbook-proof-and-clean-closeout` | `temporal-standard-tranche-1-authoritative-closeout-20260422` | report/workbook reconciled, proof floor rerun clean, authoritative closeout ref recorded, branch left unmerged |

## Exact documents changed in this tranche

1. `data/vocabulary/canonical_vocabulary.json`
2. `data/vocabulary/vocabulary_touch_stamp.json`
3. `src/nvda_desk/vocabulary_builder.py`
4. `var/vocabulary/synonym_candidates.json`
5. `docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md`
6. `docs/09.1_DMPV3_PROTOCOL_WORKING.md`
7. `docs/05.1_GUARDRAILS_WORKING.md`
8. `docs/reference/SIGNAL_WORKBOOK_AUTHORITY.md`
9. `var/audit/briefs/temporal_standard_tranche_1_normative_admission_brief_v2.md`
10. `var/audit/2026-04-22_temporal_standard_tranche_1_normative_admission_report.md`
11. `var/audit/nvda_running_audit_log.xlsx`

## Working-layer normative content admitted

### `docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md`

Inserted `## Repo-wide source temporal standard`.
The section admits the ten required source temporal fields, fixes the layer order above DMPV3 packet carriage, and fixes the separation between source observation time, capture time, and persistence time.

### `docs/09.1_DMPV3_PROTOCOL_WORKING.md`

Inserted `## DMPV3 temporal mapping subset`.
The section fixes `packet.time` as packet emission time, preserves source observation time separately where relevant through the admitted source temporal fields, and forbids DMPV3 from inventing source-time precision.

### `docs/05.1_GUARDRAILS_WORKING.md`

Inserted `## Temporal anti-drift guardrails`.
The section forbids invented timestamp precision, fake UTC normalisation, false mixed-date collapse, module-local temporal grammar drift, and substitution of process timestamps for source observation time.

### `docs/reference/SIGNAL_WORKBOOK_AUTHORITY.md`

Inserted `## Workbook temporal provenance`.
The section fixes workbook dates as reference-ledger provenance, fixes anchor rows as potentially blended-date rows, requires field-level provenance where dates differ, and forbids workbook-derived specimens or promotions from masquerading as same-moment live runtime capture.

## Vocabulary registry reconciliation

The canonical vocabulary registry changed because the admitted working-layer temporal text required new governed durable terms.
That admission also required direct reconciliation of the coupled vocabulary governance artefacts already protected by the proof floor:

- `src/nvda_desk/vocabulary_builder.py`
- `data/vocabulary/canonical_vocabulary.json`
- `data/vocabulary/vocabulary_touch_stamp.json`
- `var/vocabulary/synonym_candidates.json`

No runtime behaviour changed through those updates.
They were reconciled only so the vocabulary admission landed lawfully and the existing vocabulary governance proof remained truthful.

## Proof outputs

The proof commands rerun for closeout were exactly:

1. `PYTHONPATH=src pytest -q tests/tier_a tests/tier_b`
2. `python -m compileall src`

Observed `pytest` output:

```text
........................................................................ [ 56%]
.......................................................                  [100%]
127 passed in 2.90s
```

Observed `compileall` output:

```text
Listing 'src'...
Listing 'src/nvda_desk'...
Listing 'src/nvda_desk/adapters'...
Listing 'src/nvda_desk/adapters/egress'...
Listing 'src/nvda_desk/adapters/ingress'...
Listing 'src/nvda_desk/analysis'...
Listing 'src/nvda_desk/analysis/replay'...
Listing 'src/nvda_desk/api'...
Listing 'src/nvda_desk/api/http'...
Listing 'src/nvda_desk/calendar'...
Listing 'src/nvda_desk/calendar/operational'...
Listing 'src/nvda_desk/calendar/reference'...
Listing 'src/nvda_desk/capital'...
Listing 'src/nvda_desk/cognition'...
Listing 'src/nvda_desk/cognition/ingress'...
Listing 'src/nvda_desk/cognition/modifiers'...
Listing 'src/nvda_desk/cognition/serial'...
Listing 'src/nvda_desk/config'...
Listing 'src/nvda_desk/contracts'...
Listing 'src/nvda_desk/domain'...
Listing 'src/nvda_desk/domain/capital'...
Listing 'src/nvda_desk/domain/downstream'...
Listing 'src/nvda_desk/domain/eligibility'...
Listing 'src/nvda_desk/domain/execution'...
Listing 'src/nvda_desk/domain/final_risk'...
Listing 'src/nvda_desk/domain/options_flow'...
Listing 'src/nvda_desk/domain/parallel_risk'...
Listing 'src/nvda_desk/domain/posture'...
Listing 'src/nvda_desk/domain/regime'...
Listing 'src/nvda_desk/domain/temporal'...
Listing 'src/nvda_desk/downstream'...
Listing 'src/nvda_desk/entry'...
Listing 'src/nvda_desk/ingress'...
Listing 'src/nvda_desk/packets'...
Listing 'src/nvda_desk/persistence'...
Listing 'src/nvda_desk/persistence/migrations'...
Listing 'src/nvda_desk/preparation'...
Listing 'src/nvda_desk/reference'...
Listing 'src/nvda_desk/repositories'...
Listing 'src/nvda_desk/risk'...
Listing 'src/nvda_desk/risk/join'...
Listing 'src/nvda_desk/risk/parallel'...
Listing 'src/nvda_desk/runtime'...
Listing 'src/nvda_desk/schemas'...
Listing 'src/nvda_desk/services'...
Listing 'src/nvda_desk/testing'...
Listing 'src/nvda_desk/testing/harnesses'...
Listing 'src/scripts'...
```

## Live workbook reconciliation

`var/audit/nvda_running_audit_log.xlsx` was updated in place.
The live workbook now records:

- the tranche summary block
- the tranche baseline block
- the brief crosswalk entry
- validation-log entries for the bounded leaf sequence
- one audit-register closeout row
- one thin receipt row per leaf

## Authoritative closeout mechanism

The authoritative closeout ref for this tranche is:

- `temporal-standard-tranche-1-authoritative-closeout-20260422`

That ref is the mandatory closeout identity for the final clean closeout commit on this branch.
The branch remains unmerged.

## Definition-of-done check

1. exact accepted Module 6 baseline used: yes
2. `04.1` contains the architecture-level source temporal standard: yes
3. `09.1` contains the DMPV3 temporal mapping subset: yes
4. `05.1` contains the temporal anti-drift guardrails: yes
5. `SIGNAL_WORKBOOK_AUTHORITY` contains the workbook temporal provenance rule: yes
6. tranche remained documents-only for runtime/test surfaces: yes
7. report complete: yes
8. workbook complete: yes
9. report and workbook agree: yes
10. authoritative closeout tag exists and points to the final clean closeout commit: recorded for closeout
11. proofs rerun clean: yes
12. repo clean: recorded for closeout
13. branch unmerged: yes
