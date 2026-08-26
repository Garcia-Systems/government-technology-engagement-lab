"""Chapter 13: deterministic access feasibility and responsible fallbacks."""

from dataclasses import dataclass
from decimal import Decimal
from enum import IntEnum, StrEnum

from .baseline import _fixture
from .configuration import assess_configuration_first
from .evidence import EvidenceLabel, parse_evidence_label
from .formal_rfp import load_formal_rfp_motion
from .governance import governance_scenarios
from .models import GateStatus, WorkCategory


class AccessMode(StrEnum):
    FULL_SUPPORTED_API = "FULL_SUPPORTED_API"
    READ_ONLY_API = "READ_ONLY_API"
    APPROVED_EXPORT = "APPROVED_EXPORT"
    MANUAL_EXPORT = "MANUAL_EXPORT"
    VENDOR_MANAGED_INTERFACE = "VENDOR_MANAGED_INTERFACE"
    NO_SUPPORTED_ACCESS = "NO_SUPPORTED_ACCESS"


class Freshness(IntEnum):
    ON_DEMAND_MANUAL = 0
    WEEKLY = 1
    DAILY = 2
    REAL_TIME = 3


class Completeness(StrEnum):
    COMPLETE = "COMPLETE"
    PARTIAL = "PARTIAL"
    INSUFFICIENT = "INSUFFICIENT"


class Feasibility(StrEnum):
    FEASIBLE = "FEASIBLE"
    FEASIBLE_WITH_LIMITATIONS = "FEASIBLE_WITH_LIMITATIONS"
    NOT_FEASIBLE = "NOT_FEASIBLE"


@dataclass(frozen=True)
class AccessCapability:
    mode: AccessMode
    reliability: str
    frequency: Freshness
    write_capability: bool
    completeness: Completeness
    automation_compatible: bool
    vendor_support: str
    fields: frozenset[str]
    limitations: tuple[str, ...]
    evidence: EvidenceLabel


@dataclass(frozen=True)
class AccessRequirement:
    identifier: str
    name: str
    acceptable_modes: tuple[AccessMode, ...]
    requires_write: bool
    requires_automation: bool
    required_fields: frozenset[str]
    minimum_freshness: Freshness


@dataclass(frozen=True)
class FeasibilityResult:
    status: Feasibility
    reasons: tuple[str, ...]
    capability: AccessCapability | None


@dataclass(frozen=True)
class ClosedScenario:
    key: str
    name: str
    capabilities: tuple[AccessCapability, ...]
    native_configuration_available: bool
    value_fraction: Decimal
    implementation_price: Decimal
    annual_support: Decimal
    engineering_hours: int
    acquisition_hours: int
    support_hours: int
    exports_per_year: int
    staff_minutes_per_export: int
    evidence: EvidenceLabel


@dataclass(frozen=True)
class ClosedEconomics:
    value_addressed: Decimal
    value_lost: Decimal
    first_year_cost: Decimal
    customer_net_value: Decimal
    delivery_cost: Decimal
    acquisition_cost: Decimal
    support_cost: Decimal
    seller_contribution: Decimal
    annual_manual_hours: Decimal


@dataclass(frozen=True)
class ClosedAssessment:
    scenario: ClosedScenario
    preferred: AccessRequirement
    preferred_feasibility: FeasibilityResult
    fallback_ladder: tuple[str, ...]
    selected_fallback: AccessRequirement | None
    fallback_feasibility: FeasibilityResult | None
    economics: ClosedEconomics | None
    governance_surface: str | None
    governance_implications: tuple[str, ...]
    project_viability: GateStatus
    target_viability: GateStatus
    verdict: str
    evidence: EvidenceLabel = EvidenceLabel.OBSERVED_LAB_RESULT


def load_closed_fixture() -> dict:
    return _fixture("closed_integration.json")


def intervention_requirements() -> tuple[AccessRequirement, ...]:
    return tuple(AccessRequirement(x["id"], x["name"], tuple(AccessMode(v) for v in x["acceptable_modes"]),
        x["requires_write"], x["requires_automation"], frozenset(x["required_fields"]), Freshness[x["minimum_freshness"]])
        for x in load_closed_fixture()["interventions"])


def load_closed_scenarios() -> tuple[ClosedScenario, ...]:
    raw = load_closed_fixture()
    result = []
    for item in raw["scenarios"]:
        evidence = parse_evidence_label(item["evidence"])
        caps = tuple(AccessCapability(AccessMode(x["mode"]), x["reliability"], Freshness[x["frequency"]],
            x["write_capability"], Completeness(x["completeness"]), x["automation_compatible"],
            x["vendor_support"], frozenset(x["fields"]), tuple(x["limitations"]), evidence)
            for x in item["capabilities"])
        result.append(ClosedScenario(item["key"], item["name"], caps, item["native_configuration_available"],
            Decimal(item.get("value_fraction", "0")), Decimal(item.get("implementation_price", "0")),
            Decimal(item.get("annual_support", "0")), item.get("engineering_hours", 0),
            item.get("acquisition_hours", 0), item.get("support_hours", 0), item.get("exports_per_year", 0),
            item.get("staff_minutes_per_export", 0), evidence))
    return tuple(result)


def evaluate_access(requirement: AccessRequirement, capabilities: tuple[AccessCapability, ...], native=False) -> FeasibilityResult:
    if requirement.identifier == "NATIVE_CONFIGURATION":
        return FeasibilityResult(Feasibility.FEASIBLE if native else Feasibility.NOT_FEASIBLE,
            ("NATIVE_CAPABILITY_AVAILABLE",) if native else ("NATIVE_CAPABILITY_INADEQUATE",), None)
    candidates = tuple(c for c in capabilities if c.mode in requirement.acceptable_modes)
    if not candidates:
        reason = "REQUIRED_WRITE_ACCESS_UNAVAILABLE" if requirement.requires_write else "SUPPORTED_INTERFACE_UNAVAILABLE"
        return FeasibilityResult(Feasibility.NOT_FEASIBLE, (reason,), None)
    cap = candidates[0]
    reasons = []
    if requirement.requires_write and not cap.write_capability: reasons.append("REQUIRED_WRITE_ACCESS_UNAVAILABLE")
    if requirement.requires_automation and not cap.automation_compatible: reasons.append("AUTOMATION_COMPATIBILITY_UNAVAILABLE")
    missing = requirement.required_fields - cap.fields
    if missing: reasons.append("REQUIRED_FIELDS_MISSING:" + ",".join(sorted(missing)))
    if cap.completeness is Completeness.INSUFFICIENT: reasons.append("DATA_FIELDS_INSUFFICIENT")
    if reasons: return FeasibilityResult(Feasibility.NOT_FEASIBLE, tuple(reasons), cap)
    limitations = list(cap.limitations)
    if cap.frequency < requirement.minimum_freshness: limitations.append("EXPORT_FREQUENCY_LIMITED")
    if cap.mode is AccessMode.MANUAL_EXPORT: limitations.append("MANUAL_REFRESH_REQUIRED")
    status = Feasibility.FEASIBLE_WITH_LIMITATIONS if limitations else Feasibility.FEASIBLE
    return FeasibilityResult(status, tuple(dict.fromkeys(limitations or ("REQUIRED_ACCESS_AVAILABLE",))), cap)


def _economics(s: ClosedScenario) -> ClosedEconomics:
    baseline = Decimal(load_closed_fixture()["baseline_recoverable_value"])
    value = baseline * s.value_fraction
    rates = {x.category: x.hourly_cost for x in load_formal_rfp_motion().labor_rates}
    delivery = Decimal(s.engineering_hours) * rates[WorkCategory.ENGINEERING]
    acquisition = Decimal(s.acquisition_hours) * rates[WorkCategory.SALES]
    support = Decimal(s.support_hours) * rates[WorkCategory.ENGINEERING]
    cost = s.implementation_price + s.annual_support
    manual = Decimal(s.exports_per_year * s.staff_minutes_per_export) / Decimal(60)
    return ClosedEconomics(value, baseline - value, cost, value - cost, delivery, acquisition, support,
        s.implementation_price - delivery - acquisition, manual)


def assess_closed_scenario(scenario: ClosedScenario) -> ClosedAssessment:
    reqs = {x.identifier: x for x in intervention_requirements()}
    preferred = reqs["BROAD_WRITE_INTEGRATION"]
    preferred_result = evaluate_access(preferred, scenario.capabilities, scenario.native_configuration_available)
    ladder = tuple(load_closed_fixture()["fallback_precedence"])
    order = ("NATIVE_CONFIGURATION", "READ_ONLY_EDGE", "MANUAL_ASSISTED_VIEW")
    selected = None; selected_result = None
    for key in order:
        result = evaluate_access(reqs[key], scenario.capabilities, scenario.native_configuration_available)
        if result.status is not Feasibility.NOT_FEASIBLE:
            selected, selected_result = reqs[key], result
            break
    if selected is None:
        return ClosedAssessment(scenario, preferred, preferred_result, ladder, None, None, None, None, (),
            GateStatus.FAIL, GateStatus.NOT_EVALUATED, "NO DEAL")
    if selected.identifier == "NATIVE_CONFIGURATION":
        config = assess_configuration_first(); ce = config.economics
        econ = ClosedEconomics(ce.value_addressed, ce.residual_value, ce.first_year_cost,
            ce.net_first_year_recoverable_value, ce.seller.delivery_labor_cost,
            ce.seller.acquisition_labor_cost, Decimal(), ce.seller.acquisition_adjusted_contribution, Decimal())
        project, target, verdict = config.project_viability, config.target_viability, "CONFIGURE / BUY"
        surface = "CONFIGURATION_FIRST"
    else:
        econ = _economics(scenario)
        project = GateStatus.PASS if econ.customer_net_value >= 0 and s_support_viable(scenario, econ) else GateStatus.FAIL
        target = GateStatus.PASS if project is GateStatus.PASS and econ.seller_contribution >= Decimal("10000") else GateStatus.FAIL
        verdict = "NO DEAL" if project is GateStatus.FAIL else ("NARROW CUSTOM EDGE" if target is GateStatus.PASS else "INVESTIGATE")
        surface = "READ_ONLY"
    gov = next(x for x in governance_scenarios() if x.key == surface)
    implications = tuple(x.identifier for x in gov.work_items)
    if selected.identifier == "MANUAL_ASSISTED_VIEW":
        implications += ("AUTHORIZED_HUMAN_HANDLING", "TRANSFER_CONTROLS", "FILE_RETENTION", "DATA_PROVENANCE")
    return ClosedAssessment(scenario, preferred, preferred_result, ladder, selected, selected_result, econ,
        surface, implications, project, target, verdict)


def s_support_viable(scenario: ClosedScenario, economics: ClosedEconomics) -> bool:
    return scenario.annual_support >= economics.support_cost


def closed_integration_scenarios() -> tuple[ClosedAssessment, ...]:
    return tuple(assess_closed_scenario(x) for x in load_closed_scenarios())


def assess_closed_integration() -> ClosedAssessment:
    """Baseline opportunity: preferred write project fails, approved export fallback is selected."""
    return closed_integration_scenarios()[1]
