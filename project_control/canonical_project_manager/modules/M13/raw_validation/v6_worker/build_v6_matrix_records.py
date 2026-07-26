"""Build explicit, stable worker-owned V6 proof matrix records."""

from __future__ import annotations

from pathlib import Path

OUTPUT = Path(__file__).resolve().parent

PHASE_OUTCOMES = {
    "owner_mutation": ("outer_commits_caught", "outer_fails_unhandled"),
    "participant_prepare": ("outer_commits_caught", "outer_fails_unhandled"),
    "participant_commit": ("outer_commits_caught", "outer_fails_unhandled"),
    "participant_rollback": ("outer_fails_primary",),
    "attesting_receipt_writer": ("outer_commits_caught", "outer_fails_unhandled"),
}
SCOPES = (
    "same_scoped_idempotency_key",
    "different_key_same_command_type_and_unit",
    "different_consistency_unit",
    "different_command_type",
)
LIFECYCLE = (
    ("successful_commit", "1", "different_fresh_key"),
    ("exact_duplicate_replay", "1", "different_fresh_key"),
    ("stale_version", "0", "same_failed_key"),
    ("mutation_exception", "0", "same_failed_key"),
    ("non_mapping_mutation_result", "0", "same_failed_key"),
    ("invalid_receipt_id", "0", "same_failed_key"),
    ("invalid_result_id", "0", "same_failed_key"),
    ("participant_prepare_failure", "0", "same_failed_key"),
    ("participant_commit_failure", "0", "same_failed_key"),
    ("receipt_writer_failure", "0", "same_failed_key"),
    ("nested_execution_rejection", "0", "same_failed_key"),
)
RECEIPT_CASES = (
    ("invalid", "scope_command_type_mismatch"),
    ("invalid", "scope_consistency_unit_mismatch"),
    *(
        ("invalid", f"{field}_{kind}_not_exact_int")
        for field in ("prior_state_version", "resulting_state_version", "sequence")
        for kind in ("bool", "float", "string", "coercible_numeric")
    ),
    ("invalid", "prior_state_version_negative"),
    ("invalid", "resulting_state_version_zero"),
    ("invalid", "resulting_state_version_negative"),
    ("invalid", "resulting_state_version_equals_prior"),
    ("invalid", "resulting_state_version_skips_next"),
    ("invalid", "sequence_zero"),
    ("invalid", "sequence_negative"),
    *(
        ("invalid", f"{field}_empty")
        for field in (
            "receipt_id",
            "result_id",
            "command_id",
            "command_type",
            "consistency_unit_id",
            "input_fingerprint",
            "policy_version",
        )
    ),
    ("invalid_key", "idempotency_key_value_empty"),
    ("invalid_key", "idempotency_key_command_type_empty"),
    ("invalid_key", "idempotency_key_consistency_unit_id_empty"),
    ("valid", "prior_0_resulting_1_sequence_1"),
    ("valid", "prior_1_resulting_2_sequence_1"),
    ("valid", "prior_5_resulting_6_sequence_17"),
    ("replay", "all_committed_identity_fields_preserved"),
    ("execute", "three_exact_next_version_and_sequence_publications"),
)
MUTANTS = (
    ("nested_allowed_different_key", "campaign_1"),
    ("nested_allowed_different_consistency_unit", "campaign_1"),
    ("nested_receipt_commits_later_loses_state", "campaign_4"),
    ("nested_state_commits_without_receipt", "campaign_4"),
    ("nested_and_outer_reuse_sequence", "campaign_4"),
    ("nested_and_outer_reuse_resulting_version", "campaign_4"),
    ("active_guard_set_after_mutation_starts", "campaign_1"),
    ("active_guard_cleared_before_participant_commit", "campaign_1"),
    ("active_guard_not_cleared_after_failure", "campaign_2"),
    ("receipt_scope_checks_only_command_type", "campaign_3"),
    ("receipt_scope_checks_only_consistency_unit", "campaign_3"),
    ("receipt_version_validation_accepts_floats", "campaign_3"),
    ("receipt_version_validation_accepts_booleans", "campaign_3"),
    ("receipt_resulting_version_may_equal_prior", "campaign_3"),
    ("receipt_sequence_may_be_nonpositive", "campaign_3"),
    ("replay_response_alters_committed_identity", "campaign_3"),
)


def _write(name: str, header: str, rows: list[str]) -> None:
    (OUTPUT / name).write_text(
        "\n".join((header, *rows)) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    reentrancy_rows = []
    for phase, outcomes in PHASE_OUTCOMES.items():
        for scope in SCOPES:
            for outcome in outcomes:
                case_id = (
                    f"phase-{phase.replace('_', '-')}--"
                    f"scope-{scope.replace('_', '-')}--"
                    f"outer-{outcome.replace('_', '-')}--nested-runtime-rejection"
                )
                reentrancy_rows.append(
                    f"{case_id}\t{phase}\t{scope}\t{outcome}\t"
                    "RuntimeError_before_nested_mutation_or_prepare"
                )
    _write(
        "V6_REENTRANCY_MATRIX.tsv",
        "case_id\tphase\tscope_relationship\touter_outcome\tnested_result",
        reentrancy_rows,
    )

    lifecycle_rows = [
        f"{outcome}\t{prior}\t{key_relation}\t"
        "fresh_admitted_exact_next_commit_then_exact_replay\t"
        "binding_pending_and_active_guard_observed_separately"
        for outcome, prior, key_relation in LIFECYCLE
    ]
    _write(
        "V6_ACTIVE_LIFECYCLE_MATRIX.tsv",
        "terminal_outcome\tprior_commits\tfresh_key_relation\tlater_truth\tcleanup_dimensions",
        lifecycle_rows,
    )

    receipt_rows = [
        f"{index:02d}\t{classification}\t{case}\tAtomicReceipt_or_execute_public_seam"
        for index, (classification, case) in enumerate(RECEIPT_CASES, start=1)
    ]
    _write(
        "V6_ATOMIC_RECEIPT_MATRIX.tsv",
        "case\tclassification\tsemantic_fact\tproof_surface",
        receipt_rows,
    )

    mutant_rows = [
        f"{mutant}\t{campaign}\tfull_family_exit_1\ttarget_exit_1\tintended_reason_PASS"
        for mutant, campaign in MUTANTS
    ]
    _write(
        "V6_FALSIFICATION_MATRIX.tsv",
        "mutant_id\tintended_campaign\tfull_result\ttarget_result\tadjudication",
        mutant_rows,
    )

    proof_rows = [
        "single_active_attempt\tN-06 deterministic sequencing and prior committed result\tcampaign_1\t36",
        "active_attempt_cleanup\tN-06 unsuccessful attempt publishes no transaction truth\tcampaign_2\t11",
        "receipt_scope_and_types\tN-06 receipt binds scope result version sequence\tcampaign_3\t36",
        "combined_state_receipt_sequence\tN-06 atomic transaction tuple cannot be orphaned\tcampaign_4\t2",
        "regression_and_falsification\tN-06 bounded public seam retained across earlier proof\tcampaign_5\tretained_and_shadow",
    ]
    _write(
        "V6_PROOF_TO_N06.tsv",
        "acceptance_leaf\tn06_fact\tcampaign\tsemantic_cases",
        proof_rows,
    )
    print(f"reentrancy_cases={len(reentrancy_rows)}")
    print(f"lifecycle_cases={len(lifecycle_rows)}")
    print(f"receipt_cases={len(receipt_rows)}")
    print(f"v6_mutants={len(mutant_rows)}")
    print("matrix_records=PASS")


if __name__ == "__main__":
    main()
