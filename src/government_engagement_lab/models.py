"""Typed Chapter 0 domain model; no government-wide scoring model is used."""

from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum

from .evidence import EvidenceLabel


class GateStatus(StrEnum):
    PASS = "PASS"
    FAIL = "FAIL"


class FindingCode(StrEnum):
    PROCUREMENT_DIFFICULTY = "PROCUREMENT_DIFFICULTY"
    STAKEHOLDER_FRICTION = "STAKEHOLDER_FRICTION"
    WEAK_BUYER_ACCESS = "WEAK_BUYER_ACCESS"
    LONG_SALES_CYCLE = "LONG_SALES_CYCLE"
    HIGH_SOLUTIONS_EFFORT = "HIGH_SOLUTIONS_EFFORT"


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
