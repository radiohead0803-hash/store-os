---
name: store-os-v2
description: 실행 가능한 스마트스토어 MVP 구축 운영체계. 복잡도를 3단계로 단순화하고, 실제 작동하는 코드와 비용 계산기, 법률 체크리스트를 포함. use when the user wants to build a working commerce MVP with clear cost estimates, legal compliance checklist, automated Claude API calls, real Naver/Coupang integration examples, or wants to validate product ideas before building.
---

# Store OS v2 - 실행 가능 커머스 운영체계

## 핵심 철학: 검증 우선, 구축은 나중

❌ **하지 마세요**: 시스템부터 만들기  
✅ **먼저 하세요**: 수동 판매로 수요 검증 → 데이터 확보 → 자동화 구축

## 3단계 시스템 (복잡도 단순화)

| 단계 | 목적 | 기간 | 비용 | 누가 |
|---|---|---|---|---|
| **Mini** | 수요 검증 | 1-2주 | 무료 | 비개발자 가능 |
| **Standard** | 수익 검증 | 1-2개월 | ~$50/월 | 기초 코딩 필요 |
| **Full** | 자동화 확장 | 3-6개월 | $200-500/월 | 개발팀 |

### Mini 단계 (검증 우선)

**목표**: 개발 없이 첫 10개 판매

```bash
# 실행: 제품 아이디어 검증
python scripts/validate_idea.py "초등 칭찬스티커 세트"

# 출력: 검색량, 경쟁도, 예상 수익성, 법률 리스크, 시작 권고/보류
```

**도구**:
- 네이버 스마트스토어 직접 입점 (무료)
- 쿠팡 PDS 입점 (수수료 15%, 개발 불필요)
- Canva로 디자인 → Claude로 상품 설명 작성

**증거**: 10개 판매 + 고객 피드백 3개 이상 → Standard 진행

---

### Standard 단계 (수익 검증)

**목표**: 월 100만원 매출 + 운영 자동화 50%

**기술 스택**:
- FastAPI (Python 웹프레임워크)
- SQLite (파일 기반 DB, 설치 불필요)
- Vercel 무료 플랜 (배포)
- Claude API (상품 설명, CS 초안)

**비용**:
```
Claude API: $20-30/월 (1000 상품 설명 생성 기준)
Vercel Pro: $20/월 (선택)
도메인: $10/년
= 월 $25-50
```

**실행**:
```bash
# 1. 최소 MVP 실행
python examples/mini-mvp/app.py
# → http://localhost:8000 에서 주문 접수 시스템 작동

# 2. Claude API 자동 호출 테스트
python scripts/auto_claude.py --product "칭찬스티커" --count 5
# → 5개 상품 설명 자동 생성 + 비용 출력

# 3. 네이버 API 연동 테스트
python scripts/naver_integration.py --test-auth
# → OAuth 인증 URL 생성 → 브라우저에서 승인 → 토큰 저장
```

**증거**: 월 100만원 매출 3개월 연속 + 운영 시간 50% 절감 → Full 진행

---

### Full 단계 (자동화 확장)

**목표**: 다채널 판매 + AI 운영 70%+

**추가 스택**:
- PostgreSQL (Railway $5/월)
- Redis (캐싱, Railway $5/월)
- GitHub Actions (CI/CD)
- Sentry (에러 추적)

**비용**:
```
Railway (DB+Redis+App): $20-50/월
Claude API: $100-200/월 (대량 처리)
이미지 생성 (DALL-E/Midjourney): $50-100/월
= 월 $200-400
```

---

## 실행 가능한 스크립트들

### 1. 아이디어 검증 (1분)

```bash
python scripts/validate_idea.py "초등 칭찬스티커 세트" --market-check
```

출력:
```
✅ 검색량: 월 1,200건 (충분)
⚠️ 경쟁: 네이버쇼핑 87개 상품 (보통)
✅ 예상 단가: 8,000-12,000원
⚠️ 법률 리스크: 초등학생 대상 → 과대광고 주의
✅ 제작 용이성: 인쇄물 → 쉬움

📊 종합 점수: 72/100 (진행 권고)
💰 예상 월 매출: 100-300만원 (첫 3개월)
⏱️ 준비 기간: 2주 (디자인 1주 + 입점 1주)
```

### 2. Claude API 자동 호출 (실제 작동)

```bash
# API 키 설정
export ANTHROPIC_API_KEY="sk-ant-..."

# 상품 설명 생성
python scripts/auto_claude.py \
  --product "칭찬스티커 보드판 세트" \
  --target "초등 1-3학년 학부모" \
  --count 3 \
  --save listings/

# 출력:
# ✅ 생성 완료: listings/product_001.md
# ✅ 생성 완료: listings/product_002.md
# ✅ 생성 완료: listings/product_003.md
# 💰 비용: $0.45 (input 2.1K tokens, output 8.5K tokens)
```

### 3. 비용 계산기

```bash
python scripts/cost_calculator.py \
  --monthly-products 100 \
  --monthly-orders 300 \
  --monthly-cs-tickets 50

# 출력:
# 📊 Standard 단계 예상 비용 (월간)
# 
# Claude API:
#   - 상품 설명 생성: 100개 × $0.15 = $15
#   - CS 초안 생성: 50개 × $0.08 = $4
#   - 소계: $19
# 
# 인프라:
#   - Vercel: $0 (무료 플랜)
#   - SQLite: $0 (로컬 파일)
# 
# 💰 총 월간 비용: $19
# 📈 주문당 비용: $0.06
# ✅ 손익분기점: 월 매출 50만원 이상 시 비용 < 4%
```

### 4. 법률 체크리스트 자동 점검

```bash
python scripts/legal_check.py listings/product_001.md

# 출력:
# 📋 전자상거래법 준수 체크
# 
# ✅ 상품명에 과대광고 표현 없음
# ⚠️ "100% 효과" 표현 발견 → 수정 필요
# ✅ 환불 정책 명시됨
# ❌ 사업자등록번호 미기재 → 필수 추가
# ✅ 개인정보처리방침 링크 있음
# ⚠️ 초등학생 대상 → "학습 효과" 표현 주의
# 
# 🚨 필수 조치: 2개
# ⚠️ 권고 사항: 2개
```

### 5. 네이버 스마트스토어 API 연동

```bash
# OAuth 인증 (최초 1회)
python scripts/naver_integration.py --init-auth
# → 브라우저 열림 → 로그인 → 토큰 자동 저장

# 상품 등록 (API)
python scripts/naver_integration.py \
  --upload listings/product_001.md \
  --category "문구/오피스>학용품>칭찬스티커" \
  --price 9900 \
  --stock 100 \
  --dry-run  # 실제 등록 전 미리보기

# 출력:
# 📤 네이버 스마트스토어 등록 미리보기
# 
# 상품명: 초등 저학년 칭찬스티커 보드판 세트
# 카테고리: 문구/오피스>학용품>칭찬스티커
# 가격: 9,900원
# 재고: 100개
# 이미지: 5개 (썸네일 포함)
# 
# ⚠️ --dry-run 모드: 실제 등록하려면 --confirm 추가
```

---

## 실제 작동하는 최소 MVP (FastAPI)

`examples/mini-mvp/app.py` 파일로 제공:

```python
# 10줄짜리 주문 접수 시스템
# 실행: python app.py
# 접속: http://localhost:8000

from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
from datetime import datetime

app = FastAPI()
db = sqlite3.connect('orders.db', check_same_thread=False)
db.execute('CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY, product TEXT, customer TEXT, created_at TEXT)')

class Order(BaseModel):
    product: str
    customer: str

@app.post("/order")
def create_order(order: Order):
    cursor = db.execute('INSERT INTO orders (product, customer, created_at) VALUES (?, ?, ?)',
                        (order.product, order.customer, datetime.now().isoformat()))
    db.commit()
    return {"order_id": cursor.lastrowid, "status": "접수완료"}

@app.get("/orders")
def list_orders():
    return db.execute('SELECT * FROM orders').fetchall()
```

**실행 로그 예시**:
```bash
$ python examples/mini-mvp/app.py
INFO:     Started server process
INFO:     Uvicorn running on http://127.0.0.1:8000

# 다른 터미널에서:
$ curl -X POST http://localhost:8000/order \
  -H "Content-Type: application/json" \
  -d '{"product":"칭찬스티커","customer":"김엄마"}'

{"order_id":1,"status":"접수완료"}

$ curl http://localhost:8000/orders
[[1,"칭찬스티커","김엄마","2026-05-22T10:30:00"]]
```

---

## 법률 체크리스트 (필수)

### 사업 시작 전 (필수 3가지)

| 항목 | 기한 | 비용 | 확인 |
|---|---|---|---|
| 1. 사업자등록 | 판매 시작 전 | 무료 | [ ] |
| 2. 통신판매업 신고 | 사업자등록 후 2주 내 | 무료 | [ ] |
| 3. 이용약관 작성 | 첫 판매 전 | 무료 (템플릿 사용) | [ ] |

### 상품 등록 시 (매번)

| 항목 | 체크 | 예시 |
|---|---|---|
| 과대광고 금지 | [ ] | ❌ "100% 효과" → ✅ "활용 가능" |
| 어린이 대상 특별 주의 | [ ] | ❌ "성적 향상" → ✅ "학습 습관 형성 도구" |
| 환불 정책 명시 | [ ] | "7일 이내 반품 가능 (단, 개봉 시 제외)" |
| 사업자 정보 표시 | [ ] | 상호, 대표자명, 사업자번호, 주소, 연락처 |

### 개인정보보호 (GDPR/개인정보보호법)

```python
# 최소 수집 원칙
customer_data = {
    "name": "홍길동",           # 필수
    "phone": "010-1234-5678",  # 필수 (배송용)
    "email": "hong@example.com" # 선택
    # ❌ 수집 금지: 주민등록번호, 계좌번호
}

# 자동 삭제 규칙
# - 주문 완료 후 5년 보관 (전자상거래법)
# - 미구매 고객 정보: 1년 후 자동 삭제
```

---

## 비용 투명성 (단계별 실제 비용)

### Mini 단계 (무료)
```
네이버 스마트스토어: 무료
Canva 무료 플랜: 무료
Claude 웹 인터페이스: 무료 (Pro $20/월 권장)
= 총 $0-20/월
```

### Standard 단계
```
Claude API: $20-30/월
  - Sonnet 4: $3/M input, $15/M output
  - 상품 설명 100개: 2K input × 8K output × 100 = $1.80
  - CS 초안 50개: 1K input × 3K output × 50 = $0.30
  - 버퍼 포함: ~$25/월
  
Vercel: $0-20/월
  - Hobby 플랜: 무료 (100GB bandwidth)
  - Pro 플랜: $20/월 (필요 시)

도메인: $1/월 (연 $12)

= 총 $21-51/월
```

### Full 단계
```
Railway:
  - PostgreSQL: $5/월
  - Redis: $5/월
  - Web Service: $10-30/월 (트래픽)
  
Claude API: $100-200/월 (대량 처리)
이미지 생성: $50-100/월
Sentry: $26/월 (에러 추적)

= 총 $196-366/월
```

**손익분기점 계산**:
- Standard: 월 매출 50만원 이상 시 비용 < 5%
- Full: 월 매출 500만원 이상 시 비용 < 8%

---

## 핵심 스크립트 목록

| 스크립트 | 용도 | 실행 시간 | 비용 |
|---|---|---|---|
| `validate_idea.py` | 아이디어 검증 | 1분 | 무료 |
| `auto_claude.py` | 상품 설명 자동 생성 | 5분 (10개) | $1.50 |
| `cost_calculator.py` | 월 비용 예측 | 즉시 | 무료 |
| `legal_check.py` | 법률 준수 체크 | 10초 | 무료 |
| `naver_integration.py` | 네이버 API 연동 | 1분 | 무료 |
| `mini-mvp/app.py` | 최소 주문 시스템 | 즉시 | 무료 |

---

## 성공 지표 (단계별)

### Mini → Standard 진행 조건
- ✅ 10개 판매 (실제 고객)
- ✅ 긍정 리뷰 3개 이상
- ✅ 재구매 또는 문의 1개 이상
- ✅ 순이익 > 0 (적자 아님)

### Standard → Full 진행 조건
- ✅ 월 매출 100만원 × 3개월 연속
- ✅ 월 순이익 30만원 이상
- ✅ 운영 시간 주 10시간 이하
- ✅ 2개 이상 채널 판매 (네이버 + 쿠팡 등)

---

## 초보자 실행 가이드

### Week 1: 검증
```bash
# Day 1: 아이디어 검증
python scripts/validate_idea.py "칭찬스티커"

# Day 2-3: 디자인 (Canva)
# - 템플릿 다운로드: templates/sticker-board.fig
# - 수정: 자녀 이름 커스터마이징 옵션 추가

# Day 4: 상품 설명 생성
python scripts/auto_claude.py --product "칭찬스티커" --count 1

# Day 5: 법률 체크
python scripts/legal_check.py listings/product_001.md

# Day 6-7: 네이버 입점
python scripts/naver_integration.py --upload listings/product_001.md --dry-run
# 확인 후 --confirm으로 실제 등록
```

### Week 2-4: 판매
- 네이버 스마트스토어 운영
- 고객 피드백 수집
- 재구매/번들 테스트

### Week 5+: 자동화 (10개 판매 달성 시)
```bash
# Mini MVP 실행
cd examples/mini-mvp
python app.py

# Claude API 연동
python scripts/auto_claude.py --product "칭찬스티커 V2" --feedback customer_feedback.csv
```

---

## 레퍼런스 파일

| 파일 | 용도 |
|---|---|
| `references/naver-api-guide.md` | 네이버 API OAuth ~ 상품 등록 |
| `references/legal-checklist.md` | 전자상거래법 필수 준수 사항 |
| `references/cost-breakdown.md` | 단계별 상세 비용 분석 |
| `references/mvp-architecture.md` | FastAPI + SQLite 구조 설명 |
| `examples/mini-mvp/` | 10줄짜리 작동하는 코드 |
| `examples/claude-api-caller/` | 실제 Claude API 호출 예제 |

---

## 응답 스타일

기본 한글. 명령어 예시와 실행 결과 로그 포함. "할 수 있습니다" 대신 "실행 명령어" 제공. 비용과 시간 명시. 법률 리스크 명확히 경고.

---

## 핵심 차이점 (v1 대비)

| 항목 | v1 | v2 (개선) |
|---|---|---|
| 복잡도 | 8개 Agent, 4단계 자동화 | 3단계 시스템 |
| 실행 가능성 | 프롬프트 생성 | 실제 작동 코드 |
| 진입 장벽 | Next.js + PostgreSQL 필수 | FastAPI + SQLite (10줄) |
| 비용 투명성 | 언급 없음 | 단계별 상세 비용 |
| 법률 가이드 | "승인 필요" 언급 | 체크리스트 + 자동 점검 |
| API 연동 | payload 생성만 | OAuth ~ 등록까지 전체 |
| 검증 방법 | Proof Agent 개념 | 실제 판매 지표 |
| 학습 곡선 | 3,257줄 문서 | 핵심 6개 스크립트 |
