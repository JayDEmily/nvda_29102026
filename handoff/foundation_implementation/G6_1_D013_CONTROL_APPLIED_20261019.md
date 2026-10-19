# D013 exact control application — bounded proved checkpoint

19 October 2026, 23:43 Melbourne.

Actual applied candidate `471c2f79d6b2e16912aa79b6a5febd5a7bb3738a`, branch `work/v2-g53-review-20261019`. Concrete pre-application disposition at `0ab89b6` followed actual independent V2 review; see `G6_1_D013_CONTROL_DISPOSITION_20261019.md`. Exact applied loader SHA256 `4720fb69f9d6b34032742ce47585b57f1be3610305061faf2ac9d1458c66c478` matches the independently reviewed V2 body. The exact fixed D013 descriptor and null pointer are installed; no physical domain proof, generation or runtime D013 implementation exists.

All commands below use `/workspace/scratch/d549b6d808a9/g52-dev/bin/python` in the actual repository. Complete outputs are preserved in `d013_control_applied_20261019/`. Every command returned the stated process result; strict original aggregates ran against clean applied candidate and retained their governed bytes.

| Command | Observed result |
| --- | --- |
| `-m pytest tests/architecture/test_proof_control.py` | 92 PASS, exit0, 108.03s. Includes direct synthetic strict D013 success0/skip1/mutation6, absent/malformed authority/ownership and lawful all-three-claim transition witnesses. These are control canaries, not arithmetic proof. |
| `-m mypy src tools/product_proof_claims.py tools/product_proof_outcomes.py tools/validate_product_proof.py tools/run_product_proof_gate.py` | PASS34 source files; inherited untyped M01-body notes disclosed in output. |
| `-m ruff check tools/product_proof_claims.py tests/architecture/test_proof_control.py` | PASS. No standard full-tree lint success inferred; two inherited M01 E501 findings remain untouched. |
| `tools/validate_implementation_authority.py --binding implementation/authority/G6_1_D013_IMPLEMENTATION_AUTHORITY_BINDING.yaml --brief handoff/foundation_implementation/authority/G6_1_D013_IMPLEMENTATION_BRIEF_PROPOSED.md` | PASS exact brief1f53d9c2…; modify:M02 then modify:G01. |
| `tools/run_product_proof_gate.py --aggregate neutral_market_measurement_truth_d012` | 80 PASS/strict0/process0; generation26d2b4e371c38b0960cb6081798cc618c9f308567d0df12b2aa40f3777dd2a25. |
| `tools/run_product_proof_gate.py --aggregate neutral_market_measurement_truth_pilot` | 113 PASS/strict0/process0; generation24a5af4054c277b01a140ec43481e86851e5e76263826644a80993c12c2495b7. |
| `tools/run_product_proof_gate.py --aggregate raw_signal_occurrence_truth_sqlite` | 30 PASS/strict0/process0; generation51e87129c2a31c71599b7a01beb8ba39717ed5118a4d5c849bcb2015b6c80c6f. |
| `tools/run_product_proof_gate.py --aggregate neutral_market_measurement_truth_d013` | INCOMPLETE_NO_PHYSICAL_FAMILIES/process4; truthful missing physical proof, neither intended domain RED nor GREEN. |

Actual `git diff 5f998db -- src config/product_proof/claims.json implementation/authority/FOUNDATION_IMPLEMENTATION_AUTHORITY_BINDING.yaml config/product_proof/market_measurement/generations config/product_proof/raw_signal_sqlite/generations config/product_proof/market_measurement_d012/generations` is empty. Original product code, catalogue, binding and generations are unchanged. Independent revised review separately exercised actual-state copies retaining real Git history and is not reattributed as author testing.

DELEGATED DISPOSITION: ACCEPT_BOUNDED_D013_CONTROL_ONLY under actual owner-chat/20261019T222804/D012-and-standing-human-exceptions, based on the exact review/application/checks above. Root§7.2.1 is satisfied for this unit. It permits next §7.2.2 physical source authoring, independent adequacy review, immutable admission and actual intended RED before new domain behaviour. It is not D013 domain acceptance, full G6.1, native input certification, all126 or G6.2–6.4 completion. No provider acquisition/live/composition/populated-state migration/retirement/main work is authorised. Archive packaging and later evidence-only commits do not add domain capability.

TS: 19-10-26 23:43
