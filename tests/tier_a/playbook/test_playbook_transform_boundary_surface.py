from __future__ import annotations

import pytest
from pydantic import ValidationError

from nvda_desk.config.playbook_registry import PlaybookRegistryDocument
from nvda_desk.contracts.playbook import (
    PlaybookDefinition,
    PlaybookEligibilityConstraint,
    PlaybookMetadataReceipt,
)

TRANSFORM_REQUIRED_DONOR_KEYS = (
    "import_registry_row_contract",
    "downstream_shell_request_contract",
    "review_eligibility_surface",
    "review_failure_class",
    "cognition_playbook_decision",
    "cognition_playbook_action",
    "playbook_family_candidate",
    "setup_variant_candidate",
    "execution_expression_service",
    "replay_compare_service",
    "playbook_eligibility_service",
    "cognition_runtime_service",
)


def _donor_payload(key: str) -> dict[str, object]:
    return {
        "native_playbook_metadata": "allowed",
        "nested": {
            key: {
                "source": "ACABC-0025",
                "donor_shape": "transform_required",
            }
        },
    }


@pytest.mark.parametrize("donor_key", TRANSFORM_REQUIRED_DONOR_KEYS)
def test_playbook_definition_rejects_transform_required_donor_payload_keys(
    donor_key: str,
) -> None:
    with pytest.raises(ValidationError, match="hidden playbook authority key"):
        PlaybookDefinition(
            playbook_id="gap_up_follow_through",
            setup_family="gap_up",
            setup_variant_ids=("gap_up.baseline",),
            selection_metadata=_donor_payload(donor_key),
        )


@pytest.mark.parametrize("donor_key", TRANSFORM_REQUIRED_DONOR_KEYS)
def test_playbook_constraint_rejects_transform_required_donor_payload_keys(
    donor_key: str,
) -> None:
    with pytest.raises(ValidationError, match="hidden playbook authority key"):
        PlaybookEligibilityConstraint(
            constraint_id="permission_allow_or_derisk",
            constraint_type="permission_state",
            allowed_values=("allow", "derisk"),
            metadata=_donor_payload(donor_key),
        )


@pytest.mark.parametrize("donor_key", TRANSFORM_REQUIRED_DONOR_KEYS)
def test_playbook_metadata_receipt_rejects_transform_required_donor_payload_keys(
    donor_key: str,
) -> None:
    with pytest.raises(ValidationError, match="hidden playbook authority key"):
        PlaybookMetadataReceipt(
            receipt_id="receipt-001",
            registry_id="registry-test",
            playbook_id="gap_up_follow_through",
            setup_family="gap_up",
            setup_variant_id="gap_up.baseline",
            selection_metadata=_donor_payload(donor_key),
            source_registry_fingerprint="abc123",
        )


@pytest.mark.parametrize("donor_key", TRANSFORM_REQUIRED_DONOR_KEYS)
def test_playbook_registry_document_rejects_transform_required_donor_payload_keys(
    donor_key: str,
) -> None:
    with pytest.raises(ValidationError, match="hidden playbook authority key"):
        PlaybookRegistryDocument(
            schema_version="playbook_registry.v1",
            registry_id="registry-test",
            playbooks=(),
            registry_metadata=_donor_payload(donor_key),
        )
