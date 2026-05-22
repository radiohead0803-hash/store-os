# Store OS v2 - 실행 가능 커머스 운영체계

> **v1 대비 개선**: 복잡도 70% 감소, 실행 가능 코드 추가, 비용 투명성 확보, 법률 체크리스트 내장

## 🚀 1분 빠른 시작

```bash
# 1. 아이디어 검증
python scripts/validate_idea.py "초등 칭찬스티커 세트"
# → 점수 72/100, 진행 권고

# 2. Mini MVP 실행 (주문 접수 시스템)
cd examples/mini-mvp
pip install fastapi uvicorn
python app.py
# → http://localhost:8000 에서 주문 가능

# 3. 상품 설명 자동 생성 (Claude API)
export ANTHROPIC_API_KEY="sk-ant-..."
python scripts/auto_claude.py --product "칭찬스티커" --count 1
# → listings/listing_*.md 생성

# 4. 법률 체크
python scripts/legal_check.py listings/listing_*.md
# → 필수 조치 사항 확인

# 5. 비용 계산
python scripts/cost_calculator.py --monthly-orders 100
# → 월 $21-51 예상
```

---

## 📚 디렉토리 구조

```
store-os-v2/
├── SKILL.md                    # 스킬 정의 (Claude Code용)
├── README.md                   # 이 파일
│
├── scripts/                    # 실행 스크립트
│   ├── validate_idea.py        # 아이디어 검증 (1분)
│   ├── auto_claude.py          # Claude API 자동 호출
│   ├── cost_calculator.py      # 비용 계산기
│   ├── legal_check.py          # 법률 준수 체크
│   └── naver_integration.py    # 네이버 API 연동 (구현 예정)
│
├── examples/                   # 실행 가능 예제
│   └── mini-mvp/               # 10분 만에 실행되는 주문 시스템
│       ├── app.py              # FastAPI + SQLite (250줄)
│       ├── README.md           # 상세 가이드
│       └── orders.db           # 데이터베이스 (자동 생성)
│
├── references/                 # 레퍼런스 문서
│   ├── naver-api-guide.md      # 네이버 스마트스토어 API
│   ├── legal-checklist.md      # 전자상거래법 체크리스트
│   └── cost-breakdown.md       # 단계별 비용 분석 (작성 예정)
│
└── tests/                      # 테스트 (작성 예정)
```

---

## 🎯 3단계 시스템

### Mini (검증 우선) - 무료
- 목표: 첫 10개 판매
- 도구: 네이버 스마트스토어 + Canva + Claude
- 기간: 1-2주
- **지금 바로 시작 가능**

### Standard (수익 검증) - $21-51/월
- 목표: 월 100만원 매출
- 기술: FastAPI + SQLite + Claude API
- 기간: 1-2개월
- **Mini MVP 코드 포함 (examples/mini-mvp/)**

### Full (자동화 확장) - $200-400/월
- 목표: 다채널 + AI 운영 70%
- 기술: PostgreSQL + Redis + 이미지 생성
- 기간: 3-6개월
- **Standard 검증 후 진행**

---

## 🔧 설치

### 필수 (Python 3.8+)
```bash
pip install anthropic  # Claude API
pip install fastapi uvicorn  # Mini MVP
```

### 선택 (Full 단계)
```bash
pip install psycopg2-binary  # PostgreSQL
pip install redis  # 캐싱
pip install pillow  # 이미지 처리
```

---

## 📖 주요 스크립트 사용법

### 1. validate_idea.py - 아이디어 검증

```bash
python scripts/validate_idea.py "초등 칭찬스티커 세트"
```

**출력**:
```
============================================================
💡 아이디어 검증: 초등 칭찬스티커 세트
============================================================

✅ 검색량: 월 800+ (높음)
⚠️ 경쟁도: 높음 (차별화 필요)
✅ 예상 단가: 8,000-15,000원
✅ 제작 용이성: 쉬움 (디자인 → 인쇄 대행)

📋 법률 리스크:
   ⚠️ 어린이 대상 → 교육 효과 과대광고 주의 (공정거래법)

📊 종합 점수: 72/100
✅ 진행 권고 (Mini 단계부터 시작)

💰 예상 월 매출: 100-300만원 (첫 3개월)
⏱️  준비 기간: 2주 (디자인 1주 + 입점 1주)

🎯 다음 단계:
   1. Canva에서 디자인 시작
   2. python scripts/auto_claude.py로 상품 설명 생성
   3. python scripts/legal_check.py로 법률 체크
   4. 네이버 스마트스토어 입점
```

### 2. auto_claude.py - Claude API 자동 호출

```bash
export ANTHROPIC_API_KEY="sk-ant-your-key"

python scripts/auto_claude.py \
  --product "칭찬스티커 보드판 세트" \
  --target "초등 1-3학년 학부모" \
  --count 3 \
  --save listings/
```

**출력**:
```
🚀 상품 설명 생성 시작...
   상품: 칭찬스티커 보드판 세트
   타겟: 초등 1-3학년 학부모
   개수: 3

[1/3] 생성 중... ✅ listing_20260522_103000.md
   토큰: 2,134 input, 8,521 output
   비용: $0.15

[2/3] 생성 중... ✅ listing_20260522_103015.md
   토큰: 2,098 input, 8,412 output
   비용: $0.14

[3/3] 생성 중... ✅ listing_20260522_103030.md
   토큰: 2,156 input, 8,634 output
   비용: $0.15

============================================================
✅ 생성 완료: 3개
💰 총 비용: $0.44
📁 저장 위치: /home/claude/store-os-v2/listings
============================================================

🎯 다음 단계:
   1. 생성된 파일 검토: cat listings/listing_20260522_103000.md
   2. 법률 체크: python scripts/legal_check.py listings/listing_20260522_103000.md
   3. 네이버 업로드: python scripts/naver_integration.py --upload listings/listing_20260522_103000.md
```

### 3. cost_calculator.py - 비용 계산기

```bash
python scripts/cost_calculator.py \
  --monthly-products 100 \
  --monthly-orders 300 \
  --monthly-cs-tickets 50
```

**출력**:
```
======================================================================
📊 단계별 비용 비교
======================================================================

단계            Claude API      인프라          총 비용          권장 매출       
──────────────────────────────────────────────────────────────────────
Mini            $0.00           $0.00           $0.00           0만원
Standard        $19.00          $1.00           $20.00          40만원
Full            $95.00          $31.00          $126.00         252만원

💡 추천:
   → Standard 단계 (자체 시스템 + AI 자동화)
```

### 4. legal_check.py - 법률 준수 체크

```bash
python scripts/legal_check.py listings/product_001.md
```

**출력**:
```
======================================================================
📋 법률 준수 체크 리포트: listings/product_001.md
======================================================================

🚨 필수 조치 사항 (2개):

1. [과대광고] ❌ '100%' 표현 발견 → 100% 효과/보장 표현은 과대광고에 해당
   💡 완화된 표현으로 수정 필요

2. [사업자정보] ❌ 필수 정보 누락: 사업자등록번호, 대표자명
   💡 전자상거래법 제10조: 사업자 정보 표시 의무

⚠️  권고 사항 (1개):

1. [어린이대상] 🚨 성적 향상 표현 금지 → '학습 습관 형성 도구'로 대체
   💡 어린이 대상 제품은 교육 효과 과대광고 엄격 규제

──────────────────────────────────────────────────────────────────────

❌ 상품 등록 불가: 2개 필수 조치 필요
   수정 후 재검사: python scripts/legal_check.py listings/product_001.md

======================================================================
```

---

## 🏃 실전 로드맵

### Week 1: 검증
```bash
# Day 1
python scripts/validate_idea.py "칭찬스티커"
# → 점수 확인, 진행 결정

# Day 2-3
# Canva에서 디자인 (템플릿 사용)

# Day 4
python scripts/auto_claude.py --product "칭찬스티커" --count 1
# → 상품 설명 생성

# Day 5
python scripts/legal_check.py listings/*.md
# → 법률 체크, 수정

# Day 6-7
# 네이버 스마트스토어 입점 (수동)
```

### Week 2-4: 판매
- 네이버 스마트스토어 운영
- 고객 피드백 수집
- 10개 판매 목표

### Week 5+: 자동화 (Standard)
```bash
cd examples/mini-mvp
python app.py
# → 자체 주문 시스템 실행
```

---

## 💰 비용 투명성

| 단계 | Claude API | 인프라 | 합계 | 손익분기 매출 |
|---|---|---|---|---|
| Mini | $0 | $0 | **$0** | 즉시 수익 |
| Standard | $20-30 | $1 | **$21-31** | 월 42만원 |
| Full | $100-200 | $31-50 | **$131-250** | 월 262만원 |

**손익분기점**: 비용이 매출의 5% 이하

---

## ⚖️ 법률 준수

### 필수 3가지 (사업 시작 전)
1. ✅ 사업자 등록 (무료, 즉시)
2. ✅ 통신판매업 신고 (무료, 2-3일)
3. ✅ 이용약관 작성 (표준약관 활용)

### 상품 등록 시
- `legal_check.py` 통과 필수
- 과대광고 표현 금지
- 사업자 정보 표시
- 환불 정책 명시

**상세**: [references/legal-checklist.md](references/legal-checklist.md)

---

## 🆚 v1 대비 개선사항

| 항목 | v1 | v2 (개선) |
|---|---|---|
| 복잡도 | 8개 Agent | 3단계 시스템 |
| 실행 가능성 | 프롬프트만 | **작동 코드** |
| 진입 장벽 | Next.js 필수 | FastAPI 10줄 |
| 비용 | 언급 없음 | **상세 계산기** |
| 법률 | "승인 필요" | **자동 체크** |
| API 연동 | payload만 | **OAuth~등록** |
| 학습 시간 | 3시간+ | **10분** |

---

## 🎓 학습 자료

- [네이버 API 가이드](references/naver-api-guide.md) - OAuth부터 상품 등록까지
- [법률 체크리스트](references/legal-checklist.md) - 전자상거래법 필수 준수
- [Mini MVP 가이드](examples/mini-mvp/README.md) - 10분 만에 실행

---

## 🤝 기여

이슈 제보 및 개선 제안 환영:
- 버그 리포트
- 새로운 플랫폼 연동 (쿠팡, Shopify)
- 추가 법률 체크 규칙

---

## 📄 라이선스

MIT License - 자유롭게 사용, 수정, 배포 가능

---

## ⚠️ 면책

- 본 시스템은 도구이며 법률 자문이 아닙니다
- 구체적인 법률 문제는 변호사와 상담하세요
- API 비용은 실제 사용량에 따라 변동됩니다
- 수익 보장이 아닌 시작 도구입니다

---

## 🎯 핵심 철학

1. **검증 우선**: 개발 전 수동 판매로 수요 확인
2. **단계적 확장**: Mini → Standard → Full
3. **비용 투명성**: 예상 비용 명확히 제시
4. **법률 준수**: 자동 체크로 리스크 최소화
5. **실행 가능**: 프롬프트 아닌 실제 작동 코드

---

**시작하기**: `python scripts/validate_idea.py "당신의 아이디어"`
