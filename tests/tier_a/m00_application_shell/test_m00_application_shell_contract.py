"""M00 C-PROOF for the final-composition public seam.

Before Gate D the reference and normative challenges pass while the production
API test remains expected-red because ``nvda_desk.m00_application_shell`` does
not yet exist.
"""

from __future__ import annotations

from dataclasses import replace
from datetime import timedelta
from pathlib import Path

import pytest
from tests.support.m00_application_shell_contract_harness import (
    MUTANTS,
    RecordingOwners,
    ReferenceCommand,
    evaluate_query_reference,
    evaluate_reference,
    production_api,
)

PROPOSITION_IDS = tuple(f"M00-COMP-{index:03d}" for index in range(1, 10))


def test_normative_propositions_and_vocabulary_are_explicit() -> None:
    architecture = Path("docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md").read_text(
        encoding="utf-8"
    )
    vocabulary = Path("docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md").read_text(
        encoding="utf-8"
    )
    registry = Path("docs/vocabulary/vocabulary_registry.md").read_text(encoding="utf-8")
    for proposition_id in PROPOSITION_IDS:
        assert proposition_id in architecture
    for term in (
        "Application Command",
        "Application Query",
        "Application Run Receipt",
        "Run Coordinator",
    ):
        assert f"### {term}" in registry
        assert term in vocabulary


def test_reference_run_uses_canonical_order_and_fresh_scope() -> None:
    first_owners = RecordingOwners()
    first = evaluate_reference(ReferenceCommand(), first_owners)
    second_owners = RecordingOwners()
    second = evaluate_reference(
        replace(ReferenceCommand(), command_id="m00.command.002", run_id="run.002"),
        second_owners,
    )
    assert first.owner_steps == (
        "prepared_context_packet",
        "serial",
        "parallel",
        "serial_packet",
        "parallel_packet",
        "final_risk",
        "capital",
        "scope:scope.1",
        "paper_execution",
        "portfolio_reconciliation",
    )
    assert first.scope_id == "scope.1"
    assert second.scope_id == "scope.1"
    assert first_owners is not second_owners
    assert first.replay_class is None
    assert first.live_execution_proven is False
    assert first.durable_state_proven is False


def test_reference_run_fails_closed_and_stops_before_placement() -> None:
    owners = RecordingOwners(capital_action="block")
    receipt = evaluate_reference(ReferenceCommand(), owners)
    assert receipt.outcome == "block"
    assert receipt.scope_id is None
    assert "paper_execution" not in owners.calls
    assert "portfolio_reconciliation" not in owners.calls

    with pytest.raises(ValueError, match="missing_run_id"):
        evaluate_reference(replace(ReferenceCommand(), run_id=""), RecordingOwners())
    with pytest.raises(ValueError, match="capital_time_precedes_owner_packets"):
        evaluate_reference(
            replace(
                ReferenceCommand(),
                capital_emitted_at_utc=ReferenceCommand().serial_emitted_at_utc
                - timedelta(seconds=1),
            ),
            RecordingOwners(),
        )


def test_reference_query_is_read_only_and_separate_from_runtime() -> None:
    run_calls: list[str] = []
    replay_calls: list[str] = []
    assert evaluate_query_reference(run_calls=run_calls, replay_calls=replay_calls) == (
        "review_projection"
    )
    assert run_calls == []
    assert replay_calls == ["assess", "project"]


@pytest.mark.parametrize("name", sorted(MUTANTS))
def test_named_false_positive_mutants_are_detectable(name: str) -> None:
    output = MUTANTS[name](ReferenceCommand())
    if name == "places_after_block":
        assert output.outcome == "paper_filled"
        assert "paper_execution" in output.owner_steps
    elif name == "reuses_scope":
        first_scope, second_scope = output
        assert first_scope == second_scope
    elif name == "promotes_runtime_to_replay":
        assert output["replay_class"] is not None
    else:  # pragma: no cover - closed table protects future additions
        raise AssertionError(name)


def test_production_m00_public_seam_exists_and_is_closed() -> None:
    api = production_api()
    for name in ("ApplicationCommand", "ApplicationQuery", "ApplicationRunReceipt"):
        assert api[name].model_config.get("frozen") is True
        assert api[name].model_config.get("extra") == "forbid"
    assert api["RunCoordinator"]
