# Post-Stage-5 Methodology Source Anthology

**Status:** `ASSEMBLY_CHECKPOINT — NOT YET FULLY MATERIALISED`
**Date:** 2026-08-17
**Scope:** NVDA Raw Signal methodology and execution-architecture learning after accepted IESRM Stage 5.
**Preservation rule:** source documents are not rewritten. The relational material before the verbatim corpus is navigational only.

## 1. Authority boundary

IESRM Stages 1–5 remain accepted and frozen for this anthology. This document does not redesign their semantic content.

The post-Stage-5 problem is narrower: how accepted Stage-5 meaning is transformed into proof, implementation, review, integration and final repository closure without semantic compression or false acceptance.

The embedded source documents are preserved as source records. The index may state chronology, overlap, strengthening, supersession or unresolved status, but it does not silently amend source meaning.

**Conflict rule:** where this index and an embedded or externally identified source appear to conflict, the source document plus its chronological and authority status governs. The index must be corrected; the source must not be rewritten to fit the index.

**Exactness rule:** `VERBATIM_TEXT_RETRIEVAL` means a complete File Library text read was available from the document's first heading through its final sentence and was copied here without editorial changes. It does **not** claim raw-byte identity because this runtime does not expose raw Library bytes for these records. `INDEXED_ONLY` means the exact full body was not materially available and is deliberately not reconstructed.

## 2. Document index

| ID | Source document | Role in the methodology record | Chronological / authority position | Materialisation status in this assembly |
|---|---|---|---|---|
| S01 | `07_FINAL_STANDALONE_PROOF.md` — **Stage-5-to-Stage-6 Realisation Bridge — Final Standalone Proof** | Standalone proof of the lawful Stage-5→Stage-6 bridge; intended conceptual backbone | Later durable proof; reported Git commit `d626ef681d3bd7165dfbd732f87886dd71180983`; reported file SHA-256 `b2a038b5229e0210df2bd36f7300b2850741340a53d5cbc4c7adc6a501e452ea` | **INDEXED_ONLY — exact full body unavailable in this runtime. Do not reconstruct.** |
| S02 | `CHRONOLOGICAL_DECISIONS_AND_LESSONS.md` / latest preserved chronology | Primary event ledger: retains decisions, reversals, observations and Unknowns rather than projecting later doctrine backwards | Historical primary record over the 248-page `Codec guidance 1408 CURRENT.pdf` source | **INDEXED_ONLY — long body not fully materialised by the current retrieval surface.** |
| S03 | `CURRENT_OPERATING_DOCTRINE_AND_CAUSAL_LINEAGE.md` | Present best-supported doctrine at the end of the 248-page source; classifies CURRENT / CONDITIONAL / SUPERSEDED / UNKNOWN | Later semantic consolidation; explicitly does not replace the chronology | **INDEXED_ONLY — long body not fully materialised by the current retrieval surface.** |
| S04 | `THIRD_PASS_CAUSAL_RECONSTRUCTION.md` | Independent causal reconstruction written after a blind page-by-page reread before reopening the ledger | Independent semantic cross-check; explains why decisions changed and what survived | **INDEXED_ONLY — long body not fully materialised by the current retrieval surface.** |
| S05 | `THIRD_PASS_RECONCILIATION.md` | Reconciles the blind causal reconstruction against the prior ledger; records omissions and semantic deepening | Later third-pass reconciliation | **VERBATIM_TEXT_RETRIEVAL — embedded below.** |
| S06 | `DECISION_LINEAGE_AND_REVERSALS.md` | Compact lineage map from initial positions through contrary evidence to surviving lessons | Secondary index over the chronology; explicitly not a replacement | **VERBATIM_TEXT_RETRIEVAL — embedded below.** |
| S07 | `THIRD_PASS_PAGE_NOTES.md` | Page-local evidence notes supporting chronology and later causal reconstruction | Supporting evidence, not doctrine by itself | **INDEXED_ONLY — long body not fully materialised.** |
| S08 | `SEMANTIC_GAP_AUDIT.md` / coverage-validation material | Evidence that multiple differently structured passes were used; records limits of claims of exhaustiveness | Validation/provenance layer | **INDEXED_ONLY.** |
| S09 | accepted Stage-5 checkpoint `EXEC_PLAN` Stage-6 methodology section | Repository-level materialisation of the amended generic Stage-6 method: obligations, three graphs, risk-adaptive units, proof adequacy, proof-only checkpoints, cross-unit closure, orthogonal final reviews | Accepted execution-method disposition while Stage 1–5 meaning remained frozen | **INDEXED_ONLY in this anthology; source exists separately in preserved checkpoint material.** |

### Source identity notes

- `Codec guidance 1408 CURRENT.pdf`: 248 pages; recorded SHA-256 `99599b50601943ab8ab6a298fe8eee346e97d9a10d33858bbe8c0c1a442a71be`.
- The standalone proof S01 is known by filename, title, commit and reported SHA-256, but the exact full text is not exposed by the current File Library/search surfaces. The body is therefore absent here by design rather than reconstructed from summaries.
- Large Markdown sources S02–S04 and S07 can be searched and semantically opened, but the current retrieval surface truncates long reads. A truncated read is not sufficient evidence for a verbatim corpus.

## 3. Recommended reading order

1. **S01 — Final Standalone Proof** once its exact body is materially available. It is the bridge proof and should be read before secondary summaries.
2. **S03 — Current Operating Doctrine and Causal Lineage** for the surviving doctrine and explicit CURRENT / CONDITIONAL / SUPERSEDED / UNKNOWN status.
3. **S04 — Third-Pass Causal Reconstruction** for the causal explanation of how the method evolved and why the surviving rules exist.
4. **S05 — Third-Pass Reconciliation** for what the blind reread recovered that the earlier ledger missed or expressed too weakly.
5. **S06 — Decision Lineage and Reversals** for a compact map of major learning loops and reversals.
6. **S02 — Chronological Decisions and Lessons** when exact event order, source page, reversal timing or an earlier superseded position matters.
7. **S07/S08 — Page notes and validation material** when challenging coverage, provenance or whether a conclusion was independently recovered.
8. **S09 — Accepted checkpoint ExecPlan** when translating the method back into a repository execution sequence.

## 4. Overlap and cross-reference matrix

Legend: **P** = primary treatment; **S** = substantial supporting treatment; **E** = evidence/validation; **—** = not its main job.

| Methodological concern | S01 | S02 | S03 | S04 | S05 | S06 | S07/S08 | S09 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Preserve complete Stage-5 semantic field before decomposition | P | S | P | P | S | S | E | P |
| Prevent lossy contract→proof semantic compression | P | P | P | P | S | P | E | P |
| Material semantic obligations as acceptance granularity | P | P | P | P | S | P | E | P |
| State-transition, representation and interaction graphs | P | P | P | P | S | S | E | P |
| Risk/coupling-derived reasoning / realisation units | P | P | P | P | S | P | E | P |
| Acceptance, reasoning/proof and engineering/admission granularities differ | P | P | P | P | S | P | E | P |
| Proof before implementation | P | P | P | P | S | P | E | P |
| Fresh proof-adequacy review before implementation | P | P | P | P | P | P | E | P |
| Proof-only checkpoint / proof must not be weakened for implementation | S | P | P | P | S | S | E | P |
| Local PASS does not imply cross-unit/compositional PASS | P | P | P | P | S | P | E | P |
| Whole-contract semantic review separate from integration/authority review | P | P | P | P | S | P | E | P |
| Cold-start authority/repository rebinding | P | P | P | P | S | P | E | P |
| Unknowns cannot be resolved by implementation convenience | P | P | P | P | P | P | E | P |
| Fresh context as information-topology / anchoring control | P | P | P | P | P | P | E | P |
| Reviewer independence matters more than reviewer model hierarchy | S | P | P | P | P | S | E | S |
| Model strength is risk/judgement routing, not semantic law | S | P | P | P | P | P | E | P |
| Re-decompose after repeated proof-adequacy failure | S | P | P | P | S | P | E | S |
| Anti-convergence: do not let latest attractive hypothesis become doctrine | S | P | P | P | S | P | E | — |
| Clean-room knowledge provenance | S | P | P | P | P | P | E | P |
| Pinned-state packaging/re-extraction as separate evidence object | S | P | P | P | S | P | E | P |
| Adapt methodology only on evidence, then stop steering | P | P | P | P | P | P | E | S |
| Compact law: **Plan globally. Reason locally. Review independently. Integrate globally.** | P | P | P | P | P | P | E | S |

## 5. Relational status: strengthening, qualification and supersession

This section maps relationships only. It does not replace the source wording.

| Topic | Earlier position / risk | Later durable status |
|---|---|---|
| Stage 1–5 | “Stages 0–5 are fine” was too broad | Narrowed: no demonstrated implementation defect requires discarding accepted Stage 1–5 semantics, but the Stage-5→Stage-6 handoff/traceability seam had demonstrated weakness. |
| Stage 6 failure | Initially looked like three repairable implementation/test defects | Reframed by forensics as a Stage-5→Stage-6 semantic-realisation/proof-closure failure. |
| Leafing | Smaller leaves initially looked like the answer | Qualified into risk-adaptive decomposition; uniform tiny leaves rejected. |
| Granularity | Acceptance, proof reasoning and implementation were implicitly coupled | Explicitly separated; one coherent final admission does not require monolithic reasoning or implementation. |
| Tests before code | Initially treated as a strong safeguard | Strengthened: proof itself requires semantic adequacy review before code; a test can encode the wrong meaning. |
| Reviewer topology | Final semantic reviewer carried too much closure responsibility | Split into local/fresh semantic review, whole-contract semantic review, and separate integration/authority/repository closure. |
| Model strength | XHigh/High could appear to be the safety answer | Qualified: use strength where judgement risk warrants it; independence and proof architecture remain the semantic controls. |
| Repeated proof failure | Could be treated as normal iterative correction | Strengthened: repeated broad inadequacy is evidence to re-decompose rather than keep patching one anchored packet. |
| Freshness | Fresh agent ID could be mistaken for independence | Qualified: independence depends on information topology; visible rejected artefacts may still anchor a fresh context. |
| Clean start | Clean worktree/reachable history could appear sufficient | Strengthened into knowledge-provenance cleanliness: remove prior solution/defect knowledge, reflogs/unreachable objects/residue where relevant, while preserving accepted Stage 1–5 rationale. |
| Method adaptation | Attractive new ideas could be adopted conversationally | Replace with alternatives → falsification/comparison → deliberate choice → freeze the experiment until new evidence warrants adaptation. |

## 6. Current unresolved status / Unknowns

These are intentionally not converted into doctrine:

1. **S01 exact-body materialisation:** the final standalone proof cannot yet be embedded verbatim because its exact full source text is unavailable in this runtime. This is the main reason this file is an assembly checkpoint rather than the final canonical anthology.
2. **Long-source raw materialisation:** S02–S04 and S07 are indexed and semantically discoverable, but their complete raw/full text is not exposed here. They must be hydrated before this anthology can truthfully claim a complete verbatim corpus.
3. **Run-B empirical success:** the revised risk-adaptive Stage-6 method was not proven successful at the chronology cut-off. RU1 proof adequacy had failed twice and the next topology was still an experiment.
4. **Fresh-context sufficiency with visible rejected proof:** unresolved. A fresh context may still anchor on rejected artefacts if they remain visible; the experiment deliberately left that question open.
5. **Model hierarchy:** no evidence establishes a universal rule that reviewers must run on a stronger model than authors. Independence is the durable invariant; model strength remains risk-based.
6. **Exact future unit topology:** no fixed leaf count, worker count, reviewer count, Goal count or serial/parallel pattern is a methodology law. Units must continue to be derived from accepted meaning, coupling, falsifiability and risk.

## 7. Verbatim source corpus

Only documents with `VERBATIM_TEXT_RETRIEVAL` status are embedded in this checkpoint. Source markers are anthology metadata and are **not** part of the embedded source text.

---

### SOURCE S05 BEGIN — `THIRD_PASS_RECONCILIATION.md`

# Third-pass semantic reconciliation

## Purpose

The second-pass ledger was mechanically broad and already strong, but page coverage and numbering cannot prove semantic understanding. The third pass therefore used a different method: the 248-page PDF was reread page-by-page **without consulting the existing ledger**, using a rolling semantic horizon in which the current page and immediate preceding context carried the most weight and older context was reactivated only when the conversation itself returned to it.

Only after all 248 page-local notes and an independent causal reconstruction were written was the 280-entry second-pass ledger reopened for comparison.

## Independent reconstruction result

The blind reconstruction recovered the same major causal structure as the existing ledger rather than merely reproducing its categories:

- Plan is for unresolved approach/architecture; Goal is the durable execution contract after acceptance.
- First-alpha admission had to be manual because automating an unobserved workflow would encode assumptions.
- Wrong repository/workspace identity became an epistemic failure, not an administrative nuisance.
- The first-failure rule prevented inferred downstream problems becoming architecture.
- Stage-1 independent challenge genuinely changed the semantic decomposition before code.
- `Unknown` became an authority boundary, later demonstrated by the Psycopg Plan violation.
- Model strength evolved from stage/default heuristics to evidence/risk-adaptive routing.
- Fresh agents reduce correlated reasoning error only when the information topology preserves independence.
- Run A showed that green tests plus semantic reviewers did not establish representation, transition or authority-closure adequacy.
- Forensics moved the diagnosis from three implementation defects to a Stage-5→Stage-6 realisation/proof-closure problem while retaining Stages 1–5.
- Proof itself became an artefact requiring semantic adequacy review before implementation.
- Work granularity evolved through several competing theories before converging on separate acceptance, reasoning/proof and engineering/admission scales.
- The macro orchestration law emerged from evidence: **plan globally; reason locally; review independently; integrate globally**.
- Human/Codex provenance was preserved as constitutional authority + bounded challenge → Codex-derived engineering redesign.
- Clean-room isolation was understood as knowledge provenance, not cosmetic ahistory.
- Packaging became a separate evidence object rather than a clerical final step.
- Controls were added only when evidence established a missing invariant.
- The human/LLM collaboration itself required anti-convergence controls.
- The PDF ends with an unresolved experiment rather than a claim that the revised Stage-6 method is proven.

This independent reconstruction is recorded in `THIRD_PASS_CAUSAL_RECONSTRUCTION.md`.

## Reconciliation classification

The second-pass ledger contained **280 numbered headings**: 265 primary chronological entries plus 15 durable-lesson restatements.

The blind third pass found:

- **5 genuinely missing primary decisions/lessons**;
- **5 existing entries whose facts were present but whose semantic meaning was too shallow**;
- **0 existing primary entries that required deletion as materially false summaries of the source**;
- **0 durable-lesson conclusions that had to be withdrawn**.

After correction the ledger contains **285 numbered headings**: 270 primary chronological entries plus the same 15 durable-lesson restatements.

## Genuinely missing material recovered

### A. Exactly one checkpoint auditor; then stop

**Source:** pp. 189–191.

The prior ledger recorded the checkpoint audit and its findings but not the explicit experimental stopping rule: use exactly one narrow independent checkpoint auditor because synthetic reconstruction is high-leverage contamination risk; if it passes, stop auditing and move to Codex—**no third auditor and no renewed methodology redesign**.

**Action:** added ledger 16.1.

### B. Checkpoint-audit blindness was deliberately weaker than Run-B clean-room blindness

**Source:** pp. 190–191.

The auditor should receive the candidate tarball without the construction report initially, but same-Project context was acknowledged as imperfect blindness and acceptable for this construction audit. The strict clean-room boundary was the subsequent Codex experiment, which must not receive Run A or forensic reports.

**Action:** added ledger 16.2.

### C. Plan-mode environment inspection versus execution mutation

**Source:** pp. 218–220.

The prior ledger noted that the runtime mismatch was ordinary engineering, but missed the explicit mode boundary: read-only discovery of interpreters, `uv`, PostgreSQL and baseline state was valid in Plan mode; creating `.venv`, installing dependencies, starting PostgreSQL, writing proof or changing source/config would cross into execution.

**Action:** added ledger 19.8.

### D. Parent-side pre-review does not violate reviewer independence

**Source:** p. 235.

The parent may reject a proof packet it already knows is incomplete before consuming a fresh reviewer context. Independence begins when a candidate is genuinely reviewable; it does not require commissioning an auditor against an artefact whose wheel evidence/proof ownership is openly unfinished.

**Action:** added ledger 20.4.

### E. Reviewer need not be on a stronger model than the author

**Source:** pp. 240–241.

After evidence justified escalating RU1 proof authorship, the preferred topology became Sol High author + fresh Sol High reviewer. **Independent context and adversarial role separation**, not a model-strength hierarchy, are the epistemic requirement.

**Action:** added ledger 20.11.

## Existing entries deepened rather than duplicated

### 18.1 — isolated ChatGPT experiment

The prior entry said the isolated harness planned under repository method. The third pass recovered the stronger meaning: without the normal conversational commissioning ritual, the repository control surface itself oriented a history-free worker to the active ExecPlan, Stage-5 boundary, Plan/acceptance discipline and conservative stop behaviour. This is evidence about repository self-orientation, not merely an interesting secondary run.

### 19.2 — accepted history versus contamination

The prior entry correctly kept the root ExecPlan. It now records the finer distinction that checked-off operational provenance could be untidy without constituting Run-A Stage-6 solution leakage. Removing accepted Stage1–5 rationale for cosmetic ahistory would recreate semantic compression.

### 19.5 — workbook carrier versus semantic authority

Direct `.xlsx` inspection was not merely a completeness check. Its semantic purpose was to establish whether presentation/formula structure supplied meaning absent from the rendered authority. Finding none meant carrier formatting **did not enlarge authority**; the accepted contract remained the complete semantic starting point.

### 19.6 — wrong-runtime green baseline

The previous wording only separated baseline proof from Stage6 proof. The third pass recovered the extra evidential distinction: green tests under Python 3.12/pytest 7 were useful diagnostic evidence but not authoritative promotion evidence when the repository declared Python 3.13.5.

### 19.7 — environment reconstruction and non-interference

The runtime mismatch was not merely something Codex could repair. The human should not pre-solve it from remembered environment history; Codex should diagnose its actual live environment and reconstruct it during authorised execution, reporting exact constraints if blocked.

## Material that was deliberately **not** added as new ledger entries

Several third-pass observations were already adequately represented and were not duplicated merely to increase the count. Examples include:

- the accidental run did not complete Stage6 and stopped because it could not supply an independent reviewer (already 18.4);
- Goal is not required to induce planning (already 18.8);
- accepted Stage1–5 rationale is required clean-room context (already 19.2, now deepened);
- baseline validation does not establish Stage6 (retained inside deepened 19.6);
- parent Sol High → Sol Medium after high-judgement planning (already 19.18 after renumbering);
- human bounded challenge → Codex RU3 redesign (already 19.20 after renumbering);
- repeated RU1 proof patching creates anchoring risk (already 20.12 after renumbering);
- visible rejected proof creates the unresolved freshness-versus-physical-isolation experiment (already 20.17–20.20 after renumbering).

This restraint is intentional: the third pass is meant to improve semantic fidelity, not manufacture apparent completeness through finer numbering alone.

## Conclusion

The second-pass ledger was substantially sound, but it was not semantically exhaustive. The third pass found five omissions and five places where the recorded fact was weaker than the actual lesson. The most important improvement is not the count change from 280 to 285; it is that the independent causal reconstruction can explain **why** the decisions changed, what evidence moved them, and which distinctions survived later falsification.

The final remaining limitation is intrinsic: no finite reconstruction can mathematically prove that every nuance of a 248-page conversation has been captured. The evidential basis is now three different modes of checking—chronological extraction, a second semantic-gap audit, and a blind page-local causal reconstruction followed by reconciliation—rather than repeated verification of the same ledger against itself.

### SOURCE S05 END

---

### SOURCE S06 BEGIN — `DECISION_LINEAGE_AND_REVERSALS.md`

# Decision lineage and reversals

This is a secondary index over `CHRONOLOGICAL_DECISIONS_AND_LESSONS.md`. It does **not** replace the chronological ledger. Its purpose is to make the major learning loops visible: initial position -> contradictory evidence -> correction/reversal -> surviving principle.

| Lineage | Initial position | Evidence / challenge | Correction or reversal | Surviving lesson | Ledger refs |
|---|---|---|---|---|---|
| 1 | Start with a Goal | The clean repository deliberately left the first semantic unit to Codex after source inspection | Plan first; Goal only after plan review | Goal is a completion contract, not a substitute for discovery/planning | 1.2, 1.6-1.8 |
| 2 | Bundle migration/preflight in one shell procedure | First alpha run had unproven paths, config layers and archive geometry | Walk the migration manually, one invariant at a time | Do not automate an unproven workflow | 2.1, 2.4-2.5 |
| 3 | Create a new generic staging layout | Existing WSL structure was inspected | Reuse `~/incoming` and `~/code`; avoid needless nesting | Inspect reality before encoding conventions | 2.7-2.8 |
| 4 | Potentially merge/share Windows and Linux Codex configs | Two configs served different execution contexts | Keep one canonical Desktop config; disable obsolete WSL config reversibly | Reduce ambiguity rather than force config unification | 2.10-2.14 |
| 5 | `/status` and `/debug-config` were prescribed as required diagnostics | Actual Desktop product surface did not expose them as assumed | Use a normal read-only diagnostic prompt when needed | Workflow must fit the live product, not a remembered/documented interface assumption | 3.6-3.7 |
| 6 | Full access appeared in the live preflight | Preflight showed the environment was healthy but `danger-full-access` was unnecessarily broad | Reduce to Workspace/Default; later retain read-only Custom for Plan and `Approve for me` for execution | Permission breadth should match the current phase | 3.10-3.12, 3.20 |
| 7 | First Plan failure appeared to show missing IESRM | Codex had silently fallen back to an adjacent older repo | Cancel and rebind a fresh thread; prove exact root/HEAD/skill first | Workspace identity is part of experimental integrity; diagnose the first actual failure | 3.13-3.14 |
| 8 | More permission might solve read-only helper failure | A helper could not create a temp symlink | Codex used read-only OOXML instead | Do not weaken permissions to solve an incidental tooling inconvenience | 3.15 |
| 9 | XHigh could be left on broadly for safety | High token usage and decreasing semantic uncertainty | XHigh for foundational semantic work; High for architecture; Medium for bounded execution | Model effort is judgement/risk dependent | 4.1, 4.6-4.7, 8.15-8.17, 19.17 |
| 10 | Stage 4 might need to finish in one pass | Accepted source left several architecture decisions genuinely unresolved | Accept ADR-4A-D only; keep Stage 4 open; later return one consolidated irreducible package | Partial semantic acceptance is better than fake closure | 7.1-7.6 |
| 11 | A tidy ADR heading list could be approved from summary | ADR-4E-N converted prior Unknowns into architecture choices | Inspect alternatives/evidence/consequences before accepting | Consequential architecture requires reasoning, not heading-level rubber stamps | 7.8-7.23 |
| 12 | Goal might be started again at Stage 6 | User recalled one Goal was already active from before substantive execution | Retract the suggestion; retain one Goal across the bounded unit | Goals align to coherent objectives, not internal stages | 9.8-9.10 |
| 13 | Lifetime account token history informed current Codex economics | User explained March billions were intentional paid API usage | Retract lifetime inference; judge current run only | Do not infer present workload economics from unrelated historical usage | 8.16-8.17 |
| 14 | Final handoff could stage both Linux and Windows copies | User rejected duplicate canonical state | One canonical Linux tarball; Windows copy is transport only | Minimise canonical artefact multiplicity | 11.4-11.6 |
| 15 | 100/100 tests + clean Git + semantic reviewer PASS looked like completion | Independent systems-architect audit found lifecycle, representation and stale-authority defects | Stage 6 rejected | Green proof is bounded evidence, not semantic acceptance | 12.1-12.11, 21.13 |
| 16 | Repair the three visible defects | User rejected Band-Aid treatment | Freeze failed specimen and audit the methodology before repair | A failure can be experimental evidence; understand the admission failure before patching symptoms | 13.1-13.2 |
| 17 | Known defects looked like local coding/test mistakes | Traceback showed semantic compression, missing transition/representation closure and stale authority binding | Reframe as Stage-6 realisation/closure failure | Trace source -> contract -> proof -> implementation -> reviewer -> PASS and find the first missed stop | 13.3-13.18 |
| 18 | “Stages 0-5 are fine” | Detailed Stage-5 meaning was compressed on the Stage-5 -> Stage-6 seam | Narrow the claim: no evidence requires discarding accepted semantics, but the handoff/traceability seam is weak | Preserve accepted meaning while auditing transformation fidelity | 14.18-14.19 |
| 19 | Smaller leaves quickly looked like the answer | Assistant recognised it was converging too readily on the user’s latest hypothesis | Hold model-capability, unit-size, proof-architecture and orchestration-topology diagnoses concurrently | Competing explanations must be held against evidence before redesign | 14.17-14.21 |
| 20 | Uniform leafing / worker+tester per leaf seemed safer | Test authors themselves can compress/misunderstand authority; tiny leaves add handoff/process cost | Risk-adaptive units with fresh proof-adequacy review | Acceptance granularity, reasoning granularity and implementation granularity are different | 15.1-15.12 |
| 21 | Keep refining methodology conversationally | Enough experimental evidence existed for explicit alternatives | Compare alternatives, select deliberately, then freeze Run-B methodology | Method adaptation needs experimental attribution, not “latest idea wins” | 15.3, 15.14 |
| 22 | Delete Stage-6 files from old repo to make a clean checkpoint | Reflogs/unreachable objects and caches still leaked construction/solution history | Build a fresh object store with reconstructed accepted Stage 1-5 state | A clean worktree is not a clean experiment | 14.12-14.13, 16.1-16.7 |
| 23 | Proof tests could freeze exact global state around a leaf | Prior harness showed incidental aggregate state can make later valid semantics impossible | Forbid freezing global counts/sets unless authority makes them permanent | Tests should prove enduring obligations, not snapshot topology | 17.4 |
| 24 | Final packaging from live worktree seemed adequate | Stale/working-tree contamination risk | Package from clean pinned HEAD, re-extract and revalidate | Final archive is an independent evidence object | 17.5, 21.12 |
| 25 | Run-B plan selected Psycopg 3 | Stage-4/5 authority explicitly preserved driver choice as Unknown | Restore driver Unknown and introduce exact systems-architect stop if implementation truly needs a driver | Implementation convenience cannot resolve semantic/architecture Unknowns | 19.8-19.9 |
| 26 | RU3 was one broad realisation unit | Human review identified excessive semantic/coupling surface | Codex independently derived RU3-A-F while preserving one final coherent admission | Coherent final admission does not require monolithic reasoning/implementation | 19.10-19.13, 19.19 |
| 27 | First RU1 proof-adequacy failure could be normal iteration | Second fresh reviewer again found broad, structural proof defects | Interpret repeated failure as an orchestration/granularity signal | Repeated inadequacy should trigger re-decomposition, not endless patching | 20.1-20.12 |
| 28 | Terra/Medium proof authoring looked economical | RU1 meta-proof author repeatedly failed on high-judgement proof surfaces | Escalate high-risk proof authorship/fresh contexts without claiming Terra is inherently incapable | Model routing can change when evidence reclassifies the judgement risk | 20.9 |
| 29 | Reviewer findings could be patched into the same broad proof packet | Repeated patching created anchoring/overfitting risk | Re-author smaller proof leaves from authority with fresh contexts | Fresh proof authors should derive from authority, not a defect checklist | 20.10-20.14 |
| 30 | Remove rejected RU1 proof to protect fresh authors from anchoring | User wanted to observe whether fresh-context discipline alone was sufficient | Do **not** intervene; leave rejected proof visible | Sometimes preserving contamination is itself the cleaner experiment when the hypothesis is explicitly about anchoring | 20.15-20.18 |

## The recurrent pattern

Across the thread, the strongest decisions tend to follow the same shape:

1. preserve the actual observation;
2. refuse to convert an Unknown into convenience;
3. identify the narrowest failed invariant;
4. alter methodology only when the evidence demonstrates a methodological deficiency;
5. then stop steering so the next observation remains attributable.

That pattern is the connective tissue behind the later compact rule: **Plan globally. Reason locally. Review independently. Integrate globally.**

### SOURCE S06 END

---

## 8. Indexed-only source placeholders

The following markers are deliberate no-loss placeholders. They are not summaries pretending to be the missing source bodies.

### SOURCE S01 — `07_FINAL_STANDALONE_PROOF.md`

`INDEXED_ONLY — VERBATIM BODY NOT MATERIALISED IN THIS RUNTIME.`

Known identity:

- title: `Stage-5-to-Stage-6 Realisation Bridge — Final Standalone Proof`;
- reported Git commit: `d626ef681d3bd7165dfbd732f87886dd71180983`;
- reported file SHA-256: `b2a038b5229e0210df2bd36f7300b2850741340a53d5cbc4c7adc6a501e452ea`.

Do not replace this marker with a reconstruction from remembered headings, summaries or later doctrine. Replace it only after exact source materialisation.

### SOURCE S02 — `CHRONOLOGICAL_DECISIONS_AND_LESSONS.md`

`INDEXED_ONLY — COMPLETE VERBATIM BODY NOT MATERIALISED IN THIS RUNTIME.`

Use the preserved chronology repository/source artefact when available. Do not assemble a substitute from search snippets.

### SOURCE S03 — `CURRENT_OPERATING_DOCTRINE_AND_CAUSAL_LINEAGE.md`

`INDEXED_ONLY — COMPLETE VERBATIM BODY NOT MATERIALISED IN THIS RUNTIME.`

The source is discoverable and semantically readable in parts, but long-file retrieval truncates. A partial read is not a verbatim corpus.

### SOURCE S04 — `THIRD_PASS_CAUSAL_RECONSTRUCTION.md`

`INDEXED_ONLY — COMPLETE VERBATIM BODY NOT MATERIALISED IN THIS RUNTIME.`

The source is discoverable and semantically readable in parts, but long-file retrieval truncates. A partial read is not a verbatim corpus.

### SOURCE S07 — `THIRD_PASS_PAGE_NOTES.md`

`INDEXED_ONLY — COMPLETE VERBATIM BODY NOT MATERIALISED IN THIS RUNTIME.`

### SOURCE S08 — validation / gap-audit material

`INDEXED_ONLY — SUPPORTING EVIDENCE; NOT YET EMBEDDED AS A COMPLETE SOURCE SET.`

### SOURCE S09 — accepted Stage-5 checkpoint ExecPlan Stage-6 method

`INDEXED_ONLY — PRESERVED IN CHECKPOINT MATERIAL; NOT DUPLICATED FROM A PARTIAL RETRIEVAL.`

## 9. Completion condition for the final canonical anthology

This file may be promoted from `ASSEMBLY_CHECKPOINT` to a final canonical source anthology only when:

1. S01 exact bytes/text are materially recovered and identity checked against the reported source identity where possible;
2. every source designated for verbatim inclusion is fully materialised rather than retrieved through a truncated view;
3. each body is inserted without semantic editing;
4. the index is rechecked against the fully materialised corpus for chronology, overlap and supersession errors;
5. the final file explicitly preserves unresolved experimental Unknowns rather than presenting the amended Stage-6 method as already proven successful.
