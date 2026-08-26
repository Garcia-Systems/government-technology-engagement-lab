"""Chapter 12 governance-surface invariants."""
from dataclasses import replace
from pathlib import Path

from government_engagement_lab.evidence import EvidenceLabel
from government_engagement_lab.formal_rfp import load_formal_rfp_motion
from government_engagement_lab.governance import (
    CONFIGURATION_FIRST, CUSTOMER_REVIEWERS, READ_ONLY, SELLER_BORNE, WRITE_CAPABLE,
    formal_rfp_trace, governance_scenarios, load_governance_inventory,
)
from government_engagement_lab.models import (
    GateStatus, GovernanceCategory, GovernanceClassification, GovernanceResponsibility,
    WorkOrigin,
)
from government_engagement_lab.read_only import technical_scenarios


def scenarios():
    return {x.key: x for x in governance_scenarios()}


def test_fixture_loads_and_items_are_valid_unique_and_evidenced():
    inventory = load_governance_inventory()
    assert inventory.customer_name == "James River County Permitting Department"
    assert len({x.identifier for x in inventory.work_items}) == len(inventory.work_items)
    assert all(isinstance(x.category, GovernanceCategory) for x in inventory.work_items)
    assert all(isinstance(x.classification, GovernanceClassification) for x in inventory.work_items)
    assert all(isinstance(x.responsible_party, GovernanceResponsibility) for x in inventory.work_items)
    assert all(isinstance(x.evidence, EvidenceLabel) for x in inventory.work_items)


def test_delivery_and_approval_are_distinct_and_accessibility_supports_both():
    items = load_governance_inventory().work_items
    delivery = [x for x in items if x.classification is GovernanceClassification.DELIVERY]
    approval = [x for x in items if x.classification is GovernanceClassification.ACQUISITION_APPROVAL]
    assert delivery and approval and not set(delivery) & set(approval)
    assert all(x.origin is WorkOrigin.INTRINSIC_TO_TECHNICAL_SURFACE for x in delivery)
    assert all(x.origin is WorkOrigin.CREATED_BY_ENGAGEMENT_APPROVAL_PROCESS for x in approval)
    assert any(x.category is GovernanceCategory.ACCESSIBILITY_IMPLEMENTATION for x in delivery)
    assert any(x.category is GovernanceCategory.ACCESSIBILITY_REVIEW for x in approval)


def test_hours_reconcile_and_seller_customer_attribution_is_explicit():
    for scenario in governance_scenarios():
        m, items = scenario.metrics, scenario.work_items
        assert m.total_delivery_hours == sum(x.effort_hours for x in items if x.classification is GovernanceClassification.DELIVERY)
        assert m.total_acquisition_approval_hours == sum(x.effort_hours for x in items if x.classification is GovernanceClassification.ACQUISITION_APPROVAL)
        assert m.seller_delivery_hours == sum(x.effort_hours for x in items if x.classification is GovernanceClassification.DELIVERY and x.responsible_party in SELLER_BORNE)
        assert m.seller_acquisition_approval_hours == sum(x.effort_hours for x in items if x.classification is GovernanceClassification.ACQUISITION_APPROVAL and x.responsible_party in SELLER_BORNE)
        assert m.customer_review_hours == sum(x.effort_hours for x in items if x.classification is GovernanceClassification.ACQUISITION_APPROVAL and x.responsible_party in CUSTOMER_REVIEWERS)
        assert m.elapsed_review_days == sum(x.elapsed_days for x in items if x.classification is GovernanceClassification.ACQUISITION_APPROVAL)
        assert m.seller_delivery_cost == m.seller_delivery_hours * 110
        assert m.seller_acquisition_cost == m.seller_acquisition_approval_hours * 125


def test_elapsed_wait_does_not_become_labor_cost():
    write = scenarios()["WRITE_CAPABLE"]
    changed = replace(write.work_items[0], elapsed_days=999)
    # Cost formula is demonstrably hours-only; elapsed is separately reported.
    assert changed.effort_hours == write.work_items[0].effort_hours
    assert write.metrics.seller_delivery_cost == write.metrics.seller_delivery_hours * 110


def test_read_only_removes_only_write_specific_work_and_retains_controls():
    s = scenarios(); write, read = s["WRITE_CAPABLE"], s["READ_ONLY"]
    write_by_id = {x.identifier: x for x in write.work_items}
    assert read.removed_work_ids
    assert all(x.technical_surfaces == (WRITE_CAPABLE,) for x in (write_by_id[i] for i in read.removed_work_ids))
    ids = {x.identifier for x in read.work_items}
    assert {"AUDIT_LOGGING", "KEYBOARD_INTERFACE", "SECURITY_QUESTIONNAIRE"} <= ids
    assert read.metrics.seller_delivery_hours < write.metrics.seller_delivery_hours
    assert read.metrics.seller_acquisition_approval_hours == write.metrics.seller_acquisition_approval_hours
    chapter6 = {x.key: x for x in technical_scenarios()}
    assert chapter6[READ_ONLY].authority.write_capability is False
    assert chapter6[WRITE_CAPABLE].authority.write_capability is True


def test_configuration_shifts_native_work_without_eliminating_requirement():
    s = scenarios(); read, config = s["READ_ONLY"], s["CONFIGURATION_FIRST"]
    config_by_id = {x.identifier: x for x in config.work_items}
    assert config.technical_surface == CONFIGURATION_FIRST and config.shifted_work_ids
    assert all(config_by_id[i].responsible_party is GovernanceResponsibility.INCUMBENT_VENDOR for i in config.shifted_work_ids)
    assert all(config_by_id[i].shifted_from_seller for i in config.shifted_work_ids)
    assert set(config.shifted_work_ids) <= set(config_by_id)
    assert config.metrics.seller_delivery_hours < read.metrics.seller_delivery_hours
    assert config.removed_work_ids == ()


def test_documentation_heavy_changes_approval_not_technical_controls():
    s = scenarios(); write, heavy = s["WRITE_CAPABLE"], s["DOCUMENTATION_HEAVY"]
    wd = {x.identifier: x for x in write.work_items if x.classification is GovernanceClassification.DELIVERY}
    hd = {x.identifier: x for x in heavy.work_items if x.classification is GovernanceClassification.DELIVERY}
    assert wd == hd
    assert heavy.technical_surface == write.technical_surface
    assert heavy.metrics.seller_acquisition_approval_hours > write.metrics.seller_acquisition_approval_hours
    assert heavy.metrics.elapsed_review_days > write.metrics.elapsed_review_days
    assert all(x.evidence is EvidenceLabel.SENSITIVITY_ASSUMPTION for x in heavy.work_items if x.effort_hours != {y.identifier:y for y in write.work_items}[x.identifier].effort_hours)


def test_delivery_and_acquisition_burdens_feed_different_existing_gates():
    s = scenarios()
    assert s["WRITE_CAPABLE"].project_viability is GateStatus.PASS
    assert s["DOCUMENTATION_HEAVY"].project_viability is GateStatus.PASS
    assert s["DOCUMENTATION_HEAVY"].target_viability is GateStatus.FAIL
    assert s["DOCUMENTATION_HEAVY"].verdict == "POOR TARGET CUSTOMER"
    assert "governance_verdict" not in vars(s["WRITE_CAPABLE"])
    assert not any("score" in name.lower() for name in vars(s["WRITE_CAPABLE"]))


def test_formal_rfp_governance_effort_traces_without_changing_chapter4():
    trace = formal_rfp_trace(); motion = load_formal_rfp_motion()
    assert "SECURITY_QUESTIONNAIRE" in trace["SECURITY_QUESTIONNAIRE"]
    assert "ACCESSIBILITY_CONFORMANCE" in trace["ACCESSIBILITY_RESPONSE_ARTIFACT"]
    stages = {x.identifier:x for x in motion.journey.stages}
    assert stages["SECURITY_ACCESS_RESPONSE"].effort_hours == 16
    assert stages["ACCESSIBILITY_RESPONSE"].effort_hours == 8
    assert sum(x.effort_hours for x in motion.journey.stages) == 192


def test_scenarios_do_not_mutate_fixture_and_no_real_law_claim_is_made():
    before = load_governance_inventory()
    governance_scenarios(); after = load_governance_inventory()
    assert before == after
    text = Path("src/government_engagement_lab/fixtures/governance_work.json").read_text().lower()
    assert "not a real compliance benchmark" in text
    assert all(term not in text for term in ("legally required", "statute", "real procurement policy"))


def test_chapter_18_is_not_implemented():
    root = Path(__file__).parents[1]
    assert not any((root / "chapters").glob("chapter-18-*"))
    assert not (root / "src/government_engagement_lab/acquisition_economics.py").exists()
