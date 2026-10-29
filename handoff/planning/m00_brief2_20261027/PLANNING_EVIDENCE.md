# Planning evidence and inspection limits

## Inputs and source

- Starting Git `17d7553cf3ad92700f849f696134de67b64b0dfa`.
- Input bundle `NVDA_V2_D143_ACCEPTED_FULL_HISTORY_20261027(3).bundle`, SHA-256 `ce1101aebc08f0ead1315a462418d61ff62d92759711ab90f2920c08618558cf`.
- Attachment tarball SHA-256 `5a69ded8e5c14c09ff65c649a96f534d1fb161bc51e30970d9908050439211d7`.
- Brief raw bytes SHA-256 `0d5ee211c1285b31834062ab2d871670ed2f318cbb955e7df95f80067d562007`.
- Preserved paused root plan SHA-256 `2d95d7c5e425ed1dd231f4685100f7c1db9c85ee1369fea54f91580aab6caa5a`.
- Frozen guardrails SHA-256 `585dc9b1a95719a7b60929b0d3ea64696fd6d52cd19b2b4a463c5bb9d34947b6` unchanged.

`git bundle verify` reported the input bundle okay and complete history. A clone was checked out at the exact HEAD, on `work/m00-brief2-plan-20261027`. All supplied non-HEAD refs were additionally fetched to `refs/archive/d143-input/*`, including remote-only/rejected branch tips, so a later --all bundle preserves those object histories. Source Git log for M00 shows D139's collector receipt type change at `6d6654e8c53f3a323a3b4887439259cbc7affde5`; this establishes source ancestry, not original M00 acceptance/freeze. L00 must trace complete accepted baseline and exact proof impact.

## Scope of direct inspection

Full governance and brief reads and partial source/test reads are enumerated in root plan §2. Full read of the SQLite physical brief is not an audit of every document it incorporates. Full read of the SQLite addendum is not full inspection of its inherited PA-02 implementation. Those closure/ingress questions are future L00 work and cannot be labelled resolved by the planning receipt.

Read D143's `handoff/foundation_implementation/d143_execution/INDEPENDENT_ACCEPTANCE.md` and `strict-green.log` in full. The log records historical Python3.12.14, exactly two tests passed, aggregate exit0, candidate317720d. No re-execution occurred; no new D143 validation or native certification follows. Root old plan §26 makes D145 the next scheduled signal, which is now paused by owner instruction.

Read-only external source check: official IBKR legacy market-depth documentation confirms qualified MPID/exchange distinction; error-code and tick-type references were opened. These legacy pages state they are deprecated and direct readers to current IBKR documentation. This source check neither certifies a current SDK version nor live feed availability. Future implementation must recheck current official version-relevant material. Reference URLs:

- https://interactivebrokers.github.io/tws-api/market_depth.html
- https://interactivebrokers.github.io/tws-api/message_codes.html
- https://interactivebrokers.github.io/tws-api/tick_types.html

## Recovery/verification notes

Initial extraction returned a tar ownership-restoration error after writing the one brief file; no Git operation chained after that failed extraction ran. The extracted brief bytes were read in full and hashed; packaging verification will independently compare those bytes with the original tar member. The error did not authorise ignoring an integrity check. No product behaviour was executed to compensate.

Planning writes are confined to root plan, narrow AGENTS scope notices and the planning handoff directory. No source, proof tests, old immutable generations, acceptance binding, dependency pins or GUARDRAILS change. Product/environment checks are NOT_ATTEMPTED; documentary and Git/archive integrity checks are distinct.
