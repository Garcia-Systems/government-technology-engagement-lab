# Chapter 6 — Read-Only Before Write Access

All people, systems, rules, prices, and results are a **fictional educational model**. This experiment retains Chapter 5's paid-pilot frame and changes technical authority.

## 1. Why technical authority affects the engagement
Authority creates failure modes, approvals, and support obligations. The test is whether reduced authority preserves enough value—not whether read-only is inherently better.

## 2. Read is not write
`EXPORT_ONLY` and `READ_ONLY_API` cannot mutate source state; `WRITE_NON_AUTHORITATIVE` writes outside the system of record; `WRITE_AUTHORITATIVE` can change it. Consequential writes can affect workflow outcomes. Chapter 6 implements only `EXPORT_ONLY`.

## 3. The broader integration surface
`WRITE_CAPABLE_INTEGRATION` is modeled comparison data, never executed. It assumes elevated credentials, consequential updates, rollback, conflict handling, and wider change control (`MODELED ALTERNATIVE ASSUMPTION`).

## 4. The read-only alternative
`READ_ONLY_REPORTING_EDGE` ingests an approved export, validates, normalizes, reconciles, reports, and surfaces exceptions. It retains Chapter 5's sponsor, contract shape, paid price, procurement/legal participation, and labor rates.

## 5. Technical boundary
```text
AUTHORITATIVE SYSTEM
        | approved read/export
        v
   VALIDATION
        v
 NORMALIZATION
        v
RECONCILIATION ------> EXCEPTIONS
        v
 INTERNAL VIEW

NO WRITE-BACK PATH
```
Status writes, corrections, workflow/document mutation, and consequential decisions are prohibited. No source-update function exists (`OBSERVED IMPLEMENTATION STRUCTURE`).

## 6. Synthetic implementation
Eight fixture rows produce eight normalized outputs, four exception rows (two mismatches, a duplicate, and an invalid row), and one duplicate (`OBSERVED LAB RESULT`). This is not a permitting product.

## 7. Provenance and traceability
Every output retains export ID, source row ID/status, normalized status, fixed timestamp, reason, and exception flag. Tests verify repeatability and unchanged caller input.

## 8. What value remains recoverable
Read-only models 55% of the $104,002.80 opportunity: **$57,201.54** (`MODELED ASSUMPTION`). It addresses lookup, reports, reconciliation, and duplicate visibility.

## 9. What value is lost
The excluded 45% represents authoritative updates, correction-state mutation, and full workflow automation. This fraction is transparent fiction, not measured benefit.

## 10. Governance surface
Read-only removes modeled write approval, elevated write credentials, mutation approval, broad change control, and rollback planning. Retention approval and audit requirements remain. The write baseline requires all represented considerations. These are flags and reasons, never a weighted score.

```text
MORE TECHNICAL AUTHORITY -> MORE FAILURE MODES -> MORE APPROVAL / SUPPORT SURFACE
LESS TECHNICAL AUTHORITY -> LESS VALUE CAPTURE? -> TRADEOFF
```

## 11. Stakeholder effects
Chapter 3 identities are reused. IT and Security/Governance work narrows; Sponsor, users, Procurement, Legal/Contracts, and Accessibility remain.

## 12. Buying-journey effects
Chapter 2 types are reused. Technical validation changes from 10 hours/10 days to 6/6; security review from 8/12 to 5/7; implementation from 20 to 14 elapsed days. Commercial stages remain (`MODELED ASSUMPTION`).

## 13. Customer economics
Price plus support is **$40,000**; net recoverable value is **$17,201.54**; bounded price/value payback is about **7.55 months**.

## 14. Seller economics
Ten explicit work categories total **110 engineering hours**. Chapter 4's unchanged $110 rate yields **$12,100** delivery labor. Acquisition uses the same existing rates.

## 15. Write-capable versus read-only comparison
| Surface | Value | Engineering | Governance | Executed? | Verdict |
|---|---:|---:|---|---|---|
| Write-capable | $104,002.80 | 240 h | broader | modeled only | POOR TARGET CUSTOMER |
| Read-only edge | $57,201.54 | 110 h | narrower | synthetic export | PILOT-FIRST TARGET |

## 16. Sensitivity: value too low
At 15% capture (**$15,600.42**), cost exceeds value and the result is `NO DEAL` (`SENSITIVITY ASSUMPTION`). Lower risk cannot rescue insufficient value.

## 17. Sensitivity: access still difficult
Authority remains `EXPORT_ONLY`, but unreliable approval adds 16 hours and 40 days to reviews (`SENSITIVITY ASSUMPTION`). The result is `NO DEAL`: read-only is not magically easy.

## 18. Does lower authority change the verdict?
Yes under the main fictional inputs: write-capable is `POOR TARGET CUSTOMER`; read-only is `PILOT-FIRST TARGET`, due to lower engineering, acquisition, governance, and support burden.

## 19. What Chapter 6 demonstrates
Technical authority can change governance and economics for the same problem and similar motion. This further **weakens the cookbook hypothesis under bounded assumptions**; sensitivities preserve falsifiability.

## 20. What Chapter 6 does not prove
It does not prove access, 55% capture, complete mappings, expansion, or universal read-only preference. It implements neither detailed security controls nor authoritative writes.

## 21. Why configuration-first comes next
Whether existing configuration preserves value with less custom work remains unresolved for Chapter 7. **No configuration-first behavior is implemented here.**
