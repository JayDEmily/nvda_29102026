# VI-17-L2 provenance, environment and repository-integrity candidate evidence

## Status and scope

**Worker status:** audit complete; exact candidate freeze pending; fresh independent Tester required.

This record executes only VI-17-L2 under section 9 of the accepted root `EXEC_PLAN.md`. It audits the
already accepted bounded implementation/package state. It does not change implementation meaning,
proof control, package metadata, dependencies, architecture authority or accepted package bytes.

Exact routed Worker baseline:

- branch: `work/vi17-l2-provenance-integrity`;
- commit: `4daaa4050da594e8feb893bb60f171c6828687af`;
- tree: `ee24b621e37d7d3689d77473b682b8535919c7a7`;
- accepted VI-17-L1 promotion close-out predecessor:
  `d37e5951560d1f1a2b2704888b2b2e15002288f5`;
- accepted VI-17-L1 candidate:
  `c07d5277512f600669b05a88cc2c174af3e3b046` / tree
  `5a156a0170bb31ab2253822a9cf3172bd610f5fe`;
- VI-17-L1 independent Tester PASS:
  `5397a90dd2e245e17bd5e0eb526861396dae3082`.

Incoming full-Git/package handoff used to establish this Worker state:

- `NVDA_G03_VI17_L1_TESTER_PASS_PROMOTION_WORKER_HANDOFF_FULL_GIT_AND_PACKAGE_20260928.tar(1).gz`;
- size: `6,668,847` bytes;
- SHA-256: `688ba704aa3fed6432b8f0f2eac0b804e291098f647f7880dbb3900766284e83`.

The incoming archive contains a `.git` object/ref store, repository working tree, accepted package
artefacts and package `SHA256SUMS`. It predates the local VI-17-L1 promotion and VI-17-L2 routing
commits, so it is provenance input rather than the future VI-18 terminal recovery artefact.

## 1. Final distribution and package identity

Current `pyproject.toml`, the accepted wheel metadata and the accepted VI-15 distribution authority
agree on:

- distribution name: `nvda-architecture-kernel`;
- version: `1.0.0`;
- Python requirement: `==3.13.5`;
- runtime dependencies: `PyYAML==6.0.3`, `psycopg[binary]==3.3.4`;
- build backend: `hatchling.build`, with `hatchling==1.29.0`.

Accepted package candidate:

- commit: `332c1f95da032f841e8779ef21fe3c1fceb698a2`;
- tree: `3abec93134d128978ad6bcedbd0dfa6cf4334ec6`.

Direct re-audit of the supplied final artefacts established:

| Artefact | Bytes | SHA-256 | Manifest check |
| --- | ---: | --- | --- |
| `nvda_architecture_kernel-1.0.0-py3-none-any.whl` | 37,378 | `d311960234c932c2507f7b1671c8d53bff3ec234692e65ca27b440293e37e127` | OK |
| `nvda_architecture_kernel-1.0.0.tar.gz` | 161,445 | `135e47f6ab531e8e650a2ee1adc9582965e1c81d97d08dfdc854757a790629fa` | OK |

The package-directory `SHA256SUMS` was executed from its own directory and both entries returned
`OK`.

### Wheel inventory and source binding

Direct wheel inspection established:

- 21 files total;
- 16 Python runtime files;
- wheel metadata name/version exactly `nvda-architecture-kernel==1.0.0`;
- `Requires-Python: ==3.13.5`;
- runtime dependency metadata for `PyYAML==6.0.3` and `psycopg[binary]==3.3.4`;
- all Python entries are under the `nvda_desk` package root.

Every one of the 16 wheel Python files was compared byte-for-byte with the corresponding
`src/nvda_desk/**` file at exact package candidate `332c1f95...`:

- compared: **16**;
- missing: **0**;
- mismatches: **0**.

### sdist inventory and source binding

Direct sdist inspection established:

- 117 regular files total;
- 116 repository-backed members compared against exact package candidate `332c1f95...`;
- missing repository members: **0**;
- byte mismatches: **0**;
- the only generated non-repository member is `PKG-INFO`.

These checks establish the supplied package artefacts' identity and their byte binding to the
accepted package candidate. They do not by themselves establish broader build reproducibility.

## 2. Accepted build-toolchain provenance

The accepted VI-15-L2 Worker build record binds the final package build to:

- Python `3.13.5`;
- Hatchling `1.29.0`;
- packaging `26.2`;
- pathspec `1.1.1`;
- pluggy `1.6.0`;
- trove-classifiers `2026.4.28.13`.

The Worker recorded two builds of the same candidate tree in that same environment producing the
same wheel/sdist hashes. The fresh VI-15-L2 independent Tester then rebuilt the exact detached
candidate with Python `3.13.5` / Hatchling `1.29.0` and obtained artefacts byte-for-byte identical to
the Worker artefacts and hashes above.

**Bounded claim:** this establishes the recorded accepted build provenance and observed exact-byte
repeatability in the exercised environments. It is **not** a claim that the project has a generally
reproducible build across arbitrary hosts or future toolchains.

## 3. Accepted proof/install environment identity

The accepted VI-15-L2 proof/runtime record and independent Tester disposition establish the proof
environment used for the final package/proof challenge as:

- Python `3.13.5`;
- pytest `9.0.3`;
- mypy `1.20.1`;
- Ruff `0.15.11`;
- Psycopg `3.3.4`;
- psycopg-binary `3.3.4`;
- PyYAML `6.0.3`;
- pluggy `1.6.0`;
- PostgreSQL `17.9`.

The isolated package-install proof additionally records `pip 25.1.1` and installed runtime set
`nvda-architecture-kernel==1.0.0`, `PyYAML==6.0.3`, `psycopg==3.3.4`,
`psycopg-binary==3.3.4`.

### Preserved proof-environment archives

Two separately supplied preserved environment artefacts were directly rebound in this VI-17-L2
Worker audit:

1. `NVDA_U05_PROOF_ENV_BOOTSTRAP_PY313_PG17_9_20260926.tar(1).gz`
   - outer SHA-256:
     `01050287798e53e38f33794e201df53adbe6fcba03024a027ac36d3d9cea66b8`;
   - extracted internal `SHA256SUMS`: **24/24 regular payload entries OK**;
   - `requirements.lock`: pytest `9.0.3`, mypy `1.20.1`, Ruff `0.15.11`,
     `psycopg[binary]==3.3.4`;
   - expected PostgreSQL runtime hash embedded in the bundle matches the archive below.

2. `NVDA_POSTGRESQL_17_9_PORTABLE_RUNTIME_20260921.tar(1).gz`
   - outer SHA-256:
     `59822410ac6855365c90765de5071182ab382e87d9e9a2622424e7787c4e5caf`;
   - extracted internal `SHA256SUMS`: **1,937/1,937 regular payload entries OK**;
   - direct extracted-binary readback: `postgres`, `initdb`, `pg_ctl` and `pg_config` all report
     PostgreSQL `17.9`.

The PostgreSQL runtime receipt also records preserved source archive
`postgresql-17.9.tar.bz2`, SHA-256
`3b9a62538a8da151e807a3ddb1198e8605f2032544d78f403ae883d27ecf1ee4`, and configure options
`--without-readline --without-zlib --without-icu` under the historical prefix
`/mnt/data/nvda_pg17_prefix`.

### Current Worker sandbox is not substituted for accepted proof

The current Worker sandbox was directly inspected and differs from the accepted proof/build
environment:

- Python `3.13.5`;
- pytest `9.0.2`;
- pip `25.1.1`;
- Git `2.47.3`;
- PyYAML `6.0.3` present;
- Hatchling absent;
- `build` module absent;
- Psycopg absent.

Therefore this Worker did **not** represent the current sandbox as the accepted proof environment and
did not use it as a substitute for the independently accepted product/PostgreSQL execution.

The preserved U05 bootstrap does not itself contain a PyYAML wheel. The VI-15-L2 and VI-16 Tester
records explicitly state that exact locally installed PyYAML `6.0.3` was supplied to their fresh
environments. The exact PyYAML wheel/archive digest used there is not established by the current
VI-17-L2 input. This limits a claim of fully self-contained offline environment reproduction; it does
not change the recorded accepted runtime version, package dependency metadata or accepted package
bytes.

## 4. PostgreSQL proof-environment identity and durability configuration

The accepted final proof environment used PostgreSQL `17.9` with:

- database encoding: `UTF8`;
- `fsync=on`;
- `synchronous_commit=on`;
- `full_page_writes=on`;
- Unix-domain-socket transport;
- `listen_addresses` empty / no TCP listening address in the accepted proof readback.

The portable-runtime `BUILD_RECEIPT.md` separately records an earlier transfer-validation cluster
created with `--no-locale`, whose default encoding was `SQL_ASCII`. That earlier transfer cluster is
not conflated with the later accepted U05/VI-15 proof cluster, which was freshly bootstrapped as
`UTF8` and independently checked with the durability settings above.

PostgreSQL `17.9` remains proof-environment identity only. It is not asserted as a broader production
version requirement beyond the accepted bounded proof.

## 5. Final product and architecture aggregate-result identity

The final package candidate `332c1f95...` was independently challenged in
`TESTER_VI15_L2_1790584579`, whose PASS disposition is committed at
`eed5c5f6fa9eeda02886ed8fda0d6205177823e5`:

- complete admitted product population: **479/479 PASS**;
- product proof control: six admitted families, **13/13** required current obligations;
- architecture/bootstrap blocking set: **74/74 PASS** across 11 current-blocking families;
- mypy: PASS across 16 source files;
- Ruff: PASS.

VI-16 then independently re-challenged the realised whole-BICP implementation/package in
`TESTER_VI16_L1_1790592833`, PASS commit
`9f5f7e90b463365fb39c361f2e346d9e67c6d915`, again recording:

- product: **479/479 PASS**;
- six admitted product families / **13/13** current product obligations;
- architecture/bootstrap: **74/74 PASS**;
- mypy across 16 source files and Ruff: PASS.

Current proof-control/configuration was directly parsed during this audit and still declares:

- aggregate `raw_signal_occurrence_truth_product` at `READY_FOR_PROOF`;
- 13 required current product obligations;
- six declared/admitted product families;
- 11 architecture/bootstrap test families.

A scoped Git diff from accepted package candidate `332c1f95...` to the routed VI-17-L2 baseline is
empty for `src/**`, `tests/**`, `config/**` and `pyproject.toml`, so no later substantive byte drift
was found that would detach those accepted result identities from the frozen implementation/proof
state being audited.

## 6. Final installed-package proof identity

The accepted VI-15-L2 package/install proof established in a fresh external Python `3.13.5` venv,
with `PYTHONPATH` unset and repository path absent from `sys.path`:

- `nvda_desk` loaded from external `site-packages`;
- installed `direct_url.json` bound the installation to wheel SHA-256
  `d311960234c932c2507f7b1671c8d53bff3ec234692e65ca27b440293e37e127`;
- all five configured console entry points were present;
- top-level runtime packages were only `architecture`, `composition` and
  `raw_signal_occurrence_truth`;
- direct installed A00 -> PostgreSQL-backed M00 execution produced exact observation readback,
  `one_or_more_received`, durable row counts `(1,1,1,1)`, and unchanged row counts after a fresh
  application retry.

The independent VI-15-L2 Tester separately installed its exact rebuilt wheel and reproduced the
external-site-packages binding and direct PostgreSQL-backed public-seam challenge. VI-16 then
performed an additional fresh external installed-package semantic challenge without repository path
injection.

No accepted package bytes have changed since package candidate `332c1f95...`.

## 7. Inactive-capability closure

Current primary architecture configuration directly establishes:

- `M00` is the sole active runtime module, package `nvda_desk.raw_signal_occurrence_truth`;
- `A00` is the bootstrap composition shell, package `nvda_desk.composition`;
- `P01` is `placeholder` and has no package field;
- `K01` is `placeholder` and has no package field;
- implementation allocation contains only `M00`;
- declared surfaces are empty.

The accepted wheel contains only the `nvda_desk` runtime root and the authorised architecture,
composition and Raw Signal Occurrence Truth modules. Independent VI-15-L2 and VI-16 installed-package
challenges found no importable P01, K01, DMPV3, provider/network, downstream-consumer or replay
runtime package.

This is package/runtime absence or lawful inactivity evidence only. It does not activate or prove any
of those capabilities.

## 8. Repository state, integrity, ancestry and drift

At the routed VI-17-L2 baseline before evidence mutation:

- `git status --porcelain=v1`: empty;
- `git diff --check`: success;
- `git fsck --full --no-dangling`: success;
- `git fsck --full`: success with eight dangling blobs and no corruption/error.

The eight dangling blobs are:

- `d9e05bce55672517b98b3b92de90379e30ec1be2`;
- `8b2975c927849b624b0d55b9118974975c91bada`;
- `5f2b966adcbd83a68e901e79de258e620f15c8cc`;
- `37d03df4ac72e2d4709bd454cbb53d979265de77`;
- `7293b42e4c2104678c5e61262e4b870f5056635e`;
- `8fd41f1e8b8e5c9bc1c6136fbca84c82f5a09b26`;
- `895775b2d27b6006f3f245b6742d5d021fed089b`;
- `84f827bc647c22f846909c9540ee84630eb7255f`.

All accepted candidate/review/promotion identities audited for the active U01-U06 and
VI-14/VI-15/VI-16/VI-17-L1 lineage are present and directly verified ancestors of routed baseline
`4daaa405...`:

| Unit | Candidate | Independent review | Promotion / forward state |
| --- | --- | --- | --- |
| U01 | `e8b659d7849d2f95b64ba32bed8090a8290358d4` | `4db58e9091083500a2505023a302f36447185029` | `b806447eb440a016826728af075e714beee23d31` |
| U02 | `5c62ec5147da718297b251b5a287405ebf3b4755` | `df45c5e93e7c4c19cb1cca75de5cd1c64b15537c` | `a78ae7b5515c2e482a2656cebeebae3fa5a6d584` |
| U03 | `45ca4b8dcca6fdb5001e1754fd81bdba37ce05bf` | `dc40971d24ee773ee133d07622f92d709a7cec11` | `63bbeee9cec14f38ed6da6260095ccf0d8e8e6ec` |
| U04 | `dc3b448191a2b2d3528ffb576b1ebc2c56839991` | `dd42d645b59a62f88cfbc7fba47a75e415b7296f` | recovery baseline `50ce8b2d5f84f0e6a0fc4b4c71b6e7b05a2744cb` |
| U05 | `2bdbedff62307ecfaf6186f9c12814fb662c11a7` | `9f35df4c1915de78847dfc4a23ce886dfa3b5fd8` | same accepted review identity on forward main |
| U06 | `8462630277b04d431ad393e2b73039cacb5d6247` | `562767529235cedff77d3e740a259fab9d88716e` | `ed94f745effd65050f03d921ad0ae30769877206` |
| VI-14-L1 | `076f1e979474babbb8985dc87d3b2d4d62ec0b4c` | `79b1d9d1d9da1b921c8d8197d154937dd1a699e5` | accepted forward lineage |
| VI-15-L1 | `466055a1cd5fe678a40049a00f0dc88158951d74` | `226c5cdebdfa33d5b3d8f43d3eb67b0ae6b8b355` | `abccadf20d10daa29e739c6ba54a970fcff41614` |
| VI-15-L2 | `332c1f95da032f841e8779ef21fe3c1fceb698a2` | `eed5c5f6fa9eeda02886ed8fda0d6205177823e5` | `93c1212f113e6cc4f14aca7fb7a2e560f691c38f` |
| VI-16-L1 | `9248f3b1788f8e99e59a0482c4cc393c27942715` | `9f5f7e90b463365fb39c361f2e346d9e67c6d915` | `27d83923dc982b914d898c24a03e10e221c9c2c8` |
| VI-17-L1 | `c07d5277512f600669b05a88cc2c174af3e3b046` | `5397a90dd2e245e17bd5e0eb526861396dae3082` | `d37e5951560d1f1a2b2704888b2b2e15002288f5` |

The active thin Git root `8133432ba8a07e4d04d83b14af5c3c4bd12e6b0e` is present and is an ancestor.
The separately recorded external pre-implementation predecessor
`d095954c16a9818eadb60d6364148229f2dc4558` remains absent from this intentionally thin active Git
object database. VI-17-L1 already made that transport boundary explicit and the independent Tester
accepted that exact boundary; no false local-ancestry claim is introduced here.

### Post-review substantive drift

Direct scoped diffs are empty for `src/**`, `tests/**`, `config/**` and `pyproject.toml` from each of:

- accepted package candidate `332c1f95...` -> routed VI-17-L2 baseline;
- accepted VI-16 candidate `9248f3b...` -> routed VI-17-L2 baseline;
- accepted VI-17-L1 candidate `c07d527...` -> routed VI-17-L2 baseline.

Changes after the package candidate are governance/handoff/evidence records only. No post-review
production, proof-control, configuration or dependency byte drift was found by this audit.

## 9. Recovery and resumability prerequisites for VI-18

The following prerequisites for the later VI-18 terminal recovery artefact are present:

1. the current working repository contains its `.git` object/ref store and passes Git integrity
   checks;
2. all accepted active-history candidates/reviews/promotions listed above are reachable from the
   current routed baseline;
3. the intentionally thin active-history root and the absent external predecessor boundary are
   explicitly recorded, so VI-18 need not invent unreachable ancestry;
4. the accepted wheel/sdist artefacts and their exact SHA-256 manifest are present outside the Git
   working tree and were revalidated;
5. the preserved U05 proof bootstrap and PostgreSQL portable-runtime archives are separately
   available and their outer/internal integrity has been rebound;
6. the current source packet demonstrates that a repository plus full active `.git` store and package
   artefacts can be transferred together, but it predates the local VI-17-L1 promotion and VI-17-L2
   work and therefore is **not** the terminal VI-18 recovery artefact;
7. VI-18 must create a new durable full-Git recovery artefact only after VI-17-L2 receives independent
   Tester PASS and lawful promotion, then read that new artefact back against its recorded terminal
   commit/tree as required by the ExecPlan.

No VI-18 recovery artefact is created in this leaf.

## 10. Explicit limits and unknowns

- A generally reproducible build across arbitrary hosts is **not established and not claimed**.
- The current Worker sandbox is not the accepted proof/build environment and was not substituted for
  it.
- The current Worker did not rerun the 479-case product aggregate or live PostgreSQL proof because the
  current sandbox lacks the accepted Psycopg/build toolchain; final result identity is bound to the
  already independently accepted exact candidates and the direct no-drift audit.
- The exact binary/archive digest of the PyYAML `6.0.3` overlay used by the prior independent Tester
  is **UNKNOWN** from the current inputs; its exact version and its package dependency identity are
  established.
- The external pre-implementation predecessor `d095954...` is not present in the active thin Git
  object database and is not claimed as a local ancestor.
- VI-17-L2 independent acceptance remains **UNPROVED / REQUIRED** until a fresh Tester challenges the
  exact frozen Worker candidate.

## Worker conclusion

Within VI-17-L2's authorised audit scope, the Worker identified **no material package-identity,
accepted-environment-provenance, installed-package, inactive-capability, Git-integrity, ancestry or
post-review substantive-drift gap** that prevents freezing a candidate for independent review.

This is a Worker audit conclusion only. It is not VI-17-L2 acceptance. The exact candidate must be
frozen next and routed to a fresh independent Tester before VI-18 can begin.
