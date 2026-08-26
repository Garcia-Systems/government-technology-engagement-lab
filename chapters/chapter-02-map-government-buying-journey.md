# Chapter 2 — Map the Government Buying Journey

> **Fiction notice:** James River County Permitting Department and every stage, hour, duration, approval, and path below are fictional educational modeling. They do not describe a real locality or procurement procedure.

## 1. “Nine months” hides the mechanism

Chapter 0 inherited a nine-month sales cycle and 192 solutions/sales hours. Chapter 1 used those `MODELED ASSUMPTION`s as target-attractiveness reasons, while keeping a viable project separate from a poor target. A single duration, however, cannot explain what work happens between identifying an opportunity and authorization. Chapter 2 opens that block without changing the baseline verdict.

## 2. What is an engagement journey?

An engagement journey is an identified, evidence-labeled, ordered collection of stages attached to an engagement motion. Each reusable stage records its identity, purpose, sequence, presence (`required` in this journey), active effort, elapsed duration, responsible work category, stage type, and assumptions. A journey may contain a different subset or arrangement later; Chapter 2 does not implement those later motions.

```text
PROSPECT
   ↓
SPONSOR
   ↓
DISCOVERY
   ↓
TECHNICAL VALIDATION
   ↓
SECURITY / ACCESS
   ↓
PROCUREMENT
   ↓
PROPOSAL
   ↓
CONTRACT
   ↓
IMPLEMENTATION APPROVAL
   ↓
ACCEPTANCE
```

## 3. Effort versus elapsed time

Stage existence, active effort, and elapsed duration are independent properties. The executable uses this distinction:

```text
ACTIVE EFFORT
      ≠
ELAPSED TIME

18 hours of work
inside
45 calendar days

are different constraints
```

`EFFORT` is modeled human work consumed. `ELAPSED CYCLE` is modeled calendar time before authorization or closure. The difference is waiting and scheduling, **not hidden full-time labor**, and elapsed time is never converted into labor dollars.

## 4. The fictional baseline journey

The fixture allocates exactly **192 hours** and **270 modeled days** across ten sequential stages. It adopts **30 days per modeled month**, so 270 days / 30 = **9 modeled months**. Both the sequential rule and 30-day convention are `MODELED ASSUMPTION`s for internal reconciliation—not real procurement conventions. The original cookbook supplied only totals; therefore the entire stage-level decomposition is new `MODELED ASSUMPTION`, not source-derived detail.

The journey retains `BASELINE_COOKBOOK_MOTION`. Deterministic sums are `OBSERVED LAB RESULT`s given the fictional allocations. The reusable stage and journey records are `OBSERVED IMPLEMENTATION STRUCTURE`.

## 5. Stage-by-stage walkthrough

| # | Stage | Purpose | Active effort | Elapsed | Responsible work | Type |
|---:|---|---|---:|---:|---|---|
| 1 | Prospect | initial qualification | 10 h | 14 d | Sales | Access |
| 2 | Sponsor | establish internal sponsorship | 14 h | 21 d | Customer sponsor | Access |
| 3 | Discovery | understand workflow and boundary | 30 h | 30 d | Solutions | Discovery |
| 4 | Technical validation | validate bounded feasibility | 28 h | 35 d | Engineering | Technical |
| 5 | Security / access review | review high-level constraints | 24 h | 35 d | Security / governance | Governance |
| 6 | Procurement path | determine a generic authorization route | 18 h | 45 d | Procurement | Procurement |
| 7 | Proposal | prepare and revise a proposal | 22 h | 25 d | Sales | Commercial |
| 8 | Contract | resolve the fictional agreement | 26 h | 40 d | Legal / contracts | Contracting |
| 9 | Implementation approval | authorize implementation | 12 h | 15 d | Customer IT | Approval |
| 10 | Acceptance | close the buying journey and hand off | 8 h | 10 d | Customer sponsor | Acceptance |

Every row is inspectable in `baseline_journey.json`. “Security / access review” is only a stage allocation; it is not the detailed governance model reserved for later work. “Procurement path” names no vehicle and asserts no real procedure.

## 6. Where the active work occurs

The summary groups hours by the stage's single Chapter 2 work category and by stage type. These categories explain burden; they are not stakeholder topology. Discovery is the highest-effort stage at **30 hours**. Category and type totals each reconcile to 192 hours. No arbitrary friction weight or composite journey score exists.

## 7. Where the calendar time occurs

The baseline is deliberately sequential, so total elapsed duration is the sum of stage elapsed days. Procurement path is the longest stage at **45 modeled days**, despite only **18 active hours**. Contract takes 40 days and 26 hours. Those examples make waiting and work visible without treating every elapsed hour as labor. Dependency graphs, overlap, and critical-path scheduling are intentionally absent.

## 8. Why stages should remain visible

A monolithic “sales cycle” obscures whether burden comes from access, discovery, technical validation, governance, procurement, commercial work, contracting, approval, or acceptance. Visible stages let later chapters vary composition while preserving a substantially similar technical problem. The model permits subsets, but it does not claim that any particular stage can be omitted in a real purchase.

## 9. A simplified-path sensitivity

`SIMPLIFIED_APPROVAL_PATH` is a small `SENSITIVITY ASSUMPTION`: it omits the separately prepared `PROPOSAL` stage while leaving the underlying project and all other baseline stages unchanged. The result is **170 hours** and **245 modeled days**, compared with 192 hours and 270 days. This generic hypothetical shows only:

```text
same underlying project
        +
different journey composition
        =
different effort and/or elapsed cycle
```

It is not an existing contract vehicle, formal RFP, pilot, market verdict, or factual procurement recommendation.

## 10. Connecting the journey to target attractiveness

Chapter 1's target reasons remain intact. `HIGH_SOLUTIONS_EFFORT` now traces to `journey.total_effort_hours = 192`; `LONG_SALES_CYCLE` traces to `journey.total_elapsed_days = 270`, or nine modeled months under the fixture convention. The deterministic traces do not convert qualitative findings into a score. Procurement difficulty, weak buyer access, and stakeholder friction remain partly qualitative pending later evidence.

The invariant remains:

```text
PROJECT VIABILITY: PASS
TARGET VIABILITY: FAIL
VERDICT: POOR TARGET CUSTOMER
```

## 11. Running the lab

```bash
python -m government_engagement_lab journey
python -m government_engagement_lab journey-summary
python -m government_engagement_lab journey-scenarios
pytest
```

`journey` prints every stage and the effort/time distinction. `journey-summary` exposes reconciled burden categories and extremes. `journey-scenarios` compares the unchanged baseline with the one omission sensitivity.

## 12. What Chapter 2 demonstrates

It demonstrates `OBSERVED IMPLEMENTATION STRUCTURE`: immutable stage and journey records, fixture-backed composition, deterministic sequential sums, burden summaries, and stage omission. Given the fictional assumptions, the program produces 192 hours and 270 days (`OBSERVED LAB RESULT`). It explains mechanisms beneath two Chapter 1 target findings without changing the gate classification.

## 13. What Chapter 2 does not yet explain

It does not establish real buying behavior, role authority, decision makers, influencers, blockers, security governance, real procurement paths, RFP or pilot economics, contract vehicles, acquisition cost, capacity, throughput, or repeatability. It makes no final market verdict and implements no Chapter 3-or-later engagement motion.

## 14. Why stakeholder topology comes next

A work category says where modeled effort occurs, not who decides, influences, blocks, owns risk, or supplies evidence. Chapter 3 can add that topology without forcing it into this compact decomposition. Until then, the journey locates work and calendar delay but cannot explain the relationships that create them.
