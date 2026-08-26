"""Chapter 12: inspectable governance work and economic attribution.

All controls and allocations are fictional educational assumptions.  They are not
claims about any jurisdiction, law, policy, or compliance benchmark.
"""

from dataclasses import replace
from decimal import Decimal

from .baseline import _fixture
from .evidence import EvidenceLabel, parse_evidence_label
from .models import (
    GateStatus, GovernanceCategory, GovernanceClassification, GovernanceInventory,
    GovernanceMetrics, GovernanceResponsibility, GovernanceScenario,
    GovernanceWorkItem, WorkOrigin,
)

WRITE_CAPABLE = "WRITE_CAPABLE_INTEGRATION"
READ_ONLY = "READ_ONLY_REPORTING_EDGE"
CONFIGURATION_FIRST = "CONFIGURATION_FIRST"
SELLER_BORNE = {GovernanceResponsibility.SELLER, GovernanceResponsibility.JOINT}
CUSTOMER_REVIEWERS = {
    GovernanceResponsibility.CUSTOMER_IT,
    GovernanceResponsibility.CUSTOMER_SECURITY,
    GovernanceResponsibility.CUSTOMER_ACCESSIBILITY,
    GovernanceResponsibility.CUSTOMER_OPERATIONS,
}
# The lab assigns all JOINT active hours to seller economics. This conservative,
# inspectable rule does not claim that the customer contributes no time.
JOINT_SELLER_ATTRIBUTION = "All JOINT item hours are seller-borne; customer-only owners are excluded."
SHIFT_TO_INCUMBENT = {
    "AUTHENTICATION_APPROACH", "CREDENTIAL_HANDLING", "AUDIT_LOGGING",
    "ENVIRONMENT_RESTRICTIONS", "RETENTION_ASSUMPTIONS",
}


def load_governance_inventory() -> GovernanceInventory:
    raw = _fixture("governance_work.json")
    items = tuple(GovernanceWorkItem(
        identifier=x["id"], name=x["name"], description=x["description"],
        category=GovernanceCategory(x["category"]),
        classification=GovernanceClassification(x["classification"]),
        technical_surfaces=tuple(x["technical_surfaces"]),
        responsible_party=GovernanceResponsibility(x["responsible_party"]),
        required=x["required"], effort_hours=x["effort_hours"], elapsed_days=x["elapsed_days"],
        origin=WorkOrigin(x["origin"]), evidence=parse_evidence_label(x["evidence"]),
        assumptions=tuple(x["assumptions"]), trace_to=tuple(x.get("trace_to", ())),
    ) for x in raw["items"])
    inventory = GovernanceInventory(raw["customer_name"], raw["fiction_notice"], items,
                                    parse_evidence_label(raw["evidence"]))
    validate_governance_inventory(inventory)
    return inventory


def validate_governance_inventory(inventory: GovernanceInventory) -> None:
    ids = [x.identifier for x in inventory.work_items]
    if len(ids) != len(set(ids)):
        raise ValueError("governance work-item identifiers must be unique")
    if not inventory.work_items or any(x.effort_hours < 0 or x.elapsed_days < 0 for x in inventory.work_items):
        raise ValueError("governance work allocations must be present and nonnegative")
    for item in inventory.work_items:
        if item.classification is GovernanceClassification.DELIVERY and item.origin is not WorkOrigin.INTRINSIC_TO_TECHNICAL_SURFACE:
            raise ValueError("delivery work must identify an intrinsic technical origin")
        if item.classification is GovernanceClassification.ACQUISITION_APPROVAL and item.origin is not WorkOrigin.CREATED_BY_ENGAGEMENT_APPROVAL_PROCESS:
            raise ValueError("approval work must identify its engagement-process origin")


def _metrics(items: tuple[GovernanceWorkItem, ...]) -> GovernanceMetrics:
    delivery = tuple(x for x in items if x.classification is GovernanceClassification.DELIVERY)
    approval = tuple(x for x in items if x.classification is GovernanceClassification.ACQUISITION_APPROVAL)
    seller_delivery = sum(x.effort_hours for x in delivery if x.responsible_party in SELLER_BORNE)
    seller_approval = sum(x.effort_hours for x in approval if x.responsible_party in SELLER_BORNE)
    customer_review = sum(x.effort_hours for x in approval if x.responsible_party in CUSTOMER_REVIEWERS)
    by_category = tuple((c, sum(x.effort_hours for x in items if x.category is c))
                        for c in GovernanceCategory if any(x.category is c for x in items))
    by_owner = tuple((o, sum(x.effort_hours for x in items if x.responsible_party is o))
                     for o in GovernanceResponsibility if any(x.responsible_party is o for x in items))
    return GovernanceMetrics(
        sum(x.effort_hours for x in delivery), sum(x.effort_hours for x in approval),
        seller_delivery, seller_approval, customer_review,
        sum(x.elapsed_days for x in approval), Decimal(seller_delivery) * Decimal("110"),
        Decimal(seller_approval) * Decimal("125"), by_category, by_owner,
    )


def _assessment(key: str, name: str, surface: str, items: tuple[GovernanceWorkItem, ...],
                removed: tuple[str, ...] = (), shifted: tuple[str, ...] = (),
                evidence: EvidenceLabel = EvidenceLabel.MODELED_ASSUMPTION,
                changes: tuple[str, ...] = ()) -> GovernanceScenario:
    metrics = _metrics(items)
    # Explicit Chapter 1 gate integration, never a new compliance verdict: delivery
    # burden affects project viability; approval burden affects target attractiveness.
    project = GateStatus.PASS if metrics.seller_delivery_cost <= Decimal("25000") else GateStatus.FAIL
    target = GateStatus.PASS if project is GateStatus.PASS and metrics.seller_acquisition_cost <= Decimal("7000") else GateStatus.FAIL
    verdict = "NO DEAL" if project is GateStatus.FAIL else ("POOR TARGET CUSTOMER" if target is GateStatus.FAIL else "PROMISING — VALIDATE IN DISCOVERY")
    effect = "DELIVERY ECONOMICS" if project is GateStatus.FAIL else ("TARGET ATTRACTIVENESS" if target is GateStatus.FAIL else "PROJECT AND TARGET REMAIN VIABLE")
    return GovernanceScenario(key, name, surface, items, removed, shifted, metrics,
                              project, target, verdict, effect, evidence, changes)


def governance_scenarios() -> tuple[GovernanceScenario, ...]:
    inventory = load_governance_inventory()
    write = tuple(x for x in inventory.work_items if WRITE_CAPABLE in x.technical_surfaces)
    read = tuple(x for x in inventory.work_items if READ_ONLY in x.technical_surfaces)
    removed = tuple(x.identifier for x in write if x.identifier not in {y.identifier for y in read})

    configuration = []
    shifted = []
    for item in inventory.work_items:
        if CONFIGURATION_FIRST not in item.technical_surfaces:
            continue
        if item.identifier in SHIFT_TO_INCUMBENT:
            item = replace(item, responsible_party=GovernanceResponsibility.INCUMBENT_VENDOR,
                           shifted_from_seller=True,
                           assumptions=item.assumptions + ("Native incumbent capability still requires verification and acceptance; the requirement is not eliminated.",))
            shifted.append(item.identifier)
        configuration.append(item)

    heavy = []
    multipliers = {"SECURITY_QUESTIONNAIRE": (2, 0), "SECURITY_REVIEW_MEETING": (2, 10),
                   "ACCESSIBILITY_CONFORMANCE": (2, 0), "CHANGE_CONTROL_DOCUMENTATION": (2, 0),
                   "IMPLEMENTATION_APPROVAL": (2, 5), "ACCEPTANCE_DOCUMENTATION": (2, 0)}
    for item in write:
        if item.identifier in multipliers:
            factor, extra_days = multipliers[item.identifier]
            item = replace(item, effort_hours=item.effort_hours * factor,
                           elapsed_days=item.elapsed_days + extra_days,
                           evidence=EvidenceLabel.SENSITIVITY_ASSUMPTION,
                           assumptions=item.assumptions + ("Documentation-heavy sensitivity changes approval mechanics, not the technical control surface.",))
        heavy.append(item)
    return (
        _assessment("WRITE_CAPABLE", "Write-capable governance surface", WRITE_CAPABLE, write),
        _assessment("READ_ONLY", "Read-only governance surface", READ_ONLY, read, removed=removed,
                    evidence=EvidenceLabel.OBSERVED_LAB_RESULT,
                    changes=("Write/consequential-authority-only items are absent; common controls and reviews remain.",)),
        _assessment("CONFIGURATION_FIRST", "Configuration-first governance surface", CONFIGURATION_FIRST,
                    tuple(configuration), shifted=tuple(shifted), evidence=EvidenceLabel.MODELED_ALTERNATIVE_ASSUMPTION,
                    changes=("Native capability shifts implementation ownership without eliminating requirements.",)),
        _assessment("DOCUMENTATION_HEAVY", "Documentation-heavy approval process", WRITE_CAPABLE,
                    tuple(heavy), evidence=EvidenceLabel.SENSITIVITY_ASSUMPTION,
                    changes=("Questionnaire, meeting, documentation, coordination, and review-wait assumptions increase; delivery controls are unchanged.",)),
    )


def assess_governance() -> GovernanceScenario:
    return governance_scenarios()[0]


def work_by_category(scenario: GovernanceScenario) -> dict[GovernanceCategory, int]:
    return dict(scenario.metrics.by_category)


def work_by_responsibility(scenario: GovernanceScenario) -> dict[GovernanceResponsibility, int]:
    return dict(scenario.metrics.by_responsibility)


def formal_rfp_trace() -> dict[str, tuple[str, ...]]:
    """Trace Chapter 4 governance artifacts/stages without changing its economics."""
    result: dict[str, list[str]] = {}
    for item in load_governance_inventory().work_items:
        for target in item.trace_to:
            result.setdefault(target, []).append(item.identifier)
    return {key: tuple(value) for key, value in result.items()}
