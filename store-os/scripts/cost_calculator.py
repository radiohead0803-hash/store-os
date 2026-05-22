#!/usr/bin/env python3
"""비용 계산기 - 단계별 월간 비용 예측"""
import argparse
import sys
import unicodedata
from dataclasses import dataclass

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

USD_TO_KRW = 1380  # 대략. 실제 환율은 변동. python scripts/cost_calculator.py --usd-krw 로 오버라이드 가능.

def pad_display(s: str, width: int) -> str:
    """동아시아 wide 문자(한글·전각)를 2-width로 계산해 패딩."""
    visual = sum(2 if unicodedata.east_asian_width(c) in ('W', 'F') else 1 for c in s)
    return s + ' ' * max(0, width - visual)

@dataclass
class CostEstimate:
    stage: str
    claude_api: float
    infrastructure: float
    image_gen: float
    monitoring: float
    total: float

    def per_order(self, monthly_orders: int) -> float:
        return self.total / monthly_orders if monthly_orders > 0 else 0

    def breakeven_revenue_krw(self, usd_to_krw: float = USD_TO_KRW) -> float:
        """손익분기점 매출(원). 비용이 매출의 5% 이하."""
        return (self.total * usd_to_krw) / 0.05

def calculate_claude_cost(
    monthly_products: int,
    monthly_orders: int,
    monthly_cs_tickets: int
) -> float:
    """Claude API 비용 계산"""
    # Sonnet 4 pricing: $3/M input, $15/M output

    # 상품 설명 생성 (2K input, 8K output per product)
    product_cost = monthly_products * ((2000 * 3 + 8000 * 15) / 1_000_000)

    # CS 초안 생성 (1K input, 3K output per ticket)
    cs_cost = monthly_cs_tickets * ((1000 * 3 + 3000 * 15) / 1_000_000)

    # 주문 확인 메시지 (500 input, 1K output per order)
    order_cost = monthly_orders * ((500 * 3 + 1000 * 15) / 1_000_000)

    return product_cost + cs_cost + order_cost

def estimate_mini_stage() -> CostEstimate:
    """Mini 단계 비용"""
    return CostEstimate(
        stage="Mini",
        claude_api=0.0,  # Claude 웹 (Pro 권장, 디자인+카피 모두 커버)
        infrastructure=0.0,  # 네이버 스마트스토어
        image_gen=0.0,  # Claude Design (Pro에 포함)
        monitoring=0.0,
        total=0.0
    )

def estimate_standard_stage(
    monthly_products: int,
    monthly_orders: int,
    monthly_cs_tickets: int
) -> CostEstimate:
    """Standard 단계 비용"""
    claude = calculate_claude_cost(monthly_products, monthly_orders, monthly_cs_tickets)

    # 인프라
    vercel = 0.0  # Hobby 플랜
    domain = 1.0  # 연 $12 / 12개월

    infra = vercel + domain

    return CostEstimate(
        stage="Standard",
        claude_api=claude,
        infrastructure=infra,
        image_gen=0.0,  # 별도 이미지 생성은 Standard 후반·Full에서 도입
        monitoring=0.0,
        total=claude + infra
    )

def estimate_full_stage(
    monthly_products: int,
    monthly_orders: int,
    monthly_cs_tickets: int
) -> CostEstimate:
    """Full 단계 비용"""
    claude = calculate_claude_cost(monthly_products, monthly_orders, monthly_cs_tickets)
    claude *= 5  # 대량 처리로 5배 증가

    # 인프라
    railway_db = 5.0
    railway_redis = 5.0
    railway_web = 20.0
    domain = 1.0

    infra = railway_db + railway_redis + railway_web + domain

    # 이미지 생성 (월 50개 가정)
    image = 50.0

    # 모니터링
    sentry = 26.0

    return CostEstimate(
        stage="Full",
        claude_api=claude,
        infrastructure=infra,
        image_gen=image,
        monitoring=sentry,
        total=claude + infra + image + sentry
    )

def print_cost_breakdown(estimate: CostEstimate, monthly_orders: int, monthly_revenue: int):
    """비용 상세 출력"""
    print(f"\n{'='*70}")
    print(f"📊 {estimate.stage} 단계 월간 비용 예측")
    print(f"{'='*70}\n")

    print(f"Claude API: ${estimate.claude_api:.2f}")
    if estimate.stage == "Standard":
        print("  - 상품 설명, CS 초안, 주문 확인")
    elif estimate.stage == "Full":
        print("  - 대량 처리 (제품 분석, 마케팅 자동화 포함)")

    print(f"\n인프라: ${estimate.infrastructure:.2f}")
    if estimate.stage == "Standard":
        print("  - Vercel Hobby: $0 (무료)")
        print("  - 도메인: $1")
    elif estimate.stage == "Full":
        print("  - Railway PostgreSQL: $5")
        print("  - Railway Redis: $5")
        print("  - Railway Web Service: $20")
        print("  - 도메인: $1")

    if estimate.image_gen > 0:
        print(f"\n이미지 생성: ${estimate.image_gen:.2f}")
        print("  - DALL-E 3 또는 Midjourney")

    if estimate.monitoring > 0:
        print(f"\n모니터링: ${estimate.monitoring:.2f}")
        print("  - Sentry (에러 추적)")

    print(f"\n{'─'*70}")
    print(f"💰 총 월간 비용: ${estimate.total:.2f}")

    if monthly_orders > 0:
        per_order = estimate.per_order(monthly_orders)
        print(f"📈 주문당 비용: ${per_order:.2f}")

    if monthly_revenue > 0:
        cost_ratio = (estimate.total / monthly_revenue) * 100
        print(f"📊 매출 대비 비용: {cost_ratio:.1f}%")

        if cost_ratio <= 5:
            print("   ✅ 건강한 비용 구조 (5% 이하)")
        elif cost_ratio <= 10:
            print("   ⚠️ 개선 필요 (10% 이하 목표)")
        else:
            print("   🚨 비용 과다 (매출 증대 또는 비용 절감 필요)")

    breakeven = estimate.breakeven_revenue_krw()
    print(f"\n✅ 손익분기점 매출: {breakeven/10000:.0f}만원 (비용이 매출의 5% 이하)")

def compare_stages(
    monthly_products: int,
    monthly_orders: int,
    monthly_cs_tickets: int,
    monthly_revenue: int,
    usd_to_krw: float = USD_TO_KRW,
):
    """단계별 비교"""
    mini = estimate_mini_stage()
    standard = estimate_standard_stage(monthly_products, monthly_orders, monthly_cs_tickets)
    full = estimate_full_stage(monthly_products, monthly_orders, monthly_cs_tickets)

    print(f"\n{'='*70}")
    print("📊 단계별 비용 비교")
    print(f"{'='*70}\n")

    header = (
        pad_display('단계', 12)
        + pad_display('Claude API', 14)
        + pad_display('인프라', 12)
        + pad_display('총 비용', 14)
        + pad_display('손익분기 매출', 18)
    )
    print(header)
    print('─' * 70)
    for est in (mini, standard, full):
        breakeven_krw = est.breakeven_revenue_krw(usd_to_krw)
        breakeven_label = f"{breakeven_krw/10000:,.0f}만원" if breakeven_krw > 0 else "—"
        row = (
            pad_display(est.stage, 12)
            + pad_display(f"${est.claude_api:.2f}", 14)
            + pad_display(f"${est.infrastructure:.2f}", 12)
            + pad_display(f"${est.total:.2f}", 14)
            + pad_display(breakeven_label, 18)
        )
        print(row)

    print("\n💡 추천:")
    if monthly_revenue < 500000:
        print("   → Mini 단계 (네이버 스마트스토어로 검증)")
    elif monthly_revenue < 3000000:
        print("   → Standard 단계 (자체 시스템 + AI 자동화)")
    else:
        print("   → Full 단계 (다채널 확장 + 고도 자동화)")

def main():
    parser = argparse.ArgumentParser(description="월간 비용 예측 계산기")
    parser.add_argument("--monthly-products", type=int, default=10, help="월간 신규 상품 수")
    parser.add_argument("--monthly-orders", type=int, default=100, help="월간 주문 수")
    parser.add_argument("--monthly-cs-tickets", type=int, default=20, help="월간 CS 문의 수")
    parser.add_argument("--monthly-revenue", type=int, default=1000000, help="월간 예상 매출 (원)")
    parser.add_argument("--stage", choices=["mini", "standard", "full", "all"], default="all", help="계산할 단계")
    parser.add_argument("--usd-krw", type=float, default=USD_TO_KRW, help=f"USD→KRW 환율 (기본 {USD_TO_KRW})")

    args = parser.parse_args()

    if args.stage == "all":
        compare_stages(args.monthly_products, args.monthly_orders, args.monthly_cs_tickets, args.monthly_revenue, args.usd_krw)
    elif args.stage == "mini":
        estimate = estimate_mini_stage()
        print_cost_breakdown(estimate, args.monthly_orders, args.monthly_revenue)
    elif args.stage == "standard":
        estimate = estimate_standard_stage(args.monthly_products, args.monthly_orders, args.monthly_cs_tickets)
        print_cost_breakdown(estimate, args.monthly_orders, args.monthly_revenue)
    elif args.stage == "full":
        estimate = estimate_full_stage(args.monthly_products, args.monthly_orders, args.monthly_cs_tickets)
        print_cost_breakdown(estimate, args.monthly_orders, args.monthly_revenue)

    print(f"\n{'='*70}\n")

if __name__ == "__main__":
    main()
