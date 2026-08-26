# Chapter 13 — Closed Integration Scenario

## 1. When access is the real constraint

This chapter is a wholly fictional educational experiment about the James River County Permitting Department and the fictional **CivicFlow Permitting Suite**. It makes no claim about a real government or product. Its central rule is: **technical access is a hard constraint**.

## 2. Valuable problem does not guarantee feasible integration

```text
VALUABLE PROBLEM + WILLING CUSTOMER + GOOD MOTION
+ NO RESPONSIBLE ACCESS TO THE REQUIRED SYSTEM
= INFEASIBLE ORIGINAL PROJECT
```

Chapter 1's precedence remains intact: technical-feasibility failure makes project viability fail and the original project `NO DEAL`. A materially different intervention receives its own assessment; its feasibility does not retroactively repair the preferred intervention.

## 3. Required access versus available access

Every intervention declares acceptable access modes, write and automation needs, required fields, and minimum freshness. The engine compares those requirements with actual modeled capabilities and returns `FEASIBLE`, `FEASIBLE_WITH_LIMITATIONS`, or `NOT_FEASIBLE`, plus explicit reasons. It does not calculate a score.

## 4. The fictional closed legacy system

The preferred broad integration requires a supported read/write interface. The modeled incumbent condition has no supported API, direct database access, or write interface. An approved scheduled export exists in the baseline, creating a reduced-scope decision rather than permission to invent a write route. These are `MODELED ASSUMPTION`s, not vendor facts.

## 5. Why unsupported workarounds are not acceptable

```text
NO SUPPORTED ACCESS
        ≠
TRY HARDER TO BYPASS IT
```

The implementation contains no protected-system scraping, shared credentials, unauthorized database access, reverse-engineered private endpoint, control-bypassing browser automation, hidden write path, or unsupported mutation. The choices are a supported alternative or `NO DEAL`.

## 6. The access-capability model

The closed-access fixture uses `FULL_SUPPORTED_API`, `READ_ONLY_API`, `APPROVED_EXPORT`, `MANUAL_EXPORT`, `VENDOR_MANAGED_INTERFACE`, and `NO_SUPPORTED_ACCESS`. Each capability also records reliability, frequency, write authority, completeness, automation compatibility, vendor support, evidence, fields, and limitations. Incumbent control is a dependency—not an accusation.

## 7. Scenario: write path unavailable

Broad write integration explicitly requires supported write authority. With export-only access, it deterministically fails for `REQUIRED_WRITE_ACCESS_UNAVAILABLE`. Its full delivery economics are not treated as if the project could proceed.

## 8. Fallback: approved read-only export

The approved daily export supplies the four fields needed by a read-only reporting and reconciliation edge. The edge cannot write to the authoritative source. It captures 58% of baseline recoverable value in its explicit alternative scenario, retains read-only Chapter 12 governance work, and produces a derived `NARROW CUSTOM EDGE` verdict.

## 9. Fallback: manual export

The manual scenario requires an authorized staff member to export a file weekly. It captures 31% of recoverable value and has explicit support and process burden. Its 31% value capture leaves first-year customer value below modeled cost, so customer economics fail and the result is `NO DEAL`—even though the narrowly required fields are present. The 55 engineering support hours remain separately visible.

```text
AUTHORIZED STAFF EXPORT
        ↓
APPROVED FILE LOCATION
        ↓
NORMALIZE → RECONCILE → REPORT
        ↓
STAFF REVIEWS EXCEPTIONS
```

## 10. Fallback: configuration only

When external access is unavailable but native configuration is modeled as available, Chapter 7's capability assessment and economics are reused rather than recreated. The responsible posture is `BUY / CONFIGURE`.

## 11. Hard stop: no usable access

When no supported external access, adequate native configuration, or approved export exists, no fallback is selected. Project viability fails, target viability is not evaluated, economics are not applicable, and the verdict is `NO DEAL`.

## 12. Data freshness

Freshness is categorical: `REAL_TIME`, `DAILY`, `WEEKLY`, or `ON_DEMAND_MANUAL`. Daily scheduled data can support modeled reporting; weekly/manual data cannot silently satisfy an operational real-time requirement. No weighted freshness score exists.

## 13. Data completeness

Completeness is `COMPLETE`, `PARTIAL`, or `INSUFFICIENT`, supplemented by explicit field sets. Missing any required field yields `REQUIRED_FIELDS_MISSING`; merely having a file is not feasibility.

## 14. Human-assisted economics

The manual sensitivity assumes 52 exports per year and 30 staff minutes each, producing 26 annual customer handling hours. It separately exposes seller support, freshness limits, and reduced value capture. These are `SENSITIVITY ASSUMPTION`s, not observed operational burdens.

## 15. Governance implications

The approved-export edge reuses Chapter 12's read-only surface. Manual handling adds authorized handling, transfer controls, retention, cleanup/provenance expectations, and staff review. Simpler access does not mean zero governance.

## 16. Feasibility versus economics

```text
ACCESS FAILS                         → TECHNICAL FEASIBILITY FAIL
ACCESS WORKS, VALUE TOO LOW          → CUSTOMER ECONOMICS FAIL
ACCESS WORKS, SUPPORT TOO EXPENSIVE  → DELIVERY / SUPPORT FAIL
PROJECT WORKS, ACQUISITION FAILS     → POOR TARGET CUSTOMER
```

The first failure suppresses normal project economics. The other failures occur only after an alternative passes its own access test.

## 17. Choosing the responsible fallback

For this lab—not as universal truth—the documented precedence is native configuration, approved read-only access, approved automated export, approved manual export, human-assisted workflow, then no deal.

```text
PREFERRED CUSTOM INTEGRATION
          |
          v
REQUIRED ACCESS AVAILABLE?
      /          \
    YES           NO
     |             |
     v             v
CONTINUE      EVALUATE FALLBACKS
                  |
        +---------+---------+
        |         |         |
        v         v         v
   CONFIGURE   READ ONLY   MANUAL
        |         |         |
        +---------+---------+
                  |
                  v
             VALUE ENOUGH?
              /       \
            YES        NO
             |          |
             v          v
          PROCEED     NO DEAL
```

Selection is deterministic and never invents unsupported incumbent capability.

## 18. When `NO DEAL` is the correct answer

`NO DEAL` applies to the original write project and to any overall scenario with no responsible alternative, failed customer economics, or unsustainable delivery/support. Seller enthusiasm does not override a gate.

## 19. What Chapter 13 demonstrates

Given fictional inputs, the engine rejects unsupported writes, can preserve a narrow read-only edge, prices manual dependency, reuses native configuration, and stops when no usable access exists. These classifications are `OBSERVED LAB RESULT`s; absence of an authoritative write code path is `OBSERVED IMPLEMENTATION STRUCTURE`.

## 20. What Chapter 13 does not prove

It does not prove any real interface is closed, establish general freshness needs, recommend bypass techniques, or show that a government category is attractive or unattractive. Closed integration **clarifies** the cookbook hypothesis: target conditions matter only after the technical project is possible.

## 21. Why the incumbent-vendor alternative comes next

An incumbent may control a supported interface or native capability, but Chapter 13 does not evaluate an incumbent-vendor commercial alternative. That unresolved question belongs to Chapter 14, which is intentionally not implemented here.
