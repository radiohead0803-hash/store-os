#!/usr/bin/env python3
"""법률 준수 체크 - 전자상거래법/공정거래법/개인정보보호법 자동 점검"""
import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

@dataclass
class ComplianceIssue:
    level: str  # "ERROR", "WARNING", "INFO"
    category: str
    message: str
    line_number: int = 0
    suggestion: str = ""

def check_exaggeration(content: str) -> List[ComplianceIssue]:
    """과대광고 표현 체크"""
    issues = []

    # 금지 표현
    forbidden_patterns = [
        (r'100%', "100% 효과/보장 표현은 과대광고에 해당"),
        (r'완벽(한)?', "절대적 표현 지양 ('효과적인'으로 대체)"),
        (r'최고', "최상급 표현은 증명 필요 (삭제 권장)"),
        (r'1등', "순위 표현은 공정위 심사 기준 필요"),
        (r'모든', "절대적 표현 ('대부분의'로 완화)"),
        (r'반드시', "강제성 표현 지양"),
        (r'확실(한)?', "절대적 보장 표현 금지"),
    ]

    for pattern, message in forbidden_patterns:
        matches = list(re.finditer(pattern, content))
        if matches:
            issues.append(ComplianceIssue(
                level="ERROR",
                category="과대광고",
                message=f"❌ '{pattern}' 표현 발견 → {message}",
                suggestion="완화된 표현으로 수정 필요"
            ))

    return issues

def check_children_claims(content: str) -> List[ComplianceIssue]:
    """어린이 대상 제품 특별 규제"""
    issues = []

    child_keywords = ['초등', '어린이', '아동', '유아', '칭찬']
    is_child_product = any(kw in content for kw in child_keywords)

    if not is_child_product:
        return issues

    # 교육 효과 과대광고
    educational_patterns = [
        (r'성적\s*향상', "성적 향상 표현 금지 → '학습 습관 형성 도구'로 대체"),
        (r'집중력\s*증가', "집중력 증가 보장 금지 → '집중력 향상에 도움'으로 완화"),
        (r'IQ|지능\s*발달', "지능 발달 보장 표현 금지"),
        (r'두뇌\s*발달', "두뇌 발달 직접 연관 표현 주의"),
    ]

    for pattern, message in educational_patterns:
        if re.search(pattern, content):
            issues.append(ComplianceIssue(
                level="ERROR",
                category="어린이대상",
                message=f"🚨 {message}",
                suggestion="어린이 대상 제품은 교육 효과 과대광고 엄격 규제"
            ))

    return issues

def check_refund_policy(content: str) -> List[ComplianceIssue]:
    """환불 정책 명시 확인"""
    issues = []

    refund_keywords = ['환불', '반품', '교환', '취소']
    has_refund_policy = any(kw in content for kw in refund_keywords)

    if not has_refund_policy:
        issues.append(ComplianceIssue(
            level="ERROR",
            category="환불정책",
            message="❌ 환불/반품 정책이 명시되지 않음",
            suggestion="전자상거래법: 청약철회(7일) 및 예외 사유 명시 필수"
        ))

    # 디지털 상품 특별 규정
    digital_keywords = ['다운로드', 'PDF', '파일', '디지털']
    is_digital = any(kw in content for kw in digital_keywords)

    if is_digital and has_refund_policy:
        if '다운로드' in content and '전' in content:
            issues.append(ComplianceIssue(
                level="INFO",
                category="환불정책",
                message="✅ 디지털 상품 환불 정책 확인됨",
                suggestion="다운로드 전: 환불 가능 / 다운로드 후: 불가 (명시 필요)"
            ))
        else:
            issues.append(ComplianceIssue(
                level="WARNING",
                category="환불정책",
                message="⚠️ 디지털 상품 환불 예외 명확히 필요",
                suggestion="'파일 다운로드 전까지 7일 내 전액 환불 가능' 명시"
            ))

    return issues

def check_business_info(content: str) -> List[ComplianceIssue]:
    """사업자 정보 표시 확인"""
    issues = []

    required_info = [
        ('사업자', "사업자등록번호"),
        ('대표', "대표자명"),
        ('연락처|전화|이메일', "연락처"),
        ('주소', "사업장 주소"),
    ]

    missing = []
    for pattern, name in required_info:
        if not re.search(pattern, content):
            missing.append(name)

    if missing:
        issues.append(ComplianceIssue(
            level="ERROR",
            category="사업자정보",
            message=f"❌ 필수 정보 누락: {', '.join(missing)}",
            suggestion="전자상거래법 제10조: 사업자 정보 표시 의무"
        ))

    return issues

def check_privacy_statement(content: str) -> List[ComplianceIssue]:
    """개인정보처리방침 확인"""
    issues = []

    privacy_keywords = ['개인정보', '처리방침', '프라이버시']
    has_privacy = any(kw in content for kw in privacy_keywords)

    if not has_privacy:
        issues.append(ComplianceIssue(
            level="ERROR",
            category="개인정보",
            message="❌ 개인정보처리방침 미명시",
            suggestion="개인정보보호법: 개인정보처리방침 링크 또는 전문 필수"
        ))

    return issues

def check_trademark_risk(content: str) -> List[ComplianceIssue]:
    """상표권 침해 리스크"""
    issues = []

    # 유명 브랜드명 예시 (실제로는 더 많은 DB 필요)
    famous_brands = ['디즈니', 'Disney', '뽀로로', '캐리', '포켓몬', 'Pokemon']

    for brand in famous_brands:
        if brand in content:
            issues.append(ComplianceIssue(
                level="WARNING",
                category="상표권",
                message=f"⚠️ 유명 브랜드명 '{brand}' 발견",
                suggestion="상표권 사용 허가 없이 상품명/설명 사용 금지 (고소 위험)"
            ))

    return issues

def generate_report(issues: List[ComplianceIssue], filepath: str):
    """종합 리포트 생성"""
    errors = [i for i in issues if i.level == "ERROR"]
    warnings = [i for i in issues if i.level == "WARNING"]
    infos = [i for i in issues if i.level == "INFO"]

    print(f"\n{'='*70}")
    print(f"📋 법률 준수 체크 리포트: {filepath}")
    print(f"{'='*70}\n")

    if errors:
        print(f"🚨 필수 조치 사항 ({len(errors)}개):")
        for i, issue in enumerate(errors, 1):
            print(f"\n{i}. [{issue.category}] {issue.message}")
            if issue.suggestion:
                print(f"   💡 {issue.suggestion}")

    if warnings:
        print(f"\n⚠️  권고 사항 ({len(warnings)}개):")
        for i, issue in enumerate(warnings, 1):
            print(f"\n{i}. [{issue.category}] {issue.message}")
            if issue.suggestion:
                print(f"   💡 {issue.suggestion}")

    if infos:
        print(f"\n✅ 확인 사항 ({len(infos)}개):")
        for issue in infos:
            print(f"   {issue.message}")

    print(f"\n{'─'*70}")

    if errors:
        print(f"\n❌ 상품 등록 불가: {len(errors)}개 필수 조치 필요")
        print(f"   수정 후 재검사: python scripts/legal_check.py {filepath}")
    elif warnings:
        print(f"\n⚠️  조건부 진행 가능: {len(warnings)}개 권고사항 검토 권장")
        print("   위험 감수하고 진행 또는 수정 후 재검사")
    else:
        print("\n✅ 법률 준수 통과: 등록 진행 가능")
        print(f"   다음: python scripts/naver_integration.py --upload {filepath}")

    print(f"\n{'='*70}\n")

def main():
    parser = argparse.ArgumentParser(description="전자상거래 법률 준수 체크")
    parser.add_argument("file", help="체크할 상품 설명 파일 (.md)")
    parser.add_argument("--strict", action="store_true", help="엄격 모드 (WARNING도 ERROR 처리)")

    args = parser.parse_args()

    filepath = Path(args.file)
    if not filepath.exists():
        print(f"❌ 파일을 찾을 수 없습니다: {filepath}")
        return

    content = filepath.read_text(encoding='utf-8')

    # 모든 체크 실행
    all_issues = []
    all_issues.extend(check_exaggeration(content))
    all_issues.extend(check_children_claims(content))
    all_issues.extend(check_refund_policy(content))
    all_issues.extend(check_business_info(content))
    all_issues.extend(check_privacy_statement(content))
    all_issues.extend(check_trademark_risk(content))

    # strict 모드에서는 WARNING을 ERROR로
    if args.strict:
        for issue in all_issues:
            if issue.level == "WARNING":
                issue.level = "ERROR"

    generate_report(all_issues, args.file)

if __name__ == "__main__":
    main()
