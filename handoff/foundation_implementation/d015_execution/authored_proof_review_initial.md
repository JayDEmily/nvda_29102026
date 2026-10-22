# Independent D015 authored-proof adequacy review

Disposition: **RETURN_FOR_BOUNDED_PROOF_ORACLE_COMPLETION**. No authority or environment BLOCK is established. No proof generation is admitted by this review.

Exact candidate: `376cdabcc2fc69e06caaf89a99a409a5501b8277`.

| Inspected object | SHA256 |
| --- | --- |
| D015_IMPLEMENTATION_BRIEF.md | 84baa16665db5f8543eba3b1770dafcfb36cc5e8064b2f1837beb924713acb0d |
| D015_PROOF_CONTRACT.json | e4d481ca99dbb55e2ad4b753dc33b8ba244873eac50e541a8352a6f5384a73c5 |
| implementation/authority/D015_IMPLEMENTATION_AUTHORITY_BINDING.yaml | 9625c2a4014ac3cbb55682e17b391b8e049a873c51de65a9a2a78e5e347fa471 |
| tests/product/market_measurement_d015/test_trade_direction.py | 538919de16f96efc38673abaeec092689e092254d8f638f3e1bc123943ebdd46 |
| tests/product/market_measurement_d015/typing/valid_trade_direction.py | e1c16eaad0b86a97079ac7ff8f76887ec9b18b2f357fcfa4652f88921df727f3 |
| reused tests/product/market_measurement/_support.py | 7346630a41da3decbe7218df4534b8b83d19c9ec005484c2509faed89ed0b2ea |

## Scope, authority and lineage

Read full current frozen GUARDRAILS, root AGENTS, tests override and current ExecPlan, exact brief/contract/binding, complete physical test and positive typing consumer, original setup helper, descriptor/null pointer, preserved original design RETURN and successor PASS, and full independent shared-control review. The required exact physical test name is present once, with six literal parameter rows; the typing file is explicit required support. The existing helper remains an old-family setup dependency, not newly claimed support or an imported old test function. It supplies constructor literals and raw observations; its called functions do not materialise D015 or calculate the sign expectation. No M01 private calculator is imported. Literal expected signs are independent of implementation.

Inspected physical-source Git lineage: 376cdab is the first authored D015 physical proof commit. Earlier F001–F004 were documentary design findings, closed in ecc5829 before authority binding; no earlier authored-proof RETURN/repair cycle is present in this lineage. Classification of the present finding: **ISOLATED authored-proof oracle-completeness defect**. The accepted domain/configuration choices are not being reopened; the new issue is failure of the physical oracle to enforce the complete already specified payload. It is not a second successive unresolved design-authority gap.

## Adequate existing discriminators

- Actual public M00 admission/projection and actual accepted-admission D011 materialisation precede the missing-additive-seam assertion. No scalar midpoint substitution is used.
- The synthetic R126/R127 observations have distinct IDs and matching source/subject/price/event/receipt correspondence to old D011 facts; old D011 mappings remain unchanged.
- The first success includes visible post-trade R126/R127 quote decoys. The tick cases put the last different R120 price 120 seconds earlier, beyond current freshness, and interpose an equal-price trade one second earlier. Their literal outcomes distinguish missing prior-history coverage and a naive previous-row tick test.
- All five sign outcomes use exact int-type assertions. The sixth case has real later D011100 and otherwise lawful current trade/new quote facts, but its predecessor/quotes postdate the trade. Its no-result and empty public history assertions distinguish causal refusal from silently materialising a classification.
- The first success repeats the public request after advancing only the injected clock, compares the complete original occurrence, and reopens through the public read-only reader. This is a bounded new-store sequence within one case, not another test matrix.
- The positive consumer correctly exercises the intended additive owner/read/request/result types. No mypy pass is claimed before the production public types exist.

## Required bounded correction — P001

Authority: root sections 3.1/5.3 and exact brief sections 3–5 require at least one success to prove the complete relevant typed output/configuration and selected raw/actual predecessor lineage, followed by ordinary durable readback.

Observed physical assertions are incomplete at `test_trade_direction.py:197–221`:

- Definition checks cover only equation, raw dependencies and derived dependencies, not the complete fixed definition (D/version/kernel/profile/units/shape/authority references).
- Predecessor checks compare only `result.predecessor.occurrence` to the actual midpoint, leaving all configuration evidence members unchecked.
- Raw checks compare observation IDs, public projections and exact canonical Decimal values, but not the lineage's own event instant or unit-convention reference. In particular, `RawInputLineageV1`'s existing constructor identity checks do not by themselves prove that `event_time_utc` or the selected unit reference is semantically correct.

Consequence (reasoned counterexample, not an executed mutant): a new D015 implementation could retain correct signs/projections but put request cutoff instead of native event time into every lineage, or supply a wrong/incomplete predecessor configuration snapshot. It could serialize and reopen that same wrong payload and satisfy the present equality-based retry/readback assertions. Roundtrip equality does not independently establish the initial payload's correctness.

Required proposition for closure: **one existing successful case establishes the complete fixed definition and complete actual predecessor configuration evidence, and the expected full raw lineage including event-time and unit/mapping references, from authority literals and actual public upstream reads rather than from the returned D015 result.** Its already required retry/readback must preserve that established payload. A direct full-record comparison is sufficient; no per-field mutation suite, extra parameterised case, negative typing specimen, generic fault matrix or reauthoring of accepted authority is requested. The existing parameter/policy/unit/mapping assertions can be retained and reused.

## Independent helper-free upstream sequence

To meet fixture independence without executing unadmitted D015 behaviour, ran a separate inline Python sequence under `/workspace/scratch/83dd7c79f14f/d015-runtime-GUbvor/dev/bin/python`, cwd the exact active repo. It directly constructed authority-literal public M00/D011 records/configuration; it did not import/execute the D015 test module or the old setup helper, collect pytest, or invoke any D015 factory. Existing owner-local `capture`/`validate_evidence` were used only to verify the produced upstream fact after public construction.

Observed exit 0:

1. Before raw admission, actual D011 at trade time returned None.
2. After admitting R03499/R035101 at trade-minus2/minus1 seconds with corresponding lawful receipts, actual D011 at trade time produced100; complete existing predecessor validation accepted it.
3. In a separate raw owner with only quotes at trade-plus5 seconds, D011 at trade time returned None; D011 at plus5 produced100 and its complete predecessor validation accepted it.
4. Public D015 factory was absent; no D015 behaviour was executed.

Exact reported observations:

```text
{'late': False, 'absence_before_admission': True, 'trade_time_missing_if_late': False, 'actual_midpoint': '100', 'asof': '2026-10-16T01:00:00+00:00', 'complete_validator_accepted': True}
{'late': True, 'absence_before_admission': True, 'trade_time_missing_if_late': True, 'actual_midpoint': '100', 'asof': '2026-10-16T01:00:05+00:00', 'complete_validator_accepted': True}
{'D015_seam_absent': True, 'D015_executed': False}
```

This corroborates the fixture's narrow prerequisite/causality design; it does not execute its parameterised proof, establish admitted semantic RED, or prove D015 calculation/GREEN.

## Next boundary and limitations

Return only the bounded positive-oracle completion above, then independently review exact successor physical hashes before main exercises concrete immutable-proof admission. Actual admitted clean-candidate semantic RED remains future work. No source/control implementation was reviewed or changed, no product pytest/collection or D015 typechecker was run, no generation/admission was written. Repository status remained unchanged. This report is the only reviewer-created file.
