# VI-11R9 Tester Iteration 012 disposition

## Binding

Fresh independent Tester Iteration 012 reviewed:

- submitted source packet SHA-256
  `d3d4f8000f2e7ee6e00ddef2973551a37ca680ea49112796be82d31fe88b7538`;
- handoff `36bba0d26b988881812d2333f7e1eb3e8e63786b` / tree
  `05a281546277125afa4361d8ec1eac3767d23022`;
- physical proof `0917e0319a460a6d7ffb40b776b716f80f8f8684` / tree
  `fd5a1cb626f1fb7c41602f989d5f900c080f9537`;
- Tester response SHA-256
  `c4dfccd96158991842c0ddb605ada7346609740cfb00aec3a9a17c976955f714`;
- Tester package SHA-256
  `a8c7f376171b7a5a1499ba5a6011b1e307b4ff7d4015cd37deaf4cea3c06c477`.

The independent verdict is `FAIL / RETURN_TO_WORKER`. VI-12R remains prohibited.

## Environmental disposition

The tester expressly did not reject the degraded-TCP environment. The nine mapped
namespace/filesystem propositions remain `UNPROVED`, are not passes, and are not the basis of
either finding below.

## Findings routed to VI-10R10

### T012-F001 — Critical — SyncRep wait remains unbound to the semantic transaction

`READY` excludes owner construction before the barrier is armed, but does not exclude a
command-local schema, setup or audit transaction after `GO`. That transaction can consume the
first `SyncRep` wait. Releasing the global barrier then lets a later semantic transaction return
before its own server acknowledgement.

### T012-F002 — Critical — weak references retain concrete adapter capability

The expanded graph traversal misses dereferenceable weak references and proxies. A semantic owner
can retain `weakref.ref(concrete_adapter)`, survive the direct-port rewrite, recover the concrete
adapter and call private semantic capability while the post-rewrite checker reports no adapter
identity.

## Owning-layer disposition

Both findings remain proof-layer defects. They do not change IRB/BICP/IWO/METHOD-006 meaning,
product obligations, architecture proof configuration or production scope. VI-10R10 must:

1. carry the waiting PostgreSQL transaction identity forward and correlate it to the rows carrying
   the exact expected semantic identity, rejecting any setup/audit and semantic rows committed by
   different transactions; and
2. construct the semantic owner with the record-only injected persistence capability and fail
   closed on live weak references, weak methods and weak proxies to the concrete adapter.

The failed Iteration 012 target remains preserved in ordinary Git ancestry. Fresh Tester
Iteration 013 must review a genuinely new physical proof state before VI-12R can begin.
