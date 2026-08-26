"""Fixture loading and explicit, mechanism-based Chapter 0 assessment."""

import json
from decimal import Decimal
from importlib.resources import files

from .evidence import EvidenceLabel, parse_evidence_label
from .models import (
    Assessment, BaselineCase, Burden, Conditions, Customer, EngagementEconomics,
    FindingCode, GateResult, GateStatus, Scenario,
)


def _fixture(name: str) -> dict | list:
    path = files("government_engagement_lab").joinpath("fixtures", name)
    return json.loads(path.read_text(encoding="utf-8"))


def load_baseline() -> BaselineCase:
    raw = _fixture("baseline_case.json")
    return BaselineCase(
        customer=Customer(**raw["customer"]),
        workflow=tuple(raw["workflow"]),
        operational_problems=tuple(raw["operational_problems"]),
        intervention_boundary=raw["intervention_boundary"],
        burden=Burden(
            annual_current_state=Decimal(raw["burden"]["annual_current_state"]),
            annual_recoverable_value=Decimal(raw["burden"]["annual_recoverable_value"]),
        ),
        economics=EngagementEconomics(
            implementation_price=Decimal(raw["economics"]["implementation_price"]),
            annual_support=Decimal(raw["economics"]["annual_support"]),
            engineering_hours=raw["economics"]["engineering_hours"],
            solutions_sales_hours=raw["economics"]["solutions_sales_hours"],
            sales_cycle_months=raw["economics"]["sales_cycle_months"],
        ),
        conditions=Conditions(**raw["conditions"]),
        evidence=parse_evidence_label(raw["evidence"]),
    )


def load_scenarios() -> tuple[Scenario, ...]:
    return tuple(
        Scenario(item["name"], item["verdict"], parse_evidence_label(item["evidence"]))
        for item in _fixture("cookbook_scenarios.json")
    )


def assess_baseline(case: BaselineCase) -> Assessment:
    """Apply visible gates and findings, never an arbitrary weighted score."""
    conditions = case.conditions
    findings = tuple(code for code, active in (
        (FindingCode.PROCUREMENT_DIFFICULTY, conditions.procurement_difficulty),
        (FindingCode.STAKEHOLDER_FRICTION, conditions.stakeholder_friction),
        (FindingCode.WEAK_BUYER_ACCESS, conditions.buyer_access == "weak"),
        (FindingCode.LONG_SALES_CYCLE, conditions.sales_cycle_burden),
        (FindingCode.HIGH_SOLUTIONS_EFFORT, conditions.solutions_effort_burden),
    ) if active)
    gates = (
        GateResult("Problem attractiveness", GateStatus.PASS),
        GateResult("Technical feasibility", GateStatus.PASS if conditions.technical_feasibility else GateStatus.FAIL),
        GateResult("Customer economics", GateStatus.PASS if conditions.customer_payback_viability else GateStatus.FAIL),
        GateResult("Delivery economics", GateStatus.PASS if conditions.delivery_viability else GateStatus.FAIL),
        GateResult("Support viability", GateStatus.PASS if conditions.support_viability else GateStatus.FAIL),
        GateResult("Target attractiveness", GateStatus.FAIL if findings else GateStatus.PASS),
    )
    verdict = "POOR TARGET CUSTOMER" if gates[-1].status is GateStatus.FAIL else "TARGET ATTRACTIVE"
    return Assessment(gates, findings, verdict, EvidenceLabel.OBSERVED_LAB_RESULT)
