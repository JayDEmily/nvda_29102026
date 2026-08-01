from __future__ import annotations

from nvda_desk.schemas.vocabulary import (
    RawDerivedTag,
    VocabularyCandidate,
    VocabularyCandidateAction,
    VocabularyCandidateReviewStatus,
    VocabularyDocument,
    VocabularyEntry,
)


def _document() -> VocabularyDocument:
    return VocabularyDocument(
        schema_version="v1",
        registry_version="test",
        entries=[
            VocabularyEntry(
                canonical_slug="governed_term",
                canonical_label="Governed Term",
                category="workflow",
                stage_owner="vocabulary_governance",
                maps_to_contract="GovernedTermContract",
                raw_or_derived=RawDerivedTag.DERIVED,
                allowed_aliases=["known alias"],
                disallowed_phrases=["forbidden phrase"],
            )
        ],
    )


def test_review_candidate_admission_marks_non_quarantine_plan_admissible() -> None:
    review = _document().review_candidate_admission(
        VocabularyCandidate("known_alias", "Known Alias", aliases=["fresh alias"])
    )

    assert review.status is VocabularyCandidateReviewStatus.ADMISSIBLE
    assert review.plan is not None
    assert review.plan.classification.action is VocabularyCandidateAction.ALIAS_ONLY
    assert review.plan.alias_candidates == ["fresh alias"]
    assert review.error is None


def test_review_candidate_admission_marks_quarantine_without_exception() -> None:
    review = _document().review_candidate_admission(
        VocabularyCandidate("forbidden_phrase", "Forbidden Phrase")
    )

    assert review.status is VocabularyCandidateReviewStatus.QUARANTINED
    assert review.plan is not None
    assert review.plan.classification.action is VocabularyCandidateAction.QUARANTINE
    assert review.error == "candidate token matches disallowed vocabulary phrase"


def test_review_candidate_admission_marks_missing_add_fields_invalid() -> None:
    review = _document().review_candidate_admission(
        VocabularyCandidate("new_term", "New Term", category="workflow")
    )

    assert review.status is VocabularyCandidateReviewStatus.INVALID
    assert review.candidate_slug == "new_term"
    assert review.plan is None
    assert review.error == (
        "add_new candidate admission requires: stage_owner, maps_to_contract, raw_or_derived"
    )


def test_review_candidate_payload_admission_marks_malformed_payload_invalid() -> None:
    review = _document().review_candidate_payload_admission({"candidate_slug": "partial_payload"})

    assert review.status is VocabularyCandidateReviewStatus.INVALID
    assert review.candidate_slug == "partial_payload"
    assert review.plan is None
    assert "candidate_label" in (review.error or "")


def test_review_candidate_payload_admissions_preserve_order() -> None:
    reviews = _document().review_candidate_payload_admissions(
        [
            {"candidate_slug": "known_alias", "candidate_label": "Known Alias"},
            {"candidate_slug": "forbidden_phrase", "candidate_label": "Forbidden Phrase"},
            {"candidate_slug": "partial_payload"},
        ]
    )

    assert [review.candidate_slug for review in reviews] == [
        "known_alias",
        "forbidden_phrase",
        "partial_payload",
    ]
    assert [review.status for review in reviews] == [
        VocabularyCandidateReviewStatus.ADMISSIBLE,
        VocabularyCandidateReviewStatus.QUARANTINED,
        VocabularyCandidateReviewStatus.INVALID,
    ]


def test_candidate_admission_review_summary_counts_statuses_and_actions() -> None:
    summary = _document().candidate_admission_review_summary(
        [
            VocabularyCandidate("known_alias", "Known Alias"),
            VocabularyCandidate("forbidden_phrase", "Forbidden Phrase"),
            VocabularyCandidate("new_term", "New Term", category="workflow"),
        ]
    )

    assert summary == {
        "statuses": {
            "admissible": 1,
            "quarantined": 1,
            "invalid": 1,
        },
        "actions": {
            "enrich_existing": 0,
            "add_new": 0,
            "alias_only": 1,
            "quarantine": 1,
        },
    }


def test_candidate_admission_review_report_is_json_ready() -> None:
    report = _document().candidate_admission_review_report(
        [
            VocabularyCandidate("known_alias", "Known Alias"),
            VocabularyCandidate("forbidden_phrase", "Forbidden Phrase"),
        ]
    )

    assert report["summary"]["statuses"] == {
        "admissible": 1,
        "quarantined": 1,
        "invalid": 0,
    }
    assert report["reviews"][0]["status"] == "admissible"
    assert report["reviews"][0]["plan"]["classification"]["action"] == "alias_only"
    assert report["reviews"][1]["status"] == "quarantined"
    assert report["reviews"][1]["error"] == "candidate token matches disallowed vocabulary phrase"


def test_candidate_payload_admission_review_report_keeps_invalid_payload_in_report() -> None:
    report = _document().candidate_payload_admission_review_report(
        [
            {"candidate_slug": "known_alias", "candidate_label": "Known Alias"},
            {"candidate_slug": "partial_payload"},
        ]
    )

    assert report["summary"]["statuses"] == {
        "admissible": 1,
        "quarantined": 0,
        "invalid": 1,
    }
    assert report["reviews"][1]["candidate_slug"] == "partial_payload"
    assert report["reviews"][1]["plan"] is None


def test_candidate_payload_admission_review_marks_bad_alias_list_invalid() -> None:
    review = _document().review_candidate_payload_admission(
        {
            "candidate_slug": "bad_aliases",
            "candidate_label": "Bad Aliases",
            "aliases": "not-a-list",
        }
    )

    assert review.status is VocabularyCandidateReviewStatus.INVALID
    assert review.candidate_slug == "bad_aliases"
    assert review.plan is None
    assert review.error == "candidate aliases must be a list"
