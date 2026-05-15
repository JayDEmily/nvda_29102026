# Vocabulary Candidate Evidence Hardening Receipt

Status: `bounded_evidence_hardening_recorded`

Scope:

- FWD-016 remains unopened.
- No runtime feature row was opened.
- This pass hardens candidate-level evidence for the pre-FWD-016 vocabulary governance remediation.

Candidate appendix:

- Prior aggregate count recorded: 152.
- Exact original transient 152 candidates fully reconstructed: no.
- Reason: previous remediation artefacts did not commit the pre-adjudication candidate payload; only the aggregate count was recorded.
- Reconstructable phrase decisions recorded: 88.

Disallowed phrase audit:

- Disallowed phrases audited: 58.
- Suspicious disallowed phrases remaining: 0.
- Fragment-like phrases `ithout runtime context`, `pared runtime context`, `stream opening architecture`, and `and close architecture` are explicitly represented in the candidate appendix and disallowed-phrase audit.

Tests:

- Tier A guardrail test added to `tests/tier_a/vocabulary/test_vocabulary_canonical_builder_parity.py`.
- Guardrail proves disallowed phrases are unique, disallowed phrases do not equal canonical labels or allowed aliases, and fragment-like disallowed phrases are represented in the adjudication evidence artefact.

Proof summary:

- See `VOCABULARY_CANDIDATE_EVIDENCE_HARDENING_PROOF_SUMMARY.json`.
- Earlier wrapper captures for `vocabulary_governance_conformance_candidate` timed out/aborted before status write; no pass is claimed for those files. Captured exit-code evidence is `proof_block_vocabulary_governance_conformance_candidate_bg.status = 0`.
