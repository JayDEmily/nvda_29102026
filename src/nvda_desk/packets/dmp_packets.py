"""Build canonical DMPV3 packet shells for bounded native repo surfaces."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Callable

from nvda_desk.contracts.capital import CAPITAL_DEPLOYMENT_DECISION_DATASCHEMA
from nvda_desk.contracts.packets import DeskModulePacketV3, build_dmp_v3_envelope_kwargs
from nvda_desk.contracts.prepared_context import PREPARED_CONTEXT_DATASCHEMA


class DmpPacketBuilder:
    """Build the bounded packet families required by the native repo shell."""

    @staticmethod
    def build_dmp_v3_packet(
        *,
        packet_id: str,
        dataschema: str,
        data: Any,
        packetrole: str,
        module_id: str,
        grammar_role: str,
        behaviour_class: str,
        module_version: str = "native",
        module_instance_id: str | None = None,
        stage_name: str | None = None,
        emitted_at: datetime | None = None,
        source: str | None = None,
        packet_type: str | None = None,
        datacontenttype: str = "application/json",
        traceid: str | None = None,
        runid: str | None = None,
        scenarioid: str | None = None,
        parentids: list[str] | None = None,
        dependencyids: list[str] | None = None,
        derivedfrom: str | None = None,
        replayref: str | None = None,
        sourceartifactids: list[str] | None = None,
        inputfingerprint: str | None = None,
        source_artifact_validator: Callable[[str], bool] | None = None,
        input_material: bytes | None = None,
        reviewtraceid: str | None = None,
        replaytraceid: str | None = None,
        decisiontraceid: str | None = None,
        validation_violations: list[str] | None = None,
        summary_headline: str | None = None,
        summary_keyflags: list[str] | None = None,
        summary_humanstate: str | None = None,
        dmpextensions: dict[str, Any] | None = None,
    ) -> DeskModulePacketV3:
        """Build one canonical DMPV3 packet from explicit carriage metadata."""

        return DeskModulePacketV3(
            **build_dmp_v3_envelope_kwargs(
                packet_id=packet_id,
                dataschema=dataschema,
                data=data,
                packetrole=packetrole,
                module_id=module_id,
                module_version=module_version,
                module_instance_id=module_instance_id,
                grammar_role=grammar_role,
                behaviour_class=behaviour_class,
                stage_name=stage_name,
                emitted_at=emitted_at,
                source=source,
                packet_type=packet_type,
                datacontenttype=datacontenttype,
                traceid=traceid,
                runid=runid,
                scenarioid=scenarioid,
                parentids=parentids,
                dependencyids=dependencyids,
                derivedfrom=derivedfrom,
                replayref=replayref,
                sourceartifactids=sourceartifactids,
                inputfingerprint=inputfingerprint,
                source_artifact_validator=source_artifact_validator,
                input_material=input_material,
                reviewtraceid=reviewtraceid,
                replaytraceid=replaytraceid,
                decisiontraceid=decisiontraceid,
                validation_violations=validation_violations,
                summary_headline=summary_headline,
                summary_keyflags=summary_keyflags,
                summary_humanstate=summary_humanstate,
                dmpextensions=dmpextensions,
            )
        )

    @classmethod
    def build_reference_packet(
        cls,
        *,
        packet_id: str,
        dataschema: str,
        data: Any,
        emitted_at: datetime | None = None,
        traceid: str | None = None,
        runid: str | None = None,
        scenarioid: str | None = None,
        module_id: str = "reference_data",
        module_version: str = "native",
        module_instance_id: str | None = None,
        sourceartifactids: list[str] | None = None,
        summary_headline: str | None = None,
        summary_keyflags: list[str] | None = None,
        dmpextensions: dict[str, Any] | None = None,
    ) -> DeskModulePacketV3:
        """Build a canonical reference-data packet envelope."""

        return cls.build_dmp_v3_packet(
            packet_id=packet_id,
            dataschema=dataschema,
            data=data,
            packetrole="reference_packet",
            module_id=module_id,
            module_version=module_version,
            module_instance_id=module_instance_id,
            grammar_role="reference_data",
            behaviour_class="module_output",
            emitted_at=emitted_at,
            traceid=traceid,
            runid=runid,
            scenarioid=scenarioid,
            sourceartifactids=sourceartifactids,
            summary_headline=summary_headline,
            summary_keyflags=summary_keyflags,
            dmpextensions=dmpextensions,
        )

    @classmethod
    def build_stage_packet(
        cls,
        *,
        packet_id: str,
        dataschema: str,
        data: Any,
        emitted_at: datetime | None = None,
        traceid: str | None = None,
        runid: str | None = None,
        scenarioid: str | None = None,
        module_id: str = "serial_runtime",
        module_version: str = "native",
        module_instance_id: str | None = None,
        grammar_role: str = "serial_runtime",
        stage_name: str | None = None,
        parentids: list[str] | None = None,
        dependencyids: list[str] | None = None,
        derivedfrom: str | None = None,
        sourceartifactids: list[str] | None = None,
        inputfingerprint: str | None = None,
        summary_headline: str | None = None,
        summary_keyflags: list[str] | None = None,
        dmpextensions: dict[str, Any] | None = None,
    ) -> DeskModulePacketV3:
        """Build a canonical serial-stage packet envelope."""

        return cls.build_dmp_v3_packet(
            packet_id=packet_id,
            dataschema=dataschema,
            data=data,
            packetrole="stage_packet",
            module_id=module_id,
            module_version=module_version,
            module_instance_id=module_instance_id,
            grammar_role=grammar_role,
            behaviour_class="stage_output",
            stage_name=stage_name,
            emitted_at=emitted_at,
            traceid=traceid,
            runid=runid,
            scenarioid=scenarioid,
            parentids=parentids,
            dependencyids=dependencyids,
            derivedfrom=derivedfrom,
            sourceartifactids=sourceartifactids,
            inputfingerprint=inputfingerprint,
            summary_headline=summary_headline,
            summary_keyflags=summary_keyflags,
            dmpextensions=dmpextensions,
        )

    @classmethod
    def build_parallel_risk_packet(
        cls,
        *,
        packet_id: str,
        dataschema: str,
        data: Any,
        emitted_at: datetime | None = None,
        traceid: str | None = None,
        runid: str | None = None,
        scenarioid: str | None = None,
        module_id: str = "parallel_risk_lane",
        module_version: str = "native",
        module_instance_id: str | None = None,
        parentids: list[str] | None = None,
        dependencyids: list[str] | None = None,
        derivedfrom: str | None = None,
        sourceartifactids: list[str] | None = None,
        inputfingerprint: str | None = None,
        summary_headline: str | None = None,
        summary_keyflags: list[str] | None = None,
        dmpextensions: dict[str, Any] | None = None,
    ) -> DeskModulePacketV3:
        """Build a canonical parallel-risk packet envelope."""

        return cls.build_dmp_v3_packet(
            packet_id=packet_id,
            dataschema=dataschema,
            data=data,
            packetrole="parallel_risk_packet",
            module_id=module_id,
            module_version=module_version,
            module_instance_id=module_instance_id,
            grammar_role="parallel_risk_lane",
            behaviour_class="module_output",
            emitted_at=emitted_at,
            traceid=traceid,
            runid=runid,
            scenarioid=scenarioid,
            parentids=parentids,
            dependencyids=dependencyids,
            derivedfrom=derivedfrom,
            sourceartifactids=sourceartifactids,
            inputfingerprint=inputfingerprint,
            summary_headline=summary_headline,
            summary_keyflags=summary_keyflags,
            dmpextensions=dmpextensions,
        )

    @classmethod
    def build_prepared_context_packet(
        cls,
        *,
        packet_id: str,
        data: Any,
        emitted_at: datetime | None = None,
        traceid: str | None = None,
        runid: str | None = None,
        scenarioid: str | None = None,
        parentids: list[str] | None = None,
        dependencyids: list[str] | None = None,
        sourceartifactids: list[str] | None = None,
        inputfingerprint: str | None = None,
        reviewtraceid: str | None = None,
        validation_violations: list[str] | None = None,
        summary_keyflags: list[str] | None = None,
        dmpextensions: dict[str, Any] | None = None,
    ) -> DeskModulePacketV3:
        """Build a canonical prepared-runtime-context handoff packet."""

        return cls.build_dmp_v3_packet(
            packet_id=packet_id,
            dataschema=PREPARED_CONTEXT_DATASCHEMA,
            data=data,
            packetrole="prepared_context_packet",
            module_id="prepared_ingress",
            module_version="native",
            grammar_role="prepared_runtime_context",
            behaviour_class="preparation_output",
            stage_name="runtime_context_preparation",
            emitted_at=emitted_at,
            traceid=traceid,
            runid=runid,
            scenarioid=scenarioid,
            parentids=parentids,
            dependencyids=dependencyids,
            sourceartifactids=sourceartifactids,
            inputfingerprint=inputfingerprint,
            reviewtraceid=reviewtraceid,
            validation_violations=validation_violations,
            summary_headline="prepared ingress emitted prepared context",
            summary_keyflags=summary_keyflags or ["prepared_context"],
            dmpextensions=dmpextensions,
        )

    @classmethod
    def build_review_explanation_packet(
        cls,
        *,
        packet_id: str,
        data: Any,
        emitted_at: datetime | None = None,
        traceid: str | None = None,
        runid: str | None = None,
        scenarioid: str | None = None,
        parentids: list[str] | None = None,
        dependencyids: list[str] | None = None,
        sourceartifactids: list[str] | None = None,
        inputfingerprint: str | None = None,
        reviewtraceid: str | None = None,
        summary_keyflags: list[str] | None = None,
        dmpextensions: dict[str, Any] | None = None,
    ) -> DeskModulePacketV3:
        """Build a canonical review/explanation packet without decision authority."""

        return cls.build_dmp_v3_packet(
            packet_id=packet_id,
            dataschema="nvda.review.ReviewExplanation.v1",
            data=data,
            packetrole="review_explanation_packet",
            module_id="review_explanation",
            module_version="native",
            grammar_role="review_explanation",
            behaviour_class="review_only_output",
            stage_name="review_explanation",
            emitted_at=emitted_at,
            traceid=traceid,
            runid=runid,
            scenarioid=scenarioid,
            parentids=parentids,
            dependencyids=dependencyids,
            sourceartifactids=sourceartifactids,
            inputfingerprint=inputfingerprint,
            reviewtraceid=reviewtraceid,
            summary_headline="review explanation emitted",
            summary_keyflags=summary_keyflags or ["review_explanation"],
            summary_humanstate="review_only",
            dmpextensions=dmpextensions,
        )

    @classmethod
    def build_capital_deployment_packet(
        cls,
        *,
        packet_id: str,
        data: Any,
        emitted_at: datetime | None = None,
        traceid: str | None = None,
        runid: str | None = None,
        scenarioid: str | None = None,
        parentids: list[str] | None = None,
        dependencyids: list[str] | None = None,
        derivedfrom: str | None = None,
        sourceartifactids: list[str] | None = None,
        inputfingerprint: str | None = None,
        summary_headline: str | None = None,
        summary_keyflags: list[str] | None = None,
        dmpextensions: dict[str, Any] | None = None,
    ) -> DeskModulePacketV3:
        """Build a canonical capital-deployment authority decision packet."""

        return cls.build_dmp_v3_packet(
            packet_id=packet_id,
            dataschema=CAPITAL_DEPLOYMENT_DECISION_DATASCHEMA,
            data=data,
            packetrole="capital_deployment_decision",
            module_id="capital_deployment_authority",
            module_version="native",
            grammar_role="downstream_capital_authority",
            behaviour_class="downstream_authority_output",
            stage_name="capital_deployment_authority",
            emitted_at=emitted_at,
            traceid=traceid,
            runid=runid,
            scenarioid=scenarioid,
            parentids=parentids,
            dependencyids=dependencyids,
            derivedfrom=derivedfrom,
            sourceartifactids=sourceartifactids,
            inputfingerprint=inputfingerprint,
            summary_headline=summary_headline or "capital deployment decision emitted",
            summary_keyflags=summary_keyflags or ["downstream_capital_authority"],
            summary_humanstate="capital_decision_carried",
            dmpextensions=dmpextensions,
        )


def build_dmp_v3_packet(**kwargs: Any) -> DeskModulePacketV3:
    """Proxy helper for generic canonical DMPV3 packet construction."""

    return DmpPacketBuilder.build_dmp_v3_packet(**kwargs)


def build_reference_packet(**kwargs: Any) -> DeskModulePacketV3:
    """Proxy helper for reference-data packet construction."""

    return DmpPacketBuilder.build_reference_packet(**kwargs)


def build_stage_packet(**kwargs: Any) -> DeskModulePacketV3:
    """Proxy helper for serial-stage packet construction."""

    return DmpPacketBuilder.build_stage_packet(**kwargs)


def build_parallel_risk_packet(**kwargs: Any) -> DeskModulePacketV3:
    """Proxy helper for parallel-risk packet construction."""

    return DmpPacketBuilder.build_parallel_risk_packet(**kwargs)


def build_prepared_context_packet(**kwargs: Any) -> DeskModulePacketV3:
    """Proxy helper for prepared-context packet construction."""

    return DmpPacketBuilder.build_prepared_context_packet(**kwargs)


def build_review_explanation_packet(**kwargs: Any) -> DeskModulePacketV3:
    """Proxy helper for review/explanation packet construction."""

    return DmpPacketBuilder.build_review_explanation_packet(**kwargs)


def build_capital_deployment_packet(**kwargs: Any) -> DeskModulePacketV3:
    """Proxy helper for capital-deployment authority packet construction."""

    return DmpPacketBuilder.build_capital_deployment_packet(**kwargs)
