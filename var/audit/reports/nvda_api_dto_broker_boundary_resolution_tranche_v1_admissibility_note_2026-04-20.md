# NVDA API DTO and broker-boundary resolution tranche v1 — admissibility note

Date: 2026-04-20
Active branch: `work/api-dto-broker-boundary-resolution-tranche-v1-20260420`
Repo baseline reviewed before tranche work: `main` promoted to `aa4bad4728a0ea1cfc72570337584f1c8cc11a42`

## Question set answered

### 1. What are the actual current producers and consumers of API boundary outputs?

Observed directly:

- `src/nvda_desk/api/app.py` currently produces the only bounded API outputs through `HttpApp.healthcheck()` and `HttpApp.run_once()`.
- `src/nvda_desk/api/http/app.py` is only a compatibility wrapper over `nvda_desk.api.app`.
- `src/nvda_desk/entry/asgi.py` consumes the bounded API shell by calling `create_boundary_app()`.
- `src/nvda_desk/entry/cli.py` consumes the bounded API shell by calling `boundary_app.run_once(...)`.
- no other native source files currently call `api_dto_adapter.py`.

Search evidence used during this leaf:

```bash
rg -n "api_dto_adapter|ApiDtoAdapter|to_runtime_dto|to_review_dto|to_state_dto" src tests
```

Observed result: no native call sites at tranche start.

### 2. Does the current API shell need an explicit DTO projection step?

Yes.

Reason:

- the current shell returns plain dictionaries already, so the shell is not presently leaking dataclass or Pydantic packet objects;
- however, the workbook reservation remains open because the public-boundary projection step is still implicit rather than explicit;
- the benchmark workbook and traceability appendix name `adapters/egress/api_dto_adapter.py` as the provisional boundary home for that projection.

Therefore the truthful bounded closure is to make DTO projection explicit at the current API shell rather than pretending the reservation closed merely because the existing payloads happen to be dictionary-shaped.

### 3. Should DTO projection remain in `adapters/egress/api_dto_adapter.py` or move route-local?

`adapters/egress/api_dto_adapter.py` should remain the admitted boundary owner in this tranche.

Reason:

- the current shell has only two bounded outputs and no real transport stack;
- keeping the projection in the dedicated adapter closes the reservation without widening route-local web plumbing or creating an `api/contracts` subtree that this tranche did not admit;
- the workbook explicitly reserves that module cut and allows the adapter to remain the truthful answer.

### 4. Are there any native concrete broker implementations already present?

No.

Search evidence used during this leaf:

```bash
rg -n "broker_protocol|BrokerGatewayProtocol|PaperBrokerAdapter|LiveBrokerAdapter|submit_order_intent|read_order_events|read_fill_events|read_positions" src tests
```

Observed result:

- only `src/nvda_desk/adapters/egress/broker_protocol.py` matched;
- no native `PaperBrokerAdapter` or `LiveBrokerAdapter` implementation exists;
- no runtime, repository, API, or entry file instantiates a concrete broker adapter.

Related current-state evidence:

- `src/nvda_desk/persistence/execution_records.py` is an append-only in-memory execution-record store;
- `src/nvda_desk/repositories/execution_event_repository.py` is an append-only in-memory execution-event store;
- neither file performs broker IO or implements the reserved broker boundary.

### 5. Is the truthful broker answer protocol-only plus proof?

Yes.

The repo contains no admissible native concrete broker implementation set. Creating paper or live broker adapters in this tranche would fabricate capability that is not present in the current repo state and would violate the brief stop boundary.

## Admissibility decision

This tranche is admissible with the following bounded closures:

1. retain `src/nvda_desk/adapters/egress/api_dto_adapter.py` as the dedicated DTO projection owner and make its use explicit from `src/nvda_desk/api/app.py`;
2. retain `src/nvda_desk/adapters/egress/broker_protocol.py` as a protocol-only boundary and benchmark-reconcile its protocol shape without adding concrete implementations;
3. admit only the minimum Tier A proof needed to make those two truths visible.

## Prohibited expansions reaffirmed

This leaf did **not** prove admissibility for:

- new routes;
- transport plumbing;
- live broker execution;
- paper-trading adapters;
- `analysis.scenarios`;
- `observability`;
- `legacy.imported`;
- entry or CLI widening.
