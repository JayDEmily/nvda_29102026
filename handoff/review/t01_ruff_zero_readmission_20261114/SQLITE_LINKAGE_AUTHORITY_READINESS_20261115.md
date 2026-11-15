# T01 runtime qualification — SQLite linkage is interpreter-specific

**Date:** 15 November 2026 (Melbourne). **Scope:** read-only investigation of an independent downstream prerequisite; not a product-proof run, no installed runtime change, no altered admission.

## Direct source and runtime evidence

Executed `READONLY_SQLITE_LINKAGE.py` under two already-installed Ubuntu interpreters. Raw, reproducible outputs are retained next to this report:

| Observation | T01 selected managed interpreter | Ubuntu system interpreter |
|---|---|---|
| Executable | `/home/jds/nvda_uv3135_20261112/.venv/bin/python` | `/usr/bin/python3` |
| Python version | `3.13.5` | `3.14.4` |
| `sqlite3.sqlite_version` | **3.49.1** | **3.46.1** |
| `_sqlite3.__spec__.origin` | **built-in** | `/usr/lib/python3.14/lib-dynload/_sqlite3.cpython-314-x86_64-linux-gnu.so` |
| `_sqlite3` in `sys.builtin_module_names` | **true** | **false** |
| `ldd` of Python binary | No `libsqlite3.so.0` dependency shown | No `libsqlite3.so.0` dependency shown on Python executable; the separate `_sqlite3` extension links it |
| `ldd` of separate `_sqlite3` extension | Not applicable; no extension file | Links `/usr/lib/x86_64-linux-gnu/libsqlite3.so.0` |

A direct `ctypes.CDLL("libsqlite3.so.0")`/`sqlite3_libversion()` call in either interpreter returns **3.46.1** for the current system shared library. This is a **different SQLite library/version** from the managed Python 3.13.5 module's built-in reported **3.49.1**.

The selected Python 3.13.5 script was rerun; the second output was byte-identical after normalising non-semantic loader address values. We did not change `LD_LIBRARY_PATH`, install packages, replace system libraries or execute any product test.

## Mechanism and consequence

The selected managed Python 3.13.5 build exposes `_sqlite3` as a **built-in module**, not the dynamically loaded `_sqlite3*.so` extension that the system Python 3.14.4 uses. Its reported SQLite version **3.49.1** is independent of the system shared library's observed **3.46.1**. Therefore **simply changing the system `libsqlite3.so.0` is not an evidenced route for qualifying the selected managed interpreter**. No tested `LD_LIBRARY_PATH` workaround or proof of equivalent behaviour is available.

This observation does **not** establish a production failure, prove SQLite ABI incompatibility, or rule out all possible separately qualified runtime builds. It does eliminate the assumption that the installed system shared library's version describes the selected T01 Python `sqlite3` module.

Historical seven-claim proof contracts explicitly bind **CPython 3.12.14 / SQLite 3.53.1**. The later **proposed** T01 successor plan calls for owner-selected CPython 3.13.5 with separately qualified SQLite, including a proposed 3.54.1 target; that proposal is **not** the active root `EXEC_PLAN.md`. Neither the currently observed selected **3.13.5/3.49.1** nor the system **3.14.4/3.46.1** was demonstrated to meet the exact historical proof environment.

## Gate disposition

- **First blocker remains genuine programme admission authority** for the pilot generation 5 and six D030/D031/D032/D033/D035/D036 generation 3 successors, per the separately accepted 7/7 source-adequacy review. No active admission pointer advanced.
- **Later independent runtime gate remains unqualified**. Its solution requires a genuinely accepted runtime choice and relevant compatibility evidence, rather than inferring from the version of a different shared library. This task does not authorise installing a new interpreter or changing proof expectations.
- **No product proof, architecture promotion, new generation, main merge or D145 activation** occurred in this investigation.

**Reproducibility:** `/home/jds/nvda_uv3135_20261112/.venv/bin/python READONLY_SQLITE_LINKAGE.py` and `/usr/bin/python3 READONLY_SQLITE_LINKAGE.py`, with the working directory being this handoff folder. File paths and output are exact receipts from the current Ubuntu host, not universal hardware claims.
