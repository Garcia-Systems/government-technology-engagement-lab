# Chapter 1 — Separate the Project from the Customer

> **Fiction notice:** James River County Permitting Department is wholly fictional. Every condition in this chapter is educational modeling, not evidence about a real locality, customer, or government market.

## 1. The classification mistake

Sales friction and project infeasibility are different mechanisms. Calling both “a bad opportunity” loses the reason an opportunity failed and makes a later experiment impossible to interpret. Chapter 1 therefore makes two statements executable:

```text
GOOD PROJECT ≠ GOOD TARGET CUSTOMER
POOR TARGET CUSTOMER ≠ NO DEAL
```

## 2. A project is not a customer

A **project** concerns a meaningful problem, a feasible bounded intervention, customer value, delivery, and support. A **target** concerns whether the opportunity can reasonably be reached, qualified, approved, contracted, and closed under the modeled engagement conditions. `ENGAGEMENT_MOTION` records context as `BASELINE_COOKBOOK_MOTION`; it is not a seventh score and has no stages in this chapter.

```text
                    OPPORTUNITY
                         |
          +--------------+--------------+
          |                             |
          v                             v
      PROJECT                         TARGET
      VIABILITY                      VIABILITY
          |                             |
  +-------+-------+                     |
  |       |       |                     |
PROBLEM  TECH   ECONOMICS          ACQUISITION
         |      /      \                |
         | DELIVERY  SUPPORT            |
         +-------+------+                |
                 |                       |
                 v                       v
               PASS                    FAIL
                 \                       /
                  \                     /
                   +---------+---------+
                             |
                             v
                   POOR TARGET CUSTOMER
```

Contrast that classification with a foundational failure:

```text
PROJECT VIABILITY FAILS
          ↓
       NO DEAL
```

## 3. The six evaluation gates

The implementation defines `PROBLEM_ATTRACTIVENESS`, `TECHNICAL_FEASIBILITY`, `CUSTOMER_ECONOMICS`, `DELIVERY_ECONOMICS`, `SUPPORT_ECONOMICS`, and `TARGET_ATTRACTIVENESS`. Every gate has a status, reason codes, evidence labels, and a concise explanation. Status is one of `PASS`, `FAIL`, `CONDITIONAL`, or `NOT_EVALUATED`. There is no severity weighting, government score, or 0–100 opportunity score.

## 4. Project viability

Project viability aggregates only the first five gates. `FAIL` takes precedence. A `CONDITIONAL` or `NOT_EVALUATED` gate cannot silently become a pass. Only all passes yield `PROJECT VIABILITY: PASS`.

The customer-economics gate uses a deliberately modest fictional lab rule (`MODELED ASSUMPTION`):

```text
first-year net recoverable value >= $0
```

The executable exposes recoverable annual value, implementation price, annual support, their first-year cost, first-year net recoverable value, and implementation-only payback. This deterministic rule is not a universal purchasing benchmark.

Delivery and support are separate gates. The cookbook supplies 522 engineering hours and $24,000 annual support but no seller labor rates or support delivery costs. Their baseline passes therefore inherit modeled viability conditions and explicitly say that contribution economics cannot yet be calculated.

## 5. Target viability

Target viability is the `TARGET_ATTRACTIVENESS` result. In the baseline it fails for explicit `MODELED ASSUMPTION` reasons: `PROCUREMENT_DIFFICULTY`, `STAKEHOLDER_FRICTION`, `WEAK_BUYER_ACCESS`, `LONG_SALES_CYCLE`, and `HIGH_SOLUTIONS_EFFORT`. These are mechanisms in one fiction, not claims about governments generally.

## 6. Why `POOR TARGET CUSTOMER` is not `NO DEAL`

`POOR TARGET CUSTOMER` requires a viable project and a failed target. `NO DEAL` has higher precedence when a foundational project gate fails. The distinction prevents acquisition friction from being mislabeled as technical infeasibility—and prevents a technically impossible project from being dismissed as mere sales difficulty.

## 7. Baseline gate walk-through

| Gate | Status | Basis |
|---|---|---|
| Problem attractiveness | `PASS` | positive modeled recoverable administrative value |
| Technical feasibility | `PASS` | bounded layer; authoritative systems remain authoritative |
| Customer economics | `PASS` | $104,002.80 value − $102,000.00 first-year cost = $2,002.80 |
| Delivery economics | `PASS` | inherited modeled viability; labor rates absent |
| Support economics | `PASS` | inherited modeled viability; support cost absent |
| Target attractiveness | `FAIL` | five explicit acquisition impediments |

Thus project viability is `PASS`, target viability is `FAIL`, and the verdict remains `POOR TARGET CUSTOMER` (`OBSERVED LAB RESULT` given fictional inputs).

## 8. Counterfactual: technical failure

Scenario B changes only required access: `REQUIRED_ACCESS_UNAVAILABLE` is a `SENSITIVITY ASSUMPTION`, not an observed government fact. Technical feasibility fails, project viability fails, and precedence returns `NO DEAL` (`OBSERVED LAB RESULT`). This is only a gate substitution—not the later closed-integration experiment.

## 9. Counterfactual: customer economics failure

Scenario C changes recoverable annual value from $104,002.80 to $50,000.00 while first-year cost remains $102,000.00 (`SENSITIVITY ASSUMPTION`). The transparent lab rule fails, project viability fails, and the result is `NO DEAL`. The original fixture is unchanged.

## 10. Counterfactual: repair target attractiveness

Scenario D keeps the project inputs unchanged and hypothetically replaces baseline target impediments with favorable acquisition conditions (`SENSITIVITY ASSUMPTION`). Both viability results pass. The restrained verdict is `PROMISING — VALIDATE IN DISCOVERY`, not “government is a good market.” No pilot, contract vehicle, procurement workflow, or channel is modeled.

## 11. Verdict precedence

Chapter 1 implements only this narrow order:

1. project `FAIL` → `NO DEAL`;
2. unresolved/conditional project or target → `INVESTIGATE`;
3. project `PASS` + target `FAIL` → `POOR TARGET CUSTOMER`;
4. project `PASS` + target `PASS` → `PROMISING — VALIDATE IN DISCOVERY`.

This is reusable assessment semantics, not the Chapter 20 capstone verdict engine.

## 12. Running the experiments

```bash
python -m government_engagement_lab gates
python -m government_engagement_lab gate-scenarios
pytest
```

The first command prints every baseline gate and reason. The second starts with a compact comparison, then prints each scenario's changed assumptions and individual statuses so the table never hides the mechanism. Chapter 0 remains available through `baseline` and `scenarios`.

## 13. What Chapter 1 demonstrates

The executable demonstrates `OBSERVED IMPLEMENTATION STRUCTURE`: project and target viability are independent typed results, engagement motion is non-scored context, and verdict precedence distinguishes project failure from target failure. Given the fictional inputs, deterministic `OBSERVED LAB RESULT`s reproduce the baseline and respond predictably to three labeled substitutions.

It does **not** demonstrate facts about government. Sensitivity assumptions are educational counterfactuals, not observations.

## 14. What remains unknown

Chapter 2 must still determine what evidence describes a buying journey and how engagement motion might affect acquisition conditions. This chapter does not decompose stages, actors, procurement, approvals, pilots, security, accessibility, channels, or contract vehicles. It establishes the classification boundary those later experiments may feed without changing the underlying project by accident.
