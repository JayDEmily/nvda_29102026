# Tester evidence

**Status:** `COMPLETE`

## Binding

- cycle: `TESTER_VI15_L2_1790584579`
- role: fresh independent `TESTER`
- leaf: `VI-15-L2 — complete aggregate promotion and truthful package/install proof`
- received handoff SHA-256: `b05ceb2b46c7b222ef397564587b7c0c4df77eceda8edc58f1727017ec0d57b9`
- received filename: `NVDA_G03_VI15_L2_TESTER_HANDOFF_FULL_GIT_AND_PACKAGE_20260928.tar(1).gz`
- transported branch tip: `ccb8474c352ce7f9c6b689a244977f1645376721`
- exact candidate: `332c1f95da032f841e8779ef21fe3c1fceb698a2`
- candidate tree: `3abec93134d128978ad6bcedbd0dfa6cf4334ec6`
- accepted VI-15-L1 predecessor: `abccadf20d10daa29e739c6ba54a970fcff41614`

## Candidate boundary and lineage

The exact candidate is an empty boundary commit over routed parent `3b1671dc0c15e5ab9023bd20362c432b1fd7a05a`;
both have tree `3abec93134d128978ad6bcedbd0dfa6cf4334ec6`. The accepted VI-15-L1 close-out is an ancestor.
Testing was performed from a detached worktree at the exact candidate, not from the later handoff branch tip.

## Independent proof environment

The preserved environment archives matched their recorded SHA-256 identities. Environment verification established
Python 3.13.5, pytest 9.0.3, mypy 1.20.1, Ruff 0.15.11, Psycopg 3.3.4 and PostgreSQL 17.9 with UTF8,
`fsync=on`, `synchronous_commit=on`, `full_page_writes=on`, Unix-socket-only transport.

## Complete proof axes

The complete product population was independently established as **479/479 PASS**: five non-U05 admitted families
passed **424/424**, and the U05 PostgreSQL durability family passed **55/55** in bounded groups. The initial monolithic
aggregate execution hit the command-wrapper time limit before a terminal pytest result and was therefore not counted;
no failure emitted by that incomplete run was used as evidence.

Product-proof control independently passed with six admitted physical families and **13/13** required obligations.
The separately governed architecture/bootstrap axis passed **74/74** across 11 current-blocking families. mypy passed
16 source files and Ruff passed.

## Package reconstruction and inventory

From the exact detached candidate, the independently verified Hatchling 1.29.0 build environment produced:

- `nvda_architecture_kernel-1.0.0-py3-none-any.whl` — 37,378 bytes — SHA-256
  `d311960234c932c2507f7b1671c8d53bff3ec234692e65ca27b440293e37e127`;
- `nvda_architecture_kernel-1.0.0.tar.gz` — 161,445 bytes — SHA-256
  `135e47f6ab531e8e650a2ee1adc9582965e1c81d97d08dfdc854757a790629fa`.

Both rebuilt artefacts are byte-for-byte identical to the Worker-supplied artefacts.

The wheel contains 21 files total and 16 runtime Python files. Those 16 files are byte-equal to every tracked
`src/nvda_desk/**/*.py` file and there is no extra runtime Python file. Metadata is exactly
`nvda-architecture-kernel==1.0.0`, Python `==3.13.5`, with pinned `PyYAML==6.0.3` and
`psycopg[binary]==3.3.4`. The sdist contains 117 files; every repository-backed member is byte-equal to the exact
candidate, with `PKG-INFO` the only generated member.

## Isolated installed-distribution challenge

A fresh external Python 3.13.5 environment installed the independently rebuilt exact wheel offline. `PYTHONPATH` was
unset, the repository path was absent from `sys.path`, and `nvda_desk` loaded only from external `site-packages`.
The installed `direct_url.json` binds the wheel to the exact SHA-256 above.

The installed package exposes only top-level `nvda_desk` runtime modules `architecture`, `composition` and
`raw_signal_occurrence_truth`. No P01/K01/provider/network/downstream-consumer/DMPV3/replay package was importable.

A direct Tester-authored public-seam challenge using the installed distribution and real PostgreSQL 17.9 established:

- `one_or_more_received` assessment;
- exact referential observation readback;
- durable unique policy/capture/observation/assessment rows `(1,1,1,1)`;
- idempotent fresh-application retry;
- fail-closed mismatched policy reference with zero erroneous capture rows.

The first draft of this Tester script passed a plain string where the public API requires a typed capture identity and
was correctly rejected. That was a Tester harness error; the script was corrected using the public typed constructor,
without any candidate/package mutation.

## Integrity

`git diff --check` passed, the detached candidate worktree remained clean, and `git fsck --full` returned success with
only eight pre-existing dangling blobs and no repository corruption/error.

## Disposition

`PASS`. No material VI-15-L2 finding was established. Candidate
`332c1f95da032f841e8779ef21fe3c1fceb698a2` and the exact wheel/sdist identities above are accepted for lawful
preserved-ancestry VI-15-L2 promotion/close-out only. VI-16 remains prohibited until that promotion succeeds.
