"""Load the governed PRL lane profile config from runtime-safe YAML."""

from __future__ import annotations

from pathlib import Path

import yaml

from nvda_desk.contracts.parallel_risk import (
    ParallelRiskLaneProfileConfig,
    parallel_risk_lane_profile_config_from_dict,
)

DEFAULT_PARALLEL_RISK_LANE_PROFILE_PATH = Path("config/parallel_risk_lane_profile.v1.yaml")


class ParallelRiskLaneProfileService:
    """Typed access to governed PRL profile settings without workbook or coefficient mutation."""

    def __init__(
        self,
        profile_path: Path | str = DEFAULT_PARALLEL_RISK_LANE_PROFILE_PATH,
    ) -> None:
        self.profile_path = Path(profile_path)

    def load_config(self) -> ParallelRiskLaneProfileConfig:
        """Load and validate the governed PRL lane profile config."""

        payload = yaml.safe_load(self.profile_path.read_text(encoding="utf-8")) or {}
        return parallel_risk_lane_profile_config_from_dict(payload)
