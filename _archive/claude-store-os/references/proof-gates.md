# Proof Gates

## Product Launch Gate

A product may become public only when all are true:

- Target customer and product promise are documented.
- Design assets have print-readability proof.
- No copyright-risk assets are present.
- Product page includes components, size, delivery, refund, and usage information.
- Price includes cost, packaging, fee, and margin assumptions.
- Legal/refund/privacy copy is operator-approved.
- Proof Agent records Pass or accepted Conditional Pass.

## Technical Gate

A slice may merge only when all are true:

- Unit tests for business rules pass.
- API contract checks pass.
- UI smoke path is documented or tested.
- Auth/role checks exist for approval actions.
- Secrets are not hardcoded.
- DB migrations and rollback notes exist.
- Audit events are created for automated actions.

## AI Automation Gate

AI automation may move from draft to execution only when:

- Action type is mapped to an automation level.
- Operator policy allows it.
- Budget/risk threshold is not exceeded.
- The action is logged.
- A rollback or correction path exists.

## Final Proof Output

Use this format:

| Gate | Status | Evidence | Blockers | Decision |
|---|---|---|---|---|

Decisions: Pass / Conditional Pass / Fail.
