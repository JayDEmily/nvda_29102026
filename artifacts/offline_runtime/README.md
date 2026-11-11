# Canonical NVIDIA V2 offline CPython 3.13 wheelhouse

**Preservation only — 11 November 2026. Not a product or runtime qualification.**

This branch preserves a **single verified copy** of the 23 October CPython 3.13 offline wheelhouse, previously available in ChatGPT Library as `NVDA_PY313_OFFLINE_WHEELHOUSE_COMPLETE_20261023.zip` and `NVDA_PY313_OFFLINE_WHEELHOUSE_COMPLETE_20261023(1).zip`.

Archive: `NVDA_PY313_OFFLINE_WHEELHOUSE_COMPLETE_20261023.zip`
Bytes: **29,555,356**
SHA-256: `33bc332bae5cc10d8b9dfc5ba6a4fe4664318c0e8ead6796f44e522172d2d504`

Source was retrieved through the user's authenticated ChatGPT Library to Windows Downloads, independently SHA-256-verified, then validated with Python `zipfile.testzip()` and **all 16 SHA256SUMS wheel entries**. The ZIP contains **19 entries**: one README, one `SHA256SUMS`, one `WHEEL_MANIFEST.json` and 16 wheel archives. Embedded wheels were not independently installed or run in this archival task.

This archive is the **Python 3.13 compatible** dependency set. The 17 `vendor/wheels/` distributions tracked in the original recovered Git tree include CPython **3.12**-specific wheels and are not a demonstrated substitute for the 3.13 wheelhouse.

**Known exclusions / limits:** the archive contains the pure `psycopg==3.3.4` wheel but **does not contain a `psycopg_binary` wheel** for CPython 3.13. It also does **not** contain or qualify the specified SQLite 3.54.1 shared library or the PostgreSQL 18.6 server. The future T03/T04 environment qualification must bind these independently; do not claim a passing runtime because this artifact exists.

This is an isolated preservation branch based on the exact F02 recovered commit `16b7cc67f5d24336d3768e2da006819474a8c792`. It is **not** a new active NVIDIA root, a merge, a source change or an accepted plan. Keep other source and review branches intact.

To check archive identity after cloning this branch:

```sh
sha256sum artifacts/offline_runtime/NVDA_PY313_OFFLINE_WHEELHOUSE_COMPLETE_20261023.zip
python3 -m zipfile -t artifacts/offline_runtime/NVDA_PY313_OFFLINE_WHEELHOUSE_COMPLETE_20261023.zip
```

The result SHA-256 must match the value above. GitHub is currently a **public repository**; this branch contains only the named offline dependency ZIP and this manifest, not private credentials or research attachments. The original Library copies are no longer the sole known archive location once this branch passes independent GitHub readback.
