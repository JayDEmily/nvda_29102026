"""Deterministic vocabulary synonym-candidate audit.

This audit does not call external APIs. It writes a structured escalation artefact
that a later LLM pass in the sandbox can consume.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

from nvda_desk.schemas.vocabulary import (
    VocabularyCandidate,
    VocabularyCandidateAction,
    VocabularyCandidateClassification,
    vocabulary_document_from_dict,
)
from nvda_desk.vocabulary_builder import build_canonical_payload, governed_source_hashes

OUTPUT_PATH = Path("var/vocabulary/synonym_candidates.json")
STAMP_PATH = Path("data/vocabulary/vocabulary_touch_stamp.json")
SCAN_PATHS = [Path("src"), Path("tests"), Path("docs"), Path("config")]
ALLOWED_EXTENSIONS = {".py", ".md", ".yaml", ".yml", ".json", ".toml"}
TOKEN_PATTERN = re.compile(r"[A-Za-z][A-Za-z0-9_\- ]{2,80}")


def _normalise(value: str) -> str:
    return re.sub(r"[_\-\s]+", " ", value.strip().casefold())


def _compact_normalise(value: str) -> str:
    return re.sub(r"[_\-\s]+", "", value.strip().casefold())


def _fingerprint() -> str:
    items = governed_source_hashes()
    blob = json.dumps(items, sort_keys=True).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def _load_document() -> dict:
    payload = build_canonical_payload()
    vocabulary_document_from_dict(payload)
    return payload


def _lexicon(payload: dict) -> tuple[set[str], set[str], list[tuple[str, str, str, str]]]:
    exact_tokens: set[str] = set()
    compact_exact_tokens: set[str] = set()
    entries: list[tuple[str, str, str, str]] = []
    for entry in payload["entries"]:
        label = entry["canonical_label"]
        slug = entry["canonical_slug"]
        canonical_norm = _normalise(label)
        for token in [label, slug]:
            exact_tokens.add(_normalise(token))
            compact_exact_tokens.add(_compact_normalise(token))
        for alias in entry.get("allowed_aliases", []):
            exact_tokens.add(_normalise(alias))
            compact_exact_tokens.add(_compact_normalise(alias))
        for phrase in entry.get("disallowed_phrases", []):
            exact_tokens.add(_normalise(phrase))
            compact_exact_tokens.add(_compact_normalise(phrase))
        entries.append((slug, label, canonical_norm, entry.get("category", "")))
    return exact_tokens, compact_exact_tokens, entries


def _iter_candidates():
    for base in SCAN_PATHS:
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not path.is_file() or path.suffix not in ALLOWED_EXTENSIONS:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for match in TOKEN_PATTERN.finditer(text):
                yield str(path), match.group(0)


def _is_identifier_like(raw_phrase: str) -> bool:
    return (
        " " not in raw_phrase
        and "_" not in raw_phrase
        and "-" not in raw_phrase
        and raw_phrase != raw_phrase.lower()
    )


def _is_protocol_identifier_fragment(
    raw_phrase: str,
    candidate: str,
    target: str,
    category: str,
) -> bool:
    if category != "protocol_field" or "_" not in raw_phrase:
        return False
    candidate_parts = candidate.split()
    target_parts = target.split()
    if not set(target_parts) <= set(candidate_parts):
        return False
    extra_parts = set(candidate_parts) - set(target_parts)
    return len(extra_parts) <= 1


def _is_python_function_declaration_identifier_fragment(
    path: str,
    raw_phrase: str,
    candidate: str,
    target: str,
) -> bool:
    if not path.endswith(".py") or "_" not in raw_phrase:
        return False
    if not raw_phrase.lstrip().startswith("def "):
        return False
    candidate_parts = candidate.split()
    target_parts = target.split()
    if candidate_parts[:1] != ["def"]:
        return False
    return candidate_parts[1:] == target_parts



def _candidate_slug_from_phrase(phrase: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", phrase.strip().casefold()).strip("_")
    if not slug:
        raise ValueError("candidate phrase must yield a non-empty slug")
    return slug


def _escalation_classification(phrase: str, nearest_slug: str) -> dict[str, str | None]:
    return VocabularyCandidateClassification(
        action=VocabularyCandidateAction.QUARANTINE,
        candidate_slug=_candidate_slug_from_phrase(phrase),
        matched_slug=nearest_slug,
        reason="near-match synonym candidate requires LLM escalation before vocabulary admission",
    ).to_dict()


def _escalation_admission_review(phrase: str, nearest_slug: str) -> dict:
    candidate = VocabularyCandidate(
        candidate_slug=_candidate_slug_from_phrase(phrase),
        candidate_label=phrase,
    )
    classification = VocabularyCandidateClassification(
        action=VocabularyCandidateAction.QUARANTINE,
        candidate_slug=candidate.candidate_slug,
        matched_slug=nearest_slug,
        reason="near-match synonym candidate requires LLM escalation before vocabulary admission",
    )
    return {
        "status": "quarantined",
        "candidate_slug": candidate.candidate_slug,
        "plan": {
            "classification": classification.to_dict(),
            "proposed_entry": None,
            "alias_candidates": [],
            "quarantine_reason": classification.reason,
        },
        "error": classification.reason,
    }


def _candidate_score(candidate: str, target: str) -> int:
    c_parts = candidate.split()
    t_parts = target.split()
    if candidate == target:
        return 100
    if candidate.replace(" ", "") == target.replace(" ", ""):
        return 98
    if len(c_parts) == len(t_parts) and set(c_parts) == set(t_parts):
        return 95
    if abs(len(c_parts) - len(t_parts)) == 1:
        smaller = set(c_parts) if len(c_parts) < len(t_parts) else set(t_parts)
        larger = set(c_parts) if len(c_parts) > len(t_parts) else set(t_parts)
        if smaller <= larger and len(smaller) >= 2:
            return 93
    return 0


def build_report() -> dict:
    payload = _load_document()
    exact_tokens, compact_exact_tokens, entries = _lexicon(payload)
    fingerprint = _fingerprint()
    previous_stamp = {}
    if STAMP_PATH.exists():
        previous_stamp = json.loads(STAMP_PATH.read_text(encoding="utf-8"))
    current_touched = previous_stamp.get("fingerprint") != fingerprint

    candidates: list[dict] = []
    seen: set[tuple[str, str]] = set()
    for path, raw_phrase in _iter_candidates():
        if _is_identifier_like(raw_phrase):
            continue
        phrase = _normalise(raw_phrase)
        compact_phrase = _compact_normalise(raw_phrase)
        if len(phrase) < 8 or phrase in exact_tokens or compact_phrase in compact_exact_tokens:
            continue
        best = None
        best_score = 0
        for slug, label, target, category in entries:
            score = _candidate_score(phrase, target)
            if score:
                if _is_protocol_identifier_fragment(raw_phrase, phrase, target, category):
                    score = 0
                if _is_python_function_declaration_identifier_fragment(
                    path, raw_phrase, phrase, target
                ):
                    score = 0
            if score > best_score:
                best = (slug, label)
                best_score = score
        if best is None or best_score < 93:
            continue
        key = (path, phrase)
        if key in seen:
            continue
        seen.add(key)
        candidates.append(
            {
                "phrase": phrase,
                "nearest_slug": best[0],
                "nearest_label": best[1],
                "score": best_score,
                "path": path,
                "resolution_required": "llm_escalation",
            }
        )

    sorted_candidates = sorted(
        candidates, key=lambda item: (-item["score"], item["path"], item["phrase"])
    )
    return {
        "schema_version": "v1",
        "trigger": "vocabulary_governance",
        "vocabulary_touched": current_touched,
        "fingerprint": fingerprint,
        "candidates": sorted_candidates,
        "candidate_classifications": [
            {
                "phrase": item["phrase"],
                "path": item["path"],
                "nearest_slug": item["nearest_slug"],
                "classification": _escalation_classification(
                    str(item["phrase"]), str(item["nearest_slug"])
                ),
                "admission_review": _escalation_admission_review(
                    str(item["phrase"]), str(item["nearest_slug"])
                ),
            }
            for item in sorted_candidates
        ],
    }


def write_report() -> dict:
    report = build_report()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


def write_stamp() -> None:
    report = build_report()
    if report["candidates"]:
        raise RuntimeError(
            "cannot update vocabulary touch stamp while synonym candidates require LLM escalation"
        )
    STAMP_PATH.parent.mkdir(parents=True, exist_ok=True)
    STAMP_PATH.write_text(
        json.dumps({"fingerprint": report["fingerprint"]}, indent=2) + "\n", encoding="utf-8"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check-clean",
        action="store_true",
        help="write the audit report and fail if unresolved synonym candidates exist",
    )
    parser.add_argument(
        "--write-stamp",
        action="store_true",
        help="advance the vocabulary touch stamp only when the audit is clean",
    )
    args = parser.parse_args(argv)

    if args.write_stamp:
        write_stamp()
        print("vocabulary_touch_stamp=UPDATED")
        return 0

    report = write_report()
    candidate_count = len(report["candidates"])
    print(
        "vocabulary_synonym_audit=PASS"
        f" candidates={candidate_count}"
        f" vocabulary_touched={report['vocabulary_touched']}"
    )
    if args.check_clean and candidate_count:
        print("vocabulary_synonym_audit=BLOCKED unresolved_candidates=" + str(candidate_count))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
