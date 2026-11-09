# ADR — NVDA GitHub repository investigation and Ubuntu handover snapshot (10 November 2026)

**Status:** DOCUMENTARY_RECORD_ONLY — not an adopted architecture decision, an amendment to GUARDRAILS/AGENTS/EXEC_PLAN, an R2 acceptance, an execution commission, a product-test result or an L00 release.

**Purpose:** Preserve verbatim the three user-visible findings sections produced during this thread's initial GitHub investigation. The sections below are historical point-in-time statements, with their source claims, caveats and references unaltered. Later evidence may supersede their status. This record does not replace current repository authority.

**Source repository:** https://github.com/JayDEmily/nvda_29102026

**Inspected branch positions at time of findings:** main `8ff7d82377e9bf8f9fc75c1ecef70f0ab29a2ada`; R1 `363923d47b81fca50e64036bef3c8601501e3c16`; R2 `6feb50bf8a96e244cbd68eb57536f940be6335b3`.

**Record provenance:** Findings authored in this ChatGPT handover conversation on 10 November 2026, before creation of this ADR. Three successive user-visible final messages have been concatenated in their original order, retaining all source text (including inline presentation-link tags) and the original timestamp.

## Verbatim findings — original text

The fenced block below is literal text. The `<Link>` expressions are preserved from the original response rather than converted or edited, to maintain the requested verbatim record.

````text
## NVIDIA project — initial GitHub verification

**The intended workflow is understood.** I will continue managing the engineering work, but your Ubuntu PC will become the execution environment rather than my temporary sandbox. GitHub will provide durable version history and handover evidence. We will retain the established modular architecture, test discipline and independently verified gate progression.

The first live GitHub checks confirm:

| Branch | Verified HEAD | Position |
|---|---|---|
| `main` | `8ff7d823` | Default branch |
| `execution/accepted-r1-20261030` | `363923d4` | 5 commits ahead of main |
| `planning/chat-manual-r2-20261030` | `6feb50bf` | 8 commits ahead of R1 |

The R2 branch contains R1 in its history, with no divergence reported by GitHub's comparison endpoint.

**Important distinction:** R2 is the most advanced of these three branches, but that does not mean its proposed changes have been accepted for execution.

The repository currently exposes 12 branches, including historical preservation and migration branches. Its R2 tree contains 4,730 entries. I have also read the frozen `GUARDRAILS.md` in full and verified that R1 and R2 contain the same guardrail blob.

Sources: [GitHub repository](https://github.com/JayDEmily/nvda_29102026), [R1 execution branch](https://github.com/JayDEmily/nvda_29102026/tree/execution/accepted-r1-20261030), [R2 planning branch](https://github.com/JayDEmily/nvda_29102026/tree/planning/chat-manual-r2-20261030).

## Current execution position

The live R1 execution register gives the clearest progress snapshot:

| Recorded state | Leaves |
|---|---:|
| L00 — blocked on checkpoint transfer | 1 |
| Not attempted, dependent on L00 | 37 |
| D145 implementation explicitly paused | 1 |
| **Total** | **39** |

The accompanying test ledger records **35 proof obligations, zero new test runs and zero released physical cases**. This means the 27 planned new derived-signal implementations have not been accepted under this tranche. It does **not** invalidate the separately recorded historical controlled-profile evidence.

The accepted programme retains six gates, 20 core derived-signal outputs, seven additional mandatory outputs, and D145 as a paused identity. <Link url="https://github.com/JayDEmily/nvda_29102026/blob/execution/accepted-r1-20261030/EXEC_PLAN.md" title="Accepted R1 execution plan"/>.

### Checkpoint discrepancy requiring reconciliation

GitHub now exposes an L00 successor release containing the 124,580,793-byte handover archive, the cumulative additive Git bundle, original baseline material and verification records.

<Link url="https://github.com/JayDEmily/nvda_29102026/releases/tag/nvda-l00-transfer-successor-40960483921" title="Published L00 successor checkpoint"/>

That publication occurred after the original failed delivery attempts recorded in the execution register. I can verify the assets are listed on the release, but **I have not independently downloaded, hashed and restored the successor**. Consequently, neither “L00 is still undeliverable” nor “L00 is fully accepted” is yet established from the evidence inspected.

## Architecture and module state

I have read the current architecture kernel and its governing taxonomy, ownership, dependency, public-seam, proof, lifecycle and implementation-authority documents in full. I also inspected the current architecture registries and selected implementation and test files.

The module register currently declares:

| Object | Registered state | Responsibility |
|---|---|---|
| M00 | Active | Raw Signal Occurrence Truth |
| M01 | Bootstrap | Derived Signal Calculation Truth foundation |
| M02 | Active | Neutral Market Measurement Truth, with bounded admitted capabilities |
| M03 | Active | Configured Market Conditions |
| A00 | Bootstrap | Application composition |
| P01 / K01 | Placeholder | Protocol / technical kernel |

There is an important historical distinction: the workbook's proposed responsibility migration towards M02 does **not** mean M01 has been formally retired in the current architecture registry. M01 remains registered as `bootstrap`, whereas M02 has bounded active admission. These are different propositions.

The M00 registry defines raw occurrence capture, persistence and typed read projections. It explicitly excludes provider/network integration. **An operational IBKR acquisition API is therefore not established by the architecture evidence.**

Sources: <Link url="https://github.com/JayDEmily/nvda_29102026/blob/planning/chat-manual-r2-20261030/config/architecture/modules.yaml" title="Current module registry"/> and <Link url="https://github.com/JayDEmily/nvda_29102026/blob/planning/chat-manual-r2-20261030/docs/architecture/ARCHITECTURAL_OBJECT_TAXONOMY.md" title="Architecture taxonomy"/>.

## Historical lessons recovered

The Git history and original review records establish several relevant lessons:

- **Real configuration paths matter.** The September architecture ADR documented a dependency checker that interpreted schema-valid edge mappings incorrectly while narrower fixture-based tests remained green. The current inspected source uses explicit `source` and `target` keys, and the associated test now contains a repository-configuration integration case. That is evidence of an implemented repair path, **not a fresh passing test result**.
- **Grouped leaves must release precise prerequisites.** Earlier planning review returned ambiguity around shared prerequisite release. R1 subsequently separated contracts into individually identifiable leaves such as L01a–d, L07a–b and L10a–c.
- **Mathematical definitions must not be inferred from examples.** The D141 replenishment calculation previously required clarification of its denominator and permitted zero numerator. The subsequent review records that clarification as resolved.
- **Publishing a checkpoint and independently accepting it are distinct.** GitHub Actions run `40960027067` failed at workflow validation; the repaired successor run `40960483921` succeeded. The successful publication is verified, but recipient-side acceptance still needs its own evidence.
- **Test scope remains finite.** R1 and R2 retain the standard success/reached-refusal pair, with explicitly bounded stock/option exceptions. No blanket regression or speculative permutation expansion is authorised.

Relevant records: <Link url="https://github.com/JayDEmily/nvda_29102026/blob/planning/chat-manual-r2-20261030/docs/architecture/ADR_20260902_ARCHITECTURE_KERNEL_CONFORMANCE_HARDENING.md" title="Historical architecture ADR"/>, <Link url="https://github.com/JayDEmily/nvda_29102026/blob/planning/chat-manual-r2-20261030/handoff/planning/m02_foundation_completion_20261030/INDEPENDENT_PLAN_REVIEW.md" title="R1 independent planning review"/> and <Link url="https://github.com/JayDEmily/nvda_29102026/actions/runs/40960483921" title="Successful transfer workflow"/>.

## Ubuntu transition and R2 decisions

Two proposed changes must not be mistaken for installed configuration.

**Python:** The committed `.python-version` and `pyproject.toml` still specify CPython `3.12.14`. R2 proposes `3.13.5`, but the configuration patch is explicitly marked not applied. Ubuntu interpreter availability, dependencies and SQLite compatibility have not been established in this investigation.

**Testing:** R2 proposes replacing R1's per-leaf independent product acceptance with a separate manual Tester chat performing dependent proofs at L32. Its precise trade-off is later discovery of upstream defects. This is a proposed methodology change, **not the accepted execution method**.

See <Link url="https://github.com/JayDEmily/nvda_29102026/blob/planning/chat-manual-r2-20261030/handoff/planning/chat_manual_transition_20261030/TRANSITION_REVIEW.md" title="R2 transition review"/>.

## Handover disposition

**Verified:** GitHub branch ancestry, current governing documents, registered module states, accepted R1 plan, proposed R2 deltas, recorded leaf/test statuses, relevant historical repairs and published release metadata.

**Still unknown:** Independent restoration of the final L00 successor, full historical ref integrity from a fresh Ubuntu clone, the PC's exact toolchain and dependency readiness, and independent semantic validation of all previously accepted derived-signal evidence. I inspected the relevant Git history and selected source/tests, but did not exhaustively re-audit every preservation ref or source file.

The appropriate next sequence, once authorised, is to establish GitHub-to-Ubuntu integrity and resolve L00; reconcile the exact environment and outstanding authority decisions; independently assess R2's methodology; then formulate the next accepted gate/leaf plan. **I would not start coding or silently activate R2 from the present evidence.**

No repository changes, commits, test executions, downloads onto your PC or Ubuntu operations were performed.

**Handover result: repository identified and initial authority/progress reconciliation completed; implementation remains uncommissioned in this thread.**

TS: 10-11-26 09:58
````
