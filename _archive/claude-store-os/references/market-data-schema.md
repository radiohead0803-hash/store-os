# Market Data Schema

## Minimal Input
Use at least one row per keyword or product idea.

```csv
keyword,product,demand,competition,margin,production,repeat,risk,price,cost
칭찬스티커판,초등 칭찬스티커 세트,78,55,72,86,58,18,7900,1600
```

## Supported Aliases
| Canonical | Also accepted |
|---|---|
| keyword | 키워드, search, query |
| product | 상품명, item, title |
| demand | 수요, demand_score, search_score |
| competition | 경쟁, competition_score, difficulty |
| margin | 마진, profit, margin_score |
| production | 제작, 생산성, ease, simplicity |
| repeat | 반복구매, repeatability |
| risk | 리스크, risk_score |
| price | 가격, 판매가 |
| cost | 원가, 비용 |

## Output Files
| File | Purpose |
|---|---|
| product_scores.csv | ranked opportunities and decisions |
| listings/*.md | draft product listings for unpublished review |
| content_calendar.csv | 30-day content plan |
| kpi_tracker.csv | daily KPI log template |
| store-ops-dashboard.html | local dashboard for review |

## Data Quality Rules
- Do not use fake customer PII.
- Do not treat search volume, ad score, or AI estimates as final proof.
- Mark missing values as assumptions.
- Use small paid tests only after operator approval.
