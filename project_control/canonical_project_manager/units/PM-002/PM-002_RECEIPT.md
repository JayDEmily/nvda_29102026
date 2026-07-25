# PM-002 Vocabulary Normative Truth Repair Receipt

`unit_result: pass`

## Control

- Branch: `work/NVIDIA_2026_pm001_pm010_restart_20260721`
- HEAD: `21c1e5eccfbb818bdd422afd42117f23b1f74f26`
- Prerequisite: PM-001 receipt records `unit_result: pass`
- Durable-term decisions made: none
- Gate D: closed

## Repairs

Nine rows in `VOCABULARY_NORMATIVE_TRUTH_REPAIR_REGISTER.tsv` map every bounded edit to a PM-001-exposed stale fact or authority-direction ambiguity.

Changed governed files:

- `docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md`
- `docs/vocabulary/README.md`
- `docs/vocabulary/CONSOLIDATION_WORKFLOW.md`

The repairs:

1. replace stale 42/87/16/61 wording with the reproduced 46/87/26/20/61 census;
2. keep builder/JSON equality as projection truth without moving semantic authority downstream;
3. remove the stale four-candidate/final-disposition claim;
4. make the README and workflow human-semantic-first;
5. label classifiers, audits, stamps, generated artefacts and tests as projection/evidence surfaces only.

## Current read-only audit reproduction

- Tracked report/stamp fingerprint: `4d2ba332cf6e4c009c1b14ac76b3d506b8704fe692a3457cfd098c0e653b3700` / `4d2ba332cf6e4c009c1b14ac76b3d506b8704fe692a3457cfd098c0e653b3700`.
- Tracked report: `vocabulary_touched=false`, candidate occurrences=0.
- Current in-memory `build_report()` fingerprint: `19d0676931935ed204b2ddf59d22d49d08b0d48f9e238d10d1d7c1e118307640`.
- Current in-memory state: `vocabulary_touched=true`, candidate occurrences=5, classifications=5.
- Exact occurrence inventory: `{'or coefficient authority': 1, 'ecursor runtime context': 1, 'market context': 1, 'compile playbook eligibility': 1, 'source temporal standard requires': 1}`.
- Every candidate has `resolution_required=llm_escalation`; the attached mechanical classification/review route is quarantine/quarantined. Those fields are not final semantic dispositions.
- No audit report or touch stamp was written.

## Preservation proofs

- `docs/vocabulary/vocabulary_registry.md` hash unchanged from PM-002 start.
- `data/vocabulary/canonical_vocabulary.json` hash unchanged from PM-002 start.
- Sections 10.7 and 10.8 explicit admission lines, actions and definitions are byte-identical to `HEAD`.
- No test, source, configuration, Atlas, generated data, tracked audit or stamp file changed.
- The only governed edits are the three authorised documentation paths.

## Validation meaning

Existing tests were not used to validate normative meaning and were not required for PM-002 pass. Validation is structural, hash-based and proposition-mapped. Full command output is recorded in `VALIDATION_OUTPUT.txt`.

## Files created

- `PM-002_FULL_READ_MANIFEST.tsv`
- `VOCABULARY_NORMATIVE_TRUTH_REPAIR_REGISTER.tsv`
- `PM-002_RECEIPT.md`
- `VALIDATION_OUTPUT.txt`
