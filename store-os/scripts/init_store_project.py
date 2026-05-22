#!/usr/bin/env python3
"""Scaffold a beginner-friendly Claude Store OS development package."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from textwrap import dedent

REQUIRED_DOCS = [
    "BEGINNER_START_HERE.md",
    "STORE_CONTROL_PLANE.md",
    "MAX_AUTOMATION_PLAN.md",
    "CONNECTOR_PLUGIN_PLAN.md",
    "DESIGN_AUTOMATION_PLAN.md",
    "AUTOMATION_BOUNDARY_MAP.md",
    "ERROR_VALIDATION_AGENT_PLAN.md",
    "ERROR_VALIDATION_REPORT.md",
    "UI_CSS_STYLE_DECISION.md",
    "STACK_DECISION.md",
    "DATA_MODEL.md",
    "FIRST_STICKER_VERTICAL_SLICE.md",
    "CLAUDE_AGENT_PLAN.md",
    "CLAUDE_CODE_PROMPTS.md",
    "GITHUB_RAILWAY_RUNBOOK.md",
    "PROOF_GATE_MATRIX.md",
    "FINAL_PROOF_DOSSIER.md",
    "OPERATIONS_SOP.md",
    "TROUBLESHOOTING.md",
]

ENV_EXAMPLE = """# Railway / local env example. Do not commit real secrets.
DATABASE_URL=postgresql://USER:PASSWORD@HOST:PORT/DB
AUTH_SECRET=replace-with-generated-secret
CLAUDE_API_KEY=replace-in-railway-secret-only
NEXT_PUBLIC_STORE_NAME=Claude Printable Store
AUTOMATION_MAX_PRINT_ORDER_KRW=50000
LOW_RISK_CS_AUTO_REPLY=false
"""

PRISMA_SCHEMA = """generator client { provider = \"prisma-client-js\" }
datasource db { provider = \"postgresql\" url = env(\"DATABASE_URL\") }

enum ProductStatus { idea scored design_requested design_ready proof_review approved public selling improve_or_stop }
enum ApprovalStatus { pending approved rejected conditional }

model ProductIdea {
  id String @id @default(cuid())
  title String
  target String
  problem String
  marketScore Int @default(0)
  productionScore Int @default(0)
  marginScore Int @default(0)
  riskScore Int @default(0)
  status ProductStatus @default(idea)
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}

model DesignAsset {
  id String @id @default(cuid())
  productId String?
  type String
  prompt String
  fileUrl String?
  version String @default("v1")
  proofStatus ApprovalStatus @default(pending)
  operatorApproval ApprovalStatus @default(pending)
  createdAt DateTime @default(now())
}

model Product {
  id String @id @default(cuid())
  title String
  slug String @unique
  price Int
  status ProductStatus @default(idea)
  publicVisibility Boolean @default(false)
  legalApproved Boolean @default(false)
  proofApproved Boolean @default(false)
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}

model ProofChecklist {
  id String @id @default(cuid())
  productId String
  item String
  result ApprovalStatus @default(pending)
  evidenceUrl String?
  reviewer String?
  createdAt DateTime @default(now())
}

model InventoryItem {
  id String @id @default(cuid())
  productId String
  onHand Int @default(0)
  reserved Int @default(0)
  reorderPoint Int @default(5)
  reorderLimit Int @default(30)
}

model Order {
  id String @id @default(cuid())
  customerEmail String?
  customerName String?
  paymentStatus String @default(\"pending\")
  fulfillmentStatus String @default(\"pending\")
  riskFlags String @default(\"[]\")
  createdAt DateTime @default(now())
}

model AutomationPolicy {
  id String @id @default(cuid())
  action String
  maxBudget Int?
  allowedStatuses String
  requiresApproval Boolean @default(true)
  enabled Boolean @default(false)
}

model AuditEvent {
  id String @id @default(cuid())
  actor String
  action String
  target String
  before String?
  after String?
  createdAt DateTime @default(now())
}
"""


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-name", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    out = Path(args.output)
    docs = out / "Docs"
    write(docs / "BEGINNER_START_HERE.md", f"""
# Beginner Start Here

Project: {args.project_name}

## What you are building
A Claude-operated self-owned commerce MVP for the first reward-sticker product.

## Build order
1. Read `STORE_CONTROL_PLANE.md`.
2. Run Claude Code prompts in `CLAUDE_CODE_PROMPTS.md` one slice at a time.
3. After each slice, update `PROOF_GATE_MATRIX.md`.
4. Before launch, complete `FINAL_PROOF_DOSSIER.md`.

## Minimum operational target
- Admin settings exist.
- Product idea and scoring workflow exists.
- Design workflow stores Claude Design prompts/results.
- Product cannot become public without legal and proof approval.
- Customer can submit an order.
- Inventory and reorder recommendation work.
- AI CS drafts low-risk replies only.
- Audit log records every automated action.
""")
    write(docs / "STORE_CONTROL_PLANE.md", """
# Store Control Plane

## Mission
Build and operate a Claude-based self-owned store where AI handles low-risk work and the operator approves money, law, privacy, launch, and exception decisions.

## First product
초등 저학년 칭찬스티커판 + 칭찬스티커 세트.

## Stage gates
| Stage | Pass evidence |
|---|---|
| Scope | target, product, automation levels documented |
| Architecture | stack, data model, env, deployment plan documented |
| Build | changed files, tests, screenshots/logs |
| Proof | proof checklist pass or conditional pass |
| Release | rollback, monitoring, operator SOP |
""")
    write(docs / "MAX_AUTOMATION_PLAN.md", """
# Max Automation Plan

## Goal
Operate the store with AI handling low-risk execution and the operator handling only approvals, exceptions, and risk decisions.

## Automation levels
| Level | Allowed | Blocked without operator |
|---|---|---|
| L1 AI draft | product ideas, copy, design prompts, reports | execution |
| L2 approval automation | unpublished listing, reorder request, CS draft | publish/send/order until approved |
| L3 bounded automation | low-risk FAQ, daily reports, stock alerts | risky customer/legal/money actions |
| L4 autonomous-lite | approved content posting, small safe refinements | high-cost orders, refunds, deploys |

## Required kill switches
- Disable AI execution.
- Disable product publishing.
- Disable print ordering.
- Disable auto CS replies.
- Freeze price changes.
- Force all actions to approval-required mode.

## Max-automation acceptance
- Every automated action creates an AuditEvent.
- Every L2/L3/L4 action checks AutomationPolicy.
- Every risky action has an operator approval path.
- Every automation has rollback or manual fallback.
""")
    write(docs / "CONNECTOR_PLUGIN_PLAN.md", """
# Connector and Plugin Plan

## Integration map
| System | Use | Approval |
|---|---|---|
| ChatGPT Skills | repeatable planning, proof, docs | skill validation |
| Claude Code | implementation by slice | PR review |
| GitHub connector | repo, issues, PRs, CI evidence | branch protection |
| Railway connector | deployment, DB, env | production approval |
| Claude API | product, listing, CS, reports | policy limits |
| Claude Design | design assets | print proof approval |
| S3/R2 | design and proof file storage | access review |
| Payment/PG | payment status | legal/settlement approval |
| Courier/shipping | tracking and fulfillment | initial manual review |

## Connector audit checklist
- Least privilege.
- Secret handling.
- Audit event for external action.
- Timeout/retry/fallback.
- Human gate for risky operation.
- PII minimization.
""")
    write(docs / "DESIGN_AUTOMATION_PLAN.md", """
# Claude Design Automation Plan

## Goal
Use Claude Design as the primary AI design system for sticker/printable commerce assets.

## Asset flow
product idea -> design brief -> Claude Design prompt -> asset generation -> DesignAsset version -> print proof -> copyright check -> operator approval -> listing use

## Required assets for first sticker product
| Asset | Required proof |
|---|---|
| A4 reward board PDF | actual-size readability check |
| sticker sheet | cutline/safe-area check |
| product thumbnail | mobile readability check |
| detail page images | component/size/use clarity |
| instruction card | no misleading claim |

## Automation rules
- AI may generate design briefs and Claude Design prompts automatically.
- AI may store generated assets as DesignAsset records.
- AI may request revisions when proof fails.
- AI may not publish assets to public listing before operator approval.
- Every design revision must keep prompt, file path, version, and proof status.

## Failure fallback
| Failure | Fallback |
|---|---|
| Claude Design unavailable | manual upload or external design tool exception |
| text unreadable | regenerate with fewer sections and larger type |
| cutline unsafe | request vendor template and regenerate |
| copyright risk | remove risky asset and regenerate generic design |
| poor print color | generate high-contrast and black-white variants |
""")
    write(docs / "UI_CSS_STYLE_DECISION.md", """
# UI/CSS Style Decision

## Purpose
Let the UI/CSS Trend Research Agent analyze modern admin/store design trends, propose options, and force a developer/operator style choice before frontend build.

## Recommended default for first MVP
**Bento Commerce Ops + Calm Enterprise SaaS**

Why:
- Beginner-friendly operation dashboard.
- Good separation of product, order, inventory, AI automation, and proof-gate cards.
- Less risky than heavy glassmorphism for dense admin screens.

## Style options
| Option | Best for | Visual direction | Pros | Risks | Recommended? |
|---|---|---|---|---|---|
| Calm Enterprise SaaS | admin forms/tables | neutral, clear, high contrast | reliable and readable | can feel plain | yes |
| Bento Commerce Ops | owner dashboard | KPI cards, modular grids | modern and scannable | can become cluttered | yes |
| Premium Soft Glass | customer-facing hero | translucent panels, soft gradient | premium feel | contrast/performance risk | conditional |
| Command Center Dark | error/automation monitor | dark, alert-focused | strong for logs | not ideal for full store | no for MVP |
| Minimal High-Density Admin | advanced operations | dense tables, filters | powerful later | hard for beginner | later |

## CSS token baseline
| Token | Value |
|---|---|
| radius | 16px cards, 12px controls |
| shadow | soft layered shadow, no harsh borders |
| surface | white/neutral with subtle tinted sections |
| accent | warm coral or mint accent for printable/sticker brand |
| typography | large dashboard numbers, readable body, no tiny labels |
| state colors | approved, pending, blocked, warning visually distinct |

## Developer decision
- Pick one primary style before React implementation.
- Do not mix more than two visual systems in MVP.
- Keep customer store pages softer than admin screens.

## Required preview artifacts
- `html/style-choice-board.html`
- `html/admin-dashboard-preview.html`
- `frontend/styles/design-tokens.css`
- `frontend/styles/component-patterns.md`

## Proof checklist
- [ ] 360px mobile preview checked.
- [ ] 768px tablet preview checked.
- [ ] 1280px desktop preview checked.
- [ ] Focus state visible.
- [ ] Error/pending/approved states do not rely on color only.
- [ ] Proof gate and kill switch are visible on dashboard.
""")
    write(docs / "ERROR_VALIDATION_AGENT_PLAN.md", """
# Error Validation Agent Plan

## Agents
| Agent | Role | Output |
|---|---|---|
| Error Intake Agent | collect error/log/context | error ticket |
| Error Triage Agent | severity and owner | triage result |
| Reproduction Agent | minimal repro/test | repro evidence |
| Fix Builder Agent | patch implementation | changed files |
| Regression Test Agent | test coverage | failing-then-passing test |
| Security Error Agent | leak/auth/privacy review | containment decision |
| Connector Error Agent | plugin/connector failure analysis | connector report |
| Fix Verification Agent | independent verification | Pass/Fail |
| Error Gatekeeper | release/block decision | release decision |

## Severity
| Severity | Meaning | Action |
|---|---|---|
| S0 | data loss/secret/payment/PII exposure | stop release |
| S1 | checkout/order/security broken | block release |
| S2 | major workflow broken with workaround | conditional pass only |
| S3 | minor UI/content/report issue | fix or backlog |
| S4 | improvement | backlog |
""")
    write(docs / "ERROR_VALIDATION_REPORT.md", """
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
- Original failure reproduced? no
- Fix verified? no
- Regression risk:
- Proof decision: Fail until evidence exists

## Release Decision
- Block release? yes
- Operator approval required? yes
- Next action:
""")
    write(docs / "AUTOMATION_BOUNDARY_MAP.md", """
# Automation Boundary Map

| Workflow | Level | AI may do | Operator approval |
|---|---|---|---|
| Product ideas | L1 | generate and score | choose first product |
| Design | L1/L2 | prompt Claude Design and store result | approve final print file |
| Listing | L2 | create unpublished page | approve public launch |
| FAQ CS | L3 | answer approved low-risk FAQ | review escalations |
| Print reorder | L2 | recommend quantity | approve above budget |
| Refund dispute | L0 | summarize facts | operator decides |
| Production deploy | L0 | prepare runbook | operator approves |
""")
    write(docs / "STACK_DECISION.md", """
# Stack Decision

| Layer | Pick | Reason |
|---|---|---|
| Frontend | Next.js + TypeScript | beginner-friendly full stack |
| UI | Tailwind + shadcn/ui | fast admin UI |
| DB | PostgreSQL | reliable relational commerce data |
| Deployment | Railway | simple deploy + database |
| AI | Claude API + Claude Code | planning, coding, automation drafts |
| Design | Claude Design workflow tracker | design result management |
""")
    write(docs / "DATA_MODEL.md", """
# Data Model

See `prisma/schema.prisma` for starter schema. Required entities:
ProductIdea, DesignAsset, Product, ProofChecklist, InventoryItem, Order, AutomationPolicy, AuditEvent.
""")
    write(docs / "FIRST_STICKER_VERTICAL_SLICE.md", """
# First Sticker Vertical Slice

## Flow
idea -> score -> Claude Design brief -> design_ready -> proof_review -> approved -> public -> order -> inventory -> CS -> analytics

## First product acceptance
- Product promise is clear and not exaggerated.
- A4/sticker print proof exists.
- No copyrighted character or unsafe claim.
- Product page explains components, size, usage, shipping/refund.
- Order capture and inventory updates work.
""")
    write(docs / "CLAUDE_AGENT_PLAN.md", """
# Claude Agent Plan

| Agent | Output | Proof |
|---|---|---|
| Store Orchestrator | scope, gates, choices | control plane complete |
| Product Agent | product ideas and scores | scoring rules visible |
| Design Agent | Claude Design brief | print proof attached |
| Listing Agent | product copy and FAQ | legal/claims checklist |
| Claude Code Frontend | admin/public UI | UI smoke evidence |
| Claude Code Backend | APIs/rules | unit/API tests |
| Security/Privacy Agent | risk report | no hardcoded secrets, PII minimized |
| Final Proof Agent | pass/fail dossier | evidence accepted |
""")
    write(docs / "CLAUDE_CODE_PROMPTS.md", """
# Claude Code Prompts

## Slice 1 - Project foundation
Build a Next.js TypeScript app with Tailwind and shadcn/ui. Add admin layout, env validation, README, and health endpoint. Do not add payment yet. Add tests for env and health endpoint.

## Slice 2 - Data model
Add Prisma/PostgreSQL schema for ProductIdea, DesignAsset, Product, ProofChecklist, InventoryItem, Order, AutomationPolicy, AuditEvent. Add seed data for first sticker product. Add migration notes and rollback notes.

## Slice 3 - Product workflow
Build admin screens for product ideas, scoring, design workflow, proof checklist, and approval gate. Enforce: no public product unless proofApproved and legalApproved are true.

## Slice 4 - Public store and order capture
Build public product page and order capture. Store minimal customer info. Add inventory reservation/stock decrement. Add audit event for order creation.

## Slice 5 - AI automation
Add service stubs for Claude API: product ideas, listing copy, CS draft, sales summary. Do not send PII unless redacted. Add AutomationPolicy checks before execution.

## Slice 6 - Proof and release
Add test matrix, Playwright smoke plan, security/privacy checklist, Railway runbook, and final proof dossier. Return remaining blockers.

## Slice 7 - Connectors and plugin integration
Add integration adapters/stubs for GitHub issue creation, Railway deploy evidence capture, Claude API execution logs, file-storage asset records, payment status webhook placeholders, and shipping task placeholders. All external actions must create AuditEvent and use operator approval for risky actions.

## Slice 8 - Error validation agents
Add ErrorValidationReport model or markdown output, severity classification, repro checklist, fix verification checklist, and release-blocking rules. Add tests proving S0/S1 block release and product public launch remains blocked when proof/legal approval is missing.
""")
    write(docs / "GITHUB_RAILWAY_RUNBOOK.md", """
# GitHub and Railway Runbook

## GitHub
- Use feature branches.
- Require PR checklist: tests, screenshots, proof impact, security notes.
- Protect main branch before production.

## Railway
- Put secrets in Railway variables only.
- Required env: DATABASE_URL, AUTH_SECRET, CLAUDE_API_KEY, AUTOMATION_MAX_PRINT_ORDER_KRW.
- Deploy staging first.
- Verify `/api/health` before public launch.

## Rollback
- Keep previous deployment available.
- Never run destructive DB migration without backup.
""")
    write(docs / "PROOF_GATE_MATRIX.md", """
# Proof Gate Matrix

| Gate | Required evidence | Status | Blocker |
|---|---|---|---|
| Product launch | proof checklist, legal approval, print proof | pending |  |
| Technical | tests, API contract, UI smoke | pending |  |
| Security/privacy | secrets, auth, PII, logs | pending |  |
| Automation | policy, audit log, rollback path | pending |  |
| Release | deploy logs, health, rollback, SOP | pending |  |
""")
    write(docs / "FINAL_PROOF_DOSSIER.md", """
# Final Proof Dossier

## Decision
Fail until all required evidence is attached.

| Evidence | Link/path | Accepted? |
|---|---|---|
| Changed files |  | no |
| Test logs |  | no |
| UI screenshots |  | no |
| Security/privacy report |  | no |
| Railway deploy logs |  | no |
| Rollback plan |  | no |
| Operator SOP |  | no |
""")
    write(docs / "OPERATIONS_SOP.md", """
# Operations SOP

## Daily
Check orders, risky CS, inventory alerts, failed automations, and daily report.

## Weekly
Review conversion, CS complaints, product improvement suggestions, reorder recommendations, and new product candidates.

## Monthly
Review profit, automation boundaries, security/privacy logs, vendor performance, and proof evidence refresh.
""")
    write(docs / "TROUBLESHOOTING.md", """
# Troubleshooting

| Problem | Fix |
|---|---|
| Product will not publish | check proofApproved and legalApproved |
| AI reply not sent | check AutomationPolicy and risk level |
| Railway deploy fails | check env vars and build logs |
| DB migration risk | backup and require operator approval |
| Secret exposed | rotate immediately and remove from logs/code |
""")
    write(out / "html" / "style-choice-board.html", """
<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Claude Store OS - Style Choice Board</title>
  <link rel="stylesheet" href="../frontend/styles/design-tokens.css" />
</head>
<body class="page-shell">
  <main class="container">
    <section class="hero-card">
      <p class="eyebrow">UI/CSS Trend Research Agent</p>
      <h1>개발 전 스타일 선택 보드</h1>
      <p>Claude Code가 프론트엔드를 만들기 전에 운영자가 선택해야 하는 UI 스타일 옵션입니다.</p>
    </section>
    <section class="option-grid">
      <article class="option-card recommended"><span class="badge">추천</span><h2>Bento Commerce Ops</h2><p>상품, 주문, 재고, AI 자동화, Proof Gate를 카드형으로 보여주는 현대적 운영 대시보드.</p></article>
      <article class="option-card"><h2>Calm Enterprise SaaS</h2><p>초보자가 쓰기 쉬운 명확한 테이블, 폼, 좌측 내비게이션 중심 관리자 화면.</p></article>
      <article class="option-card"><h2>Premium Soft Glass</h2><p>고객-facing 상품 페이지나 랜딩에만 제한적으로 쓰는 부드러운 프리미엄 스타일.</p></article>
      <article class="option-card danger"><h2>Command Center Dark</h2><p>에러 검증, 자동화 로그, 장애 대시보드에는 적합하지만 전체 MVP 기본값은 아님.</p></article>
    </section>
  </main>
</body>
</html>
""")
    write(out / "html" / "admin-dashboard-preview.html", """
<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Claude Store OS - Admin Dashboard Preview</title>
  <link rel="stylesheet" href="../frontend/styles/design-tokens.css" />
</head>
<body class="page-shell">
  <main class="container dashboard">
    <section class="hero-card"><p class="eyebrow">Claude Store OS</p><h1>AI 자동화 스토어 운영 대시보드</h1><p>첫 칭찬스티커 상품의 기획, 디자인, 검증, 주문, 재고, CS, 에러 상태를 한 화면에서 확인합니다.</p></section>
    <section class="kpi-grid">
      <div class="kpi-card"><span>상품 상태</span><strong>proof_review</strong><small>출시 전 검증 대기</small></div>
      <div class="kpi-card"><span>재고</span><strong>30</strong><small>재주문 기준 5</small></div>
      <div class="kpi-card warning"><span>승인 필요</span><strong>3</strong><small>법적 문구, 인쇄 증거, 가격</small></div>
      <div class="kpi-card"><span>AI 자동화</span><strong>L2</strong><small>승인 후 실행</small></div>
    </section>
    <section class="panel-grid">
      <article class="panel"><h2>Proof Gate</h2><ul><li>디자인 출력 증거: pending</li><li>저작권 점검: pending</li><li>운영자 출시 승인: blocked</li></ul></article>
      <article class="panel"><h2>Automation Kill Switch</h2><button>AI 실행 중지</button><button>상품 공개 중지</button><button>자동 CS 중지</button></article>
      <article class="panel"><h2>Error Validation</h2><p class="status-blocked">S1 release blocker: 결제/환불 플로우 미검증</p></article>
    </section>
  </main>
</body>
</html>
""")
    write(out / "frontend" / "styles" / "design-tokens.css", """
:root {
  --color-bg: #f8f7f3; --color-surface: #ffffff; --color-text: #1f2933; --color-muted: #667085; --color-border: #e6e1d8;
  --color-accent: #f28b82; --color-accent-2: #86d6c6; --color-warning: #f6c453; --color-danger: #e25555; --color-success: #37a66b;
  --radius-card: 18px; --radius-control: 12px; --shadow-soft: 0 18px 45px rgba(31, 41, 51, 0.10);
  --space-1: 0.5rem; --space-2: 0.75rem; --space-3: 1rem; --space-4: 1.5rem; --space-5: 2rem;
  font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}
* { box-sizing: border-box; }
body.page-shell { margin: 0; background: radial-gradient(circle at top left, #fff5ef, var(--color-bg)); color: var(--color-text); }
.container { width: min(1120px, calc(100% - 32px)); margin: 0 auto; padding: 32px 0; }
.hero-card, .option-card, .kpi-card, .panel { background: var(--color-surface); border: 1px solid var(--color-border); border-radius: var(--radius-card); box-shadow: var(--shadow-soft); padding: var(--space-5); }
.eyebrow { color: var(--color-accent); font-weight: 800; letter-spacing: 0.08em; text-transform: uppercase; }
h1 { font-size: clamp(2rem, 5vw, 4rem); line-height: 1.05; margin: 0 0 1rem; }
h2 { margin-top: 0; }
.option-grid, .kpi-grid, .panel-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: var(--space-4); margin-top: var(--space-4); }
.panel-grid { grid-template-columns: repeat(3, 1fr); }
.option-card.recommended { border-color: var(--color-accent); } .option-card.danger { border-color: rgba(226,85,85,.35); }
.badge { display: inline-flex; padding: .35rem .65rem; border-radius: 999px; background: #fff1ed; color: var(--color-accent); font-weight: 700; }
.kpi-card strong { display: block; font-size: 2rem; margin: .5rem 0; } .kpi-card span, .kpi-card small { color: var(--color-muted); }
.warning { border-color: rgba(246,196,83,.5); } .status-blocked { color: var(--color-danger); font-weight: 700; }
button { border: 0; border-radius: var(--radius-control); padding: .75rem 1rem; margin: .25rem; background: var(--color-text); color: white; font-weight: 700; }
button:focus-visible, a:focus-visible { outline: 3px solid var(--color-accent-2); outline-offset: 3px; }
@media (max-width: 900px) { .option-grid, .kpi-grid, .panel-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 560px) { .option-grid, .kpi-grid, .panel-grid { grid-template-columns: 1fr; } .container { width: min(100% - 20px, 1120px); padding: 20px 0; } }
""")
    write(out / "frontend" / "styles" / "component-patterns.md", """
# Component Patterns

## Admin dashboard
- Use bento KPI cards for product status, inventory, approval blockers, automation health.
- Use table rows for orders, vendors, proof checklist, and audit logs.
- Put kill switches above automation logs.
- Always show blocked/pending/approved with text labels and icons, not color only.

## Public store page
- Use softer brand visuals than admin screens.
- Keep purchase CTA clear.
- Include product size, components, usage, delivery, refund notice, and proof confidence.

## Error monitor
- Use Command Center Dark only for logs/error console pages, not beginner admin defaults.
""")
    write(out / "railway" / "railway-template.env.example", ENV_EXAMPLE)
    write(out / "prisma" / "schema.prisma", PRISMA_SCHEMA)
    write(out / ".github" / "pull_request_template.md", """
# PR Checklist

- [ ] Slice goal is clear.
- [ ] Tests pass or blocker documented.
- [ ] Screenshots/logs attached when UI/deploy changed.
- [ ] No secrets in code.
- [ ] Automation level and approval gate updated.
- [ ] Proof matrix updated.
""")
    write(out / ".github" / "ISSUE_TEMPLATE" / "store-task.yml", """
name: Store OS Task
description: Claude Store OS implementation task
body:
  - type: textarea
    id: goal
    attributes:
      label: Goal
  - type: textarea
    id: proof
    attributes:
      label: Required proof
""")
    write(out / ".github" / "workflows" / "store-checks.yml", """
name: Store Checks
on: [pull_request]
jobs:
  placeholder:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Add npm test, lint, typecheck, and proof validation here."
""")
    manifest = {"project_name": args.project_name, "required_docs": REQUIRED_DOCS, "automation_target": "max-autonomous-lite-with-operator-gates", "error_agents": ["intake", "triage", "reproduction", "fix_builder", "regression_test", "security_error", "connector_error", "ui_css_error", "fix_verification", "gatekeeper"], "ui_css_agent": "required-before-frontend-build", "html_previews": ["html/style-choice-board.html", "html/admin-dashboard-preview.html"]}
    write(out / "store-os-manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2))
    print(f"[OK] scaffolded {out}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
