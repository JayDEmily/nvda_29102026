"""Review bridge-style vocabulary candidate payloads without mutating vocabulary data."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

_REPO_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_REPO_SRC) not in sys.path:
    sys.path.insert(0, str(_REPO_SRC))

from nvda_desk.schemas.vocabulary import VocabularyDocument  # noqa: E402

DEFAULT_VOCABULARY_PATH = Path("data/vocabulary/canonical_vocabulary.json")


def _candidate_payloads_from_json_text(text: str) -> list[dict[str, Any]]:
    payload = json.loads(text)
    if isinstance(payload, list):
        candidates = payload
    elif isinstance(payload, dict) and isinstance(payload.get("candidates"), list):
        candidates = payload["candidates"]
    else:
        raise ValueError(
            "candidate payload file must be a list or an object with a candidates list"
        )
    if not all(isinstance(item, dict) for item in candidates):
        raise ValueError("candidate payload entries must be JSON objects")
    return list(candidates)


def _load_candidate_payloads(path: Path) -> list[dict[str, Any]]:
    return _candidate_payloads_from_json_text(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def _blocked_reviews(report: dict[str, Any]) -> list[dict[str, Any]]:
    blocked = []
    for review in report.get("reviews", []):
        if review.get("status") in {"invalid", "quarantined"}:
            blocked.append(review)
    return blocked


def _review_receipt(
    *,
    report: dict[str, Any] | None,
    vocabulary_path: Path,
    candidates_path: Path,
    mode: str,
    status: str,
    exit_code: int,
    error: str | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "schema_version": "v1",
        "trigger": "vocabulary_candidate_review_receipt",
        "mode": mode,
        "status": status,
        "exit_code": exit_code,
        "vocabulary_path": str(vocabulary_path),
        "candidates_path": str(candidates_path),
        "summary": report.get("summary") if report is not None else None,
        "blocked_candidates": _blocked_reviews(report) if report is not None else [],
        "error": error,
    }
    return payload


def _build_review_report_from_payloads(
    *, vocabulary_path: Path, candidates_path: str, candidates: list[dict[str, Any]]
) -> dict[str, Any]:
    document = VocabularyDocument.from_json_path(vocabulary_path)
    report = document.candidate_payload_admission_review_report(candidates)
    enriched = {
        "schema_version": "v1",
        "trigger": "vocabulary_candidate_review",
        "vocabulary_path": str(vocabulary_path),
        "candidates_path": candidates_path,
        **report,
    }
    enriched["blocked_candidates"] = _blocked_reviews(enriched)
    return enriched


def build_review_report(*, vocabulary_path: Path, candidates_path: Path) -> dict[str, Any]:
    return _build_review_report_from_payloads(
        vocabulary_path=vocabulary_path,
        candidates_path=str(candidates_path),
        candidates=_load_candidate_payloads(candidates_path),
    )


def _summary_report(report: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "v1",
        "trigger": "vocabulary_candidate_review_summary",
        "vocabulary_path": report["vocabulary_path"],
        "candidates_path": report["candidates_path"],
        "summary": report["summary"],
        "blocked_candidates": report["blocked_candidates"],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--candidates", required=True, help="JSON file containing candidate payloads"
    )
    parser.add_argument(
        "--vocabulary",
        default=str(DEFAULT_VOCABULARY_PATH),
        help="canonical vocabulary JSON path",
    )
    parser.add_argument("--output", help="optional output JSON path; stdout is used when omitted")
    parser.add_argument(
        "--receipt",
        help="optional JSON receipt path recording PASS/BLOCKED/ERROR status and summary",
    )
    parser.add_argument(
        "--summary-only",
        action="store_true",
        help="emit only the summary and blocked-candidate list instead of the full review report",
    )
    parser.add_argument(
        "--check-clean",
        action="store_true",
        help="return non-zero when invalid or quarantined candidate payloads are present",
    )
    args = parser.parse_args(argv)
    vocabulary_path = Path(args.vocabulary)
    candidates_path = Path(args.candidates)

    try:
        if args.candidates == "-":
            report = _build_review_report_from_payloads(
                vocabulary_path=vocabulary_path,
                candidates_path="-",
                candidates=_candidate_payloads_from_json_text(sys.stdin.read()),
            )
        else:
            report = build_review_report(
                vocabulary_path=vocabulary_path, candidates_path=candidates_path
            )
    except Exception as exc:
        if args.receipt:
            _write_json(
                Path(args.receipt),
                _review_receipt(
                    report=None,
                    vocabulary_path=vocabulary_path,
                    candidates_path=candidates_path,
                    mode="summary" if args.summary_only else "review",
                    status="ERROR",
                    exit_code=2,
                    error=str(exc),
                ),
            )
        raise

    output_payload = _summary_report(report) if args.summary_only else report
    text = json.dumps(output_payload, indent=2) + "\n"
    if args.output:
        _write_json(Path(args.output), output_payload)
    else:
        print(text, end="")

    statuses = report["summary"]["statuses"]
    blocked = statuses.get("invalid", 0) + statuses.get("quarantined", 0)
    exit_code = 1 if args.check_clean and blocked else 0
    status = "BLOCKED" if exit_code else "PASS"
    if args.receipt:
        _write_json(
            Path(args.receipt),
            _review_receipt(
                report=report,
                vocabulary_path=vocabulary_path,
                candidates_path=candidates_path,
                mode="summary" if args.summary_only else "review",
                status=status,
                exit_code=exit_code,
            ),
        )
    if args.check_clean:
        if blocked:
            print(f"vocabulary_candidate_review=BLOCKED blocked_candidates={blocked}")
        else:
            print("vocabulary_candidate_review=PASS blocked_candidates=0")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
