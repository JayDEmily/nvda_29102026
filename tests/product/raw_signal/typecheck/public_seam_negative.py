from datetime import datetime

from nvda_desk.raw_signal_occurrence_truth import api


def reject_cross_layer_types(
    policy: api.CaptureScopePolicyV1,
    capture: api.ScheduledCaptureOccurrenceV1,
    observation: api.RawObservationOccurrenceV1,
    assessment: api.CaptureReceiptPresenceAssessmentV1,
    when: datetime,
) -> None:
    owner = api.create_owner()

    owner.commands.register_capture_scope_policy(observation)  # STATIC_NEGATIVE register_policy
    owner.commands.realise_scheduled_capture_occurrence(
        scope_policy_ref=capture.scope_policy_ref,
        capture_occurrence_id=observation.observation_occurrence_id,  # STATIC_NEGATIVE capture
        slot_start_utc=capture.slot_start_utc,
    )
    owner.commands.admit_raw_observation_occurrence(policy)  # STATIC_NEGATIVE admit_observation
    owner.commands.derive_capture_receipt_evidence_relation(
        observation_occurrence_ref=capture.capture_occurrence_id,  # STATIC_NEGATIVE derive_relation
        capture_occurrence_ref=capture.capture_occurrence_id,
        scope_policy_ref=capture.scope_policy_ref,
    )
    owner.commands.append_capture_receipt_presence_assessment(
        assessment_occurrence_id=observation.observation_occurrence_id,  # STATIC_NEGATIVE asmt
        capture_occurrence_ref=capture.capture_occurrence_id,
        evidence_as_of_ts_utc=when,
        supersedes_assessment_ref=assessment.supersedes_assessment_ref,
    )
    owner.commands.reconcile_owed_slots(
        scope_policy_ref=observation.observation_occurrence_id,  # STATIC_NEGATIVE reconcile
        slot_starts_utc=[capture.slot_start_utc],
        capture_occurrence_ids=[capture.capture_occurrence_id],
        assessment_occurrence_ids=[assessment.assessment_occurrence_id],
    )

    owner.reads.get_capture_scope_policy(
        capture.capture_occurrence_id,  # STATIC_NEGATIVE read_policy
        policy.scope_policy_version,
    )
    owner.reads.get_scheduled_capture_occurrence(
        observation.observation_occurrence_id  # STATIC_NEGATIVE read_capture
    )
    owner.reads.get_raw_observation_occurrence(
        capture.capture_occurrence_id  # STATIC_NEGATIVE read_observation
    )
    owner.reads.get_receipt_presence_assessment(
        observation.observation_occurrence_id  # STATIC_NEGATIVE read_assessment
    )
    owner.reads.list_receipt_presence_assessments(
        observation.observation_occurrence_id  # STATIC_NEGATIVE list_assessments
    )
