from dataclasses import asdict
from decimal import Decimal

from government_engagement_lab.evidence import EvidenceLabel
from government_engagement_lab.existing_path import (
    assess_existing_path, existing_path_scenarios, load_existing_path_motion,
    rfp_vs_existing_path,
)
from government_engagement_lab.formal_rfp import load_formal_rfp_motion
from government_engagement_lab.models import DirectAccess, FindingCode, GateStatus
from government_engagement_lab.stakeholders import load_baseline_topology


def test_fixture_loads_and_mechanism_is_explicitly_fictional():
    m=load_existing_path_motion(); v=m.mechanism
    assert v.fictional and v.evidence is EvidenceLabel.MODELED_ALTERNATIVE_ASSUMPTION
    assert "wholly fictional" in v.fiction_notice and "not a claim" in v.fiction_notice
    assert v.identifier != m.identifier and v.covered_service_categories and v.seller_eligibility
    assert v.standard_terms_established and v.invoicing_path_established and v.pre_established
    assert v.statement_of_work_required and v.procurement_coordination_required


def test_project_approvals_and_governance_are_not_erased():
    m=load_existing_path_motion(); approvals=" ".join(m.mechanism.customer_approvals_still_required).lower()
    ids={s.identifier for s in m.journey.stages}
    assert {"SECURITY_ACCESS_RESPONSE", "ACCESSIBILITY_RESPONSE", "SOLUTION_DESIGN", "AUTHORIZATION"} <= ids
    assert all(word in approvals for word in ("security", "technical", "funding", "acceptance"))
    assert not m.mechanism.additional_competition_required


def test_journey_and_stakeholder_references_are_valid():
    m=load_existing_path_motion(); formal=load_formal_rfp_motion()
    valid_stages={s.identifier for s in formal.journey.stages}
    valid_people={p.identifier for p in load_baseline_topology().stakeholders}
    assert {s.identifier for s in m.journey.stages} <= valid_stages
    assert all(x.stage_id in valid_stages and x.stakeholder_id in valid_people for x in m.stakeholder_participation)


def test_primary_comparison_holds_scope_value_price_and_delivery_constant():
    rfp,path=rfp_vs_existing_path()
    assert path.motion.engineering_hours == rfp.motion.engineering_hours
    assert path.motion.implementation_price == rfp.motion.implementation_price
    assert path.motion.annual_support == rfp.motion.annual_support
    assert path.customer_economics == rfp.customer_economics
    assert path.economics.seller.delivery_labor_cost == rfp.seller_economics.delivery_labor_cost


def test_savings_reconcile_from_actual_stages_and_costs():
    rfp,path=rfp_vs_existing_path(); e=path.economics
    assert rfp.motion.journey.total_effort_hours == 192  # Chapter 4 baseline regression guard
    assert e.acquisition_hours == sum(s.effort_hours for s in path.motion.journey.stages)
    assert e.acquisition_hours_saved == rfp.motion.journey.total_effort_hours-e.acquisition_hours == 78
    assert e.acquisition_cost_saved == rfp.seller_economics.acquisition_labor_cost-e.seller.acquisition_labor_cost == Decimal("7590")
    assert e.elapsed_days_saved == rfp.motion.journey.total_elapsed_days-e.elapsed_days == 143
    assert sum(c.hours_saved for c in path.motion.stage_changes) == e.acquisition_hours_saved
    assert sum(c.days_saved for c in path.motion.stage_changes) == e.elapsed_days_saved
    assert sum(x.hours_saved for x in path.attribution) == e.acquisition_hours_saved


def test_seller_economics_are_deterministic():
    a=assess_existing_path(); s=a.economics.seller
    assert s.acquisition_adjusted_contribution == s.implementation_revenue-s.delivery_labor_cost-s.acquisition_labor_cost
    assert s.contribution_margin == s.acquisition_adjusted_contribution/s.implementation_revenue
    assert a.economics.acquisition_cost_percent_revenue == s.acquisition_labor_cost/s.implementation_revenue


def test_access_is_independent_and_sensitivities_are_ordered_without_mutation():
    before=asdict(load_existing_path_motion()); baseline,weak,nominal,strong=existing_path_scenarios()
    assert baseline.motion.buyer_access is DirectAccess.LIMITED
    assert FindingCode.BUYER_ACCESS_STILL_LIMITED in baseline.findings
    assert weak.motion.buyer_access is DirectAccess.NO and weak.target_viability is GateStatus.FAIL
    assert weak.verdict == "POOR TARGET CUSTOMER"
    assert nominal.economics.acquisition_hours_saved < baseline.economics.acquisition_hours_saved
    assert strong.economics.acquisition_hours_saved > baseline.economics.acquisition_hours_saved
    assert {"SECURITY_ACCESS_RESPONSE", "ACCESSIBILITY_RESPONSE", "SOLUTION_DESIGN"} <= {s.identifier for s in strong.motion.journey.stages}
    assert asdict(load_existing_path_motion()) == before


def test_no_path_score_or_chapter_12_surface_exists():
    payload=asdict(load_existing_path_motion())
    assert not any("score" in key.lower() for key in payload)
    assert FindingCode.SECURITY_REVIEW_STILL_REQUIRED in assess_existing_path().findings
