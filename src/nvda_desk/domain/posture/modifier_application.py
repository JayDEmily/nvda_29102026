"""Compatibility wrapper over the benchmark-owned modifier application surface."""

from __future__ import annotations

from nvda_desk.cognition.modifiers.state_conditioned import apply_posture_modifiers


def apply_modifiers(*, posture, modifier_packet=None):
    """Preserve the legacy posture modifier helper path as a thin wrapper."""

    return apply_posture_modifiers(posture=posture, modifier_packet=modifier_packet)
