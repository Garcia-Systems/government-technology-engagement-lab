# Chapter 4 — The Formal RFP Motion

## 1. The first real engagement-motion experiment

Chapter 0 made `POOR TARGET CUSTOMER` a hypothesis. Chapters 1–3 separated gates, calendar time, and stakeholder mechanisms. Chapter 4 runs the first complete motion and asks whether a good bounded project remains commercially attractive when reached through `FORMAL_RFP`.

> **Fiction notice:** James River County Permitting Department, every stage, responsibility, cost rate, threshold, artifact, and timeline below are fictional educational modeling. Nothing describes Virginia law, a real government, a bid threshold, public-notice period, protest rule, statutory time, or actual security requirement.

## 2. What “formal RFP” means in this fictional lab

It means only a generic competitive sequence with response requirements, submission, clarification, selection, and contract coordination. It is an engagement-motion model—not a procurement platform, solicitation, legal model, or empirical benchmark. A competitive loss is a visible risk, but this chapter evaluates a won engagement and defers probability-weighted economics.

## 3. The journey

The fixture runs from opportunity discovery through solicitation review, qualification, requirements interpretation, design, technical/security/accessibility responses, pricing, assembly, submission, clarification, evaluation, selection, contract review, procurement coordination, implementation planning, and authorization. Its 18 `EngagementStage` records reuse Chapter 2's stage architecture. Their sequential allocation sums to 270 modeled days under the existing 30-day modeled-month convention.

```text
GOOD TECHNICAL PROJECT
        +
CUSTOMER VALUE
        +
DELIVERY WORKS
        |
        v
FORMAL RFP MOTION
        |
        +--> PRE-AWARD TECHNICAL WORK
        +--> PROPOSAL EFFORT
        +--> PROCUREMENT
        +--> CONTRACTING
        +--> LONG ELAPSED CYCLE
        |
        v
ACQUISITION-ADJUSTED ECONOMICS
        |
        v
TARGET VERDICT
```

## 4. The work before implementation begins

Every allocation is a `MODELED ASSUMPTION`. Opportunity review, qualification, solicitation review, interpretation, meetings, design, response preparation, security, accessibility, pricing, procurement, contract support, and pre-authorization planning reconcile to **192 hours**: **84 sales hours** and **108 solutions hours**. These are active seller hours; the separate 522 engineering hours remain delivery work.

## 5. Proposal requirements

Eight lightweight `ProposalArtifact` references expose structure without generating proposal prose: technical response, implementation plan, pricing response, security questionnaire, accessibility response, support plan, assumptions/exceptions, and qualifications.

## 6. Stakeholders and approvals

Stage links reuse Chapter 3 identifiers for the Department Sponsor, Director, users, IT, Security/Governance, Accessibility, Procurement, Finance, Legal/Contracts, and incumbent representative. Each link says participation, approval, technical access, coordination, or acceptance. These are legitimate responsibilities; the model observes the work and dependencies they create rather than treating stakeholder count as bad.

## 7. Customer economics

The independent customer calculation remains: $104,002.80 recoverable annual value, $102,000 first-year cost, $2,002.80 net first-year recoverable value, and nine-month implementation-only payback. The first-year nonnegative rule is a `MODELED ASSUMPTION`, not a buying benchmark.

## 8. Delivery economics

Implementation remains **522 engineering hours**. The fictional fully loaded engineering internal cost is **$110/hour**, producing **$57,420** delivery labor cost. The rate is not an employee wage and is not market evidence.

## 9. Acquisition economics

The simple fully loaded internal rates are sales **$85/hour** and solutions **$125/hour**, all `MODELED ASSUMPTION`. Applying them to 84 and 108 hours yields **$20,640 acquisition labor cost**, an `OBSERVED LAB RESULT`. No loss probability makes acquisition work disappear.

## 10. Acquisition-adjusted contribution

The engine calculates:

```text
$78,000 implementation revenue
-57,420 delivery labor cost
-20,640 acquisition labor cost
-     0 other direct cost
=   -60 acquisition-adjusted implementation contribution
```

The margin is about **-0.08%**. This simplified contribution is not company profit. The target rule requires at least **$10,000 contribution**, a labeled fictional lab sustainability threshold—not a universal benchmark. It has no weights.

## 11. Active effort versus elapsed cycle

**192 active hours are not nine months of full-time labor.** Nine modeled months still delay revenue and implementation, occupy pipeline attention, create follow-up, and preserve uncertainty. Chapter 4 does not monetize throughput or opportunity cost; that belongs to a later chapter.

## 12. Why price alone may not solve the problem

Seller and customer gates both matter. A price that repairs seller contribution can push first-year customer cost above recoverable value. The model therefore returns `NO DEAL` when project/customer viability fails rather than declaring the target repaired.

## 13. Sensitivity: lower proposal effort

A `SENSITIVITY ASSUMPTION` halves every acquisition-stage effort allocation to **96 hours**, holding structure, price, and cycle constant. Acquisition cost falls to **$10,320** and contribution rises to **$10,260**, narrowly clearing the fictional threshold. This shows how much the deliberately simple experiment requires—not a forecast that the reduction is feasible.

## 14. Sensitivity: shorter cycle

A `SENSITIVITY ASSUMPTION` reduces each stage's delay by one third (integer modeled days). Active effort stays **192 hours**, acquisition cost stays **$20,640**, and the contribution-based target rule remains failed. Effort and elapsed time are independent; this chapter deliberately does not monetize cycle.

## 15. Sensitivity: higher price

A `SENSITIVITY ASSUMPTION` raises implementation price modestly to **$90,000**. Seller contribution becomes **$11,940**, but first-year customer cost becomes $114,000 and net recoverable value becomes **-$9,997.20**. The derived project verdict is therefore `NO DEAL`; buyer acceptance is not claimed.

## 16. Baseline verdict

Project viability aggregates the same five independent Chapter 1 project dimensions and passes. Target viability fails because the calculated -$60 contribution is below the explicit $10,000 minimum. Thus the derived verdict is:

```text
PROJECT VIABILITY: PASS
TARGET VIABILITY: FAIL
VERDICT: POOR TARGET CUSTOMER
```

## 17. What Chapter 4 reproduces

Given its fictional assumptions, the executable reproduces the cookbook's `POOR TARGET CUSTOMER` result. Findings are traced to thresholds and visible mechanisms: high acquisition effort, long cycle, multiple approvals, pre-award technical work, contract coordination, procurement dependency, weak direct buyer control, and contribution below the modeled minimum. There is no weighted friction or procurement score.

## 18. What Chapter 4 does not prove

It does not prove anything about government markets, actual procurement, win rates, legal workload, support profitability, opportunity cost, or acceptable prices. Support revenue remains $24,000 and is not forced to fail. Determinism validates arithmetic, not realism.

## 19. Why a cooperative paid pilot comes next

The unresolved falsification question is whether a different, cooperative motion can preserve customer and delivery viability while reducing pre-award burden. That is the question for Chapter 5. **Chapter 5 is not implemented here.**

Run `python -m government_engagement_lab formal-rfp`, `formal-rfp-economics`, and `formal-rfp-scenarios` to inspect the model.
