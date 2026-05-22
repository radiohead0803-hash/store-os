#!/usr/bin/env python3
"""Operational automation harness for AI/Claude Store OS.

Creates product opportunity scores, draft listings, content calendar, KPI tracker,
and a static HTML dashboard from CSV inputs.
"""
from __future__ import annotations
import argparse, csv, html, json, math, statistics, re, hashlib
from dataclasses import dataclass, asdict
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Dict, Iterable, List

ALIASES = {
    "keyword": ["keyword", "키워드", "search", "query"],
    "product": ["product", "상품명", "item", "title"],
    "demand": ["demand", "수요", "demand_score", "search_score"],
    "competition": ["competition", "경쟁", "competition_score", "difficulty"],
    "margin": ["margin", "마진", "profit", "margin_score"],
    "production": ["production", "제작", "생산성", "ease", "simplicity"],
    "repeat": ["repeat", "반복구매", "repeatability"],
    "risk": ["risk", "리스크", "risk_score"],
    "price": ["price", "가격", "판매가"],
    "cost": ["cost", "원가", "비용"],
}
DEFAULTS = {
    "keyword": "미정 키워드",
    "product": "미정 상품",
    "demand": 50,
    "competition": 50,
    "margin": 50,
    "production": 50,
    "repeat": 50,
    "risk": 30,
    "price": 0,
    "cost": 0,
}

@dataclass
class ProductScore:
    rank: int
    keyword: str
    product: str
    demand: float
    competition: float
    margin: float
    production: float
    repeat: float
    risk: float
    price: float
    cost: float
    gross_profit: float
    gross_margin_rate: float
    opportunity_score: float
    decision: str
    next_action: str
    assumptions: str


def num(value, default=0.0) -> float:
    try:
        if value is None or value == "":
            return float(default)
        return float(str(value).replace(",", "").strip())
    except ValueError:
        return float(default)


def clamp(x: float, lo=0.0, hi=100.0) -> float:
    return max(lo, min(hi, x))


def normalize_row(row: Dict[str, str]) -> tuple[Dict[str, object], List[str]]:
    lower = {str(k).strip().lower(): v for k, v in row.items()}
    out, assumptions = {}, []
    for canonical, names in ALIASES.items():
        found = None
        for name in names:
            if name.lower() in lower:
                found = lower[name.lower()]
                break
        if found is None or found == "":
            out[canonical] = DEFAULTS[canonical]
            assumptions.append(f"{canonical}=default")
        else:
            out[canonical] = found
    for key in ["demand", "competition", "margin", "production", "repeat", "risk", "price", "cost"]:
        out[key] = num(out[key], DEFAULTS[key])
    out["keyword"] = str(out["keyword"]).strip() or str(DEFAULTS["keyword"])
    out["product"] = str(out["product"]).strip() or str(DEFAULTS["product"])
    return out, assumptions


def decision(score: float) -> tuple[str, str]:
    if score >= 80:
        return "launch test", "unpublished listing + small content/ad test after approval"
    if score >= 65:
        return "improve then test", "improve target, bundle, price, or design before test"
    if score >= 50:
        return "hold", "keep in idea bank; do not spend budget yet"
    return "stop", "no paid action unless operator overrides with evidence"


def score_row(row: Dict[str, str], rank: int = 0) -> ProductScore:
    r, assumptions = normalize_row(row)
    price, cost = float(r["price"]), float(r["cost"])
    gross_profit = max(0.0, price - cost) if price else 0.0
    gross_margin_rate = round((gross_profit / price) * 100, 1) if price else 0.0
    margin_score = float(r["margin"])
    if price and cost:
        margin_score = clamp((gross_profit / price) * 100 * 1.25)
    score = (
        clamp(float(r["demand"])) * 0.30
        + clamp(margin_score) * 0.20
        + clamp(float(r["production"])) * 0.15
        + clamp(float(r["repeat"])) * 0.10
        + (100 - clamp(float(r["competition"]))) * 0.15
        + (100 - clamp(float(r["risk"]))) * 0.10
    )
    dec, action = decision(score)
    return ProductScore(
        rank=rank,
        keyword=str(r["keyword"]),
        product=str(r["product"]),
        demand=clamp(float(r["demand"])),
        competition=clamp(float(r["competition"])),
        margin=round(clamp(margin_score), 1),
        production=clamp(float(r["production"])),
        repeat=clamp(float(r["repeat"])),
        risk=clamp(float(r["risk"])),
        price=price,
        cost=cost,
        gross_profit=round(gross_profit, 1),
        gross_margin_rate=gross_margin_rate,
        opportunity_score=round(score, 1),
        decision=dec,
        next_action=action,
        assumptions="; ".join(assumptions),
    )


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: Iterable[Dict[str, object]], fields: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader(); w.writerows(rows)


def analyze_market(input_csv: Path, output_dir: Path) -> Path:
    rows = read_csv(input_csv)
    scored = [score_row(r) for r in rows]
    scored.sort(key=lambda x: x.opportunity_score, reverse=True)
    for i, s in enumerate(scored, 1):
        s.rank = i
    out = output_dir / "product_scores.csv"
    fields = list(asdict(scored[0]).keys()) if scored else list(ProductScore.__dataclass_fields__.keys())
    write_csv(out, [asdict(s) for s in scored], fields)
    summary = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "input": str(input_csv),
        "count": len(scored),
        "avg_score": round(statistics.mean([s.opportunity_score for s in scored]), 1) if scored else 0,
        "top_product": scored[0].product if scored else None,
        "top_score": scored[0].opportunity_score if scored else None,
    }
    (output_dir / "market_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return out


def slug(text: str) -> str:
    keep = []
    for ch in text.lower():
        if ch.isalnum() or "가" <= ch <= "힣": keep.append(ch)
        elif ch in " -_": keep.append("-")
    s = "".join(keep).strip("-")
    while "--" in s: s = s.replace("--", "-")
    return s[:60] or "product"


def load_scores(scores_csv: Path) -> List[Dict[str, str]]:
    return read_csv(scores_csv)


def listing_markdown(row: Dict[str, str]) -> str:
    product = row.get("product", "상품")
    keyword = row.get("keyword", product)
    price = row.get("price", "")
    score = row.get("opportunity_score", "")
    return f"""# {product} 상세페이지 초안

## Status
- Visibility: unpublished
- Approval required: proof, legal/claims, operator
- Opportunity score: {score}

## SEO Title Options
1. {keyword} | 초등맘 생활관리 Printable 세트
2. {product} - 칭찬습관·공부체크·생활루틴 관리
3. 집에서 바로 쓰는 {keyword} PDF/스티커 세트

## Core Customer
초등 저학년 자녀의 생활습관, 공부습관, 칭찬 보상을 간단히 관리하고 싶은 보호자.

## Benefit Bullets
- 출력해서 바로 사용할 수 있는 쉬운 구성
- 아이가 스스로 체크하고 성취감을 느끼는 구조
- 냉장고, 책상, 학습공간에 붙여 가족이 함께 확인 가능
- 과장된 학습효과 보장 없이 생활습관 형성에 집중

## Draft Price
- 판매가 후보: {price}원
- 번들 후보: PDF + 스티커판 + 칭찬스티커 + 사용가이드

## FAQ Draft
**Q. 몇 살 아이에게 적합한가요?**  
A. 초등 저학년 중심으로 설계하되, 가정 상황에 맞게 조정해서 사용할 수 있습니다.

**Q. 학습 성과가 보장되나요?**  
A. 보장 표현은 사용하지 않습니다. 이 상품은 생활·학습 루틴을 돕는 관리 도구입니다.

**Q. 디지털 파일인가요?**  
A. 판매 방식에 따라 PDF 다운로드 또는 실물 세트로 구성할 수 있습니다.

## Tags
{keyword}, 초등맘, 칭찬스티커, 생활습관, 공부체크표, 식단표, printable, 스마트스토어

## Approval Checklist
- [ ] 저작권/상표권 위험 없음
- [ ] 어린이 교육효과 보장 표현 없음
- [ ] 가격/구성 확인
- [ ] 디자인 출력 가독성 확인
- [ ] proof_approved=true
- [ ] legal_approved=true
- [ ] operator approval logged
"""


def generate_listings(scores_csv: Path, output_dir: Path, limit: int = 10) -> List[Path]:
    rows = load_scores(scores_csv)
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for row in rows[:limit]:
        path = output_dir / f"{row.get('rank','')}_{slug(row.get('product','product'))}.md"
        path.write_text(listing_markdown(row), encoding="utf-8")
        paths.append(path)
    return paths


def generate_calendar(scores_csv: Path, output_csv: Path, days: int = 30) -> Path:
    rows = load_scores(scores_csv)
    top = rows[:5] or [{"product": "생활관리 프린트물", "keyword": "생활관리"}]
    channels = ["blog", "instagram", "shorts", "smartstore", "community"]
    formats = ["problem-solution", "checklist", "before-after", "how-to", "review-request"]
    start = date.today()
    out_rows = []
    for i in range(days):
        item = top[i % len(top)]
        channel = channels[i % len(channels)]
        fmt = formats[i % len(formats)]
        out_rows.append({
            "date": (start + timedelta(days=i)).isoformat(),
            "channel": channel,
            "product": item.get("product", "상품"),
            "keyword": item.get("keyword", "키워드"),
            "format": fmt,
            "hook": f"{item.get('keyword','생활관리')} 때문에 매일 반복되는 고민을 줄이는 방법",
            "cta": "무료 샘플/상세페이지 확인",
            "status": "draft",
        })
    write_csv(output_csv, out_rows, list(out_rows[0].keys()))
    return output_csv


def init_kpi(output_csv: Path) -> Path:
    fields = ["date", "channel", "product", "views", "clicks", "orders", "revenue", "ad_spend", "returns", "cs_tickets", "decision", "notes"]
    today = date.today().isoformat()
    rows = [{"date": today, "channel": "smartstore", "product": "sample", "views": 0, "clicks": 0, "orders": 0, "revenue": 0, "ad_spend": 0, "returns": 0, "cs_tickets": 0, "decision": "track", "notes": "replace sample row"}]
    write_csv(output_csv, rows, fields)
    return output_csv


def render_dashboard(ops_dir: Path, output_html: Path) -> Path:
    scores_path = ops_dir / "product_scores.csv"
    kpi_path = ops_dir / "kpi_tracker.csv"
    products = read_csv(scores_path) if scores_path.exists() else []
    kpis = read_csv(kpi_path) if kpi_path.exists() else []
    total_revenue = sum(num(r.get("revenue", 0)) for r in kpis)
    total_ad = sum(num(r.get("ad_spend", 0)) for r in kpis)
    top_rows = "".join(
        f"<tr><td>{html.escape(r.get('rank',''))}</td><td>{html.escape(r.get('product',''))}</td><td>{html.escape(r.get('opportunity_score',''))}</td><td>{html.escape(r.get('decision',''))}</td></tr>"
        for r in products[:10]
    ) or "<tr><td colspan='4'>No product score data</td></tr>"
    html_doc = f"""<!doctype html><html lang='ko'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>AI Store Ops Dashboard</title><style>
body{{font-family:system-ui,-apple-system,Segoe UI,sans-serif;margin:0;background:#f8fafc;color:#0f172a}}main{{max-width:1120px;margin:auto;padding:28px}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px}}.card{{background:white;border:1px solid #e2e8f0;border-radius:18px;padding:18px;box-shadow:0 10px 30px rgba(15,23,42,.06)}}table{{width:100%;border-collapse:collapse;background:white;border-radius:14px;overflow:hidden}}td,th{{padding:10px;border-bottom:1px solid #e2e8f0;text-align:left}}.badge{{display:inline-block;background:#dbeafe;color:#1d4ed8;border-radius:999px;padding:5px 10px;font-size:12px}}.risk{{color:#b91c1c}}.ok{{color:#047857}}</style></head><body><main>
<span class='badge'>Generated {datetime.now().isoformat(timespec='seconds')}</span><h1>AI Store Operations Dashboard</h1>
<section class='grid'><div class='card'><h2>Products</h2><p>{len(products)} scored ideas</p></div><div class='card'><h2>Revenue</h2><p>{total_revenue:,.0f} KRW</p></div><div class='card'><h2>Ad Spend</h2><p>{total_ad:,.0f} KRW</p></div><div class='card'><h2>Gate</h2><p class='risk'>Public launch requires operator approval</p></div></section>
<h2>Top Product Decisions</h2><table><thead><tr><th>Rank</th><th>Product</th><th>Score</th><th>Decision</th></tr></thead><tbody>{top_rows}</tbody></table>
<h2>Next Actions</h2><ul><li>Approve or reject launch-test candidates.</li><li>Review listing markdown for claims/legal risk.</li><li>Run small content test before paid ads.</li><li>Update KPI tracker daily and rerender dashboard.</li></ul>
</main></body></html>"""
    output_html.parent.mkdir(parents=True, exist_ok=True)
    output_html.write_text(html_doc, encoding="utf-8")
    return output_html



# ---------------------------------------------------------------------------
# 100-point operations extensions: adapters, printable generation, risk scan,
# review queue, KPI decisions, and daily autopilot drafts.
# These functions intentionally produce drafts and import files, not live public
# changes. External store publishing, payments, refunds, production deploys, and
# legal/customer-trust decisions stay behind operator approval gates.
# ---------------------------------------------------------------------------

RISK_RULES = [
    ("guaranteed_outcome", re.compile(r"(100%|무조건|반드시|보장|성적\s*향상|1등|완치|치료|효과\s*보장)", re.I), "교육/건강/성과 보장 표현은 삭제하거나 완화해야 합니다."),
    ("child_sensitive_claim", re.compile(r"(아이.*교정|문제아|장애|ADHD|우울|불안|치료)", re.I), "아동 민감 정보나 치료성 표현은 전문가 검토 전 사용하지 않습니다."),
    ("copyright_trademark", re.compile(r"(디즈니|포켓몬|산리오|마블|카카오프렌즈|라인프렌즈|짱구|캐릭터)", re.I), "상표/저작권 캐릭터 표현은 사용 권한 증빙 없이는 금지합니다."),
    ("refund_delivery_risk", re.compile(r"(환불\s*불가|교환\s*불가|무조건\s*배송|당일\s*보장)", re.I), "환불/배송 단정 문구는 플랫폼 정책과 실제 운영능력에 맞게 검토합니다."),
    ("unsafe_discount", re.compile(r"(최저가|국내\s*최저|업계\s*1위|완판)", re.I), "객관적 증빙 없는 비교/최상급 표현은 삭제합니다."),
]


def scan_text_risk(text_value: str) -> dict:
    findings = []
    for code, pattern, guidance in RISK_RULES:
        matches = sorted(set(m.group(0) for m in pattern.finditer(text_value or "")))
        if matches:
            findings.append({"code": code, "matches": ", ".join(matches[:5]), "guidance": guidance})
    severity = "high" if any(f["code"] in {"guaranteed_outcome", "child_sensitive_claim", "copyright_trademark"} for f in findings) else "medium" if findings else "low"
    return {"severity": severity, "finding_count": len(findings), "findings": findings}


def scan_listing_risks(input_dir: Path, output_csv: Path) -> Path:
    rows = []
    files = list(input_dir.glob("*.md")) if input_dir.is_dir() else [input_dir]
    for path in files:
        text_value = path.read_text(encoding="utf-8", errors="ignore")
        result = scan_text_risk(text_value)
        rows.append({
            "file": str(path),
            "severity": result["severity"],
            "finding_count": result["finding_count"],
            "findings": json.dumps(result["findings"], ensure_ascii=False),
            "decision": "operator review required" if result["severity"] != "low" else "draft ok",
        })
    write_csv(output_csv, rows, ["file", "severity", "finding_count", "findings", "decision"])
    return output_csv


def export_store_import(scores_csv: Path, listings_dir: Path, output_csv: Path, platform: str = "naver") -> Path:
    """Create a draft import CSV for smartstore/shopify-like manual upload.
    It is deliberately unpublished and excludes live API calls.
    """
    rows = load_scores(scores_csv)
    import_rows = []
    for row in rows:
        product = row.get("product", "상품")
        keyword = row.get("keyword", product)
        md_files = sorted(listings_dir.glob(f"*{slug(product)}*.md")) if listings_dir.exists() else []
        detail = md_files[0].read_text(encoding="utf-8") if md_files else listing_markdown(row)
        risk = scan_text_risk(detail)
        import_rows.append({
            "platform": platform,
            "external_sku": f"DRAFT-{row.get('rank','0')}-{slug(product)}",
            "name": product,
            "seo_title": f"{keyword} | 생활관리 printable 세트",
            "price": row.get("price", ""),
            "stock": 0,
            "visibility": "unpublished",
            "category_hint": "생활/문구/육아 printable",
            "tags": f"{keyword}, 초등맘, 생활관리, printable",
            "detail_markdown": detail[:3000],
            "risk_severity": risk["severity"],
            "approval_required": "proof, legal, operator",
        })
    write_csv(output_csv, import_rows, list(import_rows[0].keys()) if import_rows else ["platform","external_sku","name"])
    return output_csv


def evaluate_kpi(kpi_csv: Path, output_csv: Path) -> Path:
    rows = read_csv(kpi_csv)
    out_rows = []
    for r in rows:
        views = num(r.get("views", 0)); clicks = num(r.get("clicks", 0)); orders = num(r.get("orders", 0))
        revenue = num(r.get("revenue", 0)); ad_spend = num(r.get("ad_spend", 0)); returns = num(r.get("returns", 0)); cs = num(r.get("cs_tickets", 0))
        ctr = (clicks / views * 100) if views else 0
        cvr = (orders / clicks * 100) if clicks else 0
        roas = (revenue / ad_spend * 100) if ad_spend else 0
        return_rate = (returns / orders * 100) if orders else 0
        if orders >= 3 and (ad_spend == 0 or roas >= 250) and return_rate <= 10 and cs <= orders:
            decision_txt = "scale cautiously"
        elif views >= 300 and ctr < 1:
            decision_txt = "improve thumbnail/title"
        elif clicks >= 50 and cvr < 1:
            decision_txt = "improve offer/detail page"
        elif return_rate > 10 or cs > orders:
            decision_txt = "pause and fix quality/CS"
        else:
            decision_txt = "continue collecting data"
        out_rows.append({**r, "ctr_percent": round(ctr, 2), "cvr_percent": round(cvr, 2), "roas_percent": round(roas, 1), "return_rate_percent": round(return_rate, 2), "ops_decision": decision_txt})
    fields = list(out_rows[0].keys()) if out_rows else ["date","ops_decision"]
    write_csv(output_csv, out_rows, fields)
    return output_csv


def _simple_pdf(output_pdf: Path, title: str, lines: list[str]) -> Path:
    """Write a minimal one-page PDF without third-party dependencies.
    Korean glyph rendering depends on viewer font substitution, so also output TXT/HTML companions.
    """
    def esc(s: str) -> str:
        return s.replace('\\','\\\\').replace('(','\\(').replace(')','\\)').encode('latin-1','replace').decode('latin-1')
    content_lines = ["BT /F1 18 Tf 50 780 Td (" + esc(title) + ") Tj ET"]
    y = 740
    for line in lines[:32]:
        content_lines.append(f"BT /F1 11 Tf 50 {y} Td ({esc(line[:90])}) Tj ET")
        y -= 20
    stream = "\n".join(content_lines)
    objs = []
    objs.append("1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj")
    objs.append("2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj")
    objs.append("3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >> endobj")
    objs.append("4 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj")
    objs.append(f"5 0 obj << /Length {len(stream.encode('latin-1'))} >> stream\n{stream}\nendstream endobj")
    pdf = "%PDF-1.4\n"
    offsets = [0]
    for obj in objs:
        offsets.append(len(pdf.encode('latin-1')))
        pdf += obj + "\n"
    xref = len(pdf.encode('latin-1'))
    pdf += f"xref\n0 {len(objs)+1}\n0000000000 65535 f \n"
    for off in offsets[1:]:
        pdf += f"{off:010d} 00000 n \n"
    pdf += f"trailer << /Size {len(objs)+1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n"
    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    output_pdf.write_bytes(pdf.encode('latin-1'))
    return output_pdf


def generate_printables(product: str, output_dir: Path, child_name: str = "") -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    name = child_name or "아이"
    templates = {
        "reward-board": [f"{name}의 칭찬 스티커판", "목표: 스스로 해낸 일을 칭찬해요", "□ 양치하기  □ 책읽기  □ 숙제하기  □ 정리하기", "스티커 10개 달성 보상: 가족과 함께 정하기"],
        "study-check": [f"{name}의 공부 체크표", "월  화  수  목  금  토  일", "읽기 / 쓰기 / 수학 / 준비물 / 정리", "부담보다 꾸준함을 칭찬합니다."],
        "meal-planner": ["주간 식단표", "월 화 수 목 금 토 일", "아침 / 점심 / 저녁 / 간식", "냉장고 재료를 먼저 확인하고 작성하세요."],
    }
    paths = []
    for key, lines in templates.items():
        title = f"{product} - {key}"
        txt = output_dir / f"{key}.txt"; txt.write_text("\n".join([title]+lines), encoding="utf-8"); paths.append(txt)
        html_path = output_dir / f"{key}.html"
        html_path.write_text("<!doctype html><meta charset='utf-8'><style>body{font-family:system-ui;padding:40px} .box{border:2px solid #111;border-radius:18px;padding:24px;margin:16px 0} h1{font-size:32px}</style>" + f"<h1>{html.escape(title)}</h1>" + "".join(f"<div class='box'>{html.escape(x)}</div>" for x in lines), encoding="utf-8")
        paths.append(html_path)
        paths.append(_simple_pdf(output_dir / f"{key}.pdf", title, lines))
    return paths


def create_review_queue(ops_dir: Path, output_csv: Path) -> Path:
    tasks = []
    for path in sorted((ops_dir / "listings").glob("*.md")) if (ops_dir / "listings").exists() else []:
        risk = scan_text_risk(path.read_text(encoding="utf-8", errors="ignore"))
        tasks.append({"artifact": str(path), "review_type": "listing legal/claims", "severity": risk["severity"], "owner": "operator", "status": "pending", "required_before": "public listing"})
    for path in sorted((ops_dir / "printables").glob("*.pdf")) if (ops_dir / "printables").exists() else []:
        tasks.append({"artifact": str(path), "review_type": "print/readability", "severity": "medium", "owner": "operator", "status": "pending", "required_before": "sale"})
    tasks.append({"artifact": "store_import.csv", "review_type": "platform import approval", "severity": "high", "owner": "operator", "status": "pending", "required_before": "manual upload/API publish"})
    write_csv(output_csv, tasks, ["artifact", "review_type", "severity", "owner", "status", "required_before"])
    return output_csv


def render_ops_runbook(output_md: Path) -> Path:
    text = """# 100-Point Store Operations Runbook

## Daily Loop
1. Import yesterday KPI CSV or update `kpi_tracker.csv`.
2. Run `evaluate-kpi` and inspect stop/scale decisions.
3. Review CS/return issues before scaling ads or inventory.
4. Approve only low-risk drafts after proof/legal/operator gates.

## Weekly Loop
1. Add new market CSV rows and rerun `run-pipeline`.
2. Generate new listings, scan risks, and create review queue.
3. Produce printables and run print/readability review.
4. Export store import CSV for manual upload or API adapter staging.

## Hard Stop Rules
- Do not publish high-risk listing text.
- Do not claim guaranteed educational outcomes.
- Do not use copyrighted/trademarked characters without rights.
- Do not automate refunds, disputes, paid ads scaling, production deploy, secrets, or legal text without approval.

## 100-Point Definition
100 points means: data intake, scoring, listing drafts, risk scan, printable drafts, import CSV, KPI decisions, review queue, dashboard, proof gates, tests, and human approval gates all exist and are validated.
"""
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text(text, encoding="utf-8")
    return output_md


# ---------------------------------------------------------------------------
# 100-point integration layer: external commerce adapters, order/CS loop,
# image-generation planning, and patent/copyright precheck.
# These functions intentionally default to staging artifacts, not live actions.
# ---------------------------------------------------------------------------

PLATFORM_FIELDS = {
    "naver": ["platform", "external_sku", "product_name", "seo_title", "price", "stock_qty", "category_hint", "detail_file", "thumbnail_prompt", "visibility", "approval_required", "risk_severity", "ip_precheck_status", "live_publish_allowed"],
    "coupang": ["platform", "external_sku", "product_name", "sale_price", "search_tags", "detail_file", "thumbnail_prompt", "visibility", "approval_required", "risk_severity", "ip_precheck_status", "live_publish_allowed"],
    "shopify": ["platform", "handle", "title", "body_html_file", "vendor", "product_type", "tags", "published", "variant_price", "image_prompt", "approval_required", "risk_severity", "ip_precheck_status"],
}

KNOWN_IP_RISK_TERMS = [
    "포켓몬", "pokemon", "디즈니", "disney", "마블", "marvel", "산리오", "sanrio", "헬로키티", "카카오프렌즈", "라인프렌즈",
    "짱구", "도라에몽", "mickey", "마리오", "닌텐도", "lego", "레고", "bt21", "bts",
]
PATENT_RISK_TERMS = [
    "특허", "실용신안", "등록디자인", "디자인권", "상표", "라이선스", "캐릭터", "독점", "기술", "자동", "장치", "구조",
]


def _read_first_line(path: Path) -> str:
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8", errors="ignore").strip().splitlines()
    return text[0].lstrip("# ").strip() if text else ""


def ip_precheck_text(text: str) -> Dict[str, object]:
    """Rule-based preliminary IP/copyright/patent screening.
    This is not legal advice; it creates a review queue and search terms.
    """
    low = text.lower()
    hits = []
    for term in KNOWN_IP_RISK_TERMS:
        if term.lower() in low:
            hits.append(f"character/trademark candidate: {term}")
    for term in PATENT_RISK_TERMS:
        if term.lower() in low:
            hits.append(f"patent/design-right review keyword: {term}")
    if "100%" in text or "무조건" in text or "보장" in text:
        hits.append("unsupported guarantee claim may create advertising/legal risk")
    severity = "high" if any("character/trademark" in h for h in hits) else "medium" if hits else "low"
    status = "blocked_until_operator_ip_review" if severity == "high" else "needs_prelaunch_ip_check" if severity == "medium" else "draft_ok_with_source_log"
    queries = []
    base = re.sub(r"\s+", " ", text[:80]).strip()
    if base:
        queries.extend([
            f"KIPRIS 상표 검색: {base}",
            f"KIPRIS 디자인/특허 검색: {base}",
            f"한국저작권위원회 저작권 등록/분쟁 키워드 확인: {base}",
            f"플랫폼 금지어/브랜드 침해 검색: {base}",
        ])
    return {"severity": severity, "status": status, "finding_count": len(hits), "findings": "; ".join(hits), "search_queries": " | ".join(queries)}


def ip_precheck(input_path: Path, output_csv: Path) -> Path:
    rows = []
    paths = []
    if input_path.is_dir():
        paths = [p for p in sorted(input_path.rglob("*")) if p.suffix.lower() in {".md", ".txt", ".csv", ".html"}]
    else:
        paths = [input_path]
    for path in paths:
        text = path.read_text(encoding="utf-8", errors="ignore")
        result = ip_precheck_text(text)
        rows.append({"artifact": str(path), **result, "legal_note": "preliminary ai/rule screening only; operator or qualified professional must approve before public use"})
    write_csv(output_csv, rows, ["artifact", "severity", "status", "finding_count", "findings", "search_queries", "legal_note"])
    return output_csv


def generate_image_plan(scores_csv: Path, listings_dir: Path, output_csv: Path, style: str = "warm clean korean mom lifestyle printable") -> Path:
    rows = []
    for r in load_scores(scores_csv):
        product = r.get("product", "상품")
        listing = listings_dir / f"{slug(product)}.md"
        detail = _read_first_line(listing)
        risk = ip_precheck_text(product + " " + detail)
        rows.append({
            "product": product,
            "image_type": "thumbnail",
            "prompt": f"{style}, original non-character design, {product}, neat printable stationery, no famous characters, no logo, high readability, ecommerce thumbnail",
            "negative_prompt": "famous character, brand logo, disney, pokemon, sanrio, copyrighted mascot, celebrity, trademarked design",
            "size": "1024x1024",
            "approval_required": "design proof + IP precheck + operator approval",
            "ip_precheck_status": risk["status"],
            "public_use_allowed": "no",
        })
        rows.append({
            "product": product,
            "image_type": "detail_page_section",
            "prompt": f"{style}, A4 printable preview for {product}, Korean text placeholders, clean blocks, parent-friendly guide layout, original icons only",
            "negative_prompt": "copyrighted characters, brand logo, guaranteed academic claims, medical claims",
            "size": "1280x720",
            "approval_required": "readability proof + claim review + operator approval",
            "ip_precheck_status": risk["status"],
            "public_use_allowed": "no",
        })
    write_csv(output_csv, rows, ["product", "image_type", "prompt", "negative_prompt", "size", "approval_required", "ip_precheck_status", "public_use_allowed"])
    return output_csv


def export_platform_payloads(scores_csv: Path, listings_dir: Path, output_dir: Path) -> list[Path]:
    """Create API/CSV staging payloads for Naver, Coupang, Shopify.
    No live API call is made; credentials and publish endpoints require operator approval.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    rows = load_scores(scores_csv)
    outputs = []
    for platform, fields in PLATFORM_FIELDS.items():
        platform_rows = []
        for r in rows:
            product = r.get("product", "상품")
            sku = slug(product)
            listing = listings_dir / f"{sku}.md"
            risk = scan_text_risk((listing.read_text(encoding="utf-8", errors="ignore") if listing.exists() else product))
            ip = ip_precheck_text(product + " " + (listing.read_text(encoding="utf-8", errors="ignore") if listing.exists() else ""))
            if platform == "shopify":
                platform_rows.append({"platform": platform, "handle": sku, "title": product, "body_html_file": str(listing), "vendor": "operator-approved", "product_type": "printable", "tags": r.get("keyword", ""), "published": "false", "variant_price": r.get("price", ""), "image_prompt": f"original clean printable thumbnail for {product}", "approval_required": "operator+legal+ip", "risk_severity": risk["severity"], "ip_precheck_status": ip["status"]})
            elif platform == "coupang":
                platform_rows.append({"platform": platform, "external_sku": sku, "product_name": product, "sale_price": r.get("price", ""), "search_tags": r.get("keyword", ""), "detail_file": str(listing), "thumbnail_prompt": f"original clean printable thumbnail for {product}", "visibility": "staged_only", "approval_required": "operator+legal+ip", "risk_severity": risk["severity"], "ip_precheck_status": ip["status"], "live_publish_allowed": "false"})
            else:
                platform_rows.append({"platform": platform, "external_sku": sku, "product_name": product, "seo_title": f"{product} | 생활관리 프린트물", "price": r.get("price", ""), "stock_qty": "digital_or_operator_defined", "category_hint": "생활/문구/디지털파일", "detail_file": str(listing), "thumbnail_prompt": f"original clean printable thumbnail for {product}", "visibility": "unpublished", "approval_required": "operator+legal+ip", "risk_severity": risk["severity"], "ip_precheck_status": ip["status"], "live_publish_allowed": "false"})
        out = output_dir / f"{platform}_api_staging.csv"
        write_csv(out, platform_rows, fields)
        outputs.append(out)
    spec = output_dir / "platform_api_connector_spec.md"
    spec.write_text("""# Platform API Connector Spec\n\nThis folder contains staging payloads for Naver SmartStore, Coupang, and Shopify.\n\n## Live API rule\n- Do not call live publish, price change, stock change, refund, ad spend, or customer message endpoints without operator approval.\n- Store real credentials only in platform secret managers or deployment secrets, never in this skill or repo.\n- Every live action requires an audit event: actor, timestamp, payload hash, approval id, rollback note.\n\n## Adapter modes\n1. CSV staging: safest beginner mode.\n2. API dry-run: validate payloads against schemas without publishing.\n3. Approved live action: only after operator approval and proof gate.\n""", encoding="utf-8")
    outputs.append(spec)
    return outputs


def ingest_orders(order_csv: Path, output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    orders = read_csv(order_csv)
    fulfillment = []
    cs = []
    shipping = []
    for o in orders:
        order_id = o.get("order_id") or o.get("주문번호") or o.get("id") or "unknown"
        product = o.get("product") or o.get("상품명") or "상품"
        status = (o.get("status") or o.get("상태") or "paid").lower()
        message = o.get("customer_message") or o.get("문의") or ""
        paid = str(o.get("paid", "true")).lower() in {"true", "1", "yes", "paid", "결제완료"}
        fulfillment_status = "hold_operator_review" if not paid or "refund" in status or "cancel" in status else "ready_to_prepare"
        fulfillment.append({"order_id": order_id, "product": product, "fulfillment_status": fulfillment_status, "required_action": "operator approve shipping/print" if fulfillment_status.startswith("hold") else "prepare printable/download or packing", "audit_required": "yes"})
        if message:
            c = classify_cs_message(message)
            cs.append({"order_id": order_id, "product": product, "message": message, "category": c["category"], "triage": c["triage"], "auto_reply_allowed": c["auto_reply_allowed"], "matched_rules": c["matched_rules"]})
        shipping.append({"order_id": order_id, "product": product, "carrier": o.get("carrier", "operator_select"), "tracking_no": o.get("tracking_no", ""), "shipping_action": "manual_or_api_staging", "live_update_allowed": "false"})
    f1 = output_dir / "fulfillment_queue.csv"; write_csv(f1, fulfillment, ["order_id", "product", "fulfillment_status", "required_action", "audit_required"])
    f2 = output_dir / "cs_triage.csv"; write_csv(f2, cs, ["order_id", "product", "message", "category", "triage", "auto_reply_allowed", "matched_rules"])
    f3 = output_dir / "shipping_update_staging.csv"; write_csv(f3, shipping, ["order_id", "product", "carrier", "tracking_no", "shipping_action", "live_update_allowed"])
    return [f1, f2, f3]


def render_live_integration_runbook(output_md: Path) -> Path:
    text = """# Live Commerce Integration Runbook\n\n## Purpose\nMove from CSV staging to approved API integration for Naver SmartStore, Coupang, Shopify, order intake, shipping updates, CS triage, and image workflows.\n\n## Required adapters\n- Product adapter: create/update product payloads, but default to draft/unpublished.\n- Order adapter: import order CSV/API feed into fulfillment queue.\n- Shipping adapter: stage tracking updates; live update only after approval.\n- CS adapter: classify customer messages; angry/refund/legal messages must escalate.\n- Image adapter: generate prompts and design briefs; public image use requires IP/readability/operator approval.\n- IP precheck adapter: scan patent/design/trademark/copyright risk and create search queries.\n\n## Human approval gates\nLive publish, paid ad scaling, refund denial, legal text, trademark/character use, production image use, domain/secret/payment changes, and destructive migrations are L0 human-only unless explicitly approved.\n\n## Evidence required before 100-point claim\n- API payload dry-run logs.\n- Secret storage proof.\n- Webhook signature validation proof.\n- Rollback plan for product price/stock/listing changes.\n- CS escalation samples.\n- IP precheck CSV with no high-risk blockers or approved exceptions.\n"""
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text(text, encoding="utf-8")
    return output_md


# --- 3rd upgrade: connector separation, order state machine, kill-switch, CS/IP/audit hardening ---
CONNECTOR_CAPABILITIES = {
    "naver": ["product_staging", "stock_staging", "order_import", "shipping_staging"],
    "coupang": ["product_staging", "order_import", "shipping_staging", "cs_import"],
    "shopify": ["product_staging", "draft_publish", "order_webhook", "fulfillment_staging"],
}
ORDER_STATES = ["draft", "paid", "proof_pending", "prepare", "shipped", "delivered", "cancel_requested", "refund_review", "refunded", "closed", "hold_operator"]
CS_RULES = [
    ("legal_threat", re.compile(r"고소|소송|법적|신고|내용증명", re.I), "operator_escalation", "no"),
    ("refund_dispute", re.compile(r"환불|반품|취소|돈.*돌려", re.I), "operator_escalation", "no"),
    ("angry_customer", re.compile(r"화남|짜증|불만|최악|사기|속았다", re.I), "operator_escalation", "no"),
    ("shipping_question", re.compile(r"배송|운송장|언제|도착", re.I), "template_reply_draft", "after template approval"),
    ("download_access", re.compile(r"다운로드|파일|pdf|링크|메일", re.I), "template_reply_draft", "after template approval"),
    ("custom_request", re.compile(r"수정|변경|이름|문구|커스텀", re.I), "operator_review", "no"),
]

def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8', errors='ignore')).hexdigest()[:16]


def build_connector_manifest(output_dir: Path) -> list[Path]:
    """Create separated platform connector specs for future live API implementation.
    This still does not call live APIs; it defines boundaries, payload ownership, and approval gates.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    matrix=[]; manifest={"mode":"staging_first", "live_default":"disabled", "connectors":{}}
    for platform, caps in CONNECTOR_CAPABILITIES.items():
        manifest["connectors"][platform] = {
            "capabilities": caps,
            "credential_storage": "external secret manager only",
            "live_publish_allowed": False,
            "required_gates": ["schema_validation", "dry_run_log", "operator_approval", "rollback_plan", "audit_event"],
            "dangerous_actions": ["live_publish", "price_change", "stock_change", "refund", "paid_ad_spend", "customer_message_send"],
        }
        for cap in caps:
            matrix.append({"platform":platform,"capability":cap,"default_mode":"csv/api_staging","live_allowed":"false","approval_required":"operator+proof+rollback","secret_policy":"never_in_repo"})
        adapter = output_dir / f"{platform}_connector_contract.md"
        adapter.write_text(f"""# {platform.title()} Connector Contract\n\n## Default\n- Mode: CSV/API staging only.\n- Live calls: disabled until operator approval, dry-run proof, webhook/secret proof, and rollback plan exist.\n\n## Capabilities\n{chr(10).join('- '+c for c in caps)}\n\n## Required implementation interface\n```text\nvalidate_payload(payload) -> validation report\ndry_run(payload) -> dry-run log\nrequest_operator_approval(payload_hash) -> approval id\nlive_execute(payload, approval_id) -> result log\nrollback(result_log) -> rollback plan/result\nwrite_audit_event(action, payload_hash, approval_id, actor) -> audit row\n```\n\n## Hard blocks\nNo credential in repo. No publish/refund/price/customer-message live action without approval.\n""", encoding='utf-8')
    manifest_path=output_dir/'connector_manifest.json'
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    matrix_path=output_dir/'api_connector_matrix.csv'
    write_csv(matrix_path, matrix, ["platform","capability","default_mode","live_allowed","approval_required","secret_policy"])
    return [manifest_path, matrix_path] + sorted(output_dir.glob('*_connector_contract.md'))


def transition_order_state(current: str, event: str, paid: bool=True, proof_ok: bool=False, shipped: bool=False) -> Dict[str, str]:
    current=(current or 'draft').lower(); event=(event or '').lower()
    decision='hold_operator'; reason='unrecognized transition requires operator review'
    if event in {'cancel','cancel_requested'}:
        decision='cancel_requested'; reason='customer/platform cancellation request'
    elif event in {'refund','refund_requested','return'}:
        decision='refund_review'; reason='refund/return requires operator policy review'
    elif current in {'draft','created'} and paid:
        decision='paid'; reason='payment confirmed; proof gate required before preparation'
    elif current=='paid' and proof_ok:
        decision='prepare'; reason='proof approved; prepare digital/physical fulfillment'
    elif current in {'prepare','proof_pending'} and shipped:
        decision='shipped'; reason='shipping/tracking confirmed'
    elif current=='shipped' and event=='delivered':
        decision='delivered'; reason='delivery confirmed'
    elif current=='delivered' and event in {'close','complete'}:
        decision='closed'; reason='order completed'
    elif not paid:
        decision='hold_operator'; reason='payment not confirmed'
    return {"from_state": current, "event": event, "to_state": decision, "reason": reason, "live_update_allowed": "false", "audit_required": "yes"}


def create_order_state_machine(order_csv: Path, output_csv: Path) -> Path:
    rows=[]
    for o in read_csv(order_csv):
        current=o.get('state') or o.get('status') or 'created'
        event=o.get('event') or o.get('상태') or current
        paid=str(o.get('paid','true')).lower() in {'true','1','yes','paid','결제완료'}
        proof_ok=str(o.get('proof_ok','false')).lower() in {'true','1','yes','pass'}
        shipped=bool(o.get('tracking_no') or str(o.get('shipped','false')).lower() in {'true','1','yes'})
        t=transition_order_state(current,event,paid,proof_ok,shipped)
        rows.append({"order_id":o.get('order_id') or o.get('주문번호') or 'unknown', **t, "operator_gate":"required_before_live_platform_update"})
    write_csv(output_csv, rows, ["order_id","from_state","event","to_state","reason","live_update_allowed","audit_required","operator_gate"])
    return output_csv


def classify_cs_message(message: str) -> Dict[str, str]:
    text=message or ''
    hits=[]
    final=("general", "template_reply_draft", "after template approval")
    for category, pattern, triage, auto in CS_RULES:
        if pattern.search(text):
            hits.append(category)
            if triage == 'operator_escalation':
                final=(category, triage, auto); break
            if final[1] != 'operator_escalation':
                final=(category, triage, auto)
    if not hits:
        hits=['general']
    return {"category": final[0], "triage": final[1], "auto_reply_allowed": final[2], "matched_rules": ";".join(hits)}


def auto_pause_rules(kpi_csv: Path, cs_csv: Path | None, risk_csv: Path | None, output_csv: Path) -> Path:
    kpis=read_csv(kpi_csv) if kpi_csv.exists() else []
    cs_rows=read_csv(cs_csv) if cs_csv and cs_csv.exists() else []
    risk_rows=read_csv(risk_csv) if risk_csv and risk_csv.exists() else []
    cs_escalations=sum(1 for r in cs_rows if 'escalation' in (r.get('triage','') + r.get('category','')))
    high_risk=sum(1 for r in risk_rows if r.get('severity')=='high')
    out=[]
    for r in kpis:
        views=num(r.get('views',0)); clicks=num(r.get('clicks',0)); orders=num(r.get('orders',0)); returns=num(r.get('returns',0)); ad=num(r.get('ad_spend',0)); revenue=num(r.get('revenue',0)); cs=num(r.get('cs_tickets',0))
        roas=(revenue/ad*100) if ad else 0; return_rate=(returns/orders*100) if orders else 0; ctr=(clicks/views*100) if views else 0
        action='continue_collecting_data'; reasons=[]
        if high_risk: action='hard_pause'; reasons.append('high IP/claims risk exists')
        if ad >= 30000 and roas < 120: action='pause_ads'; reasons.append('ad spend with low ROAS')
        if orders and return_rate > 12: action='pause_listing'; reasons.append('return rate above 12%')
        if cs > max(2, orders): action='pause_and_fix_cs'; reasons.append('CS volume exceeds order count')
        if cs_escalations >= 2: action='operator_review_required'; reasons.append('multiple escalated CS messages')
        if views >= 300 and ctr < 1 and action == 'continue_collecting_data': action='improve_thumbnail_title'; reasons.append('low CTR')
        out.append({**r, 'ctr_percent':round(ctr,2), 'roas_percent':round(roas,1), 'return_rate_percent':round(return_rate,2), 'kill_switch_action':action, 'reasons':'; '.join(reasons) or 'no hard stop triggered', 'operator_approval_required':'yes' if action!='continue_collecting_data' else 'no'})
    fields=list(out[0].keys()) if out else ['kill_switch_action','reasons']
    write_csv(output_csv,out,fields)
    return output_csv


def create_audit_log(ops_dir: Path, output_csv: Path) -> Path:
    rows=[]
    for path in sorted(ops_dir.rglob('*')):
        if path.is_file() and path.suffix.lower() in {'.csv','.md','.json','.html','.txt'}:
            text=path.read_text(encoding='utf-8', errors='ignore')
            risk='high' if any(w in text for w in ['live_publish_allowed=true','환불 불가','100% 보장']) else 'normal'
            rows.append({"timestamp":datetime.now().isoformat(timespec='seconds'),"artifact":str(path.relative_to(ops_dir)),"payload_hash":sha256_text(text),"actor":"ai_staging_harness","approval_id":"pending_operator" if risk=='high' else "not_required_for_draft","risk_level":risk,"rollback_note":"restore previous artifact or keep unpublished staging"})
    write_csv(output_csv, rows, ["timestamp","artifact","payload_hash","actor","approval_id","risk_level","rollback_note"])
    return output_csv


def sample_data(output_csv: Path) -> Path:
    rows = [
        {"keyword":"칭찬스티커판","product":"초등 칭찬스티커 세트","demand":78,"competition":55,"margin":72,"production":86,"repeat":58,"risk":18,"price":7900,"cost":1600},
        {"keyword":"주간 식단표","product":"냉장고 주간 식단표 PDF","demand":73,"competition":62,"margin":88,"production":90,"repeat":45,"risk":12,"price":5900,"cost":500},
        {"keyword":"공부체크표","product":"초등 공부습관 체크표","demand":70,"competition":58,"margin":82,"production":88,"repeat":50,"risk":16,"price":6900,"cost":700},
        {"keyword":"가계부 pdf","product":"주부 생활비 가계부 PDF","demand":68,"competition":72,"margin":90,"production":80,"repeat":35,"risk":20,"price":9900,"cost":500},
    ]
    write_csv(output_csv, rows, list(rows[0].keys()))
    return output_csv


def run_pipeline(input_csv: Path, output_dir: Path) -> None:
    scores = analyze_market(input_csv, output_dir)
    generate_listings(scores, output_dir / "listings")
    generate_calendar(scores, output_dir / "content_calendar.csv")
    init_kpi(output_dir / "kpi_tracker.csv")
    export_store_import(scores, output_dir / "listings", output_dir / "store_import.csv")
    scan_listing_risks(output_dir / "listings", output_dir / "risk_scan.csv")
    ip_precheck(output_dir / "listings", output_dir / "ip_precheck.csv")
    generate_image_plan(scores, output_dir / "listings", output_dir / "image_generation_plan.csv")
    export_platform_payloads(scores, output_dir / "listings", output_dir / "platform_api_staging")
    build_connector_manifest(output_dir / "connector_contracts")
    generate_printables("초등 칭찬스티커 세트", output_dir / "printables")
    create_review_queue(output_dir, output_dir / "operator_review_queue.csv")
    evaluate_kpi(output_dir / "kpi_tracker.csv", output_dir / "kpi_decisions.csv")
    auto_pause_rules(output_dir / "kpi_tracker.csv", None, output_dir / "risk_scan.csv", output_dir / "auto_pause_decisions.csv")
    create_audit_log(output_dir, output_dir / "audit_log.csv")
    render_ops_runbook(output_dir / "100_POINT_OPERATIONS_RUNBOOK.md")
    render_live_integration_runbook(output_dir / "LIVE_INTEGRATION_RUNBOOK.md")
    render_dashboard(output_dir, output_dir / "store-ops-dashboard.html")


def main() -> int:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    sd = sub.add_parser("sample-data"); sd.add_argument("--output", required=True)
    am = sub.add_parser("analyze-market"); am.add_argument("input_csv"); am.add_argument("--output", required=True)
    gl = sub.add_parser("generate-listings"); gl.add_argument("scores_csv"); gl.add_argument("--output", required=True); gl.add_argument("--limit", type=int, default=10)
    cc = sub.add_parser("content-calendar"); cc.add_argument("scores_csv"); cc.add_argument("--output", required=True); cc.add_argument("--days", type=int, default=30)
    ik = sub.add_parser("init-kpi"); ik.add_argument("--output", required=True)
    rd = sub.add_parser("render-dashboard"); rd.add_argument("ops_dir"); rd.add_argument("--output", required=True)
    sr = sub.add_parser("scan-risks"); sr.add_argument("input"); sr.add_argument("--output", required=True)
    ei = sub.add_parser("export-store-import"); ei.add_argument("scores_csv"); ei.add_argument("listings_dir"); ei.add_argument("--output", required=True); ei.add_argument("--platform", default="naver")
    gp = sub.add_parser("generate-printables"); gp.add_argument("product"); gp.add_argument("--output", required=True); gp.add_argument("--child-name", default="")
    ek = sub.add_parser("evaluate-kpi"); ek.add_argument("kpi_csv"); ek.add_argument("--output", required=True)
    rq = sub.add_parser("review-queue"); rq.add_argument("ops_dir"); rq.add_argument("--output", required=True)
    rb = sub.add_parser("ops-runbook"); rb.add_argument("--output", required=True)
    rp = sub.add_parser("run-pipeline"); rp.add_argument("input_csv"); rp.add_argument("--output", required=True)
    ipp = sub.add_parser("ip-precheck"); ipp.add_argument("input"); ipp.add_argument("--output", required=True)
    img = sub.add_parser("image-plan"); img.add_argument("scores_csv"); img.add_argument("listings_dir"); img.add_argument("--output", required=True); img.add_argument("--style", default="warm clean korean mom lifestyle printable")
    pp = sub.add_parser("platform-payloads"); pp.add_argument("scores_csv"); pp.add_argument("listings_dir"); pp.add_argument("--output", required=True)
    io = sub.add_parser("ingest-orders"); io.add_argument("order_csv"); io.add_argument("--output", required=True)
    lr = sub.add_parser("live-runbook"); lr.add_argument("--output", required=True)
    cm = sub.add_parser("connector-manifest"); cm.add_argument("--output", required=True)
    osm = sub.add_parser("order-state-machine"); osm.add_argument("order_csv"); osm.add_argument("--output", required=True)
    ap = sub.add_parser("auto-pause"); ap.add_argument("kpi_csv"); ap.add_argument("--cs-csv", default=""); ap.add_argument("--risk-csv", default=""); ap.add_argument("--output", required=True)
    al = sub.add_parser("audit-log"); al.add_argument("ops_dir"); al.add_argument("--output", required=True)
    args = p.parse_args()
    if args.cmd == "sample-data": print(sample_data(Path(args.output)))
    elif args.cmd == "analyze-market": print(analyze_market(Path(args.input_csv), Path(args.output)))
    elif args.cmd == "generate-listings": print("\n".join(str(p) for p in generate_listings(Path(args.scores_csv), Path(args.output), args.limit)))
    elif args.cmd == "content-calendar": print(generate_calendar(Path(args.scores_csv), Path(args.output), args.days))
    elif args.cmd == "init-kpi": print(init_kpi(Path(args.output)))
    elif args.cmd == "render-dashboard": print(render_dashboard(Path(args.ops_dir), Path(args.output)))
    elif args.cmd == "scan-risks": print(scan_listing_risks(Path(args.input), Path(args.output)))
    elif args.cmd == "export-store-import": print(export_store_import(Path(args.scores_csv), Path(args.listings_dir), Path(args.output), args.platform))
    elif args.cmd == "generate-printables": print("\n".join(str(p) for p in generate_printables(args.product, Path(args.output), args.child_name)))
    elif args.cmd == "evaluate-kpi": print(evaluate_kpi(Path(args.kpi_csv), Path(args.output)))
    elif args.cmd == "review-queue": print(create_review_queue(Path(args.ops_dir), Path(args.output)))
    elif args.cmd == "ops-runbook": print(render_ops_runbook(Path(args.output)))
    elif args.cmd == "ip-precheck": print(ip_precheck(Path(args.input), Path(args.output)))
    elif args.cmd == "image-plan": print(generate_image_plan(Path(args.scores_csv), Path(args.listings_dir), Path(args.output), args.style))
    elif args.cmd == "platform-payloads": print("\n".join(str(p) for p in export_platform_payloads(Path(args.scores_csv), Path(args.listings_dir), Path(args.output))))
    elif args.cmd == "ingest-orders": print("\n".join(str(p) for p in ingest_orders(Path(args.order_csv), Path(args.output))))
    elif args.cmd == "live-runbook": print(render_live_integration_runbook(Path(args.output)))
    elif args.cmd == "connector-manifest": print("\n".join(str(p) for p in build_connector_manifest(Path(args.output))))
    elif args.cmd == "order-state-machine": print(create_order_state_machine(Path(args.order_csv), Path(args.output)))
    elif args.cmd == "auto-pause": print(auto_pause_rules(Path(args.kpi_csv), Path(args.cs_csv) if args.cs_csv else None, Path(args.risk_csv) if args.risk_csv else None, Path(args.output)))
    elif args.cmd == "audit-log": print(create_audit_log(Path(args.ops_dir), Path(args.output)))
    elif args.cmd == "run-pipeline": run_pipeline(Path(args.input_csv), Path(args.output)); print(Path(args.output))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
