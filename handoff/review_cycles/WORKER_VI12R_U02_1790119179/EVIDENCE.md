# Worker cycle evidence

**Status:** `COMPLETE`

- source tester TAR SHA-256: `58d5c862bf7ee6765c0e0dfa7942c2ea5c195654e179157d816b7c04e654fa81`;
- source returned HEAD: `b806447eb440a016826728af075e714beee23d31`;
- forward `main` before promotion: `95c0aeabf3b76316bd32870ffe6c311be8ad1237`;
- forward `main` after fast-forward promotion: `b806447eb440a016826728af075e714beee23d31`;
- accepted U01 `e8b659d...` and Reviewer-022 PASS `4db58e9...` verified ancestors of promoted `main`;
- U02 candidate: `a77dc596b7cbc3f248097df94d8dd0bef4491bec` / tree
  `1b8672a851f63c1bab8da02fb75de8357e4fad3c`;
- production changed path: `src/nvda_desk/raw_signal_occurrence_truth/api.py` only;
- exact focused product result: `326 passed`;
- exact architecture/bootstrap and promotion result: `74 passed`;
- exact source mypy/Ruff, product-control, public-seam, structural architecture, diff and Git
  integrity checks: pass.

The first promotion preflight compared the returned wrapper against an incorrectly guessed expanded
SHA for its short `b806447` identity and stopped before mutation. The returned repository was then
inspected directly, establishing exact HEAD `b806447eb440a016826728af075e714beee23d31`; the lawful
fast-forward promotion was executed only after that exact identity and required ancestry were
verified.
