# Error Validation Agents

Use this reference when the user asks for error handling, debugging, proof, or production-grade validation.

## Core Rule

A bug is not fixed when a builder says it is fixed. A bug is fixed only when an independent Fix Verification Agent reproduces the original failure or validates the acceptance test, then records evidence.

## Error Agent Roles

| Agent | Owns | Output | Cannot do |
|---|---|---|---|
| Error Intake Agent | collect error, context, logs | error ticket | implement fix |
| Error Triage Agent | classify severity and root area | triage decision | close issue |
| Reproduction Agent | create minimal repro steps/test | repro evidence | approve fix |
| Fix Builder Agent | implement correction | patch/PR | verify own fix |
| Regression Test Agent | add/update tests | failing-then-passing test | bypass proof |
| Security Error Agent | assess leak/auth/privacy risk | severity and containment | accept unresolved high risk |
| Connector Error Agent | isolate integration failure | connector report | change secrets without approval |
| Fix Verification Agent | verify repair evidence | Pass/Fail | implement fix |
| Error Gatekeeper | decide release/block | release decision | ignore missing evidence |

## Severity Levels

| Severity | Definition | Default action |
|---|---|---|
| S0 | data loss, secret leak, payment/PII exposure | stop release, operator approval |
| S1 | checkout/order/security broken | block release |
| S2 | major workflow broken but workaround exists | conditional pass only with workaround |
| S3 | minor UI/content/report issue | fix or backlog |
| S4 | improvement/nice-to-have | backlog |

## Required Error Report

Use this exact structure:

```markdown
# Error Validation Report

## Summary
- Error ID:
- Severity:
- Affected module:
- Detected by:
- Status:

## Reproduction
- Steps:
- Expected:
- Actual:
- Evidence:

## Root Cause
- Suspected area:
- Confirmed cause:

## Fix
- Changed files:
- Tests added:
- Commands run:

## Verification
- Original failure reproduced? yes/no
- Fix verified? yes/no
- Regression risk:
- Proof decision: Pass / Conditional Pass / Fail

## Release Decision
- Block release? yes/no
- Operator approval required? yes/no
- Next action:
```

## Error Gates by Module

| Module | Must test | Blocker examples |
|---|---|---|
| Auth | role gates, session, admin only | non-admin can approve product |
| Product publish | proof/legal gates | public product without approval |
| Order capture | validation, inventory, duplicate submit | order lost or duplicate charged |
| Payment | webhook validation, idempotency | payment status wrong |
| Inventory | reserved/on hand consistency | overselling without alert |
| Print order | budget and vendor approval | high-cost order auto-created |
| CS automation | risk classifier, template source | refund denial auto-sent |
| AI prompts | PII redaction, output schema | sensitive data sent to model unnecessarily |
| Connector | timeout/retry/fallback | silent failure or missing audit log |
| Deployment | env, health check, rollback | no rollback path |

## Fix Verification Commands

Prefer commands like:

```bash
npm test
npm run lint
npm run typecheck
npm run test:e2e
npm run build
python scripts/validate_store_os.py ./out/claude-printable-store
```

If commands cannot be run, the proof agent must state that evidence is missing and return Conditional Pass or Fail.
