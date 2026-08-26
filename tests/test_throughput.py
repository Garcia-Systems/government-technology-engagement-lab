"""Chapter 16 throughput, capacity, and opportunity-cost invariants."""
from dataclasses import fields, replace
from decimal import Decimal
from pathlib import Path

from government_engagement_lab.acquisition import acquisition_report
from government_engagement_lab.evidence import EvidenceLabel
from government_engagement_lab.throughput import (CapacityState, PipelineOpportunity,
    SellerRole, additional_capacity_sensitivity, load_seller_organization,
    lost_opportunity_sensitivity, mixed_portfolio, motion_portfolio, opportunity,
    opportunity_cost, portfolio_scenarios, simulate, workload_profile)


def test_capacity_fixture_loads_with_explicit_valid_assumptions():
    org=load_seller_organization()
    assert org.fiction_notice and "not a staffing recommendation" in org.fiction_notice
    assert {r.role for r in org.roles}==set(SellerRole)
    assert all(r.evidence is EvidenceLabel.MODELED_ASSUMPTION for r in org.roles)
    assert all(r.monthly_work_hours-r.non_acquisition_reserve_hours==r.acquisition_capacity_hours for r in org.roles)
    assert org.monthly_acquisition_capacity==128


def test_profiles_reconcile_to_chapter_15_but_not_elapsed_days():
    for motion in ("FORMAL_RFP","COOPERATIVE_PAID_PILOT","PARTNER_LED","EXISTING_PURCHASING_PATH"):
        report=acquisition_report(motion); profile=workload_profile(motion)
        assert sum(profile)==report.seller_acquisition_hours
        assert sum(profile)!=report.elapsed_days
        assert len(set(profile))>1  # deliberately lumpy, never uniform hours/day


def test_pipeline_counts_demand_and_detects_overload():
    formal=motion_portfolio("FORMAL_RFP")
    assert formal.periods[0].active_opportunity_count==1
    assert formal.periods[1].active_opportunity_count==2
    assert formal.periods[1].acquisition_demand==52
    assert any(p.state is CapacityState.OVER_CAPACITY for p in formal.periods)
    assert formal.deferred_hours==98


def test_fifo_deferred_work_extends_cycle_deterministically():
    formal=motion_portfolio("FORMAL_RFP")
    completion=dict(formal.completion_periods)
    assert completion["FORMAL_RFP-6"]-6+1 > len(workload_profile("FORMAL_RFP"))
    assert formal.average_cycle_periods==Decimal("9.875")


def test_opportunity_count_is_descriptive_not_capacity_rule():
    lows=simulate("LOW",[opportunity(f"P{i}","COOPERATIVE_PAID_PILOT",1) for i in range(5)])
    highs=simulate("HIGH",[opportunity(f"R{i}","FORMAL_RFP",1) for i in range(5)])
    assert lows.periods[1].active_opportunity_count==highs.periods[1].active_opportunity_count==5
    assert lows.periods[1].state is CapacityState.AVAILABLE
    assert highs.periods[1].state is CapacityState.OVER_CAPACITY


def test_four_scenarios_reuse_seller_borne_motion_data_and_throughput():
    scenarios=portfolio_scenarios()
    assert tuple(x.name for x in scenarios)==("FORMAL_RFP","COOPERATIVE_PAID_PILOT","PARTNER_LED","EXISTING_PURCHASING_PATH")
    assert tuple(x.completed_per_year for x in scenarios)==(4,8,4,7)
    assert all(o.workload==workload_profile(o.motion) for x in scenarios for o in x.opportunities)


def test_contribution_per_deal_and_annualized_contribution_are_distinct():
    formal,pilot,partner,path=portfolio_scenarios()
    assert acquisition_report("COOPERATIVE_PAID_PILOT").acquisition_adjusted_contribution==Decimal("13310")
    assert pilot.annualized_contribution==Decimal("106480")
    assert partner.annualized_contribution==Decimal("44820")
    assert path.annualized_contribution==Decimal("52710")
    assert formal.annualized_contribution==Decimal("-240")


def test_opportunity_cost_is_displaced_contribution_not_calendar_price():
    formal,pilot,*_=portfolio_scenarios()
    assert opportunity_cost(formal,pilot)==Decimal("106720")
    assert "elapsed_days" not in opportunity_cost.__code__.co_names


def test_more_capacity_is_explicit_and_removes_overload_not_cycle_constraint():
    base=motion_portfolio("FORMAL_RFP"); extra=additional_capacity_sensitivity()
    assert extra.base_capacity==base.base_capacity+72
    assert extra.overloaded_periods==0
    assert extra.completed_per_year==base.completed_per_year==4
    assert extra.opportunities==base.opportunities


def test_lost_long_cycle_keeps_work_and_cost_but_removes_revenue():
    result=lost_opportunity_sensitivity(); lost=result.opportunities[0]
    assert lost.status=="LOST" and lost.expected_implementation_revenue==0
    assert sum(lost.workload)==192
    assert lost.acquisition_adjusted_contribution==-acquisition_report().acquisition_labor_cost
    assert result.annualized_contribution==Decimal("-20820")


def test_mixed_portfolio_and_results_do_not_mutate_prior_fixtures():
    before=acquisition_report(); mixed=mixed_portfolio()
    assert (len(mixed.opportunities),mixed.completed_per_year,mixed.annualized_contribution)==(5,5,Decimal("41620"))
    assert acquisition_report()==before


def test_no_capacity_score_probability_or_chapter_19():
    assert "score" not in {f.name for f in fields(type(portfolio_scenarios()[0]))}
    source=Path("src/government_engagement_lab/throughput.py").read_text().lower()
    assert "win_probability" not in source and "elapsed_days *" not in source
    assert not Path("chapters/chapter-20-capstone.md").exists()
    assert all(isinstance(o.evidence,EvidenceLabel) for r in portfolio_scenarios() for o in r.opportunities)
