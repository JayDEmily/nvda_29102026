# VI-12R U04 Receipt Evidence and Append-Only Assessment Evidence

## Binding and promotion prerequisite

- Received Reviewer-030 PASS/U04 handoff SHA-256:
  `3ee46b932bb45528eb1732abd97914534399e0fedc5f1ed211cee62b735d6d50`.
- Accepted U03 candidate: `45ca4b8dcca6fdb5001e1754fd81bdba37ce05bf`.
- U03 static/runtime authority clarification: `c4caa78a2d13c5dc115c83fedcdf44648efe6d78`.
- Reviewer-030 PASS: `dc40971d24ee773ee133d07622f92d709a7cec11`.
- Forward `main` after lawful fast-forward promotion: `63bbeee9cec14f38ed6da6260095ccf0d8e8e6ec` /
  tree `ecf42b1a7fc0d9d1e55444844142149612caeba2`.
- All three required U03 identities above were rechecked as ancestors of promoted `main` before U04
  work began.
- U04 branch: `work/vi12r-u04-receipt-assessment`, created from promoted `main`.
- Frozen U04 candidate: `e7eb44119bdf7fb22abacae8291788619792c96a` / tree `ea104900fcaf8e2db4177df3909956f464d6a918`.
- Candidate changed exactly `src/nvda_desk/raw_signal_occurrence_truth/api.py`.
- Candidate diff SHA-256: `6f0bb829cc752636958293068e2e0a4bbf4309ea7295b896edb98db255497e33`.

## Implemented U04 boundary

The M00 owner now derives `CaptureReceiptEvidenceRelationV1` only from an admitted observation, a
realised capture and that capture's exact stored effective scope policy. The receipt must lie inside
the capture half-open `[start,end)` interval and the injected eligibility authority must return exact
`bool` eligibility for the exact stored observation/policy pair. Lawful ineligible/out-of-slot cases
return no relation. A created relation has role exactly `evidences_receipt_presence_only` and is
stored capture-locally; no membership, count, validity, completeness, ownership or finality meaning
is added.

M00 now derives and appends `CaptureReceiptPresenceAssessmentV1` through the public owner command.
The caller cannot supply the outcome. For an already realised capture, eligible receipt evidence
visible at `evidence_as_of_ts_utc` yields `one_or_more_received`; otherwise the U04 live path yields
`zero_received`. The contract retains all three authorised discriminants, including
`unknown_not_established`; runtime restart creation of unknown remains U05 as already declared by
the accepted proof. Assessment records are append-only: the first has no predecessor; each later
record must supersede the exact immediate predecessor. Same-ID identical retry is idempotent and
changed content conflicts. Later eligible evidence can therefore append one-or-more over a prior
zero without overwriting that prior fact.

An optional injected technical assessment-persistence port receives only the already-decided frozen
assessment value. It is not given relation or outcome decision authority. No PostgreSQL layout,
restart/reconciliation behaviour, provider mapping rule, exact count or final-assessment concept was
implemented. U05 and later remain unimplemented/prohibited in this cycle.

## Frozen-candidate validation

Pinned tooling restored from preserved project wheel evidence:

- Python 3.13.5;
- pytest 9.0.3;
- mypy 1.20.1 (compiled);
- Ruff 0.15.11.

On exact candidate `e7eb44119bdf7fb22abacae8291788619792c96a` / tree `ea104900fcaf8e2db4177df3909956f464d6a918`:

- U04 bounded product proof: **29/29 passed**;
- U01+U02+U03+U04: **413/413 passed**;
- `python -m mypy src`: success across 15 source files;
- strict `--disallow-any-expr` mypy on modified `api.py`: success;
- Ruff `src tests tools`: pass;
- product-proof control: PASS, six families / 13 of 13 obligations;
- structural architecture validation: PASS, zero dependency/public-seam violations;
- dependency checker: PASS;
- public-seam checker: PASS;
- architecture/bootstrap: **74/74 passed**;
- `architecture_kernel` promotion set: **74/74 passed**;
- committed diff check: pass;
- `git fsck --full --strict`: exit 0 with five dangling-blob diagnostics;
- candidate worktree after validation: clean.

A development-only promotion-gate attempt before candidate commit was rejected solely because the
worktree was dirty, as designed. The committed clean candidate then passed the same architecture
promotion set 74/74.

Fresh independent Reviewer 031 remains required. These Worker results do not constitute U04
acceptance or promotion, and U05 remains prohibited.
