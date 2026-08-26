# Chapter 12 — Security, Accessibility, and Governance Surface

> **Fiction notice:** James River County Permitting Department, every control, owner, hour, review, and gate threshold below are fictional educational assumptions. This chapter states no real law, accessibility mandate, security policy, procurement rule, or compliance benchmark.

## 1. “Government bureaucracy” is too crude a model

Security, accessibility, auditability, supportability, authorization, and controlled deployment can be legitimate properties of delivered software. Calling all related effort “bureaucracy” hides the mechanism. Chapter 12 instead asks who does each inspectable item, why it exists, and whether active work or elapsed wait drives the result.

## 2. Delivery requirement versus approval requirement

```text
SECURITY / ACCESSIBILITY / GOVERNANCE
                |
        +-------+-------+
        |               |
        v               v
DELIVERY WORK      APPROVAL WORK
        |               |
        v               v
IMPLEMENT         DOCUMENT
TEST              RESPOND
LOG               REVIEW
CONTROL           COORDINATE
        |               |
        +-------+-------+
                |
                v
        ENGAGEMENT ECONOMICS
```

`DELIVERY` means a control, behavior, verification, or operational property intrinsic to the modeled technical surface. `ACQUISITION_APPROVAL` means a response, review, meeting, acceptance artifact, or coordination activity created by the modeled engagement/approval process. The latter may be legitimate; the classification is economic attribution, not criticism.

## 3. The governance work taxonomy

The executable vocabulary is `SECURITY_IMPLEMENTATION`, `SECURITY_REVIEW`, `ACCESSIBILITY_IMPLEMENTATION`, `ACCESSIBILITY_REVIEW`, `ACCESS_CONTROL`, `AUDITABILITY`, `DATA_HANDLING`, `DEPLOYMENT_CONTROL`, `CHANGE_CONTROL`, `DOCUMENTATION`, and `APPROVAL_COORDINATION`. Each immutable item also carries an identifier, description, applicable surfaces, owner, required flag, active hours, elapsed days, origin, evidence, notes, and optional Chapter 4 trace.

No weighted governance or compliance score exists.

## 4. Security implementation work

The fictional inventory includes authentication, least privilege, credential handling, approved access, audit logging, revocation, and environment restrictions. Write authority adds authorization, expanded write audit detail, post-write reconciliation, and production mutation controls. These are `DELIVERY` items—not procurement friction.

## 5. Security review work

The security questionnaire, review meeting, and customer review are separate `ACQUISITION_APPROVAL` items. Chapter 4's 16-hour security/access response now traces to `SECURITY_QUESTIONNAIRE`; its established economics are unchanged.

## 6. Accessibility implementation and verification

Keyboard operation, semantic structure, visible labels, export readability, and verification are delivery work for the modeled user-facing output. Preparing a conformance response and customer review are approval work. These are generic engineering capabilities; the lab asserts no applicable statute or real jurisdictional mandate.

## 7. Data-handling assumptions

Retention behavior, export handling, temporary-file cleanup, provenance, and deletion/cleanup are explicit delivery items. The read-only edge retains them: removing writes does not remove responsibility for copied data or reports.

## 8. Change and deployment control

Both primary surfaces retain environment restrictions, general rollback planning, change documentation, deployment approval, and acceptance. Only the write surface adds authoritative-write rollback, production mutation change control, and write-specific review.

## 9. Responsibility ownership

Owners use `SELLER`, `PARTNER`, `CUSTOMER_IT`, `CUSTOMER_SECURITY`, `CUSTOMER_ACCESSIBILITY`, `CUSTOMER_OPERATIONS`, `INCUMBENT_VENDOR`, and `JOINT`. For seller economics, seller and joint hours are seller-borne; customer-only and incumbent hours are excluded. This conservative lab rule is explicit. Customer approval participation remains visible separately.

```text
REQUIREMENT EXISTS
        |
        +--------------------+
        |                    |
        v                    v
SELLER IMPLEMENTS       INCUMBENT ALREADY
CUSTOM CONTROL          PROVIDES CONTROL
        |                    |
        v                    v
SELLER DELIVERY         VERIFY / CONFIGURE /
EFFORT                  ACCEPT
```

## 10. Write-capable surface

The write-capable baseline models **205 seller delivery governance hours**, **49 seller acquisition/approval hours**, **28 customer-only review hours**, and **42 elapsed review days**. At the fictional rates, governance attribution is **$22,550 delivery** and **$6,125 acquisition**. Its modeled project and target gates both pass: legitimate controls are material, but they do not automatically make the engagement unattractive.

## 11. Read-only surface

Read-only removes six write/consequential-authority items: write authorization, authoritative-write rollback, expanded write audit detail, production mutation control, post-write reconciliation, and write change review. It retains authentication, least privilege, auditing/provenance, data handling, accessibility, deployment, documentation, questionnaire, reviews, and acceptance.

The result is **151 seller delivery hours** (54 fewer), the same **49 seller approval hours**, **23 customer review hours**, and **35 review days**. Chapter 6's claim is therefore refined rather than reversed: read-only narrows governance, but does not drive it to zero.

## 12. Configuration-first surface

Configuration-first retains requirements but shifts authentication, credential handling, audit logging, environment restrictions, and retention implementation to the fictional incumbent capability. Those five items remain inspectable and are marked shifted—not removed. Seller delivery governance falls to **100 hours**; seller approval remains **49 hours**, customer review **23 hours**, and review time **35 days**. Seller work still includes role configuration, verification, accessibility, change documentation, and acceptance.

## 13. Documentation-heavy sensitivity

`DOCUMENTATION_HEAVY` holds the write-capable technical surface and all delivery items unchanged. It doubles selected questionnaire, meeting, conformance, change-documentation, coordination, and acceptance effort, while adding review delay. This `SENSITIVITY ASSUMPTION` produces **98 seller approval hours** and **57 elapsed review days**, versus 49 and 42. The technical controls did not become more extensive; the modeled approval mechanics did.

## 14. Implementation effort versus elapsed review

Active remediation and implementation consume labor. Reviewer availability consumes calendar time. The executable sums elapsed days separately and never multiplies them by an hourly rate. Thus a 12-day security wait is not 12 days of full-time seller labor.

## 15. Economic attribution

```text
TOTAL SELLER GOVERNANCE WORK
        |
        +--> DELIVERY IMPLEMENTATION
        |    access controls; audit logging; accessibility;
        |    deployment/change controls; data handling
        |
        +--> ACQUISITION / APPROVAL
             questionnaires; meetings; conformance response;
             coordination; acceptance paperwork
```

Category and responsibility totals reconcile to item-level hours. Customer reviewers are reported but never charged to seller contribution.

## 16. When governance affects delivery economics

Delivery governance hours use the delivery-cost path. If this burden crossed the fictional delivery threshold, `DELIVERY_ECONOMICS` would fail and the existing gate precedence would yield `NO DEAL`. In the four main cases it remains supported by the modeled economics.

## 17. When governance affects target attractiveness

Approval hours use the acquisition-cost path. The documentation-heavy case leaves project viability at `PASS`, but its $12,250 seller approval cost exceeds the fictional $7,000 acquisition threshold. `TARGET_ATTRACTIVENESS` fails and the existing verdict is `POOR TARGET CUSTOMER`. No new “governance verdict” is introduced.

## 18. What Chapter 12 demonstrates

Given the fictional inventory, “security requirements made delivery expensive” is mechanically different from “security approval made the engagement expensive to win.” The same is true for accessibility and governance. Read-only reduces authority-dependent delivery work; native capability shifts ownership; documentation intensity changes acquisition economics without changing controls. This **clarifies** the cookbook hypothesis: the poor-target result can be driven by approval mechanics, while legitimate control work may remain commercially supportable.

## 19. What Chapter 12 does not prove

The quantities are not market benchmarks. The chapter does not establish what any real government requires, whether any law applies, whether a control is universally necessary, whether the fictional buyer would approve the work, or whether government is a good or poor market. It does not score compliance or make Chapter 13 assumptions.

## 20. Why closed integration comes next

Chapter 12 leaves unresolved how a closed incumbent integration boundary changes feasibility, access, responsibility, and commercial leverage. Chapter 13 may test that question later. It is deliberately not implemented here.
