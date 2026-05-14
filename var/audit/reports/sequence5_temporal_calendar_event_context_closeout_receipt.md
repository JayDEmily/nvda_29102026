# Sequence 5 closeout receipt — temporal/calendar/event context

Result: PASS

Created at UTC: `2026-05-04T05:51:04Z`

## Source lock

- expected size: `2876879`
- actual size: `2876879`
- expected SHA256: `bfcdac024ac9f3c459a035b16e24d45681f13c9956e8532f8dbc83b4bf6f87cc`
- actual SHA256: `bfcdac024ac9f3c459a035b16e24d45681f13c9956e8532f8dbc83b4bf6f87cc`
- verified: `True`

## Pass criteria disposition

| Criterion | Result |
|---|---|
| Source lock verifies exactly | PASS |
| Required exact read-set files exist/read in full | PASS |
| Present temporal/calendar/event evidence directories fully read | PASS |
| JSON source surfaces parse | PASS |
| 18 Atlas slices accounted | PASS |
| 1,716 Sequence 1 records accounted upstream | PASS |
| Mandatory Sequence 5 relevant records assigned disposition | PASS |
| No relevant duplicate/unassigned records | PASS |
| Scheduled events metadata/context only | PASS |
| Unscheduled events repricing-shock context only | PASS |
| Serial/parallel/downstream capital/temporal boundaries separated | PASS |
| No forbidden source modifications | PASS |
| Sequence 6 readiness stated without opening Sequence 6 | PASS |

## Candidate mutation

Only allowed Sequence 5 audit/route artefacts were added under `var/audit/ledgers` and `var/audit/reports`.

## PM decision required

PM audit must decide Sequence 5 acceptance. This worker output does not self-accept.
