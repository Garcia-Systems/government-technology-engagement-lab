from copy import deepcopy
from decimal import Decimal

from government_engagement_lab.evidence import EvidenceLabel
from government_engagement_lab.formal_rfp import load_formal_rfp_motion
from government_engagement_lab.read_only import (SourceAccessMode, assess_technical_scenario,
    load_read_only_fixture, no_authoritative_write_path_exists, process_read_only_export,
    technical_scenarios)
from government_engagement_lab.stakeholders import load_baseline_topology


def test_fixture_pure_deterministic_processing_and_traceability():
    fixture = load_read_only_fixture(); original = deepcopy(fixture)
    first = process_read_only_export(fixture); second = process_read_only_export(fixture)
    assert fixture == original and first == second and first.source_unchanged
    assert len(first.normalized_records) == 8 and len(first.exceptions) == 4 and len(first.duplicates) == 1
    ids = {x["record_id"] for x in fixture["records"]}
    assert all(x.provenance.source_record_identifier in ids for x in first.normalized_records)
    assert all(x.provenance.source_identifier == fixture["source_identifier"] for x in first.normalized_records)


def test_authority_boundary_and_modeled_write_comparison():
    write, read, _, _ = technical_scenarios()
    assert set(SourceAccessMode) == {SourceAccessMode.EXPORT_ONLY, SourceAccessMode.READ_ONLY_API, SourceAccessMode.WRITE_NON_AUTHORITATIVE, SourceAccessMode.WRITE_AUTHORITATIVE}
    assert not read.authority.write_capability and not read.authority.authoritative_system_mutation_allowed
    assert not read.authority.consequential_action_allowed and no_authoritative_write_path_exists()
    assert write.authority.write_capability and assess_technical_scenario(write).processing is None


def test_assumptions_effort_rates_economics_and_sensitivities():
    write, read, low, hard = technical_scenarios()
    assert read.value_capture_fraction <= Decimal("1") and read.value_capture_evidence is EvidenceLabel.MODELED_ASSUMPTION
    assert read.engineering_hours == sum(x.hours for x in read.engineering_work) == 110
    assert read.engineering_hours < write.engineering_hours
    assert load_formal_rfp_motion().labor_rates == load_formal_rfp_motion().labor_rates
    base, low_result, hard_result = map(assess_technical_scenario, (read, low, hard))
    assert base.economics.value_addressed == Decimal("57201.5400")
    assert base.economics.first_year_customer_cost == Decimal("40000")
    assert base.economics.modeled_net_recoverable_value == Decimal("17201.5400")
    assert base.economics.seller.delivery_labor_cost == Decimal("12100")
    assert low_result.economics.modeled_net_recoverable_value < base.economics.modeled_net_recoverable_value
    assert low_result.verdict == "NO DEAL" and low.value_capture_evidence is EvidenceLabel.SENSITIVITY_ASSUMPTION
    assert hard.authority == read.authority and hard_result.economics.elapsed_days > base.economics.elapsed_days
    assert hard_result.verdict == "NO DEAL" and hard.evidence is EvidenceLabel.SENSITIVITY_ASSUMPTION


def test_acceptance_governance_stakeholders_and_journey_isolation():
    write, read, _, _ = technical_scenarios(); result = assess_technical_scenario(read)
    assert result.acceptance_passed
    assert not read.governance.write_approval and write.governance.write_approval
    assert not hasattr(read.governance, "score")
    topology = {x.identifier for x in load_baseline_topology().stakeholders}
    assert {x.stakeholder_id for x in read.stakeholders} <= topology
    ids = {x.identifier for x in read.journey.stages}
    assert {"TECHNICAL_VALIDATION", "SECURITY_ACCESS_REVIEW", "PURCHASING_PATH", "AGREEMENT_AUTHORIZATION"} <= ids
    assert read.journey.total_elapsed_days < write.journey.total_elapsed_days
    assert technical_scenarios()[1] == read  # scenario construction never mutates its baseline
