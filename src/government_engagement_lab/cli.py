"""Command-line interface for the executable chapters."""

import argparse
from decimal import Decimal

from .baseline import assess_baseline, load_baseline, load_scenarios
from .economics import calculate_customer_economics
from .gates import baseline_gate_assessment, gate_scenarios
from .models import GateDimension, GateStatus


def _money(value: Decimal) -> str:
    return f"${value:,.2f}"


def show_baseline() -> None:
    case = load_baseline()
    result = calculate_customer_economics(case)
    assessment = assess_baseline(case)
    print("CHAPTER 0 — THE POOR TARGET CUSTOMER HYPOTHESIS")
    print(f"FICTION NOTICE: {case.customer.fiction_notice}")
    print("No statement here is evidence about any real government or Virginia locality.\n")
    print(f"[{case.evidence}] Customer: {case.customer.name} ({case.customer.organization_type}; approximately {case.customer.staff_count} staff)")
    print(f"[{case.evidence}] Workflow: {' -> '.join(case.workflow)}")
    print(f"[{case.evidence}] Current-state annual burden: {_money(case.burden.annual_current_state)}")
    print(f"[{case.evidence}] Recoverable annual value: {_money(case.burden.annual_recoverable_value)}")
    print(f"[{case.evidence}] Implementation price: {_money(case.economics.implementation_price)}")
    print(f"[{case.evidence}] Annual support: {_money(case.economics.annual_support)}")
    print(f"[{case.evidence}] Engineering effort: {case.economics.engineering_hours} hours")
    print(f"[{case.evidence}] Solutions/sales effort: {case.economics.solutions_sales_hours} hours")
    print(f"[{case.evidence}] Sales cycle: {case.economics.sales_cycle_months} months")
    print(f"\n[{result.evidence}] Deterministic results given the fictional modeled assumptions:")
    print(f"  Customer first-year cost (implementation + support): {_money(result.first_year_cost)}")
    print(f"  Customer first-year net recoverable value: {_money(result.first_year_net_recoverable_value)}")
    print(f"  Implementation-only payback (support excluded): {result.implementation_only_payback_months:.2f} months")
    print(f"\n[{case.evidence}] Acquisition findings (unweighted):")
    for finding in assessment.findings:
        print(f"  - {finding}")
    print(f"\n[{assessment.evidence}] Gate results given the fictional modeled assumptions:")
    for gate in assessment.gates:
        print(f"  {gate.name}: {gate.status}")
    print(f"\n[{assessment.evidence}] Baseline cookbook verdict: {assessment.verdict}")
    print("This is the hypothesis later experiments must try to break—not a conclusion about government.")


def show_scenarios() -> None:
    case = load_baseline()
    print("HISTORICAL MODELED COOKBOOK SCENARIOS")
    print(f"FICTION NOTICE: {case.customer.fiction_notice}")
    print("These inherited reference points are not newly proven Chapter 0 outcomes.")
    for scenario in load_scenarios():
        print(f"[{scenario.evidence}] {scenario.name} -> {scenario.verdict}")


def _gate_label(dimension: GateDimension) -> str:
    return dimension.value.replace("_", " ").title()


def show_gates() -> None:
    case = load_baseline()
    assessment = baseline_gate_assessment()
    print("CHAPTER 1 — SEPARATE THE PROJECT FROM THE CUSTOMER")
    print(case.customer.name)
    print("FICTIONAL EDUCATIONAL MODEL")
    print(f"Engagement motion: {assessment.engagement_motion}\n")
    print("PROJECT GATES")
    for gate in assessment.gates[:-1]:
        print(f"  {_gate_label(gate.dimension):28} {gate.status}")
        for reason in gate.reasons:
            print(f"    - [{reason.evidence}] {reason.code}: {reason.explanation}")
    print(f"\nPROJECT VIABILITY             {assessment.project_viability}\n")
    target = assessment.gates[-1]
    print("TARGET GATE")
    print(f"  {_gate_label(target.dimension):28} {target.status}")
    print("  Reasons:")
    for reason in target.reasons:
        print(f"    - [{reason.evidence}] {reason.code}: {reason.explanation}")
    print(f"\nTARGET VIABILITY              {assessment.target_viability}")
    print(f"\nVERDICT\n{assessment.verdict}")


def show_gate_scenarios() -> None:
    case = load_baseline()
    scenarios = gate_scenarios()
    print("CHAPTER 1 GATE COUNTERFACTUALS")
    print(f"FICTION NOTICE: {case.customer.fiction_notice}")
    print("Changed fictional inputs are SENSITIVITY ASSUMPTIONs. Results are OBSERVED LAB RESULTs.\n")
    print(f"{'SCENARIO':26} {'PROJECT':11} {'TARGET':11} VERDICT")
    for scenario in scenarios:
        result = scenario.assessment
        target = "—" if result.project_viability is GateStatus.FAIL else result.target_viability.value
        print(f"{scenario.name:26} {result.project_viability.value:11} {target:11} {result.verdict}")
    print("\nCHANGED ASSUMPTIONS AND MECHANISMS")
    for scenario in scenarios:
        print(f"\n{scenario.name}")
        if not scenario.changed_assumptions:
            print("  - No change; original MODELED ASSUMPTION baseline.")
        for change in scenario.changed_assumptions:
            print(f"  - [{change.evidence}] {change.code}: {change.explanation}")
        for gate in scenario.assessment.gates:
            print(f"  {_gate_label(gate.dimension):28} {gate.status}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the fictional government engagement laboratory")
    parser.add_argument("command", choices=("baseline", "scenarios", "gates", "gate-scenarios"))
    args = parser.parse_args(argv)
    {"baseline": show_baseline, "scenarios": show_scenarios, "gates": show_gates, "gate-scenarios": show_gate_scenarios}[args.command]()
    return 0
