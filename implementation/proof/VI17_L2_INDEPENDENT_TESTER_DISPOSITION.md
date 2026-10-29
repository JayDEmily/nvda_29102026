# VI-17-L2 — Independent provenance/environment/integrity Tester disposition

## Disposition

**PASS**

## Exact reviewed state

- candidate commit: `57712201296c6da811e4e6838d0f3fb302239df4`;
- candidate tree: `1b017b6c01176fc61963a63bcf12d843aac8d0db`;
- Tester cycle: `TESTER_VI17_L2_1790634143`;
- accepted package candidate: `332c1f95da032f841e8779ef21fe3c1fceb698a2`;
- accepted VI-16 candidate / Tester PASS: `9248f3b1788f8e99e59a0482c4cc393c27942715` / `9f5f7e90b463365fb39c361f2e346d9e67c6d915`;
- accepted VI-17-L1 candidate / Tester PASS / promotion close-out: `c07d5277512f600669b05a88cc2c174af3e3b046` / `5397a90dd2e245e17bd5e0eb526861396dae3082` / `d37e5951560d1f1a2b2704888b2b2e15002288f5`;
- received Tester handoff SHA-256: `1f79aa5a56b0b78b1d3d53fd9ca173aa1cd5b4c2113f17d8827c3cc0de3fffab`.

The review used a detached worktree at the exact candidate rather than the later Tester-routing tip.

## Package identity and candidate binding

The supplied artefacts independently hash to:

- wheel: 37,378 bytes, `d311960234c932c2507f7b1671c8d53bff3ec234692e65ca27b440293e37e127`;
- sdist: 161,445 bytes, `135e47f6ab531e8e650a2ee1adc9582965e1c81d97d08dfdc854757a790629fa`.

Wheel metadata is `nvda-architecture-kernel==1.0.0`, `Requires-Python ==3.13.5`, with
`PyYAML==6.0.3` and `psycopg[binary]==3.3.4`. The wheel contains 21 members including exactly 16 runtime Python files;
all 16 are byte-identical to `src/nvda_desk/**/*.py` at accepted package candidate `332c1f95...`.

The sdist contains 117 file members. All 116 repository-backed members are byte-identical to the same accepted package
candidate; generated `PKG-INFO` is the only non-repository member.

## Build/proof environment provenance

The accepted VI-15-L2 Worker/Tester records independently agree on the accepted build toolchain: Python `3.13.5`,
Hatchling `1.29.0`, packaging `26.2`, pathspec `1.1.1`, pluggy `1.6.0` and trove-classifiers
`2026.4.28.13`. This disposition preserves that as exact recorded provenance; it does not claim arbitrary-host
reproducibility.

The separately preserved U05 proof bootstrap and PostgreSQL portable runtime rebind exactly to:

- bootstrap: `01050287798e53e38f33794e201df53adbe6fcba03024a027ac36d3d9cea66b8`;
- PostgreSQL runtime: `59822410ac6855365c90765de5071182ab382e87d9e9a2622424e7787c4e5caf`.

Their internal manifests verify `24/24` and `1937/1937` payload entries respectively. Extracted `postgres` and
`pg_config` identify PostgreSQL `17.9`.

A fresh bootstrap execution independently established Python `3.13.5`, pytest `9.0.3`, mypy `1.20.1`, Ruff `0.15.11`,
Psycopg `3.3.4`, PostgreSQL `17.9`, server encoding `UTF8`, `fsync=on`, `synchronous_commit=on`,
`full_page_writes=on`, and empty `listen_addresses` using a Unix socket.

The portable-runtime build receipt also records an earlier transfer-validation cluster using `SQL_ASCII`. That historical
cluster is not conflated with the accepted U05/VI-15/VI-16 proof environment, whose fresh bootstrap explicitly creates
UTF8 and whose live settings were independently read back here.

The proof bootstrap intentionally omits a PyYAML wheel. Current host PyYAML `6.0.3` was independently observed and used
only as the same bounded overlay class already recorded by prior accepted reviews. The exact binary/archive digest of the
prior accepted PyYAML overlay remains **UNKNOWN**. This PASS does not convert that limitation into a fully self-contained
or generally reproducible environment claim.

## Final result binding and no-drift check

Accepted VI-15-L2 independent proof records establish product `479/479`, six product families covering `13/13` current
product obligations, architecture/bootstrap `74/74`, and mypy/Ruff PASS. VI-16 independently re-challenged the whole
BICP and recorded the same aggregate identities.

Direct scoped Git diffs from each of package candidate `332c1f95...`, VI-16 candidate `9248f3b...`, and VI-17-L1
candidate `c07d527...` to exact VI-17-L2 candidate `5771220...` are empty for `src/**`, `tests/**`, `config/**` and
`pyproject.toml`. Those accepted result identities therefore remain attached to the final substantive state being
provenance-audited.

Current registration readback remains one active M00 runtime module, A00 bootstrap shell with permitted dependency M00,
one M00 implementation allocation and no declared surfaces. Product-proof control remains `READY_FOR_PROOF`, six
families and 13/13 current product obligations with `IA22R01-PROD-009` current and predecessor `IA17-PROD-009`
explicitly forbidden.

Structural architecture, dependency, public-seam, product-proof and implementation-authority validators passed on the
exact candidate. One first invocation of the implementation-authority validator omitted its required CLI arguments and
returned usage-error; no repository result was inferred from that Tester harness mistake. The corrected governed
invocation passed.

## Installed distribution and inactive capability closure

The exact accepted wheel was independently installed into a fresh external Python 3.13.5 proof venv with no dependency
resolution. `nvda_desk` loaded from that venv's `site-packages`, the repository path was absent from `sys.path`, and
`direct_url.json` bound the installed archive to the exact accepted wheel SHA-256.

Installed runtime subpackages were exactly `architecture`, `composition` and `raw_signal_occurrence_truth`; P01, K01,
provider, network, downstream-consumer, DMPV3-packet and replay runtime modules were absent.

A Tester-authored fixture-independent A00 -> PostgreSQL-backed M00 sequence against the fresh 17.9 cluster produced
`one_or_more_received`, exact observation readback and durable policy/capture/observation/assessment counts `(1,1,1,1)`.
A fresh application exact retry reproduced the same result with unchanged `(1,1,1,1)` counts.

## Git integrity, lineage continuity and thread-change check

The exact candidate worktree is clean. `git diff --check` and `git fsck --full --no-dangling` pass. Full fsck reports
only the previously known eight dangling blobs and no repository corruption.

Every listed accepted U01-U06 and VI-14/VI-15/VI-16/VI-17-L1 candidate/review/promotion identity exists locally and is
an ancestor of exact candidate `5771220...`. Thin root `8133432...` is also an ancestor. External predecessor
`d095954...` remains absent from the intentionally thin object database and is not claimed as local ancestry.

The recent commit graph was specifically audited because execution moved to a new Worker thread. The current sequence is
linear and monotonic:

`5397a90` VI-17-L1 Tester PASS -> `d37e595` VI-17-L1 promotion/close-out -> `4daaa40` VI-17-L2 Worker route ->
`98c3458` VI-17-L2 audit packet -> `5771220` frozen candidate -> `8d1e73e` Tester route.

No rollback, duplicate current review, reopened VI-17-L1 leaf or Worker/Tester loop was established. The historical
routing-only branch `0477558...` remains outside main as expected; its accepted Tester PASS parent `5397a90...` is the
lineage that was promoted.

## VI-18 recovery prerequisites and acceptance boundary

The supplied handoff extracted with a complete active `.git` store and package artefacts; accepted active-history
objects are reachable; preserved proof/PostgreSQL archives remain separately hash-verifiable. These are sufficient
prerequisites for VI-18 to create and then read back a new terminal recovery artefact after lawful VI-17-L2 promotion.
They are not themselves a VI-18 recovery artefact, and none was created or accepted in this Tester leaf.

No material package-identity, environment-provenance, installed-package, inactive-capability, Git-integrity, ancestry,
post-review drift or resumability gap was established. Exact candidate `57712201296c6da811e4e6838d0f3fb302239df4`
therefore satisfies VI-17-L2 and is accepted for subsequent preserved-ancestry VI-17-L2 promotion/close-out only.
VI-18 remains prohibited until that promotion/close-out completes.
