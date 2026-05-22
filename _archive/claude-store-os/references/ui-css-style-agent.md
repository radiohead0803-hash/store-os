# UI/CSS Style Trend Agent

## Purpose
Add a dedicated UI/CSS Trend Research Agent so the store system does not default to a dated admin template. The agent must research current UI patterns, compare options, propose 3-5 style systems, and let the developer/operator choose one before implementation.

## Required Agent Output
For every new store build or redesign, produce:

| Output | Required content |
|---|---|
| Trend scan | 3-5 current UI patterns relevant to commerce/admin systems |
| Style options | name, best fit, visual direction, risks, accessibility notes |
| CSS token set | colors, radius, shadow, spacing, typography, motion |
| Component impact | dashboard cards, tables, forms, product cards, approval gates |
| HTML preview impact | which HTML preview files must be updated |
| Developer choice board | option comparison and recommended pick |
| Proof evidence | screenshots/preview paths, accessibility checklist, responsive checks |

## Default Style Options

| Style | Best for | Characteristics | Risks | Accessibility guardrail |
|---|---|---|---|---|
| Calm Enterprise SaaS | beginner-friendly admin | white/neutral surfaces, clear nav, strong forms/tables | plain look | high contrast, visible focus states |
| Bento Commerce Ops | owner dashboard | KPI cards, modular sections, product/action cards | clutter if overused | strict hierarchy, keyboard order |
| Premium Soft Glass | customer-facing store and premium demo | translucent panels, gradients, layered depth | readability/performance | blur fallback, contrast-safe text |
| Command Center Dark | operations/error monitoring | dark surface, high-signal alerts, logs | eye strain | avoid low-contrast gray text |
| Minimal High-Density Admin | power users | dense tables, filters, bulk actions | overwhelming for beginners | progressive disclosure, sticky help |

## Recommended Default
For the first sticker-store MVP, recommend **Bento Commerce Ops + Calm Enterprise SaaS**:
- Use bento cards for KPIs, product status, automation health, and proof gates.
- Use calm enterprise forms/tables for orders, inventory, vendors, and audit logs.
- Use subtle gradients only for hero/summary sections, not dense data tables.

## UI Quality Gate
A UI slice may not pass until all are true:

- Responsive at 360px, 768px, and 1280px widths.
- Keyboard focus is visible.
- Text contrast is readable on all surfaces.
- Error, warning, pending, and approved states are visually distinct without relying only on color.
- Product launch approval gates are visually prominent.
- Automation kill switches are visible to the operator.
- HTML preview or screenshot evidence exists.

## Required HTML/CSS Artifacts in Scaffolds
The project scaffold should include:

```text
Docs/UI_CSS_STYLE_DECISION.md
html/style-choice-board.html
html/admin-dashboard-preview.html
frontend/styles/design-tokens.css
frontend/styles/component-patterns.md
```

These artifacts are planning/preview assets. They do not replace production React components, but they give Claude Code and the developer a concrete visual direction before coding.
