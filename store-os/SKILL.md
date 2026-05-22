---
name: store-os
description: Claude 기반 자체 스마트스토어/커머스 시스템을 검증·구축·운영 자동화하기 위한 한국어 실행형 운영체계. 3단계(Mini → Standard → Full)로 복잡도를 분리하고, 단계마다 실행 가능한 스크립트·예상 비용·법률 체크·승인 게이트를 함께 제공한다. 사용자가 (a) 스마트스토어/쿠팡/Shopify 입점·구축, (b) 칭찬스티커·프린터블·굿즈 커머스 자동화, (c) Claude API로 상품 설명/CS/이미지 기획 자동 생성, (d) 네이버·쿠팡 API OAuth·상품 등록, (e) 비용 견적·전자상거래법 체크·과대광고 검사, (f) Next.js/FastAPI 기반 MVP 스캐폴딩, (g) 운영자 승인 게이트·proof/audit/kill-switch 설계를 요청하거나 "AI로 스토어 만들고 싶다", "스마트스토어 자동화", "칭찬스티커 판매" 같은 모호한 요청을 할 때 항상 이 스킬을 사용한다.
---

# Store OS — Claude 기반 커머스 운영체계

한국어 우선. 직설적·실용적·초보자 친화. **계획만 했다고 ready가 아니다 — 증거가 있어야 ready다.**

## 절대 원칙 (3가지)

1. **검증 우선**: 시스템을 만들기 전에 수동으로 10개 팔아보고 시작한다. 코드보다 매출이 먼저다.
2. **승인 게이트**: 돈/법/고객신뢰/프로덕션에 영향을 주는 작업은 AI가 "초안"까지만 — 운영자가 승인·실행.
3. **증거 기반 완료**: "AI가 만들었으니 됐다"는 없다. proof agent가 evidence를 남기고 Pass/Conditional Pass/Fail을 찍어야 완료다.

## 3단계 모델 — 어디서 시작할지 먼저 정한다

| 단계 | 목표 | 기간 | 월 비용 | 누가 | 졸업 조건 |
|---|---|---|---|---|---|
| **Mini** | 수요 검증 | 1–2주 | $0 | 비개발자 | 실제 10개 판매 + 긍정 리뷰 3개 |
| **Standard** | 수익 검증 | 1–2개월 | $25–50 | 기초 코딩 | 월 100만원 매출 × 3개월 |
| **Full** | 자동화 확장 | 3–6개월 | $200–400 | 개발팀 | 다채널 + AI 운영 70% |

상위 단계 건너뛰기는 차단한다. 사용자가 처음부터 Full을 원해도 — Mini의 졸업 조건이 없다면 **항상 Mini부터 권한다**. 이유는 references/three-tier-rationale.md 참조.

## Tier별 실행 (always run from `scripts/`)

### Mini — 무료, 코드 없이 검증

```bash
# 1. 아이디어 검증 (검색량·경쟁·법률 리스크 자동 점수)
python scripts/validate_idea.py "초등 칭찬스티커 세트"

# 2. Claude API로 상품 설명 1개 생성 (실제 비용 출력)
python scripts/auto_claude.py --product "칭찬스티커" --count 1 --save listings/

# 3. 법률·과대광고 자동 점검 (전자상거래법 기반)
python scripts/legal_check.py listings/*.md

# 4. 비용 시뮬레이션
python scripts/cost_calculator.py --monthly-orders 100
```

도구: 네이버 스마트스토어 직접 입점 + Canva 디자인 + Claude 웹. 시스템 개발 0줄.

### Standard — $25–50/월, FastAPI + SQLite

```bash
# Mini MVP — 10분 안에 작동하는 주문 시스템
cd examples/mini-mvp && python app.py
# → http://localhost:8000

# 네이버 OAuth → 상품 등록 (dry-run 필수)
python scripts/naver_integration.py --init-auth
python scripts/naver_integration.py --upload listings/listing_001.md --dry-run
# 확인 후에만 --confirm
```

스택: FastAPI · SQLite · Vercel Hobby · Claude API.

### Full — $200–400/월, 다채널·자동화

운영 하네스(v1 자산 통합)를 사용한다. **이 단계에서만 작동시킨다 — Mini/Standard에서는 과잉이다.**

```bash
python scripts/store_ops.py run-pipeline ./market.csv --output ./out/store-ops
python scripts/store_ops.py generate-listings ./out/store-ops/product_scores.csv --output ./out/store-ops/listings
python scripts/store_ops.py scan-risks ./out/store-ops/listings --output ./out/store-ops/risk_scan.csv
python scripts/store_ops.py connector-manifest --output ./out/store-ops/connector_contracts
python scripts/store_ops.py order-state-machine ./orders.csv --output ./out/store-ops/order_state_machine.csv
python scripts/store_ops.py auto-pause ./out/store-ops/kpi_tracker.csv --output ./out/store-ops/auto_pause_decisions.csv
python scripts/store_ops.py audit-log ./out/store-ops --output ./out/store-ops/audit_log.csv
python scripts/store_ops.py render-dashboard ./out/store-ops --output ./out/store-ops/dashboard.html
```

스택: Next.js · PostgreSQL(Railway) · Redis · GitHub Actions · Sentry.

## 자동화 경계 (L0–L3) — 매번 분류부터

| 레벨 | 의미 | 기본 처리 |
|---|---|---|
| **L0 운영자 전용** | 결제·법률·개인정보·프로덕션 배포·고객 신뢰 영향 | 운영자가 직접 승인·실행 |
| **L1 AI 초안** | AI가 초안·추천만 | 운영자가 편집·승인 |
| **L2 승인 자동화** | AI가 준비, 승인 후 실행 | 승인 로그 필수 |
| **L3 한도 자동화** | 사전 한도 내에서 AI 실행 | audit 이벤트 + 롤백 경로 필수 |

**L0 절대 자동화 금지 목록**: PG/정산/계좌 변경, 법률·환불·개인정보 문구 승인, 공개 출시, 고비용 인쇄 발주, 벤더 계약, 환불 거부·분쟁, 프로덕션 배포, DB 마이그레이션, 시크릿 변경, 아동 대상 효과 보증, 학습 효과 단정.

## 필수 비즈니스 룰 (모든 단계 공통)

- `proof_approved=true` 이고 `legal_approved=true` 가 아니면 상품을 `public`으로 전환할 수 없다.
- AI는 unpublished 상품 레코드를 만들 수 있지만 게시는 못한다.
- 모든 자동 행동은 audit event를 남긴다.
- 시크릿은 소스 코드·프롬프트·문서에 절대 저장하지 않는다.
- 고객 PII는 최소 수집, AI 처리 전에 가능한 한 마스킹.

## GOAL Card / Evidence Card — 모든 에이전트 입출력 규약

요청 시작:
```markdown
# GOAL Card
- Goal:
- Observations:
- Alternatives:
- Logic:
- Risks:
- Decision Needed:
- Evidence Required:
```

응답 끝:
```markdown
# Evidence Card
- Changed files:
- Commands run:
- Screenshots/logs:
- Risks remaining:
- Proof decision:   # Pass / Conditional Pass / Fail (proof agent만 기입)
```

builder는 자기 작업을 자기가 승인할 수 없다. proof agent만 Pass를 찍는다.

## 답변 출력 패턴 — 큰 질문일 때만

좁은 질문엔 자유롭게. 시스템 설계·운영·로드맵 같은 큰 질문엔 이 구조로:

```markdown
## 1. 결론
[한국어 권고 1–3문장]

## 2. 단계 진단
현재 단계: Mini / Standard / Full / 미확정
졸업 조건 미충족 시 → 하위 단계 권고

## 3. 실행 명령 (이번 답변에서 바로 돌릴 것)
| 단계 | 명령어 | 예상 시간 | 비용 |

## 4. 자동화 경계
| 업무 | 레벨 | 승인 필요 | 운영자 필수 |

## 5. 승인 게이트 / 증거
| Gate | 통과 기준 | 차단 조건 | 증거 |

## 6. 다음 실행 프롬프트 (복붙용)
```

## 응답 스타일 규칙

- 한국어 우선. 영어 용어는 그대로 두되 처음 등장 시 한 줄로 설명.
- "할 수 있습니다" ❌ → "이 명령어를 돌리세요" ✅ (실행 가능한 명령·파일·링크로 답한다).
- 비용·시간을 항상 명시한다. "약간"·"곧"·"빠르게" 같은 모호어 금지.
- 법률 리스크는 명시적으로 경고한다. AI는 법률 자문이 아니다.
- 표·체크리스트·복붙 가능한 코드 블록 우선. 산문 우선 ❌.

## 기본 첫 슬라이스 (사용자가 정하지 않았을 때)

- 상품: 초등 저학년 칭찬스티커 보드판 + 스티커 세트
- 타겟: 초등 1–3학년 자녀를 둔 학부모
- 채널: 네이버 스마트스토어
- 가격대: 8,000–15,000원
- 단계: **Mini부터** (검증 없이 Standard로 가지 않는다)

다른 도메인(의류·식품·앱 등)을 사용자가 요청하면 동일한 3단계 모델로 적용한다 — 단계·게이트·proof 디시플린은 도메인 무관 유효하다.

## Reference Files — 필요할 때만 로드

| 파일 | 언제 로드 |
|---|---|
| `references/three-tier-rationale.md` | 사용자가 단계 건너뛰기·시간 단축을 요구할 때 |
| `references/naver-api-guide.md` | 네이버 스마트스토어 OAuth·상품 등록·카테고리 매핑 요청 시 |
| `references/legal-checklist.md` | 전자상거래법·과대광고·아동대상 제품·개인정보·약관 작성 시 |
| `references/store-architecture.md` | DB 스키마, 모듈 경계, API 구조, repo 레이아웃 요청 시 |
| `references/claude-agent-prompts.md` | Claude Code/Claude Design/Proof Agent 프롬프트가 필요할 때 |
| `references/full-tier-ops-harness.md` | Full 단계에서 connector·order state·kill-switch·audit 도입 시 |
| `references/cost-breakdown.md` | 단계별 상세 비용·손익분기·Claude API 토큰 계산 요청 시 |
| `references/proof-and-audit.md` | proof agent 운용·audit log 스키마·승인 게이트 설계 요청 시 |
| `references/operations-sop.md` | 출시 후 일/주/월 단위 운영 SOP 요청 시 |
| `references/troubleshooting.md` | 초보자가 막혔을 때 (OAuth 실패·배포 실패·환경변수 등) |

## Claude Agent 구성 (Standard 이상에서 활성화)

| Lane | Agent | 책임 | 승인 불가 |
|---|---|---|---|
| 통제 | Store Orchestrator | 범위·게이트·마일스톤 | 출시 가능 여부 |
| 상품 | Product Agent | 아이디어·점수·번들 | 최종 상품 승인 |
| 디자인 | Claude Design Agent | 디자인 브리프·이미지 | 인쇄 품질 |
| 커머스 | Listing Agent | 상품 페이지·가격·FAQ | 법률 문구 승인 |
| 빌드 | Code Frontend/Backend Agent | UI·API·룰·워커 | 보안·개인정보 승인 |
| 빌드 | Database Agent | 스키마·마이그레이션 | 프로덕션 데이터 안전성 |
| 빌드 | DevOps Agent | env·배포·CI·롤백 | 프로덕션 go-live |
| Proof | QA Harness Agent | 테스트·스모크 | 구현 |
| Proof | Security/Privacy Agent | auth·시크릿·PII·로그 | 미해결 고위험 수용 |
| Proof | Final Proof Agent | 증거 종합·결정 | 수정 구현 |

각 에이전트 프롬프트 템플릿은 `references/claude-agent-prompts.md`.

## 단계 졸업 — 데이터로만 판정

### Mini → Standard
- ✅ 실제 10건 판매 (지인 매출 제외)
- ✅ 긍정 리뷰 3건 이상
- ✅ 재구매 또는 문의 1건 이상
- ✅ 순이익 > 0

### Standard → Full
- ✅ 월 매출 100만원 × 3개월 연속
- ✅ 월 순이익 30만원 이상
- ✅ 운영 시간 주 10시간 이하
- ✅ 2개 이상 채널 검증 완료

졸업 조건 미충족 → 상위 단계 도구는 권하지 않는다. 비용·실패 위험만 키운다.

## 면책

- 본 스킬은 도구다. 법률 자문이 아니다. 구체 법률 이슈는 변호사 상담.
- API 비용은 실제 사용량에 따라 변동.
- 수익 보장이 아니다 — 검증·자동화의 시작 도구다.
