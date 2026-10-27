# M00 Brief2 portable output replay

Use the checkpoint's exact pinned CPython3.12.14 environment and committed clean checkout. Dependencies are available in vendor/wheels under the hash-locked requirements in handoff/foundation_implementation/environment/. Install the project editable offline/no-deps when running the historical subprocess proofs. No PostgreSQL server or IBKR session is required.

Run from repository root, substituting absent absolute database and new output paths outside the source tree:

```sh
PYTHONPATH=tools:src python tools/export_m00_synthetic.py --fixtures handoff/m00_brief2/fixtures --expected handoff/m00_brief2/fixtures --database /absolute/work/replay.db --output /absolute/work/output
```

The family/controls/negative directories are immutable signed inputs. The independent expected rows are read only for validation. Actual rows come from public M00 commands, SQLite, public known-ID/raw-projection/history reads and fresh-process read-only transactions. Controls are independently enumerated by subject/source/request/generation/cutoff. Per-R request/generation selection remains consumer checks on returned identity, as documented by the accepted mapping contract.

`actual_m00_output_v1.jsonl` contains196 rows:36 observations,155 base projections and5 separate controls. `actual_control_output_v1.jsonl` contains the5 control rows. Tagged Decimal values preserve lexical spelling; native integer/bool/datetime types and source-time absence remain distinct. Physical main ordering is family/scenario/kind then R/receipt/scope/sequence/occurrence; observation/control ordering uses their separately defined clock/identity fields.

`negative_outcomes_v1.json` contains18 separately versioned actual negative replays, including fresh typed retained observations, histories, absences and actual rejections. N05 carries UNKNOWN_TIED_RECEIPT_SCOPE_SEQUENCE; deterministic ID order is display order. `actual_absence_outcomes_v1.json` records supplementary public absence checks. These four datasets contain deterministic fixture clocks and identities, with no execution wallclock or database path. The manifest records source/environment/hashes/counts and remains honestly review-pending until the separate independent acceptance record. Any first failed invariant is retained with structured detail, nonzero exit and no dependent verification claim.

The admitted export proof reproduces from a clean clone into a second fresh SQLite file and compares exact hashes for all four deterministic datasets. Acceptance records and reproduction evidence accompany published outputs after independent review. Expected oracle and output_schema_v1.json remain usable separately from live acquisition. SQLite constructor validation still opens mode=rw; ordinary reads use mode=ro/query_only, so no filesystem-permission boundary is claimed. PostgreSQL runtime is deferred; live IBKR/direct-option entitlement is unverified. D145 remains paused.
