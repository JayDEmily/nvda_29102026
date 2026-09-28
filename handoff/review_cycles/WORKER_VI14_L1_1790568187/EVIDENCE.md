# Worker cycle evidence

**Status:** `COMPLETE`

Primary detailed evidence is:

`implementation/proof/VI14_L1_INTEGRATED_REAL_BOUNDARY_CANDIDATE_EVIDENCE.md`

## Exact candidate

- candidate commit: `076f1e979474babbb8985dc87d3b2d4d62ec0b4c`
- candidate tree: `45aec5c01ae8a35fa8879fab978c6fb0f0082140`
- parent/routed source: `00ca26815bc217b7fd4bb98a73eb2089caf94919`
- candidate change: one evidence record only; no `src/**`, `tests/**`, `config/**` or
  `pyproject.toml` mutation
- candidate binary diff SHA-256:
  `fdd1beb839a76c7fc751c75600102f0e15b90117464cdb2db562bb6a00899a70`

## Current integrated validation

On the exact candidate and current preserved proof environment:

- U05 real-PostgreSQL durability + U06 public composition + whole-U05 restart + real U06 PostgreSQL
  composition: **66/66 passed**;
- architecture/bootstrap: **74/74 passed**;
- product-proof control: **PASS**, six families, 13/13 product obligations;
- architecture validation: **PASS**;
- dependency/cycle validation: **PASS**;
- public-seam validation: **PASS**;
- mypy `src`: **PASS**, 16 source files;
- Ruff `src tests tools`: **PASS**;
- candidate `git diff HEAD^..HEAD --check`: **PASS**;
- `git fsck --full --no-reflogs`: exit `0`; dangling historical objects only.

Live proof environment: CPython 3.13.5, pytest 9.0.3, Psycopg 3.3.4, PostgreSQL 17.9, UTF8,
`fsync=on`, `synchronous_commit=on`, `full_page_writes=on`, Unix-domain socket transport.

The preserved proof bootstrap omits PyYAML; PyYAML 6.0.3 from the already-present host environment was
exposed as the missing dependency while the exact proof virtualenv remained first on `PYTHONPATH`.
No repository bytes changed and pinned pytest/Psycopg/mypy/Ruff identities remained unchanged.

No current production defect was found. VI-14-L1 independent Tester acceptance remains unproved.
