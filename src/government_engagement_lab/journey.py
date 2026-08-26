"""Chapter 2 journey loading and deterministic burden summaries."""

from collections import defaultdict
from dataclasses import replace

from .baseline import _fixture
from .evidence import parse_evidence_label
from .models import (
    EngagementJourney,
    EngagementMotion,
    EngagementStage,
    JourneyScenario,
    StageType,
    WorkCategory,
)


def _stage(raw: dict) -> EngagementStage:
    return EngagementStage(
        identifier=raw["identifier"],
        display_name=raw["display_name"],
        description=raw["description"],
        sequence=raw["sequence"],
        required=raw["required"],
        effort_hours=raw["effort_hours"],
        elapsed_days=raw["elapsed_days"],
        responsible_category=WorkCategory(raw["responsible_category"]),
        stage_type=StageType(raw["stage_type"]),
        evidence=parse_evidence_label(raw["evidence"]),
        assumptions=tuple(raw["assumptions"]),
    )


def load_baseline_journey() -> EngagementJourney:
    raw = _fixture("baseline_journey.json")
    return EngagementJourney(
        identifier=raw["identifier"],
        name=raw["name"],
        description=raw["description"],
        customer_name=raw["customer_name"],
        engagement_motion=EngagementMotion(raw["engagement_motion"]),
        stages=tuple(_stage(item) for item in raw["stages"]),
        modeled_days_per_month=raw["modeled_days_per_month"],
        evidence=parse_evidence_label(raw["evidence"]),
    )


def effort_by_work_category(journey: EngagementJourney) -> dict[WorkCategory, int]:
    totals: defaultdict[WorkCategory, int] = defaultdict(int)
    for stage in journey.stages:
        totals[stage.responsible_category] += stage.effort_hours
    return dict(totals)


def effort_by_stage_type(journey: EngagementJourney) -> dict[StageType, int]:
    totals: defaultdict[StageType, int] = defaultdict(int)
    for stage in journey.stages:
        totals[stage.stage_type] += stage.effort_hours
    return dict(totals)


def highest_effort_stage(journey: EngagementJourney) -> EngagementStage:
    return max(journey.stages, key=lambda stage: stage.effort_hours)


def longest_elapsed_stage(journey: EngagementJourney) -> EngagementStage:
    return max(journey.stages, key=lambda stage: stage.elapsed_days)


def load_journey_scenarios() -> tuple[JourneyScenario, ...]:
    baseline = load_baseline_journey()
    scenarios = []
    for raw in _fixture("journey_scenarios.json"):
        omitted = tuple(raw["omit_stage_ids"])
        journey = baseline if not omitted else replace(
            baseline,
            identifier=raw["journey_identifier"],
            name=raw["name"],
            description=raw["description"],
            stages=tuple(stage for stage in baseline.stages if stage.identifier not in omitted),
            evidence=parse_evidence_label(raw["evidence"]),
        )
        scenarios.append(JourneyScenario(
            key=raw["key"], name=raw["name"], journey=journey,
            changed_stage_ids=omitted, assumptions=tuple(raw["assumptions"]),
            evidence=parse_evidence_label(raw["evidence"]),
        ))
    return tuple(scenarios)
