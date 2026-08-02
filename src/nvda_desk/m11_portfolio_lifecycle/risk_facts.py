"""M11 issuance of exact portfolio owner facts for M06 consumption."""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal

from nvda_desk.m06_parallel_risk.owner_facts import (
    ConcentrationOwnerFact,
    InventoryStressOwnerFact,
    build_owner_fact,
)

from .contracts import PortfolioSnapshot


class PortfolioRiskFactIssuer:
    """Issue M11-owned facts from one revalidated portfolio snapshot and explicit measurements."""

    def issue(
        self,
        *,
        snapshot: PortfolioSnapshot,
        position_market_value: Decimal,
        portfolio_gross_market_value: Decimal,
        concentration_warning_ratio: Decimal,
        concentration_block_ratio: Decimal,
        unencumbered_quantity: Decimal,
        inventory_warning_coverage_ratio: Decimal,
        inventory_block_coverage_ratio: Decimal,
        valid_until_utc: datetime,
        owner_policy_version: str = "m11.parallel-risk-facts.v1",
    ) -> tuple[ConcentrationOwnerFact, InventoryStressOwnerFact]:
        try:
            governed = PortfolioSnapshot.model_validate(snapshot.model_dump(mode="python"))
        except Exception as exc:
            raise ValueError("portfolio_snapshot_contract_invalid") from exc
        if len(governed.positions) != 1:
            raise ValueError("portfolio_risk_facts_require_one_position")
        if valid_until_utc.tzinfo is None or valid_until_utc.utcoffset() != UTC.utcoffset(
            valid_until_utc
        ):
            raise ValueError("owner_fact_time_must_be_utc")
        position = governed.positions[0]
        authority = (
            f"m11:{governed.snapshot_id}:{governed.semantic_fingerprint}",
            f"m11:{position.position_id}:{position.semantic_fingerprint}",
        )
        concentration_ratio = position_market_value / portfolio_gross_market_value
        concentration_condition = (
            "block"
            if concentration_ratio >= concentration_block_ratio
            else "caution" if concentration_ratio >= concentration_warning_ratio else "observe"
        )
        concentration_payload = {
            "owner_policy_version": owner_policy_version,
            "as_of_utc": governed.as_of_utc,
            "valid_until_utc": valid_until_utc,
            "authority_references": authority,
            "portfolio_snapshot_id": governed.snapshot_id,
            "portfolio_snapshot_fingerprint": governed.semantic_fingerprint,
            "portfolio_state_version": governed.state_version,
            "position_market_value": position_market_value,
            "portfolio_gross_market_value": portfolio_gross_market_value,
            "concentration_ratio": concentration_ratio,
            "warning_ratio": concentration_warning_ratio,
            "block_ratio": concentration_block_ratio,
            "condition": concentration_condition,
        }
        concentration = build_owner_fact(
            ConcentrationOwnerFact, "concentration-owner-fact", concentration_payload
        )

        coverage_ratio = unencumbered_quantity / position.quantity
        inventory_condition = (
            "block"
            if coverage_ratio <= inventory_block_coverage_ratio
            else "caution" if coverage_ratio <= inventory_warning_coverage_ratio else "observe"
        )
        inventory_payload = {
            "owner_policy_version": owner_policy_version,
            "as_of_utc": governed.as_of_utc,
            "valid_until_utc": valid_until_utc,
            "authority_references": authority,
            "portfolio_snapshot_id": governed.snapshot_id,
            "portfolio_snapshot_fingerprint": governed.semantic_fingerprint,
            "portfolio_state_version": governed.state_version,
            "position_quantity": position.quantity,
            "unencumbered_quantity": unencumbered_quantity,
            "coverage_ratio": coverage_ratio,
            "warning_coverage_ratio": inventory_warning_coverage_ratio,
            "block_coverage_ratio": inventory_block_coverage_ratio,
            "condition": inventory_condition,
        }
        inventory = build_owner_fact(
            InventoryStressOwnerFact, "inventory-owner-fact", inventory_payload
        )
        return concentration, inventory


__all__ = ["PortfolioRiskFactIssuer"]
