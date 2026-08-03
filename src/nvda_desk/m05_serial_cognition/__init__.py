"""Public M05 K08/K09 serial-cognition authority API."""

from .composition import (
    SerialCognitionOutcome,
    SerialCognitionRequest,
    SerialCognitionService,
)
from .contracts import SerialCandidate, StageContext, StageInput, StageOutput
from .packet_boundary import SerialCandidatePacketAdapter
from .runner import SerialRunner
from .temporal_adapter import TemporalStageAdapter

__all__ = [
    "SerialCandidate",
    "SerialCognitionOutcome",
    "SerialCognitionRequest",
    "SerialCognitionService",
    "SerialCandidatePacketAdapter",
    "SerialRunner",
    "StageContext",
    "StageInput",
    "StageOutput",
    "TemporalStageAdapter",
]
