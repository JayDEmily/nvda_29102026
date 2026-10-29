# M01 F4 — independently verified D116/R075 normative source-meaning conflict

**Date:** 11-10-2026. **Status:** `BLOCKED — PROGRAMME-OWNER SOURCE-SEMANTICS DECISION`.
**Scope:** D116 only. This is distinct from the completed bounded D123
provider-independent repair; it does not extend or undo the D123 clarification.

## Accepted primary evidence inspected

1. `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md`, §5 K02 explicit arithmetic, line containing **`D116 = option_volume / open_interest`**.
2. `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv`, `D116` row (`Derived Signals!120`): declared raw dependencies **`R041;R075`**, description **“Option volume/open-interest ratio”**. The same row's free-text source description includes **“relative to open interest or historical average volume”**, which does not choose one mandatory denominator and conflicts with the brief's exact arithmetic.
3. `handoff/m01_completion/authority/NVDA_80_STEP_ACADEMIC_EVIDENCE_AUDIT_WITH_SIGNALS_ADDENDUM_81_94.xlsx`, `Raw Signals!A79:Y79`: **R075 = Average Option Volume**, IBKR tick **87**, generic **105**, units **contracts/day**; `Raw Signals!A51:Y52` identifies R047 and R048 as call/put option open interest, IBKR ticks **27/28** and unit contracts.
4. Same workbook, `Derived Signals!A120:O120`: D116 “Option volume/open-interest ratio” with **R041,R075**; its description allows open interest *or* historical average volume and therefore does not resolve the accepted K02 arithmetic/source selection ambiguity.
5. `tests/product/derived_signal/test_m01_f4_rc14_option_volume_oi_public.py`: a controlled M00 record labelled `R075` is populated with **synthetic 200 labelled open interest**, producing green `300 / 200 = 1.5`. This demonstrates numeric division and selection/lineage, **not** that the actual accepted R075 source supplies open interest. The test is retained unchanged as material prior evidence; it cannot prove D116's accepted denominator meaning.
6. IBKR official TWS API Available Tick Types: tick 87 **Average Option Volume**, distinct from tick 27 **Option Call Open Interest** and tick 28 **Option Put Open Interest**. Official reference: https://interactivebrokers.github.io/tws-api/tick_types.html (checked 11-10-2026).

## Established invariant failure

`R075` is average option *volume*, not open interest. Under the accepted
catalogue dependency, computing `R041/R075` calculates volume relative to
average option volume, not the explicitly accepted D116
`option_volume/open_interest` result. Those denominators are not equivalent,
and controlled test renaming does not establish source equivalence. This is a
normative source-dependency/semantic conflict, not an implementation licence to
reinterpret R075 or alter another row. The units also differ: the R075 source
register has `contracts/day`, whereas open-interest records have `contracts`.

## Exactly bounded decision required

**Does the Programme Owner preserve D116's explicit accepted `option_volume /
open_interest` arithmetic and authorise correcting D116's normative raw
dependencies to the applicable R047 (CALL) / R048 (PUT) official open-interest
source, or explicitly authorise a different D116 denominator/definition with
full necessary normative and proof synchronisation?**

The first is the evidence-supported proposal because it retains the accepted
brief arithmetic. It is **not** authorised by the D123-specific exception and
has **not** been implemented. Source R075 may still have a distinct legitimate
purpose for D117; D117 is not included in this finding or changed.

## Stop boundary

The source conflict means the RC14 D116 numerical green witness may **not** be
promoted to valid D116 semantic proof. The F4 reconciliation marks **both**
D116 edges `F4_AUTHORITY_BLOCKED_SOURCE_SEMANTICS`, while retaining their
historical numeric-test evidence. Two D123 edges are independently and
conditionally proved by the controlled M00 public-interface tests. F4 remains
unaccepted, with 54 other unproved closed-stage edges and all 30 cross-stage
own-kernel/refusal obligations outstanding. Stop downstream final F4 acceptance
at this first independently established unresolved normative invariant, without
modifying D116, R075, M00 or the accepted catalogue.
