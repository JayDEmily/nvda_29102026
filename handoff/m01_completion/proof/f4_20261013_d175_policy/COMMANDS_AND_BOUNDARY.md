# D175 investigation — commands and boundary

Base HEAD: ff4cbd16d67250755fa1dfd5f2bb91cbd159f75c. Base tree: 0e3ca1a4c52597e5c6ab2f6aed183bfc83ce16b3.

Scope is the 13-10-2026 Programme-Owner Direction: D175 Policy Resolution. Investigation and consolidated recommendation only; new financial mathematics, catalogue edits and Stage 2 are not implemented.

## Reproduction from repository root

```sh
python handoff/m01_completion/proof/f4_20261013_d175_policy/inspect_authority.py
python handoff/m01_completion/proof/f4_20261013_d175_policy/check_proposal_arithmetic.py
../diagnostic_env/bin/python -m pytest -q tests/product/derived_signal/test_m01_f4_cross_stage_rule_algebra_own_kernel.py
git log --all --format='%H %s' -G 'D175|risk_budget|CVaR_currency|stress_loss' -- src/nvda_desk/derived_signal_calculation_truth handoff/m01_completion/authority
git show d881165:src/nvda_desk/derived_signal_calculation_truth/_stage1.py
git show b6a300e -- src/nvda_desk/derived_signal_calculation_truth/_stage1.py
git show d5c39c2 --stat
git diff --cached --check
```

The archive scanner reads only the newly available admission-handover archive's active text members, excluding its Git object database and binary attachments. Exact scope and SHA are in D175_AUTHORITY_TRACE.json. Current-source/context selection functions and accepted measurement rules were read, not inferred from archive filenames or test results.

## Observations

- Static D175 catalogue closure: 95 D identities including D175; 81 raw identities. All closure rows are retained. This is not a semantic audit of all transitive rows.
- 278 admission archive text members scanned; no D175 or active-limit-carrier literal match. No universal historical absence claim.
- Inherited focused file: 10 tests passed under Python 3.12.14, pytest 9.0.3. It does not establish policy correctness or required Python 3.13.5 acceptance.
- Proposal arithmetic: 12 displayed cases/records, including contract-refusal classification, and 648 exact-rational positive-coordinate parameter combinations checked for current breach equivalence. They are not product integration tests, financial validation or programme acceptance.
- Inherited source probes: a structured zero-CVaR input yields budget 0; negative available funds is converted by abs and still yields budget 50; the pure D175 kernel emits 100 with only R205 and no derived inputs. These are read-only diagnostics of current source. The public graph separately refuses missing dependencies.
- Initial diagnostic output included the imported helper's top-level print output. It was regenerated with that print captured so SOURCE_DIAGNOSTIC_PY312.json is one valid JSON object; no product/helper source was edited.

## Explicit non-runs and invariants

No new production policy or kernel exists. The arithmetic script checks draft examples only and is outside production paths. No source, tests, schemas, accepted catalogue, authority index, root governance or package version is changed. The previous evidence-only checkpoint remains an ancestor and all previous artefacts are retained.

No supported-runtime complete regression, PostgreSQL verification, Ruff/Mypy, full public-seam integration or Stage-1 acceptance run is claimed. No Stage-2 implementation is permitted by this pass. Exact proposed policy, contracts, refusal conditions and amendments are in D175_POLICY_RESOLUTION_PROPOSAL.md, not installed as accepted normative authority.
