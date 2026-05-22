# Skills, Agents, Plugins, and Connectors Integration

Use this reference when designing how Claude Store OS coordinates AI tools, ChatGPT Skills, Claude agents, external plugins, and connectors.

## Integration Principle

Connectors and plugins are not trusted just because they exist. Each integration must have:

- Purpose.
- Data accessed.
- Permissions required.
- Failure mode.
- Human approval boundary.
- Audit log.
- Fallback path.

## Recommended Tooling Map

| Capability | Primary tool | Connector/plugin pattern | Approval |
|---|---|---|---|
| System planning | ChatGPT Skill + Claude | skill-guided workflow | none |
| Code generation | Claude Code | GitHub repo connector | PR review |
| Version control | GitHub | issues, PRs, commits, actions | branch protection |
| Deployment | Railway | project/env/database | production approval |
| AI text/product ops | Claude API | server-side API calls | policy limits |
| Design workflow | Claude Design | uploaded/generated assets | print proof approval |
| File storage | R2/S3 | asset URLs | access policy review |
| Payment | PG provider | payment status webhooks | legal/settlement approval |
| Shipping | courier API or manual CSV | tracking and fulfillment | initial manual review |
| Email/SMS | notification provider | templates only | template approval |
| Analytics | internal DB + dashboard | event tracking | privacy review |

## ChatGPT Skill Composition

When a user asks to build, validate, or improve the system, this skill should coordinate with specialized skills when available:

| Skill type | Use for |
|---|---|
| Spreadsheet skill | budget, vendor scoring, sales analysis files |
| Slides skill | investor or internal presentation |
| PDF/DOCX skills | policies, manuals, customer-facing documents |
| Domain factory skills | broader marketplace, reseller, or game/store variants |
| Skill creator | updating this operating system skill |

## Agent Topology

### Builder Agents

- Store Orchestrator Agent
- Product/Market Agent
- Claude Design Agent
- Listing/Content Agent
- Frontend Agent
- Backend Agent
- Database Agent
- Integration Agent
- DevOps/Railway Agent
- Documentation Agent

### Proof and Error Agents

- QA Harness Agent
- Security/Privacy Agent
- Connector Audit Agent
- Error Reproduction Agent
- Error Triage Agent
- Fix Verification Agent
- Final Proof Agent
- Release Gatekeeper

## Connector Audit Checklist

| Check | Pass condition |
|---|---|
| Least privilege | connector only accesses needed scope |
| Secret handling | no secret in prompts, logs, or repo |
| Audit log | external action recorded |
| Failure mode | timeout/retry/fallback documented |
| Human gate | risky operation requires approval |
| Data minimization | customer PII redacted where possible |
| Rollback | safe recovery path exists |

## Plugin/Connector Failure Policy

If a connector fails:

1. Do not mark the step complete.
2. Capture error text and operation context.
3. Classify as auth, permission, rate limit, validation, network, or unknown.
4. Try one documented fallback.
5. If fallback fails, create a human task with exact next action.
6. Record evidence in `ERROR_VALIDATION_REPORT.md`.

## 100-Point Live Commerce Adapter Layer

Use the operating harness before any live API work:

```bash
python scripts/store_ops.py platform-payloads ./out/store-ops/product_scores.csv ./out/store-ops/listings --output ./out/store-ops/platform_api_staging
python scripts/store_ops.py ingest-orders ./orders.csv --output ./out/store-ops/order_ops
python scripts/store_ops.py image-plan ./out/store-ops/product_scores.csv ./out/store-ops/listings --output ./out/store-ops/image_generation_plan.csv
python scripts/store_ops.py ip-precheck ./out/store-ops/listings --output ./out/store-ops/ip_precheck.csv
python scripts/store_ops.py live-runbook --output ./out/store-ops/LIVE_INTEGRATION_RUNBOOK.md
```

### Adapter order
1. CSV staging: create Naver, Coupang, Shopify payloads with `live_publish_allowed=false`.
2. API dry-run: validate schema, secret storage, endpoint permissions, and rollback notes.
3. Approved live action: only after operator, legal/claims, IP, and proof gates are accepted.

### Never automate without explicit approval
- public listing publish or deletion
- price, stock, settlement, refund, ad spend, coupon, or shipping commitment changes
- customer dispute or angry/refund/legal replies
- use of character, logo, brand, celebrity, or third-party design elements
- patent/design/trademark exception approval
