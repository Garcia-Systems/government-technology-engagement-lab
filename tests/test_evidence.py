import pytest

from government_engagement_lab.baseline import load_baseline, load_scenarios
from government_engagement_lab.evidence import EvidenceLabel, parse_evidence_label


def test_evidence_vocabulary_is_exact_and_invalid_labels_fail() -> None:
    assert {label.value for label in EvidenceLabel} == {
        "MODELED ASSUMPTION", "OBSERVED LAB RESULT", "OBSERVED IMPLEMENTATION STRUCTURE",
        "SENSITIVITY ASSUMPTION", "MODELED ALTERNATIVE ASSUMPTION",
    }
    with pytest.raises(ValueError):
        parse_evidence_label("REAL GOVERNMENT EVIDENCE")


def test_fixture_values_and_historical_outcomes_are_modeled_assumptions() -> None:
    assert load_baseline().evidence is EvidenceLabel.MODELED_ASSUMPTION
    assert all(item.evidence is EvidenceLabel.MODELED_ASSUMPTION for item in load_scenarios())
