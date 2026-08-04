# Unit 4 Repair Record

These defects occurred in the newly authored architecture-kernel implementation before its checkpoint commit. They were not inherited defects and were not suppressed.

| ID | Defect | Evidence | Repair | Final proof |
|---|---|---|---|---|
| U4-D01 | Generated Python fixtures contained unescaped newline literals, causing four syntax errors. | `/tmp/unit4_initial.txt` in the execution environment; no failing file was committed. | Rewrote the affected source/test literals and reran `compileall`. | `validation/unit4_implementation_and_proof.txt` records `compileall` exit 0 and 36 tests passing. |
| U4-D02 | The proposition regex contained literal backspace bytes instead of regex word-boundary escapes, so every admitted proposition appeared unknown. | `/tmp/unit4_second.txt`; no defective regex was committed. | Replaced the control bytes with raw `\\b` boundaries and scanned all Python files for remaining non-whitespace control bytes. | Structural validation and proof-control tests pass in `validation/unit4_implementation_and_proof.txt`. |
| U4-D03 | Initial Ruff execution reported import-order, line-length and one simplification defect. | `/tmp/unit4_venv.txt`; no lint-defective checkpoint was committed. | Applied Ruff formatting, safe automated fixes and bounded manual line wrapping. | Final locked-environment lint is recorded during Unit 5. |

No test was skipped, weakened, renamed or removed to obtain the passing result.
