# Connector, Order State, Kill-Switch, and Audit Upgrade

Use this reference when developing the live-ready commerce operating system beyond CSV staging. The goal is not blind automation; the goal is safe, evidence-backed operation with separated connectors, deterministic state transitions, automatic pause rules, and reviewable audit logs.

## Connector Separation

Create one adapter contract per platform:

| Platform | Default mode | Live actions blocked by default | Required proof before live |
|---|---|---|---|
| Naver SmartStore | CSV/API staging | publish, price, stock, refund, customer message | schema validation, dry-run, approval id, rollback plan, audit event |
| Coupang | CSV/API staging | product create/update, shipping update, refund, CS send | schema validation, dry-run, approval id, rollback plan, audit event |
| Shopify | draft API staging | publish, inventory change, fulfillment, refund, webhook mutation | schema validation, webhook signature proof, approval id, rollback plan, audit event |

Run:

```bash
python scripts/store_ops.py connector-manifest --output ./out/store-ops/connector_contracts
```

## Order State Machine

Do not treat orders as free text. Normalize every order into a state transition:

```text
draft/created -> paid -> proof_pending -> prepare -> shipped -> delivered -> closed
any state -> cancel_requested -> refund_review -> refunded or closed
any unsafe/unknown state -> hold_operator
```

Run:

```bash
python scripts/store_ops.py order-state-machine ./orders.csv --output ./out/store-ops/order_state_machine.csv
```

## CS Classification

Classify customer messages before drafting a response:

- legal threat: operator escalation, no auto reply.
- refund dispute: operator escalation, no auto reply.
- angry customer: operator escalation, no auto reply.
- shipping question: template draft only after approval.
- download/PDF access: template draft only after approval.
- custom request: operator review.

## Auto Pause / Kill Switch

A listing, ad, or workflow must pause when:

- high IP or claims risk exists.
- ad spend is meaningful and ROAS is below threshold.
- return rate is above threshold.
- CS volume exceeds order count.
- multiple escalated CS messages appear.
- CTR is too low after enough impressions.

Run:

```bash
python scripts/store_ops.py auto-pause ./kpi_tracker.csv --cs-csv ./cs_triage.csv --risk-csv ./risk_scan.csv --output ./auto_pause_decisions.csv
```

## Audit Log

Every staged artifact and every future live action must have:

- timestamp
- actor
- artifact/action
- payload hash
- approval id
- risk level
- rollback note

Run:

```bash
python scripts/store_ops.py audit-log ./out/store-ops --output ./out/store-ops/audit_log.csv
```

## Development Rule

A builder may generate connector payloads, state transitions, CS triage, pause decisions, and audit rows. A proof agent must verify evidence before any live API call, customer message, refund, ad spend, product publish, or price/stock mutation.
