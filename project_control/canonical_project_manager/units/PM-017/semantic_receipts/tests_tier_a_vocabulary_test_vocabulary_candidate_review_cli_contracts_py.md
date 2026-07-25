# Semantic receipt — `tests/tier_a/vocabulary/test_vocabulary_candidate_review_cli_contracts.py`

- Sequence `158`, PM-017; SHA-256 `f780d2fc5b8a8229682cbd8d06d08b70caf006d8319b45a3afa3ba4646b88357`.
- Read full test `1-463`, full CLI implementation and workflow admissions `ATLAS_FEATURE_ADMISSION_015`, `018`, `019`, `020`, `021` and `024`. Targeted run: `16 passed` inside `63 passed, 3 failed in 5.75s`.

## G1 — ordered list input produces status-bearing report
- Locator `44-67` requires trigger, status counts and source order.
- Relation `bounded_separable_clause`; strength `behavioural`.
## G2 — object-with-candidates input is accepted
- Locator `70-83` requires one admissible review from the wrapped shape.
- Relation `bounded_separable_clause`; strength `behavioural`.
## G3 — optional output file is written
- Locator `86-101` requires zero status and JSON output.
- Relation `bounded_separable_clause`; strength `behavioural`.
## G4 — review run does not mutate vocabulary input
- Locator `104-134` compares exact before/after text while producing report and PASS receipt.
- Relation `bounded_separable_clause`; strength `boundary`.
## G5 — default CLI stdout is JSON
- Locator `137-157` requires parseable stdout and alias-only count.
- Relation `bounded_separable_clause`; strength `behavioural`.
## G6 — non-object candidate entries fail
- Locator `160-178` requires non-zero process status and explicit shape error.
- Relation `bounded_separable_clause`; strength `boundary`.
## G7 — check-clean blocks quarantined candidates
- Locator `181-208` requires exit code one and blocked count.
- Relation `bounded_separable_clause`; strength `boundary`.
## G8 — check-clean passes admissible candidates
- Locator `211-233` requires zero exit and PASS count.
- Relation `bounded_separable_clause`; strength `boundary`.
## G9 — report exposes quarantined and invalid rows
- Locator `236-252` requires both blocked statuses in order.
- Relation `bounded_separable_clause`; strength `behavioural`.
## G10 — summary-only hides full reviews but not blocked candidates
- Locator `255-289` requires summary trigger/counts, no reviews, and retained blocked slug.
- Relation `bounded_separable_clause`; strength `boundary`.
## G11 — PASS receipt is emitted
- Locator `292-317` requires trigger/status/exit and empty blocked list.
- Relation `bounded_separable_clause`; strength `behavioural`.
## G12 — BLOCKED receipt is emitted
- Locator `320-346` requires blocked status/exit and candidate row.
- Relation `bounded_separable_clause`; strength `behavioural`.
## G13 — invalid input shape emits ERROR receipt
- Locator `349-375` requires non-zero command, error status/code and retained diagnostic.
- Relation `bounded_separable_clause`; strength `boundary`.
## G14 — stdin candidate input is accepted
- Locator `378-399` requires `-` source identity and alias-only summary.
- Relation `bounded_separable_clause`; strength `behavioural`.
## G15 — stdin receipt records stdin source
- Locator `402-430` requires PASS and `candidates_path == '-'`.
- Relation `bounded_separable_clause`; strength `identity_lineage`.
## G16 — invalid alias shape blocks check-clean
- Locator `433-463` requires exit one and blocked count.
- Relation `bounded_separable_clause`; strength `boundary`.

## File decision

- Groups/relationships `16/16`; final `ADMIT_TIER_A_CURRENT` under the named workflow admissions.
- CLI output and receipts are review/evidence metadata only; they do not admit terms, suppress candidates or bypass human registry/builder governance.
- No source, test, configuration, normative document, registry or proof-block mutation was executed.
