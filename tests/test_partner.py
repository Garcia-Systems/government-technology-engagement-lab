from dataclasses import replace
from decimal import Decimal

from government_engagement_lab.evidence import EvidenceLabel
from government_engagement_lab.formal_rfp import assess_formal_rfp, load_formal_rfp_motion
from government_engagement_lab.models import (
    CustomerRelationshipOwnership, DirectAccess, GateStatus, StageOwner,
)
from government_engagement_lab.partner import (
    assess_partner, calculate_partner_economics, load_partner_motion,
    partner_scenarios, seller_acquisition_hours, validate_partner_motion,
)
from government_engagement_lab.stakeholders import load_baseline_topology


def test_fictional_partner_fixture_and_boundaries_load_and_validate():
    motion = load_partner_motion()
    validate_partner_motion(motion)
    assert motion.partner_name == "Harbor Civic Solutions"
    assert motion.fictional and "wholly fictional" in motion.fiction_notice
    existing = {x.identifier for x in load_baseline_topology().stakeholders}
    assert motion.identifier not in existing
    assert motion.partner_responsibilities and motion.seller_responsibilities
    assert set(motion.partner_responsibilities).isdisjoint(motion.seller_responsibilities)
    assert motion.customer_relationship_owner is CustomerRelationshipOwnership.PARTNER_OWNED
    assert motion.contract_owner is StageOwner.PARTNER
    assert motion.evidence is EvidenceLabel.MODELED_ALTERNATIVE_ASSUMPTION


def test_stage_ownership_reuses_journey_and_topology_without_magic_channel():
    motion = load_partner_motion()
    formal = load_formal_rfp_motion()
    assert {x.stage_id for x in motion.stage_ownership} == {x.identifier for x in formal.journey.stages}
    customer_people = {x.identifier for x in load_baseline_topology().stakeholders}
    allowed = customer_people | {"HARBOR_CIVIC_SOLUTIONS", "TECHNICAL_SELLER"}
    assert all(set(x.stakeholder_ids) <= allowed for x in motion.stage_ownership)
    assert {x.primary_owner for x in motion.stage_ownership} == set(StageOwner)
    assert seller_acquisition_hours(motion) == 91
    assert seller_acquisition_hours(motion) < formal.journey.total_effort_hours
    assert any(x.primary_owner is StageOwner.PARTNER and x.seller_hours for x in motion.stage_ownership)
    assert any(x.primary_owner is StageOwner.SELLER and x.seller_hours for x in motion.stage_ownership)
    assert formal.engineering_hours == 522  # technical delivery did not disappear


def test_channel_revenue_costs_savings_support_and_customer_independence():
    motion = load_partner_motion()
    result = calculate_partner_economics(motion)
    direct = assess_formal_rfp()
    assert result.customer_contract_value == Decimal("102000")
    assert result.customer_contract_value == direct.customer_economics.first_year_cost
    assert result.customer_value_addressed == Decimal("104002.80")
    assert result.customer_first_year_net_value == direct.customer_economics.first_year_net_recoverable_value
    assert result.partner_share == Decimal("18360.00")
    assert result.seller_engagement_revenue == Decimal("83640.00")
    assert result.seller_engagement_revenue != result.customer_contract_value
    assert result.seller_delivery_cost == Decimal("57420")
    assert result.seller_acquisition_cost == Decimal("11055")
    assert result.seller_support_cost == Decimal("3300")
    assert motion.support.seller_support_revenue == Decimal("19680")
    assert motion.support.first_line_owner is StageOwner.PARTNER
    assert motion.support.escalation_owner is StageOwner.SELLER
    assert result.seller_contribution == Decimal("11205")
    assert result.acquisition_hours_saved == 101
    assert result.acquisition_cost_saved == Decimal("9585")
    assert result.net_channel_economic_effect == Decimal("-8775")
    assert result.contribution_margin == result.seller_contribution / result.seller_engagement_revenue


def test_scenarios_are_isolated_labeled_and_change_only_stated_mechanisms():
    original = load_partner_motion()
    baseline, high_fee, high_access, little = partner_scenarios()
    assert high_fee.motion.partner_share_rate == Decimal("0.35")
    assert high_fee.economics.seller_contribution < baseline.economics.seller_contribution
    assert high_fee.verdict == "NO DEAL"
    assert high_access.motion.direct_access is DirectAccess.NO
    assert high_access.economics.customer_value_addressed == baseline.economics.customer_value_addressed
    assert high_access.economics.engineering_hours == baseline.economics.engineering_hours
    assert high_access.verdict == "PARTNER-LED TARGET"
    assert little.motion.partner_share_rate == baseline.motion.partner_share_rate
    assert little.economics.seller_acquisition_hours > baseline.economics.seller_acquisition_hours
    assert little.economics.partner_share == baseline.economics.partner_share
    assert little.economics.acquisition_cost_saved < baseline.economics.acquisition_cost_saved
    assert all(x.changed_assumptions for x in (high_fee, high_access, little))
    assert load_partner_motion() == original
    assert baseline.motion.evidence is EvidenceLabel.MODELED_ALTERNATIVE_ASSUMPTION
    assert high_fee.motion.evidence is EvidenceLabel.SENSITIVITY_ASSUMPTION


def test_partner_led_verdict_obeys_foundational_precedence_and_separates_direct_target():
    baseline = assess_partner()
    assert baseline.project_viability is GateStatus.PASS
    assert baseline.direct_target_viability is GateStatus.FAIL
    assert baseline.target_viability is GateStatus.PASS
    assert baseline.verdict == "PARTNER-LED TARGET"
    broken = replace(load_partner_motion(), partner_share_rate=Decimal("0.90"))
    result = assess_partner(broken)
    assert result.project_viability is GateStatus.FAIL
    assert result.verdict == "NO DEAL"
    assert not hasattr(baseline, "score")
    assert not hasattr(baseline.motion, "channel_score")


def test_chapter_11_contract_vehicle_is_not_present():
    import government_engagement_lab.models as models
    assert not hasattr(models, "ExistingContractVehicle")
    assert "EXISTING_CONTRACT_VEHICLE" not in {x.value for x in models.EngagementMotion}
