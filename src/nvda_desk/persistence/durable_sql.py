from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any, Iterable


class DurableSqliteStore:
    def __init__(self, database_path: Path | str) -> None:
        self.database_path = Path(database_path)

    def initialise_schema(self) -> None:
        with self._connect() as connection:
            connection.executescript("""
                CREATE TABLE IF NOT EXISTS intraday_bars (
                    bar_id TEXT PRIMARY KEY,
                    symbol TEXT NOT NULL,
                    open_price REAL NOT NULL,
                    high_price REAL NOT NULL,
                    low_price REAL NOT NULL,
                    close_price REAL NOT NULL,
                    volume INTEGER NOT NULL
                );
                CREATE TABLE IF NOT EXISTS option_snapshots (
                    snapshot_id TEXT PRIMARY KEY,
                    underlying_symbol TEXT NOT NULL,
                    strike REAL NOT NULL,
                    option_type TEXT NOT NULL,
                    mid_price REAL NOT NULL
                );
                CREATE TABLE IF NOT EXISTS session_calendars (
                    session_id TEXT PRIMARY KEY,
                    trade_date TEXT NOT NULL,
                    session_state TEXT NOT NULL
                );
                """)

    def seed_dev_data(
        self, *, symbol: str = "NVDA", session_ids: Iterable[str] = ("2026-05-15",)
    ) -> None:
        self.initialise_schema()
        with self._connect() as connection:
            for index, session_id in enumerate(session_ids):
                open_price = 100.0 + index
                close_price = open_price + drift_for(index)
                connection.execute(
                    "INSERT OR REPLACE INTO intraday_bars VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (
                        f"bar-{session_id}",
                        symbol,
                        open_price,
                        open_price + high_pad_for(index),
                        open_price - low_pad_for(index),
                        close_price,
                        volume_for(index),
                    ),
                )
                connection.execute(
                    "INSERT OR REPLACE INTO option_snapshots VALUES (?, ?, ?, ?, ?)",
                    (f"opt-{session_id}", symbol, 100.0 + index, "call", 1.0 + index / 10),
                )
                connection.execute(
                    "INSERT OR REPLACE INTO session_calendars VALUES (?, ?, ?)",
                    (session_id, session_id, "regular"),
                )

    def list_intraday_bars(self) -> list[dict[str, Any]]:
        return self._select_all("intraday_bars")

    def list_option_snapshots(self) -> list[dict[str, Any]]:
        return self._select_all("option_snapshots")

    def list_session_calendars(self) -> list[dict[str, Any]]:
        return self._select_all("session_calendars")

    def _select_all(self, table_name: str) -> list[dict[str, Any]]:
        with self._connect() as connection:
            cursor = connection.execute(f"SELECT * FROM {table_name} ORDER BY 1")
            return [dict(row) for row in cursor.fetchall()]

    def _connect(self) -> sqlite3.Connection:
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection


def drift_for(index: int) -> float:
    return round(0.25 + index * 0.05, 2)


def high_pad_for(index: int) -> float:
    return round(0.70 + index * 0.05, 2)


def low_pad_for(index: int) -> float:
    return round(0.40 + index * 0.05, 2)


def volume_for(index: int) -> int:
    return 1000 + index * 100
