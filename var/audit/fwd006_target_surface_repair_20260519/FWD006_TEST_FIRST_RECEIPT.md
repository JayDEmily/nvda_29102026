# FWD-006 test-first receipt

New test surface: `tests/tier_a/temporal/test_fwd006_reopened_row_raw_capture_source_temporal_proof.py`.

The test parametrises exactly 108 reopened FWD-006 audit rows and asserts real native raw capture/source temporal behaviours, not registry or row-id presence.

Behaviour clusters: raw bundle provenance preservation; replay date-level source truth; temporal event window/source standard; upstream trace-only non-interference; transform boundary/no donor runtime.

Proof: `env PYTHONPATH=src python3 -m pytest tests/tier_a/temporal/test_fwd006_reopened_row_raw_capture_source_temporal_proof.py` -> `108 passed`.
