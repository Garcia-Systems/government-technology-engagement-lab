import json
from importlib.resources import files

from government_engagement_lab.baseline import load_baseline
from government_engagement_lab.evidence import EvidenceLabel
from government_engagement_lab.gates import baseline_gate_assessment
from government_engagement_lab.journey import (
    effort_by_stage_type, effort_by_work_category, highest_effort_stage,
    load_baseline_journey, load_journey_scenarios, longest_elapsed_stage,
)
from government_engagement_lab.models import EngagementMotion, FindingCode, GateDimension, GateStatus


def test_baseline_fixture_loads_with_complete_unique_ordered_stages() -> None:
    journey = load_baseline_journey()
    raw = json.loads(files("government_engagement_lab").joinpath("fixtures", "baseline_journey.json").read_text())
    required = {"identifier", "display_name", "description", "sequence", "required", "effort_hours", "elapsed_days", "responsible_category", "stage_type", "evidence", "assumptions"}
    assert raw["stages"] and all(required <= stage.keys() for stage in raw["stages"])
    assert len({stage.identifier for stage in journey.stages}) == len(journey.stages)
    assert [stage.sequence for stage in journey.ordered_stages] == list(range(1, 11))
    assert all(stage.evidence in EvidenceLabel for stage in journey.stages)


def test_baseline_totals_reconcile_to_chapter_zero_and_sequential_rule() -> None:
    journey, case = load_baseline_journey(), load_baseline()
    assert journey.total_effort_hours == sum(stage.effort_hours for stage in journey.stages) == 192
    assert journey.total_elapsed_days == sum(stage.elapsed_days for stage in journey.stages) == 270
    assert journey.modeled_days_per_month == 30
    assert journey.modeled_months == case.economics.sales_cycle_months == 9
    assert journey.total_effort_hours == case.economics.solutions_sales_hours
    assert journey.engagement_motion is EngagementMotion.BASELINE_COOKBOOK_MOTION


def test_burden_summaries_reconcile_and_expose_extremes_without_scores() -> None:
    journey = load_baseline_journey()
    assert sum(effort_by_work_category(journey).values()) == journey.total_effort_hours
    assert sum(effort_by_stage_type(journey).values()) == journey.total_effort_hours
    assert highest_effort_stage(journey).identifier == "DISCOVERY"
    assert longest_elapsed_stage(journey).identifier == "PROCUREMENT_PATH"
    assert not hasattr(journey, "score")
    assert not hasattr(journey, "weighted_score")


def test_chapter_one_verdict_and_journey_traces_remain_grounded() -> None:
    assessment = baseline_gate_assessment()
    assert assessment.project_viability is GateStatus.PASS
    assert assessment.target_viability is GateStatus.FAIL
    assert assessment.verdict == "POOR TARGET CUSTOMER"
    reasons = {reason.code: reason.explanation for reason in assessment.gate(GateDimension.TARGET_ATTRACTIVENESS).reasons}
    assert "192" in reasons[FindingCode.HIGH_SOLUTIONS_EFFORT]
    assert "270" in reasons[FindingCode.LONG_SALES_CYCLE]


def test_simplified_path_is_transparent_different_and_does_not_mutate_baseline() -> None:
    before = load_baseline_journey()
    scenarios = {scenario.key: scenario for scenario in load_journey_scenarios()}
    simplified = scenarios["simplified_approval_path"]
    assert simplified.evidence is EvidenceLabel.SENSITIVITY_ASSUMPTION
    assert simplified.changed_stage_ids == ("PROPOSAL",)
    assert any("SENSITIVITY ASSUMPTION" in note for note in simplified.assumptions)
    assert simplified.journey.total_effort_hours == 170
    assert simplified.journey.total_elapsed_days == 245
    assert (simplified.journey.total_effort_hours, simplified.journey.total_elapsed_days) != (before.total_effort_hours, before.total_elapsed_days)
    after = load_baseline_journey()
    assert after == before and len(after.stages) == 10
