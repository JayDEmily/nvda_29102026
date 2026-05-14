from __future__ import annotations

import ast
import importlib
from pathlib import Path

ACTIVE_REVIEW_FILES = (
    Path("src/nvda_desk/downstream/review_stage.py"),
    Path("src/nvda_desk/services/review_explanation_service.py"),
    Path("src/nvda_desk/services/downstream_review_service.py"),
    Path("src/nvda_desk/contracts/review.py"),
    Path("src/nvda_desk/contracts/replay.py"),
    Path("src/nvda_desk/analysis/replay/service.py"),
    Path("src/nvda_desk/persistence/research_logs.py"),
    Path("src/nvda_desk/repositories/research_logs.py"),
    Path("src/nvda_desk/repositories/review_repository.py"),
)
DONOR_IMPORT_PREFIXES = (
    "legacy_import",
    "nvda_desk.schemas.eval",
    "nvda_desk.schemas.replay",
    "nvda_desk.schemas.research",
    "nvda_desk.services.replay",
    "nvda_desk.services.research",
    "nvda_desk.services.evaluation_log",
    "nvda_desk.services.module_evaluators",
)
REVIEW_ONLY_FIELDS = {
    "review_packet",
    "lineage",
    "imported_citations",
    "summary",
    "resolved_surfaces",
    "packet_ids",
    "source_packet_ids",
    "resolved_coefficients",
    "missing_review_material",
    "lineage_complete",
    "explanation",
}
FORBIDDEN_RUNTIME_FIELDS = {
    "trade_allowed",
    "broker_order_id",
    "capital_sizing",
    "risk_limit_override",
    "promoted_to_runtime",
}


def _imports(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    imported: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.append(node.module)
    return imported


def test_native_review_transform_boundary_excludes_legacy_donor_imports() -> None:
    offenders: list[str] = []
    for path in ACTIVE_REVIEW_FILES:
        for imported in _imports(path):
            if any(imported == prefix or imported.startswith(f"{prefix}.") for prefix in DONOR_IMPORT_PREFIXES):
                offenders.append(f"{path}:{imported}")

    assert offenders == []


def test_native_review_stage_keeps_imported_citations_review_only() -> None:
    review_stage = importlib.import_module("nvda_desk.downstream.review_stage")
    packet = review_stage.build_review_packet(packet_id="review-1", summary="review only")
    with_citations = review_stage.attach_imported_citations(
        packet=packet,
        citations=["legacy donor eval output requires native transformation"],
    )
    with_lineage = review_stage.attach_lineage(
        packet=packet,
        event_ids=["event-1"],
        resolved_surfaces=["review and explanation layer"],
    )

    assert set(with_citations) == {"review_packet", "imported_citations"}
    assert set(with_lineage) == {"review_packet", "lineage"}
    assert set(with_citations).isdisjoint(FORBIDDEN_RUNTIME_FIELDS)
    assert set(with_lineage).isdisjoint(FORBIDDEN_RUNTIME_FIELDS)


def test_native_review_explanation_outputs_remain_review_only() -> None:
    review_contracts = importlib.import_module("nvda_desk.contracts.review")
    service_module = importlib.import_module("nvda_desk.services.review_explanation_service")
    service = service_module.ReviewExplanationService()

    output = service.build_explanation(
        review_packet=review_contracts.ReviewPacket(packet_id="review-1", summary="summary"),
        effective_policy=review_contracts.EffectivePolicySnapshot(
            policy_ids=["policy-1"],
            resolved_surfaces=["review and explanation layer"],
        ),
        review_lineage=review_contracts.ReviewLineagePacket(
            event_lineage_keys=["event-1"],
            resolved_surfaces=["review and explanation layer"],
            modifier_policy_ids=["policy-1"],
        ),
        packet_lineage=review_contracts.PacketLineageSurface(
            packet_ids=["packet-1"],
            source_packet_ids=["source-packet-1"],
        ),
    )

    assert set(output).issubset(REVIEW_ONLY_FIELDS)
    assert set(output).isdisjoint(FORBIDDEN_RUNTIME_FIELDS)
