# D003 scoped static repair

Initial mypy passed on the three changed production files. Initial Ruff reported three E501 line lengths in the new D003 source/proof, before product runtime. Only those expressions were wrapped; the physical proof file hash and immutable generation/pointer were resealed to the repaired proof bytes. Original Ruff output is retained. Repeat the failed Ruff scope; successful mypy remains valid because typing semantics are unchanged.
