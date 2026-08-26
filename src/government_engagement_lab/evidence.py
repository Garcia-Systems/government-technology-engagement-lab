"""Evidence vocabulary shared by fixtures, calculations, and later chapters."""

from enum import StrEnum


class EvidenceLabel(StrEnum):
    MODELED_ASSUMPTION = "MODELED ASSUMPTION"
    OBSERVED_LAB_RESULT = "OBSERVED LAB RESULT"
    OBSERVED_IMPLEMENTATION_STRUCTURE = "OBSERVED IMPLEMENTATION STRUCTURE"
    SENSITIVITY_ASSUMPTION = "SENSITIVITY ASSUMPTION"
    MODELED_ALTERNATIVE_ASSUMPTION = "MODELED ALTERNATIVE ASSUMPTION"


def parse_evidence_label(value: str) -> EvidenceLabel:
    """Validate and return a label from the deliberately small vocabulary."""
    return EvidenceLabel(value)
