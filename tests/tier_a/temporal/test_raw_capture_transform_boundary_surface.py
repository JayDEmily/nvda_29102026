from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
RAW_CAPTURE_SOURCE_PATHS = (
    Path("src/nvda_desk/contracts/temporal.py"),
    Path("src/nvda_desk/ingress/raw_bundle_loader.py"),
    Path("src/nvda_desk/contracts/upstream_signal.py"),
    Path("src/nvda_desk/upstream/raw_signal_ingress.py"),
)
DONOR_RUNTIME_TOKENS = (
    "sqlalchemy",
    "create_engine",
    "SessionLocal",
    "DatabaseManager",
    "seed_database",
    "backfill",
    "broker_order",
)
PROHIBITED_OWNER_IMPORTS = (
    "nvda_desk.cognition",
    "nvda_desk.downstream",
    "nvda_desk.risk",
    "nvda_desk.services",
    "nvda_desk.runtime",
)


def _source_text(path: Path) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


def test_raw_capture_transform_boundary_does_not_recreate_donor_database_runtime_names() -> None:
    for path in RAW_CAPTURE_SOURCE_PATHS:
        text = _source_text(path)
        for token in DONOR_RUNTIME_TOKENS:
            assert token not in text, f"{path} leaks transform-required donor/runtime token {token!r}"


def test_raw_capture_transform_boundary_has_no_cognition_downstream_or_risk_owner_imports() -> None:
    for path in RAW_CAPTURE_SOURCE_PATHS:
        text = _source_text(path)
        for owner_import in PROHIBITED_OWNER_IMPORTS:
            assert owner_import not in text, f"{path} imports prohibited owner {owner_import!r}"


def test_raw_capture_transform_boundary_keeps_selected_files_in_source_temporal_owner_set() -> None:
    for path in RAW_CAPTURE_SOURCE_PATHS:
        assert (REPO_ROOT / path).is_file(), f"missing raw capture/source temporal file {path}"
    assert RAW_CAPTURE_SOURCE_PATHS == (
        Path("src/nvda_desk/contracts/temporal.py"),
        Path("src/nvda_desk/ingress/raw_bundle_loader.py"),
        Path("src/nvda_desk/contracts/upstream_signal.py"),
        Path("src/nvda_desk/upstream/raw_signal_ingress.py"),
    )
