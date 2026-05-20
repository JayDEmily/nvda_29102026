"""Native contracts for admitted Atlas migration rows."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AtlasMigrationRow:
    """A native contract entry for one lawfully migrated Atlas/Bridge row."""

    surface_id: str
    atlas_record_id: str
    bridge_record_id: str
    atlas_idea_excerpt: str
    bridge_target_excerpt: str
    required_native_behaviour: str
    final_status: str
    semantic_equivalence_rationale: str


def ensure_no_open_rows(rows: tuple[AtlasMigrationRow, ...]) -> None:
    """Raise if a native migration contract still carries an unsupported row."""

    unsupported = [row.atlas_record_id for row in rows if row.final_status == "unsupported_worker_claim"]
    if unsupported:
        raise ValueError("unsupported Atlas migration rows remain: " + ", ".join(unsupported))
