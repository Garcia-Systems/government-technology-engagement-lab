from decimal import Decimal
from pathlib import Path

from government_engagement_lab.evidence import EvidenceLabel
from government_engagement_lab.formal_rfp import assess_formal_rfp, load_formal_rfp_motion
from government_engagement_lab.models import EngagementMotion, GateStatus, PilotAcceptance, SponsorStrength
from government_engagement_lab.pilot import (assess_pilot, calculate_pilot_economics,
    evaluate_acceptance, load_pilot_motion, motion_comparison, pilot_scenarios,
    run_pilot_records, validate_pilot_motion)
from government_engagement_lab.stakeholders import load_baseline_topology


def test_fixture_loads_and_boundary_is_real():
    motion = load_pilot_motion()
    validate_pilot_motion(motion)
    assert motion.identifier == "JAMES_RIVER_COOPERATIVE_PAID_PILOT"
    assert motion.journey.engagement_motion is EngagementMotion.COOPERATIVE_PAID_PILOT
    assert motion.paid and motion.pilot_price > 0 and motion.duration_days == 90
    assert motion.scope and motion.exclusions and motion.handoff
    assert "Consequential automated writes" in motion.exclusions
    assert motion.acceptance_criteria
    assert not hasattr(motion, "score")


def test_synthetic_execution_and_acceptance_are_deterministic():
    motion = load_pilot_motion()
    first = run_pilot_records(motion)
    assert first == run_pilot_records(motion)
    assert (first.records_processed, first.reconciliations_performed) == (10, 7)
    assert first.duplicate_actions_avoided == 1
    assert first.exceptions_surfaced == 2
    assert first.status_views_produced == 3
    assert first.manual_lookup_actions_reduced == 3
    assert first.report_preparation_actions_reduced == 3
    assert first.evidence is EvidenceLabel.OBSERVED_LAB_RESULT
    assert evaluate_acceptance(motion, first) is PilotAcceptance.PILOT_ACCEPTED
    assert any(r["status"] == "UNKNOWN" for r in motion.records)
    assert any(not r["permit_id"] for r in motion.records)
    assert any(r["status"] == "CORRECTION_REQUESTED" for r in motion.records)


def test_assumptions_and_observations_remain_separate():
    motion, result = load_pilot_motion(), assess_pilot()
    assert motion.evidence is EvidenceLabel.MODELED_ASSUMPTION
    assert all(c.evidence is EvidenceLabel.MODELED_ASSUMPTION for c in motion.acceptance_criteria)
    assert result.operations.evidence is EvidenceLabel.OBSERVED_LAB_RESULT
    assert result.economics.evidence is EvidenceLabel.OBSERVED_LAB_RESULT
    assert result.economics.action_value_estimate == Decimal("16.80")


def test_journey_and_stakeholders_reuse_prior_domain_structures():
    motion = load_pilot_motion()
    assert motion.journey.total_effort_hours == 58
    assert motion.journey.total_elapsed_days == 110
    assert motion.sponsor_strength is SponsorStrength.STRONG
    people = {p.identifier for p in load_baseline_topology().stakeholders}
    assert {x.stakeholder_id for x in motion.stakeholders} <= people
    assert {s.stage_type.value for s in motion.journey.stages} >= {"GOVERNANCE", "PROCUREMENT", "APPROVAL", "ACCEPTANCE"}


def test_pilot_economics_are_independent_and_exact():
    motion, formal = load_pilot_motion(), load_formal_rfp_motion()
    economics = calculate_pilot_economics(motion)
    assert economics.acquisition_hours == 58
    assert economics.authorization_days == 75
    assert motion.engineering_hours == 140 < formal.engineering_hours == 522
    assert economics.pilot_price == Decimal("36000") != formal.implementation_price
    assert economics.annualized_value_potentially_affected <= Decimal("104002.80")
    assert economics.seller.delivery_labor_cost == Decimal("15400")
    assert economics.seller.acquisition_labor_cost == Decimal("6290")
    assert economics.seller.other_direct_costs == Decimal("1000")
    assert economics.seller.acquisition_adjusted_contribution == Decimal("13310")
    assert economics.seller.contribution_margin == Decimal("13310") / Decimal("36000")
    assert economics.customer_pilot_net_benefit == Decimal("3000")
    assert motion.labor_rates == formal.labor_rates


def test_pilot_result_is_not_expansion_authorization():
    result = assess_pilot()
    assert result.acceptance is PilotAcceptance.PILOT_ACCEPTED
    assert result.project_viability is GateStatus.PASS
    assert result.target_viability is GateStatus.PASS
    assert result.verdict == "PILOT-FIRST TARGET"
    assert result.full_implementation_authorized is False
    assert result.next_step == "VALIDATE EXPANSION"


def test_sensitivities_expose_motion_failure_mechanisms():
    scenarios = {x.key: x for x in pilot_scenarios()}
    base, small, broad, weak = (scenarios[x].assessment for x in ("BASELINE", "TOO_SMALL", "TOO_BROAD", "WEAK_SPONSOR"))
    assert small.economics.seller.acquisition_adjusted_contribution < small.motion.minimum_contribution
    assert small.verdict == "POOR TARGET CUSTOMER"
    assert broad.motion.engineering_hours > base.motion.engineering_hours
    assert broad.economics.acquisition_hours > base.economics.acquisition_hours
    assert broad.economics.authorization_days > base.economics.authorization_days
    assert broad.verdict == "POOR TARGET CUSTOMER"
    assert weak.motion.sponsor_strength is SponsorStrength.LIMITED
    assert weak.economics.acquisition_hours > base.economics.acquisition_hours
    assert weak.target_viability is GateStatus.FAIL
    changed = tuple(s for k, s in scenarios.items() if k != "BASELINE")
    assert all(s.evidence is EvidenceLabel.SENSITIVITY_ASSUMPTION for s in changed)
    assert all("SENSITIVITY ASSUMPTION" in s.changed_assumptions[0] for s in changed)


def test_direct_comparison_preserves_rfp_and_exposes_context():
    before = load_formal_rfp_motion()
    formal, pilot = motion_comparison()
    assert formal["acquisition_hours"] == 192 and formal["cycle_days"] == 270
    assert formal["delivery_hours"] == 522 and formal["revenue"] == Decimal("78000")
    assert formal["contribution"] == Decimal("-60") and formal["target"] == "POOR TARGET CUSTOMER"
    assert pilot["acquisition_hours"] < formal["acquisition_hours"]
    assert pilot["cycle_days"] < formal["cycle_days"]
    assert pilot["value_addressed"] < formal["value_addressed"]
    assert pilot["target"] == "PILOT-FIRST TARGET"
    assert pilot["rates"] == formal["rates"]
    assert assess_formal_rfp().motion == before


def test_chapter_seven_is_not_implemented():
    root = Path(__file__).parents[1]
    assert not (root / "chapters/chapter-07-configuration-first.md").exists()
    assert not (root / "src/government_engagement_lab/configuration_first.py").exists()
