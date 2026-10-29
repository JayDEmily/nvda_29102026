# VI-15-L2 — Independent Tester disposition

## Disposition

**PASS**

## Exact reviewed state

- candidate commit: `332c1f95da032f841e8779ef21fe3c1fceb698a2`;
- candidate tree: `3abec93134d128978ad6bcedbd0dfa6cf4334ec6`;
- accepted VI-15-L1 predecessor: `abccadf20d10daa29e739c6ba54a970fcff41614`;
- Tester cycle: `TESTER_VI15_L2_1790584579`;
- received packet SHA-256: `b05ceb2b46c7b222ef397564587b7c0c4df77eceda8edc58f1727017ec0d57b9`.

The candidate is an empty boundary commit over routed parent `3b1671dc0c15e5ab9023bd20362c432b1fd7a05a`;
both have the same tree. Review used a detached exact-candidate worktree.

## Independent proof

- complete admitted product population: **479/479 PASS**;
- product-proof control: six admitted families, **13/13** required obligations covered;
- architecture/bootstrap blocking set: **74/74 PASS** across 11 current-blocking families;
- mypy: PASS, 16 source files;
- Ruff: PASS.

The first attempt to run the complete product aggregate as one process exceeded the command wrapper time before pytest
printed a terminal result. That incomplete execution was not counted. The same governed population was then executed
independently as five non-U05 families (**424/424**) plus all 55 U05 PostgreSQL cases in bounded groups (**55/55**).

## Exact package proof

Independent rebuild from the exact detached candidate with Python 3.13.5 / Hatchling 1.29.0 produced:

| Artefact | Bytes | SHA-256 |
| --- | ---: | --- |
| `nvda_architecture_kernel-1.0.0-py3-none-any.whl` | 37,378 | `d311960234c932c2507f7b1671c8d53bff3ec234692e65ca27b440293e37e127` |
| `nvda_architecture_kernel-1.0.0.tar.gz` | 161,445 | `135e47f6ab531e8e650a2ee1adc9582965e1c81d97d08dfdc854757a790629fa` |

Both were byte-for-byte identical to the Worker-supplied artefacts.

The wheel has 21 files total and exactly 16 Python runtime files, byte-equal to all tracked `src/nvda_desk/**/*.py`
files. Its metadata is exactly `nvda-architecture-kernel==1.0.0`, with Python `==3.13.5`, `PyYAML==6.0.3` and
`psycopg[binary]==3.3.4`. The sdist has 117 files; every repository-backed member is byte-equal to the candidate and
`PKG-INFO` is the only generated member.

## Installed-distribution challenge

A fresh external Python 3.13.5 venv installed the exact rebuilt wheel offline. `PYTHONPATH` was unset, the repository
path was absent from `sys.path`, and `nvda_desk` loaded from external `site-packages`. The installed archive identity
was bound by `direct_url.json` to the wheel SHA-256 above.

Installed top-level runtime packages were exactly:

- `nvda_desk.architecture`;
- `nvda_desk.composition`;
- `nvda_desk.raw_signal_occurrence_truth`.

No P01, K01, provider/network, downstream-consumer, DMPV3 or replay runtime package was importable.

A direct Tester-authored A00 -> PostgreSQL-backed M00 public-seam sequence against PostgreSQL 17.9 established exact
observation readback, `one_or_more_received`, durable unique rows `(1,1,1,1)`, fresh-application idempotent retry and
fail-closed mismatched policy reference with no erroneous capture row.

The first draft of the Tester challenge supplied a plain string for a typed capture identity and the installed package
correctly rejected it. This was a Tester harness error and was corrected without changing candidate/package bytes.

## Environment and integrity

The preserved proof environment was independently rebound to its recorded archive hashes and verified as Python 3.13.5,
pytest 9.0.3, mypy 1.20.1, Ruff 0.15.11, Psycopg 3.3.4 and PostgreSQL 17.9 with UTF8, `fsync=on`,
`synchronous_commit=on`, `full_page_writes=on` and Unix-socket-only transport.

The exact candidate worktree remained clean; `git diff --check` passed; `git fsck --full` returned success with eight
dangling blobs only and no corruption/error.

## Acceptance boundary

No material VI-15-L2 finding was established. The exact candidate and package identities above are accepted only for
preserved-ancestry VI-15-L2 promotion/close-out. VI-16 remains prohibited until that promotion succeeds and the current
state is lawfully advanced.
