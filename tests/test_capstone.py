"""Chapter 20 final synthesis, precedence, and traceability."""
from dataclasses import replace
from government_engagement_lab.capstone import (FICTION_NOTICE, ORIGINAL_HYPOTHESIS,
 FinalVerdict, FalsificationStatus, VerdictInputs, assess_capstone, determine_final_verdict,
 evidence_inventory, VERDICT_SEMANTICS)
from government_engagement_lab.evidence import EvidenceLabel
from government_engagement_lab.models import GateStatus
from government_engagement_lab.formal_rfp import assess_formal_rfp


def decide(**kw): return determine_final_verdict(replace(VerdictInputs(),**kw))[0]

def test_assessment_loads_every_chapter_and_preserves_baseline():
 a=assess_capstone()
 assert a.evidence_sources==tuple(f"CHAPTER_{n}" for n in range(21))
 assert a.original_hypothesis==ORIGINAL_HYPOTHESIS=="LOCAL GOVERNMENT → POOR TARGET CUSTOMER"
 assert a.baseline_motion_result=="FORMAL RFP → POOR TARGET CUSTOMER" and a.baseline_answer=="YES"
 r=assess_formal_rfp()
 assert r.project_viability is GateStatus.PASS and r.target_viability is GateStatus.FAIL

def test_vocabulary_and_semantics_are_complete():
 assert {x.value for x in FinalVerdict}=={"NO DEAL","CONFIGURE / BUY","NARROW CUSTOM EDGE","PARTNER-LED TARGET","PILOT-FIRST TARGET","REPEATABLE PROJECT","PROMISING — VALIDATE IN DISCOVERY","POOR TARGET CUSTOMER","INVESTIGATE"}
 assert set(VERDICT_SEMANTICS)==set(FinalVerdict)

def test_precedence_is_deterministic_and_foundation_dominates():
 i=VerdictInputs(foundational_pass=False,responsible_fallback=False,native_adequate=True,partner_viable=True)
 assert determine_final_verdict(i)==determine_final_verdict(i)
 assert determine_final_verdict(i)[0] is FinalVerdict.NO_DEAL

def test_native_precedes_custom_and_motion_results():
 assert decide(native_adequate=True,residual_material=False,partner_viable=True) is FinalVerdict.CONFIGURE_BUY
 assert decide(native_adequate=True,residual_material=True,residual_bounded=True,residual_access_supported=True) is FinalVerdict.NARROW_CUSTOM_EDGE
 assert decide(native_adequate=True,residual_material=True,residual_bounded=False,residual_access_supported=True) is FinalVerdict.INVESTIGATE

def test_partner_and_pilot_require_positive_evidence():
 assert decide(direct_target_pass=False,partner_viable=True,pilot_viable=True) is FinalVerdict.PARTNER_LED_TARGET
 assert decide(direct_target_pass=False,pilot_viable=True) is FinalVerdict.PILOT_FIRST_TARGET
 assert decide(direct_target_pass=False) is FinalVerdict.INVESTIGATE

def test_repeatability_is_multidimensional_not_technical_only():
 complete=dict(technical_reuse=True,delivery_reuse=True,commercial_reuse=True,support_manageable=True,multi_engagement_economics=True)
 assert decide(**complete) is FinalVerdict.REPEATABLE_PROJECT
 assert decide(technical_reuse=True) is FinalVerdict.INVESTIGATE

def test_target_failure_is_not_project_failure():
 assert decide(all_credible_motions_fail=True) is FinalVerdict.POOR_TARGET_CUSTOMER
 assert decide(foundational_pass=False,responsible_fallback=False,all_credible_motions_fail=True) is FinalVerdict.NO_DEAL
 assert decide(credible_motion_pass=True) is FinalVerdict.PROMISING
 # Acquisition difficulty alone is not a foundational failure.
 assert decide(direct_target_pass=False) is not FinalVerdict.NO_DEAL

def test_mixed_investigate_and_no_product_classification():
 assert decide() is FinalVerdict.INVESTIGATE
 assert all("PRODUCT" not in v.value for v in FinalVerdict)
 assert "product" not in assess_capstone().final_verdict.value.lower()

def test_hypothesis_and_both_directions_are_derived():
 a=assess_capstone()
 assert a.falsification_status is FalsificationStatus.CONDITIONAL
 assert a.evidence_for and a.evidence_against and a.final_verdict is FinalVerdict.CONFIGURE_BUY

def test_inventory_traces_required_prior_results_and_labels():
 inv={x.identifier:x for x in evidence_inventory()}
 expectations={"FORMAL_RFP":"CHAPTER_4","PILOT":"CHAPTER_5","SCALE_PARTNER_PATH":"CHAPTER_10",
 "GOVERNANCE":"CHAPTER_12","ACCESS":"CHAPTER_13","INCUMBENT":"CHAPTER_14",
 "ACQUISITION_THROUGHPUT":"CHAPTER_15","REPEATABILITY":"CHAPTER_17"}
 for key,chapter in expectations.items(): assert chapter in inv[key].sources
 assert "CHAPTER_11" in inv["SCALE_PARTNER_PATH"].sources
 assert "CHAPTER_16" in inv["ACQUISITION_THROUGHPUT"].sources
 assert "CHAPTER_18" in inv["REPEATABILITY"].sources
 assert "CHAPTER_19" in inv["REPEATABILITY"].sources
 assert all(isinstance(x.evidence,EvidenceLabel) for x in inv.values())

def test_no_score_or_arbitrary_ranking_and_fiction_remains_explicit():
 import government_engagement_lab.capstone as module
 source=open(module.__file__).read().lower()
 assert "weighted score" not in source and "confidence_score" not in source and "motion ranking" not in source
 assert "fictional" in FICTION_NOTICE.lower() and "not evidence about real governments" in FICTION_NOTICE
