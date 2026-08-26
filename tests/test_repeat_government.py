from dataclasses import asdict

from government_engagement_lab.repeat_government import (ReuseScope,
    assess_repeat_government, load_repeat_government_fixture,
    repeat_government_scenarios, three_level_comparison)
from government_engagement_lab.repeatability import ReuseDimension, ReuseState

def test_second_government_fixture_is_explicitly_fictional_and_distinct():
    p,_,raw=load_repeat_government_fixture()
    assert p.fictional and p.incumbent_fictional and "wholly fictional" in p.fiction_notice
    assert p.name == "Blue Ridge County" and p.department_id == "BRC_DEVELOPMENT_SERVICES"
    assert not ({"James City County","York County","Williamsburg","Newport News"} & {p.name})
    assert p.incumbent == "MunicipalWorks Development Platform"
    assert p.workflow != ("Application","Review","Correction","Resubmission","Decision","Reporting")
    assert raw["incumbent"]["missing_capabilities"]

def test_customer_conditions_explicitly_reset():
    a=assess_repeat_government(); p=a.profile; by={x.identifier:x for x in a.artifacts}
    assert a.scope is ReuseScope.CROSS_CUSTOMER and p.access_mode == "READ_ONLY_API"
    assert p.purchasing_motion == "FORMAL_RFP_REQUIRED_BY_MODEL"
    assert len(p.stakeholders) == 6 and len(p.governance_requirements) == 5
    assert by["BUYER_ACCESS"].state is ReuseState.REBUILD
    assert by["PURCHASING_PATH"].state is ReuseState.REBUILD
    assert by["PROCUREMENT_ARTIFACT"].state is ReuseState.ADAPT
    assert by["SECURITY_DOCUMENT"].state is ReuseState.ADAPT
    assert by["SECURITY_APPROVAL"].state is ReuseState.REBUILD
    assert by["ACCESSIBILITY_HARNESS"].state is ReuseState.REUSE_AS_IS
    assert by["ACCESSIBILITY_ACCEPTANCE"].state is ReuseState.REBUILD

def test_reuse_effort_and_economics_reconcile():
    a=assess_repeat_government()
    assert {x.dimension for x in a.artifacts} == set(ReuseDimension)
    assert a.engineering_greenfield_hours == 144
    assert a.engineering_hours == 81 and a.engineering_saved_hours == 63
    assert a.discovery_hours == 26
    assert a.acquisition_hours == sum(v for _,v in a.acquisition_by_category) == 104
    assert a.governance_hours == 36 and a.support_hours == 18
    assert a.customer_value == 13000
    assert all(x.adaptation_effort > 0 for x in a.artifacts if x.state is ReuseState.ADAPT)
    by={x.identifier:x for x in a.artifacts}
    assert by["ACTUAL_DISCOVERY"].state is ReuseState.REBUILD
    assert by["INTERVIEW_TEMPLATE"].hours_saved == 8
    assert by["SUPPORT_PLATFORM"].hours_saved == 17 and by["SUPPORT_INTEGRATION"].adaptation_effort == 13

def test_three_levels_and_scenarios_are_independent():
    before=asdict(assess_repeat_government())
    levels=three_level_comparison(); assert [x["level"] for x in levels] == ["FIRST DEPARTMENT","SAME-GOVERNMENT SECOND DEPARTMENT","NEW GOVERNMENT"]
    base,hard,friendly,technical=repeat_government_scenarios()
    assert hard.engineering_hours == base.engineering_hours and hard.acquisition_hours > base.acquisition_hours
    assert friendly.acquisition_hours < base.acquisition_hours and friendly.verdict == "REPEATABLE PROJECT"
    assert technical.engineering_hours > base.engineering_hours and technical.acquisition_hours < base.acquisition_hours
    assert asdict(assess_repeat_government()) == before

def test_no_score_product_or_high_engineering_shortcut_and_no_chapter_19():
    a=assess_repeat_government()
    assert a.verdict == "INVESTIGATE"  # 63 saved engineering hours do not override 104 acquisition hours.
    assert not hasattr(a,"reuse_score") and not hasattr(a,"product_classification")
    import government_engagement_lab.cli as cli
    assert not hasattr(cli,"show_engagement_motion_economics")
