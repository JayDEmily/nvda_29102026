# VI-11R8 Tester Iteration 011 disposition

## Binding

Fresh independent Tester Iteration 011 reviewed:

- submitted source packet SHA-256
  `4921897beb1cab9598854edfeae5cd8f3f39ab21309d62926c29ca9cbf473135`;
- handoff `d1bad95bddd8b868449f2566b40d38126d50a789` / tree
  `160153440bbc0edc37cdc00387cb917737262dfb`;
- physical proof `7dc7ce0bb4d162d785bac5b0f431bdab77d954e7` / tree
  `134ddc76e61f9751e46cb1990c762ee028f86719`;
- Tester response SHA-256
  `55033b85f6e5143a07e7cfd97eaf4b71947e6d8e046ba4a9bc2b7c59b5e3f554`;
- Tester package SHA-256
  `9d86a906d8aa776c92c0059494958649fd4a0e641551868680a729e0b11c36f2`.

The independent verdict is `FAIL / RETURN_TO_WORKER`. VI-12R remains prohibited.

## Environmental disposition

The tester expressly did not reject the degraded-TCP environment. The nine mapped
namespace/filesystem propositions remain `UNPROVED`, are not passes, and may remain an explicit
caveat under current Programme Owner direction.

## Findings routed to VI-10R9

### T011-F001 — Critical — SyncRep observation not bound to the semantic write

The barrier was installed before the child constructed its owner. A setup, schema-ensure or audit
transaction during `create_owner()` using the same `application_name` could therefore satisfy the
first observed `SyncRep` wait. Releasing that wait before the selected command ran left a false
positive path for an early-returning semantic write.

### T011-F002 — Critical — concrete adapter capability can escape through external storage

The proof traversed instance attributes, containers, partials and closures but explicitly skipped
classes and modules and did not inspect slots or referenced globals. The tester demonstrated that
`type(self)._cached = adapter._semantic_decision` survived the rewrite, remained callable and was
missed by the post-rewrite identity checker.

## Owning-layer disposition

Both findings remain proof-layer defects. They do not change IRB/BICP/IWO/METHOD-006 meaning,
product obligations, architecture proof configuration or production scope. VI-10R9 must:

1. construct the owner and command inputs before a proof-owned `READY`, install the server barrier
   only after `READY`, and permit the semantic command only after parent `GO`; and
2. fail closed on concrete adapter identity or bound capability stored through class/MRO state,
   slots, referenced globals or modules, with implementation-independent canaries.

The failed Iteration 011 target remains preserved in ordinary Git ancestry. Fresh Tester
Iteration 012 must review a genuinely new physical proof state before VI-12R can begin.
