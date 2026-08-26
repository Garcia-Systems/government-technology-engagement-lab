"""Chapter 4 formal-RFP motion and deterministic, unweighted economics."""

from dataclasses import replace
from decimal import Decimal

from .baseline import _fixture, load_baseline
from .economics import calculate_customer_economics
from .evidence import EvidenceLabel, parse_evidence_label
from .gates import aggregate_viability, determine_verdict
from .models import (
    EngagementJourney, EngagementMotion, EngagementStage, FindingCode,
    FormalRFPAssessment, FormalRFPMotion, FormalRFPScenario, GateDimension,
    GateStatus, LaborCostRate, MotionStakeholderParticipation, ProposalArtifact,
    SellerEconomics, StageType, WorkCategory,
)
from .gates import assess_gates
from .stakeholders import load_baseline_topology


def load_formal_rfp_motion() -> FormalRFPMotion:
    raw = _fixture("formal_rfp_motion.json")
    evidence = parse_evidence_label(raw["evidence"])
    stages = tuple(EngagementStage(
        identifier=x[0], display_name=x[1], description=f"Formal-RFP work: {x[1].lower()}.",
        sequence=x[2], required=True, effort_hours=x[3], elapsed_days=x[4],
        responsible_category=WorkCategory(x[5]), stage_type=StageType(x[6]), evidence=evidence,
        assumptions=("Fictional stage allocation; not a real procurement requirement.",),
    ) for x in raw["stages"])
    journey = EngagementJourney(
        f'{raw["identifier"]}_JOURNEY', raw["name"], raw["description"], raw["customer_name"],
        EngagementMotion(raw["engagement_motion"]), stages, raw["modeled_days_per_month"], evidence,
    )
    motion = FormalRFPMotion(
        raw["identifier"], raw["name"], raw["description"], journey,
        tuple(MotionStakeholderParticipation(x[0], x[1], x[2], evidence) for x in raw["stakeholder_participation"]),
        tuple(ProposalArtifact(x[0], x[1], x[2], evidence) for x in raw["artifacts"]),
        Decimal(raw["implementation_price"]), Decimal(raw["annual_support"]), raw["engineering_hours"],
        tuple(LaborCostRate(WorkCategory(k), Decimal(v), evidence) for k, v in raw["labor_rates"].items()),
        Decimal(raw["minimum_contribution"]), tuple(raw["major_risks"]), evidence,
    )
    validate_formal_rfp_motion(motion)
    return motion


def validate_formal_rfp_motion(motion: FormalRFPMotion) -> None:
    stage_ids = [s.identifier for s in motion.journey.stages]
    if motion.identifier != "JAMES_RIVER_FORMAL_RFP" or len(stage_ids) != len(set(stage_ids)):
        raise ValueError("formal-RFP motion and stage identifiers must be valid and unique")
    people = {p.identifier for p in load_baseline_topology().stakeholders}
    for link in motion.stakeholder_participation:
        if link.stage_id not in stage_ids or link.stakeholder_id not in people:
            raise ValueError("formal-RFP stakeholder reference is invalid")
    if any(a.stage_id not in stage_ids for a in motion.proposal_artifacts):
        raise ValueError("proposal artifact stage is invalid")


def acquisition_effort_by_category(motion: FormalRFPMotion) -> dict[WorkCategory, int]:
    result: dict[WorkCategory, int] = {}
    for stage in motion.journey.stages:
        result[stage.responsible_category] = result.get(stage.responsible_category, 0) + stage.effort_hours
    return result


def calculate_seller_economics(motion: FormalRFPMotion) -> SellerEconomics:
    rates = {r.category: r.hourly_cost for r in motion.labor_rates}
    delivery = Decimal(motion.engineering_hours) * rates[WorkCategory.ENGINEERING]
    acquisition = sum((Decimal(hours) * rates[category]
                       for category, hours in acquisition_effort_by_category(motion).items()), Decimal())
    contribution = motion.implementation_price - delivery - acquisition
    margin = contribution / motion.implementation_price
    return SellerEconomics(motion.implementation_price, delivery, acquisition, Decimal("0"),
                           contribution, margin, EvidenceLabel.OBSERVED_LAB_RESULT)


def assess_formal_rfp(motion: FormalRFPMotion | None = None) -> FormalRFPAssessment:
    motion = motion or load_formal_rfp_motion()
    baseline = load_baseline()
    case = replace(baseline, economics=replace(
        baseline.economics, implementation_price=motion.implementation_price,
        annual_support=motion.annual_support, engineering_hours=motion.engineering_hours,
        solutions_sales_hours=motion.journey.total_effort_hours,
        sales_cycle_months=int(motion.journey.modeled_months),
    ), evidence=motion.evidence)
    customer = calculate_customer_economics(case)
    base_gates = assess_gates(case)
    project = aggregate_viability(tuple(g.status for g in base_gates.gates
        if g.dimension is not GateDimension.TARGET_ATTRACTIVENESS))
    seller = calculate_seller_economics(motion)
    findings = []
    if motion.journey.total_effort_hours >= 192: findings.append(FindingCode.HIGH_ACQUISITION_EFFORT)
    if motion.journey.modeled_months >= 9: findings.append(FindingCode.LONG_ELAPSED_CYCLE)
    findings.extend((FindingCode.MULTIPLE_REQUIRED_APPROVALS,
                     FindingCode.SIGNIFICANT_PRE_AWARD_TECHNICAL_WORK,
                     FindingCode.CONTRACT_COORDINATION_BURDEN,
                     FindingCode.PROCUREMENT_DEPENDENCY,
                     FindingCode.WEAK_DIRECT_BUYER_CONTROL))
    target = GateStatus.PASS
    if seller.acquisition_adjusted_contribution < motion.minimum_contribution:
        target = GateStatus.FAIL
        findings.append(FindingCode.CONTRIBUTION_BELOW_MODELED_MINIMUM)
    verdict = determine_verdict(project, target)
    return FormalRFPAssessment(motion, customer, seller, tuple(findings), project, target,
                               verdict, EvidenceLabel.OBSERVED_LAB_RESULT)


def formal_rfp_scenarios() -> tuple[FormalRFPScenario, ...]:
    base = load_formal_rfp_motion()
    reduced = replace(base, identifier="JAMES_RIVER_FORMAL_RFP_REDUCED_EFFORT",
        journey=replace(base.journey, identifier="FORMAL_RFP_REDUCED_EFFORT_JOURNEY",
            stages=tuple(replace(s, effort_hours=s.effort_hours // 2,
                evidence=EvidenceLabel.SENSITIVITY_ASSUMPTION) for s in base.journey.stages),
            evidence=EvidenceLabel.SENSITIVITY_ASSUMPTION), evidence=EvidenceLabel.SENSITIVITY_ASSUMPTION)
    shorter = replace(base, identifier="JAMES_RIVER_FORMAL_RFP_SHORTER_CYCLE",
        journey=replace(base.journey, identifier="FORMAL_RFP_SHORTER_CYCLE_JOURNEY",
            stages=tuple(replace(s, elapsed_days=(s.elapsed_days * 2) // 3,
                evidence=EvidenceLabel.SENSITIVITY_ASSUMPTION) for s in base.journey.stages),
            evidence=EvidenceLabel.SENSITIVITY_ASSUMPTION), evidence=EvidenceLabel.SENSITIVITY_ASSUMPTION)
    higher = replace(base, identifier="JAMES_RIVER_FORMAL_RFP_HIGHER_PRICE",
                     implementation_price=Decimal("90000.00"), evidence=EvidenceLabel.SENSITIVITY_ASSUMPTION)
    return (
        FormalRFPScenario("BASELINE", "Baseline RFP", assess_formal_rfp(base), (), base.evidence),
        FormalRFPScenario("REDUCED_PROPOSAL_EFFORT", "Lower proposal work", assess_formal_rfp(reduced),
            ("SENSITIVITY ASSUMPTION: every acquisition-stage effort allocation is halved.",), EvidenceLabel.SENSITIVITY_ASSUMPTION),
        FormalRFPScenario("SHORTER_EVALUATION_CYCLE", "Shorter cycle", assess_formal_rfp(shorter),
            ("SENSITIVITY ASSUMPTION: every stage delay is reduced by one third; effort is unchanged.",), EvidenceLabel.SENSITIVITY_ASSUMPTION),
        FormalRFPScenario("HIGHER_IMPLEMENTATION_PRICE", "Higher price", assess_formal_rfp(higher),
            ("SENSITIVITY ASSUMPTION: implementation price is $90,000; acceptance is not assumed.",), EvidenceLabel.SENSITIVITY_ASSUMPTION),
    )
