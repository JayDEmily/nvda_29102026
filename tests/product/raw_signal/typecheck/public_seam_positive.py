from collections.abc import Sequence
from datetime import UTC, datetime
from decimal import Decimal

from nvda_desk.raw_signal_occurrence_truth import api


def exercise_public_seam(when: datetime) -> None:
    native_value: api.NativeValueV1 = {
        "Nested": [None, True, 1, -0.0, Decimal("1.00"), "native", b"bytes", ("tuple",)]
    }
    policy = api.CaptureScopePolicyV1(
        concept_id=api.concept_id("raw_signal.capture_scope_policy"),
        contract_id=api.contract_id("nvda.raw_signal.CaptureScopePolicy.v1"),
        units="not_applicable",
        scope_policy_id=api.scope_policy_id("scope-policy-001"),
        scope_policy_version=1,
        activation_ts_utc=datetime(2026, 9, 20, 12, 0, tzinfo=UTC),
        eligibility_policy_ref=api.eligibility_policy_ref("eligibility-policy:fixture:v1"),
    )
    capture = api.ScheduledCaptureOccurrenceV1(
        concept_id=api.concept_id("raw_signal.scheduled_capture_occurrence"),
        contract_id=api.contract_id("nvda.raw_signal.ScheduledCaptureOccurrence.v1"),
        units="not_applicable",
        capture_occurrence_id=api.capture_occurrence_id("capture-001"),
        scope_policy_ref=api.scope_policy_ref("scope-policy-001@1"),
        slot_start_utc=datetime(2026, 9, 20, 12, 0, tzinfo=UTC),
        slot_end_utc=datetime(2026, 9, 20, 12, 0, 30, tzinfo=UTC),
    )
    observation = api.RawObservationOccurrenceV1(
        concept_id=api.concept_id("raw_signal.raw_observation_occurrence"),
        contract_id=api.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
        observation_occurrence_id=api.observation_occurrence_id("observation-001"),
        delivery_artifact_ref=api.delivery_artifact_ref("delivery-001"),
        source_provider=api.provider_id("provider.fixture"),
        native_record={"Bid Price": "123.45", "Provider Null": None, "Payload": native_value},
        received_ts_utc=datetime(2026, 9, 20, 12, 0, 5, tzinfo=UTC),
        ingestion_sequence=1,
        ingestion_sequence_scope=api.ingestion_sequence_scope("collector.fixture"),
        source_temporal_kind="true_instant",
        source_timestamp_raw="2026-09-20T12:00:04.900000Z",
    )
    relation_payload = api.CaptureReceiptEvidenceRelationV1(
        concept_id=api.concept_id("raw_signal.capture_receipt_evidence_relation"),
        contract_id=api.contract_id("nvda.raw_signal.CaptureReceiptEvidenceRelation.v1"),
        units="not_applicable",
        observation_occurrence_ref=observation.observation_occurrence_id,
        capture_occurrence_ref=capture.capture_occurrence_id,
        scope_policy_ref=capture.scope_policy_ref,
        received_ts_utc=observation.received_ts_utc,
        relation_role="evidences_receipt_presence_only",
    )
    assessment = api.CaptureReceiptPresenceAssessmentV1(
        concept_id=api.concept_id("raw_signal.capture_receipt_presence_assessment"),
        contract_id=api.contract_id("nvda.raw_signal.CaptureReceiptPresenceAssessment.v1"),
        units="not_applicable",
        assessment_occurrence_id=api.assessment_occurrence_id("assessment-001"),
        capture_occurrence_ref=capture.capture_occurrence_id,
        outcome="zero_received",
        evidence_as_of_ts_utc=when,
    )

    owner = api.create_owner()

    stored_policy: api.CaptureScopePolicyV1 = owner.commands.register_capture_scope_policy(policy)
    stored_capture: api.ScheduledCaptureOccurrenceV1 = (
        owner.commands.realise_scheduled_capture_occurrence(
            scope_policy_ref=capture.scope_policy_ref,
            capture_occurrence_id=capture.capture_occurrence_id,
            slot_start_utc=capture.slot_start_utc,
        )
    )
    stored_observation: api.RawObservationOccurrenceV1 = (
        owner.commands.admit_raw_observation_occurrence(observation)
    )
    relation: api.CaptureReceiptEvidenceRelationV1 | None = (
        owner.commands.derive_capture_receipt_evidence_relation(
            observation_occurrence_ref=stored_observation.observation_occurrence_id,
            capture_occurrence_ref=stored_capture.capture_occurrence_id,
            scope_policy_ref=stored_capture.scope_policy_ref,
        )
    )
    stored_assessment: api.CaptureReceiptPresenceAssessmentV1 = (
        owner.commands.append_capture_receipt_presence_assessment(
            assessment_occurrence_id=assessment.assessment_occurrence_id,
            capture_occurrence_ref=stored_capture.capture_occurrence_id,
            evidence_as_of_ts_utc=when,
            supersedes_assessment_ref=assessment.supersedes_assessment_ref,
        )
    )
    reconciled: Sequence[api.CaptureReceiptPresenceAssessmentV1] = (
        owner.commands.reconcile_owed_slots(
            scope_policy_ref=stored_capture.scope_policy_ref,
            slot_starts_utc=[stored_capture.slot_start_utc],
            capture_occurrence_ids=[stored_capture.capture_occurrence_id],
            assessment_occurrence_ids=[stored_assessment.assessment_occurrence_id],
        )
    )

    read_policy: api.CaptureScopePolicyV1 | None = owner.reads.get_capture_scope_policy(
        stored_policy.scope_policy_id,
        stored_policy.scope_policy_version,
    )
    read_capture: api.ScheduledCaptureOccurrenceV1 | None = (
        owner.reads.get_scheduled_capture_occurrence(stored_capture.capture_occurrence_id)
    )
    read_observation: api.RawObservationOccurrenceV1 | None = (
        owner.reads.get_raw_observation_occurrence(stored_observation.observation_occurrence_id)
    )
    read_assessment: api.CaptureReceiptPresenceAssessmentV1 | None = (
        owner.reads.get_receipt_presence_assessment(stored_assessment.assessment_occurrence_id)
    )
    read_chain: Sequence[api.CaptureReceiptPresenceAssessmentV1] = (
        owner.reads.list_receipt_presence_assessments(stored_capture.capture_occurrence_id)
    )

    _ = (
        relation_payload,
        relation,
        read_policy,
        read_capture,
        read_observation,
        read_assessment,
        read_chain,
        reconciled,
    )
