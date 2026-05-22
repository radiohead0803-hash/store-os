# Store Operations Automation

## Purpose
Turn the store OS from a planning-only package into a repeatable operating loop for printable, sticker, 생활관리, and small Smart Store products.

## Operating Loop
1. **Market data intake**: import a CSV of keywords/products from Naver, Coupang, Etsy, manual competitor research, or ad tests.
2. **Product scoring**: score demand, margin, competition, production simplicity, repeatability, and risk.
3. **Listing generation**: generate unpublished listing briefs, SEO titles, benefit bullets, FAQ, tags, and approval checklist.
4. **Content calendar**: generate 30-day blog/Instagram/shorts content topics tied to the selected product line.
5. **KPI tracker**: create or update a CSV that tracks views, clicks, conversion, sales, returns, and operator decisions.
6. **Dashboard HTML**: render a beginner-readable operations dashboard with product scores, KPI status, and next actions.
7. **Proof gate**: mark every candidate as launch, improve, hold, or stop using evidence.

## Required CSV Columns
The automation accepts flexible Korean or English column names. Recommended columns:

| Column | Meaning | Example |
|---|---|---|
| keyword | search keyword or product idea | 칭찬스티커판 |
| product | product name | 초등 칭찬스티커 세트 |
| demand | demand score 0-100 | 75 |
| competition | competition score 0-100, higher means harder | 60 |
| margin | expected margin score 0-100 | 70 |
| production | production simplicity score 0-100 | 85 |
| repeat | repeatability score 0-100 | 55 |
| risk | risk score 0-100, higher means riskier | 20 |
| price | expected selling price KRW | 7900 |
| cost | expected cost KRW | 1500 |

If a column is missing, the script uses safe defaults and flags the assumption in output.

## Score Formula
Default opportunity score:

```text
score = demand*0.30 + margin*0.20 + production*0.15 + repeat*0.10 + (100-competition)*0.15 + (100-risk)*0.10
```

## Decision Bands
| Score | Decision | Rule |
|---:|---|---|
| 80+ | launch test | create listing and 30-day content test |
| 65-79 | improve then test | adjust bundle, price, design, or target |
| 50-64 | hold | keep in idea bank, do not spend ad/reorder budget |
| below 50 | stop | no paid action unless operator overrides |

## Human Approval Gates
AI may draft but cannot public-launch or spend money without approval. Require operator approval for public product visibility, paid ads, print orders above limit, legal/privacy/refund text, child-related outcome claims, refund disputes, vendor contracts, production deploys, secrets, and destructive migrations.

## Harness Commands
Run from the skill root or copied project folder:

```bash
python scripts/store_ops.py sample-data --output ./out/sample_market.csv
python scripts/store_ops.py analyze-market ./out/sample_market.csv --output ./out/ops
python scripts/store_ops.py generate-listings ./out/ops/product_scores.csv --output ./out/ops/listings
python scripts/store_ops.py content-calendar ./out/ops/product_scores.csv --output ./out/ops/content_calendar.csv --days 30
python scripts/store_ops.py init-kpi --output ./out/ops/kpi_tracker.csv
python scripts/store_ops.py render-dashboard ./out/ops --output ./out/ops/store-ops-dashboard.html
python scripts/store_ops.py run-pipeline ./out/sample_market.csv --output ./out/ops
```

## Proof Evidence
Each run should preserve:
- input CSV path and timestamp
- generated product score CSV
- generated listing markdown files
- content calendar CSV
- KPI tracker CSV
- dashboard HTML
- operator decision notes

A product is not approved simply because it scored high. Approval requires market evidence, proof checklist, legal/claims review, and operator acceptance.
