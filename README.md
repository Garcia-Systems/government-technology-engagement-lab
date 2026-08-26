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

This repository currently contains **Chapter 0 only**. Historical scenario names and verdicts are preserved as inspectable reference data, not implemented experiments.

## Architecture

- `models.py` contains immutable typed domain records and explicit gate/finding enums.
- `fixtures/*.json` contains the fictional baseline and historical cookbook scenarios.
- `economics.py` performs three transparent customer calculations using `Decimal`.
- `baseline.py` loads fixtures and assesses gates through visible, unweighted acquisition findings.
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
```

The baseline command shows the modeled inputs, derived customer economics, acquisition findings, independent gates, and inherited verdict. The scenarios command shows only historical modeled cookbook outcomes.

## Chapter 0 calculation boundary

Given the fictional assumptions, the executable computes:

```text
first-year cost = $78,000.00 + $24,000.00 = $102,000.00
first-year net recoverable value = $104,002.80 - $102,000.00 = $2,002.80
implementation-only payback = $78,000.00 / $104,002.80 × 12 ≈ 9.00 months
```

The last measure excludes annual support and is deliberately not called full first-year payback. Positive modeled customer economics, technical feasibility, and support viability coexist with a target-attractiveness failure. Thus `POOR TARGET CUSTOMER` is the hypothesis subsequent experiments must attempt to break—not a repository-wide conclusion.
