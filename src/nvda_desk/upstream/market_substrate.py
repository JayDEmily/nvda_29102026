from __future__ import annotations

from collections.abc import Iterable

from nvda_desk.contracts.market_substrate import (
    MarketSubstrateObservation,
    MarketSubstrateSnapshot,
)


def build_market_substrate_snapshot(
    *, substrate_id: str, observations: Iterable[MarketSubstrateObservation]
) -> MarketSubstrateSnapshot:
    copied = [observation.model_copy(deep=True) for observation in observations]
    observation_ids = [observation.observation_id for observation in copied]
    duplicate_ids = sorted(
        {
            observation_id
            for observation_id in observation_ids
            if observation_ids.count(observation_id) > 1
        }
    )
    if duplicate_ids:
        raise ValueError(f"duplicate market substrate observations: {duplicate_ids}")
    return MarketSubstrateSnapshot(substrate_id=substrate_id, observations=copied)
