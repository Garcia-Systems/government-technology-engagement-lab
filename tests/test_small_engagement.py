from dataclasses import fields
from decimal import Decimal

from government_engagement_lab.baseline import load_baseline
from government_engagement_lab.evidence import EvidenceLabel
from government_engagement_lab.formal_rfp import load_formal_rfp_motion
from government_engagement_lab.models import EngagementScale, GateStatus
from government_engagement_lab.small_engagement import (
    assess_small_engagement, assess_small_engagement_scenarios,
    load_small_engagement, load_small_engagement_scenarios)


def test_fixture_loads_with_explicit_bounded_scope():
    engagement = load_small_engagement()
    scope = engagement.scope
    assert engagement.scale is EngagementScale.SMALL_DEPARTMENTAL
    assert scope.department_team and scope.user_count == 8 and scope.workflow_slice
    assert scope.data_sources and scope.technical_authority
    assert scope.included_features and scope.excluded_features
    assert set(scope.included_features).isdisjoint(scope.excluded_features)
    assert scope.implementation_duration_days and scope.support_boundary and scope.acceptance_boundary
    assert scope.evidence is EvidenceLabel.MODELED_ASSUMPTION


def test_value_engineering_and_acquisition_have_visible_sources():
    engagement = load_small_engagement()
    assessment = assess_small_engagement(engagement)
    assert assessment.customer.annual_value_addressed == Decimal("43681.1760")
    assert assessment.customer.annual_value_addressed < load_baseline().burden.annual_recoverable_value
    assert engagement.engineering_hours == sum(x.hours for x in engagement.engineering_work) == 120
    assert engagement.acquisition_hours == sum(x.effort_hours for x in engagement.acquisition_stages) == 58
    assert {x.identifier for x in engagement.acquisition_stages} >= {
        "BOUNDED_DISCOVERY", "TECHNICAL_ACCESS_REVIEW", "PURCHASING_AUTHORIZATION", "CONTRACT"}


def test_rates_and_economics_calculate_transparently():
    engagement = load_small_engagement(); result = assess_small_engagement(engagement)
    assert [(x.category, x.hourly_cost) for x in engagement.labor_rates] == [
        (x.category, x.hourly_cost) for x in load_formal_rfp_motion().labor_rates]
    assert result.customer.first_year_cost == Decimal("34000")
    assert result.customer.net_recoverable_value == Decimal("9681.1760")
    assert result.customer.customer_supported_price == Decimal("39681.1760")
    assert result.seller.delivery_labor_cost == Decimal("13200")
    assert result.seller.acquisition_labor_cost == Decimal("5970")
    assert result.seller.acquisition_adjusted_contribution == Decimal("9830")
    assert result.seller.contribution_margin == Decimal("9830") / Decimal("30000")
    assert result.seller_break_even_price == Decimal("30170")
    assert result.support_cost == Decimal("3300")
    assert result.customer.customer_supported_price != result.seller_break_even_price


def test_sensitivities_change_named_mechanisms_without_mutating_baseline():
    scenarios = load_small_engagement_scenarios()
    baseline, too_small, efficient, support = scenarios
    before = load_small_engagement()
    assert too_small.implementation_price < baseline.implementation_price
    assert too_small.scope.user_count < baseline.scope.user_count
    assert too_small.engineering_hours < baseline.engineering_hours
    assert too_small.acquisition_hours == baseline.acquisition_hours  # explicit stage floor remains
    assert efficient.scope == baseline.scope and efficient.engineering_work == baseline.engineering_work
    assert efficient.acquisition_hours < baseline.acquisition_hours
    assert support.scope == baseline.scope and support.engineering_work == baseline.engineering_work
    assert support.support_hours > baseline.support_hours
    assert load_small_engagement() == before
    assert all(x.evidence in {EvidenceLabel.MODELED_ASSUMPTION, EvidenceLabel.SENSITIVITY_ASSUMPTION} for x in scenarios)


def test_small_does_not_hard_code_either_verdict_and_project_target_are_distinct():
    baseline, too_small, efficient, high_support = assess_small_engagement_scenarios()
    assert baseline.project_viability is GateStatus.PASS
    assert baseline.target_viability is GateStatus.FAIL
    assert baseline.verdict == "POOR TARGET CUSTOMER"
    assert too_small.verdict == "NO DEAL"
    assert efficient.verdict == "PROMISING — VALIDATE IN DISCOVERY"
    assert high_support.project_viability is GateStatus.FAIL
    assert high_support.verdict == "NO DEAL"


def test_no_contract_size_score_or_chapter_nine_model_exists():
    assert "score" not in {field.name for field in fields(type(load_small_engagement()))}
    import government_engagement_lab.models as models
    assert not hasattr(models.EngagementMotion, "LARGER_CONTRACT")
