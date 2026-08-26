"""Chapter 19: normalize and compare prior engagement-motion results.

This module deliberately contains no weighted score, Chapter 20 final verdict,
or best-to-worst ranking.  It
loads Chapter 4--18 results, gives unlike commercial fields common names, and
keeps unavailable/not-applicable values as ``None``.
"""
from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum
from functools import cache

from .acquisition import AcquisitionEconomics, acquisition_reports
from .baseline import load_baseline
from .closed_integration import assess_closed_integration, Feasibility
from .evidence import EvidenceLabel
from .governance import governance_scenarios
from .incumbent import AlternativeType, compare_alternatives
from .models import GateStatus
from .read_only import read_only_scenarios
from .throughput import portfolio_scenarios


class MotionFamily(StrEnum):
    DIRECT_CUSTOM="DIRECT_CUSTOM"; BOUNDED_ENTRY="BOUNDED_ENTRY"
    LOW_AUTHORITY_TECHNICAL="LOW_AUTHORITY_TECHNICAL"
    CONFIGURATION_INCUMBENT="CONFIGURATION_INCUMBENT"; CHANNEL="CHANNEL"
    PURCHASING_PATH_ADVANTAGE="PURCHASING_PATH_ADVANTAGE"; NO_ENGAGEMENT="NO_ENGAGEMENT"


class RepeatabilityResult(StrEnum):
    ONE_OFF="ONE_OFF"; REPEATABLE_WITHIN_ACCOUNT="REPEATABLE_WITHIN_ACCOUNT"
    REPEATABLE_PROJECT="REPEATABLE_PROJECT"; CROSS_CUSTOMER_CONDITIONAL="CROSS_CUSTOMER_CONDITIONAL"
    NOT_APPLICABLE="NOT_APPLICABLE"


class HypothesisStatus(StrEnum):
    STRENGTHENED="STRENGTHENED"; WEAKENED="WEAKENED"; CONDITIONAL="CONDITIONAL"
    NOT_RESOLVED="NOT RESOLVED"


@dataclass(frozen=True)
class GovernanceComparison:
    surface: str
    seller_delivery_hours: int | None
    seller_approval_acquisition_hours: int | None
    elapsed_review_days: int | None
    disposition: str


@dataclass(frozen=True)
class ThroughputComparison:
    contribution_per_deal: Decimal
    completed_engagements_per_year: int
    annualized_contribution: Decimal
    overloaded_periods: int
    deferred_hours: int


@dataclass(frozen=True)
class ViabilityDimensions:
    problem_attractiveness: GateStatus
    technical_feasibility: GateStatus
    customer_economics: GateStatus
    delivery_economics: GateStatus
    support_economics: GateStatus
    target_attractiveness: GateStatus


@dataclass(frozen=True)
class MotionComparison:
    identifier: str; name: str; family: MotionFamily; technical_posture: str
    customer_value_addressed: Decimal; residual_value: Decimal
    customer_implementation_price: Decimal; recurring_customer_cost: Decimal
    customer_first_year_cost: Decimal; customer_first_year_net_value: Decimal
    payback_months: Decimal | None; value_coverage_percent: Decimal
    seller_engagement_revenue: Decimal | None; engineering_configuration_hours: int | None
    seller_acquisition_hours: int | None; seller_acquisition_cost: Decimal | None
    acquisition_cost_percent_revenue: Decimal | None; seller_delivery_cost: Decimal | None
    seller_support_obligation: str; acquisition_adjusted_contribution: Decimal | None
    contribution_margin: Decimal | None; elapsed_cycle_days: int | None
    customer_economics_result: str; project_viability: GateStatus; target_viability: GateStatus
    technical_access_requirement: str; available_access_compatibility: str
    write_authority: str; read_only_capability: str; native_configuration_possible: str
    unsupported_access_risk: str; procurement_path: str; sponsor_requirement: str
    governance: GovernanceComparison; support_owner: str; escalation_model: str
    customer_relationship_owner: str; throughput: ThroughputComparison | None
    repeatability: RepeatabilityResult; major_risks: tuple[str, ...]
    commercial_verdict: str; viability: ViabilityDimensions
    evidence_sources: tuple[str, ...]; evidence: EvidenceLabel


EVIDENCE_PRECEDENCE = {
    "FORMAL_RFP_ECONOMICS": ("CHAPTER_4", "CHAPTER_15"),
    "PILOT_ECONOMICS": ("CHAPTER_5", "CHAPTER_15"),
    "READ_ONLY_TECHNICAL_SURFACE": ("CHAPTER_6", "CHAPTER_12", "CHAPTER_13"),
    "CONFIGURATION_RESIDUAL": ("CHAPTER_7", "CHAPTER_14"),
    "CONTRACT_SIZE_ECONOMICS": ("CHAPTER_8", "CHAPTER_9"),
    "PARTNER_MOTION": ("CHAPTER_10", "CHAPTER_15"),
    "EXISTING_PATH": ("CHAPTER_11", "CHAPTER_15"),
    "GOVERNANCE_ATTRIBUTION": ("CHAPTER_12",), "ACCESS_FEASIBILITY": ("CHAPTER_13",),
    "INCUMBENT_ALTERNATIVE": ("CHAPTER_14",), "THROUGHPUT": ("CHAPTER_16",),
    "REPEATABILITY": ("CHAPTER_17", "CHAPTER_18"),
}


@cache
def _governance(key: str, disposition="REMAINS_WITH_SELLER") -> GovernanceComparison:
    x=next(g for g in governance_scenarios() if g.key==key).metrics
    return GovernanceComparison(key,x.seller_delivery_hours,x.seller_acquisition_approval_hours,
                                x.elapsed_review_days,disposition)


@cache
def _throughput_rows() -> tuple[tuple[str, ThroughputComparison], ...]:
    return tuple((x.name, ThroughputComparison(x.opportunities[0].acquisition_adjusted_contribution,
        x.completed_per_year,x.annualized_contribution,x.overloaded_periods,x.deferred_hours)
        ) for x in portfolio_scenarios())


def _customer(value: Decimal, cost: Decimal):
    payback=(cost/value*Decimal(12)) if value else None
    return value-cost,payback,(value/load_baseline().burden.annual_recoverable_value*Decimal(100))


def _from_acquisition(r: AcquisitionEconomics, *, name: str, family: MotionFamily,
        posture: str, access: str, compatibility: str, procurement: str, sponsor: str,
        governance_key="WRITE_CAPABLE", governance_disposition="REMAINS_WITH_SELLER",
        support_owner="CUSTOM_SELLER", relationship="CUSTOM_SELLER", risks=(), verdict="CONDITIONAL",
        sources=(), repeatability=RepeatabilityResult.CROSS_CUSTOMER_CONDITIONAL) -> MotionComparison:
    recurring=r.customer_cost-r.implementation_revenue if r.motion!="PARTNER_LED" else Decimal("24000")
    implementation=r.customer_contract_value-recurring
    net,payback,coverage=_customer(r.customer_value_addressed,r.customer_cost)
    technical=GateStatus.FAIL if compatibility=="INCOMPATIBLE" else GateStatus.PASS
    customer=GateStatus.PASS if net>=0 else GateStatus.FAIL
    delivery=GateStatus.PASS if r.acquisition_adjusted_contribution>=r.minimum_contribution else GateStatus.FAIL
    target=GateStatus.PASS if technical is GateStatus.PASS and customer is GateStatus.PASS and delivery is GateStatus.PASS else GateStatus.FAIL
    margin=r.acquisition_adjusted_contribution/r.implementation_revenue
    support=GateStatus.PASS if recurring>=0 else GateStatus.FAIL
    return MotionComparison(r.motion,name,family,posture,r.customer_value_addressed,
        load_baseline().burden.annual_recoverable_value-r.customer_value_addressed,implementation,recurring,
        r.customer_cost,net,payback,coverage,r.implementation_revenue,r.engineering_hours,
        r.seller_acquisition_hours,r.acquisition_labor_cost,r.acquisition_cost_per_revenue*Decimal(100),
        r.delivery_labor_cost,"SELLER RETAINS ANNUAL SUPPORT OBLIGATION",r.acquisition_adjusted_contribution,
        margin,r.elapsed_days,"PASS" if customer is GateStatus.PASS else "FAIL",technical,target,access,
        compatibility,"REQUIRED" if "WRITE" in access else "NOT_REQUIRED","SUPPORTED" if "READ" in access or "EXPORT" in access else "LIMITED",
        "YES" if governance_key=="CONFIGURATION_FIRST" else "NO",
        "HARD_CONSTRAINT" if compatibility=="INCOMPATIBLE" else "CONDITIONAL",procurement,sponsor,
        _governance(governance_key,governance_disposition),support_owner,"SELLER TRIAGE; CUSTOMER/INCUMBENT ESCALATION",
        relationship,dict(_throughput_rows()).get(r.motion),repeatability,tuple(risks),
        "TECHNICALLY INFEASIBLE UNDER CLOSED ACCESS" if technical is GateStatus.FAIL else verdict,
        ViabilityDimensions(GateStatus.PASS,technical,customer,delivery,support,target),tuple(sources),EvidenceLabel.OBSERVED_LAB_RESULT)


def motion_comparisons() -> tuple[MotionComparison, ...]:
    """LOAD → NORMALIZE → COMPARE prior outputs; no new motion economics."""
    reports={x.motion:x for x in acquisition_reports()}; base=load_baseline().burden.annual_recoverable_value
    closed=assess_closed_integration().preferred_feasibility.status is Feasibility.NOT_FEASIBLE
    broad_compat="INCOMPATIBLE" if closed else "COMPATIBLE"
    rows=[
      _from_acquisition(reports["FORMAL_RFP"],name="Formal RFP",family=MotionFamily.DIRECT_CUSTOM,posture="BROAD_WRITE_CUSTOM",access="FULL_SUPPORTED_WRITE_API",compatibility=broad_compat,procurement="FORMAL_SOLICITATION",sponsor="HELPFUL_NOT_SUFFICIENT",risks=("HIGH_ACQUISITION_EFFORT","LONG_ELAPSED_CYCLE","HIGH_PRE_AWARD_TECHNICAL_WORK","CLOSED_ACCESS"),verdict="WEAK SELLER ECONOMICS",sources=("CHAPTER_4","CHAPTER_13","CHAPTER_15","CHAPTER_16")),
      _from_acquisition(reports["COOPERATIVE_PAID_PILOT"],name="Cooperative paid pilot",family=MotionFamily.BOUNDED_ENTRY,posture="BOUNDED_PILOT",access="APPROVED_PILOT_ACCESS",compatibility="CONDITIONAL",procurement="COOPERATIVE_PAID_PILOT",sponsor="STRONG_SPONSOR_REQUIRED",governance_key="READ_ONLY",risks=("BOUNDED_SCOPE","LOWER_ACQUISITION_SURFACE","LIMITED_VALUE_CAPTURE","REQUIRES_STRONG_SPONSOR"),verdict="PILOT-FIRST TARGET",sources=("CHAPTER_5","CHAPTER_12","CHAPTER_15","CHAPTER_16")),
      _from_acquisition(reports["CONFIGURATION_FIRST"],name="Configuration-first",family=MotionFamily.CONFIGURATION_INCUMBENT,posture="NATIVE_CONFIGURATION",access="SUPPORTED_NATIVE_ACCESS",compatibility="COMPATIBLE",procurement="CONFIGURATION_SERVICES",sponsor="OPERATIONAL_SPONSOR",governance_key="CONFIGURATION_FIRST",governance_disposition="SHIFTS_TO_INCUMBENT",support_owner="INCUMBENT_AND_CONFIGURATION_SELLER",risks=("NATIVE_CAPABILITY_USED","LOWER_CUSTOM_OWNERSHIP","RESIDUAL_REMAINS"),verdict="CONDITIONAL ON RESIDUAL",sources=("CHAPTER_7","CHAPTER_12","CHAPTER_14","CHAPTER_15")),
      _from_acquisition(reports["SMALL_DEPARTMENTAL"],name="Small departmental project",family=MotionFamily.BOUNDED_ENTRY,posture="BOUNDED_DEPARTMENTAL",access="APPROVED_EXPORT_OR_READ_ONLY_API",compatibility="CONDITIONAL",procurement="SMALL_PROJECT_PATH",sponsor="DEPARTMENT_SPONSOR",governance_key="READ_ONLY",risks=("LIMITED_VALUE_CAPTURE","MINIMUM_CONTRIBUTION_MISSED"),verdict="ECONOMICALLY FRAGILE",sources=("CHAPTER_8","CHAPTER_15")),
      _from_acquisition(reports["JUSTIFIED_LARGER_CONTRACT"],name="Larger justified contract",family=MotionFamily.DIRECT_CUSTOM,posture="JUSTIFIED_BROADER_SCOPE",access="APPROVED_SUPPORTED_INTERFACE",compatibility="CONDITIONAL",procurement="JUSTIFIED_LARGER_CONTRACT",sponsor="STRONG_CROSS_FUNCTIONAL_SPONSOR",risks=("LARGER_DELIVERY_COMMITMENT","SCOPE_JUSTIFICATION_REQUIRED"),verdict="VIABLE IF SCOPE IS JUSTIFIED",sources=("CHAPTER_9","CHAPTER_15")),
      _from_acquisition(reports["PARTNER_LED"],name="Partner / channel",family=MotionFamily.CHANNEL,posture="PARTNER_LED_BROAD_CUSTOM",access="FULL_SUPPORTED_WRITE_API",compatibility=broad_compat,procurement="PARTNER_OR_PRIME_PATH",sponsor="PARTNER_AND_CUSTOMER_SPONSOR",governance_disposition="SHIFTS_TO_PARTNER",support_owner="CUSTOM_SELLER_WITH_PARTNER_FRONTLINE",relationship="PARTNER",risks=("LOWER_SELLER_ACQUISITION","CHANNEL_COST","PARTNER_DEPENDENCY","REDUCED_CUSTOMER_RELATIONSHIP_OWNERSHIP"),verdict="CONDITIONAL ON PARTNER LEVERAGE",sources=("CHAPTER_10","CHAPTER_12","CHAPTER_15","CHAPTER_16")),
      _from_acquisition(reports["EXISTING_PURCHASING_PATH"],name="Existing purchasing path",family=MotionFamily.PURCHASING_PATH_ADVANTAGE,posture="BROAD_CUSTOM_EXISTING_PATH",access="FULL_SUPPORTED_WRITE_API",compatibility=broad_compat,procurement="EXISTING_CONTRACT_VEHICLE",sponsor="BUYER_ACCESS_STILL_REQUIRED",risks=("LOWER_PROCUREMENT_WORK","BUYER_ACCESS_STILL_REQUIRED","TECHNICAL_GOVERNANCE_REMAINS"),verdict="IMPROVED DIRECT ECONOMICS",sources=("CHAPTER_11","CHAPTER_12","CHAPTER_13","CHAPTER_15","CHAPTER_16")),
    ]
    # Chapter 6's read-only result is intentionally not reconstructed through Chapter 15.
    ro=next(x for x in read_only_scenarios() if x.scenario.key=="READ_ONLY_REPORTING_EDGE"); e=ro.economics; s=e.seller
    net,payback,coverage=_customer(e.value_addressed,e.first_year_customer_cost)
    rows.insert(2,MotionComparison("READ_ONLY_EDGE","Read-only pilot / edge",MotionFamily.LOW_AUTHORITY_TECHNICAL,"READ_ONLY_REPORTING_EDGE",e.value_addressed,base-e.value_addressed,e.engagement_price,e.support,e.first_year_customer_cost,net,payback,coverage,s.implementation_revenue,ro.scenario.engineering_hours,e.acquisition_hours,s.acquisition_labor_cost,s.acquisition_labor_cost/s.implementation_revenue*100,s.delivery_labor_cost,"CUSTOM SELLER SUPPORTS EXPORT, MAPPINGS, REPORTS, AND ACCESS EXPIRATION",s.acquisition_adjusted_contribution,s.contribution_margin,e.elapsed_days,"PASS",ro.project_viability,ro.target_viability,"APPROVED_EXPORT_OR_READ_ONLY_API","COMPATIBLE","PROHIBITED","SUPPORTED","NO","CONDITIONAL", "BOUNDED_PILOT_PATH","STRONG_SPONSOR_REQUIRED",_governance("READ_ONLY","WRITE_WORK_DISAPPEARS; COMMON REVIEWS REMAIN"),"CUSTOM_SELLER","SELLER TRIAGE; CUSTOMER/INCUMBENT ACCESS ESCALATION","CUSTOM_SELLER",None,RepeatabilityResult.CROSS_CUSTOMER_CONDITIONAL,("LOWER_TECHNICAL_AUTHORITY","LOWER_GOVERNANCE_SURFACE","REDUCED_VALUE_CAPTURE","INTERFACE_CHANGE_DEPENDENCY"),ro.verdict,ViabilityDimensions(GateStatus.PASS,GateStatus.PASS,GateStatus.PASS,GateStatus.PASS,GateStatus.PASS,ro.target_viability),("CHAPTER_6","CHAPTER_12","CHAPTER_13","CHAPTER_14"),EvidenceLabel.OBSERVED_LAB_RESULT))
    inc=next(x for x in compare_alternatives() if x.alternative.alternative_type is AlternativeType.INCUMBENT_MODULE); a=inc.alternative;e=inc.economics
    rows.append(MotionComparison("INCUMBENT_BUY_CONFIGURE","Incumbent buy / configure",MotionFamily.CONFIGURATION_INCUMBENT,"INCUMBENT_MODULE",e.annual_value_addressed,e.residual_value,a.implementation_price,a.recurring_fee,e.first_year_customer_cost,e.first_year_net_recoverable_value,e.full_first_year_payback_months,e.percent_addressed*100,None,a.provider_effort_hours,None,None,None,None,"INCUMBENT VENDOR OWNS SUPPORT; PROFITABILITY NOT MODELED",None,None,a.implementation_duration_days,"PASS",GateStatus.PASS,GateStatus.PASS,a.technical_access_required,"COMPATIBLE","NATIVE_VENDOR_ONLY","NOT_REQUIRED","YES","LOW", "INCUMBENT_PURCHASING_PATH","OPERATIONAL_SPONSOR",_governance("CONFIGURATION_FIRST","SHIFTS_TO_INCUMBENT"),a.support_owner,"INCUMBENT SINGLE SUPPORT OWNER","INCUMBENT_VENDOR",None,RepeatabilityResult.NOT_APPLICABLE,tuple(x.value for x in a.risk_findings),inc.commercial_result,ViabilityDimensions(GateStatus.PASS,GateStatus.PASS,GateStatus.PASS,GateStatus.NOT_EVALUATED,GateStatus.PASS,GateStatus.PASS),("CHAPTER_7","CHAPTER_12","CHAPTER_13","CHAPTER_14"),EvidenceLabel.MODELED_ALTERNATIVE_ASSUMPTION))
    rows.append(MotionComparison("NO_ENGAGEMENT","No engagement",MotionFamily.NO_ENGAGEMENT,"NONE",Decimal(),base,Decimal(),Decimal(),Decimal(),Decimal(),None,Decimal(),None,None,0,Decimal(),None,Decimal(),"NONE",None,None,0,"BASELINE",GateStatus.NOT_EVALUATED,GateStatus.NOT_EVALUATED,"NOT_APPLICABLE","NOT_APPLICABLE","NONE","NONE","NO","NONE","NONE","NONE",GovernanceComparison("NONE",0,0,0,"WORK_NOT_STARTED"),"NONE","NONE","NONE",None,RepeatabilityResult.NOT_APPLICABLE,("FULL_RECOVERABLE_VALUE_REMAINS",),"BASELINE — ACTION MUST BE JUSTIFIED",ViabilityDimensions(GateStatus.PASS,GateStatus.NOT_EVALUATED,GateStatus.NOT_EVALUATED,GateStatus.NOT_EVALUATED,GateStatus.NOT_EVALUATED,GateStatus.NOT_EVALUATED),("CHAPTER_0","CHAPTER_14"),EvidenceLabel.OBSERVED_IMPLEMENTATION_STRUCTURE))
    return tuple(rows)


def conditional_findings() -> tuple[str, ...]:
    return ("WEAK_BUYER_ACCESS: partner-led may improve direct acquisition, but channel cost and access remain.",
      "HIGH_INCUMBENT_COVERAGE: buy/configure may avoid custom ownership.",
      "STRONG_SPONSOR_AND_BOUNDED_SCOPE: pilot-first may improve on a formal RFP.",
      "EXISTING_PURCHASING_PATH: procurement work falls; buyer access and technical governance remain.",
      "CLOSED_ACCESS: broad custom motions are infeasible before economics.",
      "NARROW_CONFIGURATION_RESIDUAL: a read-only custom edge may be justified.")


def hypothesis_status() -> tuple[HypothesisStatus, tuple[str, ...]]:
    rows=motion_comparisons(); viable=[x for x in rows if x.target_viability is GateStatus.PASS]
    failed=[x for x in rows if x.target_viability is GateStatus.FAIL]
    status=HypothesisStatus.CONDITIONAL if viable and failed else (HypothesisStatus.WEAKENED if viable else HypothesisStatus.STRENGTHENED)
    return status,("Engagement-motion variation materially changes acquisition, access, contribution, and cycle evidence.",
      f"{len(viable)} motions pass target viability while {len(failed)} fail under the normalized scenario.",
      "This Chapter 19 synthesis is evidence for, not the final Chapter 20 verdict.")
