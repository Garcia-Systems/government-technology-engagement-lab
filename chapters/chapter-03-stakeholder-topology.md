# Chapter 3 — Stakeholder Topology

## 1. Why stakeholder count is misleading

```text
STAKEHOLDER COUNT ≠ STAKEHOLDER FRICTION
```

A headcount describes participation. It does not reveal who decides, whose approval is required, who controls access, or whether dependencies are sequential. This chapter therefore records relationships and authorities rather than producing a weighted stakeholder score. Every organization, authority, and relationship below is a **MODELED ASSUMPTION** for the wholly fictional James River County Permitting Department—not a claim about a real locality.

## 2. Meet the fictional stakeholder map

```text
                     DEPARTMENT DIRECTOR
                    (problem / purchase)
                              |
                         REPORTS_TO
                              ^
                              |
                    OPERATIONS MANAGER
                    (LIMITED SPONSOR)
                  /          |           \
          DEPENDS_ON   REQUIRES_APPROVAL  REQUIRES_APPROVAL
               /             |                  \
              v              v                   v
       IT REPRESENTATIVE  PROCUREMENT       LEGAL / CONTRACTS
          |          \          |
   CONTROLS_ACCESS   DEPENDS_ON  purchase path
          |              \
          v               v
 SOLUTIONS ENGINEER   INCUMBENT VENDOR
          ^
          |
 SECURITY / GOVERNANCE advises IT

Accessibility and IT acceptance are separately required from the sponsor.
Permitting staff supply workflow information to the sponsor.
```

The fixture also includes finance, accessibility, security/governance, permitting-user, and seller-solutions functions. The topology is a deterministic list of typed nodes, relationships, and stage mappings—an **OBSERVED IMPLEMENTATION STRUCTURE**.

## 3. Decision makers, approvers, blockers, and users

The role vocabulary is `DECISION_MAKER`, `INFLUENCER`, `APPROVER`, `BLOCKER`, `USER`, `TECHNICAL_GATEKEEPER`, and `SPONSOR`. Roles may be combined and need not all occur in another topology. `BLOCKER` is not a judgment of motive: it means legitimate authority or control can prevent progress until a requirement is satisfied.

Authority domains make five different questions inspectable: `PROBLEM_OWNER`, `PURCHASE_APPROVER`, `TECHNICAL_ACCESS_OWNER`, `CONTRACT_APPROVER`, and `IMPLEMENTATION_ACCEPTOR`. Permitting staff influence discovery and acceptance without each becoming a purchase approver.

## 4. The difference between sponsorship and authority

```text
WANTS THE PROJECT
       ≠
CAN AUTHORIZE EVERY STEP
```

The Operations Manager is the baseline internal sponsor and problem owner. Sponsor strength is `LIMITED`: the sponsor coordinates the journey but lacks procurement, contract, security, and technical-access authority. The Department Director has meaningful department decision and purchase authority but still cannot authorize every external function.

## 5. Technical gatekeepers

The IT Representative controls systems and interface access. The incumbent-vendor representative may control a supported interface path. Security/governance can withhold its modeled approval until requirements are met. These are dependencies, not a real security review, integration design, vendor comparison, or claim that access is closed.

## 6. Procurement and contract authority

Procurement controls the fictional purchasing path, finance confirms modeled budget availability, and legal/contracts approves contract terms when needed. No solicitation, contract vehicle, threshold, detailed procedure, or real legal rule is modeled. Their separation demonstrates that department desire and contract authorization are different authorities.

## 7. Stakeholders mapped to the buying journey

Every Chapter 2 stage has a primary responsible party, participants, approvers, possible blockers, and technical gatekeepers. For example, `SECURITY_ACCESS_REVIEW` includes the sponsor, solutions engineer, IT, security/governance, and incumbent-vendor representative; security approval is required, while IT and the interface representative expose access-control dependencies. The CLI prints the complete mapping:

```text
STAGE → PARTICIPANTS → REQUIRED APPROVALS → BLOCKING AUTHORITIES → ACCESS OWNERS
```

This is linkage to the existing ten-stage journey, not implementation of the reviews named by those stages.

## 8. Where coordination burden appears

Chapter 3 refines Chapter 1's `STAKEHOLDER_FRICTION` through explicit reasons: `MULTIPLE_REQUIRED_APPROVALS`, `ACCESS_CONTROL_DEPENDENCY`, `SEQUENTIAL_APPROVAL_DEPENDENCY`, `INCUMBENT_VENDOR_DEPENDENCY`, and `CROSS_FUNCTIONAL_COORDINATION`. `UNCLEAR_DECISION_AUTHORITY` appears only in the fragmented-authority sensitivity. Each finding names people, stages, an explanation, and evidence classification.

## 9. Baseline topology

The baseline combines an existing project owner, multiple approvals, technical-access control, and a procurement dependency. The system reports stakeholder count, role assignments, participation per stage, approval paths, blocking paths, technical-access dependencies, most-involved stakeholders, and highest-participation stages as **OBSERVED LAB RESULT** values given the fictional topology. It does not infer that a high count is bad. Chapter 1 remains `PASS` project / `FAIL` target / `POOR TARGET CUSTOMER`.

## 10. Strong-sponsor sensitivity

`STRONG_SPONSOR` changes only modeled authority. The sponsor gains clearer department decision and purchase coordination authority, consolidating one budget-approval dependency. Procurement, IT, security, and their legitimate controls remain. This **SENSITIVITY ASSUMPTION** reduces an explicit coordination mechanism; it is not a pilot or alternate engagement motion.

## 11. Fragmented-authority sensitivity

`FRAGMENTED_AUTHORITY` adds a separate finance approval and blocking path at proposal, plus `UNCLEAR_DECISION_AUTHORITY`. Approval and coordination dependencies increase explicitly. This is a **SENSITIVITY ASSUMPTION**, not a general statement about governments.

## 12. No-sponsor sensitivity

`NO_SPONSOR` removes the sponsor role and marks sponsor strength `ABSENT`. The bounded technical-project identifier and technical-feasibility assumption stay unchanged. Target access worsens, but the scenario does not become `NO DEAL` automatically:

```text
GOOD PROJECT ≠ GOOD TARGET
```

## 13. Why more stakeholders does not automatically mean a worse opportunity

No rule maps stakeholder count to a gate or verdict. Effects arise only through named mechanisms—missing sponsorship, required approval, ambiguity, access control, blocking authority, or cross-functional coordination. Counts remain descriptive, and no `friction_score` exists.

## 14. Running the lab

```bash
python -m government_engagement_lab stakeholders
python -m government_engagement_lab stakeholder-summary
python -m government_engagement_lab stakeholder-scenarios
```

The first command prints nodes, authorities, relationships, and journey linkage. The second prints reconcilable counts without a score. The third compares `BASELINE`, `STRONG_SPONSOR`, `FRAGMENTED_AUTHORITY`, and `NO_SPONSOR`, including actual mechanism changes.

## 15. What Chapter 3 demonstrates

Stakeholder topology can be executable without becoming an arbitrary ranking. It distinguishes sponsorship from authority, shows which relationships produce coordination work, and gives Chapter 1's high-level friction reason a trace to Chapter 2 stages and Chapter 3 findings.

## 16. What Chapter 3 does not yet establish

It does not establish real procedures, detailed security or accessibility workload, solicitation mechanics, proposal economics, integration closure, acquisition cost, throughput, repeatability, channels, pilots, contract vehicles, or a final motion verdict. All participation remains fictional modeling.

## 17. Why the formal RFP motion comes next

The stage-to-authority structure can later support a formal motion by making required participation inspectable. Chapter 3 stops at topology. Chapter 4 must decide how a formal RFP motion uses these dependencies; nothing here implements that motion.
