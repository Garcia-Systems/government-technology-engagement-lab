"""Chapter 6: a deterministic read-only edge and modeled authority comparison."""

from copy import deepcopy
from dataclasses import dataclass, replace
from decimal import Decimal
from enum import StrEnum

from .baseline import _fixture, load_baseline
from .evidence import EvidenceLabel
from .formal_rfp import load_formal_rfp_motion
from .models import (EngagementJourney, GateStatus, LaborCostRate,
                     MotionStakeholderParticipation, SellerEconomics, WorkCategory)
from .pilot import load_pilot_motion
from .stakeholders import load_baseline_topology


class SourceAccessMode(StrEnum):
    EXPORT_ONLY = "EXPORT_ONLY"
    READ_ONLY_API = "READ_ONLY_API"
    WRITE_NON_AUTHORITATIVE = "WRITE_NON_AUTHORITATIVE"
    WRITE_AUTHORITATIVE = "WRITE_AUTHORITATIVE"


class TechnicalRiskFinding(StrEnum):
    NO_AUTHORITATIVE_WRITES = "NO_AUTHORITATIVE_WRITES"
    LIMITED_DATA_ACCESS = "LIMITED_DATA_ACCESS"
    BOUNDED_DATA_RETENTION = "BOUNDED_DATA_RETENTION"
    REVERSIBLE_PROCESSING = "REVERSIBLE_PROCESSING"
    LOWER_CHANGE_CONTROL_SURFACE = "LOWER_CHANGE_CONTROL_SURFACE"
    LOWER_DEPLOYMENT_RISK = "LOWER_DEPLOYMENT_RISK"
    LIMITED_SUPPORT_SURFACE = "LIMITED_SUPPORT_SURFACE"
    AUTHORITATIVE_WRITE_ACCESS = "AUTHORITATIVE_WRITE_ACCESS"
    CONSEQUENTIAL_UPDATE_PATH = "CONSEQUENTIAL_UPDATE_PATH"
    BROADER_ACCESS_REQUIREMENTS = "BROADER_ACCESS_REQUIREMENTS"
    HIGHER_CHANGE_CONTROL_SURFACE = "HIGHER_CHANGE_CONTROL_SURFACE"
    LARGER_SUPPORT_SURFACE = "LARGER_SUPPORT_SURFACE"


@dataclass(frozen=True)
class TechnicalAuthority:
    source_access_mode: SourceAccessMode
    write_capability: bool
    authoritative_system_mutation_allowed: bool
    consequential_action_allowed: bool
    authentication_assumptions: str
    deployment_boundary: str
    data_retention_assumptions: str
    audit_logging_required: bool
    support_surface: tuple[str, ...]
    evidence: EvidenceLabel


@dataclass(frozen=True)
class GovernanceSurface:
    write_approval: bool
    elevated_credentials: bool
    production_mutation_approval: bool
    broader_change_control: bool
    rollback_planning: bool
    production_data_retention_approval: bool
    additional_audit_requirements: bool


@dataclass(frozen=True)
class Provenance:
    source_identifier: str
    source_record_identifier: str
    source_status: str
    normalized_status: str
    transformation_timestamp: str
    reason: str
    exception_flag: bool


@dataclass(frozen=True)
class NormalizedRecord:
    permit_id: str
    reported_status: str
    provenance: Provenance


@dataclass(frozen=True)
class ReadOnlyResult:
    records_ingested: int
    normalized_records: tuple[NormalizedRecord, ...]
    exceptions: tuple[NormalizedRecord, ...]
    duplicates: tuple[NormalizedRecord, ...]
    status_summary: tuple[tuple[str, int], ...]
    source_unchanged: bool
    evidence: EvidenceLabel = EvidenceLabel.OBSERVED_LAB_RESULT


@dataclass(frozen=True)
class EngineeringWork:
    category: str
    hours: int
    evidence: EvidenceLabel = EvidenceLabel.MODELED_ASSUMPTION


@dataclass(frozen=True)
class ReadOnlyEconomics:
    value_addressed: Decimal
    engagement_price: Decimal
    support: Decimal
    first_year_customer_cost: Decimal
    modeled_net_recoverable_value: Decimal
    payback_months: Decimal
    acquisition_hours: int
    elapsed_days: int
    seller: SellerEconomics


@dataclass(frozen=True)
class TechnicalScenario:
    key: str
    name: str
    authority: TechnicalAuthority
    governance: GovernanceSurface
    risk_findings: tuple[TechnicalRiskFinding, ...]
    allowed_operations: tuple[str, ...]
    prohibited_operations: tuple[str, ...]
    engineering_work: tuple[EngineeringWork, ...]
    journey: EngagementJourney
    stakeholders: tuple[MotionStakeholderParticipation, ...]
    value_capture_fraction: Decimal
    value_capture_evidence: EvidenceLabel
    price: Decimal
    support: Decimal
    other_direct_cost: Decimal
    access_reliable: bool
    acceptance_criteria: tuple[str, ...]
    changed_assumptions: tuple[str, ...] = ()
    evidence: EvidenceLabel = EvidenceLabel.MODELED_ASSUMPTION

    @property
    def engineering_hours(self) -> int:
        return sum(x.hours for x in self.engineering_work)


@dataclass(frozen=True)
class TechnicalAssessment:
    scenario: TechnicalScenario
    processing: ReadOnlyResult | None
    economics: ReadOnlyEconomics
    acceptance_passed: bool
    project_viability: GateStatus
    target_viability: GateStatus
    verdict: str


READ_ONLY_SUPPORT = ("source schema changes", "export failures", "normalization mappings", "reporting defects", "exception interpretation", "access expiration")
WRITE_SUPPORT = READ_ONLY_SUPPORT + ("write failures", "partial commits", "rollback", "authoritative-system conflicts", "retry/replay", "post-write state reconciliation")


def load_read_only_fixture() -> dict:
    return _fixture("read_only_records.json")


def process_read_only_export(fixture: dict | None = None) -> ReadOnlyResult:
    """Pure transform: accepts copied input and exposes no repository write primitive."""
    source = fixture if fixture is not None else load_read_only_fixture()
    before = deepcopy(source)
    mapping = {"submitted": "SUBMITTED", "under review": "IN_REVIEW", "approved": "APPROVED",
               "corrections needed": "CORRECTION_REQUESTED", "resubmitted": "RESUBMITTED", "closed": "CLOSED"}
    outputs, exceptions, duplicates, seen = [], [], [], set()
    for raw in source["records"]:
        normalized = mapping.get(raw.get("source_status", ""), "UNKNOWN")
        duplicate = bool(raw.get("permit_id")) and (raw["permit_id"], normalized) in seen
        mismatch = normalized != raw.get("reported_status")
        invalid = not raw.get("record_id") or not raw.get("permit_id") or normalized == "UNKNOWN"
        reasons = [name for name, yes in (("INVALID_SOURCE_RECORD", invalid), ("DUPLICATE", duplicate), ("STATUS_MISMATCH", mismatch)) if yes]
        reason = "+".join(reasons) if reasons else "DIRECT_STATUS_MAPPING"
        provenance = Provenance(source["source_identifier"], raw.get("record_id", ""), raw.get("source_status", ""),
                                normalized, source["transformation_timestamp"], reason, bool(reasons))
        record = NormalizedRecord(raw.get("permit_id", ""), raw.get("reported_status", ""), provenance)
        outputs.append(record)
        if reasons: exceptions.append(record)
        if duplicate: duplicates.append(record)
        if raw.get("permit_id"): seen.add((raw["permit_id"], normalized))
    counts = {}
    for item in outputs:
        counts[item.provenance.normalized_status] = counts.get(item.provenance.normalized_status, 0) + 1
    return ReadOnlyResult(len(source["records"]), tuple(outputs), tuple(exceptions), tuple(duplicates),
                          tuple(sorted(counts.items())), source == before)


def _authority(read_only: bool) -> TechnicalAuthority:
    return TechnicalAuthority(SourceAccessMode.EXPORT_ONLY if read_only else SourceAccessMode.WRITE_AUTHORITATIVE,
        not read_only, not read_only, not read_only,
        "Time-limited approved export credential" if read_only else "Elevated production integration credential",
        "Isolated reporting edge; no authoritative-system route" if read_only else "Modeled production integration boundary",
        "Bounded export retained for pilot then deleted" if read_only else "Production state and integration logs retained",
        True, READ_ONLY_SUPPORT if read_only else WRITE_SUPPORT, EvidenceLabel.MODELED_ASSUMPTION)


def _governance(read_only: bool) -> GovernanceSurface:
    return GovernanceSurface(*( (False, False, False, False, False, True, True) if read_only else (True, True, True, True, True, True, True) ))


def _journey(read_only: bool) -> EngagementJourney:
    base = load_pilot_motion().journey
    reductions = {"TECHNICAL_VALIDATION": (6, 6), "SECURITY_ACCESS_REVIEW": (5, 7), "IMPLEMENTATION": (0, 14)}
    if not read_only: return base
    stages = tuple(replace(s, effort_hours=reductions[s.identifier][0], elapsed_days=reductions[s.identifier][1]) if s.identifier in reductions else s for s in base.stages)
    return replace(base, identifier="READ_ONLY_REPORTING_EDGE_JOURNEY", stages=stages)


def _stakeholders() -> tuple[MotionStakeholderParticipation, ...]:
    topology_ids = {x.identifier for x in load_baseline_topology().stakeholders}
    links = load_pilot_motion().stakeholders
    assert {x.stakeholder_id for x in links} <= topology_ids
    return links


def _work(read_only: bool) -> tuple[EngineeringWork, ...]:
    hours = (18, 10, 14, 14, 12, 10, 10, 12, 6, 4) if read_only else (22, 14, 20, 20, 18, 20, 24, 48, 38, 16)
    names = ("source ingestion", "validation", "normalization", "reconciliation", "reporting", "exception handling", "audit/provenance", "testing", "deployment", "documentation")
    return tuple(EngineeringWork(n, h) for n, h in zip(names, hours))


def technical_scenarios() -> tuple[TechnicalScenario, ...]:
    common = dict(stakeholders=_stakeholders(), price=Decimal("36000"), support=Decimal("4000"), other_direct_cost=Decimal("1000"),
                  acceptance_criteria=("records ingested", "normalization correct", "reconciliation correct", "expected exceptions surfaced", "report produced", "no source mutation", "provenance preserved"))
    write = TechnicalScenario("WRITE_CAPABLE_INTEGRATION", "Broader write-capable surface", _authority(False), _governance(False),
        tuple(TechnicalRiskFinding(x) for x in ("AUTHORITATIVE_WRITE_ACCESS", "CONSEQUENTIAL_UPDATE_PATH", "BROADER_ACCESS_REQUIREMENTS", "HIGHER_CHANGE_CONTROL_SURFACE", "LARGER_SUPPORT_SURFACE")),
        ("read", "normalize", "report", "authoritative update"), (), _work(False), _journey(False), value_capture_fraction=Decimal("1.00"),
        value_capture_evidence=EvidenceLabel.MODELED_ALTERNATIVE_ASSUMPTION, access_reliable=True, **common)
    read = TechnicalScenario("READ_ONLY_REPORTING_EDGE", "Read-only reporting edge", _authority(True), _governance(True),
        tuple(TechnicalRiskFinding(x) for x in ("NO_AUTHORITATIVE_WRITES", "LIMITED_DATA_ACCESS", "BOUNDED_DATA_RETENTION", "REVERSIBLE_PROCESSING", "LOWER_CHANGE_CONTROL_SURFACE", "LOWER_DEPLOYMENT_RISK", "LIMITED_SUPPORT_SURFACE")),
        ("ingest approved export", "validate", "normalize", "reconcile", "report", "surface exceptions"),
        ("authoritative update", "status write", "correction submission", "workflow mutation", "document mutation", "consequential automated decision"),
        _work(True), _journey(True), value_capture_fraction=Decimal("0.55"), value_capture_evidence=EvidenceLabel.MODELED_ASSUMPTION, access_reliable=True, **common)
    low = replace(read, key="READ_ONLY_VALUE_TOO_LOW", name="Read-only value too low", value_capture_fraction=Decimal("0.15"),
                  value_capture_evidence=EvidenceLabel.SENSITIVITY_ASSUMPTION, changed_assumptions=("Value capture reduced to 15%.",), evidence=EvidenceLabel.SENSITIVITY_ASSUMPTION)
    hard_stages = tuple(replace(s, effort_hours=s.effort_hours + (8 if s.identifier in ("TECHNICAL_VALIDATION", "SECURITY_ACCESS_REVIEW") else 0),
                                elapsed_days=s.elapsed_days + (20 if s.identifier in ("TECHNICAL_VALIDATION", "SECURITY_ACCESS_REVIEW") else 0)) for s in read.journey.stages)
    hard = replace(read, key="READ_ONLY_ACCESS_DIFFICULT", name="Read-only access still difficult", access_reliable=False,
                   journey=replace(read.journey, identifier="DIFFICULT_READ_ONLY_ACCESS_JOURNEY", stages=hard_stages),
                   changed_assumptions=("Approved export access is unreliable and delayed.",), evidence=EvidenceLabel.SENSITIVITY_ASSUMPTION)
    return write, read, low, hard


def calculate_read_only_economics(scenario: TechnicalScenario) -> ReadOnlyEconomics:
    value = load_baseline().burden.annual_recoverable_value * scenario.value_capture_fraction
    rates: tuple[LaborCostRate, ...] = load_formal_rfp_motion().labor_rates
    by_rate = {x.category: x.hourly_cost for x in rates}
    delivery = Decimal(scenario.engineering_hours) * by_rate[WorkCategory.ENGINEERING]
    acquisition_stages = tuple(s for s in scenario.journey.stages if s.sequence <= 8)
    acquisition = sum((Decimal(s.effort_hours) * by_rate[s.responsible_category] for s in acquisition_stages), Decimal())
    contribution = scenario.price - delivery - acquisition - scenario.other_direct_cost
    seller = SellerEconomics(scenario.price, delivery, acquisition, scenario.other_direct_cost, contribution,
                             contribution / scenario.price, EvidenceLabel.OBSERVED_LAB_RESULT)
    cost = scenario.price + scenario.support
    return ReadOnlyEconomics(value, scenario.price, scenario.support, cost, value - cost,
                             scenario.price / value * Decimal(12), sum(s.effort_hours for s in acquisition_stages),
                             sum(s.elapsed_days for s in acquisition_stages), seller)


def assess_technical_scenario(scenario: TechnicalScenario) -> TechnicalAssessment:
    processing = process_read_only_export() if not scenario.authority.write_capability else None
    economics = calculate_read_only_economics(scenario)
    accepted = processing is not None and processing.source_unchanged and len(processing.normalized_records) == processing.records_ingested and all(x.provenance.source_record_identifier for x in processing.normalized_records)
    project = GateStatus.PASS if economics.modeled_net_recoverable_value >= 0 and scenario.access_reliable else GateStatus.FAIL
    target = GateStatus.PASS if project is GateStatus.PASS and economics.seller.acquisition_adjusted_contribution >= Decimal("10000") and economics.elapsed_days <= 90 else GateStatus.FAIL
    verdict = "NO DEAL" if project is GateStatus.FAIL else ("PILOT-FIRST TARGET" if target is GateStatus.PASS else "POOR TARGET CUSTOMER")
    return TechnicalAssessment(scenario, processing, economics, accepted, project, target, verdict)


def read_only_scenarios() -> tuple[TechnicalAssessment, ...]:
    return tuple(assess_technical_scenario(x) for x in technical_scenarios())


def no_authoritative_write_path_exists() -> bool:
    """Executable structural invariant: this module intentionally exports no write operation."""
    return not any(name.startswith(("write_", "update_", "mutate_", "submit_correction")) for name in globals())
