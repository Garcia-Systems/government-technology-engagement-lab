"""Chapter 18: repeatability across wholly fictional governments."""
from dataclasses import dataclass, replace
from decimal import Decimal
from enum import StrEnum

from .baseline import _fixture
from .evidence import EvidenceLabel, parse_evidence_label
from .repeatability import ReuseArtifact, ReuseDimension, ReuseState, summarize_dimensions, assess_repeat_department, department_one_reference

class ReuseScope(StrEnum):
    WITHIN_CUSTOMER = "WITHIN_CUSTOMER"
    CROSS_CUSTOMER = "CROSS_CUSTOMER"

@dataclass(frozen=True)
class GovernmentProfile:
    identifier: str; name: str; fictional: bool; department_id: str; department_name: str
    workflow: tuple[str, ...]; incumbent: str; incumbent_fictional: bool; incumbent_capabilities: tuple[str, ...]
    access_mode: str; purchasing_motion: str; purchasing_path: str; stakeholders: tuple[tuple[str,str], ...]
    governance_requirements: tuple[str, ...]; fiction_notice: str

@dataclass(frozen=True)
class CrossGovernmentAssessment:
    key: str; name: str; scope: ReuseScope; profile: GovernmentProfile
    artifacts: tuple[ReuseArtifact, ...]; summaries: tuple; acquisition_by_category: tuple[tuple[str,int], ...]
    engineering_greenfield_hours: int; engineering_hours: int; discovery_hours: int; acquisition_hours: int
    governance_hours: int; support_hours: int; elapsed_days: int; customer_value: Decimal
    seller_contribution: Decimal; verdict: str; changed_assumptions: tuple[str, ...]
    evidence: EvidenceLabel = EvidenceLabel.OBSERVED_LAB_RESULT

    @property
    def engineering_saved_hours(self): return self.engineering_greenfield_hours-self.engineering_hours

def load_repeat_government_fixture():
    raw=_fixture("repeat_government.json"); g,d,i=raw["government"],raw["department"],raw["incumbent"]
    profile=GovernmentProfile(g["identifier"],g["name"],g["fictional"],d["identifier"],d["name"],tuple(d["workflow"]),i["name"],i["fictional"],tuple(i["capabilities"]),raw["access"]["mode"],raw["purchasing"]["motion"],raw["purchasing"]["path"],tuple((x["id"],x["authority"]) for x in raw["stakeholders"]),tuple(raw["governance"]["requirements"]),raw["fiction_notice"])
    ev=parse_evidence_label(raw["evidence"])
    artifacts=tuple(ReuseArtifact(x[0],ReuseDimension(x[1]),x[2],"JRC_PERMITTING",d["identifier"],ReuseState(x[3]),x[4],x[5],ev,x[6]) for x in raw["artifacts"])
    return profile,artifacts,raw

def _assess(key="DIFFERENT_GOVERNMENT_BASELINE",name="Different government baseline",*, eng=0, acq=0, gov=0, support=0, days=0, artifact_changes=None, changes=()):
    p,arts,raw=load_repeat_government_fixture()
    if artifact_changes:
        arts=tuple(replace(a, adaptation_effort=artifact_changes.get(a.identifier,a.adaptation_effort), state=(ReuseState.REBUILD if artifact_changes.get(a.identifier,a.adaptation_effort)==a.first_department_effort else a.state)) for a in arts)
    sums=summarize_dimensions(arts); req={x.dimension:x.hours_required for x in sums}
    engineering=sum(req[x] for x in (ReuseDimension.ENGINEERING_REUSE,ReuseDimension.CONFIGURATION_REUSE,ReuseDimension.TEST_REUSE))+eng
    discovery=req[ReuseDimension.DISCOVERY_REUSE]
    acquisition_items=tuple(raw["acquisition"].items()); acquisition=sum(v for _,v in acquisition_items)+acq
    governance=req[ReuseDimension.SECURITY_GOVERNANCE_REUSE]+gov; support_hours=req[ReuseDimension.SUPPORT_REUSE]+support
    e=raw["economics"]; price,support_revenue,value=map(Decimal,(e["implementation_price"],e["annual_support_revenue"],e["annual_recoverable_value"]))
    contribution=price+support_revenue-Decimal(engineering+discovery)*Decimal(e["engineering_rate"])-Decimal(acquisition+governance)*Decimal(e["engagement_rate"])-Decimal(support_hours)*Decimal(e["support_rate"])-Decimal(e["other_direct_cost"])
    green=sum(x.greenfield_hours for x in sums if x.dimension in (ReuseDimension.ENGINEERING_REUSE,ReuseDimension.CONFIGURATION_REUSE,ReuseDimension.TEST_REUSE))
    # Engineering alone is intentionally insufficient: commercial and approval work must be manageable.
    verdict="REPEATABLE PROJECT" if contribution>=Decimal("10000") and acquisition<=90 and governance<=40 else "INVESTIGATE"
    return CrossGovernmentAssessment(key,name,ReuseScope.CROSS_CUSTOMER,p,arts,sums,acquisition_items,green,engineering,discovery,acquisition,governance,support_hours,e["elapsed_days"]+days,value-(price+support_revenue),contribution,verdict,tuple(changes))

def assess_repeat_government(): return _assess()

def repeat_government_scenarios():
    return (assess_repeat_government(),
      _assess("HARD_COMMERCIAL_RESET","Same technical pattern, hard commercial reset",acq=34,gov=6,days=55,changes=("Buyer access, sponsor, purchasing path, and contract setup reset.",)),
      _assess("FRIENDLY_SECOND_GOVERNMENT","Commercially friendly second government",acq=-34,gov=-8,days=-55,changes=("Strong sponsor and direct small-project path reduce, but do not eliminate, new-customer work.",)),
      _assess("TECHNICAL_VARIATION","Technical variation breaks reuse",eng=34,acq=-24,days=10,artifact_changes={"REPORT_SHELL":15,"NORMALIZATION":14,"STATUS_MAPPING":18},changes=("Good access and purchasing coexist with a divergent data and status model.",)))

def three_level_comparison():
    d1=department_one_reference(); d2=assess_repeat_department(); g=assess_repeat_government()
    return ({"level":"FIRST DEPARTMENT","engineering_hours":d1["engineering_hours"],"acquisition_hours":d1["acquisition_hours"],"governance_hours":d1["governance_hours"],"support_hours":d1["support_hours"],"elapsed_days":d1["elapsed_days"],"contribution":Decimal(d1["contribution"])},
      {"level":"SAME-GOVERNMENT SECOND DEPARTMENT","engineering_hours":d2.engineering_hours,"acquisition_hours":d2.acquisition_hours,"governance_hours":d2.governance_hours,"support_hours":d2.support_hours,"elapsed_days":d2.elapsed_days,"contribution":d2.economics.marginal_contribution},
      {"level":"NEW GOVERNMENT","engineering_hours":g.engineering_hours,"acquisition_hours":g.acquisition_hours,"governance_hours":g.governance_hours,"support_hours":g.support_hours,"elapsed_days":g.elapsed_days,"contribution":g.seller_contribution})
