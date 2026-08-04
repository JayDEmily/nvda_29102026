# Gate 123 — Coefficient Authority Contract

Status: complete on `main`; Gate 124 is now the active gate in the signal-coefficient authority pack

## Purpose

Install the typed governed coefficient-authority contract and the first authority file without promoting the legacy example registry into runtime truth.

## What changed

- `src/nvda_desk/config_models.py` now defines a typed governed authority schema for mutable runtime surfaces, temporal thresholds, and timing parameters.
- `config/coefficient_authority.v1.yaml` now freezes the admitted tranche-one authority file with explicit owner stage, units, baseline, min/max envelope, transform family, and allowed upstream drivers.
- Config docs and example path surfaces now distinguish the governed authority file from the legacy salvage/example registry.
- Deterministic validation tests now fail cleanly on unknown surfaces, absurd ranges, and illegal transform families.

## Proof slice

- `PYTHONPATH=src pytest -q tests/test_gate122_signal_coefficient_authority_planning.py tests/test_gate122_signal_coefficient_authority_closeout.py tests/test_gate123_coefficient_authority.py tests/test_fixtures_and_config.py tests/test_boundaries_and_config_surface.py tests/test_playbook_registry.py`

## Outcome

- the repo now has one typed governed coefficient-authority contract for the admitted tranche-one universe
- the legacy `coefficients_registry.example.yaml` remains reference-only rather than becoming runtime authority by drift
- Gate 124 can now externalise mutable runtime surfaces from hard-coded constants into a governed file that already validates deterministically

## Packaged artefact

- `nvda_repo_signal_coefficient_authority_gate123_main_2026-03-31.zip`
