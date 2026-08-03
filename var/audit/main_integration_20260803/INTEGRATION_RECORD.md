# Main Integration Record — 2026-08-03

## Authority

Direct user instruction to place the accepted vocabulary-governance and root-control work on `main`, validate the resulting checkpoint, confirm clean state, and produce a full-history handoff archive.

## Baseline and integration

- Accepted `main` baseline: `98c462a4f8fb258b79429ec083565d6f2e2fffd9`.
- Vocabulary-governance commit: `3a8e861bf75455a650dd0049c9cc5b52e75cbe36`.
- Root-control/normative-routing commit: `9e1d22b627f7b94873d514616b4fce2d727ce9de`.
- Integration method: clean `--ff-only` advancement of local `main` from `98c462a` to `9e1d22b`, followed by one bounded live-roadmap checkpoint update on `main`.

## Pre-integration drift disposition

Before integration, the working tree contained one uncommitted line change in `ROADMAP_LEDGER.md`. It replaced the accepted ExecPlan-oriented index rule with wording copied from the incoming root-control tarball. The change was not part of commit `9e1d22b`, weakened the agreed routing rule, and was discarded before integration. The exact diff is retained in `evidence/ROADMAP_LEDGER_PREINTEGRATION_DRIFT.diff.gz`.

## Normative read set

The complete read set and pre-mutation hashes are recorded in `FULL_READ_MANIFEST.tsv`.

## Validation

Results are recorded after execution in `VALIDATION_SUMMARY.md` and the `evidence/` logs.
