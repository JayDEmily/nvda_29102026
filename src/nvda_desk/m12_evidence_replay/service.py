"""Canonical M12 K19 evidence replay classifier and review projector."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from nvda_desk.m10_execution_gateway.contracts import semantic_fingerprint

from .contracts import ReplayAssessment, ReplayEnvelope, ReplayMaterial, ReviewProjection


class EvidenceReplayService:
    """Classify exact retained replay evidence without live reads or side effects."""

    def build_material(
        self,
        *,
        owner_module: str,
        contract_version: str,
        occurrence_id: str,
        content: BaseModel,
        sequence: int,
        material_label: str,
        material_time_utc: datetime | None = None,
    ) -> ReplayMaterial:
        owner_token = str(owner_module).strip()
        if (
            len(owner_token) != 3
            or owner_token[0] != "M"
            or not owner_token[1:].isdigit()
            or not 0 <= int(owner_token[1:]) <= 15
        ):
            raise ValueError("owner_module_invalid")
        if not isinstance(content, BaseModel):
            raise TypeError("replay_material_content_must_be_pydantic")
        if material_time_utc is not None:
            from datetime import UTC

            if material_time_utc.tzinfo is None or material_time_utc.utcoffset() != UTC.utcoffset(
                material_time_utc
            ):
                raise ValueError("material_time_must_be_utc")
        contract_type = content.__class__
        contract_path = f"{contract_type.__module__}:{contract_type.__qualname__}"
        if not contract_type.__module__.startswith("nvda_desk."):
            raise ValueError("replay_material_contract_must_be_repository_owned")
        try:
            validated_content = contract_type.model_validate(content.model_dump(mode="python"))
        except Exception as exc:
            raise ValueError("replay_material_content_not_type_valid") from exc
        content_snapshot = validated_content.model_dump(mode="python")
        content_fingerprint = semantic_fingerprint(content_snapshot)
        payload = {
            "contract_version": "1.0.0",
            "owner_module": owner_token,
            "contract_path": contract_path,
            "contract_name": contract_type.__name__,
            "owner_contract_version": contract_version,
            "occurrence_id": occurrence_id,
            "content_snapshot": content_snapshot,
            "content_fingerprint": content_fingerprint,
            "sequence": sequence,
            "material_time_utc": material_time_utc,
            "material_label": material_label,
            "verified": True,
            "retrievable": True,
        }
        fingerprint = semantic_fingerprint(payload)
        return ReplayMaterial.model_validate(
            {
                **payload,
                "material_id": f"replay-material:{fingerprint[:24]}",
                "semantic_fingerprint": fingerprint,
            }
        )

    def build_envelope(
        self,
        *,
        replay_run_id: str,
        replay_class: str,
        target_id: str,
        original_output_id: str,
        original_output_occurrence_id: str,
        original_output_fingerprint: str,
        original_reasons: tuple[str, ...],
        materials: tuple[ReplayMaterial, ...],
        executable_versions: tuple[str, ...],
        missing_material: tuple[str, ...] = (),
        unverifiable_material: tuple[str, ...] = (),
        contradictions: tuple[str, ...] = (),
    ) -> ReplayEnvelope:
        material_values = tuple(
            ReplayMaterial.model_validate(item.model_dump(mode="python")) for item in materials
        )
        domain_payload = {
            "contract_version": "1.0.0",
            "replay_class": replay_class,
            "target_id": target_id,
            "original_output_id": original_output_id,
            "original_output_occurrence_id": original_output_occurrence_id,
            "original_output_fingerprint": original_output_fingerprint,
            "original_reasons": original_reasons,
            "material_fingerprints": tuple(item.semantic_fingerprint for item in material_values),
            "executable_versions": executable_versions,
            "missing_material": missing_material,
            "unverifiable_material": unverifiable_material,
            "contradictions": contradictions,
            "live_side_effects_allowed": False,
            "runtime_promotion_allowed": False,
        }
        domain_fingerprint = semantic_fingerprint(domain_payload)
        fingerprint = semantic_fingerprint(
            {"replay_run_id": replay_run_id, "semantic_domain_fingerprint": domain_fingerprint}
        )
        return ReplayEnvelope.model_validate(
            {
                "envelope_id": f"replay-envelope:{fingerprint[:24]}",
                "contract_version": "1.0.0",
                "replay_run_id": replay_run_id,
                "replay_class": replay_class,
                "target_id": target_id,
                "original_output_id": original_output_id,
                "original_output_occurrence_id": original_output_occurrence_id,
                "original_output_fingerprint": original_output_fingerprint,
                "original_reasons": original_reasons,
                "materials": material_values,
                "material_ids": tuple(item.material_id for item in material_values),
                "executable_versions": executable_versions,
                "missing_material": missing_material,
                "unverifiable_material": unverifiable_material,
                "contradictions": contradictions,
                "live_side_effects_allowed": False,
                "runtime_promotion_allowed": False,
                "semantic_domain_fingerprint": domain_fingerprint,
                "semantic_fingerprint": fingerprint,
            }
        )

    def assess(
        self,
        envelope: ReplayEnvelope,
        *,
        reproduced_output_id: str | None = None,
        reproduced_output_fingerprint: str | None = None,
        reproduced_reasons: tuple[str, ...] | None = None,
        executable_versions: tuple[str, ...] | None = None,
        isolated_execution: bool = True,
        live_side_effects: tuple[str, ...] = (),
        runtime_authority_promoted: bool = False,
    ) -> ReplayAssessment:
        try:
            envelope = ReplayEnvelope.model_validate(envelope.model_dump(mode="python"))
        except Exception as exc:
            raise ValueError("replay_envelope_contract_invalid") from exc
        if not isolated_execution:
            raise ValueError("replay_execution_must_be_isolated")
        if live_side_effects:
            raise ValueError("live_side_effects_forbidden")
        if runtime_authority_promoted:
            raise ValueError("runtime_authority_promotion_forbidden")

        if envelope.replay_class == "comparison_only" and any(
            value not in (None, (), "")
            for value in (
                reproduced_output_id,
                reproduced_output_fingerprint,
                reproduced_reasons,
                executable_versions,
            )
        ):
            raise ValueError("comparison_only_cannot_carry_reexecution_result")

        missing = list(envelope.missing_material)
        original_material = next(
            (
                item
                for item in envelope.materials
                if item.occurrence_id == envelope.original_output_occurrence_id
                and item.content_fingerprint == envelope.original_output_fingerprint
            ),
            None,
        )
        if original_material is None and "original_output_occurrence" not in missing:
            missing.append("original_output_occurrence")

        exact_matches: list[str] = []
        mismatches: list[str] = []
        reproduced_id = reproduced_output_id
        reproduced_fp = reproduced_output_fingerprint

        incomplete = bool(missing or envelope.unverifiable_material or envelope.contradictions)
        if envelope.replay_class == "comparison_only":
            status = "comparison_only"
            reproduced_id = None
            reproduced_fp = None
        elif envelope.replay_class == "preserved_occurrence_replay":
            if incomplete:
                status = "non_authoritative_incomplete"
            else:
                status = "authoritative_match"
                exact_matches = ["preserved_occurrence", "material_completeness"]
                reproduced_id = envelope.original_output_id
                reproduced_fp = envelope.original_output_fingerprint
        else:
            result_present = (
                reproduced_output_id is not None
                and reproduced_output_fingerprint is not None
                and reproduced_reasons is not None
                and executable_versions is not None
            )
            if not result_present and "isolated_reexecution_result" not in missing:
                missing.append("isolated_reexecution_result")
                incomplete = True
            if incomplete:
                status = "non_authoritative_incomplete"
                reproduced_id = reproduced_output_id
                reproduced_fp = reproduced_output_fingerprint
            else:
                if reproduced_output_fingerprint == envelope.original_output_fingerprint:
                    exact_matches.append("semantic_fingerprint")
                else:
                    mismatches.append("semantic_fingerprint")
                if reproduced_reasons == envelope.original_reasons:
                    exact_matches.append("reasons_constraints")
                else:
                    mismatches.append("reasons_constraints")
                if executable_versions == envelope.executable_versions:
                    exact_matches.append("executable_versions")
                else:
                    mismatches.append("executable_versions")
                status = "authoritative_match" if not mismatches else "semantic_mismatch"

        payload = {
            "contract_version": "1.0.0",
            "envelope_id": envelope.envelope_id,
            "envelope_fingerprint": envelope.semantic_fingerprint,
            "replay_run_id": envelope.replay_run_id,
            "replay_class": envelope.replay_class,
            "target_id": envelope.target_id,
            "authority_status": status,
            "verified_material_ids": envelope.material_ids,
            "missing_material": tuple(missing),
            "unverifiable_material": envelope.unverifiable_material,
            "contradictions": envelope.contradictions,
            "exact_matches": tuple(exact_matches),
            "mismatches": tuple(mismatches),
            "reproduced_output_id": reproduced_id,
            "reproduced_output_fingerprint": reproduced_fp,
            "live_side_effects_performed": False,
            "runtime_authority_promoted": False,
        }
        fingerprint = semantic_fingerprint(payload)
        return ReplayAssessment.model_validate(
            {
                **payload,
                "assessment_id": f"replay-assessment:{fingerprint[:24]}",
                "semantic_fingerprint": fingerprint,
            }
        )

    def project(
        self, *, envelope: ReplayEnvelope, assessment: ReplayAssessment
    ) -> ReviewProjection:
        try:
            envelope = ReplayEnvelope.model_validate(envelope.model_dump(mode="python"))
            assessment = ReplayAssessment.model_validate(assessment.model_dump(mode="python"))
        except Exception as exc:
            raise ValueError("review_projection_input_contract_invalid") from exc
        if (
            assessment.envelope_id != envelope.envelope_id
            or assessment.envelope_fingerprint != envelope.semantic_fingerprint
            or assessment.replay_run_id != envelope.replay_run_id
            or assessment.target_id != envelope.target_id
            or assessment.replay_class != envelope.replay_class
        ):
            raise ValueError("review_projection_binding_mismatch")
        explanation = (
            f"target={assessment.target_id} | replay_class={assessment.replay_class} | "
            f"authority_status={assessment.authority_status} | "
            f"verified={','.join(assessment.verified_material_ids)} | "
            f"missing={','.join(assessment.missing_material)} | "
            f"mismatches={','.join(assessment.mismatches)}"
        )
        payload = {
            "contract_version": "1.0.0",
            "envelope_id": envelope.envelope_id,
            "envelope_fingerprint": envelope.semantic_fingerprint,
            "assessment_id": assessment.assessment_id,
            "assessment_fingerprint": assessment.semantic_fingerprint,
            "target_id": assessment.target_id,
            "replay_class": assessment.replay_class,
            "authority_status": assessment.authority_status,
            "verified_material_ids": assessment.verified_material_ids,
            "missing_material": assessment.missing_material,
            "unverifiable_material": assessment.unverifiable_material,
            "contradictions": assessment.contradictions,
            "exact_matches": assessment.exact_matches,
            "mismatches": assessment.mismatches,
            "explanation": explanation,
            "live_side_effects_performed": False,
            "runtime_authority_promoted": False,
        }
        fingerprint = semantic_fingerprint(payload)
        return ReviewProjection.model_validate(
            {
                **payload,
                "projection_id": f"review-projection:{fingerprint[:24]}",
                "semantic_fingerprint": fingerprint,
            }
        )
