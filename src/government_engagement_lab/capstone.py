"""Chapter 20: deterministic synthesis of Chapters 0--19.

This module adds no motion assumptions or score.  It applies ordered structural
rules to the normalized Chapter 19 rows and retains their evidence labels.
"""
from dataclasses import dataclass
from enum import StrEnum

from .evidence import EvidenceLabel
from .models import GateStatus
from .motion_economics import MotionComparison, motion_comparisons
from .repeat_government import assess_repeat_government
from .repeatability import assess_repeat_department
from .formal_rfp import assess_formal_rfp


FICTION_NOTICE = ("Wholly fictional educational laboratory. Results are deterministic consequences "
                  "of modeled assumptions, not evidence about real governments.")
ORIGINAL_HYPOTHESIS = "LOCAL GOVERNMENT → POOR TARGET CUSTOMER"


class FinalVerdict(StrEnum):
    NO_DEAL="NO DEAL"; CONFIGURE_BUY="BUY / CONFIGURE"; NARROW_CUSTOM_EDGE="NARROW CUSTOM EDGE"
    PARTNER_LED_TARGET="PARTNER-LED TARGET"; PILOT_FIRST_TARGET="PILOT-FIRST TARGET"
    REPEATABLE_PROJECT="REPEATABLE PROJECT"
    PROMISING="PROMISING — VALIDATE IN DISCOVERY"; POOR_TARGET_CUSTOMER="POOR TARGET CUSTOMER"
    INVESTIGATE="INVESTIGATE"


class FalsificationStatus(StrEnum):
    CONFIRMED="CONFIRMED"; WEAKENED="WEAKENED"; FALSIFIED="FALSIFIED"; CONDITIONAL="CONDITIONAL"


VERDICT_SEMANTICS = {
 FinalVerdict.NO_DEAL:"A foundational project gate fails and no responsible fallback is viable.",
 FinalVerdict.CONFIGURE_BUY:"An adequate supported native/incumbent path leaves no material custom residual.",
 FinalVerdict.NARROW_CUSTOM_EDGE:"An adequate supported path leaves a bounded, material, supportable custom residual.",
 FinalVerdict.PARTNER_LED_TARGET:"Direct acquisition fails but a sustainable, accessible partner motion works.",
 FinalVerdict.PILOT_FIRST_TARGET:"Only a bounded paid, sponsor-dependent entry is established; rollout is unproven.",
 FinalVerdict.REPEATABLE_PROJECT:"Technical, delivery, commercial-artifact and support reuse work across engagements; this is not a product.",
 FinalVerdict.PROMISING:"Project and a credible motion pass, subject to real discovery validation.",
 FinalVerdict.POOR_TARGET_CUSTOMER:"The project passes but credible acquisition motions remain sustainably unattractive.",
 FinalVerdict.INVESTIGATE:"Mixed conditional evidence has no stronger structural rule.",
}


@dataclass(frozen=True)
class VerdictInputs:
    foundational_pass: bool = True; responsible_fallback: bool = True
    native_adequate: bool = False; customer_economics_pass: bool = True
    residual_material: bool = False; residual_bounded: bool = False; residual_access_supported: bool = False
    delivery_support_pass: bool = True; direct_target_pass: bool = False
    partner_viable: bool = False; pilot_viable: bool = False
    technical_reuse: bool = False; delivery_reuse: bool = False
    commercial_reuse: bool = False; support_manageable: bool = False; multi_engagement_economics: bool = False
    credible_motion_pass: bool = False; all_credible_motions_fail: bool = False


def determine_final_verdict(i: VerdictInputs) -> tuple[FinalVerdict, str]:
    """Apply explicit precedence; the first matching rule wins."""
    if (not i.foundational_pass and not i.responsible_fallback) or not i.customer_economics_pass or not i.delivery_support_pass:
        return FinalVerdict.NO_DEAL, "1 FOUNDATIONAL FEASIBILITY FAILURE"
    if i.native_adequate and not i.residual_material:
        return FinalVerdict.CONFIGURE_BUY, "2 ADEQUATE NATIVE / INCUMBENT SOLUTION"
    if i.native_adequate and i.residual_material and i.residual_bounded and i.residual_access_supported:
        return FinalVerdict.NARROW_CUSTOM_EDGE, "3 BOUNDED MATERIAL CUSTOM RESIDUAL"
    if not i.direct_target_pass and i.partner_viable:
        return FinalVerdict.PARTNER_LED_TARGET, "4 DIRECT FAILS; PARTNER WORKS"
    if not i.direct_target_pass and i.pilot_viable:
        return FinalVerdict.PILOT_FIRST_TARGET, "5 DIRECT FAILS; PAID PILOT WORKS"
    if all((i.technical_reuse,i.delivery_reuse,i.commercial_reuse,i.support_manageable,i.multi_engagement_economics)):
        return FinalVerdict.REPEATABLE_PROJECT, "6 MULTI-DIMENSIONAL REPEATABLE DELIVERY"
    if i.credible_motion_pass:
        return FinalVerdict.PROMISING, "7 PROJECT AND CREDIBLE TARGET MOTION PASS"
    if i.foundational_pass and i.all_credible_motions_fail:
        return FinalVerdict.POOR_TARGET_CUSTOMER, "8 PROJECT PASSES; CREDIBLE MOTIONS FAIL"
    return FinalVerdict.INVESTIGATE, "9 MIXED / CONDITIONAL EVIDENCE"


@dataclass(frozen=True)
class EvidenceFinding:
    identifier: str; finding: str; sources: tuple[str,...]; evidence: EvidenceLabel


@dataclass(frozen=True)
class GateSynthesis:
    problem: str; technical: str; customer: str; delivery: str; support: str; target: str
    within_account: str; cross_government: str


@dataclass(frozen=True)
class CapstoneAssessment:
    original_hypothesis: str; baseline_motion_result: str; baseline_answer: str
    broader_answer: str; falsification_status: FalsificationStatus
    final_verdict: FinalVerdict; evidence_posture: str; precedence_rule: str
    motions: tuple[MotionComparison,...]; gates: GateSynthesis
    evidence_for: tuple[EvidenceFinding,...]; evidence_against: tuple[EvidenceFinding,...]
    supporting_findings: tuple[str,...]; contradictory_findings: tuple[str,...]
    unresolved_conditions: tuple[str,...]; recommended_posture: tuple[str,...]
    evidence_sources: tuple[str,...]; fiction_notice: str = FICTION_NOTICE


def evidence_inventory() -> tuple[EvidenceFinding,...]:
    """A trace inventory only: values remain in the reusable prior outputs."""
    return (
      EvidenceFinding("ORIGINAL","Baseline hypothesis and non-technical rejection mechanisms.",( "CHAPTER_0","CHAPTER_1","CHAPTER_2","CHAPTER_3"),EvidenceLabel.MODELED_ASSUMPTION),
      EvidenceFinding("FORMAL_RFP","Formal RFP fails target viability while its project/customer value gates pass.",( "CHAPTER_4","CHAPTER_15","CHAPTER_16","CHAPTER_19"),EvidenceLabel.OBSERVED_LAB_RESULT),
      EvidenceFinding("PILOT","Bounded paid pilot passes modeled target viability but requires a strong sponsor.",( "CHAPTER_5","CHAPTER_15","CHAPTER_16","CHAPTER_19"),EvidenceLabel.OBSERVED_LAB_RESULT),
      EvidenceFinding("READ_ONLY_CONFIGURATION","Read-only and configuration reduce authority and custom surface while leaving residual value.",( "CHAPTER_6","CHAPTER_7","CHAPTER_12","CHAPTER_19"),EvidenceLabel.OBSERVED_LAB_RESULT),
      EvidenceFinding("SCALE_PARTNER_PATH","Contract size, partner, and existing-path experiments separate access and acquisition mechanisms.",( "CHAPTER_8","CHAPTER_9","CHAPTER_10","CHAPTER_11","CHAPTER_19"),EvidenceLabel.OBSERVED_LAB_RESULT),
      EvidenceFinding("GOVERNANCE","Legitimate delivery work is distinct from acquisition/approval work; some motions shift rather than remove it.",( "CHAPTER_12",),EvidenceLabel.OBSERVED_LAB_RESULT),
      EvidenceFinding("ACCESS","No supported access overrides favorable commercial economics and invokes responsible fallbacks.",( "CHAPTER_13",),EvidenceLabel.OBSERVED_LAB_RESULT),
      EvidenceFinding("INCUMBENT","The adequate supported incumbent alternative is selected ahead of custom ownership.",( "CHAPTER_14",),EvidenceLabel.MODELED_ALTERNATIVE_ASSUMPTION),
      EvidenceFinding("ACQUISITION_THROUGHPUT","Pre-award technical/proposal work and elapsed congestion differ from delivery cost and per-deal contribution.",( "CHAPTER_15","CHAPTER_16"),EvidenceLabel.OBSERVED_LAB_RESULT),
      EvidenceFinding("REPEATABILITY","Reuse is multi-dimensional within-account; cross-customer commercial and approval work resets.",( "CHAPTER_17","CHAPTER_18","CHAPTER_19"),EvidenceLabel.OBSERVED_LAB_RESULT),
    )


def assess_capstone() -> CapstoneAssessment:
    rows=motion_comparisons(); by={x.identifier:x for x in rows}; rfp=assess_formal_rfp()
    # Chapter 14 already applied feasibility → economics → adequacy → ownership.
    inputs=VerdictInputs(native_adequate=True, residual_material=False,
        direct_target_pass=rfp.target_viability is GateStatus.PASS,
        partner_viable=by["PARTNER_LED"].target_viability is GateStatus.PASS,
        pilot_viable=by["COOPERATIVE_PAID_PILOT"].target_viability is GateStatus.PASS,
        technical_reuse=True,delivery_reuse=True,commercial_reuse=True,support_manageable=True,
        multi_engagement_economics=assess_repeat_department().structural_interpretation=="REPEATABLE PROJECT",
        credible_motion_pass=any(x.target_viability is GateStatus.PASS for x in rows))
    verdict,rule=determine_final_verdict(inputs)
    inventory=evidence_inventory(); by_ev={x.identifier:x for x in inventory}
    evidence_for=(by_ev["FORMAL_RFP"],by_ev["ACCESS"],by_ev["REPEATABILITY"])
    evidence_against=(by_ev["PILOT"],by_ev["READ_ONLY_CONFIGURATION"],by_ev["SCALE_PARTNER_PATH"])
    unresolved=("Sponsor authority","actual purchasing path and contracting effort","actual incumbent capability and residual value",
      "supported technical access","security, accessibility, and governance requirements","actual burden, value, willingness to pay, and sales effort",
      "partner availability and acceptable ownership terms","cross-customer technical and commercial repeatability")
    posture=("DO NOT TARGET GENERIC FORMAL RFPs.","PREFER SUPPORTED INCUMBENT CONFIGURATION BEFORE CUSTOM OWNERSHIP.",
      "IF A MATERIAL RESIDUAL IS PROVEN, TEST A SPONSORED PAID, READ-ONLY BOUNDED EDGE OR A VIABLE PARTNER / EXISTING PATH.",
      "REJECT CLOSED ACCESS, UNSUPPORTED WRITES, AND ACQUISITION-UNECONOMIC SMALL CONTRACTS.")
    cross=assess_repeat_government()
    return CapstoneAssessment(ORIGINAL_HYPOTHESIS,"FORMAL RFP → POOR TARGET CUSTOMER","YES",
      "NO CATEGORY-WIDE CONCLUSION; RESULTS ARE MOTION-DEPENDENT",FalsificationStatus.CONDITIONAL,
      verdict,"STRONG WITHIN LAB; CONDITIONAL OUTSIDE IT",rule,rows,
      GateSynthesis("PASS","CONDITIONAL BY SUPPORTED ACCESS / INTERVENTION","PASS FOR SOME MOTIONS; FAIL FOR OTHERS",
       "PASS FOR BOUNDED MOTIONS; CONDITIONAL FOR BROAD CUSTOM","PASS / CONDITIONAL BY OWNERSHIP",
       "FAIL FOR FORMAL RFP; BETTER FOR PILOT / PARTNER / EXISTING PATH","REPEATABLE PROJECT",
       f"{cross.verdict}; COMMERCIAL AND APPROVAL RESET REMAINS"),evidence_for,evidence_against,
      tuple(x.finding for x in evidence_against),tuple(x.finding for x in evidence_for),unresolved,posture,
      tuple(f"CHAPTER_{n}" for n in range(21)))
