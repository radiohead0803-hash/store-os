#!/usr/bin/env python3
"""Validate a Claude Store OS scaffold for beginner-operable completeness."""
from __future__ import annotations
import argparse
from pathlib import Path

REQUIRED = [
    "Docs/BEGINNER_START_HERE.md",
    "Docs/STORE_CONTROL_PLANE.md",
    "Docs/MAX_AUTOMATION_PLAN.md",
    "Docs/CONNECTOR_PLUGIN_PLAN.md",
    "Docs/DESIGN_AUTOMATION_PLAN.md",
    "Docs/AUTOMATION_BOUNDARY_MAP.md",
    "Docs/ERROR_VALIDATION_AGENT_PLAN.md",
    "Docs/ERROR_VALIDATION_REPORT.md",
    "Docs/STACK_DECISION.md",
    "Docs/DATA_MODEL.md",
    "Docs/FIRST_STICKER_VERTICAL_SLICE.md",
    "Docs/CLAUDE_AGENT_PLAN.md",
    "Docs/CLAUDE_CODE_PROMPTS.md",
    "Docs/GITHUB_RAILWAY_RUNBOOK.md",
    "Docs/PROOF_GATE_MATRIX.md",
    "Docs/FINAL_PROOF_DOSSIER.md",
    "Docs/OPERATIONS_SOP.md",
    "Docs/TROUBLESHOOTING.md",
    "railway/railway-template.env.example",
    "prisma/schema.prisma",
    "frontend/styles/component-patterns.md",
    "frontend/styles/design-tokens.css",
    "html/admin-dashboard-preview.html",
    "html/style-choice-board.html",
    "Docs/UI_CSS_STYLE_DECISION.md",
    ".github/pull_request_template.md",
]

KEYWORDS = [
    "proofApproved",
    "legalApproved",
    "AutomationPolicy",
    "DesignAsset",
    "AuditEvent",
    "CLAUDE_API_KEY",
    "rollback",
    "AuditEvent",
    "AutomationPolicy",
    "Error Validation",
    "Connector",
    "kill switches",
    "admin-dashboard-preview.html",
    "style-choice-board.html",
    "design-tokens.css",
    "Bento Commerce Ops",
    "UI/CSS Style Decision",
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project")
    args = parser.parse_args()
    root = Path(args.project)
    errors: list[str] = []
    for rel in REQUIRED:
        if not (root / rel).exists():
            errors.append(f"missing required file: {rel}")
    combined = "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in root.rglob("*.md"))
    combined += "\n" + "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in root.rglob("*.prisma"))
    combined += "\n" + "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in root.rglob("*.example"))
    for kw in KEYWORDS:
        if kw not in combined:
            errors.append(f"missing required concept: {kw}")
    if errors:
        print("[FAIL] Claude Store OS scaffold validation failed")
        for e in errors:
            print(f"- {e}")
        return 1
    print("[PASS] Claude Store OS scaffold contains required beginner-operable artifacts")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
