from government_engagement_lab.baseline import assess_baseline, load_baseline, load_scenarios
from government_engagement_lab.models import FindingCode, GateStatus


def test_fixture_identity_workflow_and_engagement_inputs() -> None:
    case = load_baseline()
    assert case.customer.name == "James River County Permitting Department"
    assert case.customer.staff_count == 32
    assert "Wholly fictional" in case.customer.fiction_notice
    assert "James City County" in case.customer.fiction_notice
    assert case.workflow == (
        "Application", "Intake", "Validation", "Department Review",
        "Corrections / Resubmission", "Approval", "Status / Record", "Reporting",
    )
    assert case.economics.engineering_hours == 522
    assert case.economics.solutions_sales_hours == 192
    assert case.economics.sales_cycle_months == 9


def test_assessment_keeps_project_gates_separate_from_target_gate() -> None:
    assessment = assess_baseline(load_baseline())
    gates = {gate.name: gate.status for gate in assessment.gates}
    assert gates == {
        "Problem attractiveness": GateStatus.PASS,
        "Technical feasibility": GateStatus.PASS,
        "Customer economics": GateStatus.PASS,
        "Delivery economics": GateStatus.PASS,
        "Support viability": GateStatus.PASS,
        "Target attractiveness": GateStatus.FAIL,
    }
    assert assessment.verdict == "POOR TARGET CUSTOMER"
    assert set(assessment.findings) == set(FindingCode)


def test_verdict_uses_explicit_findings_without_weighted_score() -> None:
    assessment = assess_baseline(load_baseline())
    assert assessment.findings
    assert not hasattr(assessment, "score")
    assert not hasattr(load_baseline(), "government_score")


def test_historical_scenario_verdicts_load() -> None:
    scenarios = {scenario.name: scenario.verdict for scenario in load_scenarios()}
    assert scenarios == {
        "Baseline": "POOR TARGET CUSTOMER",
        "Cooperative pilot": "PROMISING — VALIDATE IN DISCOVERY",
        "Formal RFP": "POOR TARGET CUSTOMER",
        "Higher contract value": "POOR TARGET CUSTOMER",
        "Closed legacy integration": "NO DEAL",
        "Existing vendor module": "BUY / CONFIGURE",
        "Reusable technology + hard sales": "POOR TARGET CUSTOMER",
    }
