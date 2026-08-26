"""Chapter 10 fictional partner/prime motion and transparent channel economics."""

from dataclasses import replace
from decimal import Decimal

from .baseline import _fixture, load_baseline
from .evidence import EvidenceLabel, parse_evidence_label
from .formal_rfp import calculate_seller_economics, load_formal_rfp_motion
from .models import (
    ChannelEffect, CustomerRelationshipOwnership, DirectAccess, GateStatus,
    PartnerAssessment, PartnerCompensationType, PartnerEconomics, PartnerMotion,
    PartnerStageOwnership, StageOwner, SupportOwnership, WorkCategory,
)
from .stakeholders import load_baseline_topology


def load_partner_motion() -> PartnerMotion:
    raw = _fixture("partner_motion.json")
    evidence = parse_evidence_label(raw["evidence"])
    support = raw["support"]
    motion = PartnerMotion(
        raw["identifier"], raw["partner_name"], raw["partner_type"], raw["fictional"],
        raw["fiction_notice"], raw["seller_role"],
        CustomerRelationshipOwnership(raw["customer_relationship_owner"]),
        StageOwner(raw["contract_owner"]), tuple(raw["partner_responsibilities"]),
        tuple(raw["seller_responsibilities"]), tuple(raw["acquisition_effort_shifted"]),
        tuple(raw["acquisition_effort_retained"]),
        tuple(raw["project_management_effort_shifted"]),
        PartnerCompensationType(raw["compensation_type"]), Decimal(raw["partner_share_rate"]),
        DirectAccess(raw["direct_access"]),
        tuple(PartnerStageOwnership(x[0], StageOwner(x[1]), x[2], tuple(x[3]), evidence)
              for x in raw["stages"]),
        SupportOwnership(StageOwner(support["first_line_owner"]),
                         StageOwner(support["escalation_owner"]),
                         Decimal(support["seller_support_revenue"]),
                         support["seller_support_hours"], evidence),
        tuple(raw["dependency_risks"]), tuple(ChannelEffect(x) for x in raw["channel_effects"]),
        evidence,
    )
    validate_partner_motion(motion)
    return motion


def validate_partner_motion(motion: PartnerMotion) -> None:
    formal = load_formal_rfp_motion()
    valid_stages = {stage.identifier for stage in formal.journey.stages}
    modeled_people = {person.identifier for person in load_baseline_topology().stakeholders}
    modeled_people |= {"HARBOR_CIVIC_SOLUTIONS", "TECHNICAL_SELLER"}
    if not motion.fictional or motion.evidence is not EvidenceLabel.MODELED_ALTERNATIVE_ASSUMPTION:
        raise ValueError("partner must be explicitly fictional and alternative-assumption labeled")
    if motion.identifier in modeled_people or not motion.partner_responsibilities or not motion.seller_responsibilities:
        raise ValueError("partner identifier and responsibility boundaries must be valid")
    stage_ids = [stage.stage_id for stage in motion.stage_ownership]
    if set(stage_ids) != valid_stages or len(stage_ids) != len(set(stage_ids)):
        raise ValueError("stage ownership must cover each valid Chapter 4 journey stage once")
    if any(set(stage.stakeholder_ids) - modeled_people for stage in motion.stage_ownership):
        raise ValueError("partner stage uses an unknown Chapter 3 or external commercial stakeholder")
    if not Decimal("0") <= motion.partner_share_rate < Decimal("1"):
        raise ValueError("partner share must be a proportion")
    if not any(stage.seller_hours for stage in motion.stage_ownership):
        raise ValueError("a partner cannot erase seller technical work")


def seller_acquisition_hours(motion: PartnerMotion) -> int:
    """Seller and joint work is explicit; partner/customer stages can retain small seller inputs."""
    return sum(stage.seller_hours for stage in motion.stage_ownership)


def calculate_partner_economics(motion: PartnerMotion | None = None) -> PartnerEconomics:
    motion = motion or load_partner_motion()
    formal = load_formal_rfp_motion()
    direct = calculate_seller_economics(formal)
    rates = {rate.category: rate.hourly_cost for rate in formal.labor_rates}
    categories = {stage.identifier: stage.responsible_category for stage in formal.journey.stages}
    acquisition = sum((Decimal(stage.seller_hours) * rates[categories[stage.stage_id]]
                       for stage in motion.stage_ownership), Decimal())
    customer_contract = formal.implementation_price + formal.annual_support
    partner_share = customer_contract * motion.partner_share_rate
    seller_revenue = customer_contract - partner_share
    delivery = Decimal(formal.engineering_hours) * rates[WorkCategory.ENGINEERING]
    raw = _fixture("partner_motion.json")
    pm_cost = Decimal(raw["retained_project_management_hours"]) * rates[WorkCategory.ENGINEERING]
    support_cost = Decimal(motion.support.seller_support_hours) * rates[WorkCategory.ENGINEERING]
    contribution = seller_revenue - delivery - acquisition - pm_cost - support_cost
    hours = seller_acquisition_hours(motion)
    return PartnerEconomics(
        customer_contract, load_baseline().burden.annual_recoverable_value,
        load_baseline().burden.annual_recoverable_value - customer_contract,
        partner_share, seller_revenue, delivery, hours, acquisition, pm_cost, support_cost,
        contribution, contribution / seller_revenue,
        formal.journey.total_effort_hours - hours,
        direct.acquisition_labor_cost - acquisition,
        direct.acquisition_labor_cost - acquisition - partner_share,
        formal.engineering_hours, raw["cycle_days"], EvidenceLabel.OBSERVED_LAB_RESULT,
    )


def assess_partner(motion: PartnerMotion | None = None,
                   changed_assumptions: tuple[str, ...] = ()) -> PartnerAssessment:
    motion = motion or load_partner_motion()
    economics = calculate_partner_economics(motion)
    customer_pass = economics.customer_first_year_net_value >= 0
    delivery_pass = economics.seller_contribution >= load_formal_rfp_motion().minimum_contribution
    project = GateStatus.PASS if customer_pass and delivery_pass else GateStatus.FAIL
    direct_target = GateStatus.FAIL  # Chapter 4's comparable Formal RFP result.
    credible_access = motion.direct_access in {DirectAccess.LIMITED, DirectAccess.NO}
    target = GateStatus.PASS if project is GateStatus.PASS and credible_access else GateStatus.FAIL
    if project is GateStatus.FAIL:
        verdict = "NO DEAL"
    elif direct_target is GateStatus.FAIL and target is GateStatus.PASS:
        verdict = "PARTNER-LED TARGET"
    else:
        verdict = "POOR TARGET CUSTOMER"
    return PartnerAssessment(motion, economics, project, direct_target, target, verdict,
                             changed_assumptions)


def partner_scenarios() -> tuple[PartnerAssessment, ...]:
    baseline = load_partner_motion()
    high_fee = replace(baseline, partner_share_rate=Decimal("0.35"),
                       evidence=EvidenceLabel.SENSITIVITY_ASSUMPTION)
    high_access = replace(baseline, identifier="HARBOR_CIVIC_HIGH_VALUE_ACCESS",
                          direct_access=DirectAccess.NO,
                          evidence=EvidenceLabel.SENSITIVITY_ASSUMPTION)
    little_stages = tuple(replace(stage, seller_hours=max(stage.seller_hours,
        next(x.effort_hours for x in load_formal_rfp_motion().journey.stages
             if x.identifier == stage.stage_id) - 2 if stage.primary_owner is StageOwner.PARTNER else stage.seller_hours),
        evidence=EvidenceLabel.SENSITIVITY_ASSUMPTION) for stage in baseline.stage_ownership)
    little = replace(baseline, identifier="HARBOR_CIVIC_ADDS_LITTLE", stage_ownership=little_stages,
                     evidence=EvidenceLabel.SENSITIVITY_ASSUMPTION)
    return (
        assess_partner(baseline),
        assess_partner(high_fee, ("Partner share rises from 18% to 35%; access and work shift are unchanged.",)),
        assess_partner(high_access, ("Direct opportunity access changes from LIMITED to NO; technical value and scope are unchanged.",)),
        assess_partner(little, ("Partner fee stays at 18% while seller work on partner-owned stages increases.",)),
    )


def direct_vs_partner() -> tuple[object, PartnerAssessment]:
    from .formal_rfp import assess_formal_rfp
    return assess_formal_rfp(), assess_partner()
