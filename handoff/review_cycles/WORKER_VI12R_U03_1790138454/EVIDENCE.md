# Worker evidence

**Status:** `COMPLETE`

## Source transport

- received filename: `NVDA_G03_TESTER_VI13R_U02_R024_1790131803_FULL_GIT_20260923.tar(3).gz`
- received SHA-256: `9270587eee6236fdf077887d67cf9cfd1a656b7931831910cc93425fb7fe6649`

## U02 promotion

- previous forward `main`: `b806447eb440a016826728af075e714beee23d31`
- accepted U02: `5c62ec5147da718297b251b5a287405ebf3b4755`
- Reviewer-024 PASS: `df45c5e93e7c4c19cb1cca75de5cd1c64b15537c`
- promoted forward `main`: `a78ae7b5515c2e482a2656cebeebae3fa5a6d584`
- both required commits verified as ancestors of promoted `main`
- clean worktree and `git fsck --full --strict`: pass

## U03 candidate

- branch: `work/vi12r-u03-observation-fidelity`
- commit: `7cf8936f854fbed952a468ce06c2f2a0320d9291`
- tree: `b63aac7fb538ea6a38ce3dea5aab719fc7be0ee0`
- changed production path: `src/nvda_desk/raw_signal_occurrence_truth/api.py`
- candidate diff SHA-256: `91f20c62a03884aae9a666c105a91a4477ad66257e1ad00ffc50cba9046fb8ff`

## Exact committed validation

- Python 3.13.5
- pytest 9.0.3
- mypy 1.20.1 compiled
- Ruff 0.15.11
- focused U01+U02+U03: 366 passed
- mypy source: success, 15 files
- Ruff source: pass
- product proof control: pass, 6 families / 13 of 13 obligations
- public seam: pass
- architecture structural validation: pass, 0 dependency/public-seam violations
- architecture/bootstrap: 74 passed
- architecture promotion: 74 passed
- diff check / strict Git integrity / clean committed worktree: pass

See `implementation/proof/VI12R_U03_IMPLEMENTATION_EVIDENCE.md` for the bounded semantic statement.
