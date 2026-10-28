# Fixed R2 cumulative-additive transfer baseline

Status: producer-side Git verification observed; independent tester acceptance/possession **NOT CONFIRMED**.

- Baseline source: independently reviewed L00 full-history checkpoint.
- BASE_SHA: `97f944d51ab9e403250fe76910e2754b50425c73`
- Baseline package: `NVDA_DOWNSTREAM_RECONCILIATION_L00_CHECKPOINT_20261028.tar(1).gz` (Library duplicate of original L00 checkpoint content).
- Baseline package SHA-256: `4d02c82894513bff8d07af7a2af6a151cd3f5f14ece581ac0bf0d87ea9ed0430`
- Contained bundle name: `NVDA_DOWNSTREAM_RECONCILIATION_L00_CHECKPOINT_20261028_FULL_HISTORY.bundle`
- Contained bundle SHA-256: `91db4a1989bff366c1f547c5776ca886c276b6b1310027ae929aa1cd1efee4b9`
- Starting branch: `work/downstream-reconciliation-20261028`
- Original M00 L06 ancestor: `9b400183f275c3147b568d21b995b4aebd2af3c3`.
- D143 evidence anchor: `17d7553cf3ad92700f849f696134de67b64b0dfa`.
- All tracked source, history, authoritative plans, M00 fixtures and retained proof generations are in the one-time **Git baseline bundle**. External/non-Git prerequisites (including the project wheelhouse and other unrelated archives) are not present in or implied by post-baseline additive bundles; if necessary at L14, exact identical assets must be provided separately.
- The file basename suffix `(1)` is the duplicate Library name, not a distinct Git revision. The SHA-256 identifies these exact bytes.

## Original bundle refs and tips

```text
97f944d51ab9e403250fe76910e2754b50425c73 refs/heads/work/downstream-reconciliation-20261028
2f933701978b8318c21d5df5a119836ad4a83ecc refs/heads/work/m00-brief2-execution-20261027
fa709f645ac5ac21b861836db74ab23da9f8e17a refs/recovered/draft/archive/l04-checkpoint/checkpoint-recovered/archive/d143-input/heads/work/v2-d131-clean-lineage-20261026
17d7553cf3ad92700f849f696134de67b64b0dfa refs/recovered/draft/archive/l04-checkpoint/checkpoint-recovered/archive/d143-input/heads/work/v2-d135-topone-amendment-20261027
fa709f645ac5ac21b861836db74ab23da9f8e17a refs/recovered/draft/archive/l04-checkpoint/checkpoint-recovered/archive/d143-input/heads/work/v2-d136-rejected-refusal-20261026
fa709f645ac5ac21b861836db74ab23da9f8e17a refs/recovered/draft/archive/l04-checkpoint/checkpoint-recovered/archive/d143-input/remotes/origin/HEAD
fa709f645ac5ac21b861836db74ab23da9f8e17a refs/recovered/draft/archive/l04-checkpoint/checkpoint-recovered/archive/d143-input/remotes/origin/work/v2-d131-clean-lineage-20261026
77471e5a851ec04e73c6dc63988868064de930f8 refs/recovered/draft/archive/l04-checkpoint/checkpoint-recovered/archive/d143-input/remotes/origin/work/v2-next20-d010-clean-lineage-20261026
8e0c89b2cdf4ef504931fea894d89b2f85b2ce2e refs/recovered/draft/archive/l04-checkpoint/checkpoint-recovered/archive/d143-input/remotes/origin/work/v2-next20-execution-20261026
d5706537d03801cca9caa9078952496c59fbf41d refs/recovered/draft/archive/l04-checkpoint/checkpoint-recovered/archive/d143-input/tags/checkpoint/d014-controlled-accepted-20261022
f0190af646378441b5eabfc3616c26b3fc46c252 refs/recovered/draft/archive/l04-checkpoint/checkpoint-recovered/archive/d143-input/tags/checkpoint/g4-research-20261021
5219004223e33291f1b831382e8427742e00427f refs/recovered/draft/archive/l04-checkpoint/checkpoint-recovered/heads/work/m00-brief2-execution-20261027
bc02a472eaa3a07c7f112dee48e5b1f6fa1764dc refs/recovered/draft/archive/l04-checkpoint/checkpoint-recovered/heads/work/m00-brief2-plan-20261027
17d7553cf3ad92700f849f696134de67b64b0dfa refs/recovered/draft/archive/l04-checkpoint/checkpoint-recovered/heads/work/v2-d135-topone-amendment-20261027
17d7553cf3ad92700f849f696134de67b64b0dfa refs/recovered/draft/archive/l04-checkpoint/checkpoint-recovered/remotes/origin/HEAD
fa709f645ac5ac21b861836db74ab23da9f8e17a refs/recovered/draft/archive/l04-checkpoint/checkpoint-recovered/remotes/origin/work/v2-d131-clean-lineage-20261026
17d7553cf3ad92700f849f696134de67b64b0dfa refs/recovered/draft/archive/l04-checkpoint/checkpoint-recovered/remotes/origin/work/v2-d135-topone-amendment-20261027
fa709f645ac5ac21b861836db74ab23da9f8e17a refs/recovered/draft/archive/l04-checkpoint/checkpoint-recovered/remotes/origin/work/v2-d136-rejected-refusal-20261026
d5706537d03801cca9caa9078952496c59fbf41d refs/recovered/draft/archive/l04-checkpoint/checkpoint-recovered/tags/checkpoint/d014-controlled-accepted-20261022
f0190af646378441b5eabfc3616c26b3fc46c252 refs/recovered/draft/archive/l04-checkpoint/checkpoint-recovered/tags/checkpoint/g4-research-20261021
b05577a3a87b3bc23279075ef052125b9cab8ab1 refs/recovered/draft/archive/l04-checkpoint/heads/work/m00-brief2-execution-20261027
5219004223e33291f1b831382e8427742e00427f refs/recovered/draft/archive/l04-checkpoint/remotes/origin/HEAD
5219004223e33291f1b831382e8427742e00427f refs/recovered/draft/archive/l04-checkpoint/remotes/origin/work/m00-brief2-execution-20261027
bc02a472eaa3a07c7f112dee48e5b1f6fa1764dc refs/recovered/draft/archive/l04-checkpoint/remotes/origin/work/m00-brief2-plan-20261027
17d7553cf3ad92700f849f696134de67b64b0dfa refs/recovered/draft/archive/l04-checkpoint/remotes/origin/work/v2-d135-topone-amendment-20261027
d5706537d03801cca9caa9078952496c59fbf41d refs/recovered/draft/archive/l04-checkpoint/tags/checkpoint/d014-controlled-accepted-20261022
f0190af646378441b5eabfc3616c26b3fc46c252 refs/recovered/draft/archive/l04-checkpoint/tags/checkpoint/g4-research-20261021
0c86b187a23e750d39ce04f772f7d52c1bd578b0 refs/recovered/draft/heads/work/m00-brief2-execution-20261027
b05577a3a87b3bc23279075ef052125b9cab8ab1 refs/recovered/draft/remotes/origin/HEAD
b05577a3a87b3bc23279075ef052125b9cab8ab1 refs/recovered/draft/remotes/origin/work/m00-brief2-execution-20261027
d5706537d03801cca9caa9078952496c59fbf41d refs/recovered/draft/tags/checkpoint/d014-controlled-accepted-20261022
f0190af646378441b5eabfc3616c26b3fc46c252 refs/recovered/draft/tags/checkpoint/g4-research-20261021
d14cb0102bfdf405bc157c7e4fa3e0d1714fb41a refs/recovered/heads/work/m00-brief2-execution-20261027
fa709f645ac5ac21b861836db74ab23da9f8e17a refs/recovered/recovered/checkpoint-recovered/archive/d143-input/heads/work/v2-d131-clean-lineage-20261026
17d7553cf3ad92700f849f696134de67b64b0dfa refs/recovered/recovered/checkpoint-recovered/archive/d143-input/heads/work/v2-d135-topone-amendment-20261027
fa709f645ac5ac21b861836db74ab23da9f8e17a refs/recovered/recovered/checkpoint-recovered/archive/d143-input/heads/work/v2-d136-rejected-refusal-20261026
fa709f645ac5ac21b861836db74ab23da9f8e17a refs/recovered/recovered/checkpoint-recovered/archive/d143-input/remotes/origin/HEAD
fa709f645ac5ac21b861836db74ab23da9f8e17a refs/recovered/recovered/checkpoint-recovered/archive/d143-input/remotes/origin/work/v2-d131-clean-lineage-20261026
77471e5a851ec04e73c6dc63988868064de930f8 refs/recovered/recovered/checkpoint-recovered/archive/d143-input/remotes/origin/work/v2-next20-d010-clean-lineage-20261026
8e0c89b2cdf4ef504931fea894d89b2f85b2ce2e refs/recovered/recovered/checkpoint-recovered/archive/d143-input/remotes/origin/work/v2-next20-execution-20261026
d5706537d03801cca9caa9078952496c59fbf41d refs/recovered/recovered/checkpoint-recovered/archive/d143-input/tags/checkpoint/d014-controlled-accepted-20261022
f0190af646378441b5eabfc3616c26b3fc46c252 refs/recovered/recovered/checkpoint-recovered/archive/d143-input/tags/checkpoint/g4-research-20261021
5219004223e33291f1b831382e8427742e00427f refs/recovered/recovered/checkpoint-recovered/heads/work/m00-brief2-execution-20261027
bc02a472eaa3a07c7f112dee48e5b1f6fa1764dc refs/recovered/recovered/checkpoint-recovered/heads/work/m00-brief2-plan-20261027
17d7553cf3ad92700f849f696134de67b64b0dfa refs/recovered/recovered/checkpoint-recovered/heads/work/v2-d135-topone-amendment-20261027
17d7553cf3ad92700f849f696134de67b64b0dfa refs/recovered/recovered/checkpoint-recovered/remotes/origin/HEAD
fa709f645ac5ac21b861836db74ab23da9f8e17a refs/recovered/recovered/checkpoint-recovered/remotes/origin/work/v2-d131-clean-lineage-20261026
17d7553cf3ad92700f849f696134de67b64b0dfa refs/recovered/recovered/checkpoint-recovered/remotes/origin/work/v2-d135-topone-amendment-20261027
fa709f645ac5ac21b861836db74ab23da9f8e17a refs/recovered/recovered/checkpoint-recovered/remotes/origin/work/v2-d136-rejected-refusal-20261026
d5706537d03801cca9caa9078952496c59fbf41d refs/recovered/recovered/checkpoint-recovered/tags/checkpoint/d014-controlled-accepted-20261022
f0190af646378441b5eabfc3616c26b3fc46c252 refs/recovered/recovered/checkpoint-recovered/tags/checkpoint/g4-research-20261021
b05577a3a87b3bc23279075ef052125b9cab8ab1 refs/recovered/recovered/heads/work/m00-brief2-execution-20261027
5219004223e33291f1b831382e8427742e00427f refs/recovered/recovered/remotes/origin/HEAD
5219004223e33291f1b831382e8427742e00427f refs/recovered/recovered/remotes/origin/work/m00-brief2-execution-20261027
bc02a472eaa3a07c7f112dee48e5b1f6fa1764dc refs/recovered/recovered/remotes/origin/work/m00-brief2-plan-20261027
17d7553cf3ad92700f849f696134de67b64b0dfa refs/recovered/recovered/remotes/origin/work/v2-d135-topone-amendment-20261027
d5706537d03801cca9caa9078952496c59fbf41d refs/recovered/recovered/tags/checkpoint/d014-controlled-accepted-20261022
f0190af646378441b5eabfc3616c26b3fc46c252 refs/recovered/recovered/tags/checkpoint/g4-research-20261021
b05577a3a87b3bc23279075ef052125b9cab8ab1 refs/recovered/remotes/origin/HEAD
b05577a3a87b3bc23279075ef052125b9cab8ab1 refs/recovered/remotes/origin/work/m00-brief2-execution-20261027
d5706537d03801cca9caa9078952496c59fbf41d refs/recovered/tags/checkpoint/d014-controlled-accepted-20261022
f0190af646378441b5eabfc3616c26b3fc46c252 refs/recovered/tags/checkpoint/g4-research-20261021
d14cb0102bfdf405bc157c7e4fa3e0d1714fb41a refs/remotes/origin/HEAD
d14cb0102bfdf405bc157c7e4fa3e0d1714fb41a refs/remotes/origin/work/m00-brief2-execution-20261027
d5706537d03801cca9caa9078952496c59fbf41d refs/tags/checkpoint/d014-controlled-accepted-20261022
f0190af646378441b5eabfc3616c26b3fc46c252 refs/tags/checkpoint/g4-research-20261021
97f944d51ab9e403250fe76910e2754b50425c73 HEAD
```

## Recovery contract

1. Once only, restore the exact L00 archive/bundle and verify `BASE_SHA`, SHA-256 and required refs/tips, `git fsck --full`.
2. For each handover, fetch the **latest only** cumulative additive bundle that declares `BASE_SHA` as prerequisite.
3. Verify the updated branch HEAD, worktree tree SHA and refs against the handover. Keep the original L00 baseline intact and never rewrite history.
4. This source thread can verify a fresh local restoration, but cannot establish that a separate tester thread already possesses the exact baseline. Until the tester confirms that state, classify transfer as **CONDITIONAL / NOT YET CONFIRMED AT RECEIVER**.
