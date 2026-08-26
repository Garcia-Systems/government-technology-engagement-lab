"""Chapter 11: isolate a wholly fictional existing purchasing path."""

from dataclasses import replace
from decimal import Decimal

from .baseline import _fixture, load_baseline
from .economics import calculate_customer_economics
from .evidence import EvidenceLabel, parse_evidence_label
from .formal_rfp import assess_formal_rfp, load_formal_rfp_motion
from .gates import determine_verdict
from .models import (
    AcquisitionAttribution, DirectAccess, EngagementJourney, EngagementMotion,
    EngagementStage, ExistingPathAssessment, ExistingPathEconomics,
    ExistingPathMotion, FindingCode, GateStatus, MotionStakeholderParticipation,
    PurchasingMechanism, SellerEconomics, StageChange, StageType, WorkCategory,
)
from .stakeholders import load_baseline_topology

_BUCKETS = {
    "OPPORTUNITY_DISCOVERY": "BUYER ACCESS / QUALIFICATION", "GO_NO_GO": "BUYER ACCESS / QUALIFICATION",
    "REQUIREMENTS_INTERPRETATION": "TECHNICAL DISCOVERY", "SOLUTION_DESIGN": "TECHNICAL DISCOVERY",
    "TECHNICAL_RESPONSE": "TECHNICAL DISCOVERY", "SECURITY_ACCESS_RESPONSE": "GOVERNANCE / SECURITY",
    "ACCESSIBILITY_RESPONSE": "GOVERNANCE / SECURITY", "SOLICITATION_REVIEW": "PROCUREMENT",
    "SUBMISSION": "PROCUREMENT", "CLARIFICATIONS_MEETINGS": "PROCUREMENT",
    "EVALUATION_WAIT": "PROCUREMENT", "INTENT_SELECTION": "PROCUREMENT",
    "PROCUREMENT_COORDINATION": "PROCUREMENT", "PRICING": "PROPOSAL",
    "PROPOSAL_ASSEMBLY": "PROPOSAL", "CONTRACT_REVIEW": "CONTRACTING",
    "IMPLEMENTATION_PLANNING": "IMPLEMENTATION PLANNING", "AUTHORIZATION": "IMPLEMENTATION PLANNING",
}


def load_existing_path_motion() -> ExistingPathMotion:
    raw = _fixture("existing_purchasing_path.json")
    evidence = parse_evidence_label(raw["evidence"])
    mechanism = PurchasingMechanism(
        raw["identifier"], raw["name"], raw["description"], raw["provider_holder"], raw["fictional"],
        raw["fiction_notice"], raw["seller_eligibility"], tuple(raw["covered_service_categories"]),
        raw["pricing_mechanism"], raw["statement_of_work_required"], raw["additional_competition_required"],
        raw["contract_negotiation_required"], raw["standard_terms_established"],
        raw["invoicing_path_established"], raw["procurement_coordination_required"],
        tuple(raw["pre_established"]), tuple(raw["customer_approvals_still_required"]),
        tuple(raw["assumptions_limitations"]), evidence,
    )
    stages = tuple(EngagementStage(
        x[0], x[1], f"Existing-path project work: {x[1].lower()}.", x[2], True, x[3], x[4],
        WorkCategory(x[5]), StageType(x[6]), evidence,
        ("Fictional stage allocation; not a real procurement requirement.",),
    ) for x in raw["stages"])
    formal = load_formal_rfp_motion()
    current = {s.identifier: s for s in stages}
    reasons = {
        "SOLICITATION_REVIEW": "Removed: the alternative assumption says no new solicitation is required.",
        "PROPOSAL_ASSEMBLY": "Removed: a project SOW replaces the full proposal package.",
        "SUBMISSION": "Removed: no competitive-response submission is modeled.",
        "CLARIFICATIONS_MEETINGS": "Removed: solicitation clarifications are not needed.",
        "EVALUATION_WAIT": "Removed: no competitive evaluation wait is modeled.",
        "INTENT_SELECTION": "Removed: seller eligibility is already established; project approval remains.",
        "TECHNICAL_RESPONSE": "Reduced: project technical documentation remains but the full response package does not.",
        "PRICING": "Reduced: only project-specific fixed pricing remains.",
        "CONTRACT_REVIEW": "Reduced: general terms exist but project-specific SOW review remains.",
        "PROCUREMENT_COORDINATION": "Reduced: the invoicing and vendor path exist but work-order coordination remains.",
    }
    changes = tuple(StageChange(s.identifier, s.effort_hours, current.get(s.identifier, _zero(s)).effort_hours,
        s.elapsed_days, current.get(s.identifier, _zero(s)).elapsed_days,
        reasons[s.identifier], evidence) for s in formal.journey.stages if s.identifier in reasons)
    journey = EngagementJourney(f'{raw["motion_identifier"]}_JOURNEY', raw["motion_name"], raw["description"],
        formal.journey.customer_name, EngagementMotion.EXISTING_PURCHASING_PATH, stages,
        formal.journey.modeled_days_per_month, evidence)
    motion = ExistingPathMotion(raw["motion_identifier"], raw["motion_name"], mechanism, journey,
        tuple(MotionStakeholderParticipation(x[0], x[1], x[2], evidence) for x in raw["stakeholder_participation"]),
        changes, DirectAccess(raw["buyer_access"]), formal.implementation_price, formal.annual_support,
        formal.engineering_hours, formal.labor_rates, formal.minimum_contribution, evidence)
    validate_existing_path_motion(motion)
    return motion


def _zero(stage: EngagementStage) -> EngagementStage:
    return replace(stage, effort_hours=0, elapsed_days=0)


def validate_existing_path_motion(motion: ExistingPathMotion) -> None:
    formal = load_formal_rfp_motion()
    valid = {s.identifier for s in formal.journey.stages}
    people = {s.identifier for s in load_baseline_topology().stakeholders}
    m = motion.mechanism
    if not m.fictional or m.evidence is not EvidenceLabel.MODELED_ALTERNATIVE_ASSUMPTION:
        raise ValueError("purchasing mechanism must be explicitly fictional and alternative-assumption labeled")
    if not m.covered_service_categories or not m.seller_eligibility or not m.pre_established:
        raise ValueError("coverage, eligibility, and pre-established terms must be explicit")
    if not m.customer_approvals_still_required or not m.statement_of_work_required:
        raise ValueError("project-specific approval and statement of work must remain")
    ids = [s.identifier for s in motion.journey.stages]
    if len(ids) != len(set(ids)) or set(ids) - valid:
        raise ValueError("existing path must reuse unique Chapter 2/4 journey stage identifiers")
    if any(x.stage_id not in ids or x.stakeholder_id not in people for x in motion.stakeholder_participation):
        raise ValueError("existing-path stakeholder reference is invalid")
    if motion.engineering_hours != formal.engineering_hours or motion.implementation_price != formal.implementation_price:
        raise ValueError("primary comparison must hold delivery scope and customer price constant")


def _seller_economics(motion: ExistingPathMotion) -> SellerEconomics:
    rates = {r.category: r.hourly_cost for r in motion.labor_rates}
    delivery = Decimal(motion.engineering_hours) * rates[WorkCategory.ENGINEERING]
    acquisition = sum((Decimal(s.effort_hours) * rates[s.responsible_category] for s in motion.journey.stages), Decimal())
    contribution = motion.implementation_price - delivery - acquisition
    return SellerEconomics(motion.implementation_price, delivery, acquisition, Decimal(), contribution,
        contribution / motion.implementation_price, EvidenceLabel.OBSERVED_LAB_RESULT)


def acquisition_attribution(motion: ExistingPathMotion) -> tuple[AcquisitionAttribution, ...]:
    formal = load_formal_rfp_motion(); current = {s.identifier: s.effort_hours for s in motion.journey.stages}
    names = tuple(dict.fromkeys(_BUCKETS.values()))
    return tuple(AcquisitionAttribution(name,
        sum(s.effort_hours for s in formal.journey.stages if _BUCKETS[s.identifier] == name),
        sum(current.get(s.identifier, 0) for s in formal.journey.stages if _BUCKETS[s.identifier] == name)) for name in names)


def assess_existing_path(motion: ExistingPathMotion | None = None, *, key: str = "BASELINE",
                         changed_assumptions: tuple[str, ...] = ()) -> ExistingPathAssessment:
    motion = motion or load_existing_path_motion(); formal = assess_formal_rfp(); seller = _seller_economics(motion)
    hours = motion.journey.total_effort_hours
    economics = ExistingPathEconomics(seller, hours, formal.motion.journey.total_effort_hours-hours,
        formal.seller_economics.acquisition_labor_cost-seller.acquisition_labor_cost,
        motion.journey.total_elapsed_days, formal.motion.journey.total_elapsed_days-motion.journey.total_elapsed_days,
        seller.acquisition_labor_cost/motion.implementation_price, Decimal(hours)/motion.implementation_price*Decimal(10000),
        EvidenceLabel.OBSERVED_LAB_RESULT)
    baseline = load_baseline()
    customer = calculate_customer_economics(replace(baseline, economics=replace(baseline.economics,
        implementation_price=motion.implementation_price, annual_support=motion.annual_support,
        engineering_hours=motion.engineering_hours)))
    findings = [FindingCode.STANDARD_TERMS_ALREADY_ESTABLISHED, FindingCode.REDUCED_PROCUREMENT_COORDINATION,
        FindingCode.REDUCED_PROPOSAL_ADMINISTRATION, FindingCode.REDUCED_CONTRACT_SETUP,
        FindingCode.SHORTER_ELAPSED_APPROVAL_PATH, FindingCode.PROJECT_SPECIFIC_APPROVAL_STILL_REQUIRED,
        FindingCode.SECURITY_REVIEW_STILL_REQUIRED, FindingCode.TECHNICAL_VALIDATION_STILL_REQUIRED]
    if motion.buyer_access is not DirectAccess.YES: findings.append(FindingCode.BUYER_ACCESS_STILL_LIMITED)
    project = GateStatus.PASS
    meaningful = economics.acquisition_hours_saved >= 60 and seller.acquisition_adjusted_contribution >= motion.minimum_contribution
    target = GateStatus.PASS if meaningful and motion.buyer_access is DirectAccess.YES else GateStatus.CONDITIONAL
    if motion.buyer_access is DirectAccess.NO or economics.acquisition_hours_saved < 30: target = GateStatus.FAIL
    return ExistingPathAssessment(key, motion, customer, economics, acquisition_attribution(motion), tuple(findings),
        project, target, determine_verdict(project, target), changed_assumptions)


def existing_path_scenarios() -> tuple[ExistingPathAssessment, ...]:
    base = load_existing_path_motion(); formal = load_formal_rfp_motion(); formal_by = {s.identifier:s for s in formal.journey.stages}
    weak = replace(base, identifier="JAMES_RIVER_EXISTING_PATH_WEAK_ACCESS", buyer_access=DirectAccess.NO,
        evidence=EvidenceLabel.SENSITIVITY_ASSUMPTION)
    # Nominal path restores most proposal/procurement work, while retaining the same technical scope.
    restore = {"SOLICITATION_REVIEW", "PROPOSAL_ASSEMBLY", "SUBMISSION", "CLARIFICATIONS_MEETINGS", "CONTRACT_REVIEW", "PROCUREMENT_COORDINATION"}
    nominal_stages = list(base.journey.stages)
    for sid in restore:
        source=formal_by[sid]
        nominal_stages.append(replace(source, sequence=len(nominal_stages)+1, evidence=EvidenceLabel.SENSITIVITY_ASSUMPTION)) if sid not in {s.identifier for s in nominal_stages} else None
    nominal = replace(base, identifier="JAMES_RIVER_NOMINAL_EXISTING_PATH",
        journey=replace(base.journey, stages=tuple(nominal_stages), evidence=EvidenceLabel.SENSITIVITY_ASSUMPTION),
        evidence=EvidenceLabel.SENSITIVITY_ASSUMPTION)
    strong_remove={"OPPORTUNITY_DISCOVERY", "GO_NO_GO", "TECHNICAL_RESPONSE", "PRICING", "CONTRACT_REVIEW", "PROCUREMENT_COORDINATION"}
    strong_stages=tuple(replace(s, effort_hours=(max(1, s.effort_hours//4) if s.identifier in strong_remove else s.effort_hours),
        elapsed_days=(max(1, s.elapsed_days//4) if s.identifier in strong_remove else s.elapsed_days), evidence=EvidenceLabel.SENSITIVITY_ASSUMPTION) for s in base.journey.stages)
    strong=replace(base, identifier="JAMES_RIVER_STRONG_EXISTING_PATH", buyer_access=DirectAccess.YES,
        journey=replace(base.journey, stages=strong_stages, evidence=EvidenceLabel.SENSITIVITY_ASSUMPTION), evidence=EvidenceLabel.SENSITIVITY_ASSUMPTION)
    return (assess_existing_path(base), assess_existing_path(weak, key="WEAK_BUYER_ACCESS", changed_assumptions=("Sponsor access changes from LIMITED to NO; procurement savings remain.",)),
        assess_existing_path(nominal, key="NOMINAL_PATH", changed_assumptions=("Full proposal and substantial procurement/contract work return.",)),
        assess_existing_path(strong, key="STRONG_PATH", changed_assumptions=("More commercial setup is removed and credible access is assumed; governance remains.",)))


def rfp_vs_existing_path():
    return assess_formal_rfp(), assess_existing_path()
