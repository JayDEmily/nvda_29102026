# Config Surfaces

These files preserve two different config roles. They are not interchangeable.

## Governed coefficient authority

- `coefficient_authority.v1.yaml`

This is the typed Gate 123 authority surface for the admitted tranche-one coefficient universe only. It freezes owner stage, units, baseline, min/max envelope, transform family, and allowed upstream drivers for the coefficient surfaces that later gates may wire into runtime.

This file is governed authority even though Gate 124 and Gate 126 have not yet wired every consumer to it. It is not a salvage placeholder.

## Legacy example and salvage surfaces

These files preserve useful structure salvaged from the master archive. They remain **example-only** and are not the governed runtime authority for coefficient surfaces.

Files:
- `runtime_settings.example.yaml`
- `evaluation_config.example.yaml`
- `coefficients_registry.example.yaml`
- `strategy_variants.example.yaml`

Use the example files as compatibility/reference inputs when promoting more of the archive into typed runtime configuration. Do not treat `coefficients_registry.example.yaml` as interchangeable with `coefficient_authority.v1.yaml`. Gate 124 runtime mutable-surface baselines, floors, and caps now load from `coefficient_authority.v1.yaml`; Gate 126 now reads the admitted temporal threshold and timing subset from the same governed file inside `TemporalStateClassifier`; the salvage registry remains reference-only.

## Governed signal workbook lineage

The canonical vocabulary slug for this lineage surface is `signal_coefficient_reference_workbook`.
The canonical workbook reference ledger is `data/reference/signal_workbooks/2026-03-25_NVDA_SIGNAL_WORKBOOK_v3_bounds_handoff_copy.xlsx`. It is discoverable law and provenance only, not direct runtime authority. When typed config or contracts are promoted from workbook material, they must preserve workbook lineage through `workbook_ref` or successor lineage fields. See `docs/reference/SIGNAL_WORKBOOK_AUTHORITY.md`.
