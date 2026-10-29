# Independent D014 authored-proof adequacy review

Disposition: RETURN_FOR_AUTHORED_PROOF_REPAIR. Do not admit these exact four hashes as immutable generation 1 yet.

Reference: independent-review/g61-d014-authored-proof/e13ccd9/20261020.
Reviewer: /root/d014_physical_proof_review, independently judging the authored source, not implementing it or exercising unadmitted proof.

## Candidate, authority and evidence boundary

Verified clean HEAD e13ccd9d6570753027ea39832aa5f269d2aacb76, tree 012f07b109f4b5fb7132048de919aad5c1bfaf70, repository /workspace/scratch/d549b6d808a9/resume-20261020-ejayrse7/repository. The delta from 85b83e91649fef0f259796b722c90b0771d86be0 contains exactly the four proof sources and root/record documentary progress. No reviewer source/branch/worktree/plan/ledger mutation occurred.

| Physical source | SHA256 |
| --- | --- |
| test_raw_ratio.py | a7e8ec6b5aca44e21068b78eefdf619e3ffef34d52ff1e001371345aff7b0318 |
| _support.py | 49c6149d1ff64e002154b275bc9c54793cf60623bb0c9878c0fd5539fbc058e6 |
| typing/valid_seam.py | 3d1e2ac2449fc13be7db8f0e26c2b505dee5e6810d591dd190d4044bf859dacc |
| typing/invalid_seam.py | 84b2806f0c8be162321c35f792f987550a3cf2ff428d37edd007042fcc699fc9 |

The exact accepted brief SHA c23ea315c94b478c568f105e94891a03af62393792a1478c33027a0371738bb8 and incorporated contract SHA 54850f780c4442924e2d28ed319ae5f0fb109e291b367391ac0a4c86190294fc were independently hashed and read. Historical PROPOSED headings do not erase actual designV2/delegated admission in G6_1_D014_DESIGN_REVIEW_20261020.md and current root section 7.3. This review does not reopen that design decision or supply native-source law.

Read GUARDRAILS.md, AGENTS.md including reviewer recurrence/fixture-independence rules, tests/AGENTS.override.md, current root plan, exact four sources, native binding, D014 design/control/collection-phase dispositions, D012 proof findings and actual 9b692ec -> 7eaddf9 repair diff, D013 initial/revised proof reports and actual 3876ad0 repair diff. Primary code inspected includes M00 public record/mapping/projection/history/owner declarations, M02 _selection.py, _evaluation.py codec, _sqlite.py path/schema/transaction/identity discipline and _rational.py codec. The accepted mathematical brief's K02 equation/nonzero denominator/raw-unit clauses were inspected directly. README/Makefile/pyproject were read for repository context; stale README scope does not override current explicit authority.

All observations below are SOURCE-LEVEL ADEQUACY, not product runtime results. No pytest, collection, new-seam mypy, aggregate, new API invocation or authored helper execution occurred. Missing additive names are the intended later RED boundary, not a proof defect. No result is inferred from existing old aggregate receipts.

## F001 — Important / RECURRENT_CLASS: duplicate consistency still lacks the independent source distinctions repaired in D012

Source: test_raw_ratio.py lines 414-418, with parameter dimensions at 249-307 and the unchanged-history assertions at 493-505.

The only conflicting-duplicate witness returns one page containing `(first, replace(first, source_provider="OTHER"))`; the identical-duplicate positive returns `(first, first)` on one page. This correctly detects the specific good-first / eligibility-invalid-second filtering bug, but does not independently discriminate duplicate comparison across page boundaries, reverse arrival order, or equal-valued different native Decimal representation. The real-multipage positive has distinct IDs, so it does not establish cross-page same-ID consistency. P04's native-representation identity test changes a single lawful observation in a separate source; it is not a conflicting same-ID duplicate refusal.

This is not a demand to duplicate every old test. The exact class matters because current brief section 5 explicitly requires complete stable pagination/deduplication and preservation of native Decimal tuples; section 9/P02 and root 7.3's second review-focus class require duplicate content not to hide the actual source distinction. The D012 F001 lineage expressly identified missing independent duplicate order/page/representation witnesses. Its accepted repair at 7eaddf9 independently parameterised reverse/cross_page and added representation, stale and receipt differences. D014 has restored the exact same collapsed-discriminator gap at its new public path, while the original D012 aggregate exercises the old factory, not the new raw-ratio wiring.

Concrete escaping mechanism, INFERRED from source: a new-path adapter that checks conflicting repeated IDs only within the current page and compares eligible Decimal values by numeric equality can satisfy every current D014 duplicate witness while accepting a later-page conflicting same-ID record or Decimal("2") versus Decimal("2.0"). Existing unchanged _selection._same_content actually compares native tuples and keeps its seen map across all pages; its correctness is not the finding. The authored new-path proof cannot independently establish that these distinctions reach that helper intact. No such defective implementation is claimed to exist.

Required class-level closure: source-derived duplicate-consistency proof must independently retain same-ID exact content consistency across order and pagination, including numerically equal but representation-distinct native Decimal content, without conflating that with ordinary invalid-record filtering or distinct-ID ambiguity. Preserve lawful identical duplicates and lawful distinct-ID ineligible records, and immediate unchanged empty/nonempty history for refusals. The closure comes from accepted exact-content/pagination/native-representation law and the relevant actual repair lineage; it requires no new financial/native convention or open-ended test expansion. No production patch is prescribed.

## F002 — Important / ISOLATED: P05 does not establish its mandatory exact declared table constraints

Source: test_raw_ratio.py lines 905-951 (positive profile checks) and 1126-1148 (schema corruptions).

P05 checks the exact three table names and STRICT bits, then `PRAGMA table_info` column names, NOT NULL bits and types. It never inspects the PK ordinal field, declared foreign-key targets/columns, or the configuration kind CHECK. `PRAGMA foreign_key_check == []` establishes no violated existing references; it cannot establish that the foreign-key declaration exists. The schema-negative modes cover an extra table, trigger omission/alteration and an extra column, but no constraint removal/change. Trigger checks do not supply missing table-constraint evidence.

Accepted brief section 7 explicitly fixes composite primary keys, the configuration-kind CHECK, and occurrence -> definition foreign key, and mandates validating the exact declared table/trigger schema with no downgrade tolerance. Root 7.3.2 assigns exact schema proof to P05. Current source is insufficient for that exact proposition: a consistently constructed/accepted downgraded schema can retain every observed name/type/null/STRICT property, admit lawful data and pass all current schema mutation cases.

Independent documentary probe in static_review.py constructs two in-memory SQLite schema declarations with identical column names/types/NOT NULL/STRICT and clean foreign_key_check, but one omits the configuration PK and kind CHECK. Every projection actually used by the authored positive table check is identical while sqlite_schema SQL differs. This is a standard-library schema-information counterexample, not an execution of the D014 tests, M00, M02, domain storage or an admitted product aggregate. The production baseline _sqlite._schema compares exact schema SQL plus foreign_key_check; this demonstrates that the existing architecture already distinguishes declaration equality from consistency of current rows.

Required closure: independently establish the exact authority-fixed PK/CHECK/FK declarations and reject a constraint downgrade while holding the other schema/data/hash/profile properties lawful. Retain all current separate hash/payload/index/equation/trigger/path checks. No particular implementation or patch is prescribed.

Classification rationale: ISOLATED is used for the newly identified declaration-versus-current-data blind spot. Prior D012 F003's separate hash/payload/index proof was inspected; those content-integrity dimensions are now independently covered. This finding is not another absent first-insert or version-confounding witness. Broadly calling all insufficient evidence one recurrence class would erase the specific mechanism required by AGENTS.

## Adequate source observations retained

P01 directly creates an independent real M00 probe, explicitly admits both literal observations and projects each before `seam()`. For its actual transition it creates a second empty raw store, creates a new owner, asserts empty history and `materialise is None`, asserts public projection absence, then explicitly admits inputs and materialises exact 1/3. Support raw_source provisions an empty real M00 file only; configuration registers literals but does not materialise/retry. The public sequencing therefore is visible in the test rather than hidden in helper composition. Review independently decomposed those calls against M00's public producer/projector source; it did not execute Worker helpers or absent new names. Memory and SQLite P01 modes remain distinct.

P01 checks typed complete occurrence/raw lineage, old authority snapshots through exact registered configuration reads, parameter+selection refs, sorted unit refs and independent canonical logical hash. Its oracle does not import production serialization. Exact identity excludes calculated time and includes the authority-defined request/config/raw snapshots.

P02 has 50 refusal labels plus six positive modes, each under empty/populated history. Refusals check history immediately after each call; all 208 unsupported IDs are separately checked. The trace is cleared per request, not once for the unsupported batch. Latest-invalid, late receipt, inclusive freshness/skew and real two-page selection are separate lawful controls. F001 concerns the specific missing duplicate interaction, not this broad coverage.

P03 has 14 independent literal expected cases, including +/-1/3, 1/2, zero, +/-1, signed-zero denominator absence, artificial signed 2/1, fractional 2.50/1.25, huge/tiny exponent, and >4300-digit rational components. Low precision and Inexact/Rounded traps surround materialise; global integer conversion limits must remain unchanged. Native Decimal tuples and exact integer-text wire values are checked. Signed artificial algebra is expressly not claimed native displayed-size validity; no integer/positivity/magnitude/clipping requirement is invented.

P04 independently varies 11 dimensions: definition, parameter, selection, bid/ask unit, bid/ask mapping, raw identity, native representation, asof and cutoff. It permits asymmetric lawful unit/mapping versions; later-clock retry retains the first complete fact/time. Old/new getters, history ordering/limits/inclusive filters/unknown reads and every configuration family atomic conflict are authored separately. Conflicting registration starts with newly offered lawful members and then bad old-key content, and verifies no version2 member escaped.

P05's precommit/postcommit/competing branches begin before any materialisation. The connection subclass observes a real native INSERT, blocks before COMMIT for competing first writers, observes zero committed rows on an independent connection, then releases and checks truthful busy/retry/one first fact/time. Faults distinguish confirmed rollback versus lost commit acknowledgement. The profile observer demands writer policy on a genuinely new definition2 fact, separately from ordinary retry: D013's operation-scope repair is carried correctly. Writer-child exit precedes a fresh reader child that imports only the public API and receives path/admission/ID; its recovered bundle includes typed occurrence, every registered definition/parameter/selection/unit/mapping and bounded history, with unchanged bytes.

Separate corruptions cover payload bytes, content hash, logical hash, index, canonical ratio/integer text, native representation, registered configuration content/link, definition link and rehashed wrong equation. The wrong-equation case is valid: result is excluded from the authority-defined logical identity, so changing result to 999/1 and recomputing content hash legitimately leaves all logical-ID bytes unchanged. An independent fixed-equation check must reject it; no additional outer logical rehash is necessary. Path, readonly, appid/version, journal, triggers and real raw/v1/D013 cross-file refusal are authored. F002 is limited to exact table constraints.

## Static specimen review

Positive source is consistent with the accepted exact factories, owner/reader methods and typed return records, while retaining old Decimal and D013 predecessor-evidence facets. It uses assert_type rather than Any/object casts. Actual positive mypy GREEN is a later admitted implementation obligation.

| Negative line | Expected code | Meaning |
| --- | --- | --- |
| 18 | assignment | old Decimal reader is not new reader |
| 19 | assignment | D013 reader is not new reader |
| 20 | assignment | old occurrence is not raw-ratio occurrence |
| 21 | assignment | D013 occurrence is not raw-ratio occurrence |
| 22 | assignment | ExactRatio is not Decimal |
| 23 | attr-defined | readonly facet cannot materialise |
| 24 | arg-type | owner materialise requires CalculationRequestV1 |
| 25 | arg-type | reader requires readonly storage |
| 26 | assignment | raw-ratio occurrence is not old occurrence |
| 27 | assignment | raw-ratio occurrence is not D013 occurrence |

Exactly seven assignment, one attr-defined and two arg-type sites. Harness requires the exact line/code set, total error count10, exit1 and empty stderr; dependency/import/Any errors cannot substitute for these diagnostics. No specimen mypy was run against deliberately absent additive names. P06's old-body AST preservation is bounded to this currently admitted additive-only unit, not permanent future semantic law.

## Actual checks and close-out

Actual executable checks, exit0: pinned CPython3.12.14 static_review.py (four compile-only files, exact six mandatory names, source-derived count163, exact ten misuse sites, proof hashes, clean candidate and standard-library documentary schema counterexample); pinned scoped `python -m ruff check tests/product/market_measurement_d014` (All checks passed!). These are not actual collected163 cases or runtime proof. Read-only git/status/diff/log/show and file inspections supplied the identified primary evidence.

The D013 per-operation budget/write-retry class and D014 resolver-readiness-versus-observed-outcome class are respected by current source. No extra law is derived from those receipts. No control suite, old aggregate, implementation review, full typing, environment provisioning, protected process inspection/control or shared fixture mutation occurred.

No authority gap blocks a bounded repair: accepted meaning defines both required closure propositions. Preserve this first RETURN before unadmitted proof repair, then obtain fresh independent adequacy for changed hashes before immutable generation admission and the genuine strict intended missing-seam RED. No new owner approval question is required by this review. This RETURN is not an observed D014 product defect, native source claim, implementation failure or rollback of accepted old controlled arithmetic.
