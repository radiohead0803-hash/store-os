# Maximum Automation Operating Model

Use this reference when the user asks for the maximum practical operating model, autonomous operation, or beginner-operable completion.

## Automation Target

The goal is not a fully uncontrolled store. The goal is an AI-operated store where the operator only handles approval, exception, and risk decisions.

## Operating Levels

| Level | Name | AI may execute | Operator still owns |
|---|---|---|---|
| L0 | Manual control | nothing without operator | legal, money, production, disputes |
| L1 | AI draft | plans, copy, code prompts, reports | approval and execution |
| L2 | Approval automation | create draft records, prepare publish/reorder/CS actions | click approve/reject |
| L3 | Bounded automation | low-risk FAQ, reports, stock alerts, internal task creation | policy limits and audit review |
| L4 | Autonomous-lite | pre-approved low-cost reorders, approved content posting, safe listing refinements | daily review and kill switch |

## Max-Automation Store Flow

```text
market signal -> AI product idea -> score -> design brief -> Claude Design asset -> print proof -> listing draft -> legal/proof approval -> public product -> order -> inventory -> shipping task -> CS classification -> sales analytics -> improvement task -> next product
```

## Operator Kill Switches

Always require these controls in the system:

- Disable all AI execution.
- Disable public product publishing.
- Disable print order creation.
- Disable automatic CS replies.
- Freeze prices.
- Disable content posting.
- Force all actions to approval-required mode.

## Autonomous-lite Allow List

AI may perform these under written policy limits:

| Action | Default limit | Required audit evidence |
|---|---:|---|
| Daily report generation | no limit | report path and timestamp |
| Low-risk FAQ response | approved templates only | ticket, template, response |
| Low stock alert | no purchase | product, stock, threshold |
| Small reorder recommendation | max 50,000 KRW | vendor quote and stock data |
| Unpublished listing draft | no public visibility | generated fields and source prompt |
| Detail copy improvement draft | no legal/refund text | before/after diff |
| GitHub issue creation | internal only | issue title and scope |

## Never Autonomous

- PG, settlement, or bank changes.
- Refund denial, legal threats, angry-customer escalation.
- Product public launch without proof and legal approval.
- Vendor contract changes.
- High-cost print orders.
- Production database migration.
- Secret rotation or credential changes.
- Any child-related claim implying guaranteed educational improvement.

## Beginner Completion Bar

The system is beginner-operable only when:

1. A non-developer can read the runbook and know the next action.
2. Claude Code prompts are split by vertical slice.
3. Every slice has a test and proof checklist.
4. Every AI action creates an audit event.
5. Every risky action is blocked by an approval gate.
6. There is a rollback or manual fallback for every automation.
7. Daily/weekly/monthly operator SOPs are documented.
8. Error agents can classify, reproduce, fix, and prove common failures.
