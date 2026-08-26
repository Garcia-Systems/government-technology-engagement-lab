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
from .read_only import (assess_technical_scenario, read_only_scenarios,
                        technical_scenarios)
from .configuration import (BURDEN, assess_configuration_first,
                            configuration_scenarios, load_capability_fixture,
                            load_current_configuration)
from .small_engagement import (assess_small_engagement,
                               assess_small_engagement_scenarios)
from .larger_contract import (assess_larger_contract, assess_larger_contract_scenarios,
                              contract_size_comparison)
from .partner import assess_partner, direct_vs_partner, partner_scenarios
from .existing_path import (assess_existing_path, existing_path_scenarios,
                            rfp_vs_existing_path)
from .governance import (JOINT_SELLER_ATTRIBUTION, assess_governance,
                         formal_rfp_trace, governance_scenarios)
from .closed_integration import (assess_closed_integration,
                                 closed_integration_scenarios,
                                 evaluate_access, intervention_requirements,
                                 load_closed_fixture)
from .incumbent import (assess_incumbent, compare_alternatives,
                        incumbent_scenarios, load_incumbent_fixture)
from .repeat_government import (assess_repeat_government, repeat_government_scenarios,
                                three_level_comparison)
from .acquisition import (acquisition_report, acquisition_reports, focused_scenarios,
                          lost_deal_sensitivity)
from .throughput import (additional_capacity_sensitivity, load_seller_organization,
                         lost_opportunity_sensitivity, mixed_portfolio,
                         opportunity_cost, portfolio_scenarios)
from .repeatability import (assess_repeat_department, department_one_reference,
                            repeat_department_scenarios)
from .motion_economics import (conditional_findings, hypothesis_status,
                               motion_comparisons)
from .capstone import assess_capstone, evidence_inventory


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


def _show_read_only_economics(result) -> None:
    e, s = result.economics, result.economics.seller
    print(f"  Value addressed [MODELED ASSUMPTION]: {_money(e.value_addressed)}")
    print(f"  Engagement price: {_money(e.engagement_price)}; support: {_money(e.support)}")
    print(f"  First-year customer cost: {_money(e.first_year_customer_cost)}")
    print(f"  Net recoverable value: {_money(e.modeled_net_recoverable_value)}; bounded payback: {e.payback_months:.2f} months")
    print(f"  Engineering: {result.scenario.engineering_hours} h; acquisition: {e.acquisition_hours} h; cycle: {e.elapsed_days} d")
    print(f"  Delivery labor: {_money(s.delivery_labor_cost)}; acquisition labor: {_money(s.acquisition_labor_cost)}")
    print(f"  Support obligation: {_money(e.support)}; acquisition-adjusted contribution: {_money(s.acquisition_adjusted_contribution)}")


def show_read_only() -> None:
    result = assess_technical_scenario(technical_scenarios()[1]); s = result.scenario
    print("CHAPTER 6 — READ-ONLY BEFORE WRITE ACCESS\nFICTIONAL EDUCATIONAL MODEL")
    print(f"FICTION NOTICE: {load_baseline().customer.fiction_notice}")
    a = s.authority
    print(f"\nTECHNICAL AUTHORITY [{a.evidence}]: {a.source_access_mode.value}")
    print(f"  write capability={a.write_capability}; authoritative mutation={a.authoritative_system_mutation_allowed}; consequential action={a.consequential_action_allowed}")
    print(f"  authentication: {a.authentication_assumptions}\n  source/deployment boundary: {a.deployment_boundary}\n  retention: {a.data_retention_assumptions}; audit logging required={a.audit_logging_required}")
    print("ALLOWED OPERATIONS: " + ", ".join(s.allowed_operations)); print("PROHIBITED OPERATIONS: " + ", ".join(s.prohibited_operations))
    p = result.processing
    print(f"\nSYNTHETIC PROCESSING [OBSERVED LAB RESULT]: ingested={p.records_ingested}; normalized={len(p.normalized_records)}; exceptions={len(p.exceptions)}; duplicates={len(p.duplicates)}; source unchanged={p.source_unchanged}")
    print("REPORT: " + ", ".join(f"{k}={v}" for k, v in p.status_summary))
    print("PROVENANCE")
    for row in p.normalized_records: print(f"  {row.provenance.source_record_identifier}: {row.provenance.source_status} -> {row.provenance.normalized_status}; {row.provenance.reason}; exception={row.provenance.exception_flag}")
    print("\nGOVERNANCE FINDINGS (unweighted): " + ", ".join(x.value for x in s.risk_findings))
    print("STAKEHOLDER EFFECTS: IT and Security/Governance participation narrows; Sponsor, users, Procurement, Legal/Contracts, and Accessibility remain.")
    print("JOURNEY EFFECTS: technical validation and security/access review explicitly shrink; commercial authorization stages remain.")
    print("ENGINEERING WORK [MODELED ASSUMPTION]: " + ", ".join(f"{x.category}={x.hours}h" for x in s.engineering_work))
    _show_read_only_economics(result)
    print(f"ACCEPTANCE: {result.acceptance_passed}; PROJECT VIABILITY: {result.project_viability.value}; TARGET VIABILITY: {result.target_viability.value}; VERDICT: {result.verdict}")
    print("EVIDENCE: inputs=MODELED ASSUMPTION; processing=OBSERVED LAB RESULT; no write path=OBSERVED IMPLEMENTATION STRUCTURE")


def show_read_only_economics() -> None:
    print("CHAPTER 6 — READ-ONLY ECONOMICS\nFICTIONAL EDUCATIONAL MODEL")
    _show_read_only_economics(assess_technical_scenario(technical_scenarios()[1]))


def show_read_only_scenarios() -> None:
    print("CHAPTER 6 — TECHNICAL-SURFACE SCENARIOS\nFICTIONAL EDUCATIONAL MODEL")
    print(f"{'TECHNICAL SURFACE':31} {'VALUE':12} {'ENG H':6} {'ACQ H':6} {'CYCLE':7} {'GOVERNANCE':11} VERDICT")
    for a in read_only_scenarios():
        governance = "broader" if a.scenario.authority.write_capability else "narrower"
        print(f"{a.scenario.name:31} {_money(a.economics.value_addressed):12} {a.scenario.engineering_hours:4}h {a.economics.acquisition_hours:4}h {a.economics.elapsed_days:4}d {governance:11} {a.verdict}")
        print(f"  AUTHORITATIVE WRITES? {a.scenario.authority.authoritative_system_mutation_allowed}; CONSEQUENTIAL ACTIONS? {a.scenario.authority.consequential_action_allowed}; PROVENANCE? {a.processing is not None}; ROLLBACK REQUIRED? {a.scenario.governance.rollback_planning}")
        for change in a.scenario.changed_assumptions: print(f"  [{a.scenario.evidence}] {change}")


def _configuration_economics(a) -> None:
    e=a.economics; s=e.seller
    print(f"  Value addressed: {_money(e.value_addressed)} ({e.percent_addressed:.1%}); residual: {_money(e.residual_value)}")
    print(f"  Price: {_money(e.implementation_price)}; support: {_money(e.annual_support)}; first-year cost: {_money(e.first_year_cost)}")
    print(f"  Net first-year recoverable value: {_money(e.net_first_year_recoverable_value)}; implementation payback: {e.payback_months:.2f} months")
    print(f"  Configuration: {e.configuration_hours} h; engineering: {e.engineering_hours} h; acquisition: {e.acquisition_hours} h / {e.elapsed_days} d")
    print(f"  Delivery labor: {_money(s.delivery_labor_cost)}; acquisition labor: {_money(s.acquisition_labor_cost)}; contribution: {_money(s.acquisition_adjusted_contribution)}")


def show_configure_first() -> None:
    a=assess_configuration_first(); fixture=load_capability_fixture()
    print("CHAPTER 7 — CONFIGURATION-FIRST GOVERNMENT ENGAGEMENT\nFICTIONAL EDUCATIONAL MODEL")
    print("FICTION NOTICE: "+fixture["fiction_notice"]); print(f"INCUMBENT: {fixture['system_name']} [{fixture['evidence']}]")
    print("\nCAPABILITIES")
    for c in a.capabilities: print(f"  {c.identifier}: {c.support.value}; enabled={c.enabled}; {c.effort_hours} h; [{c.evidence}] — {c.limitations}")
    before=load_current_configuration()
    print(f"\nCURRENT GAPS [MODELED ASSUMPTION]: {len(before['statuses'])} inconsistent statuses; required fields, queues, reports, and notifications unconfigured; correction work partly outside the system.")
    print("\nSEQUENTIAL RESIDUAL FUNNEL")
    for step in a.steps: print(f"  {step.stage:30} {step.intervention_id:26} addressed {_money(step.addressed):>12}; remaining {_money(step.remaining)}")
    print(f"RESIDUAL: {_money(a.economics.residual_value)} — {a.residual_classification.value} [thresholds: MODELED ASSUMPTION]")
    print("\nECONOMICS"); _configuration_economics(a)
    if a.custom_residual_candidate: print("CUSTOM RESIDUAL CANDIDATE: "+a.custom_residual_candidate)
    print(f"PROJECT VIABILITY: {a.project_viability.value}; TARGET VIABILITY: {a.target_viability.value}; VERDICT: {a.verdict}")
    print("EVIDENCE: fictional capabilities=MODELED ALTERNATIVE ASSUMPTION; allocations/effort=MODELED ASSUMPTION; calculations=OBSERVED LAB RESULT; unsupported guard=OBSERVED IMPLEMENTATION STRUCTURE")


def show_configure_first_economics() -> None:
    print("CHAPTER 7 — CONFIGURATION-FIRST ECONOMICS\nFICTIONAL EDUCATIONAL MODEL")
    _configuration_economics(assess_configuration_first())


def show_configure_first_scenarios() -> None:
    print("CHAPTER 7 — CONFIGURATION-FIRST SCENARIOS\nFICTIONAL EDUCATIONAL MODEL")
    print(f"{'SCENARIO':28} {'ADDRESSED':12} {'RESIDUAL':12} {'CLASS':10} {'CFG H':6} {'ACQ H':6} VERDICT / OPERATION")
    for a in configuration_scenarios():
        e=a.economics
        print(f"{a.name:28} {_money(e.value_addressed):12} {_money(e.residual_value):12} {a.residual_classification.value:10} {e.configuration_hours:4}h {e.acquisition_hours:4}h {a.verdict} / {a.operational_recommendation} [{a.assumption_evidence}]")


def show_residual() -> None:
    a=assess_configuration_first(); print("CHAPTER 7 — RESIDUAL FUNNEL")
    print(f"Original recoverable value       {_money(sum(v for _,v in BURDEN))}")
    for step in a.steps: print(f"After {step.intervention_id.lower().replace('_',' '):29} {_money(step.remaining)}")
    print(f"Residual recoverable value       {_money(a.economics.residual_value)}\nResidual classification          {a.residual_classification.value}")


def _show_small_economics(a) -> None:
    e, c, s = a.engagement, a.customer, a.seller
    print("\nCUSTOMER ECONOMICS")
    print(f"  Annual value addressed: {_money(c.annual_value_addressed)} ({c.percent_original_value_addressed:.1f}% of original)")
    print(f"  Price / support / first-year cost: {_money(e.implementation_price)} / {_money(e.annual_support_revenue)} / {_money(c.first_year_cost)}")
    print(f"  Net recoverable value: {_money(c.net_recoverable_value)}; implementation payback: {c.implementation_payback_months:.2f} months")
    print(f"  Modeled customer-supported price: {_money(c.customer_supported_price)} [OBSERVED LAB RESULT]")
    print("SELLER ECONOMICS")
    print(f"  Engineering: {e.engineering_hours} h / {_money(s.delivery_labor_cost)}")
    print(f"  Acquisition: {e.acquisition_hours} h / {_money(s.acquisition_labor_cost)}")
    print(f"  Support: {_money(e.annual_support_revenue)} revenue / {e.support_hours} h / {_money(a.support_cost)} cost")
    print(f"  Other direct: {_money(s.other_direct_costs)}; contribution: {_money(s.acquisition_adjusted_contribution)} ({s.contribution_margin:.2%})")
    print(f"  Seller break-even price: {_money(a.seller_break_even_price)} [OBSERVED LAB RESULT]")
    print(f"  Acquisition h / $10k revenue: {a.ratios.acquisition_hours_per_implementation_revenue * Decimal(10000):.2f}")
    print(f"  Acquisition cost / revenue: {a.ratios.acquisition_cost_per_implementation_revenue:.2%}; engineering h / $10k: {a.ratios.engineering_hours_per_implementation_revenue * Decimal(10000):.2f}")
    print(f"  Value / price: {a.ratios.value_addressed_per_price:.2f}; contribution / price: {a.ratios.contribution_per_price:.2%}")


def show_small_engagement() -> None:
    a = assess_small_engagement(); e = a.engagement
    print("CHAPTER 8 — SMALL DEPARTMENTAL ENGAGEMENT\nFICTIONAL EDUCATIONAL MODEL")
    print(f"{e.customer_name}; scale={e.scale.value} [{e.evidence}]")
    print(f"\nSCOPE: {e.scope.department_team}; {e.scope.user_count} users; {e.scope.workflow_slice}")
    print(f"Authority: {e.scope.technical_authority}; duration: {e.scope.implementation_duration_days} days")
    print("Included: " + "; ".join(e.scope.included_features)); print("Excluded: " + "; ".join(e.scope.excluded_features))
    print("Data: " + "; ".join(e.scope.data_sources)); print("Support boundary: " + e.scope.support_boundary)
    print("Acceptance boundary: " + e.scope.acceptance_boundary)
    print("\nACQUISITION JOURNEY (the floor is the sum of explicit non-implementation stage work)")
    for stage in e.journey.ordered_stages:
        print(f"  {stage.display_name:32} {stage.effort_hours:2} h {stage.elapsed_days:3} d [{stage.evidence}]")
    print(f"Total journey elapsed: {e.journey.total_elapsed_days} modeled days; acquisition effort: {e.acquisition_hours} h")
    print("Stakeholders: " + ", ".join(e.stakeholder_ids))
    _show_small_economics(a)
    print(f"\nPROJECT VIABILITY: {a.project_viability.value}\nTARGET VIABILITY: {a.target_viability.value}\nCOMMERCIAL VERDICT: {a.verdict} [{a.evidence}]")
    print("EASIER TO APPROVE ≠ ECONOMIC TO SELL")


def show_small_engagement_economics() -> None:
    print("CHAPTER 8 — SMALL-ENGAGEMENT ECONOMICS\nFICTIONAL EDUCATIONAL MODEL")
    _show_small_economics(assess_small_engagement())


def show_small_engagement_scenarios() -> None:
    print("CHAPTER 8 — CONTRACT-SIZE SCENARIOS\nFICTIONAL EDUCATIONAL MODEL")
    print(f"{'SCENARIO':29} {'VALUE':12} {'PRICE':11} {'ENG':5} {'ACQ':5} {'CONTRIB':12} {'BREAK-EVEN':12} {'SUPPORTED':12} VERDICT")
    for a in assess_small_engagement_scenarios():
        e, c, s = a.engagement, a.customer, a.seller
        print(f"{e.name:29} {_money(c.annual_value_addressed):12} {_money(e.implementation_price):11} {e.engineering_hours:3}h {e.acquisition_hours:3}h {_money(s.acquisition_adjusted_contribution):12} {_money(a.seller_break_even_price):12} {_money(c.customer_supported_price):12} {a.verdict}")
        for change in e.changed_assumptions: print(f"  [{e.evidence}] {change}")


def show_contract_size() -> None:
    show_small_engagement_scenarios()

def _show_larger_economics(a) -> None:
    e=a.engagement; s=a.seller
    print(f"  Value addressed / residual: {_money(e.value_addressed)} / {_money(e.residual_value)}")
    print(f"  Price / support / first-year cost: {_money(e.implementation_price)} / {_money(e.annual_support_revenue)} / {_money(a.first_year_cost)}")
    print(f"  Customer net / payback: {_money(a.net_customer_value)} / {a.payback_months:.2f} months")
    print(f"  Engineering: {e.engineering_hours} h; acquisition: {e.acquisition_floor_hours} h floor + {e.acquisition_hours-e.acquisition_floor_hours} h incremental = {e.acquisition_hours} h; cycle: {e.cycle_days} d")
    print(f"  Support: {e.support_hours} h / {_money(a.support_cost)} cost / {_money(e.annual_support_revenue)} revenue")
    print(f"  Seller contribution: {_money(s.acquisition_adjusted_contribution)} ({s.contribution_margin:.2%})")
    print(f"  SELLER PRICE FLOOR: {_money(a.seller_price_floor)}; CUSTOMER PRICE CEILING: {_money(a.customer_price_ceiling)}")
    print(f"  VIABLE PRICE CORRIDOR: {_money(a.viable_price_corridor)} ({a.corridor_class.value})")
    print(f"  Acquisition cost / revenue: {a.acquisition_cost_percent_revenue:.2%}; acquisition h / $10k: {a.acquisition_hours_per_10000_revenue:.2f}")

def show_larger_contract() -> None:
    a=assess_larger_contract(); e=a.engagement
    print("CHAPTER 9 — LARGER CONTRACT EXPERIMENT\nFICTIONAL EDUCATIONAL MODEL")
    print(f"BASELINE SCOPE: {e.baseline_scope}; users: {e.users}; added data: {', '.join(e.additional_data_sources)}")
    print("\nVALUE LADDER / DECOMPOSABLE ADDED SCOPE")
    print(f"  Chapter 8 baseline: {_money(e.baseline_value)}")
    remaining=e.opportunity_value-e.baseline_value
    for c in e.components:
        remaining-=c.incremental_value-c.overlap
        print(f"  + {c.identifier}: {_money(c.incremental_value)}; overlap {_money(c.overlap)}; residual {_money(remaining)} [{c.evidence}]")
        print(f"    burden={', '.join(c.burden_categories)}; engineering={sum(x.hours for x in c.engineering)} h; acquisition={sum(x.hours for x in c.acquisition)} h")
        print(f"    governance={'; '.join(c.governance_surface)}; support={'; '.join(c.support_surface)}")
    print("\nECONOMICS [OBSERVED LAB RESULT]"); _show_larger_economics(a)
    print(f"PROJECT VIABILITY: {a.project_viability.value}; TARGET VIABILITY: {a.target_viability.value}; VERDICT: {a.verdict}")
    print("MORE REVENUE ≠ MORE CONTRIBUTION; BIGGER DEAL ≠ BETTER DEAL")

def show_larger_contract_economics() -> None:
    print("CHAPTER 9 — LARGER-CONTRACT ECONOMICS\nFICTIONAL EDUCATIONAL MODEL"); _show_larger_economics(assess_larger_contract())

def show_larger_contract_scenarios() -> None:
    print("CHAPTER 9 — LARGER-CONTRACT SCENARIOS\nFICTIONAL EDUCATIONAL MODEL")
    print(f"{'SCENARIO':31} {'VALUE':12} {'PRICE':11} {'ENG':5} {'ACQ':5} {'FLOOR':12} {'CEILING':12} {'CORRIDOR':12} VERDICT")
    for a in assess_larger_contract_scenarios():
        e=a.engagement
        print(f"{e.name:31} {_money(e.value_addressed):12} {_money(e.implementation_price):11} {e.engineering_hours:3}h {e.acquisition_hours:3}h {_money(a.seller_price_floor):12} {_money(a.customer_price_ceiling):12} {_money(a.viable_price_corridor):12} {a.verdict}")
        for change in e.changed_assumptions: print(f"  [{e.evidence}] {change}")

def show_contract_size_comparison() -> None:
    print("SMALL DEPARTMENTAL VS CHAPTER 9 LARGER CONTRACTS")
    small,*larger=contract_size_comparison()
    print(f"{'SCENARIO':31} {'VALUE':12} {'PRICE':11} {'ENG':5} {'ACQ':5} {'ACQ COST':12} {'FLOOR':12} {'CEILING':12} {'CORRIDOR':12} VERDICT")
    e=small.engagement; print(f"{'Small departmental':31} {_money(small.customer.annual_value_addressed):12} {_money(e.implementation_price):11} {e.engineering_hours:3}h {e.acquisition_hours:3}h {_money(small.seller.acquisition_labor_cost):12} {_money(small.seller_break_even_price):12} {_money(small.customer.customer_supported_price):12} {_money(small.customer.customer_supported_price-small.seller_break_even_price):12} {small.verdict}")
    for a in larger:
        e=a.engagement; print(f"{e.name:31} {_money(e.value_addressed):12} {_money(e.implementation_price):11} {e.engineering_hours:3}h {e.acquisition_hours:3}h {_money(a.seller.acquisition_labor_cost):12} {_money(a.seller_price_floor):12} {_money(a.customer_price_ceiling):12} {_money(a.viable_price_corridor):12} {a.verdict}")


def _show_partner_economics(a) -> None:
    e = a.economics
    print("CUSTOMER ECONOMICS")
    print(f"  Value addressed / total first-year contract: {_money(e.customer_value_addressed)} / {_money(e.customer_contract_value)}")
    print(f"  First-year net recoverable value: {_money(e.customer_first_year_net_value)}")
    print("SELLER ECONOMICS")
    print(f"  MODELED SELLER ENGAGEMENT REVENUE: {_money(e.seller_engagement_revenue)}")
    print(f"  Delivery / acquisition / retained PM / support cost: {_money(e.seller_delivery_cost)} / {_money(e.seller_acquisition_cost)} / {_money(e.retained_project_management_cost)} / {_money(e.seller_support_cost)}")
    print(f"  Acquisition-adjusted contribution: {_money(e.seller_contribution)} ({e.contribution_margin:.2%})")
    print("CHANNEL LEVERAGE (not a score)")
    print(f"  Seller acquisition: {e.seller_acquisition_hours} h; saved: {e.acquisition_hours_saved} h / {_money(e.acquisition_cost_saved)}")
    print(f"  Channel cost: {_money(e.partner_share)}; net channel economic effect: {_money(e.net_channel_economic_effect)}")
    print("  Access enablement and loss of control remain descriptive; labor savings alone do not decide access value.")


def show_partner() -> None:
    a = assess_partner(); m = a.motion
    print("CHAPTER 10 — PARTNER / PRIME-CONTRACTOR MOTION\nFICTIONAL EDUCATIONAL MODEL")
    print("FICTION NOTICE: " + m.fiction_notice)
    print(f"PARTNER: {m.partner_name} ({m.identifier}; {m.partner_type}) [{m.evidence}]")
    print(f"SELLER ROLE: {m.seller_role}")
    print("\nPARTNER OWNS: " + "; ".join(m.partner_responsibilities))
    print("SELLER RETAINS: " + "; ".join(m.seller_responsibilities))
    print(f"CUSTOMER RELATIONSHIP: {m.customer_relationship_owner.value}; CONTRACT: {m.contract_owner.value}")
    print("\nPARTNER-LED JOURNEY / PRIMARY OWNER / RETAINED SELLER HOURS")
    for stage in m.stage_ownership:
        print(f"  {stage.stage_id:31} {stage.primary_owner.value:8} {stage.seller_hours:3} h  ({', '.join(stage.stakeholder_ids)})")
    print(f"\nPARTNER SHARE: {m.partner_share_rate:.0%} of first-year customer contract [{m.evidence}]")
    _show_partner_economics(a)
    print(f"SUPPORT: customer → {m.support.first_line_owner.value} first-line → {m.support.escalation_owner.value} escalation; seller support revenue {_money(m.support.seller_support_revenue)} / {m.support.seller_support_hours} h")
    print("DEPENDENCIES: " + "; ".join(m.dependency_risks))
    print("UNWEIGHTED CHANNEL EFFECTS: " + "; ".join(x.value for x in m.channel_effects))
    print(f"DIRECT ACCESS: {m.direct_access.value}; PROJECT: {a.project_viability.value}; DIRECT TARGET: {a.direct_target_viability.value}; PARTNER TARGET: {a.target_viability.value}")
    print(f"VERDICT: {a.verdict} [{a.evidence}]")


def show_partner_economics() -> None:
    print("CHAPTER 10 — CHANNEL ECONOMICS\nFICTIONAL EDUCATIONAL MODEL")
    _show_partner_economics(assess_partner())


def show_partner_scenarios() -> None:
    print("CHAPTER 10 — PARTNER SCENARIOS\nFICTIONAL EDUCATIONAL MODEL")
    print(f"{'SCENARIO':29} {'SHARE':7} {'ACCESS':8} {'ACQ H':6} {'CHANNEL':12} {'CONTRIB':12} VERDICT")
    for a in partner_scenarios():
        e, m = a.economics, a.motion
        print(f"{m.identifier:29} {m.partner_share_rate:6.0%} {m.direct_access.value:8} {e.seller_acquisition_hours:4}h {_money(e.partner_share):12} {_money(e.seller_contribution):12} {a.verdict}")
        for change in a.changed_assumptions: print(f"  [SENSITIVITY ASSUMPTION] {change}")


def show_direct_vs_partner() -> None:
    direct, partner = direct_vs_partner(); d, p = direct.seller_economics, partner.economics
    print("FORMAL RFP DIRECT vs PARTNER / PRIME — SAME FICTIONAL TECHNICAL SCOPE")
    print(f"{'MOTION':18} {'CUST PRICE':12} {'SELLER REV':12} {'ENG H':6} {'ACQ H':6} {'ACQ COST':11} {'CHANNEL':11} {'CONTRIB':11} {'ACCESS':8} VERDICT")
    print(f"{'Direct RFP':18} {_money(direct.customer_economics.first_year_cost):12} {_money(d.implementation_revenue + direct.motion.annual_support):12} {direct.motion.engineering_hours:4}h {direct.motion.journey.total_effort_hours:4}h {_money(d.acquisition_labor_cost):11} {_money(Decimal()):11} {_money(d.acquisition_adjusted_contribution):11} {'LIMITED':8} {direct.verdict}")
    print(f"{'Partner-led':18} {_money(p.customer_contract_value):12} {_money(p.seller_engagement_revenue):12} {p.engineering_hours:4}h {p.seller_acquisition_hours:4}h {_money(p.seller_acquisition_cost):11} {_money(p.partner_share):11} {_money(p.seller_contribution):11} {partner.motion.direct_access.value:8} {partner.verdict}")
    print("\nOWNERSHIP")
    print("  Direct: relationship= DIRECT; contract= SELLER; support= SELLER")
    print(f"  Partner: relationship= {partner.motion.customer_relationship_owner.value}; contract= {partner.motion.contract_owner.value}; support= {partner.motion.support.first_line_owner.value} first-line / {partner.motion.support.escalation_owner.value} escalation")
    print("Customer price and value are identical; splitting revenue does not improve customer economics.")


def _show_existing_path_economics(a) -> None:
    e, s = a.economics, a.economics.seller
    print("CUSTOMER ECONOMICS (held constant with Formal RFP)")
    print(f"  First-year cost / net recoverable value: {_money(a.customer_economics.first_year_cost)} / {_money(a.customer_economics.first_year_net_recoverable_value)}")
    print(f"  Implementation-only payback: {a.customer_economics.implementation_only_payback_months:.2f} months")
    print("SELLER ECONOMICS")
    print(f"  Revenue / engineering effort / delivery cost: {_money(s.implementation_revenue)} / {a.motion.engineering_hours} h / {_money(s.delivery_labor_cost)}")
    print(f"  Acquisition: {e.acquisition_hours} h / {_money(s.acquisition_labor_cost)}; contribution: {_money(s.acquisition_adjusted_contribution)} ({s.contribution_margin:.2%})")
    print(f"  Acquisition cost / revenue: {e.acquisition_cost_percent_revenue:.2%}; acquisition h / $10,000 revenue: {e.acquisition_hours_per_10000_revenue:.2f}")
    print(f"  SAVED: {e.acquisition_hours_saved} h / {_money(e.acquisition_cost_saved)} / {e.elapsed_days_saved} modeled days")


def show_existing_path() -> None:
    a=assess_existing_path(); m=a.motion; v=m.mechanism
    print("CHAPTER 11 — EXISTING CONTRACT VEHICLE SCENARIO\nFICTIONAL EDUCATIONAL MODEL")
    print("FICTION NOTICE: "+v.fiction_notice)
    print(f"\nFICTIONAL PURCHASING MECHANISM: {v.fictional_name} ({v.identifier}) [{v.evidence}]")
    print(f"Provider/holder: {v.provider_holder}\nSeller eligibility: {v.seller_eligibility}\nPricing: {v.pricing_mechanism}")
    print("\nPRE-ESTABLISHED\n  - " + "\n  - ".join(v.pre_established))
    print("\nSTILL PROJECT-SPECIFIC\n  - " + "\n  - ".join(v.customer_approvals_still_required))
    print("\nJOURNEY")
    for s in m.journey.ordered_stages: print(f"  {s.sequence:2}. {s.display_name:31} {s.effort_hours:3} h {s.elapsed_days:3} d")
    print("\nCHANGES FROM FORMAL RFP [MODELED ALTERNATIVE ASSUMPTION]")
    for c in m.stage_changes: print(f"  {c.stage_id:31} {c.baseline_hours:2}->{c.existing_path_hours:2} h {c.baseline_days:2}->{c.existing_path_days:2} d — {c.reason}")
    _show_existing_path_economics(a)
    print("\nACQUISITION ATTRIBUTION")
    for x in a.attribution: print(f"  {x.bucket:30} {x.formal_rfp_hours:3} -> {x.existing_path_hours:3} h (saved {x.hours_saved:3})")
    print("\nTARGET FINDINGS\n  - " + "\n  - ".join(x.value for x in a.findings))
    print(f"\nBUYER ACCESS: {m.buyer_access.value}; PROJECT VIABILITY: {a.project_viability.value}; TARGET VIABILITY: {a.target_viability.value}")
    print(f"VERDICT: {a.verdict} [{a.evidence}]")


def show_existing_path_economics() -> None:
    print("CHAPTER 11 — EXISTING-PATH ECONOMICS\nFICTIONAL EDUCATIONAL MODEL")
    _show_existing_path_economics(assess_existing_path())


def show_existing_path_scenarios() -> None:
    print("CHAPTER 11 — EXISTING-PATH SCENARIOS\nAll mechanisms are fictional; changed inputs are SENSITIVITY ASSUMPTIONs.")
    print(f"{'SCENARIO':22} {'ACCESS':8} {'ACQ H':6} {'CYCLE':7} {'ACQ COST':12} {'CONTRIB':12} VERDICT")
    for a in existing_path_scenarios():
        e=a.economics
        print(f"{a.key:22} {a.motion.buyer_access.value:8} {e.acquisition_hours:4}h {e.elapsed_days:4}d {_money(e.seller.acquisition_labor_cost):12} {_money(e.seller.acquisition_adjusted_contribution):12} {a.verdict}")
        for x in a.changed_assumptions: print(f"  [SENSITIVITY ASSUMPTION] {x}")


def show_rfp_vs_existing_path() -> None:
    rfp, path=rfp_vs_existing_path(); e=path.economics
    print("FORMAL RFP DIRECT vs DIRECT WITH EXISTING PURCHASING PATH")
    print("Same customer, technical scope, value, price, support, engineering effort, and labor rates.")
    print(f"{'MOTION':25} {'ACQ HRS':8} {'CYCLE':8} {'ACQ COST':12} {'CONTRIB.':12} {'BUYER ACCESS':13} {'PROCUREMENT':12} VERDICT")
    print(f"{'Formal RFP':25} {rfp.motion.journey.total_effort_hours:6}h {rfp.motion.journey.total_elapsed_days:6}d {_money(rfp.seller_economics.acquisition_labor_cost):12} {_money(rfp.seller_economics.acquisition_adjusted_contribution):12} {'LIMITED':13} {'DIFFICULT':12} {rfp.verdict}")
    print(f"{'Existing path':25} {e.acquisition_hours:6}h {e.elapsed_days:6}d {_money(e.seller.acquisition_labor_cost):12} {_money(e.seller.acquisition_adjusted_contribution):12} {path.motion.buyer_access.value:13} {'REDUCED':12} {path.verdict}")
    print("\nSTAGE-LEVEL SAVINGS")
    print(f"{'STAGE':31} {'HOURS SAVED':12} DAYS SAVED")
    for c in path.motion.stage_changes: print(f"{c.stage_id:31} {c.hours_saved:11}h {c.days_saved:10}d")
    print(f"TOTAL                           {e.acquisition_hours_saved:11}h {e.elapsed_days_saved:10}d")


def _show_governance_metrics(scenario) -> None:
    m = scenario.metrics
    print("\nGOVERNANCE ATTRIBUTION [OBSERVED LAB RESULT]")
    print(f"  Seller delivery governance:       {m.seller_delivery_hours:3} h / {_money(m.seller_delivery_cost)}")
    print(f"  Seller acquisition / approval:    {m.seller_acquisition_approval_hours:3} h / {_money(m.seller_acquisition_cost)}")
    print(f"  Customer-only reviewer effort:    {m.customer_review_hours:3} h")
    print(f"  Elapsed review time (not labor):   {m.elapsed_review_days:3} modeled days")
    print(f"  Attribution rule: {JOINT_SELLER_ATTRIBUTION}")
    print("\nCATEGORY TOTALS")
    for category, hours in m.by_category:
        print(f"  {category.value:34} {hours:3} h")
    print("RESPONSIBILITY TOTALS")
    for owner, hours in m.by_responsibility:
        print(f"  {owner.value:34} {hours:3} h")
    print(f"\nPROJECT VIABILITY: {scenario.project_viability.value}; TARGET ATTRACTIVENESS: {scenario.target_viability.value}")
    print(f"VERDICT EFFECT: {scenario.verdict_effect}; EXISTING-GATE VERDICT: {scenario.verdict}")


def show_governance() -> None:
    scenario = assess_governance()
    inventory_notice = "Wholly fictional educational assumptions; no real law, policy, jurisdiction, or compliance mandate is represented."
    print("CHAPTER 12 — SECURITY, ACCESSIBILITY, AND GOVERNANCE SURFACE")
    print("FICTION NOTICE: " + inventory_notice)
    print(f"TECHNICAL SURFACE: {scenario.technical_surface} [{scenario.evidence}]")
    print("\nWORK ITEMS")
    for item in scenario.work_items:
        print(f"  {item.identifier}")
        print(f"    {item.classification.value} | {item.category.value} | {item.responsible_party.value} | required={item.required}")
        print(f"    active={item.effort_hours} h; elapsed review={item.elapsed_days} d; origin={item.origin.value}")
        print(f"    [{item.evidence}] {item.description}")
    _show_governance_metrics(scenario)
    print("\nChapter 12 distinguishes legitimate implementation from review mechanics; neither is labeled generic bureaucracy.")


def show_governance_summary() -> None:
    scenario = assess_governance()
    print("CHAPTER 12 — GOVERNANCE SUMMARY\nFICTIONAL EDUCATIONAL MODEL")
    print("DELIVERY WORK ≠ ACQUISITION / APPROVAL WORK; ELAPSED WAIT ≠ LABOR")
    _show_governance_metrics(scenario)
    print("\nFORMAL-RFP TRACE")
    for target, items in formal_rfp_trace().items():
        print(f"  Chapter 4 {target}: {', '.join(items)}")


def show_governance_scenarios() -> None:
    print("CHAPTER 12 — GOVERNANCE SCENARIOS\nFICTIONAL EDUCATIONAL MODEL")
    for scenario in governance_scenarios():
        print(f"\n{scenario.name} [{scenario.evidence}]")
        print(f"  surface={scenario.technical_surface}; removed={', '.join(scenario.removed_work_ids) or 'none'}")
        print(f"  shifted (not eliminated)={', '.join(scenario.shifted_work_ids) or 'none'}")
        _show_governance_metrics(scenario)


def show_governance_surfaces() -> None:
    print("CHAPTER 12 — GOVERNANCE-SURFACE COMPARISON")
    print("All quantities are fictional model inputs/results, not real compliance benchmarks.\n")
    print(f"{'SURFACE':24} {'SELLER DELIVERY':16} {'SELLER APPROVAL':16} {'CUSTOMER REVIEW':17} {'REVIEW DAYS':12} EFFECT")
    for s in governance_scenarios():
        m = s.metrics
        print(f"{s.key:24} {m.seller_delivery_hours:14}h {m.seller_acquisition_approval_hours:14}h {m.customer_review_hours:15}h {m.elapsed_review_days:10}d {s.verdict_effect}")
    write, read, config, heavy = governance_scenarios()
    print("\nWORK REMOVED BY READ-ONLY (authority-dependent only): " + ", ".join(read.removed_work_ids))
    print("WORK SHIFTED TO INCUMBENT (requirements remain): " + ", ".join(config.shifted_work_ids))
    print("DOCUMENTATION-HEAVY keeps the write-capable technical control surface and changes approval mechanics only.")


def _show_closed(a) -> None:
    s, p = a.scenario, a.preferred_feasibility
    print(f"\n{s.name} ({s.key}) [{s.evidence}]")
    print(f"Preferred intervention: {a.preferred.name}")
    print("Required access: " + ", ".join(x.value for x in a.preferred.acceptable_modes) + "; supported write required")
    print("Available access: " + ", ".join(x.mode.value for x in s.capabilities))
    print(f"Preferred feasibility: {p.status.value}")
    print("Reasons: " + ", ".join(p.reasons))
    print("Fallback ladder: " + " -> ".join(a.fallback_ladder))
    print("Selected fallback: " + (a.selected_fallback.name if a.selected_fallback else "NO DEAL"))
    if a.fallback_feasibility:
        print(f"Fallback feasibility: {a.fallback_feasibility.status.value}")
        cap = a.fallback_feasibility.capability
        print(f"Freshness: {cap.frequency.name if cap else 'NATIVE'}; completeness: {cap.completeness.value if cap else 'NATIVE'}")
    if a.economics is None:
        print("Customer economics: NOT APPLICABLE — TECHNICAL FEASIBILITY FAILED")
        print("Seller economics: NOT APPLICABLE — TECHNICAL FEASIBILITY FAILED")
    else:
        e = a.economics
        print(f"Value addressed / lost: {_money(e.value_addressed)} / {_money(e.value_lost)}")
        print(f"Customer first-year cost / net: {_money(e.first_year_cost)} / {_money(e.customer_net_value)}")
        print(f"Seller delivery / acquisition / support: {_money(e.delivery_cost)} / {_money(e.acquisition_cost)} / {_money(e.support_cost)}")
        print(f"Seller implementation contribution: {_money(e.seller_contribution)}")
        print(f"Manual handling: {e.annual_manual_hours} staff h/year")
    print("Governance implications: " + (", ".join(a.governance_implications) or "NOT EVALUATED"))
    print(f"Project viability: {a.project_viability.value}; target viability: {a.target_viability.value}")
    print(f"Commercial verdict: {a.verdict} [{a.evidence}]")


def show_closed_integration() -> None:
    print("CHAPTER 13 — CLOSED INTEGRATION SCENARIO")
    print("FICTION NOTICE: " + load_closed_fixture()["fiction_notice"])
    _show_closed(assess_closed_integration())


def show_closed_integration_scenarios() -> None:
    print("CHAPTER 13 — CLOSED-INTEGRATION SCENARIOS\nFICTIONAL EDUCATIONAL MODEL")
    for assessment in closed_integration_scenarios():
        _show_closed(assessment)


def show_access_matrix() -> None:
    scenarios = {a.scenario.key: a.scenario for a in closed_integration_scenarios()}
    scenario_for = {"BROAD_WRITE_INTEGRATION": "CLOSED_WRITE", "NATIVE_CONFIGURATION": "CONFIGURATION_ONLY",
                    "READ_ONLY_EDGE": "READ_ONLY_EXPORT", "MANUAL_ASSISTED_VIEW": "MANUAL_EXPORT_ONLY"}
    print("CHAPTER 13 — REQUIRED ACCESS / AVAILABLE ACCESS MATRIX")
    print("FICTIONAL LAB DECISION RULE; NOT A UNIVERSAL INTEGRATION STANDARD\n")
    print(f"{'INTERVENTION':38} {'REQUIRED ACCESS':34} {'AVAILABLE?':11} FEASIBILITY")
    for req in intervention_requirements():
        modeled = scenarios[scenario_for[req.identifier]]
        result = evaluate_access(req, modeled.capabilities, modeled.native_configuration_available)
        required = "native capability" if not req.acceptable_modes else "/".join(x.value for x in req.acceptable_modes)
        available = "yes" if result.status.value != "NOT_FEASIBLE" else "no"
        print(f"{req.name:38} {required:34} {available:11} {result.status.value}")


def _show_alternative(a) -> None:
    x, e = a.alternative, a.economics
    print(f"\n{x.display_name} ({x.identifier}) [{x.evidence}]")
    print(f"  Type/provider/model: {x.alternative_type.value} / {x.provider} / {x.implementation_model}")
    print("  Capabilities: " + (", ".join(x.capabilities) or "none"))
    print("  Major limitations: " + ("; ".join(x.limitations) or "none"))
    print(f"  Value addressed / residual: {_money(e.annual_value_addressed)} / {_money(e.residual_value)} ({e.percent_addressed:.2%} addressed)")
    print(f"  Implementation / recurring / first-year cost: {_money(e.implementation_cost)} / {_money(e.recurring_cost)} / {_money(e.first_year_customer_cost)}")
    print(f"  First-year net recoverable value: {_money(e.first_year_net_recoverable_value)}")
    payback = "N/A" if e.implementation_payback_months is None else f"{e.implementation_payback_months:.2f} months implementation-only; {e.full_first_year_payback_months:.2f} months including recurring"
    print(f"  Payback: {payback}")
    print(f"  Technical access: {x.technical_access_required} -> {a.access_result}; feasible={a.feasible}")
    print(f"  Governance/support: {x.governance_surface} / {x.support_owner}; custom ownership={x.custom_ownership_required}")
    print("  Unweighted risk findings: " + (", ".join(r.value for r in x.risk_findings) or "none"))
    if a.seller_economics:
        print(f"  Custom seller contribution: {_money(a.seller_economics.acquisition_adjusted_contribution)}")
    print(f"  Adequate: {a.adequate}; commercial result: {a.commercial_result} [{e.evidence}]")


def show_incumbent() -> None:
    scenario, fixture = assess_incumbent(), load_incumbent_fixture()
    print("CHAPTER 14 — INCUMBENT VENDOR ALTERNATIVE")
    print("FICTION NOTICE: " + fixture["fiction_notice"])
    print("All product, price, access, implementation, licensing, service, support, and roadmap details are fictional.")
    _show_alternative(next(x for x in scenario.assessments if x.alternative.identifier == "INCUMBENT_MODULE"))
    print("\nCUSTOM REFERENCES")
    for assessment in scenario.assessments:
        if assessment.alternative.custom_ownership_required:
            _show_alternative(assessment)
    rule = fixture["adequacy"]
    print(f"\nADEQUACY RULE [MODELED ASSUMPTION]: coverage >= {Decimal(rule['minimum_percent']):.0%} AND residual <= {_money(Decimal(rule['maximum_residual']))}")
    print("Decision precedence: feasible -> customer economics -> adequate coverage -> supportable -> acquisition viable -> lower custom ownership.")
    print(f"SELECTED COMMERCIAL RESULT: {scenario.selected_result} [OBSERVED LAB RESULT]")


def show_incumbent_scenarios() -> None:
    print("CHAPTER 14 — INCUMBENT SENSITIVITIES\nFICTIONAL EDUCATIONAL MODEL; no weighted alternative score exists.")
    print(f"{'SCENARIO':26} {'COVERAGE':10} {'RESIDUAL':13} {'1Y COST':13} {'NET':13} RESULT")
    for scenario in incumbent_scenarios():
        a = next(x for x in scenario.assessments if x.alternative.identifier == "INCUMBENT_MODULE")
        e = a.economics
        print(f"{scenario.key:26} {e.percent_addressed:8.2%} {_money(e.residual_value):13} {_money(e.first_year_customer_cost):13} {_money(e.first_year_net_recoverable_value):13} {scenario.selected_result}")
        for change in scenario.changed_assumptions:
            print(f"  [SENSITIVITY ASSUMPTION] {change}")


def show_alternatives() -> None:
    print("CHAPTER 14 — SOLUTION ALTERNATIVE COMPARISON")
    print("FICTION NOTICE: " + load_incumbent_fixture()["fiction_notice"])
    print("Different line-item structures are normalized through first-year customer totals; they are not treated as identical products.")
    for assessment in compare_alternatives():
        _show_alternative(assessment)



def _show_acquisition_row(x) -> None:
    print(f"\n{x.motion} [{x.evidence}]")
    for category, (hours, cost) in x.by_category().items():
        print(f"  {category.value:34} {hours:4} h  {_money(cost):>12}")
    print(f"  TOTAL SELLER ACQUISITION          {x.seller_acquisition_hours:4} h  {_money(x.acquisition_labor_cost):>12}")
    if x.partner_acquisition_hours or x.customer_acquisition_hours:
        print(f"  Partner/customer-owned: {x.partner_acquisition_hours}/{x.customer_acquisition_hours} h; total work: {x.total_customer_acquisition_work} h")
    print(f"  Seller revenue / customer contract: {_money(x.implementation_revenue)} / {_money(x.customer_contract_value)}")
    print(f"  Delivery cost / contribution: {_money(x.delivery_labor_cost)} / {_money(x.delivery_contribution)}")
    print(f"  Other direct costs: {_money(x.other_direct_costs)}")
    print(f"  Acquisition-adjusted contribution: {_money(x.acquisition_adjusted_contribution)} ({x.sustainability})")
    print(f"  Acq cost/revenue: {x.acquisition_cost_per_revenue:.2%}; acq h/$10k: {x.acquisition_hours_per_10000_revenue:.2f}; acq cost/value: {x.acquisition_cost_per_value:.2%}")
    print(f"  Acq h/engineering h: {x.acquisition_hours_per_engineering_hour:.3f}; acq cost/delivery cost: {x.acquisition_cost_per_delivery_cost:.2%}")
    print(f"  Elapsed cycle: {x.elapsed_days} modeled days (displayed, not monetized)")

def show_acquisition() -> None:
    print("CHAPTER 15 — ACQUISITION ECONOMICS\nWON-DEAL ECONOMICS; FICTIONAL MODELED ASSUMPTIONS, NOT MARKET BENCHMARKS")
    _show_acquisition_row(acquisition_report())

def show_acquisition_summary() -> None:
    print("CHAPTER 15 — CROSS-MOTION ACQUISITION SUMMARY")
    print(f"{'MOTION':31} {'HOURS':>5} {'ACQ COST':>12} {'REVENUE':>12} {'ACQ %':>7} {'DELIVERY':>12} {'DELIV CONTR':>13} {'ACQ-ADJ':>12} {'DAYS':>5}")
    for x in acquisition_reports():
        print(f"{x.motion:31} {x.seller_acquisition_hours:5} {_money(x.acquisition_labor_cost):>12} {_money(x.implementation_revenue):>12} {x.acquisition_cost_per_revenue:6.1%} {_money(x.delivery_labor_cost):>12} {_money(x.delivery_contribution):>13} {_money(x.acquisition_adjusted_contribution):>12} {x.elapsed_days:5}")

def show_acquisition_scenarios() -> None:
    print("CHAPTER 15 — FOCUSED ATTRIBUTION SCENARIOS")
    for x in focused_scenarios(): _show_acquisition_row(x)
    lost=lost_deal_sensitivity(); print(f"\nLOST-DEAL SENSITIVITY [{lost.evidence}]: revenue {_money(lost.implementation_revenue)}; retained acquisition cost {_money(lost.acquisition_cost_retained)}; opportunity contribution {_money(lost.opportunity_contribution)}")

def show_contribution_waterfall() -> None:
    print("CHAPTER 15 — CONTRIBUTION WATERFALLS (simplified modeled contribution, not profit)")
    for x in acquisition_reports():
        print(f"\n{x.motion}\n  Seller engagement revenue       {_money(x.implementation_revenue):>14}\n  Delivery labor cost            -{_money(x.delivery_labor_cost):>14}\n  DELIVERY CONTRIBUTION           {_money(x.delivery_contribution):>14}\n  Acquisition labor cost         -{_money(x.acquisition_labor_cost):>14}\n  Other direct costs             -{_money(x.other_direct_costs):>14}\n  ACQ.-ADJUSTED CONTRIBUTION      {_money(x.acquisition_adjusted_contribution):>14}")

def _throughput_row(result) -> None:
    report=acquisition_report(result.opportunities[0].motion) if result.name != "MIXED" else None
    motion=result.name
    hours="mixed" if report is None else str(report.seller_acquisition_hours)
    cycle="mixed" if report is None else str(report.elapsed_days)
    per_deal="mixed" if report is None else _money(report.acquisition_adjusted_contribution)
    print(f"{motion:31} {hours:>7} {cycle:>9} {result.completed_per_year:10} {result.average_active:10.2f} {per_deal:>14} {_money(result.annualized_contribution):>15} {result.overloaded_periods:8} {result.deferred_hours:10}")

def show_throughput_summary() -> None:
    print("CHAPTER 16 — THROUGHPUT AND OPPORTUNITY COST")
    print("FICTIONAL LAB RESULTS; NOT STAFFING RATIOS OR INDUSTRY BENCHMARKS")
    print(f"{'MOTION':31} {'ACQ HRS':>7} {'BASE DAYS':>9} {'DONE/YR':>10} {'AVG ACTIVE':>10} {'CONTRIB/DEAL':>14} {'ANNUAL CONTRIB':>15} {'OVERLOAD':>8} {'DEFERRED H':>10}")
    for result in portfolio_scenarios(): _throughput_row(result)
    print("\nContribution/deal × completed successful engagements = annualized contribution; this is not accounting profit.")

def show_throughput() -> None:
    org=load_seller_organization()
    print("CHAPTER 16 — FICTIONAL SELLER CAPACITY [MODELED ASSUMPTION]")
    print(org.fiction_notice)
    for role in org.roles:
        print(f"  {role.role.value:30} work={role.monthly_work_hours}h acquisition={role.acquisition_capacity_hours}h reserve={role.non_acquisition_reserve_hours}h [{role.evidence}]")
    print(f"  TOTAL ACQUISITION CAPACITY: {org.monthly_acquisition_capacity} h / modeled 30-day period\n")
    show_throughput_summary()

def show_pipeline() -> None:
    print("CHAPTER 16 — SYNTHETIC PERIOD-BY-PERIOD PIPELINE")
    print("FIFO: oldest due bucket receives capacity first; unfinished work rolls forward and pauses progression.")
    for result in portfolio_scenarios():
        print(f"\n{result.name} [OBSERVED LAB RESULT]")
        print(f"{'PERIOD':>6} {'ACTIVE':>6} {'DEMAND':>7} {'CAPACITY':>8} {'DONE H':>7} {'DEFER H':>7} STATE / COMPLETED")
        for p in result.periods[:12]: print(f"{p.period:6} {p.active_opportunity_count:6} {p.acquisition_demand:7} {p.available_capacity:8} {p.work_completed:7} {p.deferred_hours:7} {p.state.value} / {','.join(p.completed_identifiers) or '-'}")

def show_throughput_scenarios() -> None:
    print("CHAPTER 16 — PORTFOLIOS AND SENSITIVITIES")
    results=portfolio_scenarios();
    for result in results: _throughput_row(result)
    mixed=mixed_portfolio(); print("\nMIXED PORTFOLIO"); _throughput_row(mixed)
    extra=additional_capacity_sensitivity(); print("\nADD SECOND SOLUTIONS RESOURCE [SENSITIVITY ASSUMPTION]"); _throughput_row(extra)
    lost=lost_opportunity_sensitivity(); print("\nONE FORMAL RFP LOST [SENSITIVITY ASSUMPTION]"); _throughput_row(lost)
    print(f"\nOpportunity cost of Formal-RFP-heavy versus pilot-first: {_money(opportunity_cost(results[0],results[1]))}; derived from unrealized portfolio contribution, not calendar-time pricing.")

def _repeat_row(a) -> None:
    print(f"{a.key:38} eng={a.engineering_hours:3} discovery={a.discovery_hours:2} acquisition={a.acquisition_hours:3} governance={a.governance_hours:2} support={a.support_hours:2} total={a.total_effort_hours:3} contribution={_money(a.economics.marginal_contribution)}")

def show_reuse() -> None:
    a=assess_repeat_department()
    print("CHAPTER 17 — REUSE BY DIMENSION\nREUSABLE SOFTWARE ≠ REUSABLE ENGAGEMENT")
    print(f"{'DIMENSION':30} {'GREENFIELD':>10} {'REQUIRED':>9} {'SAVED':>7}")
    for x in a.summaries: print(f"{x.dimension.value:30} {x.greenfield_hours:10} {x.hours_required:9} {x.hours_saved:7} [{x.evidence}]")
    print("\nARTIFACT INVENTORY")
    for x in a.artifacts: print(f"  {x.identifier:26} {x.state.value:12} saved={x.hours_saved:2}h required={x.adaptation_effort:2}h — {x.reason}")

def show_repeat_department_summary() -> None:
    a=assess_repeat_department(); d1=department_one_reference()
    print("CHAPTER 17 — FIRST DEPARTMENT VERSUS SECOND DEPARTMENT")
    print(f"Reference motion: {a.reference_motion} — {a.reference_reason}")
    print(f"{'DIMENSION':24} {'DEPT 1':>10} {'DEPT 2':>10}")
    for label,k,v in (("Engineering hours","engineering_hours",a.engineering_hours),("Discovery hours","discovery_hours",a.discovery_hours),("Acquisition hours","acquisition_hours",a.acquisition_hours),("Governance hours","governance_hours",a.governance_hours),("Elapsed cycle (days)","elapsed_days",a.elapsed_days),("Support hours","support_hours",a.support_hours)):
        print(f"{label:24} {d1[k]:10} {v:10}")
    print(f"{'Implementation price':24} {_money(Decimal(d1['implementation_price'])):>10} {_money(a.economics.implementation_price):>10}")
    print(f"{'Contribution':24} {_money(Decimal(d1['contribution'])):>10} {_money(a.economics.marginal_contribution):>10}")
    print(f"\nEngineering greenfield / with reuse / saved: {a.engineering_greenfield_hours} / {a.engineering_hours} / {a.engineering_greenfield_hours-a.engineering_hours} h")
    print(f"Project: {a.project_verdict}; target: {a.target_verdict}; interpretation: {a.structural_interpretation}")
    print("REPEATABLE PROJECT ≠ PRODUCT")

def show_repeat_department_scenarios() -> None:
    print("CHAPTER 17 — REPEATABILITY SCENARIOS [SENSITIVITY ASSUMPTIONS]")
    for a in repeat_department_scenarios():
        _repeat_row(a)
        for change in a.changed_assumptions: print("  - " + change)
        print(f"  target={a.target_verdict}; structure={a.structural_interpretation}")

def show_repeat_department() -> None:
    a=assess_repeat_department()
    print("CHAPTER 17 — REPEATABILITY ACROSS DEPARTMENTS")
    print(f"FICTION NOTICE: {a.target.fiction_notice}")
    print(f"First department: {a.source.name}\n  {' -> '.join(a.source.workflow)}")
    print(f"Second department: {a.target.name}\n  {' -> '.join(a.target.workflow)}")
    print(f"Reference: {a.reference_motion} — {a.reference_reason}")
    show_reuse()
    print("\nMARGINAL SECOND-DEPARTMENT ECONOMICS")
    print(f"Engineering greenfield / reuse-adjusted / saved: {a.engineering_greenfield_hours} / {a.engineering_hours} / {a.engineering_greenfield_hours-a.engineering_hours} h")
    print(f"Discovery / acquisition / governance / support: {a.discovery_hours} / {a.acquisition_hours} / {a.governance_hours} / {a.support_hours} h")
    print(f"Customer first-year cost / net value: {_money(a.economics.first_year_customer_cost)} / {_money(a.economics.customer_net_value)}")
    print(f"Seller marginal contribution: {_money(a.economics.marginal_contribution)}")
    print("Findings: " + ", ".join(a.findings))
    print(f"Project: {a.project_verdict}; target: {a.target_verdict}; interpretation: {a.structural_interpretation}")
    print("Evidence: inputs [MODELED ASSUMPTION]; calculations [OBSERVED LAB RESULT]; artifact states [OBSERVED IMPLEMENTATION STRUCTURE]")

def _government_row(a) -> None:
    print(f"{a.key:32} eng={a.engineering_hours:3} acq={a.acquisition_hours:3} gov={a.governance_hours:2} support={a.support_hours:2} days={a.elapsed_days:3} contribution={_money(a.seller_contribution):>11} {a.verdict}")

def show_repeat_government() -> None:
    a=assess_repeat_government(); p=a.profile
    print("CHAPTER 18 — REPEATABILITY ACROSS GOVERNMENTS")
    print("FICTION NOTICE: "+p.fiction_notice)
    print("Reference: James River County (fictional) — Department 1 and same-government Department 2")
    print(f"New customer: {p.name}; department: {p.department_name}")
    print("Workflow: " + " -> ".join(p.workflow))
    print(f"Incumbent: {p.incumbent} (fictional); access: {p.access_mode}")
    print("Stakeholder topology: " + ", ".join(f"{x}:{y}" for x,y in p.stakeholders))
    print(f"Purchasing motion/path: {p.purchasing_motion} / {p.purchasing_path}")
    print("Governance requirements: " + "; ".join(p.governance_requirements))
    print("\nCROSS_CUSTOMER REUSE INVENTORY")
    for x in a.artifacts: print(f"  {x.identifier:26} {x.state.value:12} required={x.adaptation_effort:2}h saved={x.hours_saved:2}h")
    print(f"\nEngineering greenfield/reuse-adjusted/saved: {a.engineering_greenfield_hours}/{a.engineering_hours}/{a.engineering_saved_hours} h")
    print(f"Discovery/acquisition/governance/support: {a.discovery_hours}/{a.acquisition_hours}/{a.governance_hours}/{a.support_hours} h")
    print("Acquisition (Chapter 15 categories): " + ", ".join(f"{k}={v}h" for k,v in a.acquisition_by_category))
    print("Procurement reset: PURCHASING_PATH=REBUILD; governance documents adapt while approvals rebuild")
    print(f"Customer net value: {_money(a.customer_value)}; seller contribution: {_money(a.seller_contribution)}; elapsed: {a.elapsed_days} days")
    print(f"Verdict: {a.verdict}")
    print("SECOND DEPARTMENT SUCCESS ≠ REPEATABLE MARKET; CROSS-CUSTOMER REUSE ≠ PRODUCT")
    print("Evidence: fixture [MODELED ALTERNATIVE ASSUMPTION]; calculations [OBSERVED LAB RESULT]; scope [OBSERVED IMPLEMENTATION STRUCTURE]")

def show_repeat_government_summary() -> None:
    print("CHAPTER 18 — CROSS-GOVERNMENT SUMMARY")
    _government_row(assess_repeat_government())
    print("Technical repeatability ≠ commercial repeatability ≠ market repeatability.")

def show_repeat_government_scenarios() -> None:
    print("CHAPTER 18 — CROSS-GOVERNMENT SCENARIOS [SENSITIVITY ASSUMPTION]")
    for a in repeat_government_scenarios():
        _government_row(a)
        for x in a.changed_assumptions: print("  - "+x)

def show_repeatability_matrix() -> None:
    print("CHAPTER 18 — THREE-LEVEL REPEATABILITY MATRIX [OBSERVED LAB RESULT]")
    print(f"{'LEVEL':36} {'ENG':>5} {'ACQ':>5} {'GOV':>5} {'SUP':>5} {'DAYS':>5} {'CONTRIBUTION':>14}")
    for x in three_level_comparison():
        print(f"{x['level']:36} {x['engineering_hours']:5} {x['acquisition_hours']:5} {x['governance_hours']:5} {x['support_hours']:5} {x['elapsed_days']:5} {_money(x['contribution']):>14}")
    print("Raw artifact states remain available through repeat-government; no repeatability score exists.")

def _na(value, formatter=str):
    return "NOT_APPLICABLE" if value is None else formatter(value)

def show_motions() -> None:
    print("CHAPTER 19 — ENGAGEMENT MOTION ECONOMICS [OBSERVED IMPLEMENTATION STRUCTURE]")
    print("No weighted score, universal winner, or best-to-worst ranking is produced.")
    print(f"{'MOTION':29} {'VALUE':>13} {'ACQ HRS':>9} {'DAYS':>6} {'CUSTOMER':>10} {'SELLER':>10} {'ACCESS':>13}  VERDICT")
    for x in motion_comparisons():
        print(f"{x.name:29} {_money(x.customer_value_addressed):>13} {_na(x.seller_acquisition_hours):>9} {_na(x.elapsed_cycle_days):>6} {x.customer_economics_result:>10} {x.viability.delivery_economics.value:>10} {x.available_access_compatibility:>13}  {x.commercial_verdict}")
    print("\nCONDITIONAL FINDINGS")
    for finding in conditional_findings(): print("- "+finding)

def show_motion_customer() -> None:
    print("CHAPTER 19 — CUSTOMER COMPARISON")
    print(f"{'MOTION':29} {'VALUE':>13} {'IMPLEMENT':>13} {'RECUR':>12} {'FIRST YEAR':>13} {'NET VALUE':>13} {'PAYBACK':>12} {'RESIDUAL':>13}")
    for x in motion_comparisons():
        payback=_na(x.payback_months,lambda v:f"{v:.2f} mo")
        print(f"{x.name:29} {_money(x.customer_value_addressed):>13} {_money(x.customer_implementation_price):>13} {_money(x.recurring_customer_cost):>12} {_money(x.customer_first_year_cost):>13} {_money(x.customer_first_year_net_value):>13} {payback:>12} {_money(x.residual_value):>13}")

def show_motion_seller() -> None:
    print("CHAPTER 19 — SELLER COMPARISON (elapsed cycle is not monetized)")
    print(f"{'MOTION':29} {'REVENUE':>14} {'DELIVERY':>14} {'ACQUISITION':>14} {'CONTRIBUTION':>14} {'MARGIN':>10} {'DAYS':>6} {'/YEAR':>6} {'ANNUALIZED':>14}")
    for x in motion_comparisons():
        t=x.throughput
        print(f"{x.name:29} {_na(x.seller_engagement_revenue,_money):>14} {_na(x.seller_delivery_cost,_money):>14} {_na(x.seller_acquisition_cost,_money):>14} {_na(x.acquisition_adjusted_contribution,_money):>14} {_na(x.contribution_margin,lambda v:f'{v:.1%}'):>10} {_na(x.elapsed_cycle_days):>6} {_na(t.completed_engagements_per_year if t else None):>6} {_na(t.annualized_contribution if t else None,_money):>14}")

def show_motion_structure() -> None:
    print("CHAPTER 19 — STRUCTURAL COMPARISON")
    for x in motion_comparisons():
        g=x.governance
        print(f"\n{x.identifier} — {x.commercial_verdict}")
        print(f"  ACCESS: {x.technical_access_requirement} / {x.available_access_compatibility}; WRITE={x.write_authority}; READ-ONLY={x.read_only_capability}; NATIVE={x.native_configuration_possible}")
        print(f"  PROCUREMENT: {x.procurement_path}; SPONSOR: {x.sponsor_requirement}")
        print(f"  GOVERNANCE: {g.surface}; SELLER DELIVERY={_na(g.seller_delivery_hours)}h; APPROVAL={_na(g.seller_approval_acquisition_hours)}h; REVIEW={_na(g.elapsed_review_days)}d; {g.disposition}")
        print(f"  SUPPORT: {x.support_owner}; {x.seller_support_obligation}; ESCALATION={x.escalation_model}")
        print(f"  RELATIONSHIP: {x.customer_relationship_owner}; REPEATABILITY: {x.repeatability.value}")
        print(f"  EVIDENCE: {', '.join(x.evidence_sources)}; RISKS: {', '.join(x.major_risks)}")

def show_hypothesis_status() -> None:
    status,reasons=hypothesis_status()
    print("CHAPTER 19 — POOR TARGET CUSTOMER HYPOTHESIS STATUS")
    print(f"STATUS: {status.value}")
    for reason in reasons: print("- "+reason)
    print("NOT A CHAPTER 20 FINAL VERDICT")

def show_capstone_evidence() -> None:
    print("CHAPTER 20 — CAPSTONE EVIDENCE INVENTORY")
    print("FICTION NOTICE: "+assess_capstone().fiction_notice)
    for x in evidence_inventory():
        print(f"{x.identifier}: [{x.evidence.value}] {x.finding} SOURCES={','.join(x.sources)}")

def show_capstone_verdict() -> None:
    a=assess_capstone()
    print("CHAPTER 20 — CAPSTONE VERDICT")
    print("FICTION NOTICE: "+a.fiction_notice)
    print(f"BASELINE: {a.baseline_motion_result} ({a.baseline_answer})")
    print(f"HYPOTHESIS: {a.falsification_status.value}")
    print(f"FINAL VERDICT: {a.final_verdict.value}")
    print(f"PRECEDENCE: {a.precedence_rule}")
    for reason in a.supporting_findings: print("- "+reason)

def show_capstone() -> None:
    a=assess_capstone()
    print("CHAPTER 20 — POOR CUSTOMER OR POOR MOTION?")
    print("FICTION NOTICE: "+a.fiction_notice)
    print(f"ORIGINAL HYPOTHESIS: {a.original_hypothesis}")
    print(f"BASELINE FORMAL RFP: {a.baseline_motion_result}; CORRECT UNDER BASELINE? {a.baseline_answer}")
    print("STRONGEST EVIDENCE FOR: "+a.evidence_for[0].finding)
    print("STRONGEST EVIDENCE AGAINST: "+a.evidence_against[0].finding)
    print("\nMOTION SUMMARY")
    for x in a.motions: print(f"- {x.name}: project={x.project_viability.value}; target={x.target_viability.value}; {x.commercial_verdict}")
    print(f"\nPROJECT / TARGET: problem={a.gates.problem}; technical={a.gates.technical}; target={a.gates.target}")
    print(f"REPEATABILITY: within-account={a.gates.within_account}; cross-government={a.gates.cross_government}")
    print(f"HYPOTHESIS FALSIFICATION: {a.falsification_status.value}; {a.broader_answer}")
    print(f"FINAL VERDICT: {a.final_verdict.value} [{a.evidence_posture}]")
    print("TRIGGERED PRECEDENCE: "+a.precedence_rule)
    print("\nRECOMMENDED ENGAGEMENT POSTURE")
    for x in a.recommended_posture: print("- "+x)
    print("\nUNRESOLVED REAL DISCOVERY CONDITIONS")
    for x in a.unresolved_conditions: print("- "+x)
    print("\nEVIDENCE LABELS: MODELED ASSUMPTION; OBSERVED LAB RESULT; OBSERVED IMPLEMENTATION STRUCTURE; SENSITIVITY ASSUMPTION; MODELED ALTERNATIVE ASSUMPTION")

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the fictional government engagement laboratory")
    parser.add_argument("command", choices=("baseline", "scenarios", "gates", "gate-scenarios", "journey", "journey-summary", "journey-scenarios", "stakeholders", "stakeholder-summary", "stakeholder-scenarios", "formal-rfp", "formal-rfp-economics", "formal-rfp-scenarios", "pilot", "pilot-economics", "pilot-scenarios", "compare-motions", "read-only", "read-only-economics", "read-only-scenarios", "compare-technical-surfaces", "configure-first", "configure-first-economics", "configure-first-scenarios", "residual", "small-engagement", "small-engagement-economics", "small-engagement-scenarios", "contract-size", "larger-contract", "larger-contract-economics", "larger-contract-scenarios", "contract-size-comparison", "partner", "partner-economics", "partner-scenarios", "direct-vs-partner", "existing-path", "existing-path-economics", "existing-path-scenarios", "rfp-vs-existing-path", "governance", "governance-summary", "governance-scenarios", "governance-surfaces", "closed-integration", "closed-integration-scenarios", "access-matrix", "incumbent", "incumbent-scenarios", "alternatives", "acquisition", "acquisition-summary", "acquisition-scenarios", "contribution-waterfall", "throughput", "throughput-summary", "throughput-scenarios", "pipeline", "repeat-department", "repeat-department-summary", "repeat-department-scenarios", "reuse", "repeat-government", "repeat-government-summary", "repeat-government-scenarios", "repeatability-matrix", "motions", "motion-customer", "motion-seller", "motion-structure", "hypothesis-status", "capstone", "capstone-evidence", "capstone-verdict"))
    args = parser.parse_args(argv)
    {"baseline": show_baseline, "scenarios": show_scenarios, "gates": show_gates,
     "gate-scenarios": show_gate_scenarios, "journey": show_journey,
     "journey-summary": show_journey_summary, "journey-scenarios": show_journey_scenarios,
     "stakeholders": show_stakeholders, "stakeholder-summary": show_stakeholder_summary,
     "stakeholder-scenarios": show_stakeholder_scenarios,
     "formal-rfp": show_formal_rfp, "formal-rfp-economics": show_formal_rfp_economics,
     "formal-rfp-scenarios": show_formal_rfp_scenarios, "pilot": show_pilot,
     "pilot-economics": show_pilot_economics, "pilot-scenarios": show_pilot_scenarios,
     "compare-motions": show_motion_comparison, "read-only": show_read_only,
     "read-only-economics": show_read_only_economics, "read-only-scenarios": show_read_only_scenarios,
     "compare-technical-surfaces": show_read_only_scenarios,
     "configure-first": show_configure_first, "configure-first-economics": show_configure_first_economics,
     "configure-first-scenarios": show_configure_first_scenarios, "residual": show_residual,
     "small-engagement": show_small_engagement, "small-engagement-economics": show_small_engagement_economics,
     "small-engagement-scenarios": show_small_engagement_scenarios, "contract-size": show_contract_size,
     "larger-contract": show_larger_contract, "larger-contract-economics": show_larger_contract_economics,
     "larger-contract-scenarios": show_larger_contract_scenarios, "contract-size-comparison": show_contract_size_comparison,
     "partner": show_partner, "partner-economics": show_partner_economics,
     "partner-scenarios": show_partner_scenarios, "direct-vs-partner": show_direct_vs_partner,
     "existing-path": show_existing_path, "existing-path-economics": show_existing_path_economics,
     "existing-path-scenarios": show_existing_path_scenarios, "rfp-vs-existing-path": show_rfp_vs_existing_path,
     "governance": show_governance, "governance-summary": show_governance_summary,
     "governance-scenarios": show_governance_scenarios, "governance-surfaces": show_governance_surfaces, "closed-integration": show_closed_integration, "closed-integration-scenarios": show_closed_integration_scenarios, "access-matrix": show_access_matrix, "incumbent": show_incumbent, "incumbent-scenarios": show_incumbent_scenarios, "alternatives": show_alternatives, "acquisition": show_acquisition, "acquisition-summary": show_acquisition_summary, "acquisition-scenarios": show_acquisition_scenarios, "contribution-waterfall": show_contribution_waterfall, "throughput": show_throughput, "throughput-summary": show_throughput_summary, "throughput-scenarios": show_throughput_scenarios, "pipeline": show_pipeline, "repeat-department": show_repeat_department, "repeat-department-summary": show_repeat_department_summary, "repeat-department-scenarios": show_repeat_department_scenarios, "reuse": show_reuse, "repeat-government": show_repeat_government, "repeat-government-summary": show_repeat_government_summary, "repeat-government-scenarios": show_repeat_government_scenarios, "repeatability-matrix": show_repeatability_matrix, "motions": show_motions, "motion-customer": show_motion_customer, "motion-seller": show_motion_seller, "motion-structure": show_motion_structure, "hypothesis-status": show_hypothesis_status, "capstone": show_capstone, "capstone-evidence": show_capstone_evidence, "capstone-verdict": show_capstone_verdict}[args.command]()
    return 0
