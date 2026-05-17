from __future__ import annotations

import pytest

from nvda_desk.persistence.import_registry import ImportRegistryService
from nvda_desk.schemas.import_registry import (
    GrammarMappingRow,
    GrammarRole,
    ImportRegistryDocument,
    ImportRegistryRow,
    MaturityState,
    RuntimeTarget,
    SourceForm,
    import_registry_document_from_dict,
)


def test_import_registry_schema_bounds_vocabularies_and_rejects_duplicate_ids() -> None:
    row = ImportRegistryRow(
        registry_id="reg-1",
        source_form=SourceForm.MODULE,
        maturity_state=MaturityState.CANDIDATE,
        runtime_target=RuntimeTarget.REVIEW_ONLY,
        import_depth=2,
        source_path="legacy/a.py",
    )
    grammar = GrammarMappingRow(
        mapping_id="map-1",
        registry_id="reg-1",
        grammar_role=GrammarRole.SERVICE,
        source_tokens=("risk", "gate"),
    )
    document = ImportRegistryDocument(registry_rows=(row,), grammar_mappings=(grammar,))

    assert document.registry_index()["reg-1"] == row
    assert document.grammar_role_ids(GrammarRole.SERVICE) == ("map-1",)

    with pytest.raises(ValueError, match="duplicate registry_id"):
        ImportRegistryDocument(registry_rows=(row, row))

    with pytest.raises(ValueError, match="extra"):
        import_registry_document_from_dict(
            {
                "schema_version": "import_registry.v1",
                "registry_rows": [{"registry_id": "reg-1", "source_form": "module"}],
                "unknown": True,
            }
        )


def test_import_registry_service_reports_backlogs_depth_and_readiness(tmp_path) -> None:
    registry_path = tmp_path / "registry.jsonl"
    registry_path.write_text(
        '{"registry_id":"reg-a","source_form":"module","maturity_state":"candidate",'
        '"runtime_target":"review_only","import_depth":3,"source_path":"legacy/a.py"}\n'
        '{"registry_id":"reg-b","source_form":"function","maturity_state":"blocked",'
        '"runtime_target":"runtime","import_depth":1,"source_path":"legacy/b.py",'
        '"blockers":["missing native owner"]}\n',
        encoding="utf-8",
    )
    grammar_path = tmp_path / "grammar.jsonl"
    grammar_path.write_text(
        '{"mapping_id":"map-a","registry_id":"reg-a","grammar_role":"service",'
        '"source_tokens":["market","state"]}\n',
        encoding="utf-8",
    )

    service = ImportRegistryService(registry_path=registry_path, grammar_mapping_path=grammar_path)
    document = service.load_enriched_document()

    assert service.registry_path_accessor() == registry_path
    assert service.grammar_mapping_path_accessor() == grammar_path
    assert service.coverage_summary(document)["registry_rows"] == 2
    assert service.runtime_target_ids(document, RuntimeTarget.RUNTIME) == ("reg-b",)
    assert service.grammar_role_ids(document, GrammarRole.SERVICE) == ("map-a",)
    assert service.runtime_gap_report(document)[0]["registry_id"] == "reg-b"
    assert service.runtime_depth_report(document)["max_depth"] == 3
    assert service.executable_backlog_report(document)[0]["registry_id"] == "reg-a"
    assert service.import_depth_by_role_report(document)["service"] == 3
    assert service.runtime_target_breakdown(document) == {"review_only": 1, "runtime": 1}
    assert service.tokenize_text("Risk-Gate service") == ("risk", "gate", "service")
    assert service.infer_readiness(document.registry_rows[0]).value == "ready"
    assert service.readiness_blockers(document.registry_rows[1]) == ("missing native owner",)
    assert service.runtime_contract_status(document.registry_rows[0]) == "review_only_ready"


def test_import_registry_service_no_loss_assertion_and_report_writer(tmp_path) -> None:
    service = ImportRegistryService(registry_path=tmp_path / "missing.jsonl")
    document = service.seed_document(
        registry_rows=[
            ImportRegistryRow(
                registry_id="reg-a",
                source_form=SourceForm.MODULE,
                maturity_state=MaturityState.CANDIDATE,
                runtime_target=RuntimeTarget.REVIEW_ONLY,
            )
        ],
        grammar_mappings=[],
    )

    service.assert_no_loss(document, expected_registry_ids=("reg-a",))
    with pytest.raises(AssertionError, match="missing registry ids"):
        service.assert_no_loss(document, expected_registry_ids=("reg-a", "reg-b"))

    report_path = tmp_path / "report.json"
    service.write_report(report_path, service.registry_summary_report(document))
    assert '"registry_rows": 1' in report_path.read_text(encoding="utf-8")
