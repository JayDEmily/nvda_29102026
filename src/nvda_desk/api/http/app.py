"""Compatibility wrapper over the benchmark-owned API app shell."""

from __future__ import annotations

from nvda_desk.api.app import HttpApp, create_app, register_routes

__all__ = ["HttpApp", "create_app", "register_routes"]
