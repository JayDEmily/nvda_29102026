from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping


class _AppendOnlySidecar:
    def __init__(self) -> None:
        self._rows: list[dict[str, Any]] = []
        self._ids: set[str] = set()

    def _append(self, row_id: str, row: Mapping[str, Any]) -> dict[str, Any]:
        row_key = str(row_id).strip()
        if not row_key:
            raise ValueError("row_id must be non-empty")
        if row_key in self._ids:
            raise ValueError(f"duplicate row_id: {row_key}")
        payload = deepcopy(dict(row))
        self._ids.add(row_key)
        self._rows.append(payload)
        return deepcopy(payload)

    def _list(self) -> list[dict[str, Any]]:
        return deepcopy(self._rows)


class ResearchNoteService(_AppendOnlySidecar):
    def create_research_note(self, note_id: str, *, title: str, body: str) -> dict[str, Any]:
        return self._append(
            note_id,
            {"note_id": note_id.strip(), "title": title.strip(), "body": body},
        )

    def list_research_notes(self) -> list[dict[str, Any]]:
        return self._list()


class PromotionDecisionService(_AppendOnlySidecar):
    def create_promotion_decision(
        self, decision_id: str, *, candidate_id: str, decision: str, rationale: str
    ) -> dict[str, Any]:
        return self._append(
            decision_id,
            {
                "decision_id": decision_id.strip(),
                "candidate_id": candidate_id.strip(),
                "decision": decision.strip(),
                "rationale": rationale,
            },
        )

    def list_promotion_decisions(self) -> list[dict[str, Any]]:
        return self._list()


class EvaluationRunService:
    def __init__(self) -> None:
        self._evaluation_runs = _AppendOnlySidecar()
        self._experiment_runs = _AppendOnlySidecar()

    def record_evaluation_run(
        self, run_id: str, *, kind: str, payload: Mapping[str, Any]
    ) -> dict[str, Any]:
        return self._evaluation_runs._append(
            run_id,
            {"run_id": run_id.strip(), "kind": kind.strip(), "payload": deepcopy(dict(payload))},
        )

    def list_evaluation_runs(self) -> list[dict[str, Any]]:
        return self._evaluation_runs._list()

    def record_experiment_run(
        self, run_id: str, *, kind: str, payload: Mapping[str, Any]
    ) -> dict[str, Any]:
        return self._experiment_runs._append(
            run_id,
            {"run_id": run_id.strip(), "kind": kind.strip(), "payload": deepcopy(dict(payload))},
        )

    def list_experiment_runs(self) -> list[dict[str, Any]]:
        return self._experiment_runs._list()
