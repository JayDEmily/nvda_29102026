from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker


def create_engine_from_url(database_url: str) -> Engine:
    connect_args: dict[str, object] = {}
    if database_url.startswith("sqlite"):
        connect_args["check_same_thread"] = False
    return create_engine(database_url, future=True, connect_args=connect_args)


def create_session_factory(database_url: str) -> sessionmaker[Session]:
    engine = create_engine_from_url(database_url)
    return sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
