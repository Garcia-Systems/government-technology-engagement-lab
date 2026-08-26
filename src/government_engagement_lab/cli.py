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
from .formal_rfp import (acquisition_effort_by_category, assess_formal_rfp,
                         formal_rfp_scenarios)
from .pilot import assess_pilot, motion_comparison, pilot_scenarios


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


def show_formal_rfp() -> None:
    result = assess_formal_rfp()
    motion = result.motion
    print("CHAPTER 4 — THE FORMAL RFP MOTION\nFICTIONAL EDUCATIONAL MODEL")
    print("No real procurement law, threshold, schedule, or security rule is represented.\n")
    print(f"{motion.name} ({motion.identifier}) [{motion.evidence}]")
    print("\nJOURNEY")
    for stage in motion.journey.ordered_stages:
        print(f"  {stage.sequence:2}. {stage.display_name:30} {stage.effort_hours:3} h  {stage.elapsed_days:3} d [{stage.evidence}]")
    print("\nACTIVE SELLER EFFORT")
    for category, hours in acquisition_effort_by_category(motion).items():
        print(f"  {category.value:16} {hours:3} h")
    print(f"  TOTAL            {motion.journey.total_effort_hours:3} h")
    print(f"ELAPSED SALES CYCLE  {motion.journey.total_elapsed_days} modeled days = {motion.journey.modeled_months} modeled months")
    print(f"IMPLEMENTATION EFFORT {motion.engineering_hours} engineering h")
    print("\nPROPOSAL ARTIFACTS")
    for artifact in motion.proposal_artifacts:
        print(f"  {artifact.name} -> {artifact.stage_id}")
    print("\nSTAKEHOLDER DEPENDENCIES")
    for link in motion.stakeholder_participation:
        print(f"  {link.stage_id}: {link.stakeholder_id} ({link.responsibility})")
    _show_formal_rfp_economics(result)
    print("\nTARGET FINDINGS")
    for finding in result.findings: print(f"  - {finding.value}")
    print(f"\nPROJECT VIABILITY: {result.project_viability.value}")
    print(f"TARGET VIABILITY:  {result.target_viability.value}")
    print(f"VERDICT: {result.verdict} [{result.evidence}]")


def _show_formal_rfp_economics(result=None) -> None:
    result = result or assess_formal_rfp()
    motion, customer, seller = result.motion, result.customer_economics, result.seller_economics
    print("\nCUSTOMER VIEW")
    print(f"  Recoverable annual value:        {_money(load_baseline().burden.annual_recoverable_value)}")
    print(f"  First-year cost:                 {_money(customer.first_year_cost)}")
    print(f"  Net first-year recoverable value:{_money(customer.first_year_net_recoverable_value):>14}")
    print(f"  Implementation-only payback:     {customer.implementation_only_payback_months:.2f} months")
    print("\nSELLER VIEW")
    for rate in motion.labor_rates:
        print(f"  [{rate.evidence}] {rate.category.value} fully loaded internal cost: {_money(rate.hourly_cost)}/h")
    print(f"  Implementation revenue:          {_money(seller.implementation_revenue)}")
    print(f"  Delivery labor cost:             {_money(seller.delivery_labor_cost)}")
    print(f"  Acquisition labor cost:          {_money(seller.acquisition_labor_cost)}")
    print(f"  Other direct costs:              {_money(seller.other_direct_costs)}")
    print(f"  Acquisition-adjusted contribution: {_money(seller.acquisition_adjusted_contribution)}")
    print(f"  Contribution margin:             {seller.contribution_margin:.2%}")
    print(f"  [{motion.evidence}] Lab minimum contribution: {_money(motion.minimum_contribution)}")


def show_formal_rfp_economics() -> None:
    print("CHAPTER 4 — FORMAL RFP ECONOMICS\nFICTIONAL EDUCATIONAL MODEL")
    _show_formal_rfp_economics()


def show_formal_rfp_scenarios() -> None:
    print("CHAPTER 4 — FORMAL RFP SENSITIVITIES\nFICTIONAL EDUCATIONAL MODEL")
    print(f"{'SCENARIO':22} {'CUSTOMER':9} {'ACQ H':7} {'CYCLE':8} {'CONTRIB':13} VERDICT")
    for scenario in formal_rfp_scenarios():
        a = scenario.assessment
        customer = "PASS" if a.customer_economics.first_year_net_recoverable_value >= 0 else "FAIL"
        print(f"{scenario.name:22} {customer:9} {a.motion.journey.total_effort_hours:3} h   {a.motion.journey.modeled_months:5.2f} mo {_money(a.seller_economics.acquisition_adjusted_contribution):13} {a.verdict}")
    print("\nAll changes are labeled SENSITIVITY ASSUMPTION; baseline data is not mutated.")


def show_pilot() -> None:
    result, motion = assess_pilot(), assess_pilot().motion
    print("CHAPTER 5 — COOPERATIVE PAID PILOT\nFICTIONAL EDUCATIONAL MODEL")
    print(f"FICTION NOTICE: {motion.fiction_notice}")
    print(f"\n{motion.name} ({motion.identifier}) — PAID: {motion.paid}; DURATION: {motion.duration_days} days")
    print("\nINCLUDED SCOPE")
    for item in motion.scope: print(f"  + [{motion.evidence}] {item}")
    print("EXCLUSIONS")
    for item in motion.exclusions: print(f"  - [{motion.evidence}] {item}")
    print(f"HANDOFF: {motion.handoff}")
    print("\nPILOT JOURNEY")
    for stage in motion.journey.ordered_stages:
        print(f"  {stage.sequence:2}. {stage.display_name:28} {stage.effort_hours:2} h {stage.elapsed_days:3} d")
    print("\nSTAKEHOLDERS (Chapter 3 identities; sponsor coordinates but does not replace approvers)")
    for link in motion.stakeholders: print(f"  {link.stakeholder_id}: {link.responsibility}")
    print("\nACCEPTANCE CRITERIA [MODELED ASSUMPTION]")
    for c in motion.acceptance_criteria: print(f"  {c.identifier}: {c.metric} {c.operator} {c.threshold}")
    o = result.operations
    print("\nSYNTHETIC OPERATIONAL RESULT [OBSERVED LAB RESULT]")
    for name, value in o.__dict__.items():
        if name != "evidence": print(f"  {name}: {value}")
    _show_pilot_economics(result)
    print(f"\nPROJECT VIABILITY: {result.project_viability.value}")
    print(f"TARGET VIABILITY:  {result.target_viability.value}")
    print(f"PILOT ACCEPTANCE:  {result.acceptance.value}")
    print(f"COMMERCIAL VERDICT: {result.verdict}")
    print(f"FULL IMPLEMENTATION AUTHORIZED: {result.full_implementation_authorized}")
    print(f"NEXT STEP: {result.next_step} — expansion still requires a separate decision and broader reviews.")


def _show_pilot_economics(result=None) -> None:
    result = result or assess_pilot()
    e, m, s = result.economics, result.motion, result.economics.seller
    print("\nCUSTOMER ECONOMICS")
    print(f"  Pilot price (includes {_money(m.pilot_period_support)} pilot support): {_money(e.pilot_price)}")
    print(f"  Annualized opportunity value affected, not captured: {_money(e.annualized_value_potentially_affected)}")
    print(f"  Expected measurable pilot benefit [MODELED ASSUMPTION]: {_money(e.expected_measurable_benefit)}")
    print(f"  Customer pilot net benefit [OBSERVED LAB RESULT]: {_money(e.customer_pilot_net_benefit)}")
    print(f"  Synthetic-action value translation [MODELED ECONOMIC RESULT]: {_money(e.action_value_estimate)}")
    print("SELLER ECONOMICS [OBSERVED LAB RESULT]")
    print(f"  Revenue: {_money(s.implementation_revenue)}; delivery cost: {_money(s.delivery_labor_cost)}")
    print(f"  Acquisition: {e.acquisition_hours} h / {e.authorization_days} days to authorization / {_money(s.acquisition_labor_cost)}")
    print(f"  Other direct cost: {_money(s.other_direct_costs)}")
    print(f"  Acquisition-adjusted contribution: {_money(s.acquisition_adjusted_contribution)} ({s.contribution_margin:.2%})")
    print(f"  Acquisition h / $10k revenue: {Decimal(e.acquisition_hours) / (e.pilot_price / Decimal(10000)):.2f}")
    print(f"  Delivery h / $10k revenue: {Decimal(m.engineering_hours) / (e.pilot_price / Decimal(10000)):.2f}")
    print(f"  Acquisition cost / revenue: {s.acquisition_labor_cost / e.pilot_price:.2%}")
    print(f"  Opportunity value addressed: {e.annualized_value_potentially_affected / load_baseline().burden.annual_recoverable_value:.2%}")


def show_pilot_economics() -> None:
    print("CHAPTER 5 — PILOT ECONOMICS\nFICTIONAL EDUCATIONAL MODEL")
    _show_pilot_economics()


def show_pilot_scenarios() -> None:
    print("CHAPTER 5 — PILOT SENSITIVITIES\nFICTIONAL EDUCATIONAL MODEL")
    print(f"{'SCENARIO':22} {'ACQ H':7} {'AUTH D':8} {'ENG H':7} {'CONTRIB':13} VERDICT")
    for scenario in pilot_scenarios():
        a = scenario.assessment
        print(f"{scenario.name:22} {a.economics.acquisition_hours:3} h   {a.economics.authorization_days:3} d   {a.motion.engineering_hours:3} h   {_money(a.economics.seller.acquisition_adjusted_contribution):13} {a.verdict}")
        for change in scenario.changed_assumptions: print(f"  [{scenario.evidence}] {change}")
    print("No weighted pilot score is calculated.")


def show_motion_comparison() -> None:
    print("FORMAL RFP VERSUS COOPERATIVE PAID PILOT\nFICTIONAL EDUCATIONAL MODEL")
    print(f"{'MOTION':28} {'ACQ H':7} {'AUTH D':8} {'DEL H':7} {'REVENUE':12} {'CONTRIBUTION':14} TARGET")
    for row in motion_comparison():
        print(f"{row['motion']:28} {row['acquisition_hours']:3} h   {row['cycle_days']:3} d   {row['delivery_hours']:3} h   {_money(row['revenue']):12} {_money(row['contribution']):14} {row['target']}")
        print(f"  value addressed: {_money(row['value_addressed'])}; stakeholders: {row['stakeholders']}; approval stages: {row['approval_stages']}; support: {_money(row['support'])}")
    print("\n[OBSERVED LAB RESULT] SAME PROBLEM + DIFFERENT ENGAGEMENT MOTION = DIFFERENT TARGET RESULT")
    print("This result exists only within fictional assumptions; it is not empirical government-market evidence.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the fictional government engagement laboratory")
    parser.add_argument("command", choices=("baseline", "scenarios", "gates", "gate-scenarios", "journey", "journey-summary", "journey-scenarios", "stakeholders", "stakeholder-summary", "stakeholder-scenarios", "formal-rfp", "formal-rfp-economics", "formal-rfp-scenarios", "pilot", "pilot-economics", "pilot-scenarios", "compare-motions"))
    args = parser.parse_args(argv)
    {"baseline": show_baseline, "scenarios": show_scenarios, "gates": show_gates,
     "gate-scenarios": show_gate_scenarios, "journey": show_journey,
     "journey-summary": show_journey_summary, "journey-scenarios": show_journey_scenarios,
     "stakeholders": show_stakeholders, "stakeholder-summary": show_stakeholder_summary,
     "stakeholder-scenarios": show_stakeholder_scenarios,
     "formal-rfp": show_formal_rfp, "formal-rfp-economics": show_formal_rfp_economics,
     "formal-rfp-scenarios": show_formal_rfp_scenarios, "pilot": show_pilot,
     "pilot-economics": show_pilot_economics, "pilot-scenarios": show_pilot_scenarios,
     "compare-motions": show_motion_comparison}[args.command]()
    return 0
