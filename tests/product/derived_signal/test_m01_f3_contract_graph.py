"""F3a: independent public contract-predecessor proofs (brief K02, §8.1, §§11–13)."""
from dataclasses import replace
from datetime import timedelta
from decimal import Decimal

import pytest

from nvda_desk.derived_signal_calculation_truth import api

from .test_m01_stage1_predecessor_scope import NOW, _setup


@pytest.mark.parametrize("target", ["D109", "D170"])
def test_f3_contract_predecessors_remain_exact_and_reconstructable(target: str) -> None:
    owner, req = _setup(target=target)
    result = owner.materialise(req)
    assert result is not None
    direct = [owner.reads.get_derived_occurrence(x) for x in result.predecessor_occurrence_ids]
    option_mids = [x for x in direct if x is not None and x.derived_signal_id == "D087"]
    assert len(option_mids) == 2
    assert {x.selection_identity.value_for("contract_id") for x in option_mids} == {
        "C100", "P100"
    }
    assert {x.derived_occurrence_id for x in option_mids} <= set(result.predecessor_occurrence_ids)
    assert all(x.raw_input_lineage for x in option_mids)
    assert {v.observation_occurrence_id for v in result.raw_input_lineage} >= {
        "obs-R034-C100", "obs-R034-P100", "obs-R035-C100", "obs-R035-P100"
    }
    assert owner.materialise(req) == result


@pytest.mark.parametrize("target", ["D109", "D170"])
def test_f3_contract_graph_refuses_unavailable_input_at_cutoff(target: str) -> None:
    owner, req = _setup(target=target)
    at = NOW - timedelta(seconds=1)
    assert owner.materialise(replace(req, as_of_utc=at, knowledge_cutoff_utc=at)) is None


@pytest.mark.parametrize("target", ["D109", "D170"])
def test_f3_contract_graph_refuses_wrong_child_policy_version(target: str) -> None:
    owner, req = _setup(target=target)
    broken = tuple((did, api.VersionRefV1(ref.context_id, 987)) for did, ref in req.predecessor_selection_policy_refs)
    assert owner.materialise(replace(req, predecessor_selection_policy_refs=broken)) is None


def test_f3_d109_cross_strike_call_put_cannot_masquerade_as_atm_pair() -> None:
    owner, req = _setup(target="D109", put_strike=Decimal("105"))
    assert owner.materialise(req) is None
