"""Typed domain records; no government-wide scoring model is used."""

from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum

from .evidence import EvidenceLabel


class GateStatus(StrEnum):
    PASS = "PASS"
    FAIL = "FAIL"
    CONDITIONAL = "CONDITIONAL"
    NOT_EVALUATED = "NOT_EVALUATED"


class GateDimension(StrEnum):
    PROBLEM_ATTRACTIVENESS = "PROBLEM_ATTRACTIVENESS"
    TECHNICAL_FEASIBILITY = "TECHNICAL_FEASIBILITY"
    CUSTOMER_ECONOMICS = "CUSTOMER_ECONOMICS"
    DELIVERY_ECONOMICS = "DELIVERY_ECONOMICS"
    SUPPORT_ECONOMICS = "SUPPORT_ECONOMICS"
    TARGET_ATTRACTIVENESS = "TARGET_ATTRACTIVENESS"


class EngagementMotion(StrEnum):
    """Context for an assessment, deliberately not a scored gate."""

    BASELINE_COOKBOOK_MOTION = "BASELINE_COOKBOOK_MOTION"


class FindingCode(StrEnum):
    MEANINGFUL_ADMINISTRATIVE_BURDEN = "MEANINGFUL_ADMINISTRATIVE_BURDEN"
    TECHNICALLY_FEASIBLE_BOUNDED_INTERVENTION = "TECHNICALLY_FEASIBLE_BOUNDED_INTERVENTION"
    CUSTOMER_VALUE_EXCEEDS_MODELED_COST = "CUSTOMER_VALUE_EXCEEDS_MODELED_COST"
    DELIVERY_ASSUMPTION_VIABLE = "DELIVERY_ASSUMPTION_VIABLE"
    SUPPORT_ASSUMPTION_VIABLE = "SUPPORT_ASSUMPTION_VIABLE"
    PROCUREMENT_DIFFICULTY = "PROCUREMENT_DIFFICULTY"
    STAKEHOLDER_FRICTION = "STAKEHOLDER_FRICTION"
    WEAK_BUYER_ACCESS = "WEAK_BUYER_ACCESS"
    LONG_SALES_CYCLE = "LONG_SALES_CYCLE"
    HIGH_SOLUTIONS_EFFORT = "HIGH_SOLUTIONS_EFFORT"
    REQUIRED_ACCESS_UNAVAILABLE = "REQUIRED_ACCESS_UNAVAILABLE"
    INSUFFICIENT_CUSTOMER_VALUE = "INSUFFICIENT_CUSTOMER_VALUE"
    TARGET_ACCESS_CONDITIONS_IMPROVED = "TARGET_ACCESS_CONDITIONS_IMPROVED"


@dataclass(frozen=True)
class Customer:
    name: str
    organization_type: str
    staff_count: int
    fiction_notice: str


@dataclass(frozen=True)
class Burden:
    annual_current_state: Decimal
    annual_recoverable_value: Decimal


@dataclass(frozen=True)
class EngagementEconomics:
    implementation_price: Decimal
    annual_support: Decimal
    engineering_hours: int
    solutions_sales_hours: int
    sales_cycle_months: int


@dataclass(frozen=True)
class Conditions:
    technical_feasibility: bool
    customer_payback_viability: bool
    delivery_viability: bool
    support_viability: bool
    procurement_difficulty: bool
    stakeholder_friction: bool
    buyer_access: str
    sales_cycle_burden: bool
    solutions_effort_burden: bool


@dataclass(frozen=True)
class BaselineCase:
    customer: Customer
    workflow: tuple[str, ...]
    operational_problems: tuple[str, ...]
    intervention_boundary: str
    burden: Burden
    economics: EngagementEconomics
    conditions: Conditions
    evidence: EvidenceLabel


@dataclass(frozen=True)
class Scenario:
    name: str
    verdict: str
    evidence: EvidenceLabel


@dataclass(frozen=True)
class GateResult:
    name: str
    status: GateStatus


@dataclass(frozen=True)
class Assessment:
    gates: tuple[GateResult, ...]
    findings: tuple[FindingCode, ...]
    verdict: str
    evidence: EvidenceLabel


@dataclass(frozen=True)
class GateReason:
    code: FindingCode
    explanation: str
    evidence: EvidenceLabel


@dataclass(frozen=True)
class DimensionResult:
    dimension: GateDimension
    status: GateStatus
    reasons: tuple[GateReason, ...]
    explanation: str


@dataclass(frozen=True)
class GateAssessment:
    gates: tuple[DimensionResult, ...]
    project_viability: GateStatus
    target_viability: GateStatus
    verdict: str
    engagement_motion: EngagementMotion
    evidence: EvidenceLabel = EvidenceLabel.OBSERVED_LAB_RESULT

    def gate(self, dimension: GateDimension) -> DimensionResult:
        return next(gate for gate in self.gates if gate.dimension is dimension)


@dataclass(frozen=True)
class GateScenario:
    key: str
    name: str
    assessment: GateAssessment
    changed_assumptions: tuple[GateReason, ...] = ()
