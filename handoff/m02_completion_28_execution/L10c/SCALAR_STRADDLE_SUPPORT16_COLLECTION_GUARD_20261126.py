"""External finite-population guard; no product imports, fixtures or oracle changes."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

import pytest

_expected: list[str] = []
_cleared = False
_next = 0


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _stop(reason: str) -> None:
    pytest.exit("EXACT COLLECTION GUARD: " + reason, returncode=4)


@pytest.hookimpl(wrapper=True, tryfirst=True)
def pytest_runtestloop(session):
    """Run after completed collection, before any ordinary runtest protocol."""
    global _expected, _cleared
    import product_proof_outcomes as observer

    expected_path = Path(os.environ["NVDA_GATE_EXPECTED"])
    report_path = Path(os.environ["NVDA_GATE_REPORT"])
    if not expected_path.is_absolute() or not report_path.is_absolute() or report_path.exists():
        _stop("expected and unused report paths must be absolute")
    data = expected_path.read_bytes()
    expected = json.loads(data)
    observed = [item.nodeid for item in session.items]
    markers = [
        item.nodeid
        for item in session.items
        if hasattr(item, "callspec")
        or any(item.get_closest_marker(name) is not None for name in ("skip", "skipif", "xfail"))
    ]
    reasons = []
    if hashlib.sha256(data).hexdigest() != os.environ["NVDA_GATE_EXPECTED_SHA256"]:
        reasons.append("expected-list digest")
    if (
        not isinstance(expected, list)
        or not expected
        or any(not isinstance(n, str) or "::" not in n or "[" in n or "]" in n for n in expected)
        or len(set(expected)) != len(expected)
    ):
        reasons.append("invalid exact-node list")
    if observed != expected or observer._collected != expected:
        reasons.append("ordered exact collection mismatch")
    if observer._errors or observer._deselected or session.testsfailed:
        reasons.append("collection errors/deselection")
    if session.testscollected != len(observed) or markers:
        reasons.append("collection count, parametrisation or prohibited marker")
    if (
        session.config.option.collectonly
        or session.config.option.setuponly
        or session.config.option.continue_on_collection_errors
        or session.shouldfail
        or session.shouldstop
    ):
        reasons.append("incompatible execution mode/session")
    observer_path = Path(observer.__file__).resolve()
    if _sha(observer_path) != os.environ["NVDA_GATE_OBSERVER_SHA256"]:
        reasons.append("observer digest mismatch")
    result = {
        "nonce": os.environ["NVDA_PROOF_NONCE"],
        "expected_sha256": hashlib.sha256(data).hexdigest(),
        "expected": expected,
        "observed": observed,
        "observer_collected": list(observer._collected),
        "collection_errors": list(observer._errors),
        "deselected": list(observer._deselected),
        "prohibited_markers_or_parametrisation": markers,
        "observer_path": str(observer_path),
        "observer_sha256": _sha(observer_path),
        "reasons": reasons,
        "cleared": not reasons,
    }
    # Persist the pre-call decision before allowing any test protocol.
    with report_path.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, sort_keys=True)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    if reasons:
        _stop("; ".join(reasons))
    _expected = expected
    _cleared = True
    return (yield)


@pytest.hookimpl(wrapper=True, tryfirst=True)
def pytest_runtest_protocol(item, nextitem):
    """Fail closed if the actual protocol population/order changes after collection."""
    global _next
    if (
        not _cleared
        or [member.nodeid for member in item.session.items] != _expected
        or _next >= len(_expected)
        or item.nodeid != _expected[_next]
        or (nextitem.nodeid if nextitem is not None else None)
        != (_expected[_next + 1] if _next + 1 < len(_expected) else None)
    ):
        _stop("test protocol outside cleared exact ordered population")
    _next += 1
    return (yield)
