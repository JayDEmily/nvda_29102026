# Actual source/documentary checks

Candidate: e13ccd9d6570753027ea39832aa5f269d2aacb76 / tree 012f07b109f4b5fb7132048de919aad5c1bfaf70, clean before checks.

Command: /tmp/nvda-g61-runtime-GBILkakx/dev/bin/python /tmp/d014-authored-proof-review-g6yYjr/static_review.py

Exit 0. Interpreter: 3.12.14 (main, Aug 25 2026, 14:00:49) [Clang 22.1.3]. Four source files compile-only PASS, zero authored-module imports/execution. Six mandatory functions exactly match contract. REFUSALS50/POSITIVES6/STORAGE_CASES23; source-projected163 total cases (not pytest collection). Support has zero materialise calls. No authored Any/cast escape found. Negative sites: 18assignment,19assignment,20assignment,21assignment,22assignment,23attr-defined,24arg-type,25arg-type,26assignment,27assignment.

Exact four hashes:

- test_raw_ratio.py a7e8ec6b5aca44e21068b78eefdf619e3ffef34d52ff1e001371345aff7b0318
- _support.py 49c6149d1ff64e002154b275bc9c54793cf60623bb0c9878c0fd5539fbc058e6
- typing/valid_seam.py 3d1e2ac2449fc13be7db8f0e26c2b505dee5e6810d591dd190d4044bf859dacc
- typing/invalid_seam.py 84b2806f0c8be162321c35f792f987550a3cf2ff428d37edd007042fcc699fc9

Independent standard-library in-memory schema-information probe: configuration declarations with/without PK and kind CHECK have equal authored-profile projections: column names [owner_namespace,kind,context_id,version,payload,content_sha256], types [TEXT,TEXT,TEXT,TEXT,BLOB,TEXT], NOT NULL [1,1,1,1,1,1], STRICT1, foreign_key_check[]. sqlite_schema declarations differ. This is a documentary counterexample to those projections establishing exact schema, not domain/product/test execution.

Source observation: conflicting duplicate only `(first, replace(first, source_provider="OTHER"))` same page; identical control same page; no independent reverse/cross-page/Decimal-representation duplicate dimension. Exact lines and rationale are in REVIEW.md.

Command: /tmp/nvda-g61-runtime-GBILkakx/dev/bin/python -m ruff check tests/product/market_measurement_d014

cwd: /workspace/scratch/d549b6d808a9/resume-20261020-ejayrse7/repository. Exit0; stdout: All checks passed!

No pytest/collection/mypy/product aggregate/new-seam/application import or source mutation occurred. Check output is transcribed here; the executable independent source/probe is preserved adjacent. This file is not a raw stdout byte archive.
