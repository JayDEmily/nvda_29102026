"""Tier A proof for exact M06 concentration, inventory and liquidity owner facts."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest
from tests.support.m06_k10_contract_harness import make_prepared
from tests.support.m11_k16_k17_contract_harness import production_execution_receipt

from nvda_desk.m06_parallel_risk import (
    LiquidityOwnerFact,
    ParallelRiskEvaluator,
    ParallelRiskInput,
    ParallelRiskOwnerFacts,
)
from nvda_desk.m11_portfolio_lifecycle import (
    PortfolioLifecycleService,
    PortfolioRiskFactIssuer,
)

TEST_NOW = datetime(2026, 8, 1, 2, 30, tzinfo=UTC)


def _portfolio_facts(*, concentration: str = "0.25", inventory_coverage: str = "0.90"):
    service = PortfolioLifecycleService()
    snapshot = service.reconcile_fill(production_execution_receipt()).snapshot
    position = snapshot.positions[0]
    concentration_ratio = Decimal(concentration)
    inventory_ratio = Decimal(inventory_coverage)
    concentration_fact, inventory_fact = PortfolioRiskFactIssuer().issue(
        snapshot=snapshot,
        position_market_value=Decimal("100000") * concentration_ratio,
        portfolio_gross_market_value=Decimal("100000"),
        concentration_warning_ratio=Decimal("0.40"),
        concentration_block_ratio=Decimal("0.60"),
        unencumbered_quantity=position.quantity * inventory_ratio,
        inventory_warning_coverage_ratio=Decimal("0.50"),
        inventory_block_coverage_ratio=Decimal("0.20"),
        valid_until_utc=snapshot.as_of_utc + timedelta(hours=1),
    )
    return concentration_fact, inventory_fact


def _liquidity_fact(*, coverage: str = "2.0", stale: bool = False) -> LiquidityOwnerFact:
    prepared = make_prepared(now=TEST_NOW)
    as_of = prepared.effective_at_utc - (timedelta(hours=2) if stale else timedelta(minutes=1))
    valid_until = as_of + timedelta(minutes=30)
    return LiquidityOwnerFact.issue(
        provider_id="provider.paper.depth.v1",
        source_capture_refs=prepared.source_capture_refs,
        as_of_utc=as_of,
        valid_until_utc=valid_until,
        required_notional=Decimal("10000"),
        available_notional=Decimal("10000") * Decimal(coverage),
        warning_coverage_ratio=Decimal("1.0"),
        block_coverage_ratio=Decimal("0.5"),
        owner_policy_version="m01.liquidity-coverage.v1",
    )


def _input(owner_facts: ParallelRiskOwnerFacts | None = None) -> ParallelRiskInput:
    return ParallelRiskInput.from_prepared(
        make_prepared(vix_level=18.0, now=TEST_NOW),
        evaluator_policy_version="parallel-risk.compat.v1",
        aggregation_version="parallel-risk.aggregate.v1",
        threshold_authority_refs=("m07:caution:v1", "m07:block:v1"),
        vix_caution_threshold=30.0,
        vix_block_threshold=50.0,
        owner_facts=owner_facts,
    )


def test_m11_issues_exact_snapshot_bound_portfolio_facts() -> None:
    concentration, inventory = _portfolio_facts()
    assert concentration.owner_module == "M11"
    assert inventory.owner_module == "M11"
    assert concentration.portfolio_snapshot_id == inventory.portfolio_snapshot_id
    assert concentration.condition == "observe"
    assert inventory.condition == "observe"
    assert all(ref.startswith("m11:") for ref in concentration.authority_references)


def test_complete_current_owner_facts_remove_three_unknown_families() -> None:
    concentration, inventory = _portfolio_facts()
    facts = ParallelRiskOwnerFacts.build(
        concentration=concentration,
        inventory_stress=inventory,
        liquidity=_liquidity_fact(),
    )
    result = ParallelRiskEvaluator().evaluate(_input(facts))
    by_family = {item.family: item for item in result.observations}
    assert by_family["concentration"].state == "observe"
    assert by_family["inventory_stress"].state == "observe"
    assert by_family["liquidity"].state == "observe"
    assert not {"concentration", "inventory_stress", "liquidity"} & set(result.unknown_families)


def test_owner_caution_and_block_conditions_map_without_recalculation() -> None:
    concentration, inventory = _portfolio_facts(concentration="0.45", inventory_coverage="0.10")
    facts = ParallelRiskOwnerFacts.build(
        concentration=concentration,
        inventory_stress=inventory,
        liquidity=_liquidity_fact(coverage="0.75"),
    )
    result = ParallelRiskEvaluator().evaluate(_input(facts))
    by_family = {item.family: item for item in result.observations}
    assert by_family["concentration"].state == "caution"
    assert by_family["inventory_stress"].state == "block"
    assert by_family["liquidity"].state == "caution"
    assert result.state == "block"


def test_stale_owner_fact_is_explicit_unknown_not_safe() -> None:
    concentration, inventory = _portfolio_facts()
    facts = ParallelRiskOwnerFacts.build(
        concentration=concentration,
        inventory_stress=inventory,
        liquidity=_liquidity_fact(stale=True),
    )
    result = ParallelRiskEvaluator().evaluate(_input(facts))
    liquidity = next(item for item in result.observations if item.family == "liquidity")
    assert liquidity.state == "unknown"
    assert liquidity.reason == "liquidity_owner_fact_stale"
    assert liquidity.limitation == "liquidity_owner_fact_stale"


def test_absent_owner_facts_preserve_explicit_unknowns() -> None:
    result = ParallelRiskEvaluator().evaluate(_input())
    assert {"concentration", "inventory_stress", "liquidity"}.issubset(set(result.unknown_families))


def test_forged_owner_fact_or_bundle_is_rejected() -> None:
    concentration, inventory = _portfolio_facts()
    with pytest.raises(ValueError, match="owner_fact_fingerprint_mismatch"):
        concentration.model_copy(update={"owner_policy_version": "m11.forged.v9"}).model_validate(
            concentration.model_copy(update={"owner_policy_version": "m11.forged.v9"}).model_dump(
                mode="python"
            )
        )
    facts = ParallelRiskOwnerFacts.build(
        concentration=concentration,
        inventory_stress=inventory,
        liquidity=_liquidity_fact(),
    )
    forged = facts.model_copy(update={"semantic_fingerprint": "0" * 64})
    with pytest.raises(ValueError, match="parallel_risk_owner_facts_fingerprint_mismatch"):
        _input(forged)
