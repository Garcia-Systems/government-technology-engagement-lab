"""Chapter 7: deterministic configuration-first residual experiment."""

from copy import deepcopy
from dataclasses import dataclass, replace
from decimal import Decimal
from enum import StrEnum

from .baseline import _fixture, load_baseline
from .evidence import EvidenceLabel
from .formal_rfp import load_formal_rfp_motion
from .models import GateStatus, SellerEconomics, WorkCategory


class SupportState(StrEnum):
    SUPPORTED = "SUPPORTED"
    CONFIGURABLE = "CONFIGURABLE"
    NOT_SUPPORTED = "NOT_SUPPORTED"


class ResidualClass(StrEnum):
    IMMATERIAL = "IMMATERIAL"
    NARROW = "NARROW"
    MATERIAL = "MATERIAL"
    BROAD = "BROAD"


@dataclass(frozen=True)
class Capability:
    identifier: str; description: str; support: SupportState; enabled: bool
    effort_hours: int; categories: tuple[str, ...]; limitations: str
    evidence: EvidenceLabel = EvidenceLabel.MODELED_ALTERNATIVE_ASSUMPTION


@dataclass(frozen=True)
class Intervention:
    identifier: str; stage: str; capability_id: str | None
    coverage: tuple[tuple[str, Decimal], ...]; effort_hours: int; support_hours: int
    limitations: str; evidence: EvidenceLabel = EvidenceLabel.MODELED_ASSUMPTION


@dataclass(frozen=True)
class ResidualStep:
    intervention_id: str; stage: str; addressed: Decimal; remaining: Decimal


@dataclass(frozen=True)
class ConfigurationEconomics:
    value_addressed: Decimal; residual_value: Decimal; percent_addressed: Decimal
    implementation_price: Decimal; annual_support: Decimal; first_year_cost: Decimal
    net_first_year_recoverable_value: Decimal; payback_months: Decimal
    configuration_hours: int; engineering_hours: int; acquisition_hours: int
    elapsed_days: int; seller: SellerEconomics


@dataclass(frozen=True)
class ConfigurationAssessment:
    key: str; name: str; capabilities: tuple[Capability, ...]
    interventions: tuple[Intervention, ...]; steps: tuple[ResidualStep, ...]
    residual_classification: ResidualClass; economics: ConfigurationEconomics
    project_viability: GateStatus; target_viability: GateStatus; verdict: str
    operational_recommendation: str; assumption_evidence: EvidenceLabel
    custom_residual_candidate: str | None


BURDEN = (
    ("duplicate_entry", Decimal("18000.00")),
    ("status_reconciliation", Decimal("17002.80")),
    ("report_preparation", Decimal("14000.00")),
    ("lookup_search", Decimal("16000.00")),
    ("correction_administration", Decimal("21000.00")),
    ("workflow_rework", Decimal("18000.00")),
)
RESIDUAL_THRESHOLDS = ((Decimal("5000"), ResidualClass.IMMATERIAL),
                       (Decimal("25000"), ResidualClass.NARROW),
                       (Decimal("50000"), ResidualClass.MATERIAL))
THRESHOLD_EVIDENCE = EvidenceLabel.MODELED_ASSUMPTION


def load_capability_fixture() -> dict: return _fixture("incumbent_capabilities.json")
def load_current_configuration() -> dict: return _fixture("before_configuration.json")
def load_expected_configuration() -> dict: return _fixture("after_configuration_expected.json")


def capabilities() -> tuple[Capability, ...]:
    return tuple(Capability(x["id"], x["description"], SupportState(x["support"]), x["enabled"],
                            x["effort_hours"], tuple(x["categories"]), x["limitations"])
                 for x in load_capability_fixture()["capabilities"])


def interventions() -> tuple[Intervention, ...]:
    # Overlap is intentional; sequential remaining-category recovery caps it.
    return (
      Intervention("STATUS_STANDARDIZATION", "STANDARDIZATION", "status_categories", (("status_reconciliation", Decimal("0.55")), ("lookup_search", Decimal("0.10"))), 26, 4, "Canonical statuses require governance."),
      Intervention("REQUIRED_FIELDS", "CONFIGURATION", "required_fields", (("correction_administration", Decimal("0.45")),), 20, 4, "Cannot validate external facts."),
      Intervention("SAVED_QUEUES", "CONFIGURATION", "saved_views", (("lookup_search", Decimal("0.55")),), 18, 3, "Platform records only."),
      Intervention("NATIVE_REPORTING", "NATIVE_AUTOMATION_REPORTING", "scheduled_reports", (("report_preparation", Decimal("0.75")),), 22, 4, "Native fields only."),
      Intervention("NATIVE_NOTIFICATIONS", "NATIVE_AUTOMATION_REPORTING", "notifications", (("workflow_rework", Decimal("0.25")),), 18, 4, "Configured events only."),
      Intervention("PROCESS_STANDARDIZATION", "PROCESS_CHANGE", None, (("duplicate_entry", Decimal("0.30")), ("correction_administration", Decimal("0.20")), ("workflow_rework", Decimal("0.40"))), 28, 6, "Requires adoption and training."),
    )


def apply_configuration(current: dict | None = None, caps: tuple[Capability, ...] | None = None) -> tuple[dict, tuple[str, ...]]:
    source = load_current_configuration() if current is None else current
    result = deepcopy(source); available = {c.identifier: c for c in (caps or capabilities())}
    required = ("status_categories", "required_fields", "saved_views", "scheduled_reports", "notifications")
    unsupported = [x for x in required if available[x].support is SupportState.NOT_SUPPORTED]
    if unsupported: raise ValueError("Unsupported configuration: " + ", ".join(unsupported))
    result.update({"statuses":["SUBMITTED","IN_REVIEW","APPROVED","CORRECTION_REQUESTED","RESUBMITTED","CLOSED"],
                   "required_fields":["applicant_email","parcel_id","permit_type"],
                   "saved_queues":["CORRECTIONS_DUE","MY_ACTIVE_REVIEWS"],
                   "reports":["WEEKLY_PERMIT_STATUS"],
                   "notification_rules":["CORRECTION_REQUESTED_NOTICE","STATUS_CHANGED_NOTICE"]})
    result["process"] = {"single_correction_owner": True, "duplicate_review_step": False}
    return result, tuple(k for k in result if result[k] != source.get(k))


def classify_residual(value: Decimal) -> ResidualClass:
    for ceiling, label in RESIDUAL_THRESHOLDS:
        if value < ceiling: return label
    return ResidualClass.BROAD


def _evaluate(caps: tuple[Capability, ...], ints: tuple[Intervention, ...]) -> tuple[tuple[ResidualStep, ...], Decimal]:
    remaining = dict(BURDEN); support = {c.identifier: c.support for c in caps}; steps=[]
    for item in ints:
        if item.capability_id and support[item.capability_id] is SupportState.NOT_SUPPORTED:
            steps.append(ResidualStep(item.identifier, item.stage, Decimal(), sum(remaining.values()))); continue
        addressed = Decimal()
        for category, fraction in item.coverage:
            recovery = remaining[category] * fraction
            remaining[category] -= recovery; addressed += recovery
        steps.append(ResidualStep(item.identifier, item.stage, addressed, sum(remaining.values())))
    return tuple(steps), sum(remaining.values())


def _assessment(key="BASELINE", name="Configuration-first baseline", caps=None, ints=None,
                evidence=EvidenceLabel.MODELED_ASSUMPTION, recommendation="CONFIGURE, THEN MEASURE") -> ConfigurationAssessment:
    caps=capabilities() if caps is None else caps; ints=interventions() if ints is None else ints
    steps,residual=_evaluate(caps,ints); value=sum(v for _,v in BURDEN)-residual
    active=[i for i,s in zip(ints,steps) if s.addressed]
    config_hours=sum(i.effort_hours for i in active); engineering_hours=24
    acquisition_hours=54; elapsed_days=70; price=Decimal("44000"); annual_support=Decimal("6000")
    rates={x.category:x.hourly_cost for x in load_formal_rfp_motion().labor_rates}
    delivery=Decimal(config_hours)*rates[WorkCategory.SOLUTIONS]+Decimal(engineering_hours)*rates[WorkCategory.ENGINEERING]
    acquisition=Decimal(acquisition_hours)*rates[WorkCategory.SALES]
    contribution=price-delivery-acquisition
    seller=SellerEconomics(price,delivery,acquisition,Decimal(),contribution,contribution/price,EvidenceLabel.OBSERVED_LAB_RESULT)
    cost=price+annual_support; net=value-cost
    econ=ConfigurationEconomics(value,residual,value/sum(v for _,v in BURDEN),price,annual_support,cost,net,
                                price/value*12,config_hours,engineering_hours,acquisition_hours,elapsed_days,seller)
    project=GateStatus.PASS if net >= 0 else GateStatus.FAIL
    target=GateStatus.PASS if project is GateStatus.PASS and contribution >= Decimal("10000") else GateStatus.FAIL
    rc=classify_residual(residual)
    if project is GateStatus.FAIL: verdict="NO DEAL"
    elif target is GateStatus.FAIL: verdict="POOR TARGET CUSTOMER"
    elif rc is ResidualClass.IMMATERIAL: verdict="CONFIGURE / BUY"
    elif rc in (ResidualClass.NARROW, ResidualClass.MATERIAL): verdict="NARROW CUSTOM EDGE"
    else: verdict="INVESTIGATE"
    candidate="READ-ONLY CROSS-SOURCE RECONCILIATION VIEW (Chapter 6 candidate only)" if rc in (ResidualClass.NARROW,ResidualClass.MATERIAL) else None
    return ConfigurationAssessment(key,name,caps,ints,steps,rc,econ,project,target,verdict,recommendation,evidence,candidate)


def configuration_scenarios() -> tuple[ConfigurationAssessment, ...]:
    basecaps=capabilities(); baseints=interventions(); base=_assessment()
    strong_caps=tuple(replace(c,support=SupportState.CONFIGURABLE) if c.identifier=="cross_system_reconciliation" else c for c in basecaps)
    strong_ints=baseints+(Intervention("CROSS_SYSTEM_RECONCILIATION","NATIVE_AUTOMATION_REPORTING","cross_system_reconciliation",(("duplicate_entry",Decimal("0.80")),("status_reconciliation",Decimal("0.70"))),20,5,"Fictional stronger-incumbent capability."),)
    weak_ids={"scheduled_reports","notifications","duplicate_warnings","correction_tracking","rule_automation"}
    weak_caps=tuple(replace(c,support=SupportState.NOT_SUPPORTED,enabled=False) if c.identifier in weak_ids else c for c in basecaps)
    poor_ints=(replace(baseints[0],coverage=(("status_reconciliation",Decimal("0.80")),("lookup_search",Decimal("0.20"))),effort_hours=40),)+baseints[1:]
    return (base,
      _assessment("STRONG_INCUMBENT","Strong incumbent capability",strong_caps,strong_ints,EvidenceLabel.MODELED_ALTERNATIVE_ASSUMPTION),
      _assessment("WEAK_INCUMBENT","Weak incumbent capability",weak_caps,baseints,EvidenceLabel.SENSITIVITY_ASSUMPTION),
      _assessment("POOR_STANDARDIZATION","Poor standardization",basecaps,poor_ints,EvidenceLabel.SENSITIVITY_ASSUMPTION,"STANDARDIZE FIRST"))


def assess_configuration_first() -> ConfigurationAssessment: return configuration_scenarios()[0]
