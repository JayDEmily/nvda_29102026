"""Leaf-2 accepted-brief §§8, 11, 13, 14 temporal and graph proof."""
from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from typing import Any, cast

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.derived_signal_calculation_truth import _stage1
from nvda_desk.raw_signal_occurrence_truth import api as raw_api

NOW = datetime(2026, 10, 8, 6, 0, tzinfo=UTC)


def _point(raw_id: str, label: str, value: Decimal, *, seconds: int = 0,
           received_seconds: int | None = None, kind: str = "true_instant") -> raw_api.ProjectedRawValueV1:
    moment = NOW + timedelta(seconds=seconds)
    receipt = NOW + timedelta(seconds=seconds if received_seconds is None else received_seconds)
    return raw_api.ProjectedRawValueV1(
        raw_signal_catalogue_id=raw_api.RawSignalCatalogueId(raw_id),
        observation_occurrence_id=raw_api.observation_occurrence_id(label),
        projection_mapping_id=f"map-{raw_id}", projection_mapping_version=1,
        source_provider="proof", source_variant="snapshot", native_field_path=(raw_id,),
        native_value=value, native_units="USD", subject_instrument="NVDA",
        source_temporal_kind=kind,
        source_timestamp_raw=moment.isoformat() if kind == "true_instant" else None,
        source_timezone_native="UTC" if kind == "true_instant" else None,
        received_ts_utc=receipt, ingestion_sequence=1,
        ingestion_sequence_scope=raw_api.ingestion_sequence_scope("proof:snapshot"),
        revision_vintage_native=None,
    )


def _setup(*, values: dict[str, tuple[raw_api.ProjectedRawValueV1, ...]],
           skew_seconds: int = 10, stale_seconds: int = 60,
           allowed: tuple[str, ...] = ("true_instant",),
           context: tuple[api.VersionRefV1, ...] = (),
           persistence: Any = None) -> tuple[Any, api.CalculationRequestV1]:
    class Reader:
        def list_projected_raw_history(self, raw_signal_catalogue_id: Any, **kwargs: Any) -> Any:
            return raw_api.ProjectedRawHistoryPageV1(
                items=values.get(raw_signal_catalogue_id.value, ()), next_cursor=None
            )

        def project_raw_value(self, *args: object, **kwargs: object) -> object | None:
            return None

    all_ids = ("R034", "R035")
    parameter = api.CalculationParameterSetV1(
        context_id="basic", version=1, profile="P_BASIC", parameters=(("selection_mode", "exact"),)
    )
    selection = api.InputSelectionPolicyVersionV1(
        context_id="selector", version=1, join_keys=("subject_instrument",),
        maximum_staleness=timedelta(seconds=stale_seconds),
        maximum_skew=timedelta(seconds=skew_seconds),
        temporal_basis_permissions=allowed, basket_membership=(),
    )
    unit = api.UnitConventionVersionV1(
        context_id="units", version=1, native_units="USD", canonical_units="USD",
        scale=Decimal(1), offset=Decimal(0),
    )
    mappings = tuple(
        raw_api.RawSignalProjectionMappingV1(
            mapping_id=f"map-{rid}", version=1,
            raw_signal_catalogue_id=raw_api.RawSignalCatalogueId(rid),
            source_provider="proof", source_variant="snapshot",
            native_field_path=(rid,), native_units="USD",
        ) for rid in all_ids
    )
    bindings = tuple(api.RawInputBindingV1(
        rid, api.VersionRefV1(f"map-{rid}", 1), api.VersionRefV1("units", 1), "NVDA"
    ) for rid in all_ids)
    owner = api.create_owner(
        raw_projection_reader=Reader(), persistence=persistence, raw_projection_mappings=mappings,
        parameter_sets=(parameter,), input_selection_policies=(selection,),
        unit_conventions=(unit,), contexts=(), utc_now=lambda: NOW,
    )
    request = api.CalculationRequestV1(
        derived_signal_id="D013", subject_instrument="NVDA", as_of_utc=NOW,
        knowledge_cutoff_utc=NOW, calculation_definition_version="calc-v1",
        parameter_set_id="basic", parameter_set_version=1,
        input_selection_policy_id="selector", input_selection_policy_version=1,
        context_refs=context, raw_input_bindings=bindings,
        parameter_profile_refs=(api.ParameterProfileRefV1("P_BASIC", "basic", 1),),
    )
    return owner, request


def _raw(*, bid_seconds: int = 0, ask_seconds: int = 0,
         bid_receipt: int | None = None, ask_receipt: int | None = None,
         bid_kind: str = "true_instant") -> dict[str, tuple[raw_api.ProjectedRawValueV1, ...]]:
    return {
        "R034": (_point("R034", "bid", Decimal(100), seconds=bid_seconds,
                        received_seconds=bid_receipt, kind=bid_kind),),
        "R035": (_point("R035", "ask", Decimal(102), seconds=ask_seconds,
                        received_seconds=ask_receipt),),
    }


def test_leaf2_public_cutoff_as_of_freshness_and_skew_refuse() -> None:
    valid, request = _setup(values=_raw())
    assert valid.materialise(request) is not None
    for values in (
        _raw(ask_receipt=1),         # unseen until after knowledge cutoff
        _raw(bid_seconds=1),         # known ahead-of-as-of event cannot be consumed
        _raw(bid_seconds=-61),       # latest bid outside freshness
        _raw(bid_seconds=-30),       # individually fresh but outside synchronous skew
        _raw(bid_kind="receipt_only"),  # temporal basis not permitted
    ):
        owner, checked = _setup(values=values)
        assert owner.materialise(checked) is None


def test_leaf2_graph_retry_is_stable_and_changed_cutoff_appends() -> None:
    owner, request = _setup(values=_raw())
    first = owner.materialise(request)
    assert first is not None
    assert owner.materialise(request) == first
    history = owner.reads.list_derived_history(
        derived_signal_id="D013", subject_instrument="NVDA", limit=10
    )
    assert len(history) == 1
    successor = owner.materialise(replace(request, knowledge_cutoff_utc=NOW + timedelta(seconds=1)))
    assert successor is not None and successor.derived_occurrence_id != first.derived_occurrence_id
    assert successor.supersedes_derived_occurrence_id == first.derived_occurrence_id
    assert owner.reads.get_derived_occurrence(first.derived_occurrence_id) == first
    assert len(owner.reads.list_derived_history(
        derived_signal_id="D013", subject_instrument="NVDA", limit=10
    )) == 2
    assert len(successor.predecessor_occurrence_ids) == 2
    for predecessor_id in successor.predecessor_occurrence_ids:
        assert owner.reads.get_derived_occurrence(predecessor_id) is not None


def test_leaf2_history_reuse_requires_exact_context_and_raw_mapping_unit_versions() -> None:
    owner, request = _setup(values=_raw())
    base = owner.materialise(request)
    assert base is not None
    first_predecessor = owner.reads.get_derived_occurrence(base.predecessor_occurrence_ids[0])
    assert first_predecessor is not None
    assert first_predecessor.raw_input_lineage
    permitted = cast(Any, owner)._compatible_history(
        derived_signal_id=first_predecessor.derived_signal_id, request=request,
        parameter_ref=api.VersionRefV1("basic", 1),
        selection_ref=api.VersionRefV1("selector", 1),
    )
    assert first_predecessor in permitted

    alternate_context = replace(request, context_refs=(api.VersionRefV1("other-context", 3),))
    assert not cast(Any, owner)._compatible_history(
        derived_signal_id=first_predecessor.derived_signal_id, request=alternate_context,
        parameter_ref=api.VersionRefV1("basic", 1),
        selection_ref=api.VersionRefV1("selector", 1),
    )

    # A future definition/revision and a different exact field-level mapping cannot
    # become predecessor truth merely because Dxxx and subject happen to match.
    alternate_mapping = replace(
        request,
        raw_input_bindings=(
            replace(request.raw_input_bindings[0],
                    projection_mapping_ref=api.VersionRefV1("map-R034", 2)),
            *request.raw_input_bindings[1:],
        ),
    )
    alternate_units = replace(
        request,
        raw_input_bindings=(
            replace(request.raw_input_bindings[0],
                    unit_convention_ref=api.VersionRefV1("units", 2)),
            *request.raw_input_bindings[1:],
        ),
    )
    for incompatible in (alternate_mapping, alternate_units,
                         replace(request, calculation_definition_version="calc-v2")):
        assert first_predecessor not in cast(Any, owner)._compatible_history(
            derived_signal_id=first_predecessor.derived_signal_id, request=incompatible,
            parameter_ref=api.VersionRefV1("basic", 1),
            selection_ref=api.VersionRefV1("selector", 1),
        )


def test_leaf2_history_anchor_no_future_nearest_neighbour_substitution() -> None:
    def kv(name: str, t: int) -> _stage1.KernelValueV1:
        return _stage1.KernelValueV1(
            value=Decimal(100 + t), occurrence_id=name,
            effective_at_utc=NOW + timedelta(seconds=t),
            received_ts_utc=NOW, subject_instrument="NVDA", source_temporal_kind="true_instant",
        )
    # Anchor at -60s; a point at -59s is ineligible, even though nearest.
    assert _stage1._history_anchor((kv("latest", 0), kv("future-reference", -59)),
                                   as_of=NOW, seconds=60) is None
    selected = _stage1._history_anchor(
        (kv("latest", 0), kv("future-reference", -59), kv("exact", -60)),
        as_of=NOW, seconds=60,
    )
    assert selected is not None and selected[1].occurrence_id == "exact"


def test_leaf2_k04_refuses_shortened_or_unspecified_historical_baseline() -> None:
    points = tuple(
        _stage1.KernelValueV1(
            value=Decimal(i + 1), occurrence_id=f"baseline-{i}",
            effective_at_utc=NOW - timedelta(days=4 - i),
            received_ts_utc=NOW - timedelta(days=4 - i),
            subject_instrument="NVDA", source_temporal_kind="true_instant",
        ) for i in range(5)
    )
    def evaluate(**settings: object) -> object:
        parameter = api.CalculationParameterSetV1(
            context_id="baseline", version=1, profile="P_BASELINE",
            parameters=tuple(settings.items()),
        )
        return _stage1.evaluate_stage1_kernel(
            "D029", raw_inputs={"R144": points}, derived_inputs={}, parameter_set=parameter,
            contexts=(), as_of_utc=NOW, knowledge_cutoff_utc=NOW,
        )
    assert evaluate(minimum_sample=2, history_count=4) is not None
    assert evaluate(minimum_sample=2, history_count=5) is None
    assert evaluate(minimum_sample=2) is None  # no implementation-chosen window


def test_leaf2_k05_requires_exact_versioned_sampling_schedule_not_only_return_count() -> None:
    closes = tuple(
        _stage1.KernelValueV1(
            value=Decimal(100 + i), occurrence_id=f"close-{i}",
            effective_at_utc=NOW - timedelta(days=5 - i),
            received_ts_utc=NOW - timedelta(days=5 - i),
            subject_instrument="NVDA", source_temporal_kind="true_instant",
        ) for i in range(6)
    )
    full_schedule = tuple(item.effective_at_utc for item in closes)
    def evaluate(points: tuple[_stage1.KernelValueV1, ...], **settings: object) -> object:
        param = api.CalculationParameterSetV1(
            context_id="rv", version=1, profile="P_VOL_WINDOW",
            parameters=tuple(settings.items()),
        )
        return _stage1.evaluate_stage1_kernel(
            "D035", raw_inputs={"R151": points}, derived_inputs={}, parameter_set=param,
            contexts=(), as_of_utc=NOW, knowledge_cutoff_utc=NOW,
        )
    config = dict(required_intervals=5,
                  trading_year_fraction_per_interval=Decimal("0.003968253968253968253968253968"))
    assert evaluate(closes, **config, required_sample_instants_utc=full_schedule) is not None
    assert evaluate(closes[:-1], **config, required_sample_instants_utc=full_schedule) is None
    assert evaluate(closes, **config) is None  # never claim five-day sufficiency by count alone
    # Six prices in an hour satisfy count but not the five named trading-day sample instants.
    compressed = tuple(
        replace(v, effective_at_utc=NOW - timedelta(minutes=5 - i),
                received_ts_utc=NOW - timedelta(minutes=5 - i))
        for i, v in enumerate(closes)
    )
    assert evaluate(compressed, **config, required_sample_instants_utc=full_schedule) is None
    # If one expected close is missing, an extra out-of-window point cannot substitute.
    wrong = (*closes[:2], replace(closes[2], effective_at_utc=NOW - timedelta(days=20)),
             *closes[3:])
    assert evaluate(wrong, **config, required_sample_instants_utc=full_schedule) is None
