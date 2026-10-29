# D005 scoped static repair

Initial scoped mypy reported that a one-element inferred tuple variable could not be assigned the two-element version1 phase sequence. The source now annotates a variadic tuple of PhaseIntervalV1; no phase content or ordering changed. Original output retained; repeat the failed mypy scope before candidate. No product runtime.

Initial Ruff reported tuple concatenation on the same ordered phase sequence and unsorted additive API exports. Both exact tuples use iterable unpacking with the same order, exports sorted; the physical proof hash and generation were resealed. Repeat failed Ruff scope only. Original output retained.
