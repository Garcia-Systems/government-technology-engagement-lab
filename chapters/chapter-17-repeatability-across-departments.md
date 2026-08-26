# Chapter 17 — Repeatability Across Departments

## 1. The second department is the real reuse test

Chapter 17 keeps the experiment inside wholly fictional James River County. The source is the **James River County Permitting Department**; the target is the equally fictional **James River County Inspections Department**. Nothing models a real locality. The reference motion is `COOPERATIVE_PAID_PILOT`, selected because Chapter 5 found a bounded paid project plausible without importing the unattractive Formal RFP burden.

```text
FIRST DEPARTMENT
      |
      +--> CODE
      +--> TESTS
      +--> DOCUMENTS
      +--> PROCUREMENT PATH
      +--> CUSTOMER KNOWLEDGE
      |
      v
SECOND DEPARTMENT
      |
      +--> WHAT REUSES?
      +--> WHAT ADAPTS?
      +--> WHAT RESTARTS?
```

## 2. Reusable software is not a reusable engagement

`REUSABLE SOFTWARE ≠ REUSABLE ENGAGEMENT`. The implementation therefore has nine independent dimensions, explicit artifacts, and `REUSE_AS_IS`, `ADAPT`, `REBUILD`, and `NOT_APPLICABLE` states—never a reuse score.

```text
ENGINEERING REUSE
        ≠
SALES REUSE
        ≠
PROCUREMENT REUSE
        ≠
APPROVAL REUSE
```

## 3. Meet the fictional second department

The bounded workflow is **Inspection Request → Scheduling → Assignment → Site Visit → Findings → Correction → Reinspection → Closure → Reporting**. It differs in users, mobile findings, scheduling, its reinspection loop, budget owner, and department review. These are `MODELED ASSUMPTION`s.

## 4. Technical reuse

Provenance, normalization, and test utilities reuse as-is. The report shell, ingestion framework, status vocabulary, and acceptance fixtures adapt. Department mappings rebuild. The explicit model produces **138 greenfield engineering hours versus 53 with reuse: 85 saved** (`OBSERVED LAB RESULT`).

## 5. Discovery reuse

Interview, burden, and access templates travel, but the interviews and answers do not. Their 30-hour first-build/reference effort becomes 18 hours, not zero. “We already know government” is not evidence.

## 6. Sales-motion reuse

County credibility and a sponsor introduction reduce access work, but the permitting sponsor cannot authorize inspections. Qualification, sponsor, and budget-owner work remain department-specific.

## 7. Procurement reuse

The same fictional purchasing path and master terms reuse, while scope, budget, work order, departmental authorization, and acceptance repeat. Same government does not mean free procurement.

## 8. Governance-document reuse versus approval reuse

The architecture, data-flow, and control narrative adapts from 18 to 7 hours. Security/accessibility approval rebuilds at 16 hours. **Document reuse reduces seller preparation; it does not grant customer approval.**

## 9. Support reuse

Runtime, monitoring, deployment shell, and playbook are shared. Mappings, credentials, report definitions, exceptions, and workflow rules remain specific. The marginal support model requires 14 hours and costs $980; the second department is neither free nor an entirely separate runtime.

## 10. First department versus second department

| Dimension | Department 1 | Department 2 |
|---|---:|---:|
| Engineering hours | 152 | 53 |
| Discovery hours | 30 | 18 |
| Acquisition hours | 72 | 42 |
| Governance hours | 34 | 23 |
| Elapsed cycle | 120 days | 105 days |
| Support hours | 32 | 14 |
| Implementation price | $42,000 | $42,000 |
| Contribution | $13,970 | $33,605 |

## 11. Marginal second-department economics

The first engagement carries framework, harness, documentation, and account setup investment. Chapter 17 does not rewrite its contribution. For Department 2, $42,000 implementation plus $6,000 support faces $6,390 delivery, $3,570 acquisition, $1,955 governance, $980 support, and $1,500 other direct cost, leaving **$33,605** marginal contribution. (The executable figure is authoritative if inputs change.) Customer first-year cost is $48,000 against $60,000 modeled recoverable value. All amounts are fictional marginal analysis, not product economics or a benchmark.

## 12. Scenario: technical reuse, commercial reset

Scenario B preserves 53 engineering hours but expands discovery, sponsor, budget, and approval work. It demonstrates that engineering reuse can coexist with weak target attractiveness.

## 13. Scenario: commercial reuse, technical variation

Scenario C lowers account/procurement work while a unique adapter and changed workflow add 44 engineering hours. An easier sale can remain expensive delivery.

## 14. Scenario: strong repeatability

Scenario D reduces explicit work across technical, discovery, commercial, governance, and support dimensions, but retains mapping, review, acceptance, and support work. It is favorable—not perfect.

## 15. What actually travels?

The canonical model, report shell, harness, purchasing path, security-document structure, and support infrastructure travel. Department mappings, workflow discovery, authorization, and security approval restart or materially adapt. Findings make those mechanisms visible rather than averaging them.

## 16. Repeatable project versus product

The baseline supports **`REPEATABLE PROJECT`** because engineering, acquisition, governance preparation, and support all improve while bounded department delivery remains. `REPEATABLE PROJECT ≠ PRODUCT`: discovery, mapping, configuration, acceptance, and support variation remain. No product classification or product economics is introduced.

## 17. What Chapter 17 demonstrates

Given modeled inputs, a second department can have better marginal economics and a more promising target result. It clarifies `POOR TARGET CUSTOMER`: the verdict is motion- and account-context-dependent, but code reuse alone cannot overturn it.

## 18. What Chapter 17 does not prove

One second department does not prove a repeatable market, public-sector reuse rate, universal procurement shortcut, transferable approval, or product. Artifact structure is `OBSERVED IMPLEMENTATION STRUCTURE`; calculated savings are `OBSERVED LAB RESULT`; scenarios are `SENSITIVITY ASSUMPTION`s.

## 19. Why a different government comes next

This chapter deliberately holds locality context constant. Whether purchasing paths, trust, governance work, and artifacts transfer to another government remains unresolved. Chapter 18 functionality is not implemented here.
