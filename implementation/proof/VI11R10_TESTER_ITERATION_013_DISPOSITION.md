# VI-11R10 Tester Iteration 013 disposition

## Binding

Fresh independent Tester Iteration 013 reviewed:

- submitted source packet SHA-256
  `f67ef9c88c9b6470f46200815f5ac4b29505f3ce309a6a3ca482eeb6832280b3`;
- submitted handoff `2b17c3b545242475889b85aa158000f443f4ca65` / tree
  `1cc95061579ffb2aad4743490ac38f2eb10685cb`;
- physical proof `548a61107fda52e643142542ddb60dee584bd46e` / tree
  `e4e0850990545b46d57bb8241596fa1e51c60451`;
- Tester response SHA-256
  `69f2bf610d1e3ae66752c6b7a3a3b32bdbcb5528f8b74298dcf7ffa5becf2a68`;
- Tester continuity `39b5ca75e74ecd5cdee50c66c3a26fe3f34aec65` / tree
  `b044dae0738d9a7bf416319dc18bc7ea59c379b9`;
- Tester package SHA-256
  `1ee53d2c546ce8d31557d00b1c35cd654deb00e35bd46f6a11404945b9a5ad3d`.

The independent verdict is `FAIL / RETURN_TO_WORKER`. VI-12R remains prohibited.

## Environmental disposition

The verdict is not based on the degraded-TCP/namespace environment. The nine mapped
namespace/filesystem propositions remain `UNPROVED`, are not passes and are not a rejection basis.
Tester Iteration 013 independently executed the database-backed cases against PostgreSQL 17.9 and
the exact Python 3.13.5 project environment.

## Findings routed to VI-10R11

### T013-F001 — Critical — marker XID can name audit identity rather than semantic payload

The submitted proof inferred the semantic transaction by finding rows containing one literal
identity marker. A normalised representation can write that marker to an audit/identity row in the
waited transaction, then commit the actual payload in a later transaction joined by a surrogate.
Fresh semantic readback succeeds while the marker helper sees only the waited transaction and the
predicate returns a false positive.

### T013-F002 — Critical — injected proxy contains the concrete adapter

The submitted record-only proxy stored the concrete adapter as `self._inner`. The graph checker and
rewriter treated that proxy as opaque, so a semantic owner could recover `_port._inner`, execute a
private adapter semantic method and still satisfy the submitted no-capability check.

## Owning-layer disposition

Both findings are accepted proof-layer defects. They do not change IRB/BICP/IWO/METHOD-006 meaning,
product obligations, architecture proof configuration or production scope. VI-10R11 must:

1. observe transaction identity at the post-`GO` database-write boundary without relying on
   marker text, reject any multi-XID semantic append and fail closed on a newly created untraced
   durable relation; and
2. inject a genuinely record-only capability whose reachable state contains no concrete adapter,
   with private/non-protocol dispatch rejected at the capability boundary itself.

The failed Iteration 013 target and the tester continuity commit remain preserved in ordinary Git
ancestry. Fresh Tester Iteration 014 must review a genuinely new physical proof state before VI-12R
can begin.
