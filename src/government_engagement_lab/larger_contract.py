"""Chapter 9 larger-contract experiment: explicit scope, value, and price corridor."""
from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum

from .baseline import _fixture, load_baseline
from .evidence import EvidenceLabel, parse_evidence_label
from .formal_rfp import load_formal_rfp_motion
from .gates import determine_verdict
from .models import EngagementScale, GateStatus, LaborCostRate, SellerEconomics, WorkCategory
from .small_engagement import assess_small_engagement

class CorridorClass(StrEnum):
    NO_CORRIDOR="NO_CORRIDOR"; FRAGILE_CORRIDOR="FRAGILE_CORRIDOR"; VIABLE_CORRIDOR="VIABLE_CORRIDOR"

@dataclass(frozen=True)
class Work:
    name: str; hours: int

@dataclass(frozen=True)
class AcquisitionWork:
    name: str; hours: int; category: WorkCategory

@dataclass(frozen=True)
class ScopeComponent:
    identifier: str; description: str; burden_categories: tuple[str,...]
    incremental_value: Decimal; overlap: Decimal; engineering: tuple[Work,...]
    acquisition: tuple[AcquisitionWork,...]; governance_surface: tuple[str,...]
    support_surface: tuple[str,...]; evidence: EvidenceLabel

@dataclass(frozen=True)
class LargerContract:
    key: str; name: str; scale: EngagementScale; baseline_scope: str
    baseline_value: Decimal; opportunity_value: Decimal; components: tuple[ScopeComponent,...]
    baseline_engineering: tuple[Work,...]; acquisition_floor: tuple[AcquisitionWork,...]
    acquisition_factor: Decimal; implementation_price: Decimal; annual_support_revenue: Decimal
    support_hours: int; other_direct_cost: Decimal; cycle_days: int; users: int
    additional_data_sources: tuple[str,...]; labor_rates: tuple[LaborCostRate,...]
    minimum_contribution: Decimal; fragile_threshold: Decimal
    changed_assumptions: tuple[str,...]; evidence: EvidenceLabel
    @property
    def value_addressed(self): return self.baseline_value + sum((x.incremental_value-x.overlap for x in self.components),Decimal())
    @property
    def residual_value(self): return self.opportunity_value-self.value_addressed
    @property
    def engineering_hours(self): return sum(x.hours for x in self.baseline_engineering)+sum(w.hours for c in self.components for w in c.engineering)
    @property
    def acquisition_floor_hours(self): return sum(x.hours for x in self.acquisition_floor)
    @property
    def incremental_acquisition_hours(self): return sum(x.hours for c in self.components for x in c.acquisition)
    @property
    def acquisition_hours(self): return self.acquisition_floor_hours + int(Decimal(self.incremental_acquisition_hours)*self.acquisition_factor)

@dataclass(frozen=True)
class LargerAssessment:
    engagement: LargerContract; seller: SellerEconomics; support_cost: Decimal
    customer_price_ceiling: Decimal; seller_price_floor: Decimal; viable_price_corridor: Decimal
    corridor_class: CorridorClass; first_year_cost: Decimal; net_customer_value: Decimal
    payback_months: Decimal; acquisition_cost_percent_revenue: Decimal
    acquisition_hours_per_10000_revenue: Decimal; project_viability: GateStatus
    target_viability: GateStatus; verdict: str

def _work(x): return Work(x[0],x[1])
def _acq(x): return AcquisitionWork(x[0],x[1],WorkCategory(x[2]))
def _component(x,evidence):
    return ScopeComponent(x["id"],x["description"],tuple(x["burden_categories"]),Decimal(x["incremental_value"]),Decimal(x["overlap"]),tuple(_work(w) for w in x["engineering"]),tuple(_acq(w) for w in x["acquisition"]),tuple(x["governance"]),tuple(x["support"]),evidence)

def load_larger_contract_scenarios():
    raw=_fixture("larger_contract.json"); base=raw["scenarios"][0]; rates=load_formal_rfp_motion().labor_rates; out=[]
    for item in raw["scenarios"]:
        merged=base|item; evidence=parse_evidence_label(item["evidence"])
        components=tuple(_component(x,evidence) for x in merged["components"])
        ids=[x.identifier for x in components]
        if len(ids)!=len(set(ids)): raise ValueError("scope component identifiers must be unique")
        e=LargerContract(item["key"],item["name"],EngagementScale.JUSTIFIED_LARGER,merged["baseline_scope"],Decimal(raw["baseline_value"]),Decimal(raw["opportunity_value"]),components,tuple(_work(x) for x in merged["baseline_engineering"]),tuple(_acq(x) for x in merged.get("acquisition_floor",raw["acquisition_floor"])),Decimal(merged.get("acquisition_factor","1")),Decimal(merged["price"]),Decimal(merged["support_revenue"]),merged["support_hours"],Decimal(merged["other_direct_cost"]),merged["cycle_days"],merged["users"],tuple(merged["additional_data_sources"]),rates,Decimal(raw["minimum_contribution"]),Decimal(raw["fragile_corridor_threshold"]),tuple(item.get("changed_assumptions",())),evidence)
        if e.value_addressed>e.opportunity_value: raise ValueError("scope double counts modeled opportunity value")
        out.append(e)
    return tuple(out)

def load_larger_contract(): return load_larger_contract_scenarios()[0]

def assess_larger_contract(e=None):
    e=e or load_larger_contract(); rates={x.category:x.hourly_cost for x in e.labor_rates}
    delivery=Decimal(e.engineering_hours)*rates[WorkCategory.ENGINEERING]
    floor_cost=sum((Decimal(x.hours)*rates[x.category] for x in e.acquisition_floor),Decimal())
    incremental_cost=sum((Decimal(x.hours)*e.acquisition_factor*rates[x.category] for c in e.components for x in c.acquisition),Decimal())
    acquisition=floor_cost+incremental_cost; contribution=e.implementation_price-delivery-acquisition-e.other_direct_cost
    seller=SellerEconomics(e.implementation_price,delivery,acquisition,e.other_direct_cost,contribution,contribution/e.implementation_price,EvidenceLabel.OBSERVED_LAB_RESULT)
    support_cost=Decimal(e.support_hours)*rates[WorkCategory.ENGINEERING]
    ceiling=e.value_addressed-e.annual_support_revenue
    floor=delivery+acquisition+e.other_direct_cost+e.minimum_contribution
    corridor=ceiling-floor
    classification=CorridorClass.NO_CORRIDOR if corridor<0 else (CorridorClass.FRAGILE_CORRIDOR if corridor<e.fragile_threshold else CorridorClass.VIABLE_CORRIDOR)
    first=e.implementation_price+e.annual_support_revenue; net=e.value_addressed-first
    project=GateStatus.PASS if net>=0 and e.annual_support_revenue>=support_cost else GateStatus.FAIL
    target=GateStatus.PASS if contribution>=e.minimum_contribution and corridor>=0 else GateStatus.FAIL
    return LargerAssessment(e,seller,support_cost,ceiling,floor,corridor,classification,first,net,e.implementation_price/e.value_addressed*12,acquisition/e.implementation_price,Decimal(e.acquisition_hours)/(e.implementation_price/Decimal(10000)),project,target,determine_verdict(project,target))

def assess_larger_contract_scenarios(): return tuple(assess_larger_contract(x) for x in load_larger_contract_scenarios())

def contract_size_comparison(): return (assess_small_engagement(),)+assess_larger_contract_scenarios()
