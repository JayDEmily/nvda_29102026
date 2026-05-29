# Gate 1 Normative Authority Repair — Full Read Manifest

Date: 2026-05-29  
Final-build branch: `work/NVIDIA_2026_gate1_normative_repair_final_20260529`  
Parent compact-baseline commit: `834a4f11252e6d413383ac32249352edfd07346e`

## Objective

Repair only the evidenced Gate 1 normative-authority defects on top of the compact Git-preserving baseline, then establish a deliberately empty successor planning/ledger state as expressly directed by the user.

## Direct user authority applied in this leaf

- Perform the Gate 1 normative repair.
- Deliver one final tarball named `NVIDIA_2026.tar.gz`.
- Replace `PLANS.md` with the literal user-completion placeholder.
- Retire the existing `ROADMAP_LEDGER.md` and create `ROADMAP_LEDGER_V2.md` as a placeholder.
- Do **not** modify `AGENTS.md`.

## Read evidence provenance

The normative authority audit was performed against the verified active repository source and its compact-baseline descendant. The final build was then freshly extracted from compact-baseline commit `834a4f11252e6d413383ac32249352edfd07346e` before applying the bounded repair patch, avoiding contamination from an interrupted working directory.

## Authority and control files read in full for Gate 1 audit/repair

| Path | Reason | Mutation relevance |
|---|---|---|
| `AGENTS.md` | Root execution harness and read-before-mutate law | Read-only; expressly not modified by user direction |
| `PLANS.md` | Existing frozen standing plan | Replaced by explicit user instruction |
| `ROADMAP_LEDGER.md` | Existing live ledger/history surface | Replaced by retirement tombstone by explicit user instruction; prior contents retained in Git history |
| `intent_migration/AGENTS.override.md` | Intent-migration route authority | Read-only retained route context |
| `intent_migration/atlas_tranche_roadmap/AGENTS.override.md` | Route named by the defective working overlay | Read-only retained route context |
| `docs/00_CONTROL_SURFACE_ROUTING_INDEX.md` | Routes core/addendum interpretation | Touched: addendum interpretation clarification |
| `docs/01_NORMATIVE_CORE.md` and `docs/01.1_NORMATIVE_WORKING.md` | Highest numbered normative law and companion | Read-only constraint |
| `docs/02_BRIEFING_AND_EXECUTION_OPERATING_MODEL_CORE.md` and `.1` companion | Governed operating behaviour | Read-only context |
| `docs/03_DOMAIN_MODEL_CORE.md` and `.1` companion | Domain meanings | Read-only context |
| `docs/04_TECHNICAL_ARCHITECTURE_CORE.md` and `.1` companion | Technical architecture | Read-only context |
| `docs/05_GUARDRAILS_CORE.md` and `.1` companion | Anti-drift and shortcut law | Read-only constraint |
| `docs/06_PROCESS_AND_TRANCHE_LAW_CORE.md` | Process/document-touch owner | Direct governing core |
| `docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md` | Mixed current/historical overlay identified in audit | Touched: historical register made non-operative; old Atlas planning route/evidence classified historical/externalised; clean baseline has no active Atlas migration pack |
| `docs/07_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_CORE.md` | Ownership/output separation law | Direct governing core |
| `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md` | Ownership supplements affected by `06.1` ambiguity | Touched: ownership meaning separated from mutation authority/completion claims |
| `docs/08_TESTING_AND_PROMOTION_CORE.md` and `.1` companion | Proof and promotion law | Read-only validation context |
| `docs/09_DMPV3_PROTOCOL_CORE.md` and `.1` companion | Packet-carriage law | Read-only context |
| `docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md` and `.1` companion | Vocabulary authority | Governs registry repair |
| `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md` | Accepted architecture terms requiring defined vocabulary | Definition authority for registry repair |
| `docs/vocabulary/README.md` | Vocabulary surface routing | Read-only context |
| `docs/vocabulary/CONSOLIDATION_WORKFLOW.md` | Vocabulary admission workflow | Read-only context |
| `docs/vocabulary/vocabulary_registry.md` | Incomplete architecture-term definitions | Touched: replaces unresolved architecture definitions |

## Touched files in this leaf

- `PLANS.md`
- `ROADMAP_LEDGER.md`
- `ROADMAP_LEDGER_V2.md`
- `docs/00_CONTROL_SURFACE_ROUTING_INDEX.md`
- `docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md`
- `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md`
- `docs/vocabulary/vocabulary_registry.md`
- `handoff/NVIDIA_2026/**`

## Explicitly excluded from this leaf

- `AGENTS.md` mutation;
- route-override rewriting;
- source mutation;
- test mutation;
- configuration mutation;
- generated canonical vocabulary or generated `var/` mutation;
- Atlas tranche execution or migration replanning;
- generated Atlas-slice or original Atlas/Bridge source mutation.

## Scope-control falsification gate

An interrupted workspace contained additional edits to `src/nvda_desk/vocabulary_builder.py`, `data/vocabulary/canonical_vocabulary.json`, `data/vocabulary/vocabulary_touch_stamp.json`, and `var/vocabulary/synonym_candidates.json`. A disposable worktree based on the compact parent commit applied the Gate 1 document/control repair without those extra edits and ran `python3 scripts/run_proof_block.py --check-all`; it passed with `proof_blocks_check_all=PASS count=51`. Those extra source/generated-output changes were therefore ruled out as necessary for this leaf and are not included in `NVIDIA_2026`.

## Known retained residue

Older route-override and planning documents remain in the Git-preserving repository as historical material and may contain prior “active” wording. This leaf does not silently reinterpret or rewrite those files. The successor programme is intentionally reserved to the user through placeholder `PLANS.md` and `ROADMAP_LEDGER_V2.md`. `ROADMAP_LEDGER.md` remains present only as a retirement tombstone so existing path references do not become dangling paths.
