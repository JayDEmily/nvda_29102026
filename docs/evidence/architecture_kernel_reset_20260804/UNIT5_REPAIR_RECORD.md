# Unit 5 Repair Record

These issues were found during packaging and closeout validation. None was suppressed and none was repaired by weakening an admitted proposition.

| ID | Finding | Repair | Evidence |
|---|---|---|---|
| U5-D01 | The first offline lock attempt resolved all operating systems and required the Windows-only `colorama` dependency of pytest, but the supplied wheelhouses contain Linux CPython 3.13.5 artefacts only. | Restricted the lock to Linux x86_64, matching the supplied platform-specific wheels. Windows portability is not claimed. | `pyproject.toml:[tool.uv]`; `uv.lock`; resolver output recorded in the execution history. |
| U5-D02 | A repository-relative wheel source recorded in `uv.lock` was not sufficient for bare `uv sync --offline`; uv still required the source policy in project configuration. | Added `no-index = true` and `find-links = ["vendor/wheels"]` under `[tool.uv]`. A new empty `.venv` then reconstructed successfully without command-line source overrides. | `validation/intermediate/unit5_initial_offline_source_failure.txt`; `validation/unit5_environment_and_promotion.txt`. |
| U5-D03 | The first installed-metadata assertion expected the display spelling `PyYAML`; the standards-normalised metadata returned `pyyaml`. | Corrected the validation assertion to compare dependency names case-insensitively. No package metadata or dependency was changed. | `validation/intermediate/unit5_metadata_assertion_failure.txt`; `validation/unit5_build_and_isolated_install.txt`. |
| U5-D04 | `git diff --check` treated preserved CRLF-delimited CSV/TSV audit evidence as newly introduced trailing whitespace. Rewriting those files would alter historical byte evidence. | Added `.gitattributes` marking the supplied audit-evidence subtree binary and immutable for Git diff/normalisation purposes. The evidence bytes were not changed. | `.gitattributes`; `validation/unit5_git_precloseout.txt`. |

The final proof population still contains all eight admitted architecture/bootstrap test files, including positive, negative and false-positive fixtures. No test was skipped, xfailed, redirected, renamed or removed to obtain green output.
