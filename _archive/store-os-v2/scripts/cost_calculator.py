#!/usr/bin/env python3
"""비용 계산기 - 단계별 월간 비용 예측"""
import argparse
from dataclasses import dataclass

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
    
    def breakeven_revenue(self, margin_rate: float = 0.3) -> float:
        """손익분기점 매출 (비용이 매출의 5% 이하일 때)"""
        return self.total / 0.05

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
        claude_api=0.0,  # 웹 인터페이스 사용
        infrastructure=0.0,  # 네이버 스마트스토어
        image_gen=0.0,  # Canva 무료
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
        image_gen=0.0,  # Canva Pro $13/월은 선택
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
        print(f"  - 상품 설명, CS 초안, 주문 확인")
    elif estimate.stage == "Full":
        print(f"  - 대량 처리 (제품 분석, 마케팅 자동화 포함)")
    
    print(f"\n인프라: ${estimate.infrastructure:.2f}")
    if estimate.stage == "Standard":
        print(f"  - Vercel Hobby: $0 (무료)")
        print(f"  - 도메인: $1")
    elif estimate.stage == "Full":
        print(f"  - Railway PostgreSQL: $5")
        print(f"  - Railway Redis: $5")
        print(f"  - Railway Web Service: $20")
        print(f"  - 도메인: $1")
    
    if estimate.image_gen > 0:
        print(f"\n이미지 생성: ${estimate.image_gen:.2f}")
        print(f"  - DALL-E 3 또는 Midjourney")
    
    if estimate.monitoring > 0:
        print(f"\n모니터링: ${estimate.monitoring:.2f}")
        print(f"  - Sentry (에러 추적)")
    
    print(f"\n{'─'*70}")
    print(f"💰 총 월간 비용: ${estimate.total:.2f}")
    
    if monthly_orders > 0:
        per_order = estimate.per_order(monthly_orders)
        print(f"📈 주문당 비용: ${per_order:.2f}")
    
    if monthly_revenue > 0:
        cost_ratio = (estimate.total / monthly_revenue) * 100
        print(f"📊 매출 대비 비용: {cost_ratio:.1f}%")
        
        if cost_ratio <= 5:
            print(f"   ✅ 건강한 비용 구조 (5% 이하)")
        elif cost_ratio <= 10:
            print(f"   ⚠️ 개선 필요 (10% 이하 목표)")
        else:
            print(f"   🚨 비용 과다 (매출 증대 또는 비용 절감 필요)")
    
    breakeven = estimate.breakeven_revenue()
    print(f"\n✅ 손익분기점 매출: {breakeven/10000:.0f}만원 (비용이 매출의 5% 이하)")

def compare_stages(
    monthly_products: int,
    monthly_orders: int,
    monthly_cs_tickets: int,
    monthly_revenue: int
):
    """단계별 비교"""
    mini = estimate_mini_stage()
    standard = estimate_standard_stage(monthly_products, monthly_orders, monthly_cs_tickets)
    full = estimate_full_stage(monthly_products, monthly_orders, monthly_cs_tickets)
    
    print(f"\n{'='*70}")
    print(f"📊 단계별 비용 비교")
    print(f"{'='*70}\n")
    
    print(f"{'단계':<15} {'Claude API':<15} {'인프라':<15} {'총 비용':<15} {'권장 매출':<15}")
    print(f"{'─'*70}")
    print(f"{'Mini':<15} ${mini.claude_api:<14.2f} ${mini.infrastructure:<14.2f} ${mini.total:<14.2f} {mini.breakeven_revenue()/10000:<14.0f}만원")
    print(f"{'Standard':<15} ${standard.claude_api:<14.2f} ${standard.infrastructure:<14.2f} ${standard.total:<14.2f} {standard.breakeven_revenue()/10000:<14.0f}만원")
    print(f"{'Full':<15} ${full.claude_api:<14.2f} ${full.infrastructure:<14.2f} ${full.total:<14.2f} {full.breakeven_revenue()/10000:<14.0f}만원")
    
    print(f"\n💡 추천:")
    if monthly_revenue < 500000:
        print(f"   → Mini 단계 (네이버 스마트스토어로 검증)")
    elif monthly_revenue < 3000000:
        print(f"   → Standard 단계 (자체 시스템 + AI 자동화)")
    else:
        print(f"   → Full 단계 (다채널 확장 + 고도 자동화)")

def main():
    parser = argparse.ArgumentParser(description="월간 비용 예측 계산기")
    parser.add_argument("--monthly-products", type=int, default=10, help="월간 신규 상품 수")
    parser.add_argument("--monthly-orders", type=int, default=100, help="월간 주문 수")
    parser.add_argument("--monthly-cs-tickets", type=int, default=20, help="월간 CS 문의 수")
    parser.add_argument("--monthly-revenue", type=int, default=1000000, help="월간 예상 매출 (원)")
    parser.add_argument("--stage", choices=["mini", "standard", "full", "all"], default="all", help="계산할 단계")
    
    args = parser.parse_args()
    
    if args.stage == "all":
        compare_stages(args.monthly_products, args.monthly_orders, args.monthly_cs_tickets, args.monthly_revenue)
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
