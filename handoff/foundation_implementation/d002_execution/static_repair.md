# D002 scoped static repair

Initial scoped mypy passed on three changed production files. Initial scoped Ruff failed E501 at `_temporal_age.py:293` (102 > 100), before any runtime product proof. The line was split into a parenthesised condition, leaving the validation expression and behaviour intact. The original `ruff_initial.log` is retained. Repeat only the failed Ruff check on its original file set after this material source repair; mypy success remains valid because typing semantics did not change.
