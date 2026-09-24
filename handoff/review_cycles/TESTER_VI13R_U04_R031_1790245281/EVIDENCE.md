# Tester evidence

**Status:** `COMPLETE`

## Binding

- role: fresh independent Reviewer 031 / TESTER
- authorised scope: IWO-U04 receipt evidence and append-only assessment state only
- received source TAR SHA-256: `5263abf8b66351ae0bc4aa52c79c09b070ac2248a286f1715c5b37e801c3e785`
- received filename: `NVDA_G03_WORKER_VI12R_U04_R031_HANDOFF_FULL_GIT_20260924.tar(1).gz`
- transported repository HEAD before review: `4b724b3d1fb84e8129f03246d4a6653049abaf24`
- exact U04 candidate: `e7eb44119bdf7fb22abacae8291788619792c96a`
- candidate tree: `ea104900fcaf8e2db4177df3909956f464d6a918`
- promoted U03 parent/main: `63bbeee9cec14f38ed6da6260095ccf0d8e8e6ec`
- candidate-to-transport changes under `src/**`, `tests/**`, `config/**`, `tools/**`, `pyproject.toml`: none
- candidate production diff: exactly one path, `src/nvda_desk/raw_signal_occurrence_truth/api.py`

## Governing material inspected

Read before disposition: root `README.md`, `GUARDRAILS.md`, root `AGENTS.md`,
`tests/AGENTS.override.md`, complete current `EXEC_PLAN.md`, `CURRENT_STATE.md`, active Reviewer-031
request, IRB BC-007/008/009/010, IWO-U04, admitted U04 product-proof family and physical U04 proof,
Worker U04 response/evidence/commands, exact candidate implementation/diff, and the U03 Reviewer-030
lineage needed to confirm lawful promotion before U04.

The U04 proof family expressly records `relation materialisation is not required` as an adjacent
nonclaim while requiring `zero_received` / `one_or_more_received` to discriminate eligible committed
receipt evidence visible at `evidence_as_of_ts_utc`.

## Independent exact-candidate execution

Environment preflight:

- Python 3.13.5 available;
- pytest 9.0.2 available;
- `python -m mypy` unavailable (`No module named mypy`);
- `python -m ruff` unavailable (`No module named ruff`).

Exact detached candidate results:

- U04 bounded proof: **29/29 passed**;
- U01+U02+U03+U04 excluding exactly the three test bodies whose execution requires the unavailable
  mypy module: **410 passed / 3 deselected**;
- full U01-U04 invocation without deselection: **410 passed / 3 failed**, with all three failures
  attributable solely to `No module named mypy`;
- product-proof control validator: **PASS**, six families / 13 of 13 obligations;
- structural architecture validator: **PASS**;
- dependency checker: **PASS**;
- public-seam checker: **PASS**;
- architecture/bootstrap direct run: **72 passed / 2 failed**, both failures attributable solely to
  the unavailable mypy module;
- candidate diff check: **PASS**;
- `git fsck --full --strict`: exit 0 with five unreachable dangling-blob diagnostics already present
  in the supplied repository.

Worker-preserved pinned mypy/Ruff and 413/413/74/74 evidence is retained as Worker evidence and is
not represented as independently rerun by Reviewer 031.

## R031-U04-F001 — material escape

### Authority defeated

- IRB BC-007: receipt-evidence relation materialisation is optional.
- IRB BC-008 / IA17-PROD-007: assessment outcome represents eligible committed raw-observation
  evidence visible to the assessment own transaction at UTC system-knowledge
  `evidence_as_of_ts_utc`.
- IRB BC-009: missing required authority must not be silently replaced by fabricated semantic truth.
- U04 admitted proof family: `relation materialisation is not required`.

### Candidate mechanism

`append_assessment` determines `one_or_more_received` only by scanning
`state.relations_by_capture`; no admitted observations are considered and no eligibility decision is
performed unless the optional relation command was invoked earlier. It additionally filters those
stored relations by `relation.received_ts_utc <= evidence_as_of_ts_utc`, using receipt time rather
than a knowledge/commit-visibility discriminator.

### Public-seam canary A — optional relation omitted

Setup on the exact candidate:

1. construct owner with an eligibility authority that returns exact `True`;
2. register the effective policy and realise the capture;
3. admit an in-slot observation;
4. deliberately do **not** invoke `derive_capture_receipt_evidence_relation`;
5. append the assessment at an as-of after the observation receipt.

Observed:

- eligibility-authority calls: **0**;
- assessment outcome: **`zero_received`**.

The assertion requiring eligibility evaluation failed with
`AssertionError: eligibility was never evaluated: 0`.

### Public-seam canary B — missing eligibility authority masked as zero

With the same in-slot admitted observation but no eligibility authority injected, assessment append
returns **`zero_received`**. The candidate therefore converts an unresolved eligibility question into
zero instead of failing closed when such evidence requires eligibility adjudication.

### Knowledge-time evidence

The candidate source directly uses
`relation.received_ts_utc <= evidence_as_of_ts_utc` to decide relation visibility. `received_ts_utc`
is the observation receipt-time fact; BC-008 defines `evidence_as_of_ts_utc` as system-knowledge time
representing committed evidence visible to the assessment's own transaction. Receipt time alone does
not establish transaction visibility/commit time and cannot make optional relation materialisation a
semantic prerequisite.

## Recurrence classification

`ISOLATED`.

This is the first post-implementation Reviewer failure in U04. The relevant U04 lineage contains the
initial Worker candidate but no earlier U04 Reviewer-failure / Worker-repair pair. The finding is
therefore routed as one bounded mechanism-level repair rather than being labelled recurrent.

## Disposition

**FAIL / RETURN_TO_WORKER.**

U04 cannot be promoted. U05 remains prohibited.
