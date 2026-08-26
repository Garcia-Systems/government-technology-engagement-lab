"""Chapter 8 small-departmental engagement and contract-size economics."""

from dataclasses import dataclass
from decimal import Decimal

from .baseline import _fixture, load_baseline
from .evidence import EvidenceLabel, parse_evidence_label
from .formal_rfp import load_formal_rfp_motion
from .gates import aggregate_viability, determine_verdict
from .models import (EngagementJourney, EngagementMotion, EngagementScale,
                     EngagementStage, GateStatus, LaborCostRate, SellerEconomics,
                     StageType, WorkCategory)
from .stakeholders import load_baseline_topology


@dataclass(frozen=True)
class ScopeBoundary:
    department_team: str
    user_count: int
    workflow_slice: str
    data_sources: tuple[str, ...]
    technical_authority: str
    included_features: tuple[str, ...]
    excluded_features: tuple[str, ...]
    implementation_duration_days: int
    support_boundary: str
    acceptance_boundary: str
    evidence: EvidenceLabel


@dataclass(frozen=True)
class EngineeringWorkItem:
    name: str
    hours: int


@dataclass(frozen=True)
class SmallEngagement:
    key: str
    name: str
    customer_name: str
    scale: EngagementScale
    scope: ScopeBoundary
    value_fraction: Decimal
    implementation_price: Decimal
    annual_support_revenue: Decimal
    support_hours: int
    other_direct_cost: Decimal
    engineering_work: tuple[EngineeringWorkItem, ...]
    journey: EngagementJourney
    stakeholder_ids: tuple[str, ...]
    labor_rates: tuple[LaborCostRate, ...]
    minimum_contribution: Decimal
    customer_price_rule: str
    changed_assumptions: tuple[str, ...]
    evidence: EvidenceLabel

    @property
    def engineering_hours(self) -> int:
        return sum(item.hours for item in self.engineering_work)

    @property
    def acquisition_stages(self) -> tuple[EngagementStage, ...]:
        return tuple(stage for stage in self.journey.stages if stage.identifier != "IMPLEMENTATION")

    @property
    def acquisition_hours(self) -> int:
        return sum(stage.effort_hours for stage in self.acquisition_stages)


@dataclass(frozen=True)
class SmallCustomerEconomics:
    original_recoverable_value: Decimal
    percent_original_value_addressed: Decimal
    annual_value_addressed: Decimal
    implementation_price: Decimal
    annual_support: Decimal
    first_year_cost: Decimal
    net_recoverable_value: Decimal
    implementation_payback_months: Decimal
    customer_supported_price: Decimal
    evidence: EvidenceLabel = EvidenceLabel.OBSERVED_LAB_RESULT


@dataclass(frozen=True)
class ScaleRatios:
    acquisition_hours_per_implementation_revenue: Decimal
    acquisition_cost_per_implementation_revenue: Decimal
    engineering_hours_per_implementation_revenue: Decimal
    value_addressed_per_price: Decimal
    contribution_per_price: Decimal


@dataclass(frozen=True)
class SmallEngagementAssessment:
    engagement: SmallEngagement
    customer: SmallCustomerEconomics
    seller: SellerEconomics
    support_cost: Decimal
    support_contribution: Decimal
    seller_break_even_price: Decimal
    ratios: ScaleRatios
    project_viability: GateStatus
    target_viability: GateStatus
    verdict: str
    evidence: EvidenceLabel = EvidenceLabel.OBSERVED_LAB_RESULT


def _scope(raw: dict) -> ScopeBoundary:
    return ScopeBoundary(raw["department_team"], raw["user_count"], raw["workflow_slice"],
        tuple(raw["data_sources"]), raw["technical_authority"], tuple(raw["included_features"]),
        tuple(raw["excluded_features"]), raw["implementation_duration_days"], raw["support_boundary"],
        raw["acceptance_boundary"], parse_evidence_label(raw["evidence"]))


def _load_raw() -> dict:
    return _fixture("small_engagement.json")


def load_small_engagement_scenarios() -> tuple[SmallEngagement, ...]:
    raw = _load_raw()
    source = {item["key"]: item for item in raw["scenarios"]}
    built: list[SmallEngagement] = []
    baseline_scope = source["SMALL_BASELINE"]["scope"]
    baseline = source["SMALL_BASELINE"]
    evidence = parse_evidence_label(raw["evidence"])
    rates = tuple(LaborCostRate(WorkCategory(k), Decimal(v), evidence)
                  for k, v in raw["labor_rates"].items())
    # Chapter 8 deliberately reuses Chapter 4's seller-rate assumptions.
    if {(r.category, r.hourly_cost) for r in rates} != {(r.category, r.hourly_cost) for r in load_formal_rfp_motion().labor_rates}:
        raise ValueError("Chapter 8 labor rates must remain consistent with prior chapters")
    valid_people = {person.identifier for person in load_baseline_topology().stakeholders}
    for item in raw["scenarios"]:
        merged = baseline | item
        scope_raw = baseline_scope | item.get("scope_changes", {})
        stage_effort = item.get("stage_effort_overrides", {})
        stage_days = item.get("stage_day_overrides", {})
        stages = tuple(EngagementStage(s[0], s[1], "Bounded departmental journey stage.", n,
            True, stage_effort.get(s[0], s[2]), stage_days.get(s[0], s[3]), WorkCategory(s[4]),
            StageType(s[5]), parse_evidence_label(item["evidence"]),
            ("Explicit fictional stage effort; required stages do not disappear when delivery shrinks.",))
            for n, s in enumerate(baseline["stages"], 1))
        journey = EngagementJourney(f'{item["key"]}_JOURNEY', item["name"],
            "A bounded but authorized small-department buying journey.", raw["customer_name"],
            EngagementMotion.SMALL_DEPARTMENTAL, stages, raw["modeled_days_per_month"],
            parse_evidence_label(item["evidence"]))
        stakeholders = tuple(merged["stakeholder_ids"])
        if not set(stakeholders) <= valid_people:
            raise ValueError("small-engagement stakeholder reference is invalid")
        built.append(SmallEngagement(item["key"], item["name"], raw["customer_name"],
            EngagementScale(item["scale"]), _scope(scope_raw), Decimal(merged["value_fraction"]),
            Decimal(merged["implementation_price"]), Decimal(merged["annual_support_revenue"]),
            merged["support_hours"], Decimal(merged["other_direct_cost"]),
            tuple(EngineeringWorkItem(x[0], x[1]) for x in merged["engineering_work"]), journey,
            stakeholders, rates, Decimal(raw["minimum_contribution"]), raw["customer_price_rule"],
            tuple(item.get("changed_assumptions", ())), parse_evidence_label(item["evidence"])))
    return tuple(built)


def load_small_engagement() -> SmallEngagement:
    return load_small_engagement_scenarios()[0]


def assess_small_engagement(engagement: SmallEngagement | None = None) -> SmallEngagementAssessment:
    engagement = engagement or load_small_engagement()
    original = load_baseline().burden.annual_recoverable_value
    value = original * engagement.value_fraction
    supported_price = max(Decimal(), value - engagement.annual_support_revenue)
    first_year = engagement.implementation_price + engagement.annual_support_revenue
    customer = SmallCustomerEconomics(original, engagement.value_fraction * Decimal(100), value,
        engagement.implementation_price, engagement.annual_support_revenue, first_year, value - first_year,
        engagement.implementation_price / value * Decimal(12), supported_price)
    rates = {rate.category: rate.hourly_cost for rate in engagement.labor_rates}
    delivery = Decimal(engagement.engineering_hours) * rates[WorkCategory.ENGINEERING]
    acquisition = sum((Decimal(stage.effort_hours) * rates[stage.responsible_category]
                       for stage in engagement.acquisition_stages), Decimal())
    support_cost = Decimal(engagement.support_hours) * rates[WorkCategory.ENGINEERING]
    contribution = engagement.implementation_price - delivery - acquisition - engagement.other_direct_cost
    seller = SellerEconomics(engagement.implementation_price, delivery, acquisition,
        engagement.other_direct_cost, contribution, contribution / engagement.implementation_price,
        EvidenceLabel.OBSERVED_LAB_RESULT)
    break_even = delivery + acquisition + engagement.other_direct_cost + engagement.minimum_contribution
    project = aggregate_viability((
        GateStatus.PASS if value > 0 else GateStatus.FAIL,
        GateStatus.PASS,  # inherited read-only/configuration-first feasibility
        GateStatus.PASS if engagement.implementation_price <= supported_price else GateStatus.FAIL,
        GateStatus.PASS if engagement.implementation_price - delivery - engagement.other_direct_cost >= engagement.minimum_contribution else GateStatus.FAIL,
        GateStatus.PASS if engagement.annual_support_revenue >= support_cost else GateStatus.FAIL,
    ))
    target = GateStatus.PASS if contribution >= engagement.minimum_contribution else GateStatus.FAIL
    ratios = ScaleRatios(Decimal(engagement.acquisition_hours) / engagement.implementation_price,
        acquisition / engagement.implementation_price,
        Decimal(engagement.engineering_hours) / engagement.implementation_price,
        value / engagement.implementation_price, contribution / engagement.implementation_price)
    return SmallEngagementAssessment(engagement, customer, seller, support_cost,
        engagement.annual_support_revenue - support_cost, break_even, ratios, project, target,
        determine_verdict(project, target))


def assess_small_engagement_scenarios() -> tuple[SmallEngagementAssessment, ...]:
    return tuple(assess_small_engagement(item) for item in load_small_engagement_scenarios())
