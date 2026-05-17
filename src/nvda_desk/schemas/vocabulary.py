"""Canonical vocabulary governance contracts.

This module stays dependency-light so vocabulary validation can run before wider
runtime dependencies are needed.  The schema owns validation and proof helper
methods only; generator ownership of the committed canonical vocabulary remains
in :mod:`nvda_desk.vocabulary_builder`.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, replace
from enum import Enum
from pathlib import Path
from typing import Any, Mapping, TypeVar


def _normalise_token(value: str) -> str:
    return value.strip().casefold()


class VocabularyCategory(str, Enum):
    AUDIT_CLASSIFICATION = "audit_classification"
    AUDIT_SURFACE = "audit_surface"
    AUTHORITY_CLASS = "authority_class"
    AUTHORITY_SURFACE = "authority_surface"
    CARRIER = "carrier"
    PARALLEL_RISK_SURFACE = "parallel_risk_surface"
    PERSISTENCE_RULE = "persistence_rule"
    PERSISTENCE_SURFACE = "persistence_surface"
    PROMOTION_RULE = "promotion_rule"
    PROMOTION_SURFACE = "promotion_surface"
    PROTOCOL = "protocol"
    PROTOCOL_FIELD = "protocol_field"
    PROTOCOL_SURFACE = "protocol_surface"
    REFERENCE_DATA = "reference_data"
    REVIEW_SURFACE = "review_surface"
    STAGE = "stage"
    WORKFLOW = "workflow"


class RawDerivedTag(str, Enum):
    RAW = "raw"
    DERIVED = "derived"
    NOT_APPLICABLE = "not_applicable"


class VocabularyCandidateAction(str, Enum):
    ENRICH_EXISTING = "enrich_existing"
    ADD_NEW = "add_new"
    ALIAS_ONLY = "alias_only"
    QUARANTINE = "quarantine"


class VocabularyCandidateReviewStatus(str, Enum):
    ADMISSIBLE = "admissible"
    QUARANTINED = "quarantined"
    INVALID = "invalid"


EnumT = TypeVar("EnumT", bound=Enum)


def _coerce_enum(enum_type: type[EnumT], value: EnumT | str, field_name: str) -> EnumT:
    if isinstance(value, enum_type):
        return value
    if isinstance(value, str):
        try:
            return enum_type(value)
        except ValueError as exc:
            allowed = ", ".join(member.value for member in enum_type)
            if field_name == "category":
                raise ValueError(
                    f"category is not governed; category must be one of: {allowed}"
                ) from exc
            raise ValueError(f"{field_name} must be one of: {allowed}") from exc
    raise TypeError(f"{field_name} must be a string or {enum_type.__name__}")


def _validate_optional_token(value: str | None, field_name: str, slug: str) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string when set for {slug}")
    return value


@dataclass(frozen=True)
class VocabularyCandidate:
    candidate_slug: str
    candidate_label: str
    category: VocabularyCategory | str | None = None
    stage_owner: str | None = None
    maps_to_contract: str | None = None
    raw_or_derived: RawDerivedTag | str | None = None
    aliases: list[str] = field(default_factory=list)

    def tokens(self) -> set[str]:
        required_fields = {
            "candidate_slug": self.candidate_slug,
            "candidate_label": self.candidate_label,
        }
        for field_name, value in required_fields.items():
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be a non-empty string")
        tokens = {_normalise_token(self.candidate_slug), _normalise_token(self.candidate_label)}
        for alias in self.aliases:
            if not isinstance(alias, str) or not alias.strip():
                raise ValueError("candidate aliases must be non-empty strings")
            tokens.add(_normalise_token(alias))
        if self.category is not None:
            _coerce_enum(VocabularyCategory, self.category, "category")
        if self.raw_or_derived is not None:
            _coerce_enum(RawDerivedTag, self.raw_or_derived, "raw_or_derived")
        return tokens

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> VocabularyCandidate:
        if not isinstance(payload, Mapping):
            raise ValueError("candidate payload must be a mapping")
        aliases = payload.get("aliases", [])
        if aliases is None:
            aliases = []
        if not isinstance(aliases, list):
            raise ValueError("candidate aliases must be a list")
        return cls(
            candidate_slug=payload["candidate_slug"],
            candidate_label=payload["candidate_label"],
            category=payload.get("category"),
            stage_owner=payload.get("stage_owner"),
            maps_to_contract=payload.get("maps_to_contract"),
            raw_or_derived=payload.get("raw_or_derived"),
            aliases=list(aliases),
        )


@dataclass(frozen=True)
class VocabularyCandidateClassification:
    action: VocabularyCandidateAction
    candidate_slug: str
    matched_slug: str | None = None
    reason: str = ""

    def to_dict(self) -> dict[str, str | None]:
        return {
            "action": self.action.value,
            "candidate_slug": self.candidate_slug,
            "matched_slug": self.matched_slug,
            "reason": self.reason,
        }


@dataclass(frozen=True)
class VocabularyCandidateAdmissionPlan:
    classification: VocabularyCandidateClassification
    proposed_entry: VocabularyEntry | None = None
    alias_candidates: list[str] = field(default_factory=list)
    quarantine_reason: str | None = None

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "classification": self.classification.to_dict(),
            "proposed_entry": (
                self.proposed_entry.to_dict() if self.proposed_entry is not None else None
            ),
            "alias_candidates": list(self.alias_candidates),
            "quarantine_reason": self.quarantine_reason,
        }
        return payload


@dataclass(frozen=True)
class VocabularyCandidateAdmissionReview:
    status: VocabularyCandidateReviewStatus
    candidate_slug: str | None
    plan: VocabularyCandidateAdmissionPlan | None = None
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status.value,
            "candidate_slug": self.candidate_slug,
            "plan": self.plan.to_dict() if self.plan is not None else None,
            "error": self.error,
        }


@dataclass(frozen=True)
class VocabularyEntry:
    canonical_slug: str
    canonical_label: str
    category: VocabularyCategory | str
    stage_owner: str
    maps_to_contract: str
    family: str | None = None
    setup_variant: str | None = None
    execution_expression: str | None = None
    horizon: str | None = None
    raw_or_derived: RawDerivedTag | str = RawDerivedTag.NOT_APPLICABLE
    allowed_aliases: list[str] = field(default_factory=list)
    disallowed_phrases: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        object.__setattr__(self, "category", self._category())
        object.__setattr__(self, "raw_or_derived", self._raw_or_derived())

    def _category(self) -> VocabularyCategory:
        return _coerce_enum(VocabularyCategory, self.category, "category")

    def _raw_or_derived(self) -> RawDerivedTag:
        return _coerce_enum(RawDerivedTag, self.raw_or_derived, "raw_or_derived")

    def validate(self) -> None:
        required_fields = {
            "canonical_slug": self.canonical_slug,
            "canonical_label": self.canonical_label,
            "stage_owner": self.stage_owner,
            "maps_to_contract": self.maps_to_contract,
        }
        for field_name, value in required_fields.items():
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be a non-empty string")

        self._category()
        self._raw_or_derived()
        _validate_optional_token(self.family, "family", self.canonical_slug)
        _validate_optional_token(self.setup_variant, "setup_variant", self.canonical_slug)
        _validate_optional_token(
            self.execution_expression, "execution_expression", self.canonical_slug
        )
        _validate_optional_token(self.horizon, "horizon", self.canonical_slug)

        if len(self.allowed_aliases) != len(set(self.allowed_aliases)):
            raise ValueError(f"allowed_aliases must be unique for {self.canonical_slug}")
        if len(self.disallowed_phrases) != len(set(self.disallowed_phrases)):
            raise ValueError(f"disallowed_phrases must be unique for {self.canonical_slug}")

        canonical_slug_token = _normalise_token(self.canonical_slug)
        canonical_label_token = _normalise_token(self.canonical_label)

        alias_tokens: set[str] = set()
        for alias in self.allowed_aliases:
            if not isinstance(alias, str) or not alias.strip():
                raise ValueError(
                    f"alias entries must be non-empty strings for {self.canonical_slug}"
                )
            alias_token = _normalise_token(alias)
            if alias_token in {canonical_slug_token, canonical_label_token}:
                raise ValueError(
                    f"canonical slug or label cannot also be an alias for {self.canonical_slug}"
                )
            if alias_token in alias_tokens:
                raise ValueError(
                    f"normalised alias duplication for {self.canonical_slug}: {alias!r}"
                )
            alias_tokens.add(alias_token)

        disallowed_tokens: set[str] = set()
        for phrase in self.disallowed_phrases:
            if not isinstance(phrase, str) or not phrase.strip():
                raise ValueError(
                    f"disallowed phrases must be non-empty strings for {self.canonical_slug}"
                )
            phrase_token = _normalise_token(phrase)
            if phrase_token in {canonical_slug_token, canonical_label_token}:
                raise ValueError(
                    f"canonical slug or label cannot also be a disallowed phrase for {self.canonical_slug}"
                )
            if phrase_token in alias_tokens:
                raise ValueError(
                    f"phrase cannot be both allowed alias and disallowed phrase for {self.canonical_slug}: {phrase!r}"
                )
            if phrase_token in disallowed_tokens:
                raise ValueError(
                    f"normalised disallowed phrase duplication for {self.canonical_slug}: {phrase!r}"
                )
            disallowed_tokens.add(phrase_token)

    def to_dict(self) -> dict[str, Any]:
        self.validate()
        payload: dict[str, Any] = {
            "canonical_slug": self.canonical_slug,
            "canonical_label": self.canonical_label,
            "category": self._category().value,
            "stage_owner": self.stage_owner,
            "maps_to_contract": self.maps_to_contract,
            "allowed_aliases": list(self.allowed_aliases),
            "disallowed_phrases": list(self.disallowed_phrases),
            "notes": list(self.notes),
        }
        optional_fields = {
            "family": self.family,
            "setup_variant": self.setup_variant,
            "execution_expression": self.execution_expression,
            "horizon": self.horizon,
        }
        for field_name, value in optional_fields.items():
            if value is not None:
                payload[field_name] = value
        raw_or_derived = self._raw_or_derived()
        if raw_or_derived is not RawDerivedTag.NOT_APPLICABLE:
            payload["raw_or_derived"] = raw_or_derived.value
        return payload


@dataclass(frozen=True)
class VocabularyDocument:
    schema_version: str
    registry_version: str
    notes: list[str] = field(default_factory=list)
    entries: list[VocabularyEntry] = field(default_factory=list)

    @property
    def entry_index(self) -> dict[str, VocabularyEntry]:
        self.validate()
        return {entry.canonical_slug: entry for entry in self.entries}

    def validate(self) -> None:
        if not isinstance(self.schema_version, str) or not self.schema_version.strip():
            raise ValueError("schema_version must be a non-empty string")
        if not isinstance(self.registry_version, str) or not self.registry_version.strip():
            raise ValueError("registry_version must be a non-empty string")

        slug_owner: dict[str, str] = {}
        label_owner: dict[str, str] = {}
        alias_owner: dict[str, str] = {}
        disallowed_owner: dict[str, str] = {}
        for entry in self.entries:
            entry.validate()
            slug_token = _normalise_token(entry.canonical_slug)
            label_token = _normalise_token(entry.canonical_label)
            if slug_token in slug_owner:
                raise ValueError(
                    f"canonical_slug values must be unique after normalisation: {slug_owner[slug_token]!r} vs {entry.canonical_slug!r}"
                )
            slug_owner[slug_token] = entry.canonical_slug
            if label_token in label_owner:
                raise ValueError(
                    f"canonical_label values must be unique after normalisation: {label_owner[label_token]!r} vs {entry.canonical_slug!r}"
                )
            label_owner[label_token] = entry.canonical_slug
            if label_token in alias_owner:
                raise ValueError(
                    f"canonical label collides with alias of {alias_owner[label_token]!r}: {entry.canonical_label!r}"
                )
            if label_token in disallowed_owner:
                raise ValueError(
                    f"canonical label collides with disallowed phrase of {disallowed_owner[label_token]!r}: {entry.canonical_label!r}"
                )
            for alias in entry.allowed_aliases:
                alias_token = _normalise_token(alias)
                if alias_token in slug_owner:
                    raise ValueError(
                        f"alias collides with canonical slug of {slug_owner[alias_token]!r}: {alias!r}"
                    )
                if alias_token in label_owner:
                    raise ValueError(
                        f"alias collides with canonical label of {label_owner[alias_token]!r}: {alias!r}"
                    )
                owner = alias_owner.setdefault(alias_token, entry.canonical_slug)
                if owner != entry.canonical_slug:
                    raise ValueError(
                        f"alias collision for {alias!r}: {owner} vs {entry.canonical_slug}"
                    )
                if alias_token in disallowed_owner:
                    raise ValueError(
                        f"alias collides with disallowed phrase of {disallowed_owner[alias_token]!r}: {alias!r}"
                    )
            for phrase in entry.disallowed_phrases:
                phrase_token = _normalise_token(phrase)
                if phrase_token in slug_owner:
                    raise ValueError(
                        f"disallowed phrase collides with canonical slug of {slug_owner[phrase_token]!r}: {phrase!r}"
                    )
                if phrase_token in label_owner:
                    raise ValueError(
                        f"disallowed phrase collides with canonical label of {label_owner[phrase_token]!r}: {phrase!r}"
                    )
                owner = disallowed_owner.setdefault(phrase_token, entry.canonical_slug)
                if owner != entry.canonical_slug:
                    raise ValueError(
                        f"disallowed phrase collision for {phrase!r}: {owner} vs {entry.canonical_slug}"
                    )
                if phrase_token in alias_owner:
                    raise ValueError(
                        f"disallowed phrase collides with alias of {alias_owner[phrase_token]!r}: {phrase!r}"
                    )

    def classify_candidate(
        self, candidate: VocabularyCandidate
    ) -> VocabularyCandidateClassification:
        self.validate()
        candidate_tokens = candidate.tokens()

        token_owners: dict[str, tuple[str, str]] = {}
        disallowed_owners: dict[str, str] = {}
        for entry in self.entries:
            slug_token = _normalise_token(entry.canonical_slug)
            label_token = _normalise_token(entry.canonical_label)
            token_owners[slug_token] = (entry.canonical_slug, "canonical_slug")
            token_owners[label_token] = (entry.canonical_slug, "canonical_label")
            for alias in entry.allowed_aliases:
                token_owners[_normalise_token(alias)] = (entry.canonical_slug, "allowed_alias")
            for phrase in entry.disallowed_phrases:
                disallowed_owners[_normalise_token(phrase)] = entry.canonical_slug

        disallowed_matches = sorted(candidate_tokens & set(disallowed_owners))
        if disallowed_matches:
            token = disallowed_matches[0]
            return VocabularyCandidateClassification(
                action=VocabularyCandidateAction.QUARANTINE,
                candidate_slug=candidate.candidate_slug,
                matched_slug=disallowed_owners[token],
                reason="candidate token matches disallowed vocabulary phrase",
            )

        matches: dict[str, set[str]] = {}
        for token in candidate_tokens:
            owner = token_owners.get(token)
            if owner is None:
                continue
            matched_slug, match_type = owner
            matches.setdefault(matched_slug, set()).add(match_type)

        if len(matches) > 1:
            return VocabularyCandidateClassification(
                action=VocabularyCandidateAction.QUARANTINE,
                candidate_slug=candidate.candidate_slug,
                reason="candidate tokens match multiple governed vocabulary entries",
            )
        if not matches:
            return VocabularyCandidateClassification(
                action=VocabularyCandidateAction.ADD_NEW,
                candidate_slug=candidate.candidate_slug,
                reason="candidate does not match governed slugs, labels, aliases, or disallowed phrases",
            )

        matched_slug, match_types = next(iter(matches.items()))
        if match_types <= {"allowed_alias"}:
            action = VocabularyCandidateAction.ALIAS_ONLY
            reason = "candidate matches an explicit allowed alias of an existing governed term"
        elif "allowed_alias" in match_types:
            action = VocabularyCandidateAction.ALIAS_ONLY
            reason = "candidate contains an alias match and must be handled as alias-only"
        else:
            action = VocabularyCandidateAction.ENRICH_EXISTING
            reason = "candidate matches an existing governed slug or label"
        return VocabularyCandidateClassification(
            action=action,
            candidate_slug=candidate.candidate_slug,
            matched_slug=matched_slug,
            reason=reason,
        )

    def classify_candidate_payload(
        self, payload: Mapping[str, Any]
    ) -> VocabularyCandidateClassification:
        return self.classify_candidate(VocabularyCandidate.from_dict(payload))

    def classify_candidates(
        self, candidates: list[VocabularyCandidate]
    ) -> list[VocabularyCandidateClassification]:
        return [self.classify_candidate(candidate) for candidate in candidates]

    def plan_candidate_admission(
        self, candidate: VocabularyCandidate
    ) -> VocabularyCandidateAdmissionPlan:
        classification = self.classify_candidate(candidate)
        if classification.action is VocabularyCandidateAction.QUARANTINE:
            return VocabularyCandidateAdmissionPlan(
                classification=classification,
                quarantine_reason=classification.reason,
            )
        if classification.action is VocabularyCandidateAction.ADD_NEW:
            missing_fields = [
                field_name
                for field_name, value in {
                    "category": candidate.category,
                    "stage_owner": candidate.stage_owner,
                    "maps_to_contract": candidate.maps_to_contract,
                    "raw_or_derived": candidate.raw_or_derived,
                }.items()
                if value is None
            ]
            if missing_fields:
                raise ValueError(
                    "add_new candidate admission requires: " + ", ".join(missing_fields)
                )
            proposed_entry = VocabularyEntry(
                canonical_slug=candidate.candidate_slug,
                canonical_label=candidate.candidate_label,
                category=candidate.category,
                stage_owner=candidate.stage_owner or "",
                maps_to_contract=candidate.maps_to_contract or "",
                raw_or_derived=candidate.raw_or_derived or RawDerivedTag.NOT_APPLICABLE,
                allowed_aliases=list(candidate.aliases),
            )
            proposed_entry.validate()
            return VocabularyCandidateAdmissionPlan(
                classification=classification, proposed_entry=proposed_entry
            )
        if classification.matched_slug is None:
            return VocabularyCandidateAdmissionPlan(
                classification=VocabularyCandidateClassification(
                    action=VocabularyCandidateAction.QUARANTINE,
                    candidate_slug=candidate.candidate_slug,
                    reason="non-add candidate classification did not resolve a governed vocabulary entry",
                ),
                quarantine_reason="non-add candidate classification did not resolve a governed vocabulary entry",
            )
        matched_entry = self.entry_index[classification.matched_slug]
        existing_tokens = {
            _normalise_token(matched_entry.canonical_slug),
            _normalise_token(matched_entry.canonical_label),
            *{_normalise_token(alias) for alias in matched_entry.allowed_aliases},
        }
        alias_candidates = []
        for alias in [candidate.candidate_label, *candidate.aliases]:
            if _normalise_token(alias) not in existing_tokens:
                alias_candidates.append(alias)
        return VocabularyCandidateAdmissionPlan(
            classification=classification,
            alias_candidates=alias_candidates,
        )

    def plan_candidate_admissions(
        self, candidates: list[VocabularyCandidate]
    ) -> list[VocabularyCandidateAdmissionPlan]:
        return [self.plan_candidate_admission(candidate) for candidate in candidates]

    def candidate_admission_summary(self, candidates: list[VocabularyCandidate]) -> dict[str, int]:
        summary = {action.value: 0 for action in VocabularyCandidateAction}
        for plan in self.plan_candidate_admissions(candidates):
            summary[plan.classification.action.value] += 1
        return summary

    def with_candidate_admission(self, candidate: VocabularyCandidate) -> VocabularyDocument:
        plan = self.plan_candidate_admission(candidate)
        if plan.classification.action is VocabularyCandidateAction.QUARANTINE:
            raise ValueError("quarantined vocabulary candidate cannot be admitted")
        if plan.classification.action is VocabularyCandidateAction.ADD_NEW:
            if plan.proposed_entry is None:
                raise ValueError("add_new candidate admission requires a proposed entry")
            document = VocabularyDocument(
                schema_version=self.schema_version,
                registry_version=self.registry_version,
                notes=list(self.notes),
                entries=[*self.entries, plan.proposed_entry],
            )
            document.validate()
            return document
        matched_slug = plan.classification.matched_slug
        if matched_slug is None:
            raise ValueError("candidate admission requires a matched governed entry")

        new_entries: list[VocabularyEntry] = []
        for entry in self.entries:
            if entry.canonical_slug != matched_slug:
                new_entries.append(entry)
                continue
            alias_tokens = {_normalise_token(alias) for alias in entry.allowed_aliases}
            aliases = list(entry.allowed_aliases)
            for alias in plan.alias_candidates:
                alias_token = _normalise_token(alias)
                if alias_token not in alias_tokens:
                    aliases.append(alias)
                    alias_tokens.add(alias_token)
            new_entries.append(replace(entry, allowed_aliases=aliases))

        document = VocabularyDocument(
            schema_version=self.schema_version,
            registry_version=self.registry_version,
            notes=list(self.notes),
            entries=new_entries,
        )
        document.validate()
        return document

    def with_candidate_admissions(
        self, candidates: list[VocabularyCandidate]
    ) -> VocabularyDocument:
        document = self
        for candidate in candidates:
            document = document.with_candidate_admission(candidate)
        return document

    def review_candidate_admission(
        self, candidate: VocabularyCandidate
    ) -> VocabularyCandidateAdmissionReview:
        candidate_slug = getattr(candidate, "candidate_slug", None)
        try:
            plan = self.plan_candidate_admission(candidate)
        except (TypeError, ValueError) as exc:
            return VocabularyCandidateAdmissionReview(
                status=VocabularyCandidateReviewStatus.INVALID,
                candidate_slug=candidate_slug if isinstance(candidate_slug, str) else None,
                error=str(exc),
            )
        if plan.classification.action is VocabularyCandidateAction.QUARANTINE:
            return VocabularyCandidateAdmissionReview(
                status=VocabularyCandidateReviewStatus.QUARANTINED,
                candidate_slug=plan.classification.candidate_slug,
                plan=plan,
                error=plan.quarantine_reason,
            )
        return VocabularyCandidateAdmissionReview(
            status=VocabularyCandidateReviewStatus.ADMISSIBLE,
            candidate_slug=plan.classification.candidate_slug,
            plan=plan,
        )

    def review_candidate_payload_admission(
        self, payload: Mapping[str, Any]
    ) -> VocabularyCandidateAdmissionReview:
        candidate_slug = None
        if isinstance(payload, Mapping):
            raw_slug = payload.get("candidate_slug")
            if isinstance(raw_slug, str):
                candidate_slug = raw_slug
        try:
            candidate = VocabularyCandidate.from_dict(payload)
        except (KeyError, TypeError, ValueError) as exc:
            return VocabularyCandidateAdmissionReview(
                status=VocabularyCandidateReviewStatus.INVALID,
                candidate_slug=candidate_slug,
                error=str(exc),
            )
        return self.review_candidate_admission(candidate)

    def review_candidate_admissions(
        self, candidates: list[VocabularyCandidate]
    ) -> list[VocabularyCandidateAdmissionReview]:
        return [self.review_candidate_admission(candidate) for candidate in candidates]

    def review_candidate_payload_admissions(
        self, payloads: list[Mapping[str, Any]]
    ) -> list[VocabularyCandidateAdmissionReview]:
        return [self.review_candidate_payload_admission(payload) for payload in payloads]

    def candidate_admission_review_summary(
        self, candidates: list[VocabularyCandidate]
    ) -> dict[str, dict[str, int]]:
        status_summary = {status.value: 0 for status in VocabularyCandidateReviewStatus}
        action_summary = {action.value: 0 for action in VocabularyCandidateAction}
        for review in self.review_candidate_admissions(candidates):
            status_summary[review.status.value] += 1
            if review.plan is not None:
                action_summary[review.plan.classification.action.value] += 1
        return {"statuses": status_summary, "actions": action_summary}

    def candidate_payload_admission_review_summary(
        self, payloads: list[Mapping[str, Any]]
    ) -> dict[str, dict[str, int]]:
        status_summary = {status.value: 0 for status in VocabularyCandidateReviewStatus}
        action_summary = {action.value: 0 for action in VocabularyCandidateAction}
        for review in self.review_candidate_payload_admissions(payloads):
            status_summary[review.status.value] += 1
            if review.plan is not None:
                action_summary[review.plan.classification.action.value] += 1
        return {"statuses": status_summary, "actions": action_summary}

    def candidate_admission_review_report(
        self, candidates: list[VocabularyCandidate]
    ) -> dict[str, Any]:
        reviews = self.review_candidate_admissions(candidates)
        return {
            "summary": self.candidate_admission_review_summary(candidates),
            "reviews": [review.to_dict() for review in reviews],
        }

    def candidate_payload_admission_review_report(
        self, payloads: list[Mapping[str, Any]]
    ) -> dict[str, Any]:
        reviews = self.review_candidate_payload_admissions(payloads)
        return {
            "summary": self.candidate_payload_admission_review_summary(payloads),
            "reviews": [review.to_dict() for review in reviews],
        }

    def to_dict(self) -> dict[str, Any]:
        self.validate()
        return {
            "schema_version": self.schema_version,
            "registry_version": self.registry_version,
            "notes": list(self.notes),
            "entries": [entry.to_dict() for entry in self.entries],
        }

    @classmethod
    def from_json_text(cls, text: str) -> VocabularyDocument:
        payload = json.loads(text)
        if not isinstance(payload, Mapping):
            raise ValueError("JSON root must decode to an object mapping")
        return vocabulary_document_from_dict(dict(payload))

    @classmethod
    def from_json_path(cls, path: str | Path) -> VocabularyDocument:
        return cls.from_json_text(Path(path).read_text(encoding="utf-8"))

    def to_json_text(self) -> str:
        return json.dumps(self.to_dict(), indent=2, sort_keys=False) + "\n"


def vocabulary_document_from_dict(payload: Mapping[str, Any]) -> VocabularyDocument:
    allowed_fields = {"schema_version", "registry_version", "notes", "entries"}
    unknown_fields = sorted(set(payload) - allowed_fields)
    if unknown_fields:
        joined = ", ".join(unknown_fields)
        raise ValueError(f"unknown top-level vocabulary document field(s): {joined}")

    entry_payloads = payload.get("entries", [])
    if not isinstance(entry_payloads, list):
        raise ValueError("entries must be a list")
    entries = [VocabularyEntry(**entry_payload) for entry_payload in entry_payloads]
    document = VocabularyDocument(
        schema_version=payload["schema_version"],
        registry_version=payload["registry_version"],
        notes=list(payload.get("notes", [])),
        entries=entries,
    )
    document.validate()
    return document
