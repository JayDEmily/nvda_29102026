from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

from nvda_desk.config.parallel_risk_signal_inventory import ParallelRiskSignalInventoryService
from nvda_desk.contracts.parallel_risk import (
    ParallelRiskSignalInventoryDocument,
    parallel_risk_signal_inventory_document_from_dict,
)

CONFIG = Path("config/parallel_risk_signal_inventory.v1.yaml")
WORKBOOK = Path(
    "data/reference/signal_workbooks/2026-03-25_NVDA_SIGNAL_WORKBOOK_v3_bounds_handoff_copy.xlsx"
)

FORBIDDEN_RUNTIME_TOKENS = ("openpyxl", "load_workbook", "SpreadsheetFile", "import_xlsx")
FORBIDDEN_AUTHORITY_FIELDS = {
    "candidate_formation_allowed",
    "playbook_selection_allowed",
    "capital_sizing_allowed",
    "broker_execution_allowed",
    "direct_workbook_runtime_read_allowed",
}


def _payload() -> dict:
    return yaml.safe_load(CONFIG.read_text(encoding="utf-8"))


def test_parallel_risk_signal_inventory_config_loads_and_validates() -> None:
    document = ParallelRiskSignalInventoryService(CONFIG).load_document()

    assert isinstance(document, ParallelRiskSignalInventoryDocument)
    assert document.inventory_id == "parallel_risk_signal_inventory.v1"
    assert document.source_workbook_path == str(WORKBOOK)
    assert document.source_workbook_sheet == "Parallel Risk Lane Signal Inventory"
    assert document.direct_workbook_runtime_read_allowed is False
    assert document.authority_flags.direct_workbook_runtime_read_allowed is False
    assert {record.signal_id for record in document.required_runtime_records()} == {
        "source_time_utc",
        "scheduled_event_window_active",
        "vix_level",
        "spot_price",
        "front_dte",
        "next_dte",
    }


def test_parallel_risk_signal_inventory_config_preserves_workbook_lineage() -> None:
    document = ParallelRiskSignalInventoryService(CONFIG).load_document()

    assert len(document.source_workbook_sha256) == 64
    for record in document.records:
        assert record.workbook_lineage_refs
        assert any(
            "Parallel Risk Lane Signal Inventory!" in ref for ref in record.workbook_lineage_refs
        )


def test_parallel_risk_signal_inventory_runtime_loader_does_not_read_workbook(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original_read_text = Path.read_text
    read_paths: list[Path] = []

    def guarded_read_text(path: Path, *args, **kwargs) -> str:
        read_paths.append(path)
        assert path.suffix != ".xlsx"
        return original_read_text(path, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", guarded_read_text)

    document = ParallelRiskSignalInventoryService(CONFIG).load_document()

    assert len(document.records) >= 6
    assert read_paths == [CONFIG]
    runtime_source = Path("src/nvda_desk/config/parallel_risk_signal_inventory.py").read_text(
        encoding="utf-8"
    )
    for token in FORBIDDEN_RUNTIME_TOKENS:
        assert token not in runtime_source


def test_parallel_risk_signal_inventory_invalid_status_fails() -> None:
    payload = _payload()
    payload["records"][0]["inventory_status"] = "invented_status"

    with pytest.raises(ValidationError):
        parallel_risk_signal_inventory_document_from_dict(payload)


def test_parallel_risk_signal_inventory_missing_required_field_fails() -> None:
    payload = _payload()
    del payload["records"][0]["signal_family"]

    with pytest.raises(ValidationError):
        parallel_risk_signal_inventory_document_from_dict(payload)


def test_parallel_risk_signal_inventory_does_not_introduce_trade_authority() -> None:
    payload = _payload()
    document = parallel_risk_signal_inventory_document_from_dict(payload)

    dumped = document.model_dump()
    authority_flags = dumped["authority_flags"]
    for field in FORBIDDEN_AUTHORITY_FIELDS:
        assert authority_flags[field] is False

    records_by_id = document.record_map()
    assert records_by_id["capital_sizing_signal"].inventory_status == "excluded"
    assert records_by_id["capital_sizing_signal"].required_for_current_atom is False
    assert records_by_id["order_instruction_signal"].inventory_status == "excluded"
    assert records_by_id["order_instruction_signal"].required_for_current_atom is False

    mutated = deepcopy(payload)
    mutated["authority_flags"] = {"capital_sizing_allowed": True}
    with pytest.raises(ValidationError):
        parallel_risk_signal_inventory_document_from_dict(mutated)
