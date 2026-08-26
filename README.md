# Government Technology Engagement Lab

> An executable laboratory testing whether government technology opportunities are poor targets inherently or because of procurement, acquisition, governance, and engagement motion.

## Fiction and evidence notice

**James River County Permitting Department is wholly fictional.** It is not James City County, Williamsburg, York County, Newport News, any actual Virginia locality, or any real government customer. Every system, workflow, procurement rule, staffing figure, price, labor input, security requirement, approval process, contract assumption, and financial assumption in Chapter 0 is fictional educational modeling unless explicitly stated otherwise.

The lab uses a controlled vocabulary:

- `MODELED ASSUMPTION`: a fictional input or inherited cookbook outcome;
- `OBSERVED LAB RESULT`: a deterministic program result *given those fictional inputs*, not real-world evidence;
- `OBSERVED IMPLEMENTATION STRUCTURE`: a fact about this repository's implementation;
- `SENSITIVITY ASSUMPTION`: an input varied to inspect sensitivity; and
- `MODELED ALTERNATIVE ASSUMPTION`: a fictional alternative to a baseline input.

Only the first two labels are applied to Chapter 0 data and results. The others establish evidence discipline for later work.

## What this repository tests

The fictional cookbook returned `POOR TARGET CUSTOMER`. This lab asks whether that verdict is intrinsic to a customer category or instead depends on the engagement motion. It tries to **falsify**, not confirm, the verdict. Chapter 0 reconstructs the reference case and turns its mechanisms into an executable hypothesis; it does not test alternatives yet.

The important separations are:

```text
PROBLEM ATTRACTIVENESS       TECHNICAL FEASIBILITY
CUSTOMER ECONOMICS           DELIVERY ECONOMICS
SUPPORT ECONOMICS            TARGET ATTRACTIVENESS
ENGAGEMENT MOTION

GOOD PROJECT ≠ GOOD TARGET CUSTOMER
POOR TARGET CUSTOMER ≠ NO DEAL
```

## What it does not claim

This repository does **not** claim that real governments behave like this fictional department, that the fixtures contain actual procurement requirements or sales cycles, that prices reflect the government market, or that security/accessibility assumptions describe a real locality. It does not conclude that government is inherently good or bad as a technology market.

## Experimental progression

Executable labs challenge earlier modeled verdicts rather than arranging evidence to confirm them:

```text
MULTI-LOCATION RESTAURANT  PROMISING      → executable investigation → INVESTIGATE
CONSTRUCTION / TRADES      PROMISING      → executable investigation → REPEATABLE PROJECT / VALIDATE
MULTI-LOCATION RETAIL      BUY / CONFIGURE → executable investigation → INVESTIGATE
LOCAL GOVERNMENT           POOR TARGET CUSTOMER → executable engagement experiment → ???
```

This repository currently contains **Chapters 0–8 only**. Chapter 8 implements only the small-departmental contract-size experiment; Chapter 9 and later experiments remain unimplemented.

## Architecture

- `models.py` contains immutable typed domain records, including reusable engagement stages and journeys.
- `fixtures/*.json` contains the fictional baseline, journey decomposition, and deliberately small scenario data.
- `economics.py` performs three transparent customer calculations using `Decimal`.
- `baseline.py` preserves Chapter 0; `gates.py` evaluates Chapter 1 viability; `journey.py` loads Chapter 2 journeys and calculates unweighted burden summaries; `stakeholders.py` loads, validates, and summarizes Chapter 3 topology; `formal_rfp.py` implements Chapter 4; `pilot.py` implements Chapter 5; `read_only.py` implements Chapter 6; `configuration.py` implements Chapter 7; and `small_engagement.py` implements Chapter 8's scope, acquisition-floor, support, break-even, and scenario economics.
- `evidence.py` owns the reusable evidence vocabulary; `cli.py` presents the executable chapter.
- `chapters/` explains the model as a textbook; `tests/` lock down identity, economics, evidence, and verdict mechanics.

Chapter 4 calculates a simplified acquisition-adjusted implementation contribution using explicitly fictional fully loaded internal cost rates; it is not company profit. No generic government score, procurement simulation, later experiment, database, or web application is present.

## Running the lab

Python 3.11 or newer is required. From the repository root:

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -e .
pytest
python -m government_engagement_lab baseline
python -m government_engagement_lab scenarios
python -m government_engagement_lab gates
python -m government_engagement_lab gate-scenarios
python -m government_engagement_lab journey
python -m government_engagement_lab journey-summary
python -m government_engagement_lab journey-scenarios
python -m government_engagement_lab stakeholders
python -m government_engagement_lab stakeholder-summary
python -m government_engagement_lab stakeholder-scenarios
python -m government_engagement_lab formal-rfp
python -m government_engagement_lab formal-rfp-economics
python -m government_engagement_lab formal-rfp-scenarios
python -m government_engagement_lab pilot
python -m government_engagement_lab pilot-economics
python -m government_engagement_lab pilot-scenarios
python -m government_engagement_lab compare-motions
python -m government_engagement_lab read-only
python -m government_engagement_lab read-only-economics
python -m government_engagement_lab read-only-scenarios
python -m government_engagement_lab compare-technical-surfaces
python -m government_engagement_lab configure-first
python -m government_engagement_lab configure-first-economics
python -m government_engagement_lab configure-first-scenarios
python -m government_engagement_lab residual
python -m government_engagement_lab small-engagement
python -m government_engagement_lab small-engagement-economics
python -m government_engagement_lab small-engagement-scenarios
python -m government_engagement_lab contract-size
```

The baseline command shows the modeled inputs, derived customer economics, acquisition findings, independent gates, and inherited verdict. The scenarios command shows only historical modeled cookbook outcomes. `gates` shows the Chapter 1 baseline with separate project and target viability. `gate-scenarios` compares four compact gate substitutions and then prints their mechanisms.

## Chapter 0 calculation boundary

Given the fictional assumptions, the executable computes:

```text
first-year cost = $78,000.00 + $24,000.00 = $102,000.00
first-year net recoverable value = $104,002.80 - $102,000.00 = $2,002.80
implementation-only payback = $78,000.00 / $104,002.80 × 12 ≈ 9.00 months
```

The last measure excludes annual support and is deliberately not called full first-year payback. Positive modeled customer economics, technical feasibility, and support viability coexist with a target-attractiveness failure. Thus `POOR TARGET CUSTOMER` is the hypothesis subsequent experiments must attempt to break—not a repository-wide conclusion.

## Chapter 1 gate framework

Chapter 1 makes six dimensions independently inspectable: `PROBLEM_ATTRACTIVENESS`, `TECHNICAL_FEASIBILITY`, `CUSTOMER_ECONOMICS`, `DELIVERY_ECONOMICS`, `SUPPORT_ECONOMICS`, and `TARGET_ATTRACTIVENESS`. `ENGAGEMENT_MOTION` is separate context (`BASELINE_COOKBOOK_MOTION`), not a score. Statuses are limited to `PASS`, `FAIL`, `CONDITIONAL`, and `NOT_EVALUATED`; every result carries explicit evidence-labeled reasons.

The first five gates determine project viability. The target gate separately determines target viability. Precedence is deliberately modest: a failed project is `NO DEAL`; a passing project with a failed target is `POOR TARGET CUSTOMER`; uncertainty is `INVESTIGATE`; and both passing yields the restrained `PROMISING — VALIDATE IN DISCOVERY`. There is no weighted or 0–100 opportunity score.

The customer-economics rule is a fictional `MODELED ASSUMPTION`: first-year net recoverable value must be nonnegative. It exposes recoverable annual value, implementation price, annual support, first-year cost, net value, and implementation-only payback. It is not a universal purchasing benchmark. Delivery and support remain separate inherited viability assumptions because seller labor rates and support delivery costs are absent.

The four Chapter 1 cases are: unchanged baseline (`PASS` project / `FAIL` target), unavailable required access (`FAIL` project / `NO DEAL`), reduced recoverable value (`FAIL` project / `NO DEAL`), and hypothetical improved target conditions (`PASS` / `PASS` / validate in discovery). Each changed fictional condition is a `SENSITIVITY ASSUMPTION`; each deterministic classification is an `OBSERVED LAB RESULT`. These substitutions demonstrate classification semantics only—not procurement stages, pilots, channels, security reviews, or any Chapter 2+ motion.

## Chapter 2 buying journey

Chapter 2 represents stage existence, active human effort, and elapsed calendar time separately. Ten sequential fixture-backed stages reconcile to **192 hours** and **270 modeled days**, using the explicit fictional convention **30 modeled days = one modeled month**. Thus `192 HOURS OF EFFORT ≠ 9 MONTHS OF FULL-TIME LABOR`: effort is work consumed; elapsed cycle is calendar time before authorization or closure.

The original handoff supplied only the totals. Every stage allocation and the 30-day convention is therefore a new `MODELED ASSUMPTION`, not a real procurement convention. Deterministic summaries expose effort by work category and stage type, plus the highest-effort and longest-elapsed stages; no weighted journey score is used. Chapter 1's `HIGH_SOLUTIONS_EFFORT` and `LONG_SALES_CYCLE` reasons now trace to these totals while its `PASS` project / `FAIL` target / `POOR TARGET CUSTOMER` result remains unchanged.

One narrow `SIMPLIFIED_APPROVAL_PATH` sensitivity omits `PROPOSAL`, producing 170 hours and 245 modeled days. It demonstrates composability only: it is not a contract vehicle, later engagement motion, real procedure, or market verdict.

## Chapter 3 stakeholder topology

Chapter 3 connects fictional stakeholders directly to Chapter 2 stages. Its typed role vocabulary is `DECISION_MAKER`, `INFLUENCER`, `APPROVER`, `BLOCKER`, `USER`, `TECHNICAL_GATEKEEPER`, and `SPONSOR`; its explicit relationships include reporting, approval, dependency, access control, advice, information supply, and required acceptance. Every stakeholder structure is a `MODELED ASSUMPTION`, not a real-locality fact.

Descriptive summaries count stakeholders, role assignments, stage participation, approvals, blocking paths, and technical-access dependencies without a score. Explicit findings make Chapter 1's `STAKEHOLDER_FRICTION` traceable to visible mechanisms. Authority-only sensitivities cover a strong sponsor, fragmented authority, and no sponsor while leaving legitimate controls or the underlying technical project visible. Chapter 4 reuses these stakeholder identifiers in its formal-RFP stage participation rather than duplicating the topology.


## Chapter 4 formal RFP motion

Chapter 4 is the first complete engagement-motion experiment. `FORMAL_RFP` reuses the Chapter 2 journey types and Chapter 3 stakeholder identities while making 18 fictional stages, eight lightweight proposal artifacts, responsibilities, pre-award work, and calendar delay explicit. The baseline preserves **$78,000 implementation**, **$24,000 annual support**, **522 engineering hours**, **192 acquisition hours**, and **nine modeled months**.

Seller rates are `MODELED ASSUMPTION`s for fully loaded internal cost—not wages: sales **$85/hour**, solutions **$125/hour**, and engineering **$110/hour**. Given these inputs, `OBSERVED LAB RESULT`s are **$57,420 delivery labor cost**, **$20,640 acquisition labor cost**, and **-$60 acquisition-adjusted implementation contribution**. A fictional **$10,000 minimum contribution** is a transparent lab sustainability rule, not a business benchmark. Customer economics remain independently positive by **$2,002.80**, so the derived baseline is project `PASS`, target `FAIL`, and `POOR TARGET CUSTOMER`. No weighted RFP score or win-probability expected value is used.

The sensitivities do not mutate the baseline. Halving stage effort produces 96 hours and repairs seller contribution; reducing delay leaves 192 hours and acquisition cost unchanged; increasing price to $90,000 repairs seller contribution but makes first-year customer value negative, yielding `NO DEAL`, not an assumed acceptable price. These are sensitivities, not claims that a buyer would accept them.

## Chapter 5 cooperative paid pilot

Chapter 5 keeps the fictional department and core permitting-status burden recognizable while changing the engagement motion. The $36,000, 90-day pilot is paid, bounded to one team/eight modeled users/one workflow slice, measurable, time-limited, and explicit about exclusions and handoff. Synthetic reconciliation produces deterministic operational evidence; modeled time and labor assumptions remain separate from those observations.

The baseline pilot uses 58 pre-authorization acquisition hours, 75 modeled days to authorization, and 140 engineering hours. Reusing Chapter 4's internal rates produces $15,400 delivery cost, $6,290 acquisition cost, $1,000 other direct cost, and $13,310 acquisition-adjusted contribution. The modeled customer side separates $52,000 annualized value potentially affected from both the $104,002.80 full opportunity and a $39,000 expected pilot benefit.

All seven synthetic acceptance criteria pass, producing `PILOT_ACCEPTED`; project and target viability pass and the commercial verdict is `PILOT-FIRST TARGET`. Crucially, `full_implementation_authorized` remains false and the next step is only `VALIDATE EXPANSION`. Pilot acceptance does not approve production expansion or erase procurement, contracting, security, accessibility, access, alignment, or support work.

Direct comparison shows the same fictional problem yields `POOR TARGET CUSTOMER` under `FORMAL_RFP` and `PILOT-FIRST TARGET` under `COOPERATIVE_PAID_PILOT`. Thus the cookbook hypothesis is **WEAKENED UNDER THIS FICTIONAL PILOT MOTION**—not disproved, and emphatically not evidence that government is generally a good customer. Too-small, too-broad, and weak-sponsor sensitivities each return to poor target conditions. No weighted score or real procurement rule is used.


## Chapter 6 read-only before write access

Chapter 6 holds the paid-pilot frame substantially constant and changes technical authority. Its vocabulary distinguishes `EXPORT_ONLY`, `READ_ONLY_API`, `WRITE_NON_AUTHORITATIVE`, and `WRITE_AUTHORITATIVE`. The implemented edge uses an approved synthetic export: validation → normalization → reconciliation → report/exceptions. There is no authoritative write path; every immutable output retains source provenance.

The main edge models 55% value capture (**$57,201.54**) and **110 engineering hours**. It narrows—but does not erase—IT and governance work; procurement, contracts, accessibility, sponsor, and users remain. At $36,000 plus $4,000 support, customer net recoverable value is **$17,201.54**. The 240-hour write-capable surface is comparison data only.

The main result is `PILOT-FIRST TARGET`, versus `POOR TARGET CUSTOMER` for the write comparison, further **weakening but not disproving** the cookbook hypothesis. A 15%-capture sensitivity and difficult-access sensitivity both become `NO DEAL`; read-only is neither universally preferred nor automatically easy. Chapter 7 tests the configuration-first question next.

## Chapter 7 configuration-first experiment

Chapter 7 introduces the entirely fictional **CivicFlow Permitting Suite** and inventories configurable statuses/workflows, validation, queues, notifications, exports/API, reports/dashboards, roles, warnings, correction tracking, audit history, and rules. Every product capability is a `MODELED ALTERNATIVE ASSUMPTION`; cross-system reconciliation is explicitly unsupported.

The sequence is **inventory → standardize → configure validation/queues → native reporting/automation → process change → measure residual → custom edge only if material**. Configuration has explicit discovery, configuration, engineering, acquisition, training/change, and recurring support work. Native capability, configuration, process change, and custom ownership remain distinct.

The six-category `MODELED ASSUMPTION` decomposition reconciles exactly to the unchanged **$104,002.80** Chapter 0 recoverable value. Sequential capped recovery prevents double counting and reports the residual after every intervention. The baseline result is conditional: configuration removes a meaningful portion, while a measured residual leaves the Chapter 6 read-only reconciliation view as a candidate only. Strong-incumbent, weak-incumbent, and poor-standardization sensitivities show that neither `BUY / CONFIGURE` nor `NARROW CUSTOM EDGE` is hard-coded. This changes the interpretation of `POOR TARGET CUSTOMER`: custom software should not own burden already removable by incumbent capability, while the remaining engagement must still pass project and target gates.

```bash
python -m government_engagement_lab configure-first
python -m government_engagement_lab configure-first-economics
python -m government_engagement_lab configure-first-scenarios
python -m government_engagement_lab residual
```

## Chapter 8 small departmental engagement

Chapter 8 changes contract size while retaining the same fictional customer and a bounded correction/resubmission reporting problem. The main scope has one correction-desk team, eight users, a read-only export plus configuration mapping, a standardized status view, exception report, management summary, provenance, 120 engineering hours, and bounded annual support. It addresses a modeled **42% / $43,681.18** of original recoverable value—not the whole problem.

The **acquisition floor** emerges from required journey stages rather than a universal threshold. The baseline still consumes 58 acquisition hours and $5,970 acquisition labor against a $30,000 implementation. Its $9,830 acquisition-adjusted contribution misses the fictional $10,000 sustainability requirement by $170, while customer first-year economics remain positive. Seller break-even is **$30,170** and the independently derived customer-supported ceiling is **$39,681.18**, producing project `PASS`, target `FAIL`, and `POOR TARGET CUSTOMER` at the modeled price.

The scenarios show why smaller is not a verdict. “Too small” preserves required acquisition work and becomes `NO DEAL`; “efficient small” reduces explicit stage mechanisms to 36 hours and becomes `PROMISING — VALIDATE IN DISCOVERY`; high recurring support becomes `NO DEAL` without changing delivery scope. The fixture therefore reveals a possible middle band and **complicates**, rather than universally confirms or disproves, the cookbook hypothesis. No minimum contract size, real willingness to pay, market price, or real procurement norm is claimed.

```bash
python -m government_engagement_lab small-engagement
python -m government_engagement_lab small-engagement-economics
python -m government_engagement_lab small-engagement-scenarios
python -m government_engagement_lab contract-size
```

Chapter 9's larger-contract question remains unimplemented.
