from __future__ import annotations

from pathlib import Path

import pytest
from pydantic import ValidationError

from nvda_desk.config.playbook_registry import (
    PlaybookRegistryDocument,
    build_playbook_metadata_receipts,
    load_playbook_registry,
)
from nvda_desk.contracts.eligibility import (
    EligibilityAdmissibilitySurface,
    PlaybookEligibilityOutput,
)
from nvda_desk.contracts.playbook import (
    PlaybookDefinition,
    PlaybookEligibilityConstraint,
    PlaybookMetadataReceipt,
)
from nvda_desk.contracts.posture import PermissionState
from nvda_desk.playbooks.library import select_playbook_metadata_receipts


def _registry() -> PlaybookRegistryDocument:
    return PlaybookRegistryDocument(
        schema_version="playbook_registry.v1",
        registry_id="registry-test",
        playbooks=(
            PlaybookDefinition(
                playbook_id="gap_up_follow_through",
                setup_family="gap_up",
                setup_variant_ids=("gap_up.baseline", "gap_up.risk_defined"),
                eligibility_constraints=(
                    PlaybookEligibilityConstraint(
                        constraint_id="permission_allow_or_derisk",
                        constraint_type="permission_state",
                        allowed_values=("allow", "derisk"),
                    ),
                ),
                selection_metadata={"setup_family": "gap_up", "timeframe": "intraday"},
            ),
            PlaybookDefinition(
                playbook_id="volatility_mean_reversion",
                setup_family="volatility_reversion",
                setup_variant_ids=("volatility_reversion.baseline",),
                eligibility_constraints=(),
                selection_metadata={"setup_family": "volatility_reversion"},
                enabled=False,
            ),
        ),
    )


def test_playbook_registry_rejects_duplicate_playbook_ids() -> None:
    first = PlaybookDefinition(
        playbook_id="gap_up_follow_through",
        setup_family="gap_up",
        setup_variant_ids=("gap_up.baseline",),
    )
    second = PlaybookDefinition(
        playbook_id="gap_up_follow_through",
        setup_family="gap_up",
        setup_variant_ids=("gap_up.risk_defined",),
    )

    with pytest.raises(ValidationError, match="duplicate playbook_id"):
        PlaybookRegistryDocument(
            schema_version="playbook_registry.v1",
            registry_id="registry-test",
            playbooks=(first, second),
        )


def test_playbook_definition_rejects_duplicate_setup_variant_ids() -> None:
    with pytest.raises(ValidationError, match="duplicate setup_variant_id"):
        PlaybookDefinition(
            playbook_id="gap_up_follow_through",
            setup_family="gap_up",
            setup_variant_ids=("gap_up.baseline", "gap_up.baseline"),
        )


def test_playbook_definition_rejects_hidden_authority_keys() -> None:
    with pytest.raises(ValidationError, match="hidden playbook authority key"):
        PlaybookDefinition(
            playbook_id="gap_up_follow_through",
            setup_family="gap_up",
            setup_variant_ids=("gap_up.baseline",),
            selection_metadata={"nested": {"capital_deployment": "not_allowed"}},
        )


def test_playbook_constraint_metadata_rejects_hidden_authority_keys() -> None:
    with pytest.raises(ValidationError, match="hidden playbook authority key"):
        PlaybookEligibilityConstraint(
            constraint_id="permission_allow_or_derisk",
            constraint_type="permission_state",
            allowed_values=("allow", "derisk"),
            metadata={"broker_placement": {"side": "buy"}},
        )


def test_playbook_constraint_rejects_duplicate_allowed_values() -> None:
    with pytest.raises(ValidationError, match="duplicate allowed value"):
        PlaybookEligibilityConstraint(
            constraint_id="permission_allow_or_derisk",
            constraint_type="permission_state",
            allowed_values=("allow", "allow"),
        )


def test_playbook_registry_metadata_rejects_hidden_authority_keys() -> None:
    with pytest.raises(ValidationError, match="hidden playbook authority key"):
        PlaybookRegistryDocument(
            schema_version="playbook_registry.v1",
            registry_id="registry-test",
            playbooks=(),
            registry_metadata={"live_order_execution": True},
        )


def test_playbook_metadata_receipts_are_deterministic_and_copy_safe() -> None:
    registry = _registry()
    receipts = build_playbook_metadata_receipts(registry)

    assert [receipt.playbook_id for receipt in receipts] == [
        "gap_up_follow_through",
        "gap_up_follow_through",
    ]
    assert receipts[0].receipt_id == "registry-test:gap_up_follow_through:gap_up.baseline"
    assert receipts[1].receipt_id == "registry-test:gap_up_follow_through:gap_up.risk_defined"
    assert receipts[0].source_registry_fingerprint == receipts[1].source_registry_fingerprint

    copied = receipts[0].model_copy(deep=True)
    copied.selection_metadata["setup_family"] = "mutated"
    assert receipts[0].selection_metadata["setup_family"] == "gap_up"


def test_playbook_definition_detaches_nested_selection_metadata_from_caller() -> None:
    selection_metadata = {"setup_family": "gap_up", "nested": {"source": "fixture"}}

    definition = PlaybookDefinition(
        playbook_id="gap_up_follow_through",
        setup_family="gap_up",
        setup_variant_ids=("gap_up.baseline",),
        selection_metadata=selection_metadata,
    )
    selection_metadata["nested"]["source"] = "mutated"

    assert definition.selection_metadata["nested"]["source"] == "fixture"


def test_playbook_constraint_detaches_nested_metadata_from_caller() -> None:
    metadata = {"reason": "permission", "nested": {"source": "fixture"}}

    constraint = PlaybookEligibilityConstraint(
        constraint_id="permission_allow_or_derisk",
        constraint_type="permission_state",
        allowed_values=("allow", "derisk"),
        metadata=metadata,
    )
    metadata["nested"]["source"] = "mutated"

    assert constraint.metadata["nested"]["source"] == "fixture"


def test_playbook_registry_detaches_nested_registry_metadata_from_caller() -> None:
    registry_metadata = {"authority": "playbook_library", "nested": {"source": "fixture"}}

    registry = PlaybookRegistryDocument(
        schema_version="playbook_registry.v1",
        registry_id="registry-test",
        playbooks=(),
        registry_metadata=registry_metadata,
    )
    registry_metadata["nested"]["source"] = "mutated"

    assert registry.registry_metadata["nested"]["source"] == "fixture"


def test_playbook_metadata_receipt_detaches_nested_selection_metadata_from_caller() -> None:
    selection_metadata = {"setup_family": "gap_up", "nested": {"source": "fixture"}}

    receipt = PlaybookMetadataReceipt(
        receipt_id="receipt-001",
        registry_id="registry-test",
        playbook_id="gap_up_follow_through",
        setup_family="gap_up",
        setup_variant_id="gap_up.baseline",
        selection_metadata=selection_metadata,
        source_registry_fingerprint="abc123",
    )
    selection_metadata["nested"]["source"] = "mutated"

    assert receipt.selection_metadata["nested"]["source"] == "fixture"


def test_playbook_metadata_receipt_rejects_hidden_authority_keys() -> None:
    from nvda_desk.contracts.playbook import PlaybookMetadataReceipt

    with pytest.raises(ValidationError, match="hidden playbook authority key"):
        PlaybookMetadataReceipt(
            receipt_id="receipt-001",
            registry_id="registry-test",
            playbook_id="gap_up_follow_through",
            setup_family="gap_up",
            setup_variant_id="gap_up.baseline",
            selection_metadata={"nested": {"capital_deployment": "not_allowed"}},
            source_registry_fingerprint="abc123",
        )


def test_playbook_selection_consumes_eligibility_without_capital_authority() -> None:
    registry = _registry()
    eligibility = PlaybookEligibilityOutput(
        admissibility_surface=EligibilityAdmissibilitySurface(
            permission_state=PermissionState.ALLOW,
        ),
        active_family_ids=["gap_up"],
        active_setup_variant_ids=["gap_up.baseline"],
    )

    receipts = select_playbook_metadata_receipts(registry=registry, eligibility=eligibility)

    assert len(receipts) == 1
    assert receipts[0].setup_variant_id == "gap_up.baseline"
    assert "authorised_notional_usd" not in type(receipts[0]).model_fields
    assert "capital_deployment" not in receipts[0].model_dump()


def test_playbook_selection_permission_block_dominates_active_ids() -> None:
    registry = _registry()
    eligibility = PlaybookEligibilityOutput(
        admissibility_surface=EligibilityAdmissibilitySurface(
            permission_state=PermissionState.BLOCK,
            no_trade_reasons=["permission_block"],
        ),
        active_family_ids=["gap_up"],
        active_setup_variant_ids=["gap_up.baseline"],
    )

    assert select_playbook_metadata_receipts(registry=registry, eligibility=eligibility) == []


def test_playbook_selection_deduplicates_family_candidates_before_receipt_filtering() -> None:
    registry = _registry()
    eligibility = PlaybookEligibilityOutput(
        admissibility_surface=EligibilityAdmissibilitySurface(
            permission_state=PermissionState.ALLOW,
        ),
        active_family_ids=["gap_up", "gap_up"],
        active_setup_variant_ids=["gap_up.baseline", "gap_up.risk_defined"],
    )

    receipts = select_playbook_metadata_receipts(registry=registry, eligibility=eligibility)

    assert [receipt.setup_variant_id for receipt in receipts] == [
        "gap_up.baseline",
        "gap_up.risk_defined",
    ]


def test_playbook_registry_loader_rejects_duplicate_yaml_keys(tmp_path: Path) -> None:
    registry_path = tmp_path / "playbook_registry.yaml"
    registry_path.write_text(
        """
        schema_version: playbook_registry.v1
        registry_id: duplicate-yaml
        playbooks:
          first:
            setup_family: gap_up
            setup_variant_ids: [gap_up.baseline]
          first:
            setup_family: gap_up
            setup_variant_ids: [gap_up.risk_defined]
        """,
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="duplicate YAML key"):
        load_playbook_registry(registry_path)
