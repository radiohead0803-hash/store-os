#!/usr/bin/env python3
"""Claude API 자동 호출 - 상품 설명 자동 생성"""
import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

try:
    import anthropic
except ImportError:
    print("[ERROR] anthropic 패키지가 설치되지 않았습니다.")
    print("        설치: pip install anthropic")
    sys.exit(1)

def count_tokens_estimate(text: str) -> int:
    """토큰 수 추정 (실제로는 Claude가 계산)"""
    # 간단한 추정: 한글 1글자 ≈ 2 토큰, 영문 1단어 ≈ 1.3 토큰
    korean_chars = sum(1 for c in text if ord(c) >= 0xAC00 and ord(c) <= 0xD7A3)
    other_chars = len(text) - korean_chars
    return int(korean_chars * 2 + other_chars / 5)

def calculate_cost(input_tokens: int, output_tokens: int, model: str = "claude-sonnet-4-20250514") -> float:
    """비용 계산"""
    # Sonnet 4 pricing
    input_cost = (input_tokens / 1_000_000) * 3.0
    output_cost = (output_tokens / 1_000_000) * 15.0
    return input_cost + output_cost

def generate_product_listing(
    product: str,
    target: str,
    api_key: str,
    model: str = "claude-sonnet-4-20250514"
) -> tuple[str, dict]:
    """Claude API 호출하여 상품 설명 생성"""
    
    client = anthropic.Anthropic(api_key=api_key)
    
    prompt = f"""당신은 스마트스토어 상품 상세페이지 작성 전문가입니다.

상품명: {product}
타겟 고객: {target}

아래 형식으로 상품 설명을 작성해주세요:

# [매력적인 상품 제목]

## 이런 분들께 추천합니다
- 항목 1
- 항목 2
- 항목 3

## 상품 특징
1. **특징 1 제목**: 설명
2. **특징 2 제목**: 설명
3. **특징 3 제목**: 설명

## 구성품
- 구성 1
- 구성 2

## 사용 방법
1. 단계 1
2. 단계 2

## 주의사항
- 과대광고 금지: "100% 효과" 같은 표현 사용 금지
- 어린이 대상: "성적 향상" 대신 "학습 습관 형성 도구"로 표현
- 환불 정책 명시

## FAQ
Q: 질문 1?
A: 답변 1

Q: 질문 2?
A: 답변 2

---
**법률 준수 체크리스트**
- [ ] 과대광고 표현 없음
- [ ] 사업자 정보 표시됨
- [ ] 환불 정책 명확함
"""

    response = client.messages.create(
        model=model,
        max_tokens=4000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    content = response.content[0].text
    
    usage = {
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
        "cost": calculate_cost(response.usage.input_tokens, response.usage.output_tokens)
    }
    
    return content, usage

def save_listing(content: str, product: str, output_dir: Path, metadata: dict):
    """생성된 리스팅 저장"""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"listing_{timestamp}.md"
    filepath = output_dir / filename
    
    # 메타데이터 추가
    full_content = f"""---
product: {product}
generated_at: {datetime.now().isoformat()}
model: {metadata.get('model', 'unknown')}
cost: ${metadata['cost']:.4f}
---

{content}
"""
    
    filepath.write_text(full_content, encoding='utf-8')
    return filepath

def main():
    parser = argparse.ArgumentParser(description="Claude API로 상품 설명 자동 생성")
    parser.add_argument("--product", required=True, help="상품명")
    parser.add_argument("--target", default="초등학생 학부모", help="타겟 고객")
    parser.add_argument("--count", type=int, default=1, help="생성 개수")
    parser.add_argument("--save", default="listings/", help="저장 디렉토리")
    parser.add_argument("--model", default="claude-sonnet-4-20250514", help="Claude 모델")
    
    args = parser.parse_args()
    
    # API 키 확인
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY 환경변수가 설정되지 않았습니다.")
        print("   설정: export ANTHROPIC_API_KEY='sk-ant-...'")
        sys.exit(1)
    
    output_dir = Path(args.save)
    total_cost = 0.0
    generated_files = []
    
    print(f"\n🚀 상품 설명 생성 시작...")
    print(f"   상품: {args.product}")
    print(f"   타겟: {args.target}")
    print(f"   개수: {args.count}")
    print(f"   모델: {args.model}\n")
    
    for i in range(args.count):
        print(f"[{i+1}/{args.count}] 생성 중...", end=" ")
        
        try:
            content, usage = generate_product_listing(
                args.product,
                args.target,
                api_key,
                args.model
            )
            
            filepath = save_listing(
                content,
                args.product,
                output_dir,
                {"model": args.model, "cost": usage["cost"]}
            )
            
            total_cost += usage["cost"]
            generated_files.append(filepath)
            
            print(f"✅ {filepath.name}")
            print(f"   토큰: {usage['input_tokens']:,} input, {usage['output_tokens']:,} output")
            print(f"   비용: ${usage['cost']:.4f}\n")
            
        except Exception as e:
            print(f"❌ 실패: {e}\n")
    
    # 결과 요약
    print(f"{'='*60}")
    print(f"✅ 생성 완료: {len(generated_files)}개")
    print(f"💰 총 비용: ${total_cost:.4f}")
    print(f"📁 저장 위치: {output_dir.absolute()}")
    print(f"{'='*60}\n")
    
    if generated_files:
        print("🎯 다음 단계:")
        print(f"   1. 생성된 파일 검토: cat {generated_files[0]}")
        print(f"   2. 법률 체크: python scripts/legal_check.py {generated_files[0]}")
        print(f"   3. 네이버 업로드: python scripts/naver_integration.py --upload {generated_files[0]}")

if __name__ == "__main__":
    main()
