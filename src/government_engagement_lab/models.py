"""Typed domain records; no government-wide scoring model is used."""

from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum

from .evidence import EvidenceLabel


class GateStatus(StrEnum):
    PASS = "PASS"
    FAIL = "FAIL"
    CONDITIONAL = "CONDITIONAL"
    NOT_EVALUATED = "NOT_EVALUATED"


class GateDimension(StrEnum):
    PROBLEM_ATTRACTIVENESS = "PROBLEM_ATTRACTIVENESS"
    TECHNICAL_FEASIBILITY = "TECHNICAL_FEASIBILITY"
    CUSTOMER_ECONOMICS = "CUSTOMER_ECONOMICS"
    DELIVERY_ECONOMICS = "DELIVERY_ECONOMICS"
    SUPPORT_ECONOMICS = "SUPPORT_ECONOMICS"
    TARGET_ATTRACTIVENESS = "TARGET_ATTRACTIVENESS"


class EngagementMotion(StrEnum):
    """Context for an assessment, deliberately not a scored gate."""

    BASELINE_COOKBOOK_MOTION = "BASELINE_COOKBOOK_MOTION"
    FORMAL_RFP = "FORMAL_RFP"
    COOPERATIVE_PAID_PILOT = "COOPERATIVE_PAID_PILOT"
    CONFIGURATION_FIRST = "CONFIGURATION_FIRST"


class PilotAcceptance(StrEnum):
    PILOT_ACCEPTED = "PILOT_ACCEPTED"
    PILOT_CONDITIONAL = "PILOT_CONDITIONAL"
    PILOT_FAILED = "PILOT_FAILED"


class StageType(StrEnum):
    ACCESS = "ACCESS"
    DISCOVERY = "DISCOVERY"
    TECHNICAL = "TECHNICAL"
    GOVERNANCE = "GOVERNANCE"
    PROCUREMENT = "PROCUREMENT"
    COMMERCIAL = "COMMERCIAL"
    CONTRACTING = "CONTRACTING"
    APPROVAL = "APPROVAL"
    ACCEPTANCE = "ACCEPTANCE"


class WorkCategory(StrEnum):
    SALES = "SALES"
    SOLUTIONS = "SOLUTIONS"
    ENGINEERING = "ENGINEERING"
    CUSTOMER_SPONSOR = "CUSTOMER_SPONSOR"
    CUSTOMER_IT = "CUSTOMER_IT"
    PROCUREMENT = "PROCUREMENT"
    LEGAL_CONTRACTS = "LEGAL_CONTRACTS"
    SECURITY_GOVERNANCE = "SECURITY_GOVERNANCE"


class StakeholderRole(StrEnum):
    DECISION_MAKER = "DECISION_MAKER"
    INFLUENCER = "INFLUENCER"
    APPROVER = "APPROVER"
    BLOCKER = "BLOCKER"
    USER = "USER"
    TECHNICAL_GATEKEEPER = "TECHNICAL_GATEKEEPER"
    SPONSOR = "SPONSOR"


class AuthorityDomain(StrEnum):
    PROBLEM_OWNER = "PROBLEM_OWNER"
    PURCHASE_APPROVER = "PURCHASE_APPROVER"
    TECHNICAL_ACCESS_OWNER = "TECHNICAL_ACCESS_OWNER"
    CONTRACT_APPROVER = "CONTRACT_APPROVER"
    IMPLEMENTATION_ACCEPTOR = "IMPLEMENTATION_ACCEPTOR"


class RelationshipType(StrEnum):
    REPORTS_TO = "REPORTS_TO"
    REQUIRES_APPROVAL_FROM = "REQUIRES_APPROVAL_FROM"
    DEPENDS_ON = "DEPENDS_ON"
    CONTROLS_ACCESS_FOR = "CONTROLS_ACCESS_FOR"
    ADVISES = "ADVISES"
    SUPPLIES_INFORMATION_TO = "SUPPLIES_INFORMATION_TO"
    ACCEPTANCE_REQUIRED_FROM = "ACCEPTANCE_REQUIRED_FROM"


class SponsorStrength(StrEnum):
    STRONG = "STRONG"
    LIMITED = "LIMITED"
    ABSENT = "ABSENT"


class FrictionReason(StrEnum):
    MULTIPLE_REQUIRED_APPROVALS = "MULTIPLE_REQUIRED_APPROVALS"
    UNCLEAR_DECISION_AUTHORITY = "UNCLEAR_DECISION_AUTHORITY"
    ACCESS_CONTROL_DEPENDENCY = "ACCESS_CONTROL_DEPENDENCY"
    SEQUENTIAL_APPROVAL_DEPENDENCY = "SEQUENTIAL_APPROVAL_DEPENDENCY"
    INCUMBENT_VENDOR_DEPENDENCY = "INCUMBENT_VENDOR_DEPENDENCY"
    CROSS_FUNCTIONAL_COORDINATION = "CROSS_FUNCTIONAL_COORDINATION"


class FindingCode(StrEnum):
    MEANINGFUL_ADMINISTRATIVE_BURDEN = "MEANINGFUL_ADMINISTRATIVE_BURDEN"
    TECHNICALLY_FEASIBLE_BOUNDED_INTERVENTION = "TECHNICALLY_FEASIBLE_BOUNDED_INTERVENTION"
    CUSTOMER_VALUE_EXCEEDS_MODELED_COST = "CUSTOMER_VALUE_EXCEEDS_MODELED_COST"
    DELIVERY_ASSUMPTION_VIABLE = "DELIVERY_ASSUMPTION_VIABLE"
    SUPPORT_ASSUMPTION_VIABLE = "SUPPORT_ASSUMPTION_VIABLE"
    PROCUREMENT_DIFFICULTY = "PROCUREMENT_DIFFICULTY"
    STAKEHOLDER_FRICTION = "STAKEHOLDER_FRICTION"
    WEAK_BUYER_ACCESS = "WEAK_BUYER_ACCESS"
    LONG_SALES_CYCLE = "LONG_SALES_CYCLE"
    HIGH_SOLUTIONS_EFFORT = "HIGH_SOLUTIONS_EFFORT"
    REQUIRED_ACCESS_UNAVAILABLE = "REQUIRED_ACCESS_UNAVAILABLE"
    INSUFFICIENT_CUSTOMER_VALUE = "INSUFFICIENT_CUSTOMER_VALUE"
    TARGET_ACCESS_CONDITIONS_IMPROVED = "TARGET_ACCESS_CONDITIONS_IMPROVED"
    HIGH_ACQUISITION_EFFORT = "HIGH_ACQUISITION_EFFORT"
    LONG_ELAPSED_CYCLE = "LONG_ELAPSED_CYCLE"
    MULTIPLE_REQUIRED_APPROVALS = "MULTIPLE_REQUIRED_APPROVALS"
    SIGNIFICANT_PRE_AWARD_TECHNICAL_WORK = "SIGNIFICANT_PRE_AWARD_TECHNICAL_WORK"
    CONTRACT_COORDINATION_BURDEN = "CONTRACT_COORDINATION_BURDEN"
    PROCUREMENT_DEPENDENCY = "PROCUREMENT_DEPENDENCY"
    WEAK_DIRECT_BUYER_CONTROL = "WEAK_DIRECT_BUYER_CONTROL"
    CONTRIBUTION_BELOW_MODELED_MINIMUM = "CONTRIBUTION_BELOW_MODELED_MINIMUM"


@dataclass(frozen=True)
class Customer:
    name: str
    organization_type: str
    staff_count: int
    fiction_notice: str


@dataclass(frozen=True)
class Burden:
    annual_current_state: Decimal
    annual_recoverable_value: Decimal


@dataclass(frozen=True)
class EngagementEconomics:
    implementation_price: Decimal
    annual_support: Decimal
    engineering_hours: int
    solutions_sales_hours: int
    sales_cycle_months: int


@dataclass(frozen=True)
class Conditions:
    technical_feasibility: bool
    customer_payback_viability: bool
    delivery_viability: bool
    support_viability: bool
    procurement_difficulty: bool
    stakeholder_friction: bool
    buyer_access: str
    sales_cycle_burden: bool
    solutions_effort_burden: bool


@dataclass(frozen=True)
class BaselineCase:
    customer: Customer
    workflow: tuple[str, ...]
    operational_problems: tuple[str, ...]
    intervention_boundary: str
    burden: Burden
    economics: EngagementEconomics
    conditions: Conditions
    evidence: EvidenceLabel


@dataclass(frozen=True)
class Scenario:
    name: str
    verdict: str
    evidence: EvidenceLabel


@dataclass(frozen=True)
class GateResult:
    name: str
    status: GateStatus


@dataclass(frozen=True)
class Assessment:
    gates: tuple[GateResult, ...]
    findings: tuple[FindingCode, ...]
    verdict: str
    evidence: EvidenceLabel


@dataclass(frozen=True)
class GateReason:
    code: FindingCode
    explanation: str
    evidence: EvidenceLabel


@dataclass(frozen=True)
class DimensionResult:
    dimension: GateDimension
    status: GateStatus
    reasons: tuple[GateReason, ...]
    explanation: str


@dataclass(frozen=True)
class GateAssessment:
    gates: tuple[DimensionResult, ...]
    project_viability: GateStatus
    target_viability: GateStatus
    verdict: str
    engagement_motion: EngagementMotion
    evidence: EvidenceLabel = EvidenceLabel.OBSERVED_LAB_RESULT

    def gate(self, dimension: GateDimension) -> DimensionResult:
        return next(gate for gate in self.gates if gate.dimension is dimension)


@dataclass(frozen=True)
class GateScenario:
    key: str
    name: str
    assessment: GateAssessment
    changed_assumptions: tuple[GateReason, ...] = ()


@dataclass(frozen=True)
class EngagementStage:
    identifier: str
    display_name: str
    description: str
    sequence: int
    required: bool
    effort_hours: int
    elapsed_days: int
    responsible_category: WorkCategory
    stage_type: StageType
    evidence: EvidenceLabel
    assumptions: tuple[str, ...]


@dataclass(frozen=True)
class EngagementJourney:
    identifier: str
    name: str
    description: str
    customer_name: str
    engagement_motion: EngagementMotion
    stages: tuple[EngagementStage, ...]
    modeled_days_per_month: int
    evidence: EvidenceLabel
    result_evidence: EvidenceLabel = EvidenceLabel.OBSERVED_LAB_RESULT

    @property
    def ordered_stages(self) -> tuple[EngagementStage, ...]:
        return tuple(sorted(self.stages, key=lambda stage: stage.sequence))

    @property
    def total_effort_hours(self) -> int:
        return sum(stage.effort_hours for stage in self.stages)

    @property
    def total_elapsed_days(self) -> int:
        """Sum stage durations under Chapter 2's sequential-stage rule."""
        return sum(stage.elapsed_days for stage in self.stages)

    @property
    def modeled_months(self) -> Decimal:
        return Decimal(self.total_elapsed_days) / Decimal(self.modeled_days_per_month)


@dataclass(frozen=True)
class JourneyScenario:
    key: str
    name: str
    journey: EngagementJourney
    changed_stage_ids: tuple[str, ...]
    assumptions: tuple[str, ...]
    evidence: EvidenceLabel


@dataclass(frozen=True)
class Stakeholder:
    identifier: str
    display_name: str
    organizational_function: str
    roles: tuple[StakeholderRole, ...]
    journey_stage_ids: tuple[str, ...]
    approval_authority: tuple[AuthorityDomain, ...]
    blocking_authority: tuple[AuthorityDomain, ...]
    access_control_domain: str | None
    evidence: EvidenceLabel
    notes: str


@dataclass(frozen=True)
class StakeholderRelationship:
    source_id: str
    target_id: str
    relationship_type: RelationshipType
    stage_ids: tuple[str, ...]
    explanation: str
    evidence: EvidenceLabel


@dataclass(frozen=True)
class StageStakeholders:
    stage_id: str
    primary_responsible_id: str
    participant_ids: tuple[str, ...]
    approver_ids: tuple[str, ...]
    blocker_ids: tuple[str, ...]
    technical_gatekeeper_ids: tuple[str, ...]


@dataclass(frozen=True)
class StakeholderFrictionFinding:
    reason: FrictionReason
    stakeholder_ids: tuple[str, ...]
    stage_ids: tuple[str, ...]
    explanation: str
    evidence: EvidenceLabel


@dataclass(frozen=True)
class StakeholderTopology:
    identifier: str
    customer_name: str
    stakeholders: tuple[Stakeholder, ...]
    relationships: tuple[StakeholderRelationship, ...]
    stages: tuple[StageStakeholders, ...]
    findings: tuple[StakeholderFrictionFinding, ...]
    sponsor_strength: SponsorStrength
    technical_project_identifier: str
    evidence: EvidenceLabel


@dataclass(frozen=True)
class StakeholderSummary:
    stakeholder_count: int
    role_assignment_count: int
    participants_per_stage: tuple[tuple[str, int], ...]
    approval_dependency_count: int
    blocking_dependency_count: int
    technical_access_dependency_count: int
    most_involved_stakeholder_ids: tuple[str, ...]
    highest_participation_stage_ids: tuple[str, ...]
    evidence: EvidenceLabel = EvidenceLabel.OBSERVED_LAB_RESULT


@dataclass(frozen=True)
class StakeholderScenario:
    key: str
    name: str
    topology: StakeholderTopology
    changed_assumptions: tuple[str, ...]
    evidence: EvidenceLabel
    verdict: str


@dataclass(frozen=True)
class LaborCostRate:
    category: WorkCategory
    hourly_cost: Decimal
    evidence: EvidenceLabel


@dataclass(frozen=True)
class ProposalArtifact:
    identifier: str
    name: str
    stage_id: str
    evidence: EvidenceLabel


@dataclass(frozen=True)
class MotionStakeholderParticipation:
    stage_id: str
    stakeholder_id: str
    responsibility: str
    evidence: EvidenceLabel


@dataclass(frozen=True)
class FormalRFPMotion:
    identifier: str
    name: str
    description: str
    journey: EngagementJourney
    stakeholder_participation: tuple[MotionStakeholderParticipation, ...]
    proposal_artifacts: tuple[ProposalArtifact, ...]
    implementation_price: Decimal
    annual_support: Decimal
    engineering_hours: int
    labor_rates: tuple[LaborCostRate, ...]
    minimum_contribution: Decimal
    major_risks: tuple[str, ...]
    evidence: EvidenceLabel


@dataclass(frozen=True)
class SellerEconomics:
    implementation_revenue: Decimal
    delivery_labor_cost: Decimal
    acquisition_labor_cost: Decimal
    other_direct_costs: Decimal
    acquisition_adjusted_contribution: Decimal
    contribution_margin: Decimal
    evidence: EvidenceLabel


@dataclass(frozen=True)
class FormalRFPAssessment:
    motion: FormalRFPMotion
    customer_economics: object
    seller_economics: SellerEconomics
    findings: tuple[FindingCode, ...]
    project_viability: GateStatus
    target_viability: GateStatus
    verdict: str
    evidence: EvidenceLabel


@dataclass(frozen=True)
class FormalRFPScenario:
    key: str
    name: str
    assessment: FormalRFPAssessment
    changed_assumptions: tuple[str, ...]
    evidence: EvidenceLabel
