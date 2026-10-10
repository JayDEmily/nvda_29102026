# M01 F4 — D123 exact-option open-interest source/selection blocker

**Date:** 2026-10-10. **Disposition:** `BLOCKED / AUTHORITY DECISION REQUIRED`.
**Reviewer status:** not an F4 or Stage-1 acceptance candidate.
**Starting Git HEAD:** `6f611c68a3de32bc90e63a9ce8289f80027b5e83` (RC14).

## Accepted sources and invariant

1. Effective normative catalogue (`handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv`, SHA-256 `8045c8c0c4a62fbc3b88759a65b415efb1f0d549764ddbdcae2c5c911cd8a64a`) declares **D123** as `K02_ALGEBRA`, direct inputs **R047;R048**, no D predecessor, applicability `NVDA option chain`, with concept *"Change in OI between official refreshes, tracked by exact contract."*
2. Accepted brief (§5 K02) states **D123 = current_OI - prior_official_OI**; §8.1 mandates exact option contract/underlying/expiry/strike/right identity where material, no substitution, and fail-closed missing exact match. §7 makes the CSV binding authoritative and requires separate programme authority for a dependency change.
3. Companion reference workbook, sheet `Raw Signals`, rows 51–52 (sheet positions) describes R047 as `Option Call Open Interest` / native Tick 27 and R048 as `Option Put Open Interest` / native Tick 28, both `Option aggregate` variant. The workbook is reference evidence, not authority overriding the accepted CSV. Their different option-right source roles are consistent with the accepted D119 call/put ratio rule in the brief.
4. Public owner `api.py` treats D123 as requiring exact option-contract join keys (`_EXACT_OPTION_CONTRACT_ROW_IDS`), requires binding equivalence across every declared raw ID (`_bindings_satisfy_join_keys`), then loads each declared raw ID (`_materialise`). Direct-kernel `_stage1.py` instead computes a change from each available raw history (per raw ID and its `subject_instrument`), without resolving whether one or both sides are applicable to the selected contract.

## Discriminating M00 public witness

`tests/product/derived_signal/test_m01_f4_d123_exact_contract_authority.py` supplies real M00-controlled projected history:

- Call contract `C150`: R047 official OI 100 previous, 125 current; expected exact-contract D123 change **+25 contracts**.
- Put contract `P150`: R048 official OI 40 previous, 42 current; competing opposite-right input has a distinct correct contract identity, and cannot lawfully be relabelled as C150.
- Both streams have explicit immutable mapping versions, native source identities, event/receipt times, official-vintage markers, native units, and exact contract selection metadata.
- Exact D123 public request binds both catalogue sources under their actual contract identities, with the mandatory exact-contract selection policy.

**Observed:** public `materialise(D123)` returns `None`; `D123_M00_PUBLIC_RED.log` records **1 failed** (`expected Decimal(25)` vs `None`). The diagnostic independently establishes that row-semantic policy validation succeeds, but `_bindings_satisfy_join_keys` rejects the two correct, different native option-right identities. Direct-kernel control `D123_DIRECT_KERNEL_GREEN.log` records **1 passed**, but uses a synthetic R047-only kernel input and therefore **does not establish public reachability**.

This is a proved public-path failure under this valid native distinction. It is **not**, by itself, proof that every conceivable D123 provider variant must fail.

## First unmet authority invariant

The accepted materials fix the exact-contract D123 meaning but do **not unambiguously say** how to interpret the simultaneous R047 and R048 catalogue edges when the selected contract is a call *or* a put. In particular, the materials do not explicitly admit an option-right-conditioned `R047 OR R048` dependency in a runtime that otherwise treats the declared R edges conjunctively. Constructing an R048 `put` value on the same exact `call` contract solely to satisfy the join would fabricate native source identity, contradicting §8.1.

An implementation-side relaxation or catalogue reassignment would choose a new material source/dependency law without authority. This is not an ordinary missing test or a licence to downgrade the exact-selection policy.

**Precise programme-owner decision required:** specify the admitted raw-input law for **D123** on a selected exact contract: for example, whether R047 applies only to selected calls and R048 only to selected puts (an expressly authorised side-conditional interpretation of both declared edges), or whether the normative dependency source(s) must be corrected. Include the required historical official-refresh identity and the permissible omission semantics of the non-selected side. No option is presumed accepted here.

## Scope and preserved state

- No product/production source, catalogue, guardrails, agent instruction, ExecPlan or version was modified.
- The intentionally failing D123 public witness and command logs are preserved in Git for a future authorised proof-first repair.
- The original F4 RC14 ledger remains at **490 dependencies plus D007 sentinel**, with **56 Stage-1-closed edges outstanding across 13 calculations** and **30 cross-stage own-kernel/refusal obligations unproved**. No credit is taken for D123, and none of F4/Stage 1/Stage 2 is accepted or authorised beyond its previous boundary.
- PostgreSQL 17.9 / Python 3.13.5 proof environment was freshly bootstrapped from attached offline archives and verified. The D123 witness used actual in-memory M00 public projection, not a direct D123 fixture. It does not require PostgreSQL to reproduce.
- The unrelated Stage-1 cross-stage graph was not touched after the first authority blocker.

## Separately observed source-provenance question — not adjudicated in this stopped pass

The same reference workbook calls **R075** `Average Option Volume` (Tick 87), whereas brief K02 defines **D116** as `option_volume / open_interest`, and the accepted D116 catalogue binds R041/R075. Existing worker D116 controlled-M00 proofs assign an open-interest-like numeric value to R075. This is a **source-meaning discrepancy requiring separate adjudication**; the workbook is only reference evidence, and this pass did **not** establish that a production R075 projection is invalid or reopen D116's behaviour. It should not be silently marked resolved by the earlier passing D116 test.

## Validation and handoff restriction

The known failing D123 public test must remain failing until the programme owner resolves the source/dependency law and a proof-first repair is undertaken. Do **not** delete it, weaken its expected `+25`, or mark the existing test suite green by excluding it without explicitly declaring its scope. This package is an authority-blocker handoff, **not** the requested final independent F4 review candidate.
