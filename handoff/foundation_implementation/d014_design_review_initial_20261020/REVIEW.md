# Independent D014 documentary design and authority review

Disposition: RETURN_FOR_BOUNDED_DOCUMENTARY_CORRECTION.

Reference: independent-review/g61-d014-design/ec570da/20261019.
Reviewer: /root/g61_d014_design_review. Fresh independent judgement; no subagents, shared edits, implementation, application imports, runtime/native validators, domain tests or provider operations.

## Exact subject

Repository: /workspace/scratch/d549b6d808a9/g52-recovery/repository.
Clean inspected candidate: ec570da7f1351222299508716421c0f6f2df6b42.
Tree: cc870fb7cea148961521ae7301d5c9368bba5cd9.

| Object | Independently checked SHA256 |
| --- | --- |
| handoff/foundation_implementation/authority/G6_1_D014_IMPLEMENTATION_BRIEF_PROPOSED.md | ca1a5365052c594ff2fe42533ece47a8a85de5e31f05e73b5ad1cc12a8952cb7 |
| handoff/foundation_implementation/authority/G6_1_D014_PROOF_CONTRACT_PROPOSED.json | 54850f780c4442924e2d28ed319ae5f0fb109e291b367391ac0a4c86190294fc |

This is design/authority preparation review, not implementation admission. The three findings below require bounded documentary correction and exact revised-byte review before the proposed authority is accepted. No substantive mathematical, architectural, storage or proof-design defect was established. This is not a conditional PASS for the current bytes.

## Findings

### F001 — Minor, ISOLATED: overbroad factual network nonclaim

Brief section10 line140 says `No network/provider call/SDK acquisition was performed; only public documentation reading.` The same paragraph names current remotely read public documentation. The compound denies network calls without restricting that term to broker/provider API operations. The final qualification makes intended scope understandable, but does not make the unqualified denial accurate.

Required proposition: distinguish public-documentation network retrieval from a broker connection, provider data/API operation or SDK acquisition. No source capability or execution is to be inferred from reading public documentation. This is provenance wording only, not a new provider prerequisite or a demand for acquisition work. Authority: GUARDRAILS verification-before-synthesis and claims/close-out; brief section10's own reference-only boundary.

### F002 — Minor, ISOLATED: stale marker-position/authoring statement

Brief section9 line110 says the marker/digest is supplied `below after authoring`; the actual correct marker is already immediately above at line108. Documentary checking independently finds exactly one matching contract marker. This is not a hash failure or missing contract, but the recipe must describe the actual final object rather than an unfinished authoring step. Authority: exact-byte authority/verification discipline and the section9 marker binding itself.

### F003 — Minor, ISOLATED: existing M00 mapping field name misspelled

Brief section4's mapping recipe says `selection_identity_fields=()`. The actual existing public `RawSignalProjectionMappingV1` in src/nvda_desk/raw_signal_occurrence_truth/api.py declares `selection_identity_field_paths` (line606), with type tuple[tuple[str, tuple[str, ...]], ...]. There is no `selection_identity_fields` constructor field. The same brief paragraph instructs use of the existing exact field order/types, so its intended empty metadata binding is clear, but the explicit keyword-like recipe is not exact.

Required proposition: the controlled mapping recipe must name the actual unchanged public field, carrying the empty tuple; no M00 API change or new field is authorised. Authority: AK-SEAM-001 typed boundary, unchanged-M00 boundary in brief sections2/8, and its section4 exact registration recipe.

Recurrence classification: these are new documentary accuracy/field-spelling mechanisms, not recurrence of the inspected live-pointer freeze or operation/request-budget overconstraint. No class-level runtime repair is prescribed. F001/F002 were also highlighted by the main worker after dispatch; this report evaluated the actual submitted lines rather than silently assuming they were corrected. F003 was independently identified from actual API fields. Current candidate remained unchanged during review.

## Substantive design assessment

### Meaning and signed controlled domain

Read original calculation brief in full, effective catalogue authority/index and D014 row, full version2 foundation and version3 SQLite briefs, full D012 and D013 briefs, accepted neutral-boundary/contract-classification decisions, root current checkpoints and section7 envelope. K02 fixes (bid_size-ask_size)/(bid_size+ask_size) and requires a nonzero denominator; P_BASIC does not provide a precision/rounding parameter. The effective D014 row binds R033/R036, no D predecessor, K02/P_BASIC and units text `-1 to 1`.

The proposed exact rational result avoids inventing rounding or silently refusing nonterminating ratios. For nonnegative inputs with nonzero sum, the difference is bounded by the sum; hence [-1,1]. For signed artificial finite-Decimal algebra the ratio can lie outside that interval, e.g. -3/1 yields2. Sections1/5 and contract explicitly distinguish that artificial arithmetic witness from physical negative displayed-size eligibility. The catalogue units text alone does not specify an input validator, and the preserved source README explicitly denies admitting workbook bounds as validation law. No accepted D014-specific positivity/integer/magnitude rule was found in the in-scope authorities. Do not invent one. Conversely, nothing in this review certifies signed quantities as physical/native displayed sizes.

The new source is explicitly foundation-size-fixture/cash_size_v1, with fixed shares identity conversion and controlled true-instant timestamps. It is not a production IBKR mapping. Native provider sentinels, size scaling, contracts, permissions, market-data state and event-time validity remain outside admission. This preserves source/profile holds rather than borrowing provider truth from a carrier type.

### Public compatibility, selection and configuration

Read complete actual M02 api.py, _selection.py, _rational.py and _sqlite.py, plus the M00 mapping/projection/history public declarations. Existing CalculationRequestV1/RawInputBindingV1/RawInputLineageV1 can carry this direct pair; the old D013 request cannot. A separate exact dataclass/facet, not subclass or old Decimal widening, is compatible with exact-type enforcement. All seven new read methods reproduce the old keyword/argument shapes with only occurrence return replacement. Fact parameter refs include parameter and selection; unit refs are unique/sorted; direct lineage and mapping snapshots retain R033/R036 order. Existing decoder already supports request/configuration/lineage nested types; one new exact dataclass allowlist entry is a bounded viable addition, without changing integer codec or D013 service.

Selection helper is not intrinsically price/R034-only: it compares the supplied mapping, policy and request. Exact new registrations can bind shares/R033/R036 without changing it or the old catalogue. Its actual code checks full pagination, duplicates before eligibility, exact Decimal representation/content, metadata, cutoff, freshness, rank ambiguity and page cap. New service must still enforce request/configuration admissibility, unit identity conversion, ordered bindings and pair skew, and independently validate stored facts. Independent lawful mapping/unit versions1/2 are explicitly allowed per binding, not an accidental same-version pair restriction. F003 is a documentary spelling defect only; the empty existing field is representable.

### Identity, storage and recovery

New namespace/prefix and exact brief digest prevent old authority/type/store substitution. Complete logical request/configuration/raw projection/native/canonical tuple content enters identity; calculated time is excluded, preserving original first fact/time on retry. Canonical signed rational integer text reuses existing ratio codec and avoids global integer-string-limit mutation. Recovery is required to recompute equation and eligibility, not merely trust rehashed payload/index/identity. No competing general formula framework is introduced.

The separate application_id0x4E560004/user_version1 profile, exact three STRICT tables/six immutable triggers, full typed/hash/index/logical/config validation, atomic registration, exclusive-create/path rules, independent transaction connections, read-only mode and truthful uncertainty mirror an implementable existing trusted-application pattern. New DDL/profile can be supplied in its own module without editing old store bytes. Reader needs only path/admission/IDs and must recover every registered configuration, not just dependencies of successful results. Cross-profile refusal and no migration are explicit. This is application ownership separation, not hostile-code/OS/database-role security.

### Proof/control design and recurrence

The six exact mandatory names bind P01-P06. Proposed obligations discriminate actual M00 producer integration from adapters, absence before admission from a prefilled fixture, first NEW insert from retry, independent corruption dimensions from one hash failure, individual lawful version changes from combined-only changes, and fresh typed reader recovery from caller re-registration. Support may provision literals only. Authored adequacy, immutable generation admission, intended RED and implementation/candidate review remain separate future stages; no actual authored proof was reviewed here.

Read initial and V2 D013 control reports, initial/revised authored-proof reports, implementation report, and primary Git repairs: 526cee6/3269035 and a31b71c..3876ad0. Prior immutable-generation versus live selected-pointer freeze, across-suite versus per-request budget, and first-write versus retry policy mechanisms were specifically examined. Current brief section8 protects immutable bytes while retaining lawful live advancement/revocation; section9 requires genuine first-write barriers and later retry without requiring retry to write. Future exact control diff/proof review still must exercise those distinctions. The current design does not reopen them merely by adding a third fixed descriptor.

Existing G01 source permits fixed D012/D013 descriptors with per-extension authority and global partition checks. The new bounded static addition is coherent with that structure; it does not require changing original _authority, runner/outcome/schema or old generation bytes. Null admission is not semantic RED, orphan support/nested Python/symlink ownership is global, and disposable fixture resets do not remove actual proof. Actual global ownership/proof-control execution remains future evidence.

## Documentary checks actually obtained

Read-only cat/sed/rg/nl/wc/find and Git status/rev-parse/diff/log/show were used. No repository modules were imported. Standard-library-only Python parsed raw JSON/Markdown/CSV and workbook ZIP/XML, not application/test code.

- HEAD/tree matched above; status --short was empty at entry and close-out. Diff1041de5..ec570da contains only root plan/execution-record checkpoints and the two D014 proposals, four files total; no D014 runtime/proof/control implementation.
- All eight explicit D014 incorporation-table raw SHA256s matched. Exact contract marker appears once and matches contract bytes. Six required proof IDs and six required test names match section9. These checks establish documentary association, not runtime schema/native validation.
- Exact D014 binding, descriptor/admission/generation directory, physical proof root and two runtime-module paths are absent. Existing api.py inspection contains no proposed new symbols.
- Workbook raw bytes match519ea9449297d564ae4a02afc1bf4e60e4471631c81a0842620f9fb60bb4f9ae. Independent ZIP/XML reading of Raw Signals rows37/40 confirms R033/R036, EWrapper.tickSize, tick0/3 and contracts/shares reference entries. Workbook timestamps/status labels are reference, not accepted provider mappings.
- Independently opened current official https://www.interactivebrokers.com/docs/tws-api/doc/md/streaming-data and https://www.interactivebrokers.com/docs/tws-api/doc/md/live-ticks through public web retrieval. Streaming page explicitly distinguishes watchlist aggregate snapshots from tick-by-tick; tickSize Python size is Decimal, and its callback remarks separately discuss scale. Tick-by-tick BidAsk has its own time and Decimal sizes. No callback/time/scale transposition is licensed. These facts support the proposal's cautious nonclaim, not negative quantity validity, chosen provider mapping or acquisition. No broker connection/provider data API/SDK acquisition was performed by this reviewer.

Private evidence companion: DOCUMENTARY_RESULTS.md. No executable runtime proof, source-wide typecheck/lint, native authority validator, product aggregate or architecture promotion was run. Prior D013 runtime results are read with their original attribution only.

## Decision boundary

Correct F001-F003 and submit exact new bytes for bounded follow-up review. No domain redesign, new provider investigation, runtime proof, implementation change or new owner prompt is required by these findings. Standing owner-chat/20261019T222804/D012-and-standing-human-exceptions permits later concrete delegated disposition, not fabricated review, missing domain facts or acceptance of currently unreviewed revised bytes. No D014 binding/control/proof/runtime admission, implementation acceptance, owner utterance, G6.1/full126/native acceptance or G6.2 progression follows from this report. Remaining122 foundation identities/all83 downstream outputs and source/profile/composition/transition/retirement/main holds remain as proposed boundaries, not completed work.
