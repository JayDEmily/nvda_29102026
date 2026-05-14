from __future__ import annotations

import importlib.util

from nvda_desk.contracts import packets as canonical_packets
from nvda_desk.packets import dmp_packets as canonical_packet_builders
from nvda_desk.schemas import dmp as dmp_compat
from nvda_desk.schemas import dmp_envelope as envelope_compat


def test_dmpv3_compatibility_wrappers_are_aliases_not_parallel_grammars() -> None:
    assert dmp_compat.DeskModulePacketV3 is canonical_packets.DeskModulePacketV3
    assert dmp_compat.DmpV3Packet is canonical_packets.DmpV3Packet
    assert dmp_compat.build_dmp_v3_packet is canonical_packet_builders.build_dmp_v3_packet

    assert envelope_compat.DmpV3Envelope is canonical_packets.DmpV3Envelope
    assert envelope_compat.DmpV3Lineage is canonical_packets.DmpV3Lineage
    assert envelope_compat.DmpV3Producer is canonical_packets.DmpV3Producer
    assert envelope_compat.DmpV3Summary is canonical_packets.DmpV3Summary
    assert envelope_compat.DmpV3Validation is canonical_packets.DmpV3Validation
    assert envelope_compat.DmpV3ValidationCheck is canonical_packets.DmpV3ValidationCheck
    assert (
        envelope_compat.build_dmp_v3_envelope_kwargs
        is canonical_packets.build_dmp_v3_envelope_kwargs
    )


def test_transform_required_donor_packet_service_modules_are_not_native_authority() -> None:
    forbidden_modules = [
        "nvda_desk.services.review_packets",
        "nvda_desk.services.carry_handoff",
        "nvda_desk.services.imported_market_substrate",
        "nvda_desk.services.imported_execution_planning",
        "nvda_desk.services.imported_posture_enrichers",
    ]

    for module_name in forbidden_modules:
        assert importlib.util.find_spec(module_name) is None


def test_transform_required_donor_local_envelopes_are_not_native_parallel_packet_classes() -> None:
    forbidden_attrs = [
        "ParallelRiskLanePacket",
        "PostureLocalEnvelopeSurface",
        "ClockEnvelope",
    ]

    for attr in forbidden_attrs:
        assert not hasattr(canonical_packets, attr)
        assert not hasattr(canonical_packet_builders, attr)
        assert not hasattr(dmp_compat, attr)
        assert not hasattr(envelope_compat, attr)
