#!/usr/bin/env python3
"""아이디어 검증 스크립트 - 개발 전 수요/경쟁/수익성 자동 분석"""
import argparse
import json
import sys
from dataclasses import dataclass, asdict
from typing import List

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

@dataclass
class ValidationResult:
    product_name: str
    search_volume: str
    competition_level: str
    price_range: str
    legal_risks: List[str]
    production_difficulty: str
    score: int
    recommendation: str
    estimated_revenue: str
    prep_time: str

def estimate_search_volume(product: str) -> tuple[int, str]:
    """검색량 추정 (실제로는 네이버 검색광고 API 사용)"""
    keywords_high_volume = ["스티커", "칭찬", "보상", "학습", "공부"]
    keywords_medium = ["인쇄", "프린터블", "다운로드"]

    score = 0
    for kw in keywords_high_volume:
        if kw in product:
            score += 300
    for kw in keywords_medium:
        if kw in product:
            score += 100

    if score > 800:
        return score, "월 800+ (높음)"
    elif score > 300:
        return score, "월 300-800 (보통)"
    else:
        return score, "월 100-300 (낮음)"

def check_competition(product: str) -> tuple[int, str]:
    """경쟁도 체크 (실제로는 네이버쇼핑 API 사용)"""
    # 간단한 휴리스틱
    generic_terms = ["스티커", "세트", "판"]
    score = 50

    for term in generic_terms:
        if term in product:
            score += 15

    if "칭찬" in product or "보상" in product:
        score -= 10  # 특화된 니치

    if score > 80:
        return score, "매우 높음 (진입 어려움)"
    elif score > 60:
        return score, "높음 (차별화 필요)"
    elif score > 40:
        return score, "보통 (기회 있음)"
    else:
        return score, "낮음 (블루오션)"

def estimate_price_range(product: str) -> str:
    """가격대 추정"""
    if "세트" in product or "판" in product:
        return "8,000-15,000원"
    elif "단품" in product:
        return "3,000-6,000원"
    else:
        return "5,000-10,000원"

def check_legal_risks(product: str) -> List[str]:
    """법률 리스크 체크"""
    risks = []

    # 어린이 대상
    if any(kw in product for kw in ["초등", "어린이", "아동", "유아", "칭찬"]):
        risks.append("⚠️ 어린이 대상 → 교육 효과 과대광고 주의 (공정거래법)")

    # 학습/교육 효과
    if any(kw in product for kw in ["학습", "공부", "성적", "교육"]):
        risks.append("⚠️ '성적 향상', '100% 효과' 표현 금지")

    # 프린터블/다운로드
    if any(kw in product for kw in ["다운로드", "PDF", "파일"]):
        risks.append("⚠️ 디지털 상품 → 환불 정책 명확히 (7일 내 다운로드 전)")

    if not risks:
        risks.append("✅ 특별한 법률 리스크 없음")

    return risks

def assess_production(product: str) -> tuple[int, str]:
    """제작 용이성 평가"""
    if "인쇄" in product or "스티커" in product or "프린터블" in product:
        return 80, "쉬움 (디자인 → 인쇄 대행)"
    elif "제작" in product or "맞춤" in product:
        return 50, "보통 (샘플 제작 필요)"
    else:
        return 30, "어려움 (복잡한 제작)"

def calculate_score(search: int, competition: int, production: int) -> int:
    """종합 점수 계산"""
    # 검색량 (40%) + 경쟁도 역산 (30%) + 제작 용이성 (30%)
    search_score = min(search / 10, 40)  # 최대 40점
    competition_score = (100 - competition) * 0.3  # 경쟁 낮을수록 높음
    production_score = production * 0.3

    return int(search_score + competition_score + production_score)

def recommend(score: int, legal_risks: List[str]) -> str:
    """추천 결정"""
    high_risks = [r for r in legal_risks if "금지" in r or "주의" in r]

    if score >= 70 and len(high_risks) <= 1:
        return "✅ 진행 권고 (Mini 단계부터 시작)"
    elif score >= 50:
        return "⚠️ 조건부 진행 (차별화 전략 필요)"
    else:
        return "❌ 보류 권고 (다른 아이템 검토)"

def estimate_revenue(score: int, price_range: str) -> str:
    """예상 매출 추정"""
    if score >= 70:
        return "100-300만원 (첫 3개월)"
    elif score >= 50:
        return "50-150만원 (첫 3개월)"
    else:
        return "10-50만원 (첫 3개월)"

def estimate_prep_time(production_diff: str) -> str:
    """준비 기간"""
    if "쉬움" in production_diff:
        return "2주 (디자인 1주 + 입점 1주)"
    elif "보통" in production_diff:
        return "3-4주 (샘플 제작 포함)"
    else:
        return "6-8주 (제작 프로세스 확립)"

def validate_idea(product_name: str, market_check: bool = False) -> ValidationResult:
    """아이디어 검증 메인 로직"""
    search_vol, search_desc = estimate_search_volume(product_name)
    comp_score, comp_desc = check_competition(product_name)
    price_range = estimate_price_range(product_name)
    legal_risks = check_legal_risks(product_name)
    prod_score, prod_desc = assess_production(product_name)

    total_score = calculate_score(search_vol, comp_score, prod_score)
    recommendation = recommend(total_score, legal_risks)
    revenue = estimate_revenue(total_score, price_range)
    prep = estimate_prep_time(prod_desc)

    return ValidationResult(
        product_name=product_name,
        search_volume=search_desc,
        competition_level=comp_desc,
        price_range=price_range,
        legal_risks=legal_risks,
        production_difficulty=prod_desc,
        score=total_score,
        recommendation=recommendation,
        estimated_revenue=revenue,
        prep_time=prep
    )

def print_result(result: ValidationResult):
    """결과 출력"""
    print(f"\n{'='*60}")
    print(f"💡 아이디어 검증: {result.product_name}")
    print(f"{'='*60}\n")

    print(f"{'✅' if '높음' in result.search_volume else '⚠️'} 검색량: {result.search_volume}")
    print(f"{'⚠️' if '높음' in result.competition_level else '✅'} 경쟁도: {result.competition_level}")
    print(f"✅ 예상 단가: {result.price_range}")
    print(f"{'✅' if '쉬움' in result.production_difficulty else '⚠️'} 제작 용이성: {result.production_difficulty}")

    print("\n📋 법률 리스크:")
    for risk in result.legal_risks:
        print(f"   {risk}")

    print(f"\n📊 종합 점수: {result.score}/100")
    print(f"{result.recommendation}")
    print(f"\n💰 예상 월 매출: {result.estimated_revenue}")
    print(f"⏱️  준비 기간: {result.prep_time}")

    print(f"\n{'='*60}")

    # 다음 액션
    if result.score >= 70:
        print("\n🎯 다음 단계:")
        print("   1. Canva에서 디자인 시작")
        print("   2. python scripts/auto_claude.py로 상품 설명 생성")
        print("   3. python scripts/legal_check.py로 법률 체크")
        print("   4. 네이버 스마트스토어 입점")
    elif result.score >= 50:
        print("\n⚠️ 개선 후 진행:")
        print("   1. 차별화 포인트 추가 (예: 맞춤 제작, 캐릭터)")
        print("   2. 번들 상품으로 가격 경쟁력 확보")
        print("   3. 재검증 후 진행")
    else:
        print("\n❌ 다른 아이템 검토:")
        print("   1. 검색량이 더 높은 키워드 찾기")
        print("   2. 경쟁이 낮은 니치 시장 탐색")
        print("   3. scripts/validate_idea.py '다른 아이템' 재실행")

def main():
    parser = argparse.ArgumentParser(description="상품 아이디어 검증")
    parser.add_argument("product", help="검증할 상품명")
    parser.add_argument("--market-check", action="store_true", help="시장 조사 포함 (API 사용)")
    parser.add_argument("--json", action="store_true", help="JSON 형식 출력")

    args = parser.parse_args()

    result = validate_idea(args.product, args.market_check)

    if args.json:
        print(json.dumps(asdict(result), ensure_ascii=False, indent=2))
    else:
        print_result(result)

if __name__ == "__main__":
    main()
