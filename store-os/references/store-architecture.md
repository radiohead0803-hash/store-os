# Store Architecture

## Default Stack

| Layer | Default |
|---|---|
| Frontend | Next.js + TypeScript + Tailwind + shadcn/ui |
| Backend | Next.js API routes for MVP; NestJS/FastAPI only if complexity grows |
| Database | PostgreSQL on Railway |
| Auth | Auth.js, Clerk, or managed auth |
| File storage | Cloudflare R2 or S3-compatible storage |
| AI | Claude API, Claude Design workflow, Claude Code prompts |
| Deployment | GitHub + Railway |
| Testing | unit, API contract, Playwright smoke, security/privacy checks |

## Core Modules

1. Admin dashboard
2. Operator policy settings
3. Product idea board
4. Product scoring engine
5. Design workflow tracker
6. Product listing generator
7. Proof checklist and approval gate
8. Public product pages
9. Order capture and payment status
10. Inventory and print reorder management
11. CS ticket and AI reply draft
12. Sales analytics and improvement loop
13. Audit log

## Suggested Status Flow

`idea -> scored -> design_requested -> design_ready -> proof_review -> approved -> public -> selling -> improve_or_stop`

## API Boundary

- `/api/ai/product-ideas`: generate and score product ideas.
- `/api/design/workflows`: track Claude Design prompts/results.
- `/api/products`: create and update product drafts.
- `/api/proof/checklists`: record launch evidence.
- `/api/orders`: capture and manage orders.
- `/api/inventory`: track stock and reorder points.
- `/api/vendors`: manage print vendors and quotes.
- `/api/cs`: classify tickets and draft replies.
- `/api/analytics`: sales, conversion, and improvement reports.
- `/api/audit`: immutable action logs.

## Security Defaults

- Store API keys only in Railway/GitHub secrets.
- Log AI actions without storing sensitive prompt secrets.
- Role-gate publish, refund, vendor-order, and deployment actions.
- Keep customer PII minimal and redact it from AI prompts when possible.
