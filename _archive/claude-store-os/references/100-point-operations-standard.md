# 100-Point Store Operations Standard

## Purpose
Upgrade the store OS from planning/scaffolding to operating-system grade execution while preserving human approval for money, law, privacy, customer trust, and production risk.

## Required Execution Loop
1. Market data CSV intake.
2. Product opportunity scoring.
3. Listing draft generation.
4. Risk scan for claims, child-sensitive wording, copyright/trademark, refund/delivery promises, and unsupported superlatives.
5. Printable draft generation in TXT/HTML/PDF forms.
6. Store import CSV staging for Smartstore/Shopify-like manual upload or later API adapters.
7. KPI tracker and KPI decision report.
8. Operator review queue.
9. HTML dashboard and operations runbook.
10. Proof gate: evidence accepted, missing evidence listed, blockers assigned.

## Hard Stop Conditions
- High-risk risk scan finding in listing or printable text.
- Product marked public without proof/legal/operator approval.
- Real API publish without connected credentials and audit event.
- Refund dispute, angry customer, child-related sensitive claim, legal text, paid ad scaling, vendor contract, production deploy, secrets, or DB migration without operator approval.

## Evidence Required for 100-Point Claim
- `product_scores.csv`
- `store_import.csv`
- `risk_scan.csv`
- `operator_review_queue.csv`
- `kpi_decisions.csv`
- `100_POINT_OPERATIONS_RUNBOOK.md`
- printable TXT/HTML/PDF outputs
- HTML dashboard
- passing unittest log with 20+ tests

## Scoring
- 100: all required execution artifacts exist, tests pass, and high-risk actions are gated.
- 90-99: executable but missing one integration adapter or proof evidence item.
- 80-89: strong planning and draft automation, but not enough operational evidence.
- below 80: planning/documentation only.
