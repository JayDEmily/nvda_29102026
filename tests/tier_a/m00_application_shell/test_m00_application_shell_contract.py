"""M00 C-PROOF for the final-composition public seam.

Before Gate D the reference and normative challenges pass while the production
API test remains expected-red because ``nvda_desk.m00_application_shell`` does
not yet exist.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
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
    production_query,
    production_runtime_fixture,
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
    projection = json.loads(
        Path("data/vocabulary/canonical_vocabulary.json").read_text(encoding="utf-8")
    )
    projected_ids = {entry["canonical_id"] for entry in projection["entries"]}
    for proposition_id in PROPOSITION_IDS:
        assert proposition_id in architecture

    assert "## 10.26 M00 final-composition public-contract admission lineage" in vocabulary
    assert "M00-FINAL-COMPOSITION-V1" in vocabulary
    for term, canonical_id in (
        ("Application Command", "m00.application_command"),
        ("Application Query", "m00.application_query"),
        ("Application Run Receipt", "m00.application_run_receipt"),
        ("Run Coordinator", "m00.run_coordinator"),
    ):
        assert f"### {term}" in registry
        assert f"`{canonical_id}`" in vocabulary
        assert canonical_id in projected_ids

    assert "coordinates the packetised M03 to M11 paper path" in registry
    assert "delegates M12 review queries separately" in registry
    assert "uses M13 only through admitted owner services" in registry
    assert "invokes admitted M01–M13 public seams" not in registry


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


def test_public_packet_builder_import_is_order_independent() -> None:
    env = dict(os.environ)
    env["PYTHONPATH"] = "src"
    completed = subprocess.run(
        [
            sys.executable,
            "-c",
            "from nvda_desk.packets.dmp_packets import build_prepared_context_packet; "
            "assert callable(build_prepared_context_packet)",
        ],
        cwd=Path.cwd(),
        env=env,
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr


def test_production_run_composes_exact_owner_path_and_fresh_paper_scope() -> None:
    api = production_api()
    first = production_runtime_fixture(api, suffix="101")
    second = production_runtime_fixture(api, suffix="102")

    first_receipt = first["coordinator"].run(first["command"])
    second_receipt = first["coordinator"].run(second["command"])

    assert first_receipt.outcome == "paper_filled"
    assert first_receipt.owner_steps == (
        "prepared_context_packet",
        "serial",
        "parallel",
        "serial_packet",
        "parallel_packet",
        "final_risk",
        "capital",
        "scope",
        "paper_execution",
        "portfolio_reconciliation",
    )
    assert first_receipt.run_scope_id == "paper-scope:run.m00.101"
    assert second_receipt.run_scope_id == "paper-scope:run.m00.102"
    assert first_receipt.run_scope_id != second_receipt.run_scope_id
    assert (
        first["scope_factory"].scopes[0].execution_port
        is not first["scope_factory"].scopes[1].execution_port
    )
    assert (
        first["scope_factory"].scopes[0].portfolio_service
        is not first["scope_factory"].scopes[1].portfolio_service
    )
    assert first_receipt.replay_class is None
    assert first_receipt.live_execution_proven is False
    assert first_receipt.durable_state_proven is False


def test_production_block_is_terminal_before_scope_and_placement() -> None:
    api = production_api()
    fixture = production_runtime_fixture(api, suffix="201", kill_switch=True)

    receipt = fixture["coordinator"].run(fixture["command"])

    assert receipt.outcome == "block"
    assert receipt.run_scope_id is None
    assert receipt.placement_intent is None
    assert receipt.execution_receipt is None
    assert receipt.fill_reconciliation_receipt is None
    assert fixture["scope_factory"].calls == []
    assert "paper_execution" not in receipt.owner_steps


def test_production_serial_terminal_still_evaluates_parallel_then_stops() -> None:
    api = production_api()
    fixture = production_runtime_fixture(api, suffix="301", terminal_stage="eligibility")

    receipt = fixture["coordinator"].run(fixture["command"])

    assert receipt.outcome == "serial_stand_down"
    assert receipt.owner_steps == (
        "prepared_context_packet",
        "serial",
        "parallel",
    )
    assert fixture["parallel_evaluator"].calls == [fixture["command"].parallel_input.input_id]
    assert receipt.serial_packet is None
    assert receipt.parallel_packet is None
    assert receipt.final_risk_decision is None
    assert fixture["scope_factory"].calls == []


def test_production_command_rejects_cross_run_and_time_mismatch() -> None:
    api = production_api()
    fixture = production_runtime_fixture(api, suffix="401")
    payload = fixture["command"].model_dump(mode="python")
    payload["serial_cognition"] = fixture["command"].serial_cognition.model_copy(
        update={
            "prepared_data": fixture["command"].prepared_data.model_copy(
                update={"prepared_id": "prepared.cross-run"}
            )
        }
    )
    with pytest.raises(
        ValueError,
        match="prepared_(identity|fingerprint)|serial_cognition_prepared",
    ):
        api["ApplicationCommand"].model_validate(payload)

    payload = fixture["command"].model_dump(mode="python")
    payload["intent_at_utc"] = payload["capital_receipt_emitted_at_utc"] - timedelta(seconds=1)
    with pytest.raises(ValueError, match="application_execution_time_order_invalid"):
        api["ApplicationCommand"].model_validate(payload)


def test_production_query_delegates_only_to_m12() -> None:
    api = production_api()
    fixture = production_runtime_fixture(api, suffix="501")
    query = production_query(api, suffix="501")

    projection = fixture["coordinator"].query(query)

    assert projection.replay_class == "comparison_only"
    assert projection.runtime_authority_promoted is False
    assert fixture["scope_factory"].calls == []
    assert fixture["parallel_evaluator"].calls == []


def test_production_query_requires_explicit_no_side_effect_authority() -> None:
    api = production_api()
    query = production_query(api, suffix="502")
    payload = query.model_dump(mode="python")
    payload.pop("live_side_effects")
    with pytest.raises(ValueError, match="live_side_effects"):
        api["ApplicationQuery"].model_validate(payload)

    payload = query.model_dump(mode="python")
    payload["live_side_effects"] = ("network_read",)
    with pytest.raises(ValueError, match="application_query_live_side_effects_forbidden"):
        api["ApplicationQuery"].model_validate(payload)

    payload = query.model_dump(mode="python")
    payload.pop("runtime_authority_promoted")
    with pytest.raises(ValueError, match="runtime_authority_promoted"):
        api["ApplicationQuery"].model_validate(payload)


def test_production_m00_quarantines_legacy_routes_and_wall_clock() -> None:
    package = Path("src/nvda_desk/m00_application_shell")
    source = "\n".join(path.read_text(encoding="utf-8") for path in sorted(package.glob("*.py")))
    for prohibited in (
        "runtime.orchestrator",
        "api.app",
        "api.deps",
        "datetime.now",
        "datetime.utcnow",
    ):
        assert prohibited not in source
    external_importers = {
        path.as_posix()
        for path in Path("src/nvda_desk").rglob("*.py")
        if package not in path.parents
        and "m00_application_shell" in path.read_text(encoding="utf-8")
    }
    assert external_importers == {
        "src/nvda_desk/entry/asgi.py",
        "src/nvda_desk/entry/cli.py",
    }


def test_semantic_continuity_m00_cannot_accept_caller_authored_serial_context_or_inputs() -> None:
    import nvda_desk.m00_application_shell as m00

    fields = m00.ApplicationCommand.model_fields
    assert "serial_cognition" in fields
    assert "serial_context" not in fields
    assert "serial_stage_inputs" not in fields
