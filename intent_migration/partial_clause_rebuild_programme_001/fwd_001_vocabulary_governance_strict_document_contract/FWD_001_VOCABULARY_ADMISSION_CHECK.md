# FWD-001 vocabulary admission check

Clause: `MBC-0310` / `atlas_donor_vocabulary_005`.

Durable-term outcome: `enrich_existing`.

No new canonical vocabulary term was introduced. The implementation reuses the governed vocabulary-document / JSON-helper contract surface and tightens the existing top-level document parser boundary. The test fixture field `shadow_field` is a local rejection specimen, not a durable repo term or canonical vocabulary candidate.

Canonical vocabulary data was not hand-edited. `data/vocabulary/vocabulary_touch_stamp.json` and `var/vocabulary/synonym_candidates.json` were refreshed through `scripts/vocabulary_synonym_audit.py` after the governed source fingerprint changed.
