# Sequence 7A parallel risk envelope coverage table

| Surface | Sequence 7A disposition | Proof artefact |
|---|---|---|
| Parallel risk input packet alignment | Tests written; runtime not implemented | `test_sequence7_parallel_risk_envelope_input_surface.py` |
| Temporal/calendar contribution | Tests/specimen expect caution contribution | `sequence7_parallel_risk_envelope_expected_packet.json` |
| Options repricing contribution | Tests/specimen expect options repricing contribution | `test_sequence7_parallel_risk_envelope_output_surface.py` |
| Market volatility contribution | Tests/specimen expect VIX/volatility contribution | `test_sequence7_parallel_risk_envelope_output_surface.py` |
| Tight/broad/caution/block semantics | Tests/specimen expect state ladder | `test_sequence7_parallel_risk_envelope_specimen.py` |
| Capital/sizing/brokerage exclusion | Tests assert forbidden tokens absent | input/output test modules |
| Sequence 8 coefficient/modifier authority | Not opened | route proof JSON |
