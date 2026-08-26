from copy import deepcopy
from decimal import Decimal

import pytest

from government_engagement_lab.configuration import (BURDEN, RESIDUAL_THRESHOLDS,
    SupportState, apply_configuration, assess_configuration_first, capabilities,
    classify_residual, configuration_scenarios, interventions,
    load_capability_fixture, load_current_configuration, load_expected_configuration)
from government_engagement_lab.evidence import EvidenceLabel
from government_engagement_lab.formal_rfp import load_formal_rfp_motion


def test_fictional_unique_valid_capability_fixture_and_current_state_load():
    fixture=load_capability_fixture(); caps=capabilities(); current=load_current_configuration()
    assert "fictional" in (fixture["system_name"]+fixture["fiction_notice"]).lower()
    assert len({c.identifier for c in caps}) == len(caps)
    assert all(c.support in SupportState for c in caps)
    assert all(c.evidence is EvidenceLabel.MODELED_ALTERNATIVE_ASSUMPTION for c in caps)
    assert len(current["statuses"]) == 11 and current["required_fields"] == []


def test_application_is_pure_deterministic_expected_and_rejects_unsupported():
    current=load_current_configuration(); original=deepcopy(current)
    first,changes=apply_configuration(current); second,_=apply_configuration(current)
    assert current == original and first == second == load_expected_configuration()
    assert set(changes) == {"statuses","required_fields","saved_queues","reports","notification_rules","process"}
    caps=tuple(c if c.identifier!="required_fields" else c.__class__(c.identifier,c.description,SupportState.NOT_SUPPORTED,c.enabled,c.effort_hours,c.categories,c.limitations,c.evidence) for c in capabilities())
    with pytest.raises(ValueError, match="required_fields"): apply_configuration(current,caps)


def test_decomposition_sequence_caps_recovery_and_classification():
    assert sum(v for _,v in BURDEN) == Decimal("104002.80")
    a=assess_configuration_first()
    assert len({i.identifier for i in interventions()}) == len(interventions())
    assert sum(s.addressed for s in a.steps) == a.economics.value_addressed
    assert a.economics.value_addressed <= Decimal("104002.80")
    assert a.economics.residual_value == Decimal("104002.80")-a.economics.value_addressed
    assert all(a.steps[n].remaining <= a.steps[n-1].remaining for n in range(1,len(a.steps)))
    assert classify_residual(Decimal("4999.99")).value == "IMMATERIAL"
    assert classify_residual(Decimal("5000")).value == "NARROW"
    assert RESIDUAL_THRESHOLDS and not hasattr(a,"score")


def test_effort_acquisition_rates_customer_and_seller_economics():
    a=assess_configuration_first(); e=a.economics
    assert e.configuration_hours == sum(i.effort_hours for i,s in zip(a.interventions,a.steps) if s.addressed)
    assert e.acquisition_hours == 54 and e.engineering_hours > 0
    rates={x.category:x.hourly_cost for x in load_formal_rfp_motion().labor_rates}
    assert rates and e.first_year_cost == e.implementation_price+e.annual_support
    assert e.net_first_year_recoverable_value == e.value_addressed-e.first_year_cost
    assert e.seller.acquisition_adjusted_contribution == e.implementation_price-e.seller.delivery_labor_cost-e.seller.acquisition_labor_cost


def test_scenarios_are_transparent_isolated_and_verdicts_derived():
    before=deepcopy(load_capability_fixture()); base,strong,weak,poor=configuration_scenarios()
    assert load_capability_fixture() == before and configuration_scenarios()[0] == base
    assert strong.economics.value_addressed > base.economics.value_addressed
    assert weak.economics.value_addressed < base.economics.value_addressed
    assert poor.capabilities == base.capabilities and poor.operational_recommendation == "STANDARDIZE FIRST"
    assert strong.assumption_evidence is EvidenceLabel.MODELED_ALTERNATIVE_ASSUMPTION
    assert weak.assumption_evidence is poor.assumption_evidence is EvidenceLabel.SENSITIVITY_ASSUMPTION
    assert all(x.verdict in {"CONFIGURE / BUY","NARROW CUSTOM EDGE","INVESTIGATE","POOR TARGET CUSTOMER","NO DEAL"} for x in (base,strong,weak,poor))
    assert base.custom_residual_candidate and "Chapter 6" in base.custom_residual_candidate
    assert "SMALL" not in " ".join(x.key for x in configuration_scenarios())
