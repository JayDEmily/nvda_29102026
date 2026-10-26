# D009 scoped static repair

Initial scoped mypy reported optional selection-identity access before narrowing in new D009 source. The value is now narrowed to a present identity before reading vintage.id; rejection semantics are unchanged. Original output retained. Repeat failed mypy scope, then initial scoped Ruff. No product runtime.

Initial Ruff reported style only: new reader line length, unused role enumeration, three proof line lengths, and additive export order. Each was wrapped/sorted without changing source selection or physical cases. The repaired proof hash/generation pointer were resealed. Repeat only failed Ruff scope; original output retained.
