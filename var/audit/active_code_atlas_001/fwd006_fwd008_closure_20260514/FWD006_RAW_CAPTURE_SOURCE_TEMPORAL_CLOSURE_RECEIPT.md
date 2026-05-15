# FWD-006 Raw capture and source temporal law Closure Gate Receipt

Created UTC: 2026-05-14T13:35:00Z

## Decision

`FWD-006 / 5.2 Raw capture and source temporal law` is recorded as `bounded_closed_current` for this bounded gate.

## Evidence counts

- Selected native Bridge/Atlas rows: 108
- Primary active-code records: 3
- Comparison groups: 3
- Queue records: 3
- Direct selected native Atlas links: 0
- Grouped-satisfaction overlay links: 108
- Current unresolved selected native Atlas IDs: 0

## Proof basis

- Targeted proof reruns: `raw_capture_source_temporal_law_surface, raw_capture_transform_boundary_surface, source_temporal_standard_surface` returned exit code `0` with raw bundle loader 3 passed, transform boundary 3 passed, source temporal standard 4 passed.
- Tier A/B batch regression proof records 609/609 collected unique nodes passed with captured exit-code receipts.
- Earlier batch attempts that printed pass summaries without exit-code receipts are retained only as superseded setup evidence and are not used for closure.

## Mutation boundary

No source, test, config, fixture, dependency, original Atlas/Bridge JSON, or generated slice mutation was made.
