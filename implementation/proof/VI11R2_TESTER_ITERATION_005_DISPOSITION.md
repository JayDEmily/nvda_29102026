# VI-11R2 Tester Iteration 005 Disposition

## Status

`FAIL / RETURN_TO_WORKER — ROUTED TO VI-10R3 PROOF REPAIR`

Fresh independent VI-11R2 review of the VI-10R2 successor returned eleven material proof-adequacy findings: four Critical and seven Important. The reviewed wrapper and frozen physical proof remain preserved in Git history. Production implementation remains prohibited.

## Exact review binding

- tester archive SHA-256: `e4dd373e1a4a54039a3dbee58f5777844a731df80ba6e57dee856e30b91c84c6`
- tester response SHA-256: `c6d675d86660c1f082b022676f9a13dc2bb9b811ad05ba6fdfa324c25b988cbf`
- reviewed wrapper HEAD: `c164facaf011f2dc2da7ebcb2d90790b755c8782`
- reviewed wrapper tree: `e2062af6d64e29eaaf27340c929ee0d6b70f9d35`
- reviewed physical proof candidate: `56ea445d4bb5055b9fc39114bcd3c529b7f0bae5`
- reviewed physical proof tree: `b925e086a734492457dd9633a04743aa0c3c0471`
- repair baseline: `a4c5ebc0c242c446ce14fee2c341e72ca2764212`

The tester independently verified transport, all 52 internal hashes, Git identity, 353-test collection, 13/13 structural obligation coverage, architecture/bootstrap 74/74, mypy, Ruff, dependency and public-seam validation. The failure is substantive proof adequacy.

## Findings and owning repair

| Finding | Severity | Required proof repair |
|---|---|---|
| `T005-F001` | Critical | prove PostgreSQL is the only durable cross-process semantic source and that complete independently known facts are recovered from it |
| `T005-F002` | Critical | observe command success before writer shutdown and prove each semantic fact is independently committed before later commands |
| `T005-F003` | Important | compare fresh-process readback to independently canonicalised pre-write authoritative input, not writer-returned output |
| `T005-F004` | Important | fail closed on unproved extra v1 fields and reject aware non-UTC values in every `_utc` field |
| `T005-F005` | Important | prove per-scope ingestion high-water state survives interleaving and return to a prior scope |
| `T005-F006` | Critical | inspect the complete owner/technical-mechanism boundary independent of filenames and prove the default persistence path is semantic-free |
| `T005-F007` | Important | require A00 capture realisation to consume the exact registered/effective policy reference |
| `T005-F008` | Important | reject unaligned/ill-ordered policy validity and prove v2 owns its first activation-boundary slot |
| `T005-F009` | Important | prove both halves of `[start,end)` and use a typed-but-nonexistent capture identity for missing authority |
| `T005-F010` | Critical | prove ineligible/out-of-slot observations cannot produce `one_or_more_received` assessments |
| `T005-F011` | Important | compare complete reconciled capture facts to independently derived expected owed schedule/policy identity |

## Authority disposition

The findings remain downstream proof defects. They do not alter the accepted IRB, BICP, IWO, routed METHOD-006 normatives, architecture allocation, six-family decomposition, thirteen product obligations or product tier treatment.

Under the accepted ExecPlan owning-layer rule, all eleven findings return to successor pre-implementation proof repair. No `src/nvda_desk/**` production behaviour is authorised until a fresh independent VI-11R3 rechallenge accepts the successor proof candidate.
