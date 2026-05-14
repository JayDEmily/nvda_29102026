# Gate 1 — Authority and oracle extraction: proof_executor_contract

Status: `PASS_FOR_SELECTED_FAMILY`

Selected family: `proof_executor_contract`
Native test path: `tests/tier_b/proof_model/test_proof_executor_contract.py`
Proof block: `proof_executor_contract`
Tier: `Tier B`
Architecture row: primary `5.17 Testing, proof, and checkpoint surfaces`

## Authority read set

Full-read / direct-read for this selected family:

- `AGENTS.md` lines 1-272.
- `PLANS.md` lines 1-538.
- `ROADMAP_LEDGER.md` lines 1-328.
- `tests/AGENTS.override.md` lines 1-76.
- `tests/README.md` lines 1-11.
- `tests/tier_b/README.md` lines 1-7.
- `docs/08_TESTING_AND_PROMOTION_CORE.md` lines 1-202.
- `docs/08.1_TESTING_AND_PROMOTION_WORKING.md` lines 1-13.
- `docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md` lines 1-50.
- `docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md` lines 1-33.
- `config/proof_blocks.yaml` lines 1-310.
- `tests/tier_b/proof_model/test_proof_executor_contract.py` lines 1-286 before amendment.
- `scripts/run_proof_block.py` lines 1-217.
- `Makefile` lines 1-346.
- `project_control/remote_bridge/REMOTE_BRIDGE_BLUEPRINT.md` lines 140-185, 268-286, 302-324.
- `config/retained_test_registry.yaml` selected entry lines 1978-1996.

`config/retained_test_registry.yaml` was not read in full in this pass. It was searched and the selected `proof_executor_contract` entry was read at lines 1978-1996. Any conclusions about other registry entries are `Unknown`.

## Authority basis

| Authority | Evidence |
|---|---|
| Test work must target truthful protection of real invariants, not greenness | `tests/AGENTS.override.md:5-9` |
| Native test authority is not physical location alone | `tests/README.md:3-7`; `tests/tier_b/README.md:1-7` |
| Proof artefact tier requires explicit live doctrine / active pack | `docs/08_TESTING_AND_PROMOTION_CORE.md:29-39` |
| Proof receipt / control-surface truth must be recorded if proof-backed truth changes | `docs/08_TESTING_AND_PROMOTION_CORE.md:151-169` |
| Manifest-driven proof block execution uses `config/proof_blocks.yaml` and `scripts/run_proof_block.py` | `project_control/remote_bridge/REMOTE_BRIDGE_BLUEPRINT.md:149-171`, `271-284` |
| `proof_executor_contract` is retained Tier B and owns runner/manifest/Makefile surfaces | `config/retained_test_registry.yaml:1978-1996`; `config/proof_blocks.yaml:52-63` |
| The proof-block pass proves only the named block, not the full repository | `project_control/remote_bridge/REMOTE_BRIDGE_BLUEPRINT.md:282-284` |

## Independent oracle

The independent oracle is not current runtime output. It is the manifest-driven proof-block contract:

1. only named manifest blocks may be described, checked, or run;
2. `proof_blocks` must be a list of mappings;
3. every proof block must have a non-empty `proof_block_id`;
4. every proof block must have a non-empty command;
5. duplicate `proof_block_id` values are invalid;
6. every owned path must exist before a block is run;
7. command tokenisation must not use shell evaluation;
8. a proof-block pass proves only the named block.

## Protected invariant

`proof_executor_contract` protects the manifest-driven proof-block executor as a bounded proof gate. It must resolve a named block from `config/proof_blocks.yaml`, validate the manifest block, validate owned paths, execute the declared command without shell evaluation, and report only the bounded block result.

## Forbidden behaviour

- accepting an unknown proof block;
- accepting non-mapping entries in `proof_blocks`;
- accepting duplicate `proof_block_id` values;
- accepting missing owned paths;
- running a block command before owned-path validation;
- executing manifest command text through a shell;
- treating a named proof-block pass as full-repository proof.

## Observable signals

- CLI non-zero exit with `SystemExit` stderr for invalid manifest/block conditions;
- absence of side-effect file when shell metacharacters appear in a manifest command;
- pytest failure if validation is disabled or command execution changes to `shell=True`;
- unchanged proof-block tier (`Tier B`) and no promotion claim.

## Known-good case

A manifest with one named block, one existing owned path, and a non-shell Python command is accepted and runs with exit status 0.

## Known-bad cases

- unknown block id;
- missing owned path;
- duplicate block ids;
- non-mapping proof-block entry;
- command containing `; touch shell_injection_marker.txt`, where the marker must not be created.
