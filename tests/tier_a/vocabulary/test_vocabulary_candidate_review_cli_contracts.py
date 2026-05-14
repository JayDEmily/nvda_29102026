from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from scripts.vocabulary_candidate_review import build_review_report, main


def _vocabulary_path(tmp_path: Path) -> Path:
    path = tmp_path / "vocabulary.json"
    path.write_text(
        json.dumps(
            {
                "schema_version": "v1",
                "registry_version": "test",
                "entries": [
                    {
                        "canonical_slug": "governed_term",
                        "canonical_label": "Governed Term",
                        "category": "workflow",
                        "stage_owner": "vocabulary_governance",
                        "maps_to_contract": "GovernedTermContract",
                        "raw_or_derived": "derived",
                        "allowed_aliases": ["known alias"],
                        "disallowed_phrases": ["forbidden phrase"],
                    }
                ],
            }
        )
        + "\n",
        encoding="utf-8",
    )
    return path


def _candidates_path(tmp_path: Path, payload: object) -> Path:
    path = tmp_path / "candidates.json"
    path.write_text(json.dumps(payload) + "\n", encoding="utf-8")
    return path


def test_candidate_review_cli_builds_ordered_report_from_candidates_list(tmp_path: Path) -> None:
    report = build_review_report(
        vocabulary_path=_vocabulary_path(tmp_path),
        candidates_path=_candidates_path(
            tmp_path,
            [
                {"candidate_slug": "known_alias", "candidate_label": "Known Alias"},
                {"candidate_slug": "forbidden_phrase", "candidate_label": "Forbidden Phrase"},
                {"candidate_slug": "partial_payload"},
            ],
        ),
    )

    assert report["trigger"] == "vocabulary_candidate_review"
    assert report["summary"]["statuses"] == {
        "admissible": 1,
        "quarantined": 1,
        "invalid": 1,
    }
    assert [item["candidate_slug"] for item in report["reviews"]] == [
        "known_alias",
        "forbidden_phrase",
        "partial_payload",
    ]


def test_candidate_review_cli_accepts_object_with_candidates_key(tmp_path: Path) -> None:
    report = build_review_report(
        vocabulary_path=_vocabulary_path(tmp_path),
        candidates_path=_candidates_path(
            tmp_path,
            {"candidates": [{"candidate_slug": "known_alias", "candidate_label": "Known Alias"}]},
        ),
    )

    assert report["summary"]["statuses"] == {
        "admissible": 1,
        "quarantined": 0,
        "invalid": 0,
    }


def test_candidate_review_cli_writes_output_file(tmp_path: Path) -> None:
    output = tmp_path / "reports" / "candidate_review.json"

    status = main(
        [
            "--vocabulary",
            str(_vocabulary_path(tmp_path)),
            "--candidates",
            str(_candidates_path(tmp_path, [])),
            "--output",
            str(output),
        ]
    )

    assert status == 0
    assert json.loads(output.read_text(encoding="utf-8"))["reviews"] == []


def test_candidate_review_cli_does_not_mutate_canonical_vocabulary_file(tmp_path: Path) -> None:
    vocabulary = _vocabulary_path(tmp_path)
    before = vocabulary.read_text(encoding="utf-8")
    output = tmp_path / "reports" / "candidate_review.json"
    receipt = tmp_path / "receipts" / "candidate_review.json"

    status = main(
        [
            "--vocabulary",
            str(vocabulary),
            "--candidates",
            str(
                _candidates_path(
                    tmp_path,
                    [{"candidate_slug": "known_alias", "candidate_label": "Known Alias"}],
                )
            ),
            "--output",
            str(output),
            "--receipt",
            str(receipt),
            "--check-clean",
        ]
    )

    assert status == 0
    assert vocabulary.read_text(encoding="utf-8") == before
    assert json.loads(output.read_text(encoding="utf-8"))["trigger"] == (
        "vocabulary_candidate_review"
    )
    assert json.loads(receipt.read_text(encoding="utf-8"))["status"] == "PASS"


def test_candidate_review_cli_stdout_is_json(tmp_path: Path) -> None:
    candidates = _candidates_path(
        tmp_path, [{"candidate_slug": "known_alias", "candidate_label": "Known Alias"}]
    )
    vocabulary = _vocabulary_path(tmp_path)

    completed = subprocess.run(
        [
            sys.executable,
            "scripts/vocabulary_candidate_review.py",
            "--vocabulary",
            str(vocabulary),
            "--candidates",
            str(candidates),
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    assert json.loads(completed.stdout)["summary"]["actions"]["alias_only"] == 1


def test_candidate_review_cli_rejects_non_object_candidate_entries(tmp_path: Path) -> None:
    candidates = _candidates_path(tmp_path, ["not-an-object"])

    completed = subprocess.run(
        [
            sys.executable,
            "scripts/vocabulary_candidate_review.py",
            "--vocabulary",
            str(_vocabulary_path(tmp_path)),
            "--candidates",
            str(candidates),
        ],
        check=False,
        text=True,
        capture_output=True,
    )

    assert completed.returncode != 0
    assert "candidate payload entries must be JSON objects" in completed.stderr


def test_candidate_review_cli_check_clean_returns_nonzero_for_blocked_candidates(
    tmp_path: Path,
) -> None:
    candidates = _candidates_path(
        tmp_path,
        [
            {"candidate_slug": "known_alias", "candidate_label": "Known Alias"},
            {"candidate_slug": "forbidden_phrase", "candidate_label": "Forbidden Phrase"},
        ],
    )

    completed = subprocess.run(
        [
            sys.executable,
            "scripts/vocabulary_candidate_review.py",
            "--vocabulary",
            str(_vocabulary_path(tmp_path)),
            "--candidates",
            str(candidates),
            "--check-clean",
        ],
        check=False,
        text=True,
        capture_output=True,
    )

    assert completed.returncode == 1
    assert "vocabulary_candidate_review=BLOCKED blocked_candidates=1" in completed.stdout


def test_candidate_review_cli_check_clean_returns_zero_for_admissible_candidates(
    tmp_path: Path,
) -> None:
    candidates = _candidates_path(
        tmp_path, [{"candidate_slug": "known_alias", "candidate_label": "Known Alias"}]
    )

    completed = subprocess.run(
        [
            sys.executable,
            "scripts/vocabulary_candidate_review.py",
            "--vocabulary",
            str(_vocabulary_path(tmp_path)),
            "--candidates",
            str(candidates),
            "--check-clean",
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    assert "vocabulary_candidate_review=PASS blocked_candidates=0" in completed.stdout


def test_candidate_review_cli_report_exposes_blocked_candidates(tmp_path: Path) -> None:
    report = build_review_report(
        vocabulary_path=_vocabulary_path(tmp_path),
        candidates_path=_candidates_path(
            tmp_path,
            [
                {"candidate_slug": "known_alias", "candidate_label": "Known Alias"},
                {"candidate_slug": "forbidden_phrase", "candidate_label": "Forbidden Phrase"},
                {"candidate_slug": "partial_payload"},
            ],
        ),
    )

    assert [item["status"] for item in report["blocked_candidates"]] == [
        "quarantined",
        "invalid",
    ]


def test_candidate_review_cli_summary_only_suppresses_full_reviews(tmp_path: Path) -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "scripts/vocabulary_candidate_review.py",
            "--vocabulary",
            str(_vocabulary_path(tmp_path)),
            "--candidates",
            str(
                _candidates_path(
                    tmp_path,
                    [
                        {"candidate_slug": "known_alias", "candidate_label": "Known Alias"},
                        {"candidate_slug": "forbidden_phrase", "candidate_label": "Forbidden Phrase"},
                    ],
                )
            ),
            "--summary-only",
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    payload = json.loads(completed.stdout)
    assert payload["trigger"] == "vocabulary_candidate_review_summary"
    assert payload["summary"]["statuses"] == {
        "admissible": 1,
        "quarantined": 1,
        "invalid": 0,
    }
    assert "reviews" not in payload
    assert [item["candidate_slug"] for item in payload["blocked_candidates"]] == [
        "forbidden_phrase"
    ]


def test_candidate_review_cli_writes_pass_receipt(tmp_path: Path) -> None:
    receipt = tmp_path / "receipts" / "candidate_review.json"

    status = main(
        [
            "--vocabulary",
            str(_vocabulary_path(tmp_path)),
            "--candidates",
            str(
                _candidates_path(
                    tmp_path,
                    [{"candidate_slug": "known_alias", "candidate_label": "Known Alias"}],
                )
            ),
            "--receipt",
            str(receipt),
            "--check-clean",
        ]
    )

    payload = json.loads(receipt.read_text(encoding="utf-8"))
    assert status == 0
    assert payload["trigger"] == "vocabulary_candidate_review_receipt"
    assert payload["status"] == "PASS"
    assert payload["exit_code"] == 0
    assert payload["blocked_candidates"] == []


def test_candidate_review_cli_writes_blocked_receipt(tmp_path: Path) -> None:
    receipt = tmp_path / "receipts" / "candidate_review_blocked.json"

    status = main(
        [
            "--vocabulary",
            str(_vocabulary_path(tmp_path)),
            "--candidates",
            str(
                _candidates_path(
                    tmp_path,
                    [
                        {"candidate_slug": "forbidden_phrase", "candidate_label": "Forbidden Phrase"},
                    ],
                )
            ),
            "--receipt",
            str(receipt),
            "--check-clean",
        ]
    )

    payload = json.loads(receipt.read_text(encoding="utf-8"))
    assert status == 1
    assert payload["status"] == "BLOCKED"
    assert payload["exit_code"] == 1
    assert payload["blocked_candidates"][0]["candidate_slug"] == "forbidden_phrase"


def test_candidate_review_cli_writes_error_receipt_for_invalid_payload_shape(
    tmp_path: Path,
) -> None:
    receipt = tmp_path / "receipts" / "candidate_review_error.json"
    candidates = _candidates_path(tmp_path, ["not-an-object"])

    completed = subprocess.run(
        [
            sys.executable,
            "scripts/vocabulary_candidate_review.py",
            "--vocabulary",
            str(_vocabulary_path(tmp_path)),
            "--candidates",
            str(candidates),
            "--receipt",
            str(receipt),
        ],
        check=False,
        text=True,
        capture_output=True,
    )

    payload = json.loads(receipt.read_text(encoding="utf-8"))
    assert completed.returncode != 0
    assert payload["status"] == "ERROR"
    assert payload["exit_code"] == 2
    assert "candidate payload entries must be JSON objects" in payload["error"]


def test_candidate_review_cli_accepts_candidates_from_stdin(tmp_path: Path) -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "scripts/vocabulary_candidate_review.py",
            "--vocabulary",
            str(_vocabulary_path(tmp_path)),
            "--candidates",
            "-",
            "--summary-only",
        ],
        input=json.dumps(
            [{"candidate_slug": "known_alias", "candidate_label": "Known Alias"}]
        ),
        check=True,
        text=True,
        capture_output=True,
    )

    payload = json.loads(completed.stdout)
    assert payload["candidates_path"] == "-"
    assert payload["summary"]["actions"]["alias_only"] == 1


def test_candidate_review_cli_stdin_receipt_records_stdin_candidate_source(
    tmp_path: Path,
) -> None:
    receipt = tmp_path / "receipts" / "candidate_review_stdin.json"

    completed = subprocess.run(
        [
            sys.executable,
            "scripts/vocabulary_candidate_review.py",
            "--vocabulary",
            str(_vocabulary_path(tmp_path)),
            "--candidates",
            "-",
            "--receipt",
            str(receipt),
            "--check-clean",
        ],
        input=json.dumps(
            [{"candidate_slug": "known_alias", "candidate_label": "Known Alias"}]
        ),
        check=True,
        text=True,
        capture_output=True,
    )

    payload = json.loads(receipt.read_text(encoding="utf-8"))
    assert "vocabulary_candidate_review=PASS" in completed.stdout
    assert payload["candidates_path"] == "-"
    assert payload["status"] == "PASS"


def test_candidate_review_cli_check_clean_returns_nonzero_for_invalid_candidate_aliases(
    tmp_path: Path,
) -> None:
    candidates = _candidates_path(
        tmp_path,
        [
            {
                "candidate_slug": "bad_aliases",
                "candidate_label": "Bad Aliases",
                "aliases": "not-a-list",
            }
        ],
    )

    completed = subprocess.run(
        [
            sys.executable,
            "scripts/vocabulary_candidate_review.py",
            "--vocabulary",
            str(_vocabulary_path(tmp_path)),
            "--candidates",
            str(candidates),
            "--check-clean",
        ],
        check=False,
        text=True,
        capture_output=True,
    )

    assert completed.returncode == 1
    assert "vocabulary_candidate_review=BLOCKED blocked_candidates=1" in completed.stdout
