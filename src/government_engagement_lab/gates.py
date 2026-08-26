"""Chapter 1 independent gate assessment and small counterfactuals."""

from dataclasses import replace
from decimal import Decimal

from .baseline import load_baseline
from .economics import CustomerEconomicsResult, calculate_customer_economics
from .evidence import EvidenceLabel
from .models import (
    BaselineCase,
    DimensionResult,
    EngagementMotion,
    FindingCode,
    GateAssessment,
    GateDimension,
    GateReason,
    GateScenario,
    GateStatus,
)
from .journey import load_baseline_journey

PROJECT_DIMENSIONS = (
    GateDimension.PROBLEM_ATTRACTIVENESS,
    GateDimension.TECHNICAL_FEASIBILITY,
    GateDimension.CUSTOMER_ECONOMICS,
    GateDimension.DELIVERY_ECONOMICS,
    GateDimension.SUPPORT_ECONOMICS,
)


def _reason(code: FindingCode, explanation: str, evidence: EvidenceLabel) -> GateReason:
    return GateReason(code, explanation, evidence)


def aggregate_viability(statuses: tuple[GateStatus, ...]) -> GateStatus:
    """Fail takes precedence; uncertainty is never silently promoted to pass."""
    if GateStatus.FAIL in statuses:
        return GateStatus.FAIL
    if GateStatus.CONDITIONAL in statuses:
        return GateStatus.CONDITIONAL
    if GateStatus.NOT_EVALUATED in statuses:
        return GateStatus.NOT_EVALUATED
    return GateStatus.PASS


def determine_verdict(project: GateStatus, target: GateStatus) -> str:
    """Chapter 1 precedence only; this is not the later capstone engine."""
    if project is GateStatus.FAIL:
        return "NO DEAL"
    if project is not GateStatus.PASS or target in (GateStatus.CONDITIONAL, GateStatus.NOT_EVALUATED):
        return "INVESTIGATE"
    if target is GateStatus.FAIL:
        return "POOR TARGET CUSTOMER"
    return "PROMISING — VALIDATE IN DISCOVERY"


def assess_gates(
    case: BaselineCase,
    *,
    technical_access_available: bool | None = None,
    target_conditions_improved: bool = False,
) -> GateAssessment:
    """Assess visible mechanisms without weights or a composite score.

    The modest fictional customer-economics lab rule is first-year net
    recoverable value >= 0. It is a MODELED ASSUMPTION, not a buying benchmark.
    """
    modeled = EvidenceLabel.MODELED_ASSUMPTION
    sensitivity = EvidenceLabel.SENSITIVITY_ASSUMPTION
    economics: CustomerEconomicsResult = calculate_customer_economics(case)
    access = case.conditions.technical_feasibility if technical_access_available is None else technical_access_available

    problem = DimensionResult(
        GateDimension.PROBLEM_ATTRACTIVENESS,
        GateStatus.PASS if case.burden.annual_recoverable_value > 0 else GateStatus.FAIL,
        (_reason(FindingCode.MEANINGFUL_ADMINISTRATIVE_BURDEN, "The fictional case supplies positive recoverable administrative value.", modeled),),
        "The modeled burden makes the bounded problem worth evaluating.",
    )
    technical = DimensionResult(
        GateDimension.TECHNICAL_FEASIBILITY,
        GateStatus.PASS if access else GateStatus.FAIL,
        (_reason(
            FindingCode.TECHNICALLY_FEASIBLE_BOUNDED_INTERVENTION if access else FindingCode.REQUIRED_ACCESS_UNAVAILABLE,
            "The workflow layer is feasible while existing systems remain authoritative." if access else "Required authoritative-system access is unavailable in this counterfactual.",
            modeled if technical_access_available is None else sensitivity,
        ),),
        "The bounded intervention can be delivered under modeled access assumptions." if access else "The intervention cannot operate without required access.",
    )
    customer_passes = economics.first_year_net_recoverable_value >= Decimal("0")
    customer = DimensionResult(
        GateDimension.CUSTOMER_ECONOMICS,
        GateStatus.PASS if customer_passes else GateStatus.FAIL,
        (_reason(
            FindingCode.CUSTOMER_VALUE_EXCEEDS_MODELED_COST if customer_passes else FindingCode.INSUFFICIENT_CUSTOMER_VALUE,
            f"Recoverable annual value ${case.burden.annual_recoverable_value:,.2f}; first-year cost ${economics.first_year_cost:,.2f}; net ${economics.first_year_net_recoverable_value:,.2f}; implementation-only payback {economics.implementation_only_payback_months:.2f} months.",
            modeled if case.evidence is modeled else case.evidence,
        ),),
        "MODELED ASSUMPTION rule: first-year net recoverable value must be nonnegative; this is not a universal purchasing benchmark.",
    )
    delivery = DimensionResult(
        GateDimension.DELIVERY_ECONOMICS,
        GateStatus.PASS if case.conditions.delivery_viability else GateStatus.FAIL,
        (_reason(FindingCode.DELIVERY_ASSUMPTION_VIABLE, f"Baseline treats {case.economics.engineering_hours} engineering hours as viable; seller labor rates are not supplied.", modeled),),
        "Viability is inherited, not a calculated contribution margin.",
    )
    support = DimensionResult(
        GateDimension.SUPPORT_ECONOMICS,
        GateStatus.PASS if case.conditions.support_viability else GateStatus.FAIL,
        (_reason(FindingCode.SUPPORT_ASSUMPTION_VIABLE, f"Baseline treats ${case.economics.annual_support:,.2f} annual support as viable; support delivery cost is not supplied.", modeled),),
        "Support remains a distinct modeled condition with an explicit evidence limit.",
    )
    target_codes = (
        (FindingCode.PROCUREMENT_DIFFICULTY, "procurement difficulty"),
        (FindingCode.STAKEHOLDER_FRICTION, "stakeholder friction"),
        (FindingCode.WEAK_BUYER_ACCESS, "weak buyer access"),
        (FindingCode.LONG_SALES_CYCLE, "long sales cycle"),
        (FindingCode.HIGH_SOLUTIONS_EFFORT, "high solutions effort"),
    )
    if target_conditions_improved:
        target_reasons = (_reason(FindingCode.TARGET_ACCESS_CONDITIONS_IMPROVED, "Hypothetical favorable acquisition conditions replace the baseline target impediments.", sensitivity),)
        target_status = GateStatus.PASS
    else:
        journey = load_baseline_journey()
        grounded = {
            FindingCode.LONG_SALES_CYCLE: f"long sales cycle traced to journey.total_elapsed_days = {journey.total_elapsed_days} modeled days ({journey.modeled_months} modeled months)",
            FindingCode.HIGH_SOLUTIONS_EFFORT: f"high solutions effort traced to journey.total_effort_hours = {journey.total_effort_hours} hours",
        }
        target_reasons = tuple(_reason(code, grounded.get(code, text), modeled) for code, text in target_codes)
        target_status = GateStatus.FAIL
    target = DimensionResult(
        GateDimension.TARGET_ATTRACTIVENESS,
        target_status,
        target_reasons,
        "Can the opportunity reasonably be reached, qualified, approved, contracted, and closed under this motion?",
    )
    gates = (problem, technical, customer, delivery, support, target)
    project_viability = aggregate_viability(tuple(g.status for g in gates if g.dimension in PROJECT_DIMENSIONS))
    target_viability = target.status
    return GateAssessment(
        gates,
        project_viability,
        target_viability,
        determine_verdict(project_viability, target_viability),
        EngagementMotion.BASELINE_COOKBOOK_MOTION,
    )


def baseline_gate_assessment() -> GateAssessment:
    return assess_gates(load_baseline())


def gate_scenarios() -> tuple[GateScenario, ...]:
    """Return only Chapter 1 gate substitutions, not later engagement experiments."""
    baseline = load_baseline()
    lower_value = replace(
        baseline,
        burden=replace(baseline.burden, annual_recoverable_value=Decimal("50000.00")),
        evidence=EvidenceLabel.SENSITIVITY_ASSUMPTION,
    )
    technical_change = _reason(FindingCode.REQUIRED_ACCESS_UNAVAILABLE, "Required authoritative-system access is unavailable.", EvidenceLabel.SENSITIVITY_ASSUMPTION)
    economics_change = _reason(FindingCode.INSUFFICIENT_CUSTOMER_VALUE, "Recoverable annual value changes from $104,002.80 to $50,000.00 while first-year cost stays $102,000.00.", EvidenceLabel.SENSITIVITY_ASSUMPTION)
    target_change = _reason(FindingCode.TARGET_ACCESS_CONDITIONS_IMPROVED, "Hypothetical favorable acquisition conditions replace baseline impediments.", EvidenceLabel.SENSITIVITY_ASSUMPTION)
    return (
        GateScenario("baseline", "Baseline", assess_gates(baseline)),
        GateScenario("technical_failure", "Technical failure", assess_gates(baseline, technical_access_available=False), (technical_change,)),
        GateScenario("customer_economics_failure", "Customer economics fail", assess_gates(lower_value), (economics_change,)),
        GateScenario("target_repaired", "Target repaired", assess_gates(baseline, target_conditions_improved=True), (target_change,)),
    )
