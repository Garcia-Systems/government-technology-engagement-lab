from government_engagement_lab.baseline import load_baseline
from government_engagement_lab.evidence import EvidenceLabel
from government_engagement_lab.gates import baseline_gate_assessment
from government_engagement_lab.journey import load_baseline_journey
from government_engagement_lab.models import (
    AuthorityDomain, FindingCode, FrictionReason, GateDimension, RelationshipType,
    SponsorStrength, StakeholderRole,
)
from government_engagement_lab.stakeholders import (
    coordination_dependency_count, load_baseline_topology, load_stakeholder_scenarios,
    stakeholder_friction_trace, summarize_topology,
)


def test_fixture_loads_and_references_are_typed_unique_and_valid() -> None:
    topology = load_baseline_topology()
    ids = {p.identifier for p in topology.stakeholders}
    stages = {s.identifier for s in load_baseline_journey().stages}
    assert len(ids) == len(topology.stakeholders)
    assert all(set(p.journey_stage_ids) <= stages for p in topology.stakeholders)
    assert all(isinstance(role, StakeholderRole) for p in topology.stakeholders for role in p.roles)
    assert all(isinstance(r.relationship_type, RelationshipType) for r in topology.relationships)
    assert all({r.source_id, r.target_id} <= ids for r in topology.relationships)
    for stage in topology.stages:
        assert set(stage.approver_ids + stage.blocker_ids + stage.technical_gatekeeper_ids) <= ids


def test_baseline_exposes_distinct_authorities_and_limited_sponsor() -> None:
    topology = load_baseline_topology()
    sponsor = next(p for p in topology.stakeholders if StakeholderRole.SPONSOR in p.roles)
    assert topology.sponsor_strength is SponsorStrength.LIMITED
    assert AuthorityDomain.PROBLEM_OWNER in sponsor.approval_authority
    assert AuthorityDomain.CONTRACT_APPROVER not in sponsor.approval_authority
    assert any(StakeholderRole.TECHNICAL_GATEKEEPER in p.roles for p in topology.stakeholders)
    assert any(r.relationship_type is RelationshipType.REQUIRES_APPROVAL_FROM and
               r.target_id in {"PROCUREMENT_REPRESENTATIVE", "LEGAL_CONTRACTS_REPRESENTATIVE"}
               for r in topology.relationships)


def test_summary_reconciles_and_extremes_are_deterministic() -> None:
    topology, summary = load_baseline_topology(), summarize_topology(load_baseline_topology())
    assert summary.stakeholder_count == len(topology.stakeholders)
    assert summary.role_assignment_count == sum(len(p.roles) for p in topology.stakeholders)
    assert summary.approval_dependency_count == sum(len(s.approver_ids) for s in topology.stages)
    assert summary.blocking_dependency_count == sum(len(s.blocker_ids) for s in topology.stages)
    assert summary.technical_access_dependency_count == sum(len(s.technical_gatekeeper_ids) for s in topology.stages)
    counts = {p.identifier: len(p.journey_stage_ids) for p in topology.stakeholders}
    assert set(summary.most_involved_stakeholder_ids) == {k for k, v in counts.items() if v == max(counts.values())}
    stage_counts = dict(summary.participants_per_stage)
    assert set(summary.highest_participation_stage_ids) == {k for k, v in stage_counts.items() if v == max(stage_counts.values())}
    assert not hasattr(summary, "score") and not hasattr(topology, "weighted_score")


def test_chapter_one_friction_traces_to_explicit_topology_findings() -> None:
    reasons = baseline_gate_assessment().gate(GateDimension.TARGET_ATTRACTIVENESS).reasons
    friction = next(r for r in reasons if r.code is FindingCode.STAKEHOLDER_FRICTION)
    assert set(stakeholder_friction_trace()) >= {
        FrictionReason.MULTIPLE_REQUIRED_APPROVALS,
        FrictionReason.ACCESS_CONTROL_DEPENDENCY,
        FrictionReason.CROSS_FUNCTIONAL_COORDINATION,
    }
    assert all(reason.value in friction.explanation for reason in stakeholder_friction_trace())


def test_authority_sensitivities_change_mechanisms_not_project() -> None:
    scenarios = {s.key: s for s in load_stakeholder_scenarios()}
    baseline, strong = scenarios["BASELINE"], scenarios["STRONG_SPONSOR"]
    fragmented, absent = scenarios["FRAGMENTED_AUTHORITY"], scenarios["NO_SPONSOR"]
    assert coordination_dependency_count(strong.topology) < coordination_dependency_count(baseline.topology)
    assert summarize_topology(strong.topology).approval_dependency_count < summarize_topology(baseline.topology).approval_dependency_count
    for identifier in ("IT_REPRESENTATIVE", "SECURITY_REVIEWER", "PROCUREMENT_REPRESENTATIVE"):
        assert next(p.roles for p in strong.topology.stakeholders if p.identifier == identifier) == next(p.roles for p in baseline.topology.stakeholders if p.identifier == identifier)
    assert summarize_topology(fragmented.topology).approval_dependency_count > summarize_topology(baseline.topology).approval_dependency_count
    assert summarize_topology(fragmented.topology).blocking_dependency_count > summarize_topology(baseline.topology).blocking_dependency_count
    assert absent.topology.sponsor_strength is SponsorStrength.ABSENT
    assert not any(StakeholderRole.SPONSOR in p.roles for p in absent.topology.stakeholders)
    assert absent.topology.technical_project_identifier == baseline.topology.technical_project_identifier
    assert absent.verdict != "NO DEAL"
    assert load_baseline().conditions.technical_feasibility
    assert all(s.evidence in {EvidenceLabel.MODELED_ASSUMPTION, EvidenceLabel.SENSITIVITY_ASSUMPTION} for s in scenarios.values())
    assert all("SENSITIVITY ASSUMPTION" in change for s in tuple(scenarios.values())[1:] for change in s.changed_assumptions)
