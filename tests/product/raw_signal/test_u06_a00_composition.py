from __future__ import annotations

import ast
from datetime import UTC, datetime
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest
import yaml
from tests.product.raw_signal._support import observation, policy, policy_ref

import nvda_desk.composition as composition

ROOT = Path(__file__).resolve().parents[3]


def test_architecture_runtime_edge_is_exactly_a00_to_m00() -> None:
    rules = yaml.safe_load((ROOT / "config/architecture/dependency_rules.yaml").read_text())
    assert rules["declared_owner_edges"] == [{"source": "A00", "target": "M00"}]


def test_a00_composition_uses_public_m00_seam_plus_exact_technical_exception() -> None:
    imported: set[str] = set()
    postgres_symbols: set[str] = set()
    for path in (ROOT / "src/nvda_desk/composition").glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module)
                if node.module == "nvda_desk.raw_signal_occurrence_truth._postgres":
                    postgres_symbols.update(alias.name for alias in node.names)
            elif isinstance(node, ast.Import):
                imported.update(alias.name for alias in node.names)
    m00_imports = {
        name for name in imported if name.startswith("nvda_desk.raw_signal_occurrence_truth")
    }
    assert m00_imports <= {
        "nvda_desk.raw_signal_occurrence_truth.api",
        "nvda_desk.raw_signal_occurrence_truth._postgres",
    }
    assert postgres_symbols == {"create_postgres_persistence"}

    rules = yaml.safe_load((ROOT / "config/architecture/dependency_rules.yaml").read_text())
    assert rules["public_seam_exceptions"] == [
        {
            "source_owner": "A00",
            "target_owner": "M00",
            "import_path": (
                "nvda_desk.raw_signal_occurrence_truth._postgres."
                "create_postgres_persistence"
            ),
        }
    ]


def test_a00_uses_public_application_factory_and_contains_no_raw_signal_outcome_logic() -> None:
    assert not hasattr(composition, "_build_test_application")
    builder = getattr(composition, "create_application", None)
    if builder is None:
        pytest.fail("A00 production composition symbol create_application is not implemented")
    source = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (ROOT / "src/nvda_desk/composition").glob("*.py")
    ).lower()
    for forbidden in (
        "zero_received",
        "one_or_more_received",
        "unknown_not_established",
        "_build_test_application",
    ):
        assert forbidden not in source


class _SpyCommands:
    def __init__(self, calls: list[tuple[str, Any]], sentinels: dict[str, Any]) -> None:
        self._calls = calls
        self._sentinels = sentinels

    def register_capture_scope_policy(self, value: Any) -> Any:
        self._calls.append(("register_policy", value))
        return self._sentinels["policy"]

    def realise_scheduled_capture_occurrence(self, **kwargs: Any) -> Any:
        self._calls.append(("realise_capture", kwargs))
        return self._sentinels["capture"]

    def admit_raw_observation_occurrence(self, value: Any) -> Any:
        self._calls.append(("admit_observation", value))
        return self._sentinels["observation"]

    def derive_capture_receipt_evidence_relation(self, **kwargs: Any) -> Any:
        self._calls.append(("derive_relation", kwargs))
        return self._sentinels["relation"]

    def append_capture_receipt_presence_assessment(self, **kwargs: Any) -> Any:
        self._calls.append(("append_assessment", kwargs))
        return self._sentinels["assessment"]


class _SpyReads:
    def __init__(self, calls: list[tuple[str, Any]], sentinels: dict[str, Any]) -> None:
        self._calls = calls
        self._sentinels = sentinels

    def get_raw_observation_occurrence(self, observation_occurrence_id: Any) -> Any:
        self._calls.append(("read_observation", observation_occurrence_id))
        return self._sentinels["readback"]


class _SpyOwner:
    def __init__(self, calls: list[tuple[str, Any]], sentinels: dict[str, Any]) -> None:
        self.commands = _SpyCommands(calls, sentinels)
        self.reads = _SpyReads(calls, sentinels)


def test_a00_delegates_full_semantic_argument_trace_to_exact_m00_results() -> None:
    builder = getattr(composition, "create_application", None)
    if builder is None:
        pytest.fail("A00 production composition symbol create_application is not implemented")

    calls: list[tuple[str, Any]] = []
    returned_capture_id = object()
    returned_observation_id = object()
    effective_policy_ref = object()
    sentinels = {
        "policy": object(),
        "capture": SimpleNamespace(
            capture_occurrence_id=returned_capture_id,
            scope_policy_ref=effective_policy_ref,
        ),
        "observation": SimpleNamespace(observation_occurrence_id=returned_observation_id),
        "relation": object(),
        "assessment": SimpleNamespace(outcome="m00-owned-outcome"),
        "readback": object(),
    }

    def owner_factory(**kwargs: Any) -> _SpyOwner:
        calls.append(("construct_owner", kwargs))
        return _SpyOwner(calls, sentinels)

    app = builder(raw_signal_owner_factory=owner_factory)
    raw_policy = policy()
    raw_observation = observation(observation_occurrence_id="a00-observation-input")
    authoritative_policy_ref = policy_ref()
    authoritative_slot = datetime(2026, 9, 20, 12, 0, tzinfo=UTC)
    authoritative_capture_id = "a00-capture-input"
    authoritative_assessment_id = "a00-assessment-input"
    authoritative_as_of = datetime(2026, 9, 20, 12, 0, 10, 777777, tzinfo=UTC)
    authoritative_supersedes = None

    result = app.run_raw_signal_proof_sequence(
        capture_scope_policy=raw_policy,
        scope_policy_ref=authoritative_policy_ref,
        slot_start_utc=authoritative_slot,
        capture_occurrence_id=authoritative_capture_id,
        raw_observation=raw_observation,
        assessment_occurrence_id=authoritative_assessment_id,
        assessment_evidence_as_of_ts_utc=authoritative_as_of,
        supersedes_assessment_ref=authoritative_supersedes,
    )

    assert [name for name, _ in calls] == [
        "construct_owner",
        "register_policy",
        "realise_capture",
        "admit_observation",
        "derive_relation",
        "append_assessment",
        "read_observation",
    ]
    assert calls[1][1] is raw_policy
    assert calls[2][1] == {
        "scope_policy_ref": authoritative_policy_ref,
        "slot_start_utc": authoritative_slot,
        "capture_occurrence_id": authoritative_capture_id,
    }
    assert calls[3][1] is raw_observation
    assert calls[4][1] == {
        "observation_occurrence_ref": returned_observation_id,
        "capture_occurrence_ref": returned_capture_id,
        "scope_policy_ref": effective_policy_ref,
    }
    assert calls[5][1] == {
        "assessment_occurrence_id": authoritative_assessment_id,
        "capture_occurrence_ref": returned_capture_id,
        "evidence_as_of_ts_utc": authoritative_as_of,
        "supersedes_assessment_ref": authoritative_supersedes,
    }
    assert calls[6][1] is returned_observation_id
    assert result.capture is sentinels["capture"]
    assert result.observation is sentinels["observation"]
    assert result.relation is sentinels["relation"]
    assert result.assessment is sentinels["assessment"]
    assert result.readback is sentinels["readback"]
    assert result.assessment.outcome == "m00-owned-outcome"



def test_a00_rejects_caller_policy_ref_that_disagrees_with_registered_policy() -> None:
    builder = getattr(composition, "create_application", None)
    if builder is None:
        pytest.fail("A00 production composition symbol create_application is not implemented")

    calls: list[tuple[str, Any]] = []
    registered = policy()
    sentinels = {
        "policy": registered,
        "capture": SimpleNamespace(
            capture_occurrence_id=object(),
            scope_policy_ref=policy_ref(),
        ),
        "observation": SimpleNamespace(observation_occurrence_id=object()),
        "relation": object(),
        "assessment": SimpleNamespace(outcome="m00-owned-outcome"),
        "readback": object(),
    }

    def owner_factory(**kwargs: Any) -> _SpyOwner:
        calls.append(("construct_owner", kwargs))
        return _SpyOwner(calls, sentinels)

    app = builder(raw_signal_owner_factory=owner_factory)
    mismatched_ref = policy_ref("different-policy", 1)
    with pytest.raises((TypeError, ValueError)):
        app.run_raw_signal_proof_sequence(
            capture_scope_policy=registered,
            scope_policy_ref=mismatched_ref,
            slot_start_utc=datetime(2026, 9, 20, 12, 0, tzinfo=UTC),
            capture_occurrence_id="a00-mismatch-capture",
            raw_observation=observation(observation_occurrence_id="a00-mismatch-observation"),
            assessment_occurrence_id="a00-mismatch-assessment",
            assessment_evidence_as_of_ts_utc=datetime(
                2026, 9, 20, 12, 0, 10, tzinfo=UTC
            ),
            supersedes_assessment_ref=None,
        )
    assert any(name == "register_policy" for name, _ in calls)
    assert not any(name == "realise_capture" for name, _ in calls)

def test_a00_wrong_downstream_identity_or_policy_wiring_cannot_hide_behind_correct_call_order(
) -> None:
    """The preceding spy asserts every material kwarg, not only the ordered method names."""

    source = Path(__file__).read_text(encoding="utf-8")
    for required_trace in (
        '"scope_policy_ref": authoritative_policy_ref',
        '"observation_occurrence_ref": returned_observation_id',
        '"capture_occurrence_ref": returned_capture_id',
        '"scope_policy_ref": effective_policy_ref',
        '"evidence_as_of_ts_utc": authoritative_as_of',
        "assert calls[6][1] is returned_observation_id",
    ):
        assert required_trace in source


def test_a00_has_no_private_m00_state_table_repository_or_unadmitted_consumer_bypass() -> None:
    source = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (ROOT / "src/nvda_desk/composition").glob("*.py")
    ).lower()
    for forbidden in (
        "._repository",
        "._state",
        "raw_signal_occurrence_truth.repository",
        "raw_signal_occurrence_truth.persistence",
        "dmpv3_packet",
        "p01",
        "k01",
        "downstream_consumer",
    ):
        assert forbidden not in source
