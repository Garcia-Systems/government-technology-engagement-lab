"""Chapter 17: explicit within-government, cross-department reuse experiment."""

from dataclasses import dataclass, replace
from decimal import Decimal
from enum import StrEnum

from .baseline import _fixture
from .evidence import EvidenceLabel, parse_evidence_label


class ReuseDimension(StrEnum):
    ENGINEERING_REUSE = "ENGINEERING_REUSE"
    DISCOVERY_REUSE = "DISCOVERY_REUSE"
    CONFIGURATION_REUSE = "CONFIGURATION_REUSE"
    TEST_REUSE = "TEST_REUSE"
    DOCUMENTATION_REUSE = "DOCUMENTATION_REUSE"
    SALES_MOTION_REUSE = "SALES_MOTION_REUSE"
    PROCUREMENT_REUSE = "PROCUREMENT_REUSE"
    SECURITY_GOVERNANCE_REUSE = "SECURITY_GOVERNANCE_REUSE"
    SUPPORT_REUSE = "SUPPORT_REUSE"


class ReuseState(StrEnum):
    REUSE_AS_IS = "REUSE_AS_IS"
    ADAPT = "ADAPT"
    REBUILD = "REBUILD"
    NOT_APPLICABLE = "NOT_APPLICABLE"


@dataclass(frozen=True)
class Department:
    identifier: str
    name: str
    fictional: bool
    workflow: tuple[str, ...]
    fiction_notice: str = "Wholly fictional; represents no real locality or agency."


@dataclass(frozen=True)
class ReuseArtifact:
    identifier: str
    dimension: ReuseDimension
    name: str
    source_department: str
    target_department: str
    state: ReuseState
    first_department_effort: int
    adaptation_effort: int
    evidence: EvidenceLabel
    reason: str

    @property
    def reusable_unchanged(self) -> bool:
        return self.state is ReuseState.REUSE_AS_IS

    @property
    def reusable_with_adaptation(self) -> bool:
        return self.state is ReuseState.ADAPT

    @property
    def not_reusable(self) -> bool:
        return self.state is ReuseState.REBUILD

    @property
    def hours_saved(self) -> int:
        return 0 if self.state in (ReuseState.REBUILD, ReuseState.NOT_APPLICABLE) else self.first_department_effort - self.adaptation_effort


@dataclass(frozen=True)
class DimensionSummary:
    dimension: ReuseDimension
    greenfield_hours: int
    hours_required: int
    hours_saved: int
    evidence: EvidenceLabel = EvidenceLabel.OBSERVED_LAB_RESULT


@dataclass(frozen=True)
class RepeatEconomics:
    implementation_price: Decimal
    annual_support_revenue: Decimal
    annual_recoverable_value: Decimal
    first_year_customer_cost: Decimal
    customer_net_value: Decimal
    delivery_cost: Decimal
    acquisition_cost: Decimal
    governance_cost: Decimal
    support_cost: Decimal
    other_direct_cost: Decimal
    marginal_contribution: Decimal
    evidence: EvidenceLabel = EvidenceLabel.OBSERVED_LAB_RESULT


@dataclass(frozen=True)
class RepeatAssessment:
    key: str
    name: str
    source: Department
    target: Department
    reference_motion: str
    reference_reason: str
    artifacts: tuple[ReuseArtifact, ...]
    summaries: tuple[DimensionSummary, ...]
    engineering_greenfield_hours: int
    engineering_hours: int
    discovery_hours: int
    acquisition_hours: int
    governance_hours: int
    support_hours: int
    total_effort_hours: int
    elapsed_days: int
    economics: RepeatEconomics
    findings: tuple[str, ...]
    project_verdict: str
    target_verdict: str
    structural_interpretation: str
    changed_assumptions: tuple[str, ...] = ()
    evidence: EvidenceLabel = EvidenceLabel.OBSERVED_LAB_RESULT


def _departments(raw: dict) -> tuple[Department, Department]:
    s, t = raw["source_department"], raw["target_department"]
    return (Department(s["identifier"], s["name"], s["fictional"], tuple(s["workflow"])),
            Department(t["identifier"], t["name"], t["fictional"], tuple(t["workflow"]), t["fiction_notice"]))


def load_repeatability_fixture() -> tuple[Department, Department, tuple[ReuseArtifact, ...], dict]:
    raw = _fixture("repeat_department.json")
    source, target = _departments(raw)
    evidence = parse_evidence_label(raw["evidence"])
    artifacts = tuple(ReuseArtifact(x[0], ReuseDimension(x[1]), x[2], source.identifier,
                                    target.identifier, ReuseState(x[3]), x[4], x[5], evidence, x[6])
                      for x in raw["artifacts"])
    validate_artifacts(source, target, artifacts)
    return source, target, artifacts, raw


def validate_artifacts(source: Department, target: Department, artifacts: tuple[ReuseArtifact, ...]) -> None:
    ids = [a.identifier for a in artifacts]
    if len(ids) != len(set(ids)):
        raise ValueError("reuse artifact identifiers must be unique")
    valid_departments = {source.identifier, target.identifier}
    for a in artifacts:
        if {a.source_department, a.target_department} - valid_departments:
            raise ValueError("artifact references an unknown department")
        if a.adaptation_effort < 0 or a.adaptation_effort > a.first_department_effort:
            raise ValueError("adaptation effort must be bounded by greenfield effort")
        if a.state is ReuseState.ADAPT and a.adaptation_effort == 0:
            raise ValueError("adapted artifacts retain work")
        if a.state is ReuseState.REBUILD and a.adaptation_effort != a.first_department_effort:
            raise ValueError("rebuilt artifacts receive no reuse savings")


def summarize_dimensions(artifacts: tuple[ReuseArtifact, ...]) -> tuple[DimensionSummary, ...]:
    return tuple(DimensionSummary(d, sum(a.first_department_effort for a in artifacts if a.dimension is d),
                                  sum(a.adaptation_effort for a in artifacts if a.dimension is d),
                                  sum(a.hours_saved for a in artifacts if a.dimension is d))
                 for d in ReuseDimension)


def _assessment(key="SAME_LOCALITY", name="Same locality, strong technical reuse", *,
                engineering_extra=0, discovery_extra=0, sales_extra=0, procurement_extra=0,
                governance_extra=0, support_extra=0, elapsed_extra=0, changes=()) -> RepeatAssessment:
    source, target, artifacts, raw = load_repeatability_fixture()
    summaries = summarize_dimensions(artifacts)
    required = {s.dimension: s.hours_required for s in summaries}
    engineering = sum(required[d] for d in (ReuseDimension.ENGINEERING_REUSE, ReuseDimension.CONFIGURATION_REUSE, ReuseDimension.TEST_REUSE)) + engineering_extra
    discovery = required[ReuseDimension.DISCOVERY_REUSE] + discovery_extra
    acquisition = required[ReuseDimension.SALES_MOTION_REUSE] + required[ReuseDimension.PROCUREMENT_REUSE] + required[ReuseDimension.DOCUMENTATION_REUSE] + sales_extra + procurement_extra
    governance = required[ReuseDimension.SECURITY_GOVERNANCE_REUSE] + governance_extra
    support = required[ReuseDimension.SUPPORT_REUSE] + support_extra
    e = raw["economics"]; price, support_revenue, value = map(Decimal, (e["implementation_price"], e["annual_support_revenue"], e["annual_recoverable_value"]))
    delivery_cost = Decimal(engineering + discovery) * Decimal(e["engineering_rate"])
    acquisition_cost = Decimal(acquisition) * Decimal(e["engagement_rate"])
    governance_cost = Decimal(governance) * Decimal(e["engagement_rate"])
    support_cost = Decimal(support) * Decimal(e["support_rate"])
    other = Decimal(e["other_direct_cost"])
    economics = RepeatEconomics(price, support_revenue, value, price + support_revenue,
        value - price - support_revenue, delivery_cost, acquisition_cost, governance_cost,
        support_cost, other, price + support_revenue - delivery_cost - acquisition_cost - governance_cost - support_cost - other)
    eng_greenfield = sum(s.greenfield_hours for s in summaries if s.dimension in (ReuseDimension.ENGINEERING_REUSE, ReuseDimension.CONFIGURATION_REUSE, ReuseDimension.TEST_REUSE))
    multidimensional = engineering < eng_greenfield and acquisition < raw["department_1"]["acquisition_hours"] and support <= raw["department_1"]["support_hours"]
    return RepeatAssessment(key, name, source, target, raw["reference_motion"], raw["reference_reason"], artifacts, summaries,
        eng_greenfield, engineering, discovery, acquisition, governance, support,
        engineering + discovery + acquisition + governance + support, e["elapsed_days"] + elapsed_extra, economics,
        ("CANONICAL_MODEL_REUSED", "REPORTING_SHELL_REUSED", "TEST_HARNESS_REUSED", "DEPARTMENT_MAPPING_REQUIRED",
         "NEW_WORKFLOW_DISCOVERY_REQUIRED", "PROJECT_APPROVAL_REPEATED", "PROCUREMENT_PATH_REUSED",
         "SECURITY_DOCUMENTATION_REUSED", "SECURITY_REVIEW_REPEATED", "NEW_SPONSOR_REQUIRED", "SUPPORT_INFRASTRUCTURE_SHARED"),
        "VIABLE BOUNDED PROJECT", "PROMISING — VALIDATE IN DISCOVERY" if multidimensional else "PILOT-FIRST TARGET",
        "REPEATABLE PROJECT" if multidimensional else "CUSTOM PROJECT — REUSE INSUFFICIENT", tuple(changes))


def assess_repeat_department() -> RepeatAssessment:
    return _assessment()


def repeat_department_scenarios() -> tuple[RepeatAssessment, ...]:
    return (assess_repeat_department(),
            _assessment("TECHNICAL_REUSE_COMMERCIAL_RESET", "Technical reuse high, commercial reuse low", discovery_extra=10, sales_extra=22, procurement_extra=10, elapsed_extra=45, changes=("Sponsor introduction and budget-owner access benefits removed; discovery expanded.",)),
            _assessment("COMMERCIAL_REUSE_TECHNICAL_VARIATION", "Commercial reuse high, technical variation high", engineering_extra=44, sales_extra=-6, procurement_extra=-3, elapsed_extra=10, changes=("Easy account access retained; unique adapter and workflow variation add engineering.",)),
            _assessment("STRONG_REPEATABILITY", "Strong cross-department repeatability", engineering_extra=-8, discovery_extra=-3, sales_extra=-5, procurement_extra=-4, governance_extra=-4, support_extra=-3, elapsed_extra=-20, changes=("Sponsor introduction, shared review preparation, purchasing path, and runtime all reduce explicit work.",)))


def department_one_reference() -> dict:
    return _fixture("repeat_department.json")["department_1"].copy()
