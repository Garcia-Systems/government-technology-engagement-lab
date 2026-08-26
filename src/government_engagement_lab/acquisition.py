"""Chapter 15 acquisition-work attribution and won-deal economics synthesis.

Elapsed days are retained as descriptive pipeline context and are never cost inputs.
"""
from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum

from .baseline import load_baseline
from .evidence import EvidenceLabel
from .models import EngagementMotion, FindingCode, StageOwner, WorkCategory
from .formal_rfp import assess_formal_rfp, load_formal_rfp_motion
from .pilot import assess_pilot, acquisition_stages
from .configuration import assess_configuration_first
from .small_engagement import assess_small_engagement
from .larger_contract import assess_larger_contract
from .partner import assess_partner, load_partner_motion
from .existing_path import assess_existing_path


class AcquisitionCategory(StrEnum):
    PROSPECTING="PROSPECTING"; QUALIFICATION="QUALIFICATION"; DISCOVERY="DISCOVERY"
    MEETINGS="MEETINGS"; TECHNICAL_VALIDATION="TECHNICAL_VALIDATION"
    SECURITY_APPROVAL_SUPPORT="SECURITY_APPROVAL_SUPPORT"
    ACCESSIBILITY_APPROVAL_SUPPORT="ACCESSIBILITY_APPROVAL_SUPPORT"
    PROPOSAL="PROPOSAL"; PRICING="PRICING"; PROCUREMENT_SUPPORT="PROCUREMENT_SUPPORT"
    CONTRACT_COORDINATION="CONTRACT_COORDINATION"
    IMPLEMENTATION_PLANNING="IMPLEMENTATION_PLANNING"; PARTNER_COORDINATION="PARTNER_COORDINATION"


@dataclass(frozen=True)
class AcquisitionWorkItem:
    identifier: str
    category: AcquisitionCategory
    engagement_motion: EngagementMotion
    seller_owned_hours: int
    partner_owned_hours: int
    customer_hours: int
    seller_cost_rate: Decimal
    evidence: EvidenceLabel
    source_reference: str
    @property
    def seller_cost(self) -> Decimal:
        return Decimal(self.seller_owned_hours) * self.seller_cost_rate


@dataclass(frozen=True)
class AcquisitionEconomics:
    motion: str; work_items: tuple[AcquisitionWorkItem,...]
    implementation_revenue: Decimal; customer_contract_value: Decimal
    customer_value_addressed: Decimal; customer_cost: Decimal
    engineering_hours: int; delivery_labor_cost: Decimal; other_direct_costs: Decimal
    elapsed_days: int; minimum_contribution: Decimal
    evidence: EvidenceLabel = EvidenceLabel.OBSERVED_LAB_RESULT
    @property
    def seller_acquisition_hours(self): return sum(x.seller_owned_hours for x in self.work_items)
    @property
    def partner_acquisition_hours(self): return sum(x.partner_owned_hours for x in self.work_items)
    @property
    def customer_acquisition_hours(self): return sum(x.customer_hours for x in self.work_items)
    @property
    def total_customer_acquisition_work(self): return self.seller_acquisition_hours+self.partner_acquisition_hours+self.customer_acquisition_hours
    @property
    def acquisition_labor_cost(self): return sum((x.seller_cost for x in self.work_items),Decimal())
    @property
    def delivery_contribution(self): return self.implementation_revenue-self.delivery_labor_cost
    @property
    def acquisition_adjusted_contribution(self): return self.delivery_contribution-self.acquisition_labor_cost-self.other_direct_costs
    @property
    def acquisition_cost_per_revenue(self): return self.acquisition_labor_cost/self.implementation_revenue
    @property
    def acquisition_hours_per_10000_revenue(self): return Decimal(self.seller_acquisition_hours)/(self.implementation_revenue/Decimal(10000))
    @property
    def acquisition_cost_per_value(self): return self.acquisition_labor_cost/self.customer_value_addressed
    @property
    def acquisition_hours_per_engineering_hour(self): return Decimal(self.seller_acquisition_hours)/Decimal(self.engineering_hours)
    @property
    def acquisition_cost_per_delivery_cost(self): return self.acquisition_labor_cost/self.delivery_labor_cost
    @property
    def sustainability(self): return "SUSTAINABLE" if self.acquisition_adjusted_contribution>=self.minimum_contribution else ("FRAGILE" if self.acquisition_adjusted_contribution>=0 else "UNSUSTAINABLE")
    def by_category(self):
        return {c:(sum(x.seller_owned_hours for x in self.work_items if x.category is c),sum((x.seller_cost for x in self.work_items if x.category is c),Decimal())) for c in AcquisitionCategory if any(x.category is c for x in self.work_items)}


@dataclass(frozen=True)
class LostDealSensitivity:
    motion: str; implementation_revenue: Decimal; acquisition_cost_retained: Decimal
    opportunity_contribution: Decimal
    evidence: EvidenceLabel=EvidenceLabel.SENSITIVITY_ASSUMPTION

_STAGE_CATEGORY={
 "OPPORTUNITY_DISCOVERY":AcquisitionCategory.PROSPECTING,"SPONSOR_IDENTIFICATION":AcquisitionCategory.PROSPECTING,
 "GO_NO_GO":AcquisitionCategory.QUALIFICATION,"REQUIREMENTS_INTERPRETATION":AcquisitionCategory.DISCOVERY,"BOUNDED_DISCOVERY":AcquisitionCategory.DISCOVERY,
 "CLARIFICATIONS_MEETINGS":AcquisitionCategory.MEETINGS,"SOLUTION_DESIGN":AcquisitionCategory.TECHNICAL_VALIDATION,"TECHNICAL_RESPONSE":AcquisitionCategory.TECHNICAL_VALIDATION,"TECHNICAL_VALIDATION":AcquisitionCategory.TECHNICAL_VALIDATION,
 "SECURITY_ACCESS_RESPONSE":AcquisitionCategory.SECURITY_APPROVAL_SUPPORT,"SECURITY_ACCESS_REVIEW":AcquisitionCategory.SECURITY_APPROVAL_SUPPORT,
 "ACCESSIBILITY_RESPONSE":AcquisitionCategory.ACCESSIBILITY_APPROVAL_SUPPORT,
 "PROPOSAL_ASSEMBLY":AcquisitionCategory.PROPOSAL,"PILOT_PROPOSAL":AcquisitionCategory.PROPOSAL,"PILOT_SCOPE_AGREEMENT":AcquisitionCategory.PROPOSAL,
 "PRICING":AcquisitionCategory.PRICING,"SOLICITATION_REVIEW":AcquisitionCategory.PROCUREMENT_SUPPORT,"SUBMISSION":AcquisitionCategory.PROCUREMENT_SUPPORT,"EVALUATION_WAIT":AcquisitionCategory.PROCUREMENT_SUPPORT,"INTENT_SELECTION":AcquisitionCategory.PROCUREMENT_SUPPORT,"PROCUREMENT_COORDINATION":AcquisitionCategory.PROCUREMENT_SUPPORT,"PURCHASING_PATH":AcquisitionCategory.PROCUREMENT_SUPPORT,
 "CONTRACT_REVIEW":AcquisitionCategory.CONTRACT_COORDINATION,"AGREEMENT_AUTHORIZATION":AcquisitionCategory.CONTRACT_COORDINATION,
 "IMPLEMENTATION_PLANNING":AcquisitionCategory.IMPLEMENTATION_PLANNING,"AUTHORIZATION":AcquisitionCategory.IMPLEMENTATION_PLANNING,
}

def _category(identifier, name=""):
    if identifier in _STAGE_CATEGORY:return _STAGE_CATEGORY[identifier]
    text=(identifier+" "+name).upper()
    if "SECUR" in text:return AcquisitionCategory.SECURITY_APPROVAL_SUPPORT
    if "ACCESSIB" in text:return AcquisitionCategory.ACCESSIBILITY_APPROVAL_SUPPORT
    if "PROCURE" in text:return AcquisitionCategory.PROCUREMENT_SUPPORT
    if "CONTRACT" in text:return AcquisitionCategory.CONTRACT_COORDINATION
    if "PRICE" in text or "PRIC" in text:return AcquisitionCategory.PRICING
    if "DISCOV" in text or "SCOPE" in text:return AcquisitionCategory.DISCOVERY
    if "IMPLEMENT" in text or "PLANN" in text:return AcquisitionCategory.IMPLEMENTATION_PLANNING
    return AcquisitionCategory.TECHNICAL_VALIDATION

def _stage_items(motion, stages):
    rates={x.category:x.hourly_cost for x in load_formal_rfp_motion().labor_rates}
    return tuple(AcquisitionWorkItem(f"{motion.value}:{s.identifier}",_category(s.identifier,s.display_name),motion,s.effort_hours,0,0,rates[s.responsible_category],s.evidence,f"journey:{s.identifier}") for s in stages)

def acquisition_reports() -> tuple[AcquisitionEconomics,...]:
    base=load_baseline(); value=base.burden.annual_recoverable_value; formal=assess_formal_rfp(); rates={x.category:x.hourly_cost for x in formal.motion.labor_rates}; out=[]
    def add(name,items,revenue,contract,value_addressed,cost,eng,delivery,other,days,minimum): out.append(AcquisitionEconomics(name,items,revenue,contract,value_addressed,cost,eng,delivery,other,days,minimum))
    s=formal.seller_economics; add("FORMAL_RFP",_stage_items(EngagementMotion.FORMAL_RFP,formal.motion.journey.stages),s.implementation_revenue,s.implementation_revenue+formal.motion.annual_support,value,formal.customer_economics.first_year_cost,formal.motion.engineering_hours,s.delivery_labor_cost,s.other_direct_costs,formal.motion.journey.total_elapsed_days,formal.motion.minimum_contribution)
    p=assess_pilot(); s=p.economics.seller; add("COOPERATIVE_PAID_PILOT",_stage_items(EngagementMotion.COOPERATIVE_PAID_PILOT,acquisition_stages(p.motion)),s.implementation_revenue,s.implementation_revenue+p.motion.pilot_period_support,p.economics.annualized_value_potentially_affected,p.motion.pilot_price+p.motion.pilot_period_support,p.motion.engineering_hours,s.delivery_labor_cost,s.other_direct_costs,p.economics.authorization_days,p.motion.minimum_contribution)
    c=assess_configuration_first(); e=c.economics;s=e.seller; item=AcquisitionWorkItem("CONFIGURATION_FIRST:MODELED_ACQUISITION",AcquisitionCategory.DISCOVERY,EngagementMotion.CONFIGURATION_FIRST,e.acquisition_hours,0,0,rates[WorkCategory.SALES],c.assumption_evidence,"chapter-7:acquisition_hours")
    add("CONFIGURATION_FIRST",(item,),e.implementation_price,e.first_year_cost,e.value_addressed,e.first_year_cost,e.engineering_hours,s.delivery_labor_cost,s.other_direct_costs,e.elapsed_days,formal.motion.minimum_contribution)
    sm=assess_small_engagement(); e=sm.engagement;s=sm.seller;add("SMALL_DEPARTMENTAL",_stage_items(EngagementMotion.SMALL_DEPARTMENTAL,e.acquisition_stages),e.implementation_price,sm.customer.first_year_cost,sm.customer.annual_value_addressed,sm.customer.first_year_cost,e.engineering_hours,s.delivery_labor_cost,s.other_direct_costs,e.journey.total_elapsed_days,e.minimum_contribution)
    lg=assess_larger_contract();e=lg.engagement;s=lg.seller; works=list(e.acquisition_floor)+[x for cpt in e.components for x in cpt.acquisition]
    items=tuple(AcquisitionWorkItem(f"LARGER_CONTRACT:{i}",_category(str(i),x.name),EngagementMotion.LARGER_CONTRACT,x.hours,0,0,rates[x.category],x.evidence if hasattr(x,'evidence') else e.evidence,f"chapter-9:{x.name}") for i,x in enumerate(works))
    add("JUSTIFIED_LARGER_CONTRACT",items,e.implementation_price,lg.first_year_cost,e.value_addressed,lg.first_year_cost,e.engineering_hours,s.delivery_labor_cost,s.other_direct_costs,e.cycle_days,e.minimum_contribution)
    pa=assess_partner();pm=load_partner_motion();pe=pa.economics; formal_stages={x.identifier:x for x in formal.motion.journey.stages};items=[]
    for own in pm.stage_ownership:
      src=formal_stages[own.stage_id]; residual=max(0,src.effort_hours-own.seller_hours); customer=residual if own.primary_owner is StageOwner.CUSTOMER else 0; partner=0 if own.primary_owner is StageOwner.CUSTOMER else residual
      items.append(AcquisitionWorkItem(f"PARTNER_LED:{own.stage_id}",_category(own.stage_id,src.display_name),EngagementMotion.PARTNER_LED,own.seller_hours,partner,customer,rates[src.responsible_category],own.evidence,f"chapter-10:{own.stage_id}"))
    add("PARTNER_LED",tuple(items),pe.seller_engagement_revenue,pe.customer_contract_value,pe.customer_value_addressed,pe.customer_contract_value,pe.engineering_hours,pe.seller_delivery_cost,pe.retained_project_management_cost+pe.seller_support_cost,pe.cycle_days,formal.motion.minimum_contribution)
    ex=assess_existing_path();e=ex.economics;s=e.seller;m=ex.motion;add("EXISTING_PURCHASING_PATH",_stage_items(EngagementMotion.EXISTING_PURCHASING_PATH,m.journey.stages),s.implementation_revenue,s.implementation_revenue+m.annual_support,value,ex.customer_economics.first_year_cost,m.engineering_hours,s.delivery_labor_cost,s.other_direct_costs,e.elapsed_days,m.minimum_contribution)
    return tuple(out)

def acquisition_report(motion="FORMAL_RFP"):
    return next(x for x in acquisition_reports() if x.motion==motion)

def focused_scenarios(): return tuple(acquisition_report(x) for x in ("FORMAL_RFP","COOPERATIVE_PAID_PILOT","PARTNER_LED","EXISTING_PURCHASING_PATH"))
def lost_deal_sensitivity(motion="FORMAL_RFP"):
    x=acquisition_report(motion); return LostDealSensitivity(motion,Decimal(),x.acquisition_labor_cost,-x.acquisition_labor_cost)
def acquisition_reason_trace():
    x=acquisition_report(); return {FindingCode.HIGH_SOLUTIONS_EFFORT:tuple(i.source_reference for i in x.work_items if i.seller_cost_rate==Decimal("125.00")),FindingCode.PROCUREMENT_DIFFICULTY:tuple(i.source_reference for i in x.work_items if i.category is AcquisitionCategory.PROCUREMENT_SUPPORT)}
