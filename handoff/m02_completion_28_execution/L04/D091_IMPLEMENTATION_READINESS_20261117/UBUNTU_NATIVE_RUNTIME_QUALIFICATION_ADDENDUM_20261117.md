# Ubuntu-native CPython/SQLite qualification — corrected linkage diagnosis

**Status: DIRECT NON-PRODUCT DIAGNOSIS; NO PRODUCT RUNNER RELEASE.** This addendum is **additional evidence**, not a rewrite of the earlier failed preflight `NONPRODUCT_RUNTIME_PREFLIGHT_FAILURE.json`. It leaves the owner-approved 18 D091 and separate 15 L01b finite admissions, execution holds, source/contract identities, claim/generation holds, and paused D145 unchanged.

## Directly observed, 17 November 2026

We loaded two *different* SQLite implementations on the authorised Windows/WSL Ubuntu host.

| Measured subject / method | Observed |
| --- | --- |
| Existing CPython | 3.13.5, executable `/home/jds/.local/bin/python3.13` |
| Python `import _sqlite3`; `_sqlite3.__spec__.origin` | `built-in` |
| Python `_sqlite3.__file__` | **Absent** |
| Python `sqlite3.sqlite_version` | **3.49.1** |
| Python `SELECT sqlite_source_id()` on a new **in-memory** connection | `2025-02-18 13:38:58 873d4e274b4988d260ba8354a9718324a1c26187a4ab4c1cc0227c03d0f10e70` |
| Isolated official-source-compiled `libsqlite3.so.0` via `ctypes.CDLL` | **3.54.1** |
| Independent library `sqlite3_sourceid()` through `ctypes` | `2026-10-16 14:45:20 555e07ef33f69a0957d24d8e555b702464a131d6f1607f4c3c1e4551e8e6ca76` |
| New Ubuntu library SHA-256 | `44a469c2ed17ee19dca5f0c949f97b98b7ad0f1260bdb41fc153a4530324fb2f` |
| Historical earlier library SHA-256 | `c53706980906943301153b630aeddba1b4aab6fe5eeda5752d8293952707db4e` |

**Mechanism:** the current Python interpreter's `_sqlite3` is a **built-in** module with its own SQLite 3.49.1. It is not a dynamic extension that would pick up an arbitrary `libsqlite3.so.0` from `LD_LIBRARY_PATH`. Separately, the **new library itself** correctly identifies as SQLite 3.54.1 with the originally recorded SQLite source ID. Thus the native library can be loaded, but it is *not the interpreter's active sqlite3 engine*. The prior probe's `AttributeError: module '_sqlite3' has no attribute '__file__'` is explained by that built-in module form; it does **not** demonstrate failure of SQLite 3.54.1 features. Both the failed probe and exact historical-binary mismatch remain recorded as observed failures, not silently promoted to PASS.

Astral's upstream documentation explains that standalone Python distributions may embed their dependencies and modules: https://github.com/astral-sh/python-build-standalone/blob/main/docs/technotes.rst . This provides a mechanism explanation, **not** independent verification of which distributor built the current local interpreter.

The original source archive from `https://sqlite.org/2026/sqlite-autoconf-3540100.tar.gz` passed both the recorded SHA-256 and SHA3-256 checks; its `sqlite3.c` SHA3 also matched. The compiled binary does *not* match the earlier binary built in a different GCC 14.2 environment: the current host's GCC is 15.2. Since two compilers/toolchain environments differ, **byte-identical executable output cannot be assumed**; the exact causal contribution of GCC to the hash mismatch was *not* experimentally isolated. A historical-byte-identity recovery goal is distinct from establishing a new qualified target runtime.

See `LOCAL_SQLITE_BINDING_DIAGNOSTIC_20261117.json` (complete direct observation and source IDs) and `NONPRODUCT_RUNTIME_PREFLIGHT_FAILURE.json` (original failed build/probe record).

## Correct Ubuntu-native next qualification (proposal, not already performed)

1. Preserve the programme's pinned **CPython 3.13.5** and **SQLite 3.54.1**, not arbitrarily upgrade to the latest Python or SQLite and pretend equivalence. Official CPython 3.13.5 source is available at https://www.python.org/downloads/release/python-3135/ ; SQLite publishes its amalgamation compilation procedure at https://www.sqlite.org/howtocompile.html .
2. Establish an **isolated user-owned Ubuntu runtime prefix** with dependencies sourced from the Ubuntu repositories and/or verified upstream releases, including the C build toolchain, Python extension headers, OpenSSL and the exact verified SQLite amalgamation. **Pin package/source versions and hashes**; do not replace system Python/SQLite or existing evidence. Python documents supported prefix and build configuration: https://docs.python.org/3.13/using/configure.html .
3. Build/install that **exact Python 3.13.5** runtime against the **exact SQLite 3.54.1** headers/library, ensuring its `_sqlite3` module actually links to or incorporates the intended version. A new dynamically linked Python `_sqlite3` could use a private library path, but the exact build architecture must be proved by readback, not asserted from a configure flag.
4. Record the **selected interpreter SHA-256**, `sys.version` and `sys.executable`, `_sqlite3` origin/path or native static-link evidence, the **actual interpreter-reported** `sqlite3.sqlite_version`, **actual `SELECT sqlite_source_id()`**, loaded library/source/hash where dynamically linked, SQLite compile options and exact Python package/lock versions.
5. Run only the **approved bounded non-product SQLite feature/rollback/read-only-reopen qualification** against *that exact interpreter*. For any required evidence check that cannot apply to a built-in `_sqlite3`, preserve the original result as failed/inapplicable and obtain an **independently accepted equivalent inspection contract**; never silently swap probes and describe them as equivalent.
6. Separately confirm the actual strict product Tester runner, L00 receiver and remaining product claim/generation/source binding, and independently release the admitted cases before product execution. A successful library smoke check would not itself authorise a product test.

**Local Ubuntu development-package observation:** `make` and `gcc` are available; `pkg-config`, `/usr/include/sqlite3.h` and `/usr/include/openssl/ssl.h` were not found at the checked paths. Their Ubuntu build prerequisites should be obtained/qualified in the isolated setup before attempting a complete CPython build; the *absence at those paths* is not proof that no usable alternative exists.

## Decision relevance

The owner has stated a preference for obtaining suitable verified packages and dependencies online while using Ubuntu. This preference does not itself modify the previously approved Python/SQLite version pins or retrospectively release product execution. The independent reviewer should assess **actual installed-plan runtime acceptance conditions**, not impose historical GCC14 **binary-hash equality** as a new target unless the governing requirement demonstrably makes that particular binary immutable. Product implementation, strict product testing and D145 remain outside this non-product diagnostic.
