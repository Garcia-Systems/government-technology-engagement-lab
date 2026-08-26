# Chapter 19 — Engagement Motion Economics

## 1. Same problem, different commercial machine

Chapter 19 asks which motion is viable for substantially the same fictional annual recoverable burden of **$104,002.80**. It does not ask which row has the largest number.

```text
                         SAME PROBLEM
                              |
      +-----------+-----------+-----------+-----------+
      |           |           |           |           |
      v           v           v           v           v
     RFP        PILOT      CONFIGURE    PARTNER    INCUMBENT
      |           |           |           |           |
      v           v           v           v           v
 ACQUISITION   BOUNDED     NATIVE      ACCESS      SUPPORTED
  BURDEN        ENTRY      CAPABILITY   LEVERAGE      PATH
      |           |           |           |           |
      +-----------+-----------+-----------+-----------+
                              |
                              v
                    DIFFERENT ECONOMICS
                              |
                              v
                      DIFFERENT VERDICTS
```

```text
GOVERNMENT
IS NOT ONE
ENGAGEMENT MOTION
```

## 2. Why the motions must be normalized

Prior chapters call amounts pilot price, implementation price, customer contract value, seller revenue, module cost, and support fee. Chapter 19 **loads, normalizes, compares, and explains** them; it does not recreate their economics.

The normalization vocabulary is a **MODELED ASSUMPTION** about presentation only:

* **CUSTOMER IMPLEMENTATION PRICE** — upfront amount the customer pays for the engagement.
* **SELLER ENGAGEMENT REVENUE** — implementation revenue retained by the technical seller; it can differ from customer price in a channel motion.
* **RECURRING CUSTOMER COST** — annual support or license amount paid by the customer.
* **SELLER ACQUISITION HOURS** — seller-borne pre-authorization work from Chapter 15.
* `NOT_APPLICABLE` — the repository did not model that party's economics; it never means zero.

## 3. The common comparison schema

`MotionComparison` preserves customer value, residual, customer and seller cash flows, acquisition, delivery, cycle, access, governance, support, relationship ownership, throughput, repeatability, risks, six viability dimensions, verdict, and chapter sources. It is a comparison record—not a scorecard. The six dimensions remain **problem attractiveness, technical feasibility, customer economics, delivery economics, support economics, and target attractiveness**.

## 4. Customer economics across motions

The `motion-customer` view always places value addressed beside implementation price, recurring cost, first-year cost, first-year net value, payback, coverage, and residual. A $34,000 small engagement addresses only $43,681.18; its low price cannot be read as equivalent coverage to the $104,002.80 broad motion. The read-only edge and configuration-first options also intentionally leave material residual value.

## 5. Seller economics across motions

The `motion-seller` view keeps seller implementation revenue separate from delivery and acquisition cost. The observed acquisition-adjusted contributions include Formal RFP **-$60**, pilot **$13,310**, read-only edge **$17,485**, configuration-first **$20,270**, small departmental **$9,830**, larger contract **$27,445**, partner-led **$11,205**, and existing path **$7,530**. Incumbent seller profitability is `NOT_APPLICABLE`, not invented.

## 6. Acquisition effort across motions

Chapter 15 supplies the totals and category trace. Formal RFP consumes 192 seller hours; pilot 58; configuration-first 54; small departmental 58; larger contract 77; partner-led 91; existing path 114. Buyer access, qualification, discovery, technical validation, governance support, proposal, procurement, contracting, planning, and partner coordination remain inspectable through the Chapter 15 work items.

## 7. Elapsed cycle and throughput

Elapsed days are displayed separately and are never monetized. Chapter 16 throughput is included only for Formal RFP, cooperative pilot, partner-led, and existing path: respectively 4, 8, 4, and 7 completed engagements in the modeled year, with annualized contribution of -$240, $106,480, $44,820, and $52,710. Only the RFP portfolio overloads modeled capacity (five periods and 98 deferred hours).

## 8. Technical access

Chapter 13 makes access a precedence constraint. In the closed-access baseline, broad write-dependent RFP, partner, and existing-path implementations are technically infeasible even when their arithmetic is positive. An existing contract vehicle removes no interface constraint. The approved read-only edge is compatible; native configuration and the incumbent module use supported native access.

## 9. Governance surface

Chapter 12 reports seller delivery governance hours, seller approval/acquisition governance hours, and elapsed review days. Write-capable work is 205 / 49 / 42; read-only is 151 / 49 / 35; configuration-first is 100 / 49 / 35. Read-only-only write work **disappears**. Configuration work **shifts to incumbent**. Partner-led ownership **shifts to partner**. These are deliberately different descriptions, and Chapter 19 does not add these hours to Chapter 15 totals a second time.

## 10. Support ownership

Custom motions retain seller obligations; a read-only edge includes export, mapping, reporting, schema-change, and access-expiration support. Partner-led support uses partner frontline escalation with custom-seller backing. Configuration-first divides native and configuration responsibility. The incumbent module has one incumbent support owner. Recurring revenue is not represented as pure contribution.

## 11. Configuration and incumbent alternatives

Configuration-first uses native capability, lowers custom ownership, and leaves $47,571.26 residual under Chapter 7. The incumbent module addresses $86,002.80 and leaves $18,000 residual under Chapter 14, with vendor dependency and limited customization visible. Neither result is silently promoted to a product verdict.

## 12. Direct versus partner-led

The partner motion reduces seller acquisition from 192 to 91 hours and the cycle from 270 to 225 days, but preserves channel cost, partner dependency, reduced seller relationship ownership, and the same closed-write access problem. It is attractive only when access and partner leverage exist.

## 13. Formal RFP versus existing purchasing path

The existing path lowers acquisition from 192 to 114 hours and elapsed cycle from 270 to 127 days. Buyer access and technical governance remain, while closed technical access still blocks delivery. Procurement work disappeared; technical work did not.

## 14. Small versus larger contract

The small motion is cheaper because it addresses $43,681.18, not because it provides the larger motion's $80,681.18 coverage. Under the modeled minimum contribution, the small motion is fragile at $9,830 while the justified larger contract contributes $27,445. Larger is conditional on genuine scope and value—not contract size alone.

## 15. Pilot-first entry

The paid pilot bounds scope, acquisition, and cycle, but captures $52,000 of value and requires a strong sponsor. The read-only edge lowers authority and governance and captures $57,201.54. These findings make pilot-first promising under bounded conditions, not universally dominant.

## 16. Repeatability

Chapter 17 supports meaningful within-account reuse; Chapter 18 shows that technical reuse does not automatically preserve buyer access, procurement, governance, or support economics across governments. Custom motions are therefore marked cross-customer conditional. This is an engagement-repeatability finding, not a productization conclusion.

## 17. No-engagement baseline

No engagement costs customer and seller $0, recovers $0, leaves the entire $104,002.80 recoverable value residual, and creates no custom ownership. It is a neutral baseline: every active motion must justify itself against it.

## 18. Which motions are dominated?

Chapter 19 does not claim strict dominance. The qualitative access, ownership, support, and relationship dimensions are not sufficiently interchangeable for a safe Pareto declaration. Formal RFP is clearly weak under the closed-access scenario, but that is conditional infeasibility—not a universal ranking.

## 19. Which motions are conditional?

* Weak buyer access can favor partner-led acquisition, subject to channel cost and technical access.
* High incumbent coverage can favor configure/buy, subject to residual and vendor dependency.
* Strong sponsorship plus bounded scope can favor pilot-first.
* An existing path improves procurement mechanics without guaranteeing buyer or technical access.
* Closed access makes broad custom infeasible.
* A narrow post-configuration residual can justify a read-only edge.

## 20. What happened to the `POOR TARGET CUSTOMER` hypothesis?

Chapter 19 status: **CONDITIONAL**. Engagement-motion variation materially changed access feasibility, acquisition effort, seller contribution, elapsed cycle, and throughput. Some motions pass target viability and others fail. This is explicitly **not** Chapter 20's final verdict.

## 21. What Chapter 19 demonstrates

The same business problem can run through different acquisition, procurement, governance, delivery, support, throughput, and economic machines. Cheapest, highest contribution, shortest cycle, or highest coverage is never treated alone as “best.”

## 22. What remains for the capstone

Chapter 20 will need to synthesize, without recalculation: (1) mixed project/target gate outcomes; (2) the closed-access hard constraint and feasible fallback ladder; (3) customer value, price, payback, and residual by motion; (4) seller acquisition, delivery, support, and contribution; (5) elapsed-cycle and capacity effects; (6) governance work that disappears versus shifts; (7) relationship and support ownership; (8) within-account versus cross-government repeatability; and (9) the no-engagement baseline. Chapter 19 defines no capstone precedence or final customer verdict.

### Evidence-precedence map

| Fact | Establishing chapters |
|---|---|
| Formal RFP economics | 4 / 15 |
| Pilot economics | 5 / 15 |
| Read-only surface | 6 / 12 / 13 |
| Configuration residual | 7 / 14 |
| Contract-size economics | 8 / 9 |
| Partner motion | 10 / 15 |
| Existing path | 11 / 15 |
| Governance attribution | 12 |
| Access feasibility | 13 |
| Incumbent alternative | 14 |
| Throughput | 16 |
| Repeatability | 17 / 18 |
