"""Chapter 3 stakeholder topology, validation, and descriptive calculations."""

from dataclasses import replace

from .baseline import _fixture
from .evidence import EvidenceLabel, parse_evidence_label
from .journey import load_baseline_journey
from .models import (
    AuthorityDomain, FrictionReason, RelationshipType, SponsorStrength,
    StageStakeholders, Stakeholder, StakeholderFrictionFinding,
    StakeholderRelationship, StakeholderRole, StakeholderScenario,
    StakeholderSummary, StakeholderTopology,
)


def _stakeholder(raw: dict) -> Stakeholder:
    return Stakeholder(
        raw["identifier"], raw["display_name"], raw["organizational_function"],
        tuple(StakeholderRole(value) for value in raw["roles"]),
        tuple(raw["journey_stage_ids"]),
        tuple(AuthorityDomain(value) for value in raw["approval_authority"]),
        tuple(AuthorityDomain(value) for value in raw["blocking_authority"]),
        raw["access_control_domain"], parse_evidence_label(raw["evidence"]), raw["notes"],
    )


def _relationship(raw: dict) -> StakeholderRelationship:
    return StakeholderRelationship(
        raw["source_id"], raw["target_id"], RelationshipType(raw["relationship_type"]),
        tuple(raw["stage_ids"]), raw["explanation"], parse_evidence_label(raw["evidence"]),
    )


def _stage(raw: dict) -> StageStakeholders:
    return StageStakeholders(
        raw["stage_id"], raw["primary_responsible_id"], tuple(raw["participant_ids"]),
        tuple(raw["approver_ids"]), tuple(raw["blocker_ids"]),
        tuple(raw["technical_gatekeeper_ids"]),
    )


def _finding(raw: dict) -> StakeholderFrictionFinding:
    return StakeholderFrictionFinding(
        FrictionReason(raw["reason"]), tuple(raw["stakeholder_ids"]),
        tuple(raw["stage_ids"]), raw["explanation"], parse_evidence_label(raw["evidence"]),
    )


def validate_topology(topology: StakeholderTopology) -> None:
    """Reject dangling stakeholder/stage references and inconsistent participation."""
    stakeholder_ids = [item.identifier for item in topology.stakeholders]
    if len(stakeholder_ids) != len(set(stakeholder_ids)):
        raise ValueError("stakeholder identifiers must be unique")
    valid_people = set(stakeholder_ids)
    valid_stages = {stage.identifier for stage in load_baseline_journey().stages}
    for person in topology.stakeholders:
        if not set(person.journey_stage_ids) <= valid_stages:
            raise ValueError(f"invalid journey stage for {person.identifier}")
    for relation in topology.relationships:
        if {relation.source_id, relation.target_id} - valid_people or set(relation.stage_ids) - valid_stages:
            raise ValueError("relationship contains a dangling reference")
    for stage in topology.stages:
        refs = {stage.primary_responsible_id, *stage.participant_ids, *stage.approver_ids,
                *stage.blocker_ids, *stage.technical_gatekeeper_ids}
        if stage.stage_id not in valid_stages or refs - valid_people:
            raise ValueError("stage topology contains a dangling reference")
        if stage.primary_responsible_id not in stage.participant_ids:
            raise ValueError("primary party must participate")
        if not set(stage.approver_ids + stage.blocker_ids + stage.technical_gatekeeper_ids) <= set(stage.participant_ids):
            raise ValueError("stage authorities must participate")
    for finding in topology.findings:
        if set(finding.stakeholder_ids) - valid_people or set(finding.stage_ids) - valid_stages:
            raise ValueError("friction finding contains a dangling reference")


def load_baseline_topology() -> StakeholderTopology:
    raw = _fixture("baseline_stakeholder_topology.json")
    topology = StakeholderTopology(
        raw["identifier"], raw["customer_name"], tuple(_stakeholder(x) for x in raw["stakeholders"]),
        tuple(_relationship(x) for x in raw["relationships"]), tuple(_stage(x) for x in raw["stages"]),
        tuple(_finding(x) for x in raw["findings"]), SponsorStrength(raw["sponsor_strength"]),
        raw["technical_project_identifier"], parse_evidence_label(raw["evidence"]),
    )
    validate_topology(topology)
    return topology


def summarize_topology(topology: StakeholderTopology) -> StakeholderSummary:
    participation = tuple((stage.stage_id, len(stage.participant_ids)) for stage in topology.stages)
    person_counts = {person.identifier: len(person.journey_stage_ids) for person in topology.stakeholders}
    max_person = max(person_counts.values())
    max_stage = max(count for _, count in participation)
    approvals = sum(len(stage.approver_ids) for stage in topology.stages)
    blockers = sum(len(stage.blocker_ids) for stage in topology.stages)
    technical = sum(len(stage.technical_gatekeeper_ids) for stage in topology.stages)
    return StakeholderSummary(
        len(topology.stakeholders), sum(len(person.roles) for person in topology.stakeholders),
        participation, approvals, blockers, technical,
        tuple(key for key, value in person_counts.items() if value == max_person),
        tuple(key for key, value in participation if value == max_stage),
    )


def coordination_dependency_count(topology: StakeholderTopology) -> int:
    return sum(r.relationship_type in {RelationshipType.DEPENDS_ON, RelationshipType.REQUIRES_APPROVAL_FROM,
                                      RelationshipType.ACCEPTANCE_REQUIRED_FROM}
               for r in topology.relationships)


def _sensitivity_finding(reason: FrictionReason, people: tuple[str, ...], stages: tuple[str, ...], text: str) -> StakeholderFrictionFinding:
    return StakeholderFrictionFinding(reason, people, stages, text, EvidenceLabel.SENSITIVITY_ASSUMPTION)


def load_stakeholder_scenarios() -> tuple[StakeholderScenario, ...]:
    base = load_baseline_topology()
    sponsor_id = "OPERATIONS_MANAGER"
    strong_people = tuple(replace(p, roles=p.roles + (StakeholderRole.DECISION_MAKER, StakeholderRole.APPROVER),
                                  approval_authority=p.approval_authority + (AuthorityDomain.PURCHASE_APPROVER,),
                                  evidence=EvidenceLabel.SENSITIVITY_ASSUMPTION,
                                  notes=p.notes + " Sensitivity: empowered to coordinate and authorize the department path.")
                          if p.identifier == sponsor_id else p for p in base.stakeholders)
    strong_stages = tuple(replace(stage, approver_ids=tuple(x for x in stage.approver_ids if x != "FINANCE_REPRESENTATIVE"))
                          if stage.stage_id == "PROCUREMENT_PATH" else stage for stage in base.stages)
    strong_rels = tuple(r for r in base.relationships
                        if not (r.source_id == sponsor_id and r.target_id == "FINANCE_REPRESENTATIVE"))
    strong_findings = tuple(f for f in base.findings if f.reason is not FrictionReason.CROSS_FUNCTIONAL_COORDINATION) + (
        _sensitivity_finding(FrictionReason.CROSS_FUNCTIONAL_COORDINATION,
                             (sponsor_id, "IT_REPRESENTATIVE", "PROCUREMENT_REPRESENTATIVE"),
                             ("PROCUREMENT_PATH", "IMPLEMENTATION_APPROVAL"),
                             "Empowered sponsorship reduces one budget-coordination dependency; independent controls remain."),)
    strong = replace(base, identifier="JAMES_RIVER_STRONG_SPONSOR", stakeholders=strong_people,
                     stages=strong_stages, relationships=strong_rels, findings=strong_findings,
                     sponsor_strength=SponsorStrength.STRONG, evidence=EvidenceLabel.SENSITIVITY_ASSUMPTION)

    extra = StakeholderRelationship("DEPARTMENT_DIRECTOR", "FINANCE_REPRESENTATIVE",
        RelationshipType.REQUIRES_APPROVAL_FROM, ("PROPOSAL",),
        "Fragmented authority adds separate finance approval at proposal.", EvidenceLabel.SENSITIVITY_ASSUMPTION)
    fragmented_stages = tuple(replace(stage, approver_ids=stage.approver_ids + ("FINANCE_REPRESENTATIVE",),
                                      blocker_ids=stage.blocker_ids + ("FINANCE_REPRESENTATIVE",))
                              if stage.stage_id == "PROPOSAL" else stage for stage in base.stages)
    fragmented = replace(base, identifier="JAMES_RIVER_FRAGMENTED_AUTHORITY",
        relationships=base.relationships + (extra,), stages=fragmented_stages,
        findings=base.findings + (_sensitivity_finding(FrictionReason.UNCLEAR_DECISION_AUTHORITY,
            ("DEPARTMENT_DIRECTOR", "FINANCE_REPRESENTATIVE", "PROCUREMENT_REPRESENTATIVE"), ("PROPOSAL",),
            "Proposal authority is split across an additional required approver."),),
        evidence=EvidenceLabel.SENSITIVITY_ASSUMPTION)

    no_people = tuple(replace(p, roles=tuple(r for r in p.roles if r is not StakeholderRole.SPONSOR),
                              evidence=EvidenceLabel.SENSITIVITY_ASSUMPTION,
                              notes=p.notes + " Sensitivity: sponsor status removed.")
                      if p.identifier == sponsor_id else p for p in base.stakeholders)
    no_stages = tuple(replace(stage, primary_responsible_id="DEPARTMENT_DIRECTOR",
                              participant_ids=tuple(dict.fromkeys(stage.participant_ids + ("DEPARTMENT_DIRECTOR",))))
                      if stage.stage_id == "SPONSOR" else stage for stage in base.stages)
    no_sponsor = replace(base, identifier="JAMES_RIVER_NO_SPONSOR", stakeholders=no_people,
                         stages=no_stages, sponsor_strength=SponsorStrength.ABSENT,
                         findings=base.findings + (_sensitivity_finding(
                             FrictionReason.UNCLEAR_DECISION_AUTHORITY,
                             ("DEPARTMENT_DIRECTOR", "OPERATIONS_MANAGER"), ("SPONSOR", "DISCOVERY"),
                             "Without an internal sponsor, ownership remains but internal coordination and buyer access are less clear."),),
                         evidence=EvidenceLabel.SENSITIVITY_ASSUMPTION)
    for topology in (strong, fragmented, no_sponsor):
        validate_topology(topology)
    return (
        StakeholderScenario("BASELINE", "Baseline", base, (), base.evidence, "POOR TARGET CUSTOMER"),
        StakeholderScenario("STRONG_SPONSOR", "Strong sponsor", strong,
            ("SENSITIVITY ASSUMPTION: sponsor authority expanded and one budget-coordination dependency consolidated.",), EvidenceLabel.SENSITIVITY_ASSUMPTION, "INVESTIGATE"),
        StakeholderScenario("FRAGMENTED_AUTHORITY", "Fragmented authority", fragmented,
            ("SENSITIVITY ASSUMPTION: separate finance approval and blocking path added to proposal.",), EvidenceLabel.SENSITIVITY_ASSUMPTION, "POOR TARGET CUSTOMER"),
        StakeholderScenario("NO_SPONSOR", "No sponsor", no_sponsor,
            ("SENSITIVITY ASSUMPTION: sponsor status removed; the technical project is unchanged.",), EvidenceLabel.SENSITIVITY_ASSUMPTION, "POOR TARGET CUSTOMER"),
    )


def stakeholder_friction_trace() -> tuple[FrictionReason, ...]:
    """Concrete Chapter 3 mechanisms beneath Chapter 1 STAKEHOLDER_FRICTION."""
    return tuple(f.reason for f in load_baseline_topology().findings)
