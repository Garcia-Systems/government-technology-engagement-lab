from dataclasses import asdict

from government_engagement_lab.repeatability import (ReuseDimension, ReuseState,
    assess_repeat_department, load_repeatability_fixture, repeat_department_scenarios)


def test_second_department_is_fictional_and_distinct():
    source, target, _, _ = load_repeatability_fixture()
    assert target.fictional and "no real locality" in target.fiction_notice
    assert source.identifier != target.identifier
    assert source.workflow != target.workflow
    assert "Reinspection" in target.workflow


def test_artifact_model_is_explicit_and_valid():
    source, target, artifacts, _ = load_repeatability_fixture()
    assert len({a.identifier for a in artifacts}) == len(artifacts)
    assert {a.dimension for a in artifacts} == set(ReuseDimension)
    assert {a.state for a in artifacts} <= set(ReuseState)
    assert all(a.source_department == source.identifier and a.target_department == target.identifier for a in artifacts)
    assert all(a.adaptation_effort < a.first_department_effort for a in artifacts if a.state is ReuseState.REUSE_AS_IS)
    assert all(a.adaptation_effort > 0 for a in artifacts if a.state is ReuseState.ADAPT)
    assert all(a.hours_saved == 0 for a in artifacts if a.state is ReuseState.REBUILD)


def test_dimension_and_total_calculations_reconcile():
    a = assess_repeat_department()
    for summary in a.summaries:
        artifacts = [x for x in a.artifacts if x.dimension is summary.dimension]
        assert summary.greenfield_hours == sum(x.first_department_effort for x in artifacts)
        assert summary.hours_required == sum(x.adaptation_effort for x in artifacts)
        assert summary.hours_saved == summary.greenfield_hours - summary.hours_required
    assert a.engineering_greenfield_hours == 138
    assert a.engineering_hours == 53
    assert a.discovery_hours == 18
    assert a.acquisition_hours == 42
    assert a.governance_hours == 23
    assert a.support_hours == 14
    assert a.total_effort_hours == sum((a.engineering_hours, a.discovery_hours, a.acquisition_hours, a.governance_hours, a.support_hours))


def test_document_reuse_does_not_reuse_approval_or_authorization():
    a = assess_repeat_department()
    by_id = {x.identifier: x for x in a.artifacts}
    assert by_id["SECURITY_NARRATIVE"].state is ReuseState.ADAPT
    assert by_id["SECURITY_APPROVAL"].state is ReuseState.REBUILD
    assert by_id["PURCHASING_PATH"].state is ReuseState.REUSE_AS_IS
    assert by_id["DEPARTMENT_AUTHORIZATION"].state is ReuseState.REBUILD


def test_support_and_marginal_economics_are_explicit():
    a = assess_repeat_department()
    assert a.economics.support_cost == a.support_hours * 70
    expected = (a.economics.implementation_price + a.economics.annual_support_revenue
                - a.economics.delivery_cost - a.economics.acquisition_cost
                - a.economics.governance_cost - a.economics.support_cost
                - a.economics.other_direct_cost)
    assert a.economics.marginal_contribution == expected
    assert a.economics.customer_net_value == 12000


def test_scenarios_preserve_intended_tradeoffs_and_fixture():
    before = asdict(assess_repeat_department())
    baseline, commercial_reset, technical_variation, strong = repeat_department_scenarios()
    assert commercial_reset.engineering_hours == baseline.engineering_hours
    assert commercial_reset.acquisition_hours > baseline.acquisition_hours
    assert technical_variation.acquisition_hours < baseline.acquisition_hours
    assert technical_variation.engineering_hours > baseline.engineering_hours
    assert strong.total_effort_hours < baseline.total_effort_hours
    assert asdict(assess_repeat_department()) == before


def test_interpretation_requires_multidimensional_reuse_and_is_not_product():
    baseline, commercial_reset, _, strong = repeat_department_scenarios()
    assert baseline.structural_interpretation == "REPEATABLE PROJECT"
    assert commercial_reset.structural_interpretation != "REPEATABLE PROJECT"
    assert all("PRODUCT" not in a.structural_interpretation for a in repeat_department_scenarios())
    assert not hasattr(baseline, "reuse_score")
    assert not hasattr(baseline, "product_economics")


def test_chapter_18_not_implemented():
    import government_engagement_lab.cli as cli
    assert not hasattr(cli, "show_repeat_government")
