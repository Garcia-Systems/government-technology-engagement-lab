from decimal import Decimal

from government_engagement_lab.baseline import load_baseline, load_scenarios
from government_engagement_lab.evidence import EvidenceLabel
from government_engagement_lab.gates import (
    PROJECT_DIMENSIONS,
    aggregate_viability,
    baseline_gate_assessment,
    determine_verdict,
    gate_scenarios,
)
from government_engagement_lab.models import GateDimension, GateStatus


def test_all_dimensions_and_status_vocabulary_are_explicit() -> None:
    assessment = baseline_gate_assessment()
    assert {gate.dimension for gate in assessment.gates} == set(GateDimension)
    assert PROJECT_DIMENSIONS == tuple(GateDimension)[:5]
    assert {status.value for status in GateStatus} == {"PASS", "FAIL", "CONDITIONAL", "NOT_EVALUATED"}
    assert not hasattr(assessment, "score")
    assert not hasattr(assessment, "government_score")


def test_unresolved_gate_produces_investigation_not_false_certainty() -> None:
    viability = aggregate_viability((GateStatus.PASS, GateStatus.CONDITIONAL))
    assert viability is GateStatus.CONDITIONAL
    assert determine_verdict(viability, GateStatus.PASS) == "INVESTIGATE"
    assert determine_verdict(GateStatus.PASS, GateStatus.NOT_EVALUATED) == "INVESTIGATE"


def test_baseline_separates_project_and_target_viability() -> None:
    assessment = baseline_gate_assessment()
    expected = {
        GateDimension.PROBLEM_ATTRACTIVENESS: GateStatus.PASS,
        GateDimension.TECHNICAL_FEASIBILITY: GateStatus.PASS,
        GateDimension.CUSTOMER_ECONOMICS: GateStatus.PASS,
        GateDimension.DELIVERY_ECONOMICS: GateStatus.PASS,
        GateDimension.SUPPORT_ECONOMICS: GateStatus.PASS,
        GateDimension.TARGET_ATTRACTIVENESS: GateStatus.FAIL,
    }
    assert {gate.dimension: gate.status for gate in assessment.gates} == expected
    assert assessment.project_viability is GateStatus.PASS
    assert assessment.target_viability is GateStatus.FAIL
    assert assessment.verdict == "POOR TARGET CUSTOMER"
    target = assessment.gate(GateDimension.TARGET_ATTRACTIVENESS)
    assert len(target.reasons) == 5
    assert all(reason.explanation and reason.code for reason in target.reasons)


def test_customer_gate_exposes_the_transparent_lab_rule_and_economics() -> None:
    gate = baseline_gate_assessment().gate(GateDimension.CUSTOMER_ECONOMICS)
    assert "MODELED ASSUMPTION" in gate.explanation
    detail = gate.reasons[0].explanation
    for value in ("$104,002.80", "$102,000.00", "$2,002.80", "9.00 months"):
        assert value in detail


def test_gate_counterfactuals_apply_precedence_and_label_changes() -> None:
    scenarios = {scenario.key: scenario for scenario in gate_scenarios()}
    technical = scenarios["technical_failure"]
    assert technical.assessment.gate(GateDimension.TECHNICAL_FEASIBILITY).status is GateStatus.FAIL
    assert technical.assessment.project_viability is GateStatus.FAIL
    assert technical.assessment.verdict == "NO DEAL"

    economics = scenarios["customer_economics_failure"]
    assert economics.assessment.gate(GateDimension.CUSTOMER_ECONOMICS).status is GateStatus.FAIL
    assert economics.assessment.project_viability is GateStatus.FAIL
    assert economics.assessment.verdict == "NO DEAL"

    repaired = scenarios["target_repaired"]
    assert repaired.assessment.project_viability is GateStatus.PASS
    assert repaired.assessment.target_viability is GateStatus.PASS
    assert repaired.assessment.verdict == "PROMISING — VALIDATE IN DISCOVERY"
    assert repaired.assessment.verdict != "POOR TARGET CUSTOMER"

    changes = [change for scenario in scenarios.values() for change in scenario.changed_assumptions]
    assert changes
    assert all(change.evidence is EvidenceLabel.SENSITIVITY_ASSUMPTION for change in changes)


def test_counterfactuals_do_not_mutate_chapter_zero_inputs_or_fixtures() -> None:
    gate_scenarios()
    case = load_baseline()
    assert case.burden.annual_recoverable_value == Decimal("104002.80")
    assert case.economics.implementation_price == Decimal("78000.00")
    assert case.economics.annual_support == Decimal("24000.00")
    assert case.economics.engineering_hours == 522
    assert len(load_scenarios()) == 7
