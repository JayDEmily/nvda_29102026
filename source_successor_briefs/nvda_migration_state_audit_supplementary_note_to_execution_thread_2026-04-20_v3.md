# Supplementary note to execution thread — mandatory offline-venv verification

Your returned repo is **not yet sign-offable**.

Reason:
You claimed the proof floor was:
- `PYTHONPATH=src pytest -q tests/tier_a tests/tier_b` -> `76 passed`
- `python3 -m compileall src tests/tier_a tests/tier_b` -> clean

But the delivered artefact must be verifiable in the project-supplied offline environment path, and it is not yet grounded that way.

## Direct instruction

Use **all three** of the following project-folder artefacts exactly:

1. `NVDA_two_zip_offline_venv_method_2026-04-17.md`
2. `nvda_offline_runtime_bundle_clean_2026-04-17.zip`
3. `nvda_offline_dev_supplement_clean_2026-04-17.zip`

Do **not** substitute a different environment.
Do **not** rely on a pre-existing local environment.
Do **not** claim the proof floor unless it is rerun successfully through that supplied offline method.

## Required task

1. Follow `NVDA_two_zip_offline_venv_method_2026-04-17.md` exactly.
2. Build the repo’s `.venv` using the two supplied offline zip bundles.
3. Prove that the runtime install step completes successfully.
4. Prove that the dev-supplement step completes successfully.
5. Only then rerun:
   - `PYTHONPATH=src pytest -q tests/tier_a tests/tier_b`
   - `python3 -m compileall src tests/tier_a tests/tier_b`
6. Return:
   - the updated repo zip
   - the exact install output for the offline `.venv` build
   - the exact proof outputs

## What must be fixed if the offline install fails

The current failure is packaging metadata / installability related.

You must reconcile the repo so that the supplied offline method can install it cleanly in `.venv`.

Until that is true, the claimed proof floor is not trustworthy enough for sign-off.

## Definition of done

Do not say the brief is satisfied until:
- the repo installs successfully via the supplied offline `.venv` method
- the two supplied zip bundles were actually used
- the proof floor is rerun successfully in that environment
- the updated repo zip is returned
