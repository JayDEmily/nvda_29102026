# Unit 2 — Canonical M01 → M02 → M03 workflow

## Outcome

PASS. One typed M00 upstream operation now delegates exact M01 admission, M02 projection and M03 preparation before the existing prepared-data paper-run command.

## Expected-red proof

`tests/tier_a/m00_application_shell/test_m00_upstream_workflow_contract.py` initially produced 7 failures: the four upstream contracts, M00 preparation method, CLI translation and ASGI route did not exist.

## Implemented controls

- M01 validates JSON-compatible typed payload material through the registered concrete payload model.
- M01 issues explicit repository-owned `source_artifact_id` values through an injected factory; source, capture and content identities remain distinct.
- M00 sequences exact owner services and returns immutable owner-output evidence.
- M01 non-admission and M02 withheld/rejected outcomes are terminal before M03.
- M03 prepared envelopes can carry immutable M02 projection references without altering legacy fingerprints when none exist.
- CLI `prepare` and ASGI `POST /commands/prepare` are translation-only routes.

## Validation

- Unit proof plus M01/M03 regression: 54 passed.
- Affected M01/M02/M03/M00/entry proof: 118 passed.
- Proof-authority and promotion-control fallout: 37 passed.
- `scripts/proof_authority.py --check`: PASS, 197 families / 199 paths / 69 blocks.
- Promotion membership after admission: 16 blocks / 16 families / 18 paths.
- Targeted Black/Ruff/compile and `git diff --check`: PASS.

No M05–M13 owner semantics were changed.
