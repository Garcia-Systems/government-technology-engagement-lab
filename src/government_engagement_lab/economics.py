"""Transparent calculations over fictional modeled assumptions."""

from dataclasses import dataclass
from decimal import Decimal

from .evidence import EvidenceLabel
from .models import BaselineCase


@dataclass(frozen=True)
class CustomerEconomicsResult:
    first_year_cost: Decimal
    first_year_net_recoverable_value: Decimal
    implementation_only_payback_months: Decimal
    evidence: EvidenceLabel = EvidenceLabel.OBSERVED_LAB_RESULT


def calculate_customer_economics(case: BaselineCase) -> CustomerEconomicsResult:
    """Calculate customer measures without inventing seller labor rates."""
    first_year_cost = case.economics.implementation_price + case.economics.annual_support
    return CustomerEconomicsResult(
        first_year_cost=first_year_cost,
        first_year_net_recoverable_value=case.burden.annual_recoverable_value - first_year_cost,
        implementation_only_payback_months=(
            case.economics.implementation_price / case.burden.annual_recoverable_value * Decimal(12)
        ),
    )
