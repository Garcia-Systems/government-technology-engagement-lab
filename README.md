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

This repository currently contains **Chapters 0–3 only**. Historical scenario names and verdicts are preserved as inspectable reference data, not implemented experiments. Chapter 2 decomposes the baseline buying journey; it does not implement the later motions suggested by those historical names.

## Architecture

- `models.py` contains immutable typed domain records, including reusable engagement stages and journeys.
- `fixtures/*.json` contains the fictional baseline, journey decomposition, and deliberately small scenario data.
- `economics.py` performs three transparent customer calculations using `Decimal`.
- `baseline.py` preserves Chapter 0; `gates.py` evaluates Chapter 1 viability; `journey.py` loads Chapter 2 journeys and calculates unweighted burden summaries; `stakeholders.py` loads, validates, and summarizes Chapter 3 topology.
- `evidence.py` owns the reusable evidence vocabulary; `cli.py` presents the executable chapter.
- `chapters/` explains the model as a textbook; `tests/` lock down identity, economics, evidence, and verdict mechanics.

No seller contribution margin is calculated because Chapter 0 supplies no labor rates. No generic government score, procurement simulation, later experiment, database, or web application is present.

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

Descriptive summaries count stakeholders, role assignments, stage participation, approvals, blocking paths, and technical-access dependencies without a score. Explicit findings make Chapter 1's `STAKEHOLDER_FRICTION` traceable to visible mechanisms. Authority-only sensitivities cover a strong sponsor, fragmented authority, and no sponsor while leaving legitimate controls or the underlying technical project visible. Chapter 4's formal RFP motion remains unresolved and unimplemented.
