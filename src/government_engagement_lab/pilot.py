"""Chapter 5 cooperative paid-pilot experiment over synthetic records."""

from dataclasses import dataclass, replace
from decimal import Decimal

from .baseline import _fixture, load_baseline
from .evidence import EvidenceLabel, parse_evidence_label
from .formal_rfp import acquisition_effort_by_category, load_formal_rfp_motion
from .models import (EngagementJourney, EngagementMotion, EngagementStage, GateStatus,
                     LaborCostRate, MotionStakeholderParticipation, PilotAcceptance,
                     SellerEconomics, SponsorStrength, StageType, WorkCategory)
from .stakeholders import load_baseline_topology


@dataclass(frozen=True)
class PilotCriterion:
    identifier: str
    metric: str
    threshold: int
    operator: str
    evidence: EvidenceLabel = EvidenceLabel.MODELED_ASSUMPTION


@dataclass(frozen=True)
class PilotOperationalResult:
    records_processed: int
    reconciliations_performed: int
    duplicate_actions_avoided: int
    exceptions_surfaced: int
    manual_lookup_actions_reduced: int
    report_preparation_actions_reduced: int
    status_views_produced: int
    modeled_users_completing: int
    evidence: EvidenceLabel = EvidenceLabel.OBSERVED_LAB_RESULT


@dataclass(frozen=True)
class PilotEconomics:
    pilot_price: Decimal
    pilot_period_support: Decimal
    annualized_value_potentially_affected: Decimal
    expected_measurable_benefit: Decimal
    customer_pilot_net_benefit: Decimal
    action_value_estimate: Decimal
    acquisition_hours: int
    authorization_days: int
    seller: SellerEconomics
    evidence: EvidenceLabel = EvidenceLabel.OBSERVED_LAB_RESULT


@dataclass(frozen=True)
class PilotMotion:
    identifier: str
    name: str
    customer_name: str
    fiction_notice: str
    paid: bool
    duration_days: int
    scope: tuple[str, ...]
    exclusions: tuple[str, ...]
    handoff: str
    journey: EngagementJourney
    stakeholders: tuple[MotionStakeholderParticipation, ...]
    sponsor_strength: SponsorStrength
    acceptance_criteria: tuple[PilotCriterion, ...]
    records: tuple[dict, ...]
    pilot_price: Decimal
    pilot_period_support: Decimal
    annualized_value_potentially_affected: Decimal
    expected_measurable_benefit: Decimal
    engineering_hours: int
    other_direct_cost: Decimal
    minimum_contribution: Decimal
    labor_rates: tuple[LaborCostRate, ...]
    minutes_per_avoided_action: int
    labor_cost_per_hour: Decimal
    modeled_users_completing: int
    evidence: EvidenceLabel


@dataclass(frozen=True)
class PilotAssessment:
    motion: PilotMotion
    operations: PilotOperationalResult
    economics: PilotEconomics
    acceptance: PilotAcceptance
    project_viability: GateStatus
    target_viability: GateStatus
    verdict: str
    full_implementation_authorized: bool
    next_step: str
    evidence: EvidenceLabel = EvidenceLabel.OBSERVED_LAB_RESULT


@dataclass(frozen=True)
class PilotScenario:
    key: str
    name: str
    assessment: PilotAssessment
    changed_assumptions: tuple[str, ...]
    evidence: EvidenceLabel


def load_pilot_motion() -> PilotMotion:
    raw = _fixture("pilot_case.json")
    evidence = parse_evidence_label(raw["evidence"])
    stages = tuple(EngagementStage(
        identifier=x[0], display_name=x[1], description=f"Bounded pilot work: {x[1].lower()}.",
        sequence=x[2], required=True, effort_hours=x[3], elapsed_days=x[4],
        responsible_category=WorkCategory(x[5]), stage_type=StageType(x[6]), evidence=evidence,
        assumptions=("Fictional pilot stage; not a real procurement requirement.",),
    ) for x in raw["stages"])
    journey = EngagementJourney(
        f'{raw["identifier"]}_JOURNEY', raw["name"],
        "Paid, bounded journey through authorization, delivery, measurement, and acceptance.",
        raw["customer_name"], EngagementMotion(raw["engagement_motion"]), stages,
        raw["modeled_days_per_month"], evidence,
    )
    # Chapter 4's rates are intentionally reused rather than copied from the fixture.
    rates = load_formal_rfp_motion().labor_rates
    motion = PilotMotion(
        raw["identifier"], raw["name"], raw["customer_name"], raw["fiction_notice"],
        raw["paid"], raw["duration_days"], tuple(raw["scope"]), tuple(raw["exclusions"]),
        raw["handoff"], journey,
        tuple(MotionStakeholderParticipation("PILOT", x[0], x[1], evidence) for x in raw["stakeholders"]),
        SponsorStrength.STRONG,
        tuple(PilotCriterion(x[0], x[1], x[2], x[3]) for x in raw["acceptance_criteria"]),
        tuple(raw["records"]), Decimal(raw["pilot_price"]), Decimal(raw["pilot_period_support"]),
        Decimal(raw["annualized_value_potentially_affected"]), Decimal(raw["expected_measurable_benefit"]),
        raw["engineering_hours"], Decimal(raw["other_direct_cost"]), Decimal(raw["minimum_contribution"]),
        rates, raw["value_assumptions"]["minutes_per_avoided_action"],
        Decimal(raw["value_assumptions"]["labor_cost_per_hour"]),
        raw["value_assumptions"]["modeled_users_completing"], evidence,
    )
    validate_pilot_motion(motion)
    return motion


def validate_pilot_motion(motion: PilotMotion) -> None:
    if motion.identifier != "JAMES_RIVER_COOPERATIVE_PAID_PILOT":
        raise ValueError("invalid pilot identifier")
    if not motion.paid or motion.pilot_price <= 0 or motion.duration_days <= 0:
        raise ValueError("pilot must be paid and time-limited")
    if not motion.scope or not motion.exclusions or not motion.acceptance_criteria:
        raise ValueError("pilot boundary and acceptance must be explicit")
    stage_ids = [s.identifier for s in motion.journey.stages]
    if len(stage_ids) != len(set(stage_ids)) or motion.journey.engagement_motion is not EngagementMotion.COOPERATIVE_PAID_PILOT:
        raise ValueError("invalid pilot journey")
    people = {p.identifier for p in load_baseline_topology().stakeholders}
    if {x.stakeholder_id for x in motion.stakeholders} - people:
        raise ValueError("pilot stakeholder is outside Chapter 3 topology")
    if motion.annualized_value_potentially_affected > load_baseline().burden.annual_recoverable_value:
        raise ValueError("pilot cannot address more than the full opportunity")


def run_pilot_records(motion: PilotMotion) -> PilotOperationalResult:
    allowed = {"SUBMITTED", "IN_REVIEW", "APPROVED", "CORRECTION_REQUESTED", "RESUBMITTED"}
    latest: dict[str, str] = {}
    duplicates = exceptions = reconciliations = 0
    for record in motion.records:
        permit, status = record.get("permit_id"), record.get("status")
        if not permit or status not in allowed:
            exceptions += 1
            continue
        if latest.get(permit) == status:
            duplicates += 1
            continue
        latest[permit] = status
        reconciliations += 1
    views = len(latest)
    return PilotOperationalResult(len(motion.records), reconciliations, duplicates, exceptions,
                                  views, views, views, motion.modeled_users_completing)


def acquisition_stages(motion: PilotMotion) -> tuple[EngagementStage, ...]:
    return tuple(s for s in motion.journey.ordered_stages if s.sequence <= 8)


def calculate_pilot_economics(motion: PilotMotion, operations: PilotOperationalResult | None = None) -> PilotEconomics:
    operations = operations or run_pilot_records(motion)
    rates = {r.category: r.hourly_cost for r in motion.labor_rates}
    delivery = Decimal(motion.engineering_hours) * rates[WorkCategory.ENGINEERING]
    acquisition = sum((Decimal(s.effort_hours) * rates[s.responsible_category] for s in acquisition_stages(motion)), Decimal())
    contribution = motion.pilot_price - delivery - acquisition - motion.other_direct_cost
    seller = SellerEconomics(motion.pilot_price, delivery, acquisition, motion.other_direct_cost,
                             contribution, contribution / motion.pilot_price,
                             EvidenceLabel.OBSERVED_LAB_RESULT)
    avoided = operations.duplicate_actions_avoided + operations.manual_lookup_actions_reduced + operations.report_preparation_actions_reduced
    action_value = (Decimal(avoided * motion.minutes_per_avoided_action) / Decimal(60)) * motion.labor_cost_per_hour
    return PilotEconomics(motion.pilot_price, motion.pilot_period_support,
        motion.annualized_value_potentially_affected, motion.expected_measurable_benefit,
        motion.expected_measurable_benefit - motion.pilot_price, action_value,
        sum(s.effort_hours for s in acquisition_stages(motion)),
        sum(s.elapsed_days for s in acquisition_stages(motion)), seller)


def evaluate_acceptance(motion: PilotMotion, result: PilotOperationalResult) -> PilotAcceptance:
    values = result.__dict__
    passed = sum((values[c.metric] >= c.threshold if c.operator == "gte" else values[c.metric] == c.threshold)
                 for c in motion.acceptance_criteria)
    if passed == len(motion.acceptance_criteria):
        return PilotAcceptance.PILOT_ACCEPTED
    if passed >= len(motion.acceptance_criteria) - 1:
        return PilotAcceptance.PILOT_CONDITIONAL
    return PilotAcceptance.PILOT_FAILED


def assess_pilot(motion: PilotMotion | None = None) -> PilotAssessment:
    motion = motion or load_pilot_motion()
    operations = run_pilot_records(motion)
    economics = calculate_pilot_economics(motion, operations)
    acceptance = evaluate_acceptance(motion, operations)
    project = GateStatus.PASS if (acceptance is not PilotAcceptance.PILOT_FAILED and economics.customer_pilot_net_benefit >= 0) else GateStatus.FAIL
    sustainable = economics.seller.acquisition_adjusted_contribution >= motion.minimum_contribution
    bounded = motion.engineering_hours < load_formal_rfp_motion().engineering_hours
    target = GateStatus.PASS if sustainable and bounded and motion.sponsor_strength is SponsorStrength.STRONG else GateStatus.FAIL
    verdict = "NO DEAL" if project is GateStatus.FAIL else ("PILOT-FIRST TARGET" if target is GateStatus.PASS else "POOR TARGET CUSTOMER")
    return PilotAssessment(motion, operations, economics, acceptance, project, target, verdict,
                           False, "VALIDATE EXPANSION" if acceptance is PilotAcceptance.PILOT_ACCEPTED else "RE-SCOPE")


def pilot_scenarios() -> tuple[PilotScenario, ...]:
    base = load_pilot_motion()
    small = replace(base, identifier="PILOT_TOO_SMALL", pilot_price=Decimal("12000"),
                    engineering_hours=70, expected_measurable_benefit=Decimal("13000"),
                    evidence=EvidenceLabel.SENSITIVITY_ASSUMPTION)
    broad_stages = tuple(replace(s, effort_hours=(s.effort_hours * 5) // 2,
                           elapsed_days=(s.elapsed_days * 3) // 2,
                           evidence=EvidenceLabel.SENSITIVITY_ASSUMPTION) if s.sequence <= 8 else s
                         for s in base.journey.stages)
    broad = replace(base, identifier="PILOT_TOO_BROAD", pilot_price=Decimal("65000"),
                    engineering_hours=400, annualized_value_potentially_affected=Decimal("90000"),
                    expected_measurable_benefit=Decimal("70000"), other_direct_cost=Decimal("2000"),
                    journey=replace(base.journey, stages=broad_stages, evidence=EvidenceLabel.SENSITIVITY_ASSUMPTION),
                    evidence=EvidenceLabel.SENSITIVITY_ASSUMPTION)
    weak_stages = tuple(replace(s, effort_hours=s.effort_hours + (6 if s.sequence <= 8 else 0),
                          elapsed_days=s.elapsed_days + (8 if s.sequence <= 8 else 0),
                          evidence=EvidenceLabel.SENSITIVITY_ASSUMPTION) for s in base.journey.stages)
    weak = replace(base, identifier="PILOT_WEAK_SPONSOR", sponsor_strength=SponsorStrength.LIMITED,
                   journey=replace(base.journey, stages=weak_stages, evidence=EvidenceLabel.SENSITIVITY_ASSUMPTION),
                   evidence=EvidenceLabel.SENSITIVITY_ASSUMPTION)
    label = EvidenceLabel.SENSITIVITY_ASSUMPTION
    return (
        PilotScenario("BASELINE", "Cooperative baseline", assess_pilot(base), (), base.evidence),
        PilotScenario("TOO_SMALL", "Pilot too small", assess_pilot(small),
                      ("SENSITIVITY ASSUMPTION: price, benefit, and delivery scope are reduced independently.",), label),
        PilotScenario("TOO_BROAD", "Pilot too broad", assess_pilot(broad),
                      ("SENSITIVITY ASSUMPTION: scope, governance effort, delay, price, and value surface expand.",), label),
        PilotScenario("WEAK_SPONSOR", "Weak sponsor", assess_pilot(weak),
                      ("SENSITIVITY ASSUMPTION: sponsor authority is limited and each pre-authorization stage adds coordination.",), label),
    )


def motion_comparison() -> tuple[dict, dict]:
    rfp = load_formal_rfp_motion()
    from .formal_rfp import assess_formal_rfp
    rfp_result, pilot = assess_formal_rfp(rfp), assess_pilot()
    full_value = load_baseline().burden.annual_recoverable_value
    return ({"motion": "FORMAL_RFP", "acquisition_hours": rfp.journey.total_effort_hours,
             "cycle_days": rfp.journey.total_elapsed_days, "delivery_hours": rfp.engineering_hours,
             "revenue": rfp.implementation_price, "contribution": rfp_result.seller_economics.acquisition_adjusted_contribution,
             "value_addressed": full_value, "stakeholders": len(rfp.stakeholder_participation),
             "approval_stages": 4, "support": rfp.annual_support, "target": rfp_result.verdict,
             "rates": rfp.labor_rates},
            {"motion": "COOPERATIVE_PAID_PILOT", "acquisition_hours": pilot.economics.acquisition_hours,
             "cycle_days": pilot.economics.authorization_days, "delivery_hours": pilot.motion.engineering_hours,
             "revenue": pilot.motion.pilot_price, "contribution": pilot.economics.seller.acquisition_adjusted_contribution,
             "value_addressed": pilot.motion.annualized_value_potentially_affected,
             "stakeholders": len(pilot.motion.stakeholders), "approval_stages": 3,
             "support": pilot.motion.pilot_period_support, "target": pilot.verdict,
             "rates": pilot.motion.labor_rates})
