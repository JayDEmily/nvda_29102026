# Consolidation Workflow

The vocabulary workflow is a **feeder process only**.

## Allowed flow

1. select the admitted vocabulary namespace and harvest candidate evidence only from its registered owning surfaces, exported contracts and direct consumers; use the repository-wide `global` scope only for genuinely shared concepts or final consolidation;
2. read the relevant normative and implementation context in full and compare the candidate with the accepted human-readable registry and any retained admission-lineage redirect;
3. decide exactly one human/LLM semantic action under the law in `docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md`:
   - `enrich_existing`
   - `add_new`
   - `alias_only`
   - `quarantine`
4. record the accepted human-readable meaning, action lineage and projection metadata in the owning registry record when the action changes governed vocabulary; do not duplicate the term definition in `10.1`;
5. project the accepted decision through the builder into `data/vocabulary/canonical_vocabulary.json`;
6. run audits, stamp guards and enforcement tests as downstream evidence.

Mechanical classifiers and candidate-review helpers may propose or route these action labels, but they cannot perform step 3 or create semantic admission. A stable `10.1` redirect may be retained where an admission section already has downstream lineage; new term meaning still lives only in the registry record.

### Deterministic projection record

The accepted human registry is the sole semantic input to the committed machine projection. Every canonical registry record must include one explicit `Projection metadata:` record with traceability to its accepted semantic decision and vocabulary namespace. The registry header declares the admissible namespace scopes and imports. `src/nvda_desk/vocabulary_builder.py` validates and transforms those records only; it must contain no independent term seed, namespace inference or path inference. Generated JSON is updated through `scripts/build_canonical_vocabulary.py` after a validated `/tmp` build and byte-stability check.

An audit phrase that has been read in source context and rejected as a canonical label or lawful alias may be retained in the owning human record as descriptive `audit_noncanonical_phrases` history. That field never suppresses the scanner. Suppression is allowed only from the exact resolved-occurrence evidence register, and only for the same path, line, column, normalised phrase and unchanged source-context hash.

## Guardrails

- never merge a stale harvested payload blindly;
- never let one label point to two different contract surfaces;
- never treat compatibility labels as canonical runtime truth;
- never let a new family, setup variant, execution expression, horizon, or workflow-routing concept become governed language without an accepted human-readable admission and its downstream canonical projection.

## Three-ledger split

The workflow keeps three distinct language ledgers:

1. **formal primitives / contracts**
2. **desk-compression phrases**
3. **repo labels / code slugs**

They may map to each other. They must not silently collapse into each other.


## Gate 55 alignment notes

Gate 55 extends canonical ownership to:

- Step 0 calendar/horizon routing terms;
- candidate family generation terms;
- carry handoff and carry-branch terms;
- generic family / setup-variant / execution-expression governance labels.


## Candidate Audit

- run `candidate_audit` every time the governed vocabulary surfaces change;
- pass the exact admitted namespace; the audit may inspect only its registered paths and imported lexicon;
- write the audit artefact to `var/vocabulary/synonym_candidates.json`;
- escalate any candidate entry in that artefact to an LLM pass;
- do not admit or suppress a candidate by hand-editing the artefact;
- update the vocabulary stamp only after the configured audit returns no unresolved candidate occurrences and all required semantic decisions and projection updates are recorded; a zero-candidate report or advanced stamp is algorithmic/proof evidence only, not a semantic clean certificate.
- resolve a noncanonical candidate only for its exact evidenced occurrence: path, line, column, normalised phrase and unchanged source-line context hash; the same phrase on a new path, at a new occurrence or in changed context must surface again;
- treat only canonical labels and explicitly admitted aliases as phrase-global exact tokens; disallowed phrases and historical noncanonical inventories must not suppress candidates globally.
- reserve a repository-wide cross-namespace scan for a `global` admission or final Gate C consolidation; a module admission must not create disposition work outside its declared scope.


## Schema-helper admission boundary

The vocabulary schema may expose JSON helper methods only as validation and proof helpers. These helpers must preserve the feeder-process boundary:

- `VocabularyDocument.from_json_text` may decode JSON text only into a mapping and must delegate to governed `VocabularyDocument` validation.
- `VocabularyDocument.from_json_path` may only read UTF-8 text from a path and delegate to `from_json_text`.
- `VocabularyDocument.to_json_text` may serialise a validated document for proof or round-trip use, but it does not own regeneration of `data/vocabulary/canonical_vocabulary.json`.
- Schema helpers must not admit terms, suppress synonym candidates, mutate the canonical vocabulary file, or replace the builder/generator parity proof.

## Admitted Atlas feature leaf — JSON helper contracts

`ATLAS_FEATURE_ADMISSION_001` admits the following row `5.18` vocabulary-governance records as schema-helper contracts only:

- `NIS-0108` / `VocabularyDocument.from_json_text`
- `NIS-0109` / `VocabularyDocument.from_json_path`
- `NIS-0110` / `VocabularyDocument.to_json_text`

The admitted helpers are allowed to load, validate, and serialise `VocabularyDocument` instances for proof and round-trip use. They remain subordinate to the builder/generator path for the committed canonical vocabulary artefact and must not admit durable vocabulary terms, suppress synonym candidates, or mutate `data/vocabulary/canonical_vocabulary.json`.

## Admitted Atlas feature leaf — candidate classification contracts

`ATLAS_FEATURE_ADMISSION_002` admits a bounded candidate-classification helper for row `5.18` vocabulary governance. The helper emits exactly one mechanical proposed-action label: `enrich_existing`, `add_new`, `alias_only`, or `quarantine`.

The classifier is a routing helper only. It must not mutate `data/vocabulary/canonical_vocabulary.json`, suppress synonym candidates, make the human/LLM semantic decision, or admit durable terms. Durable vocabulary changes require an accepted semantic decision first, followed by controlled human-registry update, builder projection, parity proof and retained-test execution.

The mechanical proposal boundary is:

- existing canonical slug or label match -> propose `enrich_existing`;
- explicit allowed-alias match -> propose `alias_only`;
- no governed collision -> propose `add_new`;
- disallowed phrase match or multi-entry collision -> propose `quarantine`.

These token/collision outcomes do not prove meaning, synonymy, novelty, ownership, scope or final disposition.


## Admitted Atlas feature leaf — candidate payload classification contracts

`ATLAS_FEATURE_ADMISSION_003` admits bounded candidate-payload classification helpers for row `5.18` vocabulary governance. These helpers convert bridge-style candidate payload dictionaries into `VocabularyCandidate` instances and classify ordered candidate batches without mutating the canonical vocabulary file.

The helpers are allowed to support proof and review of proposed candidate actions. They do not make semantic admission decisions or admit terms, and their outputs remain subordinate to accepted human-readable meaning before builder projection, parity proof and retained-test execution.

## Admitted Atlas feature leaf — synonym candidate quarantine annotations

`ATLAS_FEATURE_ADMISSION_004` admits a bounded synonym-candidate audit annotation for row `5.18` vocabulary governance. The synonym-candidate audit may now emit a parallel `candidate_classifications` review surface for each LLM-escalation candidate.

The annotation classifies near-match synonym candidates as `quarantine` because a near-match phrase must not be automatically admitted, suppressed, or converted to an alias before the governed LLM escalation pass resolves it. The annotation is a review/proof helper only: it must not mutate `data/vocabulary/canonical_vocabulary.json`, suppress synonym candidates, or admit durable terms by itself.

## Admitted Atlas feature leaf — clean-audit stamp guard

`ATLAS_FEATURE_ADMISSION_005` admits the vocabulary touch-stamp guard for row `5.18` vocabulary governance. `write_stamp` may advance `data/vocabulary/vocabulary_touch_stamp.json` only after the deterministic synonym-candidate audit returns no unresolved escalation candidates.

This guard preserves the feeder-process boundary: a non-empty synonym-candidate report blocks stamp advancement until the governed escalation pass resolves the candidates. The guard does not admit terms, suppress candidates, or mutate the canonical vocabulary file.
## Admitted Atlas feature leaf — candidate admission plan contracts

`ATLAS_FEATURE_ADMISSION_006` admits bounded candidate-admission plan helpers for row `5.18` vocabulary governance. These helpers convert a classified candidate into a reviewable admission plan: `add_new` candidates produce a proposed `VocabularyEntry`, `alias_only` and `enrich_existing` candidates produce candidate aliases for an existing governed entry, and `quarantine` candidates produce no mutation plan.

`ATLAS_FEATURE_ADMISSION_007` admits pure document-level candidate application helpers for proof and review only. `VocabularyDocument.with_candidate_admission` and `VocabularyDocument.with_candidate_admissions` may return a new validated `VocabularyDocument` instance for non-quarantined candidates, but they must not write `data/vocabulary/canonical_vocabulary.json`, suppress synonym candidates, or bypass the builder/generator parity workflow. Quarantined candidates must be rejected rather than admitted.


## Admitted Atlas feature leaf — candidate admission review reports

`ATLAS_FEATURE_ADMISSION_011` admits bounded candidate-admission review helpers for row `5.18` vocabulary governance. These helpers convert candidate and bridge-style candidate payload batches into review reports containing `admissible`, `quarantined`, or `invalid` statuses plus governed action counts.

The review helpers are operational proof surfaces only. They may make invalid or quarantined candidates visible without raising early batch exceptions, but they must not write `data/vocabulary/canonical_vocabulary.json`, suppress synonym candidates, edit Atlas source JSON, or bypass the governed builder/generator workflow.


## Admitted Atlas feature leaf — synonym audit admission-review annotations

`ATLAS_FEATURE_ADMISSION_012` admits bounded admission-review annotations in the deterministic synonym-candidate audit for row `5.18` vocabulary governance. Each LLM-escalation candidate may expose a parallel `admission_review` payload showing that the candidate remains `quarantined` with no proposed entry or alias mutation.

This annotation is a review/proof helper only. It must not suppress candidates, advance the vocabulary touch stamp, edit canonical vocabulary data, or replace the governed LLM escalation pass.


## Admitted Atlas feature leaf — synonym audit clean-check CLI

`ATLAS_FEATURE_ADMISSION_013` admits bounded synonym-audit CLI modes for row `5.18` vocabulary governance. `--check-clean` may write the deterministic audit report and return non-zero when unresolved escalation candidates remain; `--write-stamp` may advance the vocabulary touch stamp only through the existing clean-report guard.

These modes are workflow enforcement helpers only. They must not perform LLM resolution, suppress candidates, admit terms, mutate canonical vocabulary data, or bypass the governed review process.


## Admitted Atlas feature leaf — synonym audit clean-check proof block

`ATLAS_FEATURE_ADMISSION_014` admits a dedicated `vocabulary_synonym_audit_clean_check` proof block. The block runs `python scripts/vocabulary_synonym_audit.py --check-clean` to prove that the committed synonym-candidate report is regenerated and contains no unresolved escalation candidates.

The block is an enforcement surface only. It does not resolve LLM escalations, admit durable terms, or replace the full `vocabulary_governance_conformance_candidate` block.


## Admitted Atlas feature leaf — candidate review CLI

`ATLAS_FEATURE_ADMISSION_015` admits `scripts/vocabulary_candidate_review.py` as a bounded review CLI for row `5.18` vocabulary governance. The CLI reads a canonical vocabulary JSON document plus a bridge-style candidate-payload JSON file, emits a status-bearing admission review report, and optionally writes that report to a requested output path.

The CLI must be read-only with respect to the canonical vocabulary and Atlas source files. It may expose admissible, quarantined, and invalid candidate statuses for PM/worker review, but it must not admit terms, suppress candidates, mutate canonical vocabulary data, or bypass the governed builder/generator workflow.


## Admitted support leaf — proof receipt emission

`ATLAS_FEATURE_ADMISSION_016` admits JSON proof receipts for named proof-block describe/check/run operations. Vocabulary governance proof runs may now emit a durable receipt containing the block id, mode, command, owned paths, status, and exit code.

The receipt is evidence metadata only. It does not replace stdout/stderr/status logs, does not infer ownership outside `config/proof_blocks.yaml`, and does not admit vocabulary terms.


## Admitted support leaf — proof-block JSON listing

`ATLAS_FEATURE_ADMISSION_017` admits machine-readable proof-block listing via `scripts/run_proof_block.py --list --json`. This supports worker/PM routing of vocabulary proof blocks without parsing human-oriented command output.

The listing is metadata only. It does not run proof commands, infer ownership, admit vocabulary terms, or mutate canonical vocabulary data.


## Admitted Atlas feature leaf — candidate review clean-check CLI

`ATLAS_FEATURE_ADMISSION_018` admits `--check-clean` for `scripts/vocabulary_candidate_review.py`. The mode returns non-zero when a candidate review input contains invalid or quarantined candidates and returns zero only when all reviewed candidates are currently admissible.

This mode is an enforcement helper only. It does not admit terms or mutate canonical vocabulary data; it only blocks a candidate payload from being treated as clean when the review report still contains invalid or quarantined entries.


## Admitted Atlas feature leaf — candidate review JSON receipts

`ATLAS_FEATURE_ADMISSION_019` admits JSON receipts for `scripts/vocabulary_candidate_review.py`. The CLI may write a receipt containing mode, status, exit code, summary counts, blocked-candidate rows, and any input-shape error while keeping stdout/stderr/status logs as the primary command evidence.

The receipt is evidence metadata only. It must not admit terms, mutate canonical vocabulary data, suppress synonym candidates, edit Atlas source JSON, or replace the governed builder/generator workflow.


## Admitted Atlas feature leaf — candidate review summary-only mode

`ATLAS_FEATURE_ADMISSION_020` admits `--summary-only` for `scripts/vocabulary_candidate_review.py`. The mode emits only the status/action summary and blocked-candidate list so PM/worker routing can inspect candidate batches without parsing full review rows.

The summary is routing evidence only. It must not hide invalid/quarantined candidates, mutate canonical vocabulary data, or be treated as durable vocabulary admission.


## Admitted Atlas feature leaf — candidate review error receipts

`ATLAS_FEATURE_ADMISSION_021` admits error receipts for candidate-review input-shape failures. When `--receipt` is supplied and a candidate payload cannot be parsed as governed candidate objects, the CLI may write an `ERROR` receipt before propagating the failure.

The error receipt is a diagnostic artefact only. It must not convert invalid candidates into quarantine, suppress the failure, or permit a candidate payload to be treated as clean.


## Admitted support leaf — proof-block detailed JSON listing

`ATLAS_FEATURE_ADMISSION_022` admits detailed JSON proof-block listing via `scripts/run_proof_block.py --list --json --detailed`. The detailed listing may expose each proof block's id, tier, lifecycle, command, and owned paths so PM/worker routing can confirm proof surfaces without parsing `config/proof_blocks.yaml` directly.

The detailed listing is metadata only. It must not run proof commands, infer ownership outside the manifest, mutate proof configuration, admit vocabulary terms, or replace command stdout/stderr/status logs.


## Admitted support leaf — proof-block current-interpreter execution

`ATLAS_FEATURE_ADMISSION_023` admits current-interpreter proof-block execution for `scripts/run_proof_block.py`. When a manifest command begins with `python`, the proof runner resolves it to the interpreter currently running the proof runner so offline VENV executions do not accidentally fall back to the host Python.

The resolution is execution hygiene only. It must not rewrite proof commands in `config/proof_blocks.yaml`, infer ownership outside the proof manifest, create virtual environments, or bypass dependency-governance rules.


## Admitted Atlas feature leaf — candidate review stdin input

`ATLAS_FEATURE_ADMISSION_024` admits `--candidates -` for `scripts/vocabulary_candidate_review.py`. The CLI may read a bridge-style candidate payload from standard input for worker/PM pipelines that need to avoid writing transient candidate files.

The stdin input mode is a transport convenience only. It must preserve the same validation, summary, receipt, and clean-check semantics as file-backed candidate payloads; it must not admit terms, suppress blocked candidates, or mutate canonical vocabulary data.


## Admitted Atlas feature leaf — candidate review clean-check proof block

`ATLAS_FEATURE_ADMISSION_025` admits the `vocabulary_candidate_review_clean_check` proof block. The block runs the candidate-review CLI against a committed clean candidate fixture and requires `--check-clean` to return zero.

The proof block proves the read-only candidate-review clean path only. It must not treat the clean fixture as an Atlas admission, mutate canonical vocabulary data, hide blocked candidates, or replace the broader vocabulary-governance conformance block.
