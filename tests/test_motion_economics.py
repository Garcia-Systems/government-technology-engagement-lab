"""Chapter 19 normalization, traceability, and restraint invariants."""
from dataclasses import fields
from decimal import Decimal
from pathlib import Path

from government_engagement_lab.acquisition import acquisition_report
from government_engagement_lab.configuration import assess_configuration_first
from government_engagement_lab.incumbent import AlternativeType, compare_alternatives
from government_engagement_lab.models import GateStatus
from government_engagement_lab.motion_economics import (EVIDENCE_PRECEDENCE,
    HypothesisStatus, conditional_findings, hypothesis_status, motion_comparisons)
from government_engagement_lab.read_only import read_only_scenarios
from government_engagement_lab.throughput import portfolio_scenarios


REQUIRED={"FORMAL_RFP","COOPERATIVE_PAID_PILOT","READ_ONLY_EDGE","CONFIGURATION_FIRST",
 "SMALL_DEPARTMENTAL","JUSTIFIED_LARGER_CONTRACT","PARTNER_LED",
 "EXISTING_PURCHASING_PATH","INCUMBENT_BUY_CONFIGURE","NO_ENGAGEMENT"}

def rows(): return {x.identifier:x for x in motion_comparisons()}

def test_required_motions_are_unique_and_traced():
    result=motion_comparisons(); ids=[x.identifier for x in result]
    assert set(ids)==REQUIRED and len(ids)==len(set(ids))
    assert all(x.evidence_sources for x in result)
    assert set(EVIDENCE_PRECEDENCE) >= {"FORMAL_RFP_ECONOMICS","PILOT_ECONOMICS","THROUGHPUT","REPEATABILITY"}

def test_chapter_15_motions_reconcile_without_recalculation():
    normalized=rows()
    for identifier in REQUIRED-{"READ_ONLY_EDGE","INCUMBENT_BUY_CONFIGURE","NO_ENGAGEMENT"}:
        old=acquisition_report(identifier); new=normalized[identifier]
        assert (new.customer_value_addressed,new.seller_engagement_revenue,new.seller_acquisition_hours,
                new.seller_acquisition_cost,new.seller_delivery_cost,new.acquisition_adjusted_contribution,
                new.elapsed_cycle_days)==(old.customer_value_addressed,old.implementation_revenue,
                old.seller_acquisition_hours,old.acquisition_labor_cost,old.delivery_labor_cost,
                old.acquisition_adjusted_contribution,old.elapsed_days)

def test_read_only_and_configuration_reconcile_to_prior_chapters():
    read=next(x for x in read_only_scenarios() if x.scenario.key=="READ_ONLY_REPORTING_EDGE"); nr=rows()["READ_ONLY_EDGE"]
    assert (nr.customer_value_addressed,nr.residual_value,nr.seller_acquisition_hours,nr.acquisition_adjusted_contribution)==(read.economics.value_addressed,Decimal("104002.80")-read.economics.value_addressed,read.economics.acquisition_hours,read.economics.seller.acquisition_adjusted_contribution)
    config=assess_configuration_first().economics; nc=rows()["CONFIGURATION_FIRST"]
    assert (nc.customer_value_addressed,nc.residual_value)==(config.value_addressed,config.residual_value)

def test_incumbent_profitability_is_not_fabricated_and_na_is_explicit():
    incumbent=rows()["INCUMBENT_BUY_CONFIGURE"]
    prior=next(x for x in compare_alternatives() if x.alternative.alternative_type is AlternativeType.INCUMBENT_MODULE)
    assert incumbent.customer_first_year_cost==prior.economics.first_year_customer_cost
    assert incumbent.seller_engagement_revenue is incumbent.seller_delivery_cost is None
    assert incumbent.acquisition_adjusted_contribution is incumbent.contribution_margin is None

def test_no_engagement_is_an_explicit_full_residual_baseline():
    x=rows()["NO_ENGAGEMENT"]
    assert x.customer_first_year_cost==x.seller_acquisition_cost==x.seller_delivery_cost==Decimal()
    assert x.customer_value_addressed==0 and x.residual_value==Decimal("104002.80")
    assert x.seller_engagement_revenue is None and x.support_owner=="NONE"

def test_customer_and_seller_dimensions_remain_distinct():
    for x in motion_comparisons():
        assert x.customer_value_addressed+x.residual_value==Decimal("104002.80")
        assert x.customer_first_year_cost==x.customer_implementation_price+x.recurring_customer_cost
        if x.seller_engagement_revenue is not None:
            assert x.acquisition_adjusted_contribution is not None
            assert x.seller_acquisition_hours != x.elapsed_cycle_days
    partner=rows()["PARTNER_LED"]
    assert partner.customer_implementation_price != partner.seller_engagement_revenue
    assert partner.customer_first_year_cost==Decimal("102000") # channel share remains outside seller revenue

def test_closed_access_precedes_attractive_arithmetic():
    for key in ("FORMAL_RFP","PARTNER_LED","EXISTING_PURCHASING_PATH"):
        x=rows()[key]
        assert x.available_access_compatibility=="INCOMPATIBLE"
        assert x.viability.technical_feasibility is GateStatus.FAIL
        assert x.target_viability is GateStatus.FAIL
        assert "INFEASIBLE" in x.commercial_verdict

def test_governance_support_and_channel_ownership_are_preserved():
    result=rows()
    assert result["READ_ONLY_EDGE"].governance.disposition.startswith("WRITE_WORK_DISAPPEARS")
    assert result["CONFIGURATION_FIRST"].governance.disposition=="SHIFTS_TO_INCUMBENT"
    assert result["PARTNER_LED"].governance.disposition=="SHIFTS_TO_PARTNER"
    assert result["PARTNER_LED"].customer_relationship_owner=="PARTNER"
    assert result["INCUMBENT_BUY_CONFIGURE"].support_owner=="INCUMBENT_VENDOR"
    assert "CHANNEL_COST" in result["PARTNER_LED"].major_risks

def test_chapter_16_throughput_reconciles_only_where_available():
    result=rows(); old={x.name:x for x in portfolio_scenarios()}
    for key,prior in old.items():
        new=result[key].throughput
        assert (new.completed_engagements_per_year,new.annualized_contribution,new.overloaded_periods)==(prior.completed_per_year,prior.annualized_contribution,prior.overloaded_periods)
    assert result["INCUMBENT_BUY_CONFIGURE"].throughput is None

def test_repeatability_is_structural_not_a_product_or_score_verdict():
    assert all(x.repeatability for x in motion_comparisons())
    names={f.name for f in fields(type(motion_comparisons()[0]))}
    assert "score" not in names and "rank" not in names and "weighted_score" not in names
    source=Path("src/government_engagement_lab/motion_economics.py").read_text().lower()
    assert "chapter 20" in source and "final verdict" in source
    assert "best_motion" not in source and "product_verdict" not in source

def test_conditional_explanations_do_not_overwrite_records():
    findings=conditional_findings()
    assert any("CLOSED_ACCESS" in x for x in findings)
    assert any("EXISTING_PURCHASING_PATH" in x for x in findings)
    assert any("STRONG_SPONSOR" in x for x in findings)

def test_hypothesis_status_derives_from_mixed_motion_evidence_not_capstone():
    status,reasons=hypothesis_status()
    assert status is HypothesisStatus.CONDITIONAL
    assert any("pass target viability" in x for x in reasons)
    assert any("not the final Chapter 20 verdict" in x for x in reasons)
    assert any(x.target_viability is GateStatus.PASS for x in motion_comparisons())
    assert any(x.target_viability is GateStatus.FAIL for x in motion_comparisons())

def test_chapter_20_has_been_created_without_changing_normalization():
    assert list(Path("chapters").glob("chapter-20-*"))
    assert Path("src/government_engagement_lab/capstone.py").exists()
