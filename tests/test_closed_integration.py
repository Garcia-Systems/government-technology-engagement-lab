"""Chapter 13 closed-access invariants and economics."""
from dataclasses import replace
from decimal import Decimal
from pathlib import Path

from government_engagement_lab.closed_integration import (
    AccessMode, Completeness, Feasibility, Freshness, assess_closed_scenario,
    closed_integration_scenarios, evaluate_access, intervention_requirements,
    load_closed_fixture, load_closed_scenarios,
)
from government_engagement_lab.configuration import assess_configuration_first
from government_engagement_lab.evidence import EvidenceLabel
from government_engagement_lab.formal_rfp import load_formal_rfp_motion
from government_engagement_lab.models import GateStatus, WorkCategory


def assessments(): return {x.scenario.key: x for x in closed_integration_scenarios()}


def test_fixture_access_vocabulary_requirements_and_evidence_load():
    raw = load_closed_fixture(); scenarios = load_closed_scenarios(); reqs = intervention_requirements()
    assert raw["system_name"].endswith("(fictional)") and len(scenarios) == 5
    assert all(isinstance(c.mode, AccessMode) and isinstance(c.frequency, Freshness)
               and isinstance(c.completeness, Completeness) and isinstance(c.evidence, EvidenceLabel)
               for s in scenarios for c in s.capabilities)
    assert all(r.identifier and isinstance(r.required_fields, frozenset) for r in reqs)


def test_write_requirement_fails_and_does_not_run_original_economics():
    a = assessments()["CLOSED_WRITE"]
    assert a.preferred.requires_write
    assert a.preferred_feasibility.status is Feasibility.NOT_FEASIBLE
    assert "REQUIRED_WRITE_ACCESS_UNAVAILABLE" in a.preferred_feasibility.reasons
    # Economics, when present, belong only to the explicitly selected fallback.
    assert a.selected_fallback.identifier == "READ_ONLY_EDGE"
    assert a.preferred.identifier != a.selected_fallback.identifier


def test_read_only_export_is_feasible_never_writes_and_recalculates_value():
    a = assessments()["READ_ONLY_EXPORT"]
    assert a.selected_fallback.identifier == "READ_ONLY_EDGE"
    assert a.fallback_feasibility.status in (Feasibility.FEASIBLE, Feasibility.FEASIBLE_WITH_LIMITATIONS)
    assert not a.fallback_feasibility.capability.write_capability
    assert not a.selected_fallback.requires_write
    assert a.economics.value_addressed == Decimal("104002.80") * Decimal("0.58")
    assert a.economics.value_addressed <= Decimal("104002.80")
    assert a.verdict == "NARROW CUSTOM EDGE"


def test_manual_dependency_effort_freshness_support_and_verdict():
    a = assessments()["MANUAL_EXPORT_ONLY"]
    assert a.selected_fallback.identifier == "MANUAL_ASSISTED_VIEW"
    assert a.fallback_feasibility.capability.frequency is Freshness.WEEKLY
    assert "MANUAL_REFRESH_REQUIRED" in a.fallback_feasibility.reasons
    assert a.economics.annual_manual_hours == Decimal("26")
    assert a.economics.support_cost == Decimal("6050")
    assert a.scenario.annual_support == Decimal("8000")
    assert a.project_viability is GateStatus.FAIL and a.verdict == "NO DEAL"


def test_required_fields_and_incomplete_capability_can_fail():
    s = load_closed_scenarios()[1]; req = {x.identifier:x for x in intervention_requirements()}["READ_ONLY_EDGE"]
    cap = replace(s.capabilities[0], fields=frozenset({"permit_id"}), completeness=Completeness.PARTIAL)
    result = evaluate_access(req, (cap,))
    assert result.status is Feasibility.NOT_FEASIBLE
    assert any(x.startswith("REQUIRED_FIELDS_MISSING:") for x in result.reasons)


def test_configuration_reuses_chapter7_and_no_access_is_hard_stop():
    config = assessments()["CONFIGURATION_ONLY"]; chapter7 = assess_configuration_first()
    assert config.selected_fallback.identifier == "NATIVE_CONFIGURATION"
    assert config.economics.value_addressed == chapter7.economics.value_addressed
    assert config.verdict == "BUY / CONFIGURE"
    no = assessments()["NO_USABLE_ACCESS"]
    assert no.selected_fallback is None and no.economics is None
    assert no.project_viability is GateStatus.FAIL and no.verdict == "NO DEAL"


def test_precedence_determinism_no_invented_capability_and_fixture_immutability():
    before = load_closed_scenarios(); first = closed_integration_scenarios(); second = closed_integration_scenarios()
    assert first == second and before == load_closed_scenarios()
    assert load_closed_fixture()["fallback_precedence"] == ["NATIVE_CONFIGURATION", "APPROVED_READ_ONLY_ACCESS", "APPROVED_AUTOMATED_EXPORT", "APPROVED_MANUAL_EXPORT", "HUMAN_ASSISTED_WORKFLOW", "NO_DEAL"]
    assert assessments()["CONFIGURATION_ONLY"].selected_fallback.identifier == "NATIVE_CONFIGURATION"
    assert all(c.mode is AccessMode.NO_SUPPORTED_ACCESS for c in load_closed_scenarios()[-1].capabilities)


def test_labor_rates_governance_and_no_unauthorized_routes():
    rates = {x.category:x.hourly_cost for x in load_formal_rfp_motion().labor_rates}
    assert rates[WorkCategory.ENGINEERING] == Decimal("110") and rates[WorkCategory.SALES] == Decimal("85")
    read = assessments()["READ_ONLY_EXPORT"]
    assert read.governance_surface == "READ_ONLY" and "AUDIT_LOGGING" in read.governance_implications
    source = Path("src/government_engagement_lab/closed_integration.py").read_text().lower()
    forbidden = ("screen_scrape", "credential_sharing", "reverse_engineered_endpoint", "hidden_write", "unsupported_mutation")
    assert all(term not in source for term in forbidden)
    assert not any((Path("chapters")).glob("chapter-18-*"))
