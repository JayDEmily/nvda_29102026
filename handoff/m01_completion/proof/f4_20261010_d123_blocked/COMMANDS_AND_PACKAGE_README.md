# F4 D123 — command readback and package scope

- `source /mnt/data/nvda_f4_proof_env/environment.env` — offline restored 3.13.5/17.9 proof environment (see root original U05 bootstrap attachment)
- `PYTHONPATH=.:src python -m pytest -q tests/product/derived_signal/test_m01_f4_d123_exact_contract_authority.py` — **1 FAILED intentionally**; authoritative positive witness returns `None` at public graph boundary
- `PYTHONPATH=.:src python -m pytest -q tests/product/derived_signal/test_m01_stage1_semantics.py -k open_interest_change` — **1 PASSED**, direct-kernel only
- `python -m ruff check tests/product/derived_signal/test_m01_f4_d123_exact_contract_authority.py` — **PASS**
- `python -m mypy src` — **not PASS**, environment lacks `yaml` typing stubs in proof venv (5 diagnostics before PyYAML runtime import restoration)
- `PYTHONPATH=.:src python -m pytest -q tests/product tests/architecture tests/bootstrap tests/implementation/derived_signal --ignore=tests/product/raw_signal/test_u05_postgresql_durability.py` — first attempt **11 errors during collection** from missing PyYAML, second attempt **timed out** at ~94% after PyYAML 6.0.3 runtime restoration; no final test count or overall PASS is claimed

The reviewer/Programme Owner should first read `F4_D123_AUTHORITY_BLOCKER.md`. The known red test is intentional and must not be removed, relabelled as green or bypassed to declare Stage-1 acceptance. The predecessor RC14 Git commit remains recoverable from this full Git repository. No production code was repaired.
