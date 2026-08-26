"""Command-line interface for the executable chapters."""

import argparse
from decimal import Decimal

from .baseline import assess_baseline, load_baseline, load_scenarios
from .economics import calculate_customer_economics
from .gates import baseline_gate_assessment, gate_scenarios
from .models import GateDimension, GateStatus
from .journey import (
    effort_by_stage_type, effort_by_work_category, highest_effort_stage,
    load_baseline_journey, load_journey_scenarios, longest_elapsed_stage,
)
from .stakeholders import load_baseline_topology, load_stakeholder_scenarios, summarize_topology


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


def show_journey() -> None:
    journey = load_baseline_journey()
    print("CHAPTER 2 — MAP THE GOVERNMENT BUYING JOURNEY")
    print("FICTIONAL EDUCATIONAL MODEL")
    print(journey.customer_name)
    print(f"\n{journey.name} [{journey.evidence}]")
    for stage in journey.ordered_stages:
        print(f"\n{stage.sequence}. {stage.display_name} ({'required' if stage.required else 'optional'})")
        print(f"   effort: {stage.effort_hours} h active work")
        print(f"   elapsed: {stage.elapsed_days} modeled d")
        print(f"   work: {stage.responsible_category}; type: {stage.stage_type}")
        print(f"   purpose: {stage.description}")
    print(f"\nTOTAL ACTIVE EFFORT\n{journey.total_effort_hours} h [{journey.result_evidence}]")
    print(f"\nTOTAL ELAPSED CYCLE\n{journey.total_elapsed_days} modeled days ≈ {journey.modeled_months} modeled months [{journey.result_evidence}]")
    print("\n192 HOURS OF EFFORT ≠ 9 MONTHS OF FULL-TIME LABOR")
    print("EFFORT = human work consumed")
    print("ELAPSED CYCLE = calendar time before authorization/closure")
    print("The 30-day modeled month and all stage allocations are MODELED ASSUMPTIONs, not real procurement conventions.")


def show_journey_summary() -> None:
    journey = load_baseline_journey()
    print("CHAPTER 2 — JOURNEY BURDEN SUMMARY")
    print(f"Total active effort: {journey.total_effort_hours} h")
    print(f"Total elapsed cycle: {journey.total_elapsed_days} modeled days ({journey.modeled_months} modeled months)")
    print("\nEFFORT BY WORK CATEGORY")
    for category, hours in effort_by_work_category(journey).items():
        print(f"  {category.value:24} {hours:3} h")
    print("\nEFFORT BY STAGE TYPE")
    for stage_type, hours in effort_by_stage_type(journey).items():
        print(f"  {stage_type.value:24} {hours:3} h")
    high, long = highest_effort_stage(journey), longest_elapsed_stage(journey)
    print(f"\nHighest-effort stage: {high.identifier} ({high.effort_hours} h)")
    print(f"Longest-elapsed stage: {long.identifier} ({long.elapsed_days} modeled d)")
    print("\nActive effort and elapsed calendar time are different constraints; no weighted journey score is calculated.")


def show_journey_scenarios() -> None:
    print("CHAPTER 2 — JOURNEY COMPOSITION SENSITIVITY")
    print("Same underlying project + different journey composition = different effort and/or elapsed cycle.\n")
    print(f"{'SCENARIO':28} {'EFFORT':10} ELAPSED")
    for scenario in load_journey_scenarios():
        journey = scenario.journey
        print(f"{scenario.name:28} {journey.total_effort_hours:3} h      {journey.total_elapsed_days:3} modeled d")
    print("\nCHANGES")
    for scenario in load_journey_scenarios():
        if scenario.changed_stage_ids:
            print(f"[{scenario.evidence}] {scenario.name}: omitted {', '.join(scenario.changed_stage_ids)}")
            for assumption in scenario.assumptions:
                print(f"  - {assumption}")
    print("This sensitivity is not a market verdict, named vehicle, or real procurement procedure.")


def show_stakeholders() -> None:
    topology = load_baseline_topology()
    print("CHAPTER 3 — STAKEHOLDER TOPOLOGY\nFICTIONAL EDUCATIONAL MODEL")
    print(f"{topology.customer_name} [{topology.evidence}]")
    print("Every role and relationship is a fictional MODELED ASSUMPTION.\n")
    for person in topology.stakeholders:
        print(person.display_name)
        print(f"  Function: {person.organizational_function}")
        print(f"  Roles: {', '.join(role.value for role in person.roles)}")
        print(f"  Participates: {', '.join(person.journey_stage_ids)}")
        print(f"  Approval authority: {', '.join(x.value for x in person.approval_authority) or 'none'}")
        print(f"  Blocking authority: {', '.join(x.value for x in person.blocking_authority) or 'none'}")
        print(f"  Access/control: {person.access_control_domain or 'none'}\n")
    print("RELATIONSHIPS")
    for relation in topology.relationships:
        print(f"  {relation.source_id} —{relation.relationship_type}→ {relation.target_id} ({', '.join(relation.stage_ids)})")
    print("\nSTAGE LINKAGE")
    for stage in topology.stages:
        print(f"  {stage.stage_id}: primary={stage.primary_responsible_id}; participants={', '.join(stage.participant_ids)}")
        print(f"    approvers={', '.join(stage.approver_ids) or 'none'}; blockers={', '.join(stage.blocker_ids) or 'none'}; access owners={', '.join(stage.technical_gatekeeper_ids) or 'none'}")


def show_stakeholder_summary() -> None:
    topology = load_baseline_topology()
    summary = summarize_topology(topology)
    print("CHAPTER 3 — DESCRIPTIVE STAKEHOLDER BURDEN")
    print("FICTIONAL EDUCATIONAL MODEL — counts are not a score or verdict")
    print(f"Stakeholders: {summary.stakeholder_count}")
    print(f"Role assignments: {summary.role_assignment_count}")
    print(f"Approval dependencies: {summary.approval_dependency_count}")
    print(f"Blocking dependencies: {summary.blocking_dependency_count}")
    print(f"Technical-access dependencies: {summary.technical_access_dependency_count}")
    print(f"Most involved stakeholder(s): {', '.join(summary.most_involved_stakeholder_ids)}")
    print(f"Highest-participation stage(s): {', '.join(summary.highest_participation_stage_ids)}")
    print("Participants per stage:")
    for stage, count in summary.participants_per_stage:
        print(f"  {stage}: {count}")


def show_stakeholder_scenarios() -> None:
    print("CHAPTER 3 — STAKEHOLDER AUTHORITY SENSITIVITY")
    print("Descriptive mechanisms only; this is not a score or a real-government claim.\n")
    print(f"{'SCENARIO':24} {'APPROVALS':10} {'BLOCKING':10} SPONSOR")
    scenarios = load_stakeholder_scenarios()
    for scenario in scenarios:
        summary = summarize_topology(scenario.topology)
        print(f"{scenario.key:24} {summary.approval_dependency_count:<10} {summary.blocking_dependency_count:<10} {scenario.topology.sponsor_strength}")
    print("\nMECHANISM CHANGES")
    for scenario in scenarios:
        print(f"{scenario.key}: {scenario.verdict}")
        for change in scenario.changed_assumptions or ("MODELED ASSUMPTION: unchanged baseline topology.",):
            print(f"  - {change}")
        print("  - controls: " + ", ".join(sorted({x.value for f in scenario.topology.findings for x in (f.reason,)})))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the fictional government engagement laboratory")
    parser.add_argument("command", choices=("baseline", "scenarios", "gates", "gate-scenarios", "journey", "journey-summary", "journey-scenarios", "stakeholders", "stakeholder-summary", "stakeholder-scenarios"))
    args = parser.parse_args(argv)
    {"baseline": show_baseline, "scenarios": show_scenarios, "gates": show_gates,
     "gate-scenarios": show_gate_scenarios, "journey": show_journey,
     "journey-summary": show_journey_summary, "journey-scenarios": show_journey_scenarios,
     "stakeholders": show_stakeholders, "stakeholder-summary": show_stakeholder_summary,
     "stakeholder-scenarios": show_stakeholder_scenarios}[args.command]()
    return 0
