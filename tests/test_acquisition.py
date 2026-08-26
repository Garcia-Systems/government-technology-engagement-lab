"""Chapter 15 acquisition economics invariants."""
from dataclasses import fields
from decimal import Decimal
from pathlib import Path

from government_engagement_lab.acquisition import (AcquisitionCategory, acquisition_reason_trace,
    acquisition_report, acquisition_reports, focused_scenarios, lost_deal_sensitivity)
from government_engagement_lab.evidence import EvidenceLabel
from government_engagement_lab.formal_rfp import assess_formal_rfp, load_formal_rfp_motion
from government_engagement_lab.pilot import assess_pilot
from government_engagement_lab.partner import assess_partner
from government_engagement_lab.existing_path import assess_existing_path
from government_engagement_lab.small_engagement import assess_small_engagement
from government_engagement_lab.larger_contract import assess_larger_contract
from government_engagement_lab.models import EngagementMotion, FindingCode

EXPECTED={"FORMAL_RFP":(192,Decimal("20640")),"COOPERATIVE_PAID_PILOT":(58,Decimal("6290")),
"CONFIGURATION_FIRST":(54,Decimal("4590")),"SMALL_DEPARTMENTAL":(58,Decimal("5970")),
"JUSTIFIED_LARGER_CONTRACT":(77,Decimal("8105")),"PARTNER_LED":(91,Decimal("11055")),
"EXISTING_PURCHASING_PATH":(114,Decimal("13050"))}

def test_taxonomy_and_motion_references_are_valid():
    assert {x.name for x in AcquisitionCategory} >= {"PROSPECTING","QUALIFICATION","DISCOVERY","MEETINGS","TECHNICAL_VALIDATION","SECURITY_APPROVAL_SUPPORT","ACCESSIBILITY_APPROVAL_SUPPORT","PROPOSAL","PRICING","PROCUREMENT_SUPPORT","CONTRACT_COORDINATION","IMPLEMENTATION_PLANNING","PARTNER_COORDINATION"}
    assert all(isinstance(i.engagement_motion,EngagementMotion) for r in acquisition_reports() for i in r.work_items)

def test_owned_hours_and_costs_reconcile_by_motion():
    for report in acquisition_reports():
        hours,cost=EXPECTED[report.motion]
        assert report.seller_acquisition_hours==hours
        assert report.acquisition_labor_cost==cost
        assert sum(h for h,_ in report.by_category().values())==hours
        assert sum(c for _,c in report.by_category().values())==cost

def test_prior_chapter_totals_are_preserved():
    assert acquisition_report().seller_acquisition_hours==assess_formal_rfp().motion.journey.total_effort_hours==192
    assert acquisition_report("COOPERATIVE_PAID_PILOT").seller_acquisition_hours==assess_pilot().economics.acquisition_hours
    assert acquisition_report("PARTNER_LED").seller_acquisition_hours==assess_partner().economics.seller_acquisition_hours
    assert acquisition_report("EXISTING_PURCHASING_PATH").seller_acquisition_hours==assess_existing_path().economics.acquisition_hours
    assert acquisition_report("SMALL_DEPARTMENTAL").seller_acquisition_hours==assess_small_engagement().engagement.acquisition_hours
    assert acquisition_report("JUSTIFIED_LARGER_CONTRACT").seller_acquisition_hours==assess_larger_contract().engagement.acquisition_hours

def test_partner_and_customer_ownership_remain_separate():
    r=acquisition_report("PARTNER_LED")
    assert (r.seller_acquisition_hours,r.partner_acquisition_hours,r.customer_acquisition_hours)==(91,93,8)
    assert r.total_customer_acquisition_work==192
    assert r.acquisition_labor_cost==assess_partner().economics.seller_acquisition_cost

def test_rates_reuse_chapter_four_and_item_cost_is_mechanical():
    rates={x.hourly_cost for x in load_formal_rfp_motion().labor_rates}
    assert all(i.seller_cost_rate in rates and i.seller_cost==i.seller_cost_rate*i.seller_owned_hours for r in acquisition_reports() for i in r.work_items)

def test_contribution_waterfall_and_ratios():
    for r in acquisition_reports():
        assert r.delivery_contribution==r.implementation_revenue-r.delivery_labor_cost
        assert r.acquisition_adjusted_contribution==r.implementation_revenue-r.delivery_labor_cost-r.acquisition_labor_cost-r.other_direct_costs
        assert r.acquisition_cost_per_revenue==r.acquisition_labor_cost/r.implementation_revenue
        assert r.acquisition_hours_per_10000_revenue==Decimal(r.seller_acquisition_hours)/(r.implementation_revenue/Decimal(10000))
        assert r.delivery_labor_cost not in {r.acquisition_labor_cost,Decimal(r.elapsed_days)}

def test_governance_and_sources_are_attributed_once():
    for r in acquisition_reports():
        ids=[i.identifier for i in r.work_items]; assert len(ids)==len(set(ids))
    formal=acquisition_report(); governance=[i for i in formal.work_items if i.category in {AcquisitionCategory.SECURITY_APPROVAL_SUPPORT,AcquisitionCategory.ACCESSIBILITY_APPROVAL_SUPPORT}]
    assert sum(i.seller_owned_hours for i in governance)==24
    assert all(i.source_reference.startswith("journey:") for i in governance)

def test_partner_share_is_not_a_labor_cost():
    r=acquisition_report("PARTNER_LED"); p=assess_partner().economics
    assert r.implementation_revenue==p.seller_engagement_revenue
    assert r.customer_contract_value==p.customer_contract_value
    assert r.acquisition_labor_cost+p.partner_share != r.acquisition_labor_cost
    assert r.acquisition_adjusted_contribution==p.seller_contribution

def test_lost_deal_keeps_only_real_acquisition_exposure():
    x=lost_deal_sensitivity(); assert x.implementation_revenue==0
    assert x.acquisition_cost_retained==Decimal("20640") and x.opportunity_contribution==Decimal("-20640")

def test_customer_economics_are_not_changed_by_attribution():
    formal=acquisition_report(); prior=assess_formal_rfp()
    assert formal.customer_cost==prior.customer_economics.first_year_cost
    assert formal.customer_value_addressed==Decimal("104002.80")

def test_no_score_or_probability_engine_and_no_chapter_16():
    assert "score" not in {f.name for f in fields(type(acquisition_report()))}
    source=Path("src/government_engagement_lab/acquisition.py").read_text().lower()
    assert "win_probability" not in source and "throughput" not in source
    assert not Path("chapters/chapter-16-throughput-and-opportunity-cost.md").exists()

def test_reason_codes_trace_to_source_evidence():
    trace=acquisition_reason_trace()
    assert trace[FindingCode.HIGH_SOLUTIONS_EFFORT]
    assert trace[FindingCode.PROCUREMENT_DIFFICULTY]

def test_focused_scenarios_do_not_mutate_fixtures_and_labels_are_valid():
    before=load_formal_rfp_motion(); assert len(focused_scenarios())==4
    assert load_formal_rfp_motion()==before
    assert all(isinstance(i.evidence,EvidenceLabel) for r in acquisition_reports() for i in r.work_items)
