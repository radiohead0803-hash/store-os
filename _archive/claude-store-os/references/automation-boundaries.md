# Automation Boundaries

## Decision Rule

Classify every task into one of four levels:

| Level | Meaning | Default handling |
|---|---|---|
| L0 Human-only | money, law, privacy, production risk | operator must approve and execute |
| L1 AI draft | AI drafts/recommends only | operator edits/approves |
| L2 approval automation | AI prepares and executes after approval | approval logged |
| L3 bounded automation | AI executes under pre-approved limits | audit event required |

## Human-only

- Payment provider contracts and settlement account changes.
- Privacy policy, refund policy, legal terms approval.
- Public product launch approval.
- High-cost print orders and vendor contracts.
- Refund denial and disputes.
- Production deployment, database migration, secret rotation.
- Child-related educational claims or sensitive customer complaints.

## AI Draft

- Product ideas, names, bundles, price suggestions.
- Design briefs and Claude Design prompts.
- Listing copy, FAQ, thumbnails, detail page structure.
- Vendor comparison, reorder recommendation, sales reports.

## Approval Automation

- Product page creation as unpublished draft.
- Low-risk detail-page copy changes.
- Approved template content posting.
- Print reorder request under review.

## Bounded Automation

Allowed only after operator sets policies:

- Low-risk FAQ replies using approved answers.
- Daily report generation.
- Inventory low-stock alerts.
- Reorder suggestions under budget threshold, not direct purchase unless explicitly allowed.
- Conversion-analysis based improvement tasks.
