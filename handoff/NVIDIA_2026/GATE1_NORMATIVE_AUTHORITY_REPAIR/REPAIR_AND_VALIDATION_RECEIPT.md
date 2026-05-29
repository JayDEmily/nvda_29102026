# NVIDIA_2026 — Gate 1 Normative Authority Repair and Validation Receipt

Date: 2026-05-29  
Parent compact-baseline commit: `834a4f11252e6d413383ac32249352edfd07346e`  
Repair branch: `work/NVIDIA_2026_gate1_normative_repair_final_20260529`

## Outcome

Gate 1 authority repair is applied on a clean extraction of the compact Git-preserving baseline. The repair removes the proved ambiguity whereby working overlays mixed current planning-only state with apparently live historical mutation openings, defines previously unresolved architecture vocabulary terms, and establishes a deliberately empty successor planning/ledger state directed by the user.

## Control-state decision

| Surface | Result |
|---|---|
| `AGENTS.md` | Retained unchanged by express user instruction. |
| `PLANS.md` | Replaced with `TO BE COMPLETED BY USER.` |
| `ROADMAP_LEDGER.md` | Replaced with a retirement tombstone; former full contents remain in Git history. |
| `ROADMAP_LEDGER_V2.md` | Created with `TO BE COMPLETED BY USER.` |

## Normative repair surfaces

| File | Bounded change | Evidence in final tree |
|---|---|---|
| `docs/00_CONTROL_SURFACE_ROUTING_INDEX.md` | Clarifies that `.1` working supplements may retain lineage but do not independently reopen mutation authority. | Lines 13–19. |
| `docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md` | Declares no Atlas migration/tranche-selection/implementation pack active in this clean baseline; classifies old Atlas route/evidence as historical/externalised; converts accumulated admission branches into a non-operative historical register. | Lines 3–54 and retained-history headings below. |
| `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md` | Separates ownership meaning from present mutation authority and implementation-completion claims. | Lines 3–13. |
| `docs/vocabulary/vocabulary_registry.md` | Replaces unresolved blueprint architecture-term definitions and adds the missing governed architecture entries required by the blueprint vocabulary surface. | Lines 3–65. |

## Scope boundary proved

No source, tests, configuration, canonical/generated data, or retained `var/` artefact was changed in the final Gate 1 repair tree. An interrupted prior workspace contained proposed vocabulary-builder/generated-output edits; a disposable-worktree falsification run proved they were unnecessary because the document/control-only repair passed all 51 proof blocks without those extra edits. They are not included in this handoff.

Older route-override and planning files are retained as Git-preserved historical material and may contain former active-route wording. `docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md` now expressly makes those former Atlas route/evidence surfaces historical and non-operative in the clean baseline. They were not rewritten because the user expressly required a clean successor plan/ledger placeholder state rather than a broad history rewrite.

## Validation evidence

| Check | Observed result |
|---|---|
| Parent provenance assertion | `HEAD` before repair = `834a4f11252e6d413383ac32249352edfd07346e`; passed. |
| Placeholder/tombstone assertions | `PLANS.md`, `ROADMAP_LEDGER.md`, `ROADMAP_LEDGER_V2.md`; passed. |
| `AGENTS.md` unchanged assertion | `git diff -- AGENTS.md` byte count = `0`; passed. |
| Scope assertion | `git diff --name-only -- src tests config data var` empty; passed. |
| Gate 1 textual assertions | Required repaired clauses found; no `TODO define clearly.` remains in `docs/vocabulary/vocabulary_registry.md`; passed. |
| `git diff --check` | Passed. |
| `make scaffold-check` | `repo scaffold present`; passed. |
| `python3 scripts/run_proof_block.py --check-all` | `proof_blocks_check_all=PASS count=51`; passed. |
| Directly affected Tier A pytest selection | `26 passed in 1.16s`; passed. |

Targeted pytest selection executed:

```text
tests/tier_a/vocabulary/test_vocabulary_canonical_builder_parity.py
tests/tier_a/vocabulary/test_parallel_risk_description_vocabulary_constraints.py
tests/tier_a/parallel_risk/test_parallel_risk_description_contract.py
tests/tier_a/parallel_risk/test_parallel_risk_description_templates.py
tests/tier_a/parallel_risk/test_parallel_risk_minute_profile_contracts.py
```

## Known true / Ruled out / Next gate

**Known true**

- The compact baseline parent preserves Git history and removes obsolete forward-tree `var/` bulk while retaining live-required artefacts.
- Gate 1 repair modifies only control/normative/vocabulary-document and embedded handoff surfaces.
- No Atlas programme is active in this clean baseline until the user supplies successor planning/ledger authority.

**Ruled out**

- Inclusion of unintended `AGENTS.md` edits.
- Inclusion of unnecessary source or generated vocabulary-output changes.
- Treating old Atlas route/evidence material as an active forward programme in the repaired normative overlay.

**Next gate**

The user completes `PLANS.md` and `ROADMAP_LEDGER_V2.md`, declares the successor migration route and evidence inputs, then only that declared route may accept or reject the current external Atlas semantic/provider-graph work.
