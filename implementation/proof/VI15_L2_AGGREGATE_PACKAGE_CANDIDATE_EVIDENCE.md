# VI-15-L2 — Aggregate promotion and truthful package/install candidate evidence

## Status

**WORKER CANDIDATE FROZEN — FRESH INDEPENDENT TESTER REQUIRED.**

## Exact candidate

- branch: `work/vi15-l2-aggregate-package-proof`;
- candidate commit: `332c1f95da032f841e8779ef21fe3c1fceb698a2`;
- candidate tree: `3abec93134d128978ad6bcedbd0dfa6cf4334ec6`;
- accepted VI-15-L1 promotion close-out predecessor: `abccadf20d10daa29e739c6ba54a970fcff41614`;
- VI-15-L2 routing commit on `main` at Worker start: `3b1671dc0c15e5ab9023bd20362c432b1fd7a05a`.

The candidate is an empty boundary commit over the exact routed VI-15-L2 tree. This deliberately
freezes one unique review identity without changing production, proof, configuration, dependency,
package or documentation bytes. Relative to the accepted VI-15-L1 close-out, the candidate tree adds
only the VI-15-L2 current-state/request routing records. Relative to the accepted VI-15-L1 metadata
candidate, the only build-selected-path change is the already-promoted `EXEC_PLAN.md` progress mark
recording VI-15-L1 as accepted/promoted; that plan byte is included in the sdist and was inventoried
from the exact candidate.

## Governing proposition

VI-15-L2 section 7 of the accepted `EXEC_PLAN.md` requires one exact clean committed state where:

- the complete product blocking set is green as a separately attributable axis;
- the complete architecture/bootstrap blocking set is independently green;
- wheel and sdist are built and inventoried from that exact state;
- the built wheel is installed outside the repository/source tree without path injection;
- the installed distribution exposes the admitted Raw Signal Occurrence Truth/A00 behaviour;
- unadmitted/inactive capability is absent or lawfully inactive;
- exact package hashes, sizes and material build/proof environment identities are recorded.

Current package law is `AK-PKG-001` / `AK-PKG-002` in
`docs/architecture/ARCHITECTURE_KERNEL.md`.

## Exact-candidate blocking proof axes

### Product axis

Command:

```text
PYTHONPATH=src:. <Python-3.13.5> tools/run_product_proof_gate.py --aggregate raw_signal_occurrence_truth_product
```

Observed on exact candidate `332c1f95...`:

- **479/479 passed**;
- six admitted physical product families;
- **13/13** required product obligations covered;
- aggregate `raw_signal_occurrence_truth_product` remained `READY_FOR_PROOF`;
- no skipped or failed case was reported;
- worktree clean before and after.

An earlier execution-wrapper timeout interrupted the same unchanged aggregate during U05 and emitted
no test failure. No proof process remained afterwards, PostgreSQL was responsive with no blocked proof
session, and the governed aggregate was rerun unchanged to the explicit 479/479 result above. The
incomplete timeout is not counted as proof.

### Architecture/bootstrap axis

Command:

```text
PYTHONPATH=src:. <Python-3.13.5> tools/run_promotion_gate.py --set architecture_kernel
```

Observed on the exact candidate:

- **74/74 passed**;
- 11 current-blocking architecture/bootstrap test families;
- one active runtime module;
- one implementation allocation;
- zero dependency/public-seam violations;
- worktree clean before and after.

## Exact candidate build

The build began and ended with a clean worktree at candidate `332c1f95...` / tree `3abec931...`.
Configured backend/toolchain:

- Python `3.13.5`;
- Hatchling `1.29.0`;
- packaging `26.2`;
- pathspec `1.1.1`;
- pluggy `1.6.0`;
- trove-classifiers `2026.4.28.13`.

Commands:

```text
hatchling build -t wheel -d /mnt/data/vi15_l2_final_dist
hatchling build -t sdist -d /mnt/data/vi15_l2_final_dist
```

Exact outputs:

| Artefact | Bytes | SHA-256 |
| --- | ---: | --- |
| `nvda_architecture_kernel-1.0.0-py3-none-any.whl` | 37,378 | `d311960234c932c2507f7b1671c8d53bff3ec234692e65ca27b440293e37e127` |
| `nvda_architecture_kernel-1.0.0.tar.gz` | 161,445 | `135e47f6ab531e8e650a2ee1adc9582965e1c81d97d08dfdc854757a790629fa` |

A prior provisional build of the same tree in the same build environment produced the same two hashes.
This records observed same-environment byte identity only; it is not a broader reproducible-build claim.

## Wheel/sdist inventory

Exact-candidate inventory established:

- wheel: 21 files total;
- wheel: 16 Python files, exactly matching every tracked `src/nvda_desk/**/*.py` path and byte;
- wheel metadata: `nvda-architecture-kernel==1.0.0`, `Requires-Python ==3.13.5`;
- production dependencies: `PyYAML==6.0.3`, `psycopg[binary]==3.3.4`;
- all five console entry points target `nvda_desk.architecture.cli`;
- sdist: 117 files;
- every repository-backed sdist member is byte-equal to the exact candidate repository file;
- the only generated non-repository sdist member is `PKG-INFO`;
- sdist contains the same 16 runtime Python source files as the candidate source tree.

## Isolated installed-distribution proof

A fresh Python 3.13.5 venv was created at
`/mnt/data/vi15_l2_candidate_install_env`, with working directory
`/mnt/data/vi15_l2_candidate_outside`. The exact wheel above was installed offline using `pip 25.1.1`
with `--no-index --only-binary=:all:` and only the preserved local wheelhouses.

Installed runtime set:

- `nvda-architecture-kernel==1.0.0`;
- `PyYAML==6.0.3`;
- `psycopg==3.3.4`;
- `psycopg-binary==3.3.4`.

Direct installed proof, launched outside the repository with `PYTHONPATH` unset, established:

- the repository path is absent from `sys.path`;
- `nvda_desk`, A00 composition and M00 public-seam modules load only from the isolated venv's
  `site-packages`;
- installed `direct_url.json` records
  `sha256=d311960234c932c2507f7b1671c8d53bff3ec234692e65ca27b440293e37e127`, binding the installed
  archive to the exact Worker wheel;
- all five installed console scripts are present;
- the only top-level `nvda_desk` runtime packages are `architecture`, `composition`, and
  `raw_signal_occurrence_truth`.

Against real PostgreSQL 17.9, using only the installed A00/M00 package bytes, a direct public-seam
sequence registered policy truth, realised the exact scheduled capture, admitted one raw observation,
derived its receipt relation, appended assessment truth and read the observation back exactly:

- assessment outcome: `one_or_more_received`;
- referential readback equals the submitted observation;
- durable row counts after the sequence: `(1, 1, 1, 1)` for policy/capture/observation/assessment;
- a freshly constructed A00 application repeated the same exact identities and result;
- row counts after the fresh-application retry remained `(1, 1, 1, 1)`.

## Unadmitted/inactive capability closure

Current primary architecture registries establish:

- `M00` is the sole active runtime module and owns package
  `nvda_desk.raw_signal_occurrence_truth` with public seam `.api`;
- `A00` is the bootstrap composition shell at `nvda_desk.composition` with the declared edge
  `A00 -> M00`;
- `P01` / DMPV3 is `placeholder` and has no package field;
- `K01` is `placeholder` and has no package field;
- surfaces are empty;
- implementation allocations contain only `M00`;
- the architecture framework package is `nvda_desk.architecture`.

The exact wheel contains only the root package plus those three authorised runtime/package roots.
There is no P01, K01, provider/network, downstream-consumer or other unadmitted runtime package in the
installed module inventory. Product blocking proof is exactly the six M00 Raw Signal families; the
architecture blocking population is exactly the 11 current architecture/bootstrap families.

Accordingly, Worker evidence establishes package/runtime absence or lawful inactivity for the
currently named inactive capabilities required by VI-15-L2. This does not activate or prove any such
capability.

## Proof/runtime environment identity

Product/architecture proof environment:

- Python `3.13.5`;
- pytest `9.0.3`;
- mypy `1.20.1`;
- Ruff `0.15.11`;
- Psycopg `3.3.4` / psycopg-binary `3.3.4`;
- PyYAML `6.0.3`;
- pluggy `1.6.0`;
- PostgreSQL `17.9`, server encoding `UTF8`, `fsync=on`, `synchronous_commit=on`,
  `full_page_writes=on`, Unix socket `/mnt/data/vi15_l2_proof_env/pgsocket`, with no TCP listen
  address reported by `SHOW listen_addresses`.

Preserved proof-environment artefacts used:

- `NVDA_U05_PROOF_ENV_BOOTSTRAP_PY313_PG17_9_20260926.tar(1).gz` — SHA-256
  `01050287798e53e38f33794e201df53adbe6fcba03024a027ac36d3d9cea66b8`;
- `NVDA_POSTGRESQL_17_9_PORTABLE_RUNTIME_20260921.tar(1).gz` — SHA-256
  `59822410ac6855365c90765de5071182ab382e87d9e9a2622424e7787c4e5caf`.

Incoming VI-15-L2 Worker full-Git handoff:

- SHA-256 `67146a3a20b59f2a9dec25f0bc8d78fe3991e2a1c4ed91353c3f08421193904c`.

## Repository integrity

At candidate proof/build boundaries:

- worktree clean;
- accepted VI-15-L1 close-out is an ancestor of the candidate;
- candidate is an empty boundary commit over the routed tree;
- `git diff --check HEAD^..HEAD` returns clean;
- `git fsck --full` returns success and reports eight existing dangling blobs, with no corruption/error.

## Worker disposition

**VERIFIED:** the exact candidate `332c1f95da032f841e8779ef21fe3c1fceb698a2` / tree
`3abec93134d128978ad6bcedbd0dfa6cf4334ec6` has separately green complete product and
architecture/bootstrap blocking axes, exact wheel/sdist build and inventory, isolated installed
A00/M00 behaviour, exact package hashes and current inactive-capability exclusion evidence.

**UNPROVED:** independent VI-15-L2 Tester acceptance. The Worker does not self-award VI-15-L2 PASS.

**NOT_IN_SCOPE:** VI-16 whole-BICP semantic review and all later leaves.

**NEXT LAWFUL ACTION:** fresh independent Tester review of exactly the candidate and package artefacts
recorded above. On Tester PASS only, a subsequent Worker may promote the accepted VI-15-L2 lineage and
route VI-16-L1.
