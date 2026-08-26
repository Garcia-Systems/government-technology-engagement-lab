# Chapter 0 — The `POOR TARGET CUSTOMER` Hypothesis

> **Fiction notice:** James River County Permitting Department is wholly fictional. It is not James City County, Williamsburg, York County, Newport News, any actual Virginia locality, or any real government customer. All workflows, staffing, procurement, prices, hours, requirements, approvals, contracts, and finances below are fictional educational `MODELED ASSUMPTION`s.

## 1. The hypothesis

The fictional Custom Software Opportunity Cookbook called this opportunity `POOR TARGET CUSTOMER`. Chapter 0 reconstructs why. It does not ask the executable to endorse the verdict; it makes the verdict precise enough for later experiments to try to break it.

The eventual laboratory question is whether local government is inherently a poor target for this engagement or whether the cookbook modeled a poor acquisition and procurement motion. A possible relationship—**same technical project + different engagement motion = different commercial verdict**—is only a hypothesis. Chapter 0 neither assumes nor proves it.

## 2. Meet the fictional department

`MODELED ASSUMPTION`: James River County Permitting Department is a fictional county-level department with approximately 32 staff. The similar-sounding name creates no relationship to a real place. Its modeled conditions provide a controlled case, not a sample from which to generalize about government.

The operational problem is coordination overhead: duplicate entry, status reconciliation, report preparation, document/status lookup, correction administration, management reporting, and avoidable administrative rework.

## 3. The permitting workflow

`MODELED ASSUMPTION`:

```text
Application
    ↓
Intake
    ↓
Validation
    ↓
Department Review
    ↓
Corrections / Resubmission
    ↓
Approval
    ↓
Status / Record
    ↓
Reporting
```

The order is important and is fixture-backed. It describes only the fictional case.

## 4. The administrative burden

The cookbook modeled **$201,232.00** in annual current-state burden and **$104,002.80** in recoverable annual value (`MODELED ASSUMPTION`). No unsupported line-item decomposition is added. Consequently, these figures are not measurements of a locality, benchmarks for a government market, or proof that all modeled value can be captured.

## 5. Proposed intervention boundary

The proposed intervention is a workflow and coordination layer. Existing systems remain authoritative. The project addresses administrative handling without pretending to replace the underlying systems of record. This boundary makes the technical project plausible under the fiction; it does not establish feasibility for a real system.

## 6. Customer economics

The supplied inputs are an implementation price of **$78,000.00** and annual support of **$24,000.00** (`MODELED ASSUMPTION`). The program applies only these transparent calculations:

| Derived measure | Formula | Result | Evidence |
|---|---|---:|---|
| Customer first-year cost | implementation + annual support | $102,000.00 | `OBSERVED LAB RESULT` |
| First-year net recoverable value | recoverable annual value − first-year cost | $2,002.80 | `OBSERVED LAB RESULT` |
| Implementation-only payback | implementation / recoverable annual value × 12 | approximately 9.00 months | `OBSERVED LAB RESULT` |

Here `OBSERVED LAB RESULT` has a narrow meaning: **given fictional modeled assumptions, the program deterministically produced the result**. It is not observed government evidence. The payback measure excludes support, says so in its name, and must not be represented as full first-year payback.

## 7. Delivery and support assumptions

The cookbook supplied **522 engineering hours**, **192 solutions/sales hours**, and viable support coverage (`MODELED ASSUMPTION`). Technical feasibility and support viability both pass in the reconstructed case. Delivery is plausible within the supplied boundary.

Chapter 0 does not invent engineering or solutions labor rates. It therefore cannot calculate seller contribution margin. Effort is inspectable, but a monetary delivery-economics conclusion beyond the supplied viability condition would exceed the evidence.

## 8. Acquisition and procurement assumptions

The modeled sales cycle is **9 months**. Five explicit acquisition conditions impair target attractiveness:

- `PROCUREMENT_DIFFICULTY`
- `STAKEHOLDER_FRICTION`
- `WEAK_BUYER_ACCESS`
- `LONG_SALES_CYCLE`
- `HIGH_SOLUTIONS_EFFORT`

All are `MODELED ASSUMPTION`s about this fictional engagement. They are visible mechanisms, not an arbitrary weighted “government score,” and are not claims about actual procurement.

## 9. Why a viable project can still be a poor target

The reconstructed logic is:

```text
MEANINGFUL PROBLEM
        ↓
TECHNICALLY FEASIBLE
        ↓
CUSTOMER ECONOMICS WORK
        ↓
DELIVERY / SUPPORT PLAUSIBLE
        ↓
ACQUISITION + PROCUREMENT
        ↓
TARGET ATTRACTIVENESS FAILS
        ↓
POOR TARGET CUSTOMER
```

The executable expresses those dimensions as independent gates:

```text
Problem attractiveness       PASS
Technical feasibility        PASS
Customer economics           PASS
Delivery economics           PASS
Support viability            PASS
Target attractiveness        FAIL
```

The verdict follows the explicit target failure. It does not silently recast the case as technical failure, lack of customer value, or unsupported support. Thus **good project ≠ good target customer**. And `POOR TARGET CUSTOMER ≠ NO DEAL`: the former describes modeled target/acquisition attractiveness, while the latter is a different historical verdict.

## 10. Historical cookbook scenarios

The fixture preserves these inherited `MODELED ASSUMPTION`s:

| Historical scenario | Original modeled verdict |
|---|---|
| Baseline | `POOR TARGET CUSTOMER` |
| Cooperative pilot | `PROMISING — VALIDATE IN DISCOVERY` |
| Formal RFP | `POOR TARGET CUSTOMER` |
| Higher contract value | `POOR TARGET CUSTOMER` |
| Closed legacy integration | `NO DEAL` |
| Existing vendor module | `CONFIGURE / BUY` |
| Reusable technology + hard sales | `POOR TARGET CUSTOMER` |

These are reference points, not fresh conclusions. Chapter 0 implements none of the experiments suggested by their names.

## 11. Running the executable baseline

After installing the local package, run:

```bash
python -m government_engagement_lab baseline
python -m government_engagement_lab scenarios
pytest
```

The first command labels fictional inputs and deterministic outputs, prints the unweighted findings and gates, and identifies the verdict as the hypothesis under test. The second inspects historical outcomes without simulating them.

## 12. What Chapter 0 proves

Chapter 0 establishes only `OBSERVED IMPLEMENTATION STRUCTURE`: the supplied fictional case can be encoded in typed records, loaded from structured fixtures, calculated deterministically, and assessed through separate gates. Given those inputs, the executable reproduces the customer calculations and baseline cookbook verdict (`OBSERVED LAB RESULT`). It also shows structurally that passing technical, customer, delivery, and support gates need not force the target gate to pass.

## 13. What Chapter 0 does **not** prove

It does not prove that the burden is real or recoverable, that the price or effort is market-representative, that procurement works this way, or that a real customer would buy. It does not show that government is inherently good or bad as a market. It neither validates security/accessibility assumptions nor describes a real locality. Most importantly, reproducing a historical verdict does not validate it.

The conclusion is therefore not “government is a poor customer.” It is:

> `POOR TARGET CUSTOMER` is the hypothesis that subsequent experiments must attempt to break.

## 14. Questions the remaining lab must answer

Later chapters may ask whether engagement motion changes acquisition burden, whether a technically identical boundary survives alternative paths, and which results repeat. They will need to introduce new assumptions with `SENSITIVITY ASSUMPTION` or `MODELED ALTERNATIVE ASSUMPTION`, and keep computed outcomes distinct as `OBSERVED LAB RESULT`.

Those experiments are deliberately absent here. Chapter 1 should extend the evidence-labeled model rather than mutate the baseline, retain explicit findings rather than add an opaque score, and decide what new evidence is actually required before implementing any alternative motion.
