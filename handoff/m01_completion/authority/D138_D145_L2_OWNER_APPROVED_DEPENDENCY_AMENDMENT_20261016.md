# D138 and D145 — owner-approved Level-II raw-dependency amendments

**Approval:** 16 October 2026 (Australia/Melbourne). The programme owner answered **“Yes, I do”** to the explicit question requesting approval of *both* exact D138/D145 R-dependency corrections with unchanged mathematical definitions and preserved source-completeness/refusal requirements, immediately following the source-contract proposal in `handoff/workbook_v2/gates_01_02/G2_L2_NATIVE_CONTRACT_EVIDENCE_AND_APPROVAL_CANDIDATES_20261016.md` §4.

**Authority scope:** This records an explicit, narrow programme-owner mathematical/source-contract exception to the former effective D catalogue's two **raw_dependencies** declarations. It grants **no** provider-instance, M00 source/projection, implementation, runtime, test, independent-review, module ownership or Gate 2 acceptance authority. `GUARDRAILS.md`, `AGENTS.md`, the accepted Gate 1 main and frozen `EXEC_PLAN.md` remain unchanged.

## 1. Two independently approved definition revisions

| Definition revision | D identity | Before — direct R | After — authoritative direct R | Unchanged |
|---|---|---|---|---|
| `D138-L2-CONTRACT-20261016-01` | D138 | `R189;R190;R188` | `R185;R187;R188;R189;R190` | D011 predecessor; K06 per-side OLS of cumulative standing depth versus absolute distance from D011; bid/ask slope structure, parameter profile, output units and other fields |
| `D145-L2-CONTRACT-20261016-01` | D145 | `R187;R188;R189;R190` | `R185;R187;R188;R189;R190` | no D predecessor; K17 four-term consecutive best-book OFI equation, selected 1s/5s/1m windows, parameter profile, output units and other fields |

`R185` retains its established raw identity as native book-row **position**. `R187` retains its established raw identity as provider **operation**. `R188`/`R189`/`R190` retain side/price/size meanings. These dependencies are required to reconstruct position-indexed, operation-ordered book state; **none authorises** supplying unordered incremental events as independent standing depth or treating the new price as the key of a prior positional row.

## 2. Effective meaning, precedence and currently frozen catalogue bytes

The programme-owner-approved revisions above are the **specific effective semantic exceptions** for the two listed D identities; the earlier hash-bound catalogue remains the source of all other fields and all other D identities. The original Markdown brief and its incorporated historical CSV binding are not silently rewritten. Source crosswalk: `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv` SHA-256 `67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549`, **unchanged in this Gate 2 decision-only work**. The source-package copy under `src/nvda_desk/derived_signal_calculation_truth/` and the runtime loader hash remain unchanged as well. As with earlier owner-approved exceptions, an approved overlay takes semantic precedence for its *named* field only; it does not demonstrate that the current runtime package has incorporated that revision.

**Do not claim runtime catalogue synchronisation or executable admission.** Subsequent C–E implementation/change control must synchronise both catalogue copies and the hash-bound loader, and perform the applicable independent acceptance/proof, under its own authority. This Gate 2 pass deliberately leaves production source/configuration untouched. The old source-bound direct R lists remain visible as historical/readback facts in the G2.1–G2.5 fields. The separate G2.6 effective-overlay fields express the *new owner decision* and its propagated R closure.

## 3. Conditions retained; not a snapshot or projection admission

- The M00/source custodian must establish actual **SMART versus direct** `reqMarketDepth` subscription and corresponding provider callback/field projection, canonical book subject and source identity, versioned R185/R187/R188/R189/R190 mappings and units, side/position semantics and event/receipt ordering. The original workbook alone does not prove the chosen live M00 projection. Neither `R186` venue/market-maker nor `R191` Smart-depth flag is silently made a new direct R dependency; selection/provenance sufficiency is a separate question, requiring its own authority if definition scope changes.
- **D138:** require an initially valid standing book, replay of ordered same-book mutations, known completeness within the requested level scope and correct cutoff before K06 cumulative-depth OLS. Partial/missing/wrongly ordered, shifted, reset or ambiguous book state cannot produce a slope.
- **D145:** require at least the necessary prior/current best states; replay position-addressed operations through pre-window warm-up before the first included OFI transition. Preserve the provider event sequence, source/subject alignment, window boundaries and refusal when complete valid predecessor/book state is absent.
- On IBKR **error 317** reset, clear the affected reconstructed depth book; refuse required dependent states until a valid reinitialisation is proven. Fail closed on an absent/conflicted field mapping, incorrect native variant, missing book operations/sequence, insufficient warm-up, temporal ambiguity or broken source completeness. No inferred defaults, fabricated snapshots or silently substituted `Rxxx` identity.
- None of these conditions proves a particular source instance exists. The provider documentation establishes native API semantics, not that a repo-specific M00 projection or live series is admitted.

## 4. Gate 2 disposition and propagation

The mathematical **approval question** of `G2I-015` (D138) and `G2I-018` (D145) is answered `APPROVED`; both distinct **native source-contract/admission questions** remain `BLOCKED`. D138 adds terminal R185/R187 to its D011-derived closure. D145 adds terminal R185 and has **32 existing transitive descendants** in the original D graph; **30** already reach R185 through other predecessor paths, so only **D152 and D153** gain it as a new terminal R. This is static dependency propagation, not 32 independent definition changes or proof of wrong downstream calculations; established downstream disqualifiers stay in force.

`D001_D209_TRACEABILITY.csv` retains the original documented source-readback columns, and separately gives each row's post-approval direct R, terminal R and effect/status. The two issue records and their per-D links separately record owner approval and source-custodian blockers. The 35 unknown classifications, the five historically empty groups and definitive future downstream module count remain unresolved until required evidence and decisions are obtained. **Gate 2 remains BLOCKED**; C–E work remains outside the present authorisation.
