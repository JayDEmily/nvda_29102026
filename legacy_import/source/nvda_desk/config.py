from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="NVDA_DESK_", extra="ignore")

    database_url: str = Field(default="sqlite+pysqlite:///./var/nvda_desk_dev.db")
    market_timezone: str = Field(default="America/New_York")
    pre_market_start_hour: int = Field(default=4, ge=0, le=23)
    regular_open_hour: int = Field(default=9, ge=0, le=23)
    regular_open_minute: int = Field(default=30, ge=0, le=59)
    regular_close_hour: int = Field(default=16, ge=0, le=23)
    regular_close_minute: int = Field(default=0, ge=0, le=59)
    after_hours_end_hour: int = Field(default=20, ge=0, le=23)
    playbook_registry_path: str = Field(default="config/playbook_registry.example.yaml")
    coefficient_authority_path: str = Field(default="config/coefficient_authority.v1.yaml")
    options_flow_history_lane_enabled: bool = Field(default=False)


def get_settings() -> Settings:
    return Settings()
