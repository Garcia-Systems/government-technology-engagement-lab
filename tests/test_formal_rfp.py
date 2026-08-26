from dataclasses import replace
from decimal import Decimal

from government_engagement_lab.evidence import EvidenceLabel
from government_engagement_lab.formal_rfp import (
    acquisition_effort_by_category, assess_formal_rfp, calculate_seller_economics,
    formal_rfp_scenarios, load_formal_rfp_motion, validate_formal_rfp_motion,
)
from government_engagement_lab.models import EngagementMotion, FindingCode, GateStatus, WorkCategory
from government_engagement_lab.stakeholders import load_baseline_topology


def test_fixture_identity_baselines_and_references():
    motion = load_formal_rfp_motion()
    validate_formal_rfp_motion(motion)
    assert motion.identifier == "JAMES_RIVER_FORMAL_RFP"
    assert motion.journey.engagement_motion is EngagementMotion.FORMAL_RFP
    assert len({s.identifier for s in motion.journey.stages}) == len(motion.journey.stages)
    assert {x.stakeholder_id for x in motion.stakeholder_participation} <= {x.identifier for x in load_baseline_topology().stakeholders}
    assert motion.journey.total_effort_hours == 192
    assert motion.journey.total_elapsed_days == 270
    assert motion.journey.modeled_months == 9
    assert motion.engineering_hours == 522
    assert motion.implementation_price == Decimal("78000")
    assert motion.annual_support == Decimal("24000")


def test_labor_assumptions_and_deterministic_seller_economics():
    motion = load_formal_rfp_motion()
    assert all(r.evidence is EvidenceLabel.MODELED_ASSUMPTION for r in motion.labor_rates)
    assert set(acquisition_effort_by_category(motion)) == {WorkCategory.SALES, WorkCategory.SOLUTIONS}
    result = calculate_seller_economics(motion)
    assert result.delivery_labor_cost == Decimal("57420")
    assert result.acquisition_labor_cost == Decimal("20640")
    assert result.acquisition_adjusted_contribution == Decimal("-60")
    assert result.contribution_margin == Decimal("-60") / Decimal("78000")


def test_customer_and_seller_views_are_independent_and_verdict_is_derived():
    result = assess_formal_rfp()
    assert result.customer_economics.first_year_net_recoverable_value == Decimal("2002.80")
    assert result.seller_economics.acquisition_adjusted_contribution == Decimal("-60")
    assert result.project_viability is GateStatus.PASS
    assert result.target_viability is GateStatus.FAIL
    assert result.verdict == "POOR TARGET CUSTOMER"
    assert FindingCode.CONTRIBUTION_BELOW_MODELED_MINIMUM in result.findings
    assert FindingCode.PROCUREMENT_DEPENDENCY in result.findings
    assert not hasattr(result, "score") and not hasattr(result.motion, "procurement_score")


def test_sensitivities_are_isolated_and_labeled():
    baseline = load_formal_rfp_motion()
    scenarios = {x.key: x for x in formal_rfp_scenarios()}
    reduced = scenarios["REDUCED_PROPOSAL_EFFORT"]
    shorter = scenarios["SHORTER_EVALUATION_CYCLE"]
    higher = scenarios["HIGHER_IMPLEMENTATION_PRICE"]
    assert reduced.assessment.motion.journey.total_effort_hours == 96
    assert reduced.assessment.seller_economics.acquisition_labor_cost < calculate_seller_economics(baseline).acquisition_labor_cost
    assert reduced.assessment.target_viability is GateStatus.PASS
    assert shorter.assessment.motion.journey.total_effort_hours == 192
    assert shorter.assessment.motion.journey.total_elapsed_days < 270
    assert shorter.assessment.seller_economics.acquisition_labor_cost == Decimal("20640")
    assert higher.assessment.seller_economics.implementation_revenue == Decimal("90000")
    assert higher.assessment.customer_economics.first_year_net_recoverable_value < 0
    assert higher.assessment.verdict == "NO DEAL"
    assert all(s.evidence is EvidenceLabel.SENSITIVITY_ASSUMPTION for s in (reduced, shorter, higher))
    assert all("SENSITIVITY ASSUMPTION" in s.changed_assumptions[0] for s in (reduced, shorter, higher))
    assert load_formal_rfp_motion() == baseline
