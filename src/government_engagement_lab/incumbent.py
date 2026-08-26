"""Chapter 14: compare fictional incumbent and custom alternatives without a score."""

from dataclasses import dataclass, replace
from decimal import Decimal
from enum import StrEnum

from .baseline import _fixture
from .closed_integration import Feasibility, evaluate_access, intervention_requirements
from .configuration import BURDEN
from .evidence import EvidenceLabel, parse_evidence_label
from .formal_rfp import assess_formal_rfp
from .governance import governance_scenarios
from .models import SellerEconomics
from .read_only import read_only_scenarios


class AlternativeType(StrEnum):
    DO_NOTHING = "DO_NOTHING"
    CONFIGURATION = "CONFIGURATION"
    INCUMBENT_MODULE = "INCUMBENT_MODULE"
    INCUMBENT_SERVICES = "INCUMBENT_SERVICES"
    CUSTOM_EDGE = "CUSTOM_EDGE"
    CUSTOM_INTEGRATION = "CUSTOM_INTEGRATION"


class AlternativeRisk(StrEnum):
    SUPPORTED_VENDOR_PATH="SUPPORTED_VENDOR_PATH"; NATIVE_DATA_MODEL="NATIVE_DATA_MODEL"
    NATIVE_AUTHENTICATION="NATIVE_AUTHENTICATION"; SINGLE_SUPPORT_OWNER="SINGLE_SUPPORT_OWNER"
    LOWER_CUSTOM_INTEGRATION_SURFACE="LOWER_CUSTOM_INTEGRATION_SURFACE"; LOWER_VENDOR_CONFLICT="LOWER_VENDOR_CONFLICT"
    LIMITED_CUSTOMIZATION="LIMITED_CUSTOMIZATION"; VENDOR_ROADMAP_DEPENDENCY="VENDOR_ROADMAP_DEPENDENCY"
    RECURRING_LICENSE_COST="RECURRING_LICENSE_COST"; LIMITED_CROSS_SYSTEM_LOGIC="LIMITED_CROSS_SYSTEM_LOGIC"
    LIMITED_EXCEPTION_HANDLING="LIMITED_EXCEPTION_HANDLING"; TAILORED_RESIDUAL_COVERAGE="TAILORED_RESIDUAL_COVERAGE"
    CROSS_SYSTEM_RECONCILIATION="CROSS_SYSTEM_RECONCILIATION"; CUSTOM_EXCEPTION_LOGIC="CUSTOM_EXCEPTION_LOGIC"
    CUSTOM_SUPPORT_OBLIGATION="CUSTOM_SUPPORT_OBLIGATION"; INTEGRATION_DEPENDENCY="INTEGRATION_DEPENDENCY"
    HIGHER_DELIVERY_RISK="HIGHER_DELIVERY_RISK"; CUSTOM_GOVERNANCE_SURFACE="CUSTOM_GOVERNANCE_SURFACE"


@dataclass(frozen=True)
class SolutionAlternative:
    identifier: str; display_name: str; alternative_type: AlternativeType; provider: str
    implementation_model: str; capabilities: tuple[str, ...]; limitations: tuple[str, ...]
    value_categories: tuple[str, ...]; implementation_price: Decimal; recurring_fee: Decimal
    customer_effort_hours: int; provider_effort_hours: int; implementation_duration_days: int
    technical_access_required: str; governance_surface: str; support_owner: str
    custom_ownership_required: bool; supportable: bool; acquisition_viable: bool
    evidence: EvidenceLabel; risk_findings: tuple[AlternativeRisk, ...] = ()


@dataclass(frozen=True)
class AlternativeEconomics:
    annual_value_addressed: Decimal; residual_value: Decimal; percent_addressed: Decimal
    implementation_cost: Decimal; recurring_cost: Decimal; first_year_customer_cost: Decimal
    first_year_net_recoverable_value: Decimal; implementation_payback_months: Decimal | None
    full_first_year_payback_months: Decimal | None; evidence: EvidenceLabel = EvidenceLabel.OBSERVED_LAB_RESULT


@dataclass(frozen=True)
class AlternativeAssessment:
    alternative: SolutionAlternative; economics: AlternativeEconomics; feasible: bool
    adequate: bool; access_result: str; commercial_result: str
    seller_economics: SellerEconomics | None = None


@dataclass(frozen=True)
class IncumbentScenario:
    key: str; name: str; assessments: tuple[AlternativeAssessment, ...]; selected_result: str
    changed_assumptions: tuple[str, ...]; evidence: EvidenceLabel


def load_incumbent_fixture() -> dict:
    return _fixture("incumbent_alternatives.json")


def burden_values() -> dict[str, Decimal]:
    return dict(BURDEN)


def _risks(kind: AlternativeType) -> tuple[AlternativeRisk, ...]:
    if kind in (AlternativeType.INCUMBENT_MODULE, AlternativeType.INCUMBENT_SERVICES, AlternativeType.CONFIGURATION):
        return (AlternativeRisk.SUPPORTED_VENDOR_PATH, AlternativeRisk.NATIVE_DATA_MODEL,
                AlternativeRisk.NATIVE_AUTHENTICATION, AlternativeRisk.SINGLE_SUPPORT_OWNER,
                AlternativeRisk.LOWER_CUSTOM_INTEGRATION_SURFACE, AlternativeRisk.LIMITED_CUSTOMIZATION,
                AlternativeRisk.VENDOR_ROADMAP_DEPENDENCY, AlternativeRisk.RECURRING_LICENSE_COST,
                AlternativeRisk.LIMITED_CROSS_SYSTEM_LOGIC, AlternativeRisk.LIMITED_EXCEPTION_HANDLING)
    if kind in (AlternativeType.CUSTOM_EDGE, AlternativeType.CUSTOM_INTEGRATION):
        return (AlternativeRisk.TAILORED_RESIDUAL_COVERAGE, AlternativeRisk.CROSS_SYSTEM_RECONCILIATION,
                AlternativeRisk.CUSTOM_EXCEPTION_LOGIC, AlternativeRisk.CUSTOM_SUPPORT_OBLIGATION,
                AlternativeRisk.INTEGRATION_DEPENDENCY, AlternativeRisk.HIGHER_DELIVERY_RISK,
                AlternativeRisk.CUSTOM_GOVERNANCE_SURFACE)
    return ()


def load_alternatives() -> tuple[SolutionAlternative, ...]:
    result=[]
    for x in load_incumbent_fixture()["alternatives"]:
        kind=AlternativeType(x["type"])
        result.append(SolutionAlternative(x["id"],x["name"],kind,x["provider"],x["implementation_model"],
            tuple(x["capabilities"]),tuple(x["limitations"]),tuple(x["categories"]),Decimal(x["implementation_price"]),
            Decimal(x["recurring_fee"]),x["customer_effort_hours"],x["provider_effort_hours"],x["duration_days"],
            x["technical_access"],x["governance_surface"],x["support_owner"],x["custom_ownership"],
            x["supportable"],x["acquisition_viable"],parse_evidence_label(x["evidence"]),_risks(kind)))
    validate_alternatives(tuple(result))
    return tuple(result)


def validate_alternatives(items: tuple[SolutionAlternative, ...]) -> None:
    ids=[x.identifier for x in items]; valid=set(burden_values())
    if len(ids)!=len(set(ids)): raise ValueError("alternative identifiers must be unique")
    for x in items:
        if not set(x.value_categories)<=valid: raise ValueError(f"unknown burden category for {x.identifier}")
        if x.implementation_price < 0 or x.recurring_fee < 0: raise ValueError("alternative costs must be explicit and nonnegative")


def calculate_alternative_economics(item: SolutionAlternative) -> AlternativeEconomics:
    burden=burden_values(); total=sum(burden.values())
    # Sets ensure a burden category is counted once even if several capabilities address it.
    value=sum(burden[x] for x in set(item.value_categories)); value=min(value,total)
    residual=total-value; first=item.implementation_price+item.recurring_fee
    implementation_payback=(item.implementation_price/value*12) if value else None
    full_payback=(first/value*12) if value else None
    return AlternativeEconomics(value,residual,value/total if total else Decimal(),item.implementation_price,
        item.recurring_fee,first,value-first,implementation_payback,full_payback)


def is_adequate(econ: AlternativeEconomics) -> bool:
    rule=load_incumbent_fixture()["adequacy"]
    return econ.percent_addressed >= Decimal(rule["minimum_percent"]) and econ.residual_value <= Decimal(rule["maximum_residual"])


def _seller(item: SolutionAlternative) -> SellerEconomics | None:
    if not item.custom_ownership_required: return None
    if item.alternative_type is AlternativeType.CUSTOM_INTEGRATION: return assess_formal_rfp().seller_economics
    return next(x for x in read_only_scenarios() if x.scenario.key=="READ_ONLY_REPORTING_EDGE").economics.seller


def assess_alternative(item: SolutionAlternative, third_party_access=True) -> AlternativeAssessment:
    econ=calculate_alternative_economics(item)
    access=True
    if item.custom_ownership_required and not third_party_access: access=False
    feasible=access and item.supportable
    adequate=is_adequate(econ)
    result="NO DEAL"
    if feasible and econ.first_year_net_recoverable_value >= 0:
        if not item.custom_ownership_required and adequate: result="CONFIGURE / BUY"
        elif item.alternative_type is AlternativeType.CUSTOM_EDGE: result="NARROW CUSTOM EDGE"
        elif item.alternative_type is AlternativeType.CUSTOM_INTEGRATION and item.acquisition_viable: result="CUSTOM INTEGRATION"
        else: result="INVESTIGATE"
    return AlternativeAssessment(item,econ,feasible,adequate,
        "SUPPORTED_NATIVE_ACCESS" if not item.custom_ownership_required else ("SUPPORTED" if access else "NOT_FEASIBLE: SUPPORTED_INTERFACE_UNAVAILABLE"),result,_seller(item))


def compare_alternatives(items=None, third_party_access=True) -> tuple[AlternativeAssessment, ...]:
    return tuple(assess_alternative(x,third_party_access) for x in (items or load_alternatives()))


def select_result(assessments: tuple[AlternativeAssessment, ...]) -> str:
    # Feasibility → economics → adequacy → support/acquisition; then lower custom ownership.
    native=[x for x in assessments if not x.alternative.custom_ownership_required and x.alternative.alternative_type is not AlternativeType.DO_NOTHING
            and x.feasible and x.economics.first_year_net_recoverable_value>=0 and x.adequate and x.alternative.acquisition_viable]
    if native: return "CONFIGURE / BUY"
    edge=[x for x in assessments if x.alternative.alternative_type is AlternativeType.CUSTOM_EDGE and x.feasible
          and x.economics.first_year_net_recoverable_value>=0 and x.alternative.acquisition_viable]
    if edge: return "NARROW CUSTOM EDGE"
    broad=[x for x in assessments if x.alternative.alternative_type is AlternativeType.CUSTOM_INTEGRATION and x.feasible
           and x.economics.first_year_net_recoverable_value>=0 and x.alternative.acquisition_viable]
    return "CUSTOM INTEGRATION" if broad else "NO DEAL"


def incumbent_scenarios() -> tuple[IncumbentScenario, ...]:
    base=load_alternatives(); module=next(x for x in base if x.identifier=="INCUMBENT_MODULE")
    def build(key,name,replacement,access=True,changes=(),weak_native=False):
        items=tuple(replacement if x.identifier=="INCUMBENT_MODULE" else
            (replace(x,value_categories=replacement.value_categories) if weak_native and x.alternative_type in
             (AlternativeType.CONFIGURATION,AlternativeType.INCUMBENT_SERVICES) else x) for x in base)
        assessed=compare_alternatives(items,access)
        return IncumbentScenario(key,name,assessed,select_result(assessed),changes,
            EvidenceLabel.MODELED_ALTERNATIVE_ASSUMPTION if key=="CREDIBLE" else EvidenceLabel.SENSITIVITY_ASSUMPTION)
    strong=replace(module,value_categories=tuple(burden_values()),implementation_price=Decimal("24000"),implementation_duration_days=40)
    weak=replace(module,value_categories=("status_reconciliation","report_preparation","lookup_search"))
    expensive=replace(module,implementation_price=Decimal("95000"),recurring_fee=Decimal("35000"))
    return (build("CREDIBLE","Credible incumbent module",module),
        build("STRONG","Strong incumbent module",strong,changes=("Coverage expands to every modeled burden category; implementation price and duration decrease.",)),
        build("WEAK","Weak incumbent module",weak,changes=("The weak native-capability sensitivity removes correction administration and workflow rework coverage from native options.",),weak_native=True),
        build("EXPENSIVE","Expensive incumbent module",expensive,changes=("Capability is unchanged; implementation and recurring prices increase.",)),
        build("INCUMBENT_ONLY_ACCESS","Incumbent-only supported access",strong,False,("Chapter 13 third-party supported access is unavailable; native incumbent access remains supported.",)))


def assess_incumbent() -> IncumbentScenario:
    return incumbent_scenarios()[0]


def governance_ownership(surface: str):
    key="CONFIGURATION_FIRST" if surface=="CONFIGURATION_FIRST" else ("READ_ONLY" if surface=="READ_ONLY" else "WRITE_CAPABLE")
    return next(x for x in governance_scenarios() if x.key==key)


def chapter13_access_is_closed() -> bool:
    req=next(x for x in intervention_requirements() if x.identifier=="BROAD_WRITE_INTEGRATION")
    return evaluate_access(req,(),False).status is Feasibility.NOT_FEASIBLE
