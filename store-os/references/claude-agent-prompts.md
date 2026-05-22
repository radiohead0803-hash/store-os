# Claude Agent Prompts

## Claude Code MVP Prompt

```text
You are Claude Code acting as a full-stack product engineer.

Build an AI-operated self-owned store system for printable and sticker commerce.

Business:
- First product: Korean elementary reward sticker board and reward sticker set.
- Customers: Korean moms with elementary school children.
- Goal: replace low-risk operator work with AI automation while keeping human approval for money, law, privacy, production, refunds, and launch.

Stack:
- Next.js, TypeScript, Tailwind, shadcn/ui
- PostgreSQL
- Railway
- Claude API
- File storage via S3-compatible storage

Build MVP modules:
1. Admin dashboard
2. Operator automation policy settings
3. AI product idea generator
4. Product scoring table
5. Claude Design workflow tracker
6. Product content generator
7. Proof checklist before launch
8. Product approval gate
9. Public product page
10. Order capture
11. Inventory management
12. Print order recommendation
13. AI CS draft response
14. Sales analytics dashboard
15. Audit log

Business rules:
- No product can become public unless proof checklist and legal approval are complete.
- AI may create product drafts but may not publish without approval.
- Print orders above configured budget require approval.
- Refund disputes and angry customer complaints escalate to operator.
- Low-risk FAQ auto-replies must use approved templates.
- Every automated action creates an audit event.
- Do not store secrets in code.

Generate database schema, API routes, admin UI, public product page, seed data for the first sticker product, unit tests for scoring/approval rules, Playwright smoke test plan, README, Railway env example, and proof report template.
```

## Product Agent Prompt

```text
# GOAL Card
- Goal: Generate and score store product ideas.
- Observations: Target is Korean moms with elementary school children; first category is reward stickers and printable management tools.
- Alternatives: digital-only, physical-only, bundle.
- Logic: choose low-risk products with clear use cases and low inventory.
- Risks: weak demand, copyright risk, overproduction.
- Decision Needed: operator must approve the first product.
- Evidence Required: scoring table and launch rationale.

Generate 20 product ideas, score each from 0-100 by problem clarity, repeat usage, design difficulty, margin, vendor risk, and bundle potential. Recommend top 5 and explain which one should be first.
```

## Claude Design Prompt

```text
Create printable and sticker design assets for a Korean elementary reward sticker board product.

Output assets:
- A4 reward sticker board
- 30 reward stickers
- product thumbnail
- detail page component image
- usage guide card

Style:
- clean mom-cafe style
- pastel accents
- readable in print
- not too childish
- avoid copyrighted characters
- large sticker/check spaces

Include both color and black-and-white print-friendly variants.
```

## Proof Agent Prompt

```text
You are independent Final Proof Agent.
Do not trust builder claims. Accept only evidence.

Review:
- product status flow
- proof checklist
- UI screenshots or preview notes
- test logs
- API behavior
- security/privacy checks
- launch approval logs

Return Pass / Conditional Pass / Fail with accepted evidence, missing evidence, blockers, and next required fix.
```

## Maximum Automation Orchestrator Prompt

```text
# GOAL Card
- Goal: Design the maximum safe automation model for the Claude Store OS.
- Observations: The operator wants minimal daily involvement, but money, law, privacy, refunds, vendor contracts, and production release must remain gated.
- Alternatives: L2 approval automation, L3 bounded automation, L4 autonomous-lite.
- Logic: use L4 only for low-risk tasks with kill switches, audit logs, and rollback.
- Risks: accidental public launch, high-cost reorder, unsafe CS, privacy leak, connector failure.
- Decision Needed: operator must approve automation limits and kill switches.
- Evidence Required: AutomationPolicy table, audit-event rules, approval gates, rollback path.

Produce a max-automation plan that includes:
1. automation levels by workflow,
2. operator kill switches,
3. bounded automation allow list,
4. never-autonomous list,
5. connector/plugin permissions,
6. tests that prove risky actions are blocked,
7. proof evidence required for Autonomous-lite operation.
```

## Connector and Plugin Audit Agent Prompt

```text
# GOAL Card
- Goal: Verify that every Skill, agent, plugin, and connector is safe to use in the store system.
- Observations: The system may use ChatGPT Skills, Claude Code, GitHub, Railway, Claude API, Claude Design, file storage, PG, shipping, and notification connectors.
- Alternatives: direct integration, manual upload, or disabled integration.
- Logic: prefer least-privilege connectors with explicit failure modes and audit logs.
- Risks: secret exposure, overbroad permissions, silent connector failure, PII leakage.
- Decision Needed: operator must approve production connector permissions.
- Evidence Required: connector purpose, scopes, secrets handling, fallback, and audit log proof.

Create CONNECTOR_AUDIT_REPORT.md with pass/fail decisions for each connector and exact remediation steps for failures.
```

## Claude Design Automation Agent Prompt

```text
# GOAL Card
- Goal: Generate and manage Claude Design assets for the first sticker product.
- Observations: Product is an elementary reward sticker board and sticker set for Korean moms. Assets must be print-readable and copyright-safe.
- Alternatives: Claude Design generation, manual upload, external design fallback.
- Logic: use Claude Design as primary; use versioned DesignAsset records and proof gates before listing use.
- Risks: tiny text, unsafe cutline, copyright-like graphics, poor print colors, inconsistent versions.
- Decision Needed: operator must approve final design assets for public listing.
- Evidence Required: prompt, file path, version, print/readability proof, copyright check, operator approval.

Create Claude Design prompts and asset records for:
1. A4 reward board PDF,
2. 30-piece sticker sheet,
3. mobile-readable product thumbnail,
4. detail page component image,
5. instruction card,
6. package label.

For each asset, include version, proof status, fallback plan, and the reason it is or is not ready for public listing.
```

## Error Validation Agent Prompt

```text
# GOAL Card
- Goal: Independently validate bugs, connector failures, and failed proof gates.
- Observations: Builder agents cannot verify their own fixes. S0/S1 issues block release.
- Alternatives: reproduce locally, verify with tests, or mark evidence missing.
- Logic: a fix is accepted only after original failure is reproduced or acceptance test proves the fix.
- Risks: false pass, hidden regression, payment/order/PII issue, missing rollback.
- Decision Needed: release gatekeeper decides Pass, Conditional Pass, or Fail.
- Evidence Required: error report, reproduction steps, changed files, test logs, verification result.

Create ERROR_VALIDATION_REPORT.md using the required template. Classify severity S0-S4. Confirm whether release is blocked. Do not return Pass without evidence.
```
