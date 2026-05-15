# FWD-007 Raw signal families Closure Gate Receipt

Created UTC: 2026-05-14T13:35:00Z

## Decision

`FWD-007 / 5.3 Raw signal families` is recorded as `bounded_closed_current` for this bounded gate.

## Evidence counts

- Selected native Bridge/Atlas rows: 123
- Primary active-code records: 4
- Comparison groups: 3
- Queue records: 3
- Direct selected native Atlas links: 0
- Grouped-satisfaction overlay links: 123
- Current unresolved selected native Atlas IDs: 0

## Proof basis

- Targeted proof reruns: `raw_signal_contract_copy_boundary_surface, raw_signal_transform_boundary_surface` returned exit code `0` with contract copy boundary 2 passed, transform boundary 2 passed.
- Tier A/B batch regression proof records 609/609 collected unique nodes passed with captured exit-code receipts.
- Earlier batch attempts that printed pass summaries without exit-code receipts are retained only as superseded setup evidence and are not used for closure.

## Mutation boundary

No source, test, config, fixture, dependency, original Atlas/Bridge JSON, or generated slice mutation was made.
