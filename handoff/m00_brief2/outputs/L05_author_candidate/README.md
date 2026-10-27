# M00 Brief 2 — L05 provisional actual-output dataset

**Author-produced, unreviewed, and unpinned-runtime only.** Do not treat this directory as an accepted `ACTUAL_M00_OUTPUT_VERIFIED` package. Synthetic source only; never live IBKR.

`actual_m00_output_v1.jsonl`: 36 real SQLite-public-read observations, 155 projections, five separately discovered control records, each validated against `handoff/m00_brief2/output_schema_v1.json` and exactly compared (by typed canonical JSON) with immutable `fixtures/{A,B,C}/expected_m00_output_v1.jsonl` and `fixtures/controls/expected_control_output_v1.jsonl`.

`actual_control_output_v1.jsonl` holds the five independently selected control records; `actual_absence_outcomes_v1.json` holds four real public absence probes; `negative_outcomes_v1.json` refers to 18 previously independently accepted negative proofs but **does not** assert a new replay. `readback_requests_v1.json` lists the exact public selectors used; `manifest_v1.json` records hashes, version, source, counts, environment and disposition. See `../evidence/L05/AUTHOR_REPORT.md` and `REPRODUCIBILITY.json` for the separate clean-checkout reproduction.

## Reproduce with the required environment

From the checkpoint's restored Git repository at candidate exporter SHA, with the exact pinned Python 3.12.14/toolchain available, use a new empty parent directory or existing parent with **absent** output paths:

```sh
PYTHONPATH=src:tools python tools/export_m00_synthetic.py \
  --fixtures handoff/m00_brief2/fixtures \
  --expected handoff/m00_brief2/fixtures \
  --database /absolute/existing-parent/new_m00.sqlite \
  --output /absolute/existing-parent/new_output_directory
```

The command refuses overwrites and returns nonzero if any public-output mismatch or if Python 3.12.14 is not running. Formal independent review is still required after a compliant runtime execution. Do not edit immutable inputs or oracle files to obtain equality.
