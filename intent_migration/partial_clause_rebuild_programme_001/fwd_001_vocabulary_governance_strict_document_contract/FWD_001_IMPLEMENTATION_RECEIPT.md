# FWD-001 implementation receipt — Vocabulary governance strict document contract

Status: `bounded_closed_current`

Clause closed: `MBC-0310` / `atlas_donor_vocabulary_005`

Final clause state: `native_delta_required` implemented for the missing delta only.

## Behaviour added

`VocabularyDocument.from_json_text()` delegates through `vocabulary_document_from_dict()`. The dict parser now rejects unknown top-level vocabulary document fields before constructing the document. This preserves existing schema/version/notes/entries handling and adds only the strict-extra-field contract that was missing.

## Duplication guard

The existing vocabulary schema and JSON helper surface were preserved. No parallel vocabulary document model, new schema family, or donor-code transplant was added.

## Files changed

- `tests/tier_a/vocabulary/test_vocabulary_json_helper_contracts.py` — added strict unknown top-level field rejection test.
- `src/nvda_desk/schemas/vocabulary.py` — added allow-list check for top-level vocabulary document keys.
- `scripts/vocabulary_candidate_review.py` — bounded blocker repair so the proof-owned CLI can import `src` when invoked as a script from subprocess tests.
- `data/vocabulary/vocabulary_touch_stamp.json` and `var/vocabulary/synonym_candidates.json` — refreshed via governed synonym audit after the governed source fingerprint changed.

## Proofs

### Targeted JSON helper proof

```text
.........                                                                [100%]
9 passed in 0.25s
```

### Vocabulary governance conformance proof

```text
........................................................................ [ 79%]
...................                                                      [100%]
91 passed in 23.22s
```

### Synonym audit clean check

```text
vocabulary_synonym_audit=PASS candidates=0 vocabulary_touched=False
```

### Candidate review clean check

```text
{
  "schema_version": "v1",
  "trigger": "vocabulary_candidate_review_summary",
  "vocabulary_path": "data/vocabulary/canonical_vocabulary.json",
  "candidates_path": "tests/fixtures/vocabulary_candidate_review/clean_candidates.json",
  "summary": {
    "statuses": {
      "admissible": 1,
      "quarantined": 0,
      "invalid": 0
    },
    "actions": {
      "enrich_existing": 1,
      "add_new": 0,
      "alias_only": 0,
      "quarantine": 0
    }
  },
  "blocked_candidates": []
}
vocabulary_candidate_review=PASS blocked_candidates=0
```

## Next lawful owner-service leaf

`FWD-002 — Testing, proof, and checkpoint surfaces` remains next in the temporary override queue. No FWD-002 implementation was opened in this receipt.
