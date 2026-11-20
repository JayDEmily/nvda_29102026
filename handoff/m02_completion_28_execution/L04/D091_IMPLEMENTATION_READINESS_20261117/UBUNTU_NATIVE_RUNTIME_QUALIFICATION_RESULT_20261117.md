# Ubuntu-native CPython 3.13.5 / SQLite 3.54.1 — completed non-product runtime qualification

**Result: PASS for the exact bounded non-product build, linkage and SQLite mechanism checks. NOT a NVIDIA product-test acceptance, independent Tester receiver or authorisation to execute the 18 D091 + 15 L01b cases.**

**Source candidate before runtime-only work:** `b62f9f55e277cdaf22a952a38aad8e1bf835f7d2`. Work remained on draft PR #27's existing `work/t01-d091-finite-adequacy-20261116` branch; only these documentary/procedure receipts were added. No root governance, source/fixture, active proof ledgers, product code/tests, system Python or system SQLite changed.

## Observed final runtime and concrete identity

- Exact locally installed interpreter: `/home/jds/nvda_python3135_sqlite3541_20261117/python/bin/python3.13`, CPython **3.13.5**; interpreter SHA256 `d114ec20c65fb65c77608f7b8b7110d0ff95e3b3c814f65580dad17fb56e012c`.
- Official upstream CPython 3.13.5 tarball: `https://www.python.org/ftp/python/3.13.5/Python-3.13.5.tar.xz` (https://www.python.org/downloads/release/python-3135/), **downloaded and SHA256 recorded `93e583f243454e6e9e4588ca2c2662206ad961659863277afcdb96801647d640`**. A separately authenticated signature verification was not performed; do not infer one.
- Official SQLite 3.54.1 tarball: `https://sqlite.org/2026/sqlite-autoconf-3540100.tar.gz` SHA256 `926ef8d3eab93fbf6e06011901273eec076b25594a4e1cdadd50c987f4f6d64e`, also independently matched archived SHA3 hashes and source `sqlite3.c` SHA3. New private shared library SHA256 `44a469c2ed17ee19dca5f0c949f97b98b7ad0f1260bdb41fc153a4530324fb2f`, at `/home/jds/nvda_python3135_sqlite3541_20261117/sqlite/lib/libsqlite3.so.0`.
- Actual `_sqlite3` extension is a **dynamically inspectable file** (unlike the prior standalone Python built-in). `ldd` on that exact extension resolves `libsqlite3.so.0` to the above **private** user-owned library, not to Ubuntu's system 3.46.1 library.
- The **new Python itself** reports `sqlite3.sqlite_version == '3.54.1'` and `SELECT sqlite_source_id()` equals `2026-10-16 14:45:20 555e07ef33f69a0957d24d8e555b702464a131d6f1607f4c3c1e4551e8e6ca76`. OpenSSL import also succeeds with **OpenSSL 3.5.5**.
- Actual **unmodified** original repository procedure `handoff/astra_adr_completion_20261115/procedures/runtime_probe.py` exited **0** on this interpreter. All nine check keys reported true: `busy_timeout_zero`, `foreign_key_refusal`, `foreign_keys_on`, `integrity`, `journal_delete`, `readonly_durable_reopen`, `strict_tables`, `synchronous_extra`, `trigger_refusal`. Original probe's own loaded-library SHA256 matches `44a469...`.
- **Zero** NVIDIA product tests executed. No producer, M00, M02 or D091 product case was run by this Worker.

## Private build provenance and retained failures

The build was performed inside `/home/jds/nvda_python3135_sqlite3541_20261117`, with private `python/`, `sqlite/`, `deps/` and `debs/` subtrees. It did **not** use any pre-existing SQLite wheelhouse binary, write a system prefix or issue `sudo`/APT installation. C headers were obtained via **unprivileged `apt download`** of `libssl-dev`, `libffi-dev`, `libbz2-dev`, `liblzma-dev`, `libreadline-dev`, `libncurses-dev`; `dpkg-deb -x` extracted each into user-owned `deps/`. Exact downloaded package filenames and hashes are in the build receipt. The SQLite C source+headers and shared library came from the earlier verified *official* source archive, not the distribution's older SQLite headers.

**Failed attempt 1**: `make -j2` stopped because `libbz2.so` in the extracted development archive was a broken *user-local* symlink to an absent local SONAME, so the linker selected non-PIC `libbz2.a` for a shared extension and refused to link. Preserved `make.log` and `build_attempt1_failed_receipt.txt`.

**Repair 1**: inside the private `deps/` tree only, create exact links to already existing system runtime `.so` files (including bz2/lzma/ffi) rather than modify system libraries; `make -j2` and `make install` succeeded. Preserved `make_attempt2.log`/`install_attempt2.log` and details in the build receipt.

**Failed qualification after repair 1**: initial Python 3.13.5 import of `ssl` raised `ModuleNotFoundError: _ssl`, because configure's OpenSSL test had called the linker without `-lssl -lcrypto`, though user-local OpenSSL headers were present. Preserved original `config_attempt1.log`.

**Repair 2**: rerun configuration with exact `OPENSSL_LDFLAGS`, `OPENSSL_LIBS=-lssl -lcrypto` and `OPENSSL_INCLUDES` pointing to the user-owned Ubuntu developer package extraction, and the unchanged `LIBSQLITE3_CFLAGS/LIBSQLITE3_LIBS`. Current `configure_openssl.log` explicitly reports successful OpenSSL and `_ssl` checks; `make_openssl.log` and `install_openssl.log` exited 0. Re-running qualification on that final interpreter succeeded without modifying the original SQLite probe.

**Historical binary mismatch remains an identity fact, not an active feature failure:** the newly compiled user-owned `libsqlite3.so.0` hash `44a469...` differs from older GCC14.2 `c537069...`; its verified upstream SQLite **source ID** is identical, and its actual interpreter linkage and non-product SQLite mechanisms now pass. No historical executable byte-for-byte identity is claimed. The *earlier* local `_sqlite3` was built-in SQLite 3.49.1, and the old probe failed there; these earlier failures are preserved in `LOCAL_SQLITE_BINDING_DIAGNOSTIC_20261117.json` and `NONPRODUCT_RUNTIME_PREFLIGHT_FAILURE.json`.

## Durable full receipts and executed stages

- `UBUNTU_NATIVE_CPYTHON_BUILD_RECEIPT_20261117.json` — full tarball/deb/toolchain/flag/source/archive hashes, exact build phases, previous errors and repairs.
- `UBUNTU_NATIVE_CPYTHON_QUALIFICATION_RECEIPT_20261117.json` — full interpreter SHA, sqlite extension SHA/path, `ldd`, SQLite source ID/options, exact original probe stdout/checks, exit codes and readback.
- `UBUNTU_NATIVE_PYTHON_BUILD_ATTEMPT1.py` — executed official-source download, user-only deps extraction and first build attempt; this stage failed and is **not** a standalone clean replay of the final environment.
- `UBUNTU_NATIVE_PYTHON_LINKER_REPAIR.py` — actually executed bounded private-linker repair and resulting successful build/install.
- `UBUNTU_NATIVE_PYTHON_OPENSSL_REPAIR.py` — actually executed `_ssl` configure/link correction and successful final build/install.
- `UBUNTU_NATIVE_PYTHON_QUALIFICATION_PROCEDURE.py` — actually executed bounded non-product test protocol.

The above is a **multi-stage incident/recovery record**, not a claim that executing just the first script recreates the final build. A new clean receiver must assemble the final approved configuration and validate its own native hashes, dynamically linked paths, actual feature behaviour and Git/checkpoint receipt; an implementation-independent reviewer must assess that evidence. No raw build binaries or system libraries were committed to GitHub.

## Remaining independently held authority

This establishes the exact **local non-product environment-mechanism prerequisites** to a substantially stronger degree than the previous failed preflight. It does **not** prove the separately designated strict product Tester will use this same binary or confirm the full independent L00 receiver and original 66 historical ref assets, nor complete the exact D091 owner category/codec/test-port/claim/generation binding. The independent implementation-release reviewer must assess which of those are prerequisites to authoring product code/tests and which only to later executing cases; do not treat a favourable local build as case-execution release. D091 18 and L01b 15 remain admitted but execution-held; D145 remains PAUSED.
