from decimal import Decimal

import pytest

from government_engagement_lab.baseline import load_baseline
from government_engagement_lab.economics import calculate_customer_economics
from government_engagement_lab.evidence import EvidenceLabel


def test_baseline_economic_inputs_and_results() -> None:
    case = load_baseline()
    assert case.burden.annual_current_state == Decimal("201232.00")
    assert case.burden.annual_recoverable_value == Decimal("104002.80")
    assert case.economics.implementation_price == Decimal("78000.00")
    assert case.economics.annual_support == Decimal("24000.00")

    result = calculate_customer_economics(case)
    assert result.first_year_cost == Decimal("102000.00")
    assert result.first_year_net_recoverable_value == Decimal("2002.80")
    assert float(result.implementation_only_payback_months) == pytest.approx(8.9997577)
    assert result.evidence is EvidenceLabel.OBSERVED_LAB_RESULT
