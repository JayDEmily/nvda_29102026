from __future__ import annotations

import json
from pathlib import Path


def test_required_dmp_v3_protocol_terms_are_present() -> None:
    vocab = json.loads(
        Path("data/vocabulary/canonical_vocabulary.json").read_text(encoding="utf-8")
    )
    entries = {entry["canonical_slug"]: entry for entry in vocab["entries"]}

    expected = {
        "dmp_v3": "DmpV3Envelope",
        "dmp_v3_envelope": "DmpV3Envelope",
        "dmp_v3_packet": "DmpV3Packet",
        "desk_module_packet_v3": "DeskModulePacketV3",
        "packetrole": "DmpV3Envelope.packetrole",
        "producer": "DmpV3Envelope.producer",
        "lineage": "DmpV3Envelope.lineage",
        "validation": "DmpV3Envelope.validation",
        "summary": "DmpV3Envelope.summary",
        "dmpextensions": "DmpV3Envelope.dmpextensions",
        "module_id": "DmpV3Producer.module_id",
        "module_version": "DmpV3Producer.module_version",
        "module_instance_id": "DmpV3Producer.module_instance_id",
        "grammar_role": "DmpV3Producer.grammar_role",
        "behaviour_class": "DmpV3Producer.behaviour_class",
        "traceid": "DmpV3Envelope.traceid",
        "runid": "DmpV3Envelope.runid",
        "scenarioid": "DmpV3Envelope.scenarioid",
    }

    for slug, contract in expected.items():
        assert slug in entries
        assert entries[slug]["maps_to_contract"] == contract
