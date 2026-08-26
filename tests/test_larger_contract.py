from decimal import Decimal
from dataclasses import replace

from government_engagement_lab.baseline import load_baseline
from government_engagement_lab.evidence import EvidenceLabel
from government_engagement_lab.formal_rfp import load_formal_rfp_motion
from government_engagement_lab.larger_contract import (CorridorClass, assess_larger_contract,
    assess_larger_contract_scenarios, load_larger_contract, load_larger_contract_scenarios)
from government_engagement_lab.models import GateStatus

def test_fixture_expands_scope_explicitly_without_double_counting():
    e=load_larger_contract(); ids=[x.identifier for x in e.components]
    assert e.baseline_scope and e.users>8 and e.additional_data_sources
    assert len(ids)==len(set(ids)) and all(x.incremental_value>0 for x in e.components)
    assert all(x.burden_categories and x.overlap>=0 for x in e.components)
    assert e.value_addressed==Decimal("80681.1760")
    assert e.value_addressed<=load_baseline().burden.annual_recoverable_value==e.opportunity_value
    assert e.residual_value==Decimal("23321.6240")

def test_delivery_acquisition_governance_and_support_are_decomposed():
    e=load_larger_contract()
    assert e.engineering_hours==245==sum(x.hours for x in e.baseline_engineering)+sum(w.hours for c in e.components for w in c.engineering)
    assert e.acquisition_floor_hours==58 and e.incremental_acquisition_hours==19 and e.acquisition_hours==77
    assert e.acquisition_hours!=58 and Decimal(e.acquisition_hours)/Decimal(58)!=e.value_addressed/e.baseline_value
    assert all(c.governance_surface and c.support_surface for c in e.components)
    assert e.support_hours==55 and e.annual_support_revenue==Decimal("8000")
    assert [(x.category,x.hourly_cost) for x in e.labor_rates]==[(x.category,x.hourly_cost) for x in load_formal_rfp_motion().labor_rates]

def test_price_corridor_and_leverage_calculate_independently():
    a=assess_larger_contract(); e=a.engagement
    assert a.seller.delivery_labor_cost==Decimal("26950")
    assert a.seller.acquisition_labor_cost==Decimal("8105")
    assert a.seller_price_floor==Decimal("47555")
    assert a.customer_price_ceiling==e.value_addressed-e.annual_support_revenue==Decimal("72681.1760")
    assert a.viable_price_corridor==a.customer_price_ceiling-a.seller_price_floor==Decimal("25126.1760")
    assert a.corridor_class is CorridorClass.VIABLE_CORRIDOR
    assert a.acquisition_cost_percent_revenue==a.seller.acquisition_labor_cost/e.implementation_price
    assert a.acquisition_hours_per_10000_revenue==Decimal(e.acquisition_hours)/(e.implementation_price/Decimal(10000))
    # Changing seller cost cannot move the customer ceiling.
    assert assess_larger_contract(replace(e,other_direct_cost=Decimal("9999"))).customer_price_ceiling==a.customer_price_ceiling

def test_scenarios_expose_failure_mechanisms_without_mutating_baseline():
    before=load_larger_contract(); justified,price_only,overreach,efficient=assess_larger_contract_scenarios()
    assert price_only.engagement.value_addressed==price_only.engagement.baseline_value
    assert price_only.engagement.implementation_price>Decimal("30000") and price_only.net_customer_value<0
    assert price_only.project_viability is GateStatus.FAIL and price_only.verdict=="NO DEAL"
    assert overreach.engagement.engineering_hours>justified.engagement.engineering_hours
    assert overreach.engagement.value_addressed<justified.engagement.value_addressed
    assert overreach.viable_price_corridor<0 and overreach.corridor_class is CorridorClass.NO_CORRIDOR
    assert overreach.seller.acquisition_adjusted_contribution<justified.seller.acquisition_adjusted_contribution
    assert [(c.identifier,c.incremental_value,c.engineering,c.acquisition) for c in efficient.engagement.components]==[(c.identifier,c.incremental_value,c.engineering,c.acquisition) for c in justified.engagement.components]
    assert efficient.engagement.acquisition_floor_hours<justified.engagement.acquisition_floor_hours
    assert efficient.engagement.incremental_acquisition_hours==justified.engagement.incremental_acquisition_hours
    assert efficient.engagement.evidence is EvidenceLabel.SENSITIVITY_ASSUMPTION
    assert all(x.changed_assumptions or x.key=="JUSTIFIED_LARGER" for x in load_larger_contract_scenarios())
    assert load_larger_contract()==before

def test_bigger_revenue_does_not_force_a_better_verdict_or_contribution():
    justified,price_only,overreach,_=assess_larger_contract_scenarios()
    assert overreach.engagement.implementation_price>justified.engagement.implementation_price
    assert overreach.verdict=="NO DEAL" and justified.verdict=="PROMISING — VALIDATE IN DISCOVERY"
    assert overreach.seller.acquisition_adjusted_contribution<justified.seller.acquisition_adjusted_contribution
    assert price_only.seller.acquisition_adjusted_contribution>Decimal("10000")
    assert price_only.project_viability is GateStatus.FAIL and price_only.target_viability is GateStatus.PASS
