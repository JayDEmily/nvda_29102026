# VI-11R6 Tester Iteration 009 disposition

## Binding

Fresh independent Tester Iteration 009 reviewed:

- wrapper `ffa57057091b52a9abe54cb87cd1827c8dc76f4f` / tree `6b41fe3e9b281c4beeab68ae1e3a2f3ffef185e1`;
- physical proof `355497c8db9cd1f615539634ddb5fa5bea5d405d` / tree `1798b78addf2d81cfd08e1de42944afc94910b92`;
- repair/control parent `7eb85b097dd4e05705cc781fd102bddf0f6762ca`;
- submitted archive SHA-256 `70174e024783e5bdf0420a17e13e815a707be2c5ea3e88fb45f2114780c6bbb7`.

The independent verdict is `FAIL / RETURN_TO_WORKER`. VI-12R remains prohibited.

## Findings routed to VI-10R7

- `T009-F001` — **Critical** — the client PID-tree return barrier does not prove PostgreSQL server-side COMMIT acknowledgement causally precedes public method return.
- `T009-F002` — **Critical** — the default PostgreSQL mechanism can still expose private semantic capabilities that the owner could invoke while presenting a record-only public protocol.
- `T009-F003` — **Important** — exact public-seam typing covers contract/identity-bearing parameters but not every parameter and return type across all eleven facets.
- `T009-F004` — **Critical** — native numeric fidelity omits `Decimal`, including catalogue-backed IBKR `R038` Last Size.

## Prior-finding status

The tester records `T008-F001` and `T008-F005` as closed, while `T008-F002..F004` remain open through the findings above. No closed finding is to be weakened or removed during VI-10R7.

## Owning-layer disposition

All four current findings are proof-layer defects. They do not authorise production implementation or a change to IRB/BICP/IWO/METHOD-006 meaning. The existing Programme Owner catalogue direction remains unchanged: `R001`–`R323` may be carried as separately typed provenance; workbook bounds and `D001+` behaviour remain outside this tranche.

The next lawful action is a genuinely new VI-10R7 physical proof successor followed by fresh independent Tester Iteration 010 review.
