"""Hash-bound runtime representation of the accepted D001-D209 catalogue."""

from __future__ import annotations

import csv
import hashlib
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

CATALOGUE_SHA256 = "8045c8c0c4a62fbc3b88759a65b415efb1f0d549764ddbdcae2c5c911cd8a64a"
ADMITTED_KERNEL_IDS = frozenset(
    {
        "K01_TIME",
        "K02_ALGEBRA",
        "K03_CHANGE_RETURN",
        "K04_STANDARDISE_RANK",
        "K05_REALIZED_RISK",
        "K06_REGRESSION_DEPENDENCE",
        "K07_WEIGHTED_SCORE",
        "K08_RULE_BUCKET_POLICY",
        "K09_SURFACE_DENSITY",
        "K10_DISTRIBUTION_SCENARIO",
        "K11_EXPOSURE_STRESS",
        "K12_VALUE_UTILITY",
        "K13_EXPECTATION_RISK_UTILITY",
        "K14_PNL_ATTRIBUTION",
        "K15_EVALUATION",
        "K16_STRUCTURED_ASSEMBLY",
        "K17_ORDER_FLOW_IMBALANCE",
    }
)


@dataclass(frozen=True, slots=True)
class CatalogueRow:
    derived_id: str
    workbook_row: str
    family: str
    derived_signal: str
    symbolic_label: str
    raw_dependencies: tuple[str, ...]
    derived_dependencies: tuple[str, ...]
    kernel_id: str
    parameter_profiles: tuple[str, ...]
    authority_class: str
    typed_contexts: tuple[str, ...]
    parameter_window: str
    units: str
    update_cadence: str
    applicable_universe: str
    calculation_concept: str
    brief_rule_ref: str
    binding_note: str


def _split(value: str) -> tuple[str, ...]:
    return tuple(item.strip() for item in value.split(";") if item.strip())


@lru_cache(maxsize=1)
def catalogue_rows() -> tuple[CatalogueRow, ...]:
    path = Path(__file__).with_name("NVDA_DERIVED_SIGNAL_CATALOGUE.csv")
    payload = path.read_bytes()
    actual = hashlib.sha256(payload).hexdigest()
    if actual != CATALOGUE_SHA256:
        raise RuntimeError(f"runtime D catalogue digest mismatch: {actual}")
    with path.open(newline="", encoding="utf-8-sig") as handle:
        raw_rows = tuple(csv.DictReader(handle))
    rows = tuple(
        CatalogueRow(
            derived_id=row["derived_id"],
            workbook_row=row["workbook_row"],
            family=row["family"],
            derived_signal=row["derived_signal"],
            symbolic_label=row["symbolic_label"],
            raw_dependencies=_split(row["raw_dependencies"]),
            derived_dependencies=_split(row["derived_dependencies"]),
            kernel_id=row["kernel_id"],
            parameter_profiles=_split(row["parameter_profiles"]),
            authority_class=row["authority_class"],
            typed_contexts=_split(row["typed_contexts"]),
            parameter_window=row["parameter_window"],
            units=row["units"],
            update_cadence=row["update_cadence"],
            applicable_universe=row["applicable_universe"],
            calculation_concept=row["calculation_concept"],
            brief_rule_ref=row["brief_rule_ref"],
            binding_note=row["binding_note"],
        )
        for row in raw_rows
    )
    expected_ids = tuple(f"D{i:03d}" for i in range(1, 210))
    if tuple(row.derived_id for row in rows) != expected_ids:
        raise RuntimeError("runtime D catalogue is not the exact ordered D001-D209 identity set")
    if any(row.kernel_id not in ADMITTED_KERNEL_IDS for row in rows):
        raise RuntimeError("runtime D catalogue contains an unadmitted kernel identity")
    ids = set(expected_ids)
    if any(dep not in ids for row in rows for dep in row.derived_dependencies):
        raise RuntimeError("runtime D catalogue contains an unresolved derived dependency")
    for row in rows:
        for dep in row.raw_dependencies:
            if (
                len(dep) != 4
                or dep[0] != "R"
                or not dep[1:].isdigit()
                or not 1 <= int(dep[1:]) <= 323
            ):
                raise RuntimeError(f"runtime D catalogue contains invalid raw dependency {dep!r}")
    # Exercise the graph while loading so a cycle is a hard startup failure.
    _topological(rows)
    return rows


@lru_cache(maxsize=209)
def catalogue_row(derived_id: str) -> CatalogueRow:
    for row in catalogue_rows():
        if row.derived_id == derived_id:
            return row
    raise KeyError(derived_id)


def _topological(rows: tuple[CatalogueRow, ...]) -> tuple[str, ...]:
    by_id = {row.derived_id: row for row in rows}
    state: dict[str, int] = {}
    output: list[str] = []

    def visit(identity: str) -> None:
        marker = state.get(identity, 0)
        if marker == 1:
            raise RuntimeError(f"cycle in derived catalogue at {identity}")
        if marker == 2:
            return
        state[identity] = 1
        for dependency in by_id[identity].derived_dependencies:
            visit(dependency)
        state[identity] = 2
        output.append(identity)

    for row in rows:
        visit(row.derived_id)
    return tuple(output)


@lru_cache(maxsize=1)
def topological_derived_ids() -> tuple[str, ...]:
    return _topological(catalogue_rows())


__all__ = [
    "ADMITTED_KERNEL_IDS",
    "CATALOGUE_SHA256",
    "CatalogueRow",
    "catalogue_row",
    "catalogue_rows",
    "topological_derived_ids",
]
