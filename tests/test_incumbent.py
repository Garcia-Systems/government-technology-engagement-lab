from dataclasses import replace
from government_engagement_lab.configuration import BURDEN
from government_engagement_lab.evidence import EvidenceLabel
from government_engagement_lab.incumbent import (
    AlternativeType, assess_alternative, burden_values, calculate_alternative_economics,
    chapter13_access_is_closed, compare_alternatives, incumbent_scenarios, is_adequate,
    load_alternatives, load_incumbent_fixture, select_result,
)


def test_fixture_is_explicitly_fictional_and_loads():
    fixture = load_incumbent_fixture()
    assert "wholly fictional" in fixture["fiction_notice"]
    assert "CivicFlow" in fixture["provider"] and "fictional" in fixture["provider"]


def test_alternative_taxonomy_ids_categories_costs_and_evidence_are_valid():
    alternatives = load_alternatives()
    assert len({x.identifier for x in alternatives}) == len(alternatives) == 6
    assert {x.alternative_type for x in alternatives} == set(AlternativeType)
    assert all(set(x.value_categories) <= set(burden_values()) for x in alternatives)
    assert all(x.implementation_price >= 0 and x.recurring_fee >= 0 for x in alternatives)
    assert all(x.evidence is EvidenceLabel.MODELED_ALTERNATIVE_ASSUMPTION for x in alternatives)


def test_value_residual_and_first_year_economics_do_not_double_count():
    item = next(x for x in load_alternatives() if x.identifier == "INCUMBENT_MODULE")
    duplicate = replace(item, value_categories=item.value_categories + ("status_reconciliation",))
    economics = calculate_alternative_economics(duplicate)
    expected = sum(dict(BURDEN)[x] for x in set(item.value_categories))
    total = sum(x for _, x in BURDEN)
    assert economics.annual_value_addressed == expected
    assert economics.residual_value == total - expected
    assert economics.annual_value_addressed <= total
    assert economics.first_year_customer_cost == item.implementation_price + item.recurring_fee
    assert economics.first_year_net_recoverable_value == expected - economics.first_year_customer_cost


def test_documented_adequacy_rule_requires_both_conditions():
    module = next(x for x in compare_alternatives() if x.alternative.identifier == "INCUMBENT_MODULE")
    assert module.adequate and is_adequate(module.economics)
    weak = replace(module.alternative, value_categories=("status_reconciliation",))
    assert not is_adequate(calculate_alternative_economics(weak))


def test_sensitivities_change_only_disclosed_dimensions_and_do_not_mutate_fixture():
    before = load_incumbent_fixture()
    credible, strong, weak, expensive, access = incumbent_scenarios()
    base = next(x for x in credible.assessments if x.alternative.identifier == "INCUMBENT_MODULE")
    high = next(x for x in strong.assessments if x.alternative.identifier == "INCUMBENT_MODULE")
    low = next(x for x in weak.assessments if x.alternative.identifier == "INCUMBENT_MODULE")
    costly = next(x for x in expensive.assessments if x.alternative.identifier == "INCUMBENT_MODULE")
    assert high.economics.percent_addressed > base.economics.percent_addressed
    assert low.economics.percent_addressed < base.economics.percent_addressed
    assert costly.alternative.value_categories == base.alternative.value_categories
    assert costly.economics.first_year_customer_cost > base.economics.first_year_customer_cost
    assert load_incumbent_fixture() == before
    assert strong.selected_result == "BUY / CONFIGURE"
    assert weak.selected_result == "NARROW CUSTOM EDGE"
    assert access.selected_result == "BUY / CONFIGURE"


def test_closed_access_cannot_be_bypassed_but_native_access_remains():
    assert chapter13_access_is_closed()
    assessments = compare_alternatives(third_party_access=False)
    assert all(not x.feasible for x in assessments if x.alternative.custom_ownership_required)
    assert all(x.feasible for x in assessments if not x.alternative.custom_ownership_required)


def test_results_are_derived_and_no_deal_remains_possible():
    items = load_alternatives()
    assert select_result(compare_alternatives()) == "BUY / CONFIGURE"
    native_failed = tuple(replace(x, supportable=False) if not x.custom_ownership_required else
                          replace(x, supportable=False, acquisition_viable=False) for x in items)
    assessed = compare_alternatives(native_failed, third_party_access=False)
    assert select_result(assessed) == "NO DEAL"
    edge = next(x for x in items if x.alternative_type is AlternativeType.CUSTOM_EDGE)
    assert assess_alternative(edge).commercial_result == "NARROW CUSTOM EDGE"


def test_governance_and_ownership_are_explicit_without_weighted_score():
    items = load_alternatives()
    module = next(x for x in items if x.identifier == "INCUMBENT_MODULE")
    edge = next(x for x in items if x.identifier == "NARROW_CUSTOM_EDGE")
    assert module.governance_surface == "CONFIGURATION_FIRST" and module.support_owner == "INCUMBENT_VENDOR"
    assert edge.governance_surface == "READ_ONLY" and edge.custom_ownership_required
    assert not hasattr(module, "score") and not hasattr(compare_alternatives()[0], "weighted_score")


def test_chapter_15_is_not_implemented():
    from pathlib import Path
    assert not Path("chapters/chapter-15-acquisition-economics.md").exists()
    assert not Path("src/government_engagement_lab/acquisition_economics.py").exists()
