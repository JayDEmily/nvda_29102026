# F31 — Signed option flow and independent grouping: individual M01→M02 E1.1–E1.5 documentary audit

**Status:** AUTHOR-ASSESSED_WITH_PRECISE_HOLDS. No native source certification, independent semantic admission or active M02 implementation acceptance.

**Pinned source:** `c16468d1fb64f03a3e77fc8389d3e1797c2478bf` initial exact preparation HEAD; active worker later state UNKNOWN. **IDs:** D120, D121, D122.

**Common accepted mechanism / dependency:** R015/R016 native right/multiplier and independent predecessor-selection identity are distinct from option quote trade sign. D091 and D085 group axes are not interchangeable. Controlled values below are constructed from accepted formulae; they are not assertions about live provider data.

## Individual specification, legacy navigation and adversarial refusal

### D120 — Signed option order flow

- **Authority and effective inputs:** `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 K08_RULE_BUCKET_POLICY; Annex B `D120`; effective raw `R015;R016;R120;R121;R126;R127`, predecessors `D015`. Accepted overlay: `handoff/workbook_v2/r02_d120_review/D120_OWNER_APPROVED_CONTRACT_AMENDMENT.md`. The historical catalogue row may differ where a later overlay exists.
- **Independent mathematical witness / output:** One buyer option trade price=2 size=3 multiplier=100; one seller price=4 size=1 multiplier=100. Signed contracts 3-1=2; signed premium notional 3*2*100-1*4*100=200.
- **History, identity and fixture prerequisites:** Two native trade rows R120/R121 paired by occurrence; each has D015 sign and exact versioned option contract/right R015 and multiplier R016 with its own eligible identity and nonfuture timing; 1m/5m/session selection parameter. For fault injection, first construct a source-complete positive sequence whose selected state is actually reachable; preserve timestamp/knowledge-cutoff eligibility and paginate all required history before introducing the intended fault.
- **Refusal / discriminating negative case:** Multiplier absent/zero/inferred 100, wrong right, ambiguous event sign, mismatched trade-price/size occurrence, metadata arriving after trade => refuse.
- **Legacy M01 location and reuse disposition:** `src/nvda_desk/derived_signal_calculation_truth/_stage1.py:3099`. `REEXPRESS_NATIVE_MULTIPLIER_20261015_AND_PUBLIC_SEAM; preserve signed-contract and premium outputs.`. Existing public navigation: `tests/product/derived_signal/native_signed_flow_fixture.py`; `tests/product/derived_signal/test_m01_d120_native_multiplier_public.py`. These locations were inspected as existing evidence; no old test is automatically accepted as M02 proof.
- **Native and M02 holds:** Native multiplier/right mapping, trade/quote temporal alignment and policy freshness remain admission questions. Still need typed public occurrence/refusal, exact calculation/selection version, immutable complete raw+predecessor lineage and isolated SQLite first-write/readback/fresh-process proof under current root §7.

### D121 — Signed flow by delta bucket

- **Authority and effective inputs:** `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 K08_RULE_BUCKET_POLICY; Annex B `D121`; effective raw `NONE_DECLARED`, predecessors `D120;D091`. The historical catalogue row may differ where a later overlay exists.
- **Independent mathematical witness / output:** Two selected D120 occurrences: contract A delta bucket B1 signed (3 contracts,600 notional), contract B bucket B2 (-1,-400). Group(B1)=(3,600), Group(B2)=(-1,-400).
- **History, identity and fixture prerequisites:** D120 and D091 each independently versioned with same exact contract/underlying/expiry/strike/right; apply admitted absolute-delta bucket boundary/tie inclusion and grouping; select within named window. For fault injection, first construct a source-complete positive sequence whose selected state is actually reachable; preserve timestamp/knowledge-cutoff eligibility and paginate all required history before introducing the intended fault.
- **Refusal / discriminating negative case:** Mismatched contract identity; missing D091 label; silent grouping by equal unrelated UUID or metadata string => refuse.
- **Legacy M01 location and reuse disposition:** `src/nvda_desk/derived_signal_calculation_truth/_stage1.py:3141`. `REUSE_TYPED_CONTRACT_IDENTITY_GROUPING_AS_SPEC, not M01 helper by UUID.`. Existing public navigation: `tests/product/derived_signal/test_m01_f3_grouped_public.py`. These locations were inspected as existing evidence; no old test is automatically accepted as M02 proof.
- **Native and M02 holds:** Immutable delta bucket configuration, contract lineages and native provider source/temporal mapping unresolved. Still need typed public occurrence/refusal, exact calculation/selection version, immutable complete raw+predecessor lineage and isolated SQLite first-write/readback/fresh-process proof under current root §7.

### D122 — Signed flow by expiry

- **Authority and effective inputs:** `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 K08_RULE_BUCKET_POLICY; Annex B `D122`; effective raw `NONE_DECLARED`, predecessors `D120;D085`. The historical catalogue row may differ where a later overlay exists.
- **Independent mathematical witness / output:** Two D120 occurrences same right but D085 expiry-role: DTE=7 => (+3,+600), DTE=30 => (-1,-400); expiry bucket grouping preserves distinct totals.
- **History, identity and fixture prerequisites:** Match exact contract identity for D120 and D085; versioned expiry/DTE bucket boundaries and selection instant/calendar; aggregate signed contracts and signed premium notional by defined expiry group. For fault injection, first construct a source-complete positive sequence whose selected state is actually reachable; preserve timestamp/knowledge-cutoff eligibility and paginate all required history before introducing the intended fault.
- **Refusal / discriminating negative case:** Expiry mismatch, missing D085, silently using earliest available expiry or future deadline => refuse.
- **Legacy M01 location and reuse disposition:** `src/nvda_desk/derived_signal_calculation_truth/_stage1.py:3141`. `REEXPRESS_FIXED_EXPIRY_GROUPING_AS_SPEC, not generic metadata grouping.`. Existing public navigation: `tests/product/derived_signal/test_m01_f3_grouped_public.py`. These locations were inspected as existing evidence; no old test is automatically accepted as M02 proof.
- **Native and M02 holds:** Admitted calendar, expiry/DTE interpretation and option contract mapping required. Still need typed public occurrence/refusal, exact calculation/selection version, immutable complete raw+predecessor lineage and isolated SQLite first-write/readback/fresh-process proof under current root §7.

## E1.5 — bounded independent documentary challenge

- **Numerical:** One buyer option trade price=2 size=3 multiplier=100; one seller price=4 size=1 multiplier=100. Signed contracts 3-1=2; signed premium notional 3*2*100-1*4*100=200. This witness distinguishes the accepted operation, units and output shape from a plausible wrong implementation. Independently derived here; not generated by the M01 evaluator.
- **Selection/fault:** Keep D120 occurrence IDs but change a D091 contract identity. D121 must refuse while D122 depends on independently matched D085. First construct the full positive history and independently identify the exact mutation or omitted observation; a cursor exhausted before the condition is reached is not evidence for the intended refusal.
- **Authority boundary:** Family may share replay/identity/provenance engines only with separate acceptance; each D identity above keeps its own equation, prerequisite and refusal. Unresolved provider/model/source mappings remain precisely held; no fabricated native range, output or live capability.
- **Disposition:** D120=AUDITED_WITH_PRECISE_HOLDS, D121=AUDITED_WITH_PRECISE_HOLDS, D122=AUDITED_WITH_PRECISE_HOLDS. AUTHOR documentary assessment only.
