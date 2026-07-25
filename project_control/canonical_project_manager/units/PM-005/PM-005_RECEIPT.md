# PM-005 Calendar, Temporal and Provenance Vocabulary Receipt — Corrected P1 Reopen

`unit_result: pass`

## Control

- Branch: `work/NVIDIA_2026_pm001_pm010_restart_20260721`
- HEAD: `21c1e5eccfbb818bdd422afd42117f23b1f74f26`
- P2 was not opened.
- Tests, code and the former builder remained observation evidence only.

## Corrected outcome

PM-005 now contains 31 decisions: 26 canonical records and five quarantines.

The following fixed-list/former-builder audit labels have no higher normative proposition and are quarantined rather than projected:

- `CTP-024 Temporal Conformance Inventory`;
- `CTP-025 Already Conformant`;
- `CTP-026 Needs Proof/Test Remediation Only`;
- `CTP-027 Needs Code/Persistence Remediation in Tranche 3`;
- `CTP-028 Reserved / Blocked`.

Re-adjudication of repeated governing language identified one omitted normative concept:

- `CTP-031 Financial-calendar Architecture` is admitted as the four-layer architecture and reference/projection path governed by the normative core.
- `financial calendar`, `financial-calendar reference and projection`, and `financial-calendar reference and projection path` are lawful aliases of that umbrella architecture.
- This concept is explicitly distinct from `Financial Calendar Crosswalk`, which remains only a mapping policy.

Thirty-three governing-normative candidate occurrences were adjudicated inside PM-005. Contextual forms such as `source temporal`, `field level`, `market session` and `financial event` are occurrence-governed where they do not name the full canonical concept.

## Evidence

- `CALENDAR_TEMPORAL_PROVENANCE_ADJUDICATION_REGISTER.tsv`: 31 rows.
- `NORMATIVE_CANDIDATE_RE_ADJUDICATION_REGISTER.tsv`: 33 occurrence-level proposition decisions.
- Former-builder evidence is preserved by exact pre-PM-010 SHA-256 and evidence copy.
- Every locator and source revision validates.

Project-manager acceptance remains pending.
