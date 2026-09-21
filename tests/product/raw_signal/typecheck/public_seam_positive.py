from collections.abc import Sequence
from datetime import datetime

from nvda_desk.raw_signal_occurrence_truth import api


def exercise_public_seam(
    policy: api.CaptureScopePolicyV1,
    capture: api.ScheduledCaptureOccurrenceV1,
    observation: api.RawObservationOccurrenceV1,
    assessment: api.CaptureReceiptPresenceAssessmentV1,
    when: datetime,
) -> None:
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

    # Keep every inferred expression live so --disallow-any-expr checks the whole seam.
    _ = (
        relation,
        read_policy,
        read_capture,
        read_observation,
        read_assessment,
        read_chain,
        reconciled,
    )
