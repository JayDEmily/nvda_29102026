# D004 scoped static repair

Initial scoped mypy passed on three changed production sources. Initial scoped Ruff reported one line length in new D004 reader and unsorted additive API exports. The expression was line-wrapped and the same export names sorted; semantics and physical proof bytes did not change. Original Ruff output retained. Repeat only failed Ruff scope; mypy's typing result remains valid.
