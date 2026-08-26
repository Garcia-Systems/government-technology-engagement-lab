"""Command-line interface for Chapter 0 only."""

import argparse
from decimal import Decimal

from .baseline import assess_baseline, load_baseline, load_scenarios
from .economics import calculate_customer_economics


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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the fictional Chapter 0 engagement laboratory")
    parser.add_argument("command", choices=("baseline", "scenarios"))
    args = parser.parse_args(argv)
    {"baseline": show_baseline, "scenarios": show_scenarios}[args.command]()
    return 0
