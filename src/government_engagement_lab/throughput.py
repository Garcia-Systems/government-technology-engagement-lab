"""Chapter 16 deterministic pipeline-capacity laboratory.

Hours are lumpy monthly workload buckets.  Elapsed days determine how long an
opportunity stays open, but are never converted to labor cost.
"""
from dataclasses import dataclass, replace
from decimal import Decimal
from enum import StrEnum
import json
from importlib.resources import files

from .acquisition import acquisition_report
from .evidence import EvidenceLabel


class SellerRole(StrEnum):
    SOLUTIONS_ENGINEER = "SOLUTIONS_ENGINEER"
    SELLER_ACCOUNT_LEAD = "SELLER_ACCOUNT_LEAD"
    SHARED_ENGINEERING_SUPPORT = "SHARED_ENGINEERING_SUPPORT"


class CapacityState(StrEnum):
    AVAILABLE = "AVAILABLE"
    AT_CAPACITY = "AT_CAPACITY"
    OVER_CAPACITY = "OVER_CAPACITY"


@dataclass(frozen=True)
class RoleCapacity:
    role: SellerRole
    monthly_work_hours: int
    acquisition_capacity_percent: Decimal
    non_acquisition_reserve_hours: int
    evidence: EvidenceLabel

    @property
    def acquisition_capacity_hours(self) -> int:
        return int(Decimal(self.monthly_work_hours) * self.acquisition_capacity_percent)


@dataclass(frozen=True)
class SellerOrganization:
    roles: tuple[RoleCapacity, ...]
    modeled_period_days: int
    fiction_notice: str
    evidence: EvidenceLabel = EvidenceLabel.MODELED_ASSUMPTION

    @property
    def monthly_acquisition_capacity(self) -> int:
        return sum(role.acquisition_capacity_hours for role in self.roles)


@dataclass(frozen=True)
class PipelineOpportunity:
    identifier: str
    motion: str
    start_period: int
    workload: tuple[int, ...]
    elapsed_days: int
    expected_implementation_revenue: Decimal
    acquisition_adjusted_contribution: Decimal
    status: str = "PLANNED_SUCCESS"
    evidence: EvidenceLabel = EvidenceLabel.MODELED_ASSUMPTION


@dataclass(frozen=True)
class PeriodResult:
    period: int
    available_capacity: int
    acquisition_demand: int
    work_completed: int
    deferred_hours: int
    active_opportunity_count: int
    completed_identifiers: tuple[str, ...]

    @property
    def unused_capacity(self) -> int:
        return max(0, self.available_capacity - self.work_completed)

    @property
    def state(self) -> CapacityState:
        if self.acquisition_demand > self.available_capacity:
            return CapacityState.OVER_CAPACITY
        if self.acquisition_demand == self.available_capacity:
            return CapacityState.AT_CAPACITY
        return CapacityState.AVAILABLE


@dataclass(frozen=True)
class PortfolioResult:
    name: str
    opportunities: tuple[PipelineOpportunity, ...]
    periods: tuple[PeriodResult, ...]
    completion_periods: tuple[tuple[str, int], ...]
    base_capacity: int
    evidence: EvidenceLabel = EvidenceLabel.OBSERVED_LAB_RESULT

    @property
    def completed_per_year(self): return sum(p <= 12 for _, p in self.completion_periods)
    @property
    def annualized_contribution(self):
        completed={i for i,p in self.completion_periods if p<=12}
        return sum((o.acquisition_adjusted_contribution for o in self.opportunities if o.identifier in completed),Decimal())
    @property
    def overloaded_periods(self): return sum(p.state is CapacityState.OVER_CAPACITY for p in self.periods[:12])
    @property
    def deferred_hours(self): return sum(p.deferred_hours for p in self.periods[:12])
    @property
    def unused_capacity(self): return sum(p.unused_capacity for p in self.periods[:12])
    @property
    def average_active(self): return Decimal(sum(p.active_opportunity_count for p in self.periods[:12]))/Decimal(12)
    @property
    def average_cycle_periods(self):
        by_id={o.identifier:o for o in self.opportunities}; done=[p-by_id[i].start_period+1 for i,p in self.completion_periods]
        return Decimal(sum(done))/Decimal(len(done)) if done else Decimal()


def _fixture():
    return json.loads(files("government_engagement_lab.fixtures").joinpath("seller_capacity.json").read_text())


def load_seller_organization() -> SellerOrganization:
    data=_fixture()
    roles=tuple(RoleCapacity(SellerRole(x["role"]),x["monthly_work_hours"],Decimal(x["acquisition_capacity_percent"]),x["non_acquisition_reserve_hours"],EvidenceLabel(x["evidence"])) for x in data["roles"])
    return SellerOrganization(roles,data["modeled_period_days"],data["fiction_notice"])


def workload_profile(motion: str) -> tuple[int,...]:
    profile=tuple(_fixture()["workload_profiles"][motion])
    if sum(profile) != acquisition_report(motion).seller_acquisition_hours:
        raise ValueError("workload profile must reconcile to Chapter 15 acquisition hours")
    return profile


def opportunity(identifier: str, motion: str, start_period: int, status="PLANNED_SUCCESS") -> PipelineOpportunity:
    report=acquisition_report(motion)
    revenue=Decimal() if status=="LOST" else report.implementation_revenue
    contribution=-report.acquisition_labor_cost if status=="LOST" else report.acquisition_adjusted_contribution
    return PipelineOpportunity(identifier,motion,start_period,workload_profile(motion),report.elapsed_days,revenue,contribution,status)


def simulate(name: str, opportunities, organization=None, horizon=24) -> PortfolioResult:
    """FIFO rule: capacity completes the oldest active bucket first; unfinished
    bucket hours roll forward and pause that opportunity's stage progression.
    Demand reports all due work before capacity is applied.
    """
    org=organization or load_seller_organization(); opportunities=tuple(opportunities)
    state={o.identifier:{"index":0,"remaining":0,"done":None} for o in opportunities}; rows=[]
    for period in range(1,horizon+1):
        active=[o for o in opportunities if o.start_period<=period and state[o.identifier]["done"] is None]
        due=[]
        for o in active:
            s=state[o.identifier]
            if not s["remaining"] and s["index"]<len(o.workload): s["remaining"]=o.workload[s["index"]]
            due.append((o,s["remaining"]))
        demand=sum(x for _,x in due); available=org.monthly_acquisition_capacity; completed=[]
        for o,_ in due:
            s=state[o.identifier]; used=min(available,s["remaining"]); available-=used; s["remaining"]-=used
            if s["remaining"]==0:
                s["index"]+=1
                if s["index"]==len(o.workload): s["done"]=period; completed.append(o.identifier)
        rows.append(PeriodResult(period,org.monthly_acquisition_capacity,demand,org.monthly_acquisition_capacity-available,max(0,demand-org.monthly_acquisition_capacity),len(active),tuple(completed)))
        if period>=12 and all(s["done"] is not None for s in state.values()): break
    completions=tuple((o.identifier,state[o.identifier]["done"]) for o in opportunities if state[o.identifier]["done"] is not None)
    return PortfolioResult(name,opportunities,tuple(rows),completions,org.monthly_acquisition_capacity)


def motion_portfolio(motion: str, organization=None):
    arrivals=_fixture()["arrival_periods"]
    return simulate(motion,tuple(opportunity(f"{motion}-{n}",motion,p) for n,p in enumerate(arrivals,1)),organization)


def portfolio_scenarios():
    motions=("FORMAL_RFP","COOPERATIVE_PAID_PILOT","PARTNER_LED","EXISTING_PURCHASING_PATH")
    return tuple(motion_portfolio(m) for m in motions)


def mixed_portfolio():
    specs=(("MIX-RFP","FORMAL_RFP",1),("MIX-P1","COOPERATIVE_PAID_PILOT",2),("MIX-E1","EXISTING_PURCHASING_PATH",3),("MIX-P2","COOPERATIVE_PAID_PILOT",5),("MIX-E2","EXISTING_PURCHASING_PATH",7))
    return simulate("MIXED",tuple(opportunity(*x) for x in specs))


def additional_capacity_sensitivity():
    org=load_seller_organization(); se=next(x for x in org.roles if x.role is SellerRole.SOLUTIONS_ENGINEER)
    extra=replace(se,evidence=EvidenceLabel.SENSITIVITY_ASSUMPTION)
    return motion_portfolio("FORMAL_RFP",replace(org,roles=org.roles+(extra,),evidence=EvidenceLabel.SENSITIVITY_ASSUMPTION))


def lost_opportunity_sensitivity():
    opportunities=[opportunity(f"LOST-RFP-{n}","FORMAL_RFP",p,"LOST" if n==1 else "PLANNED_SUCCESS") for n,p in enumerate(_fixture()["arrival_periods"],1)]
    return simulate("FORMAL_RFP_ONE_LOST",opportunities)


def opportunity_cost(occupied: PortfolioResult, alternative: PortfolioResult) -> Decimal:
    """Contribution not realized under the occupied portfolio versus a feasible alternative."""
    return max(Decimal(),alternative.annualized_contribution-occupied.annualized_contribution)
