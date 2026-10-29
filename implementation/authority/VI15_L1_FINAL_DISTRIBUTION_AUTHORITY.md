# VI-15-L1 — Final distribution metadata authority

## Status

**PROGRAMME OWNER AUTHORITY SUPPLIED — BINDING FOR VI-15-L1.**

## Authority

During the VI-15-L1 mandatory Programme Owner checkpoint on 2026-09-28, after the Worker
reported the current distribution identity `nvda-architecture-kernel==0.1.0` and the exact
consequences of retaining or changing it, the Programme Owner directed that the distribution name
remain unchanged and the version be promoted to `1.0.0`, then explicitly instructed the Worker to
proceed.

The binding final distribution metadata for this leaf is therefore exactly:

- distribution name: `nvda-architecture-kernel`;
- distribution version: `1.0.0`.

## Scope of the authority

This decision closes only the final distribution-name/version Remaining Unknown carried to VI-15.
It does not reopen or change:

- Python import/package topology;
- M-owner identity `nvda_desk.raw_signal_occurrence_truth`;
- public seam `nvda_desk.raw_signal_occurrence_truth.api`;
- runtime dependencies;
- product semantics or proof meaning;
- PostgreSQL mechanism/authority;
- any downstream VI-15-L2 packaging proposition.

Historical evidence that truthfully records earlier `0.1.0` states remains historical evidence and
is not rewritten merely because `1.0.0` is now the authorised final distribution version.

## Required metadata consequence

The previously established pre-authority inspection identified the strictly necessary consequences
of changing the version:

1. set `[project].version` in `pyproject.toml` to `1.0.0`;
2. keep `nvda_desk.__version__` truthful at `1.0.0`;
3. update the bootstrap assertion that binds `nvda_desk.__version__` to the authorised version.

No distribution-name mutation is required.
