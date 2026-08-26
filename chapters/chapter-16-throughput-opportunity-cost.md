# Chapter 16 — Throughput and Opportunity Cost

## 1. A profitable deal can still clog the pipeline

Chapter 15 measured the cost of winning one deal. This chapter asks what the same fictional seller team can carry. An engagement can have positive won-deal contribution and still displace a more productive portfolio. Every staffing and arrival input here is a `MODELED ASSUMPTION`, not a benchmark.

## 2. Acquisition effort versus elapsed cycle

Three quantities remain separate: **active work hours**, **elapsed opportunity duration**, and **concurrent pipeline load**. Formal RFP's 192 hours over 270 modeled days are lumpy stage-period buckets, not 192/270 hours per day. Elapsed days are never multiplied by a labor rate.

## 3. The fictional solutions organization

The fixture contains one solutions engineer (160 monthly work hours, 45%/72 hours available to acquisition), one seller/account lead (25%/40 hours), and shared engineering support (10%/16 hours). The corresponding non-acquisition reserves are 88, 120, and 144 hours. Total acquisition capacity is **128 hours per modeled 30-day period**. These compact roles reuse Chapter 15's seller-side frame but are not recommended ratios.

## 4. Available acquisition capacity

```text
MODELED MONTHLY WORK HOURS
− DELIVERY / ADMIN / INTERNAL RESERVE
= ACQUISITION CAPACITY
```

The identities reconcile for every role. Capacity is shared in this intentionally simple lab; it is not an assertion that real roles are interchangeable.

## 5. Modeling an active opportunity

Each synthetic opportunity records identifier, motion, arrival period, period workload, base elapsed days, expected implementation revenue, acquisition-adjusted contribution, status, and evidence. It is a reusable experiment record, not a CRM or forecast.

## 6. Stage-based workload

The fixture turns Chapter 15 seller-owned acquisition work into explicit, nonuniform monthly buckets. Formal RFP is `24/28/30/26/20/18/18/16/12`; pilot is `24/22/12`; partner-led is `16/15/14/12/10/9/7/5/3`; existing path is `22/24/22/18/16/12`. Each profile exactly reconciles to Chapter 15. The allocations are `MODELED ASSUMPTION`s; their reconciliation and reuse are `OBSERVED IMPLEMENTATION STRUCTURE`.

## 7. Concurrency

Eight possible opportunities arrive in periods 1–8 for every single-motion comparison. Active count is descriptive; workload demand is controlling. Five opportunities can be below capacity in one motion and above it in another.

## 8. Long-cycle carrying load

No extra carrying-hour penalty is added. Long cycles still keep opportunities open: nine-bucket Formal RFP and partner motions average more than five active opportunities during the year, versus two for the pilot. This exposes WIP congestion without inventing calendar-time dollars.

```text
SELLER CAPACITY
      |
      v
+-------------------+
| ACTIVE OPPORTUNITY|
| WORK DEMAND       |
+-------------------+
      |
      v
CAPACITY REMAINING
      |
  +---+---+
  |       |
  v       v
NEW     NO ROOM
DEAL    FOR DEAL
```

## 9. Formal RFP throughput

Formal RFP completes **4** of eight arrivals in the modeled year, averages **5.17** active opportunities, has **5** overloaded periods, and exposes 98 aggregate deferred-hour observations. FIFO deferral extends average completed cycle from nine to **9.875 periods**. Per-deal acquisition-adjusted contribution is **-$60**; annualized contribution is **-$240** (`OBSERVED LAB RESULT`).

## 10. Pilot throughput

The cooperative pilot completes **8**, averages **2.00** active, and has no overloaded period or deferral. Its three-period cycle is unchanged. Contribution is **$13,310 per deal** and **$106,480 annualized**.

## 11. Partner-led throughput

Partner-led seller work is only the seller-borne **91 hours** from Chapter 15. It completes **4** because nine elapsed workload periods keep later arrivals open beyond year end, despite no overload. Contribution is **$11,205 per deal** and **$44,820 annualized**. Shifting work helps capacity but lower retained revenue and elapsed WIP still matter.

## 12. Existing-path throughput

Existing path completes **7**, averages **3.92** active, and has no overload. Procurement simplification retains 114 hours but shortens the profile to six periods. Contribution is **$7,530 per deal** and **$52,710 annualized**.

## 13. Contribution per deal versus contribution per year

```text
PER-DEAL ECONOMICS
        ≠
ANNUAL BUSINESS ECONOMICS

CONTRIBUTION / DEAL
        ×
COMPLETED SUCCESSFUL DEALS / YEAR
        =
ANNUALIZED CONTRIBUTION
```

This is simplified seller contribution, not accounting profit. The pilot illustrates that a bounded, lower-revenue deal can beat larger-revenue motions through both healthy per-deal contribution and throughput.

## 14. Opportunity cost

Opportunity cost is **alternative feasible portfolio contribution not realized because capacity was occupied**. Formal-RFP-heavy versus pilot-first produces modeled displaced contribution of **$106,720**: $106,480 minus -$240. No arbitrary value is assigned to a day or month.

## 15. Mixed portfolio

One Formal RFP, two pilots, and two existing-path opportunities all complete in year one, with no overload and **$41,620 annualized contribution**. It is a deterministic illustration, not an optimizer or proof of an ideal mix.

## 16. Sensitivity: more capacity

Adding a second 72-hour solutions resource (`SENSITIVITY ASSUMPTION`) raises capacity to 200 hours and removes all Formal-RFP overload and deferral. It still completes four in-year deals because the nine-period elapsed profile and arrival dates remain. Annualized contribution remains -$240. Hiring resolves modeled resource scarcity, not weak per-deal economics or the calendar boundary.

## 17. Sensitivity: lost long-cycle opportunity

One Formal RFP is deterministically lost. Its 192 acquisition hours and **$20,640 acquisition cost** remain, while implementation revenue becomes zero. The portfolio keeps the same capacity use and yields **-$20,820** in-year contribution. This is not a probability model.

## 18. When cycle becomes a commercial problem

Cycle is a problem when its open workload combines with arrivals to constrain starts, defer work, extend completion, or leave otherwise valuable engagements outside the year. There is deliberately no rule such as “over 180 days is poor.” A long, low-touch, high-contribution motion can remain attractive when capacity is ample.

## 19. What Chapter 16 demonstrates

Same seller team plus different motions produces different throughput. Raw opportunity count cannot describe load; acquisition intensity can crowd out work; elapsed duration independently raises WIP; and contribution per deal does not determine annual contribution. Pipeline throughput affects `TARGET_ATTRACTIVENESS`, not technical/project viability. A viable project and even positive per-deal economics can therefore remain commercially conditional.

## 20. What Chapter 16 does not prove

It proves no universal staffing ratio, WIP limit, arrival rate, win probability, capacity score, or government-market norm. All primary opportunities are treated as successful except the named sensitivity. It does not monetize calendar time, recommend hiring, optimize a portfolio, or change Chapters 0–15 fixtures.

## 21. Why repeatability across departments comes next

This lab can count throughput only for the specified fictional arrivals and motions. Whether delivery assets, discovery, configuration, governance artifacts, and learning transfer to another department remains unresolved. That is the question for Chapter 17; no repeatability-across-departments functionality is implemented here.
