#!/usr/bin/env python3
"""Generate slice-by-slice Claude Code prompts for a scaffolded project."""
from __future__ import annotations
import argparse
from pathlib import Path

PROMPTS = """# Claude Code Implementation Prompts

Use one prompt per session. Do not ask Claude Code to build everything at once.

## Prompt 1 - Foundation
You are Claude Code. Build the project foundation for a Claude-operated self-owned store. Use Next.js, TypeScript, Tailwind, shadcn/ui, PostgreSQL readiness, env validation, and a health endpoint. Add README instructions for a beginner. Do not add payments yet. Return changed files and test commands.

## Prompt 2 - UI/CSS Trend Decision
You are the UI/CSS Trend Research Agent. Before frontend implementation, analyze current commerce/admin UI trends and propose 3-5 style options. Recommend one style for a beginner-operated Claude Store OS. Generate or update Docs/UI_CSS_STYLE_DECISION.md, html/style-choice-board.html, html/admin-dashboard-preview.html, frontend/styles/design-tokens.css, and frontend/styles/component-patterns.md. Include accessibility, responsiveness, and implementation complexity. Do not proceed to React components until the developer accepts a style.

## Prompt 3 - Data and rules
Implement Prisma schema and business-rule tests. Enforce that no product can become public unless proofApproved and legalApproved are true. Add AutomationPolicy and AuditEvent. Return migration notes and rollback notes.

## Prompt 4 - Admin workflow
Build admin screens for product ideas, scoring, Claude Design workflow, product draft, proof checklist, and approval gate. Keep actions auditable. Return screenshots or preview notes.

## Prompt 5 - Public store MVP
Build public product page for the first reward-sticker product, order capture, and inventory decrement. Store minimal PII. Return UI smoke path.

## Prompt 6 - Claude automation
Add Claude service stubs for product ideas, listing copy, low-risk CS draft, and sales summary. Redact PII. Require policy checks before any execution. Return API contract notes.

## Prompt 7 - Release proof
Create final proof dossier, Railway runbook, security/privacy report, test matrix, and operator SOP. Mark release as Fail until evidence is attached.
"""

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(PROMPTS, encoding="utf-8")
    print(f"[OK] wrote {out}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
