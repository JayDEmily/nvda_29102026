# NVDA API DTO and broker-boundary resolution tranche v1 — closeout report

Date: 2026-04-20
Active branch: `work/api-dto-broker-boundary-resolution-tranche-v1-20260420`
Accepted baseline promoted to `main` before tranche start: `aa4bad4728a0ea1cfc72570337584f1c8cc11a42`
Observed pre-promotion `main`: `3556388e0b76bc90676a48a5539906b491aeeb7a`

## Direct answer

This tranche closed both queued reservations truthfully.

- API DTO reservation closed as **dedicated adapter retained and explicitly used from the bounded API shell**.
- Broker-boundary reservation closed as **protocol-only boundary retained, with no concrete broker implementation admitted**.

No prohibited surface was widened.

## Leaf chronology

1. `d4dd7aa` — reservation audit and admissibility note
2. `750f956` — API DTO boundary resolution
3. `a505035` — broker-boundary resolution
4. `9981f94` — minimum truthful proof mirror
5. tranche closeout commit — this report, brief lineage copy, and workbook reconciliation

## What changed

### API DTO reservation

Observed directly after closure:

- `src/nvda_desk/adapters/egress/api_dto_adapter.py` now owns explicit DTO projection through `ApiDtoAdapter.to_runtime_dto`, `to_review_dto`, and `to_state_dto`.
- `src/nvda_desk/api/deps.py` now exposes `get_api_dto_adapter()`.
- `src/nvda_desk/api/app.py` now injects the admitted DTO adapter into `HttpApp` and routes both `healthcheck()` and `run_once()` through that boundary owner.

Truth judgement:

- the current API shell still exposes only `healthcheck` and `run_once`;
- the shell already returned dictionary-safe payloads before this tranche;
- the reservation remained open because DTO projection was implicit rather than explicit;
- retaining the dedicated adapter and using it explicitly closes the reservation without widening routes, transport plumbing, or API contract families.

### Broker-boundary reservation

Observed directly after closure:

- `src/nvda_desk/adapters/egress/broker_protocol.py` now exposes a protocol-only `BrokerGatewayProtocol` with bounded methods:
  - `submit_order_intent`
  - `read_order_events`
  - `read_fill_events`
  - `read_positions`
- `BrokerProtocol` is retained as a compatibility alias to that protocol surface.
- no `PaperBrokerAdapter` or `LiveBrokerAdapter` implementation was admitted.

Truth judgement:

- the repo still contains execution-record and execution-event persistence shells, but no native concrete broker adapter implementation;
- no API, entry, runtime, repository, or persistence path instantiates a broker adapter;
- admitting a paper or live adapter here would fabricate capability not present in the repo.

Therefore the truthful closeout state is protocol-only plus proof.

## Proof run

### Targeted tranche proof

```bash
PYTHONPATH=src pytest -q tests/tier_a/api/test_api_dto_boundary_surface.py tests/tier_a/adapters_egress/test_broker_boundary_surface.py
```

Observed output:

- `4 passed in 1.06s`

```bash
python3 -m compileall src/nvda_desk/api src/nvda_desk/adapters/egress tests/tier_a/api tests/tier_a/adapters_egress
```

Observed output:

- clean

Additional bounded smoke used during closure:

```bash
PYTHONPATH=src python3 - <<'PY'
from nvda_desk.api.app import create_app
app = create_app()
assert app.healthcheck() == {'status': 'ok'}
receipt = app.run_once({'temporal': {'present': True}})
assert receipt['executed_stages'] == ['temporal']
print('api dto smoke -> ok')
PY
```

Observed output:

- `api dto smoke -> ok`

```bash
PYTHONPATH=src python3 - <<'PY'
from nvda_desk.adapters.egress.broker_protocol import BrokerGatewayProtocol, BrokerProtocol
assert BrokerProtocol is BrokerGatewayProtocol
print('broker protocol smoke -> ok')
PY
```

Observed output:

- `broker protocol smoke -> ok`

### Tranche proof floor

```bash
PYTHONPATH=src pytest -q tests/tier_a tests/tier_b
```

Observed output:

- `100 passed in 2.00s`

```bash
python3 -m compileall src tests/tier_a tests/tier_b
```

Observed output:

- clean

## Registry and proof surfaces admitted

- `tests/tier_a/api/test_api_dto_boundary_surface.py`
- `tests/tier_a/adapters_egress/test_broker_boundary_surface.py`
- `config/retained_test_registry.yaml`

The retained registry now admits:

- the new Tier A family root `tests/tier_a/adapters_egress/`
- `api_dto_boundary_surface`
- `broker_boundary_protocol_surface`

## Deferred truth retained intentionally

This tranche did **not** admit:

- new API routes
- transport plumbing
- broker credentials
- network execution logic
- paper-trading adapters
- live broker adapters
- `analysis.scenarios`
- `observability`
- `legacy.imported`

## Benchmark-home state after closeout

Observed benchmark-home count remains `21 / 24`.

Remaining absent benchmark homes:

- `src/nvda_desk/legacy/imported/`
- `src/nvda_desk/analysis/scenarios/`
- `src/nvda_desk/observability/`

No new top-level benchmark home was created in this tranche. The reservation work here was bounded to explicit boundary truth and proof.
