# D086 first-stage implementation candidate and independent review commission

Disposition: IMPLEMENTED_UNTESTED. No product acceptance, registration, execution, release, policy or ledger change.

## Exact candidate
- Input handoff: `8b2be76fc0e48e726b0ca947511b4cb4bb851754` (fetched branch HEAD exact).
- Source-only candidate: `e7b05ba02b0ec0233b75e8f2c49447bd83947969`; tree `fec4fcd2c77e1139fb4fac1407cc8cdaf1668b2c`.
- Full recursive NUL-delimited git ls-tree SHA256: `c4128e8d0c419e2ace167be1779a5f83ce6e62f8cd881d23e5c3b52e9927550d`; 4596 entries.
- Five changed source paths (SHA256):
  - `src/nvda_desk/market_measurement_truth/api.py`: `43672c8bb5799213e9889411d24292d8ee7c187df894a58e69b8242b45843ffe`
  - `src/nvda_desk/market_measurement_truth/_option_time_source.py`: `e604c631992ce451ed245f5c89fac03206edeb11fb5f7eb35b59a56215c262eb`
  - `src/nvda_desk/market_measurement_truth/_option_time.py`: `45873493c22e7a27417866a69e6368502704f9410ca23d5c072e1737a3c0f5f6`
  - `src/nvda_desk/market_measurement_truth/_option_time_codec.py`: `cc8f9a88bf81b078ce0deddbaff6283d417d5f253c1ec3c0e3f0fa8269dd9caf`
  - `tools/product_proof_claims.py`: `642b35c0f53e7cf78f80ec70125245c0f59567fed2ec687a2eec07d802a24a16`

## Authority and scope
Verified exact committed authority bytes before editing:
- `handoff/m02_completion_28_execution/L07a/D086_FIRST_STAGE_SOURCE_IMPLEMENTATION_COMMISSION_20261128.md`: `6b920accfd0c6e63e29351e150235b7f2eae99927cb17dab7ab210cb817eef45`
- `handoff/m02_completion_28_execution/L07a/D086_IMPLEMENTATION_BRIEF.md`: `e5747d9ba697d16281e09c115db932a60f559c03937f243be06f7c01d107b676`
- `implementation/authority/T01_D086_OPTION_TIME_AUTHORITY_BINDING.yaml`: `9ccd773c689bf24e443cd23ebba534b637781dda48fb9377bf23d32718889b97`
- `handoff/m02_completion_28_execution/L07a/D086_TEST_SOURCE.py`: `1cade586e955ec08480ddac3c0a65cde352a28629d02c857c846b41b04f7295c`
- `handoff/m02_completion_28_execution/L07a/D086_PROOF_CONTRACT.json`: `f150caf2da222ca9396fc0734e20f8393244cdf5c05e33ab9111432802f501e3`
- `handoff/m02_completion_28_execution/L07a/OPTION_TIME_CONTRACT_AND_REVIEW_20261127.md`: `48d0a8f9533c8781a11b678a440e0874f6bfac76f49f028a1050e39f4ba3b133`
- `handoff/m02_completion_28_execution/L07a/OPTION_TIME_SOURCE_POLICY_AND_SPECIMENS_PROPOSED_20261127.json`: `14a3ba2308f519d90d11eb450ac484a2c922507b7e04041c740297527a1d847a`
- `handoff/m02_completion_28_execution/L07a/OPTION_TIME_FINITE_CASES_PROPOSED_20261127.json`: `638f8703e75c15b10c2e3772ef7a8ceb0a105a6845140d0e409d50c9a1f01c7f`
- `handoff/m02_completion_28_execution/OWNER_CONSOLIDATED_64_CONDITIONAL_EXECUTION_GRANT_20261127.json`: `6a71f52981fc01da42f9c27726547d0d1ddd69851561479a007aeb30ebd95a41`
- `handoff/m02_completion_28_execution/L01a/G01_PARTITION_REMAP_20261128/PATH_ONLY_SUCCESSOR_AUTHORITY.json`: `11d90adf234d5195d3bd31a6b42df9b046c4ad53690cb279ef071d52b3049aa7`
- `handoff/m02_completion_28_execution/TEST_EVIDENCE_LEDGER.json`: `5d1ac21a0cf62fe98efe5d4bd5c510094d139e6ae6bd3fc85d10924d67189c89`

Independently accepted prerequisites rechecked against exact remote review refs and report bytes: D003/D086 authoring 69e7db0bb6e6c9c318d2b7422fafa3cf6c14e795; D003 shared-surface clearance bec4d7c1e3e195348b238ca18a85c1df2e2f51d3; D003 registration installation 3e2543da0b2f3a8a49f2f108dcdccc9b533f3eca; D001 revised implementation b471fd0becf45755313cf268856f7ffcb0b1d0b9; D001 generation 0002 installation ee0d37bb8f264bd17d6777d94724f6748de079b9. Pre-edit five source paths exactly match reviewed D003 source 731f23d3457607c9b2fb7fc332d0edfe56635142. D001 generation 0002 and admission pointer unchanged.

## Implementation
- Separate exact typed OptionTimeExpiry occurrence, owner/read/source API; reuse sealed option-time ingress and existing immutable storage mechanism without altering prior implementations. Own brief/binding pins and exact admission. Validate complete seven-role permitted roster and exact R002/R003/R013 correspondence, full D001 parent via ordinary read-only storage, subject/frame/event and knowledge-time visibility. R013 actual native date and contract identity must agree with adopted policy and selected subject; configured expiry date, local time, zone and UTC instant must agree. Reject wrong parent, date mismatch, contract mismatch and negative elapsed time. Use integer elapsed microseconds divided by 31536000000000, reduced exact ratio; zero valid.
- Separate canonical codec includes full nested D001 parent and exact ratio; child identity excludes only its own ID and first calculation timestamp. Existing store replay mechanism retains first calculation and read-only reopen.
- Fixed dormant G01 prospective route descriptor derived in memory from exact contract and remap, SHA256 `cd4df62107c7f244e6a4238fce5935d15770355d2c73120d6a99b261a9e8bd01`; no descriptor, generation, admission pointer, physical proof or active registration installed.
- All four M02 source files preserve prior bytes as exact prefixes; G01 registry reverts byte-exactly to predecessor by removing only the inserted tuple. No change to existing D001/D003/D095 implementation or registration bytes; independent candidate-specific applicability remains required.

## Worker verification and limits
- Python AST parse and compile (no execution), exact source scope/diff check, prefix/tuple checks, carrier field and six inert test-node correspondence pass. Literal-only arithmetic independent of product/proof imports: MAIN 604807/252288000, AT_EXPIRY 0/1, AFTER -1972801/252288000; date/contract mismatch and earlier-parent cases retain their independently specified invariant/positive-arithmetic distinctions. Fifteen seven-role specimen hashes reconciled.
- Scoped Ruff 0.15.11 and mypy 1.20.1: new diagnostics corrected in added code only. Remaining three Ruff and five mypy diagnostics are unchanged pre-existing api.py findings (E402 2594, I001 2666, E501 2727; ScalarStraddleSourceV1 attr-defined 2873, 2877, 2881, 2886, 2896). No clean-lint/typecheck claim.
- Exact grant/remap/ledger reconciliation: 17 allocations, 64 original reviewed case objects, exact ordered original/remapped nodes, ceilings and all execution flags false, no runs, NOT_ATTEMPTED. All hold, policy, proof, existing registration and ledger files unchanged.
- Existing Ubuntu Git object store with fresh detached worktree: 2281 historical contextual ref rows, 797 name/tip pairs, 66 original rows, 170 distinct required objects and expected types; git fsck --full --no-reflogs --no-dangling exited zero. 21 wheel sizes/hashes verified; inherited 66 VERIFIED, 5 BLOCKED, 1 UNKNOWN non-Git asset dispositions unchanged. No fresh independent receiver restoration or new external asset restoration claimed. Initial shell quoting and text-substitution attempts corrected without governed changes.

## Fresh distinct independent reviewer
Fetch exact published handoff (direct child of source candidate `e7b05ba02b0ec0233b75e8f2c49447bd83947969`); stop on mismatch. Follow AGENTS.md, GUARDRAILS.md, EXEC_PLAN.md, tests/AGENTS.override.md and execution register. Independently assess exact candidate against commissioned authority, brief/binding, inert proof and proof contract, including ordinary actual D001 ingress, complete roster and R013 contract/date join, exact expiry/time arithmetic, refusal boundaries, canonical identity/durable reconstruction, and dormant G01 route. Review candidate-specific shared-surface applicability/invalidation of D001 generation 0002, D003, D095 and G01 independently; preserve prior evidence unless exact material invalidation established. No product or proof imports, collection, execution, registration, release, policy/ledger changes or source/proof edits. Publish separate documentary verdict on `refs/heads/review/trial-cac-nvidia-d086-implementation-20261128` at `handoff/m02_completion_28_execution/L07a/INDEPENDENT_D086_IMPLEMENTATION_APPLICABILITY_VERDICT_20261128.md` with exact candidate and dispositions.
If accepted, reconcile and commission only the eligible next distinct-role bounded registration-preparation Worker under existing authority. If returned or blocked, preserve first unmet invariant and route the bounded correction. Actual D001 product acceptance and candidate-specific sole Tester intake/runtime/precall remain mandatory before any child execution. All 64 holds, D004/D085 held, D145 PAUSED, G01 R2 unadopted, main/original and sole designated Tester preserved. Continue eligible distinct-role succession once via owner-adopted CAC MVP.
