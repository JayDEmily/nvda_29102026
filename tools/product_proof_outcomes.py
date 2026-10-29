"""Observe actual pytest collection and every phase; never provide product fixtures."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import pytest

_collected: list[str] = []
_deselected: list[str] = []
_errors: list[str] = []
_outcomes: dict[str, list[dict[str, Any]]] = {}


def pytest_collection_finish(session: pytest.Session) -> None:
    _collected.extend(item.nodeid for item in session.items)


def pytest_deselected(items: list[pytest.Item]) -> None:
    _deselected.extend(item.nodeid for item in items)


def pytest_collectreport(report: pytest.CollectReport) -> None:
    if report.failed or report.skipped:
        _errors.append(report.nodeid)


def pytest_runtest_logreport(report: pytest.TestReport) -> None:
    _outcomes.setdefault(report.nodeid, []).append(
        {
            "when": report.when,
            "outcome": report.outcome,
            "wasxfail": hasattr(report, "wasxfail"),
        }
    )


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    path = Path(os.environ["NVDA_PROOF_REPORT"])
    report = {
        "nonce": os.environ["NVDA_PROOF_NONCE"],
        "collected": _collected,
        "outcomes": _outcomes,
        "collection_errors": _errors,
        "deselected": _deselected,
        "exitstatus": int(exitstatus),
    }
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(report, sort_keys=True), encoding="utf-8")
    temporary.replace(path)


def validate_outcomes(
    report: Any, nonce: str, expected: dict[str, tuple[str, ...]], exitstatus: int
) -> int:
    """Return 0 success, 5 incomplete collection, 1 invalid/failed observed proof."""
    fields = {"nonce", "collected", "outcomes", "collection_errors", "deselected", "exitstatus"}
    if not isinstance(report, dict) or set(report) != fields:
        return 1
    if (
        report["nonce"] != nonce
        or type(report["exitstatus"]) is not int
        or report["exitstatus"] != exitstatus
    ):
        return 1
    nodes, outcomes = report["collected"], report["outcomes"]
    if (
        not isinstance(nodes, list)
        or any(not isinstance(n, str) for n in nodes)
        or len(nodes) != len(set(nodes))
        or not isinstance(outcomes, dict)
    ):
        return 1
    if report["collection_errors"] or report["deselected"]:
        return 5
    by_file: dict[str, set[str]] = {}
    for node in nodes:
        parts = node.split("::")
        if len(parts) < 2:
            return 1
        by_file.setdefault(parts[0], set()).add(parts[-1].split("[")[0])
    if set(by_file) != set(expected):
        return 5
    if any(not set(names) <= by_file[path] for path, names in expected.items()):
        return 5
    if set(outcomes) != set(nodes) or exitstatus != 0:
        return 1
    for rows in outcomes.values():
        if not isinstance(rows, list) or len(rows) != 3:
            return 1
        if [row.get("when") for row in rows if isinstance(row, dict)] != [
            "setup",
            "call",
            "teardown",
        ]:
            return 1
        for row in rows:
            if (
                set(row) != {"when", "outcome", "wasxfail"}
                or row["outcome"] != "passed"
                or row["wasxfail"] is not False
            ):
                return 1
    return 0
