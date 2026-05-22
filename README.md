# Claude Store OS

> Claude AI 기반 자체 스마트스토어/커머스 운영체계. 3단계(Mini → Standard → Full) 모델로 복잡도를 분리하고, 단계마다 실행 가능한 스크립트·예상 비용·법률 체크·승인 게이트를 함께 제공.

## 한 줄

**검증 우선·승인 게이트·증거 기반 완료.** 코드보다 매출이 먼저, AI가 만들었다는 이유로 ready가 되지 않는다.

## 빠른 시작

```bash
# 1. 아이디어 검증 (1분, 무료)
python store-os/scripts/validate_idea.py "초등 칭찬스티커 세트"

# 2. Mini MVP 실행 (10분, 무료) — FastAPI + SQLite
cd store-os/examples/mini-mvp && python app.py
# → http://localhost:8000

# 3. Claude API로 상품 설명 생성 (실제 비용 출력)
export ANTHROPIC_API_KEY="sk-ant-..."
python store-os/scripts/auto_claude.py --product "칭찬스티커" --count 1

# 4. 전자상거래법 자동 점검
python store-os/scripts/legal_check.py listings/*.md

# 5. 비용 시뮬레이션
python store-os/scripts/cost_calculator.py --monthly-orders 100
```

## 3단계 모델

| 단계 | 기간 | 비용/월 | 졸업 조건 |
|---|---|---|---|
| **Mini** (검증 우선) | 1–2주 | $0 | 실 판매 10건 + 리뷰 3건 + 순이익 > 0 |
| **Standard** (수익 검증) | 1–2개월 | $25–50 | 월 매출 100만원 × 3개월 |
| **Full** (자동화 확장) | 3–6개월 | $200–400 | 다채널 + AI 운영 70% |

상위 단계 건너뛰기는 차단한다. 시스템 비용이 매출보다 빨리 늘면 가게가 망한다. 근거: [three-tier-rationale.md](store-os/references/three-tier-rationale.md).

## 디렉토리

```
.
├── README.md               # 이 파일 (GitHub 랜딩)
├── CLAUDE.md               # 프로젝트 운영 규칙 (Claude Code 자동 로드)
│                           # 스킬·MCP 자동 호출 매핑, GOAL 카탈로그, HARD-GATE
├── store-os/               # 통합 최적 스킬 (활성)
│   ├── SKILL.md            # 스킬 본체
│   ├── README.md           # 스킬 사용법
│   ├── references/         # 10개 reference (3-tier, proof/audit, cost, naver-api, legal …)
│   ├── scripts/            # 6개 실행 스크립트
│   ├── examples/mini-mvp/  # FastAPI + SQLite 주문 시스템
│   ├── templates/          # Prisma 스키마
│   ├── tests/              # 45 unittest (45/45 통과)
│   └── docs/               # spec·plan·goal 산출물 저장 위치
└── _archive/               # v1·v2 보존 (참조 전용, 수정 금지)
    ├── claude-store-os/    # v1 — 운영 디시플린 풍부, 코드 빈약
    └── store-os-v2/        # v2 — 실행 코드 풍부, 운영 룰 빈약
```

## 절대 원칙

1. **Builder ≠ Proof** — Builder는 자기 작업을 자기가 승인할 수 없다.
2. **병렬 가능 작업은 무조건 병렬** — 의존성 없는 작업은 다중 subagent.
3. **스킬 자동 호출이 기본** — 1% 가능성이면 invoke.
4. **brainstorming → writing-plans → subagent-driven-development 흐름이 표준** — HARD-GATE: 디자인 승인 전 코드 금지.
5. **GOAL 카드로 모든 복잡 시스템 작업을 정의** — [STORE-01]~[STORE-12] 카탈로그.

상세는 [CLAUDE.md](CLAUDE.md).

## 자동화 경계 (L0–L3)

| 레벨 | 의미 | 처리 |
|---|---|---|
| **L0** 운영자 전용 | 결제·법률·개인정보·프로덕션·고객 신뢰 영향 | 자동화 절대 금지 |
| **L1** AI 초안 | AI 추천 | 운영자 편집·승인 |
| **L2** 승인 자동화 | AI 준비, 승인 후 실행 | 승인 로그 의무 |
| **L3** 한도 자동화 | 사전 한도 내 자동 | audit + 롤백 경로 의무 |

## 도메인 적용

기본 첫 슬라이스: **초등 저학년 칭찬스티커 보드판 + 스티커 세트** (네이버 스마트스토어, 8,000–15,000원). 다른 도메인(의류·식품·앱·디지털 굿즈)에도 동일 3단계 모델 적용.

## 면책

- 본 도구는 법률 자문이 아니다. 구체 법률 이슈는 변호사 상담.
- API 비용은 실제 사용량에 따라 변동.
- 수익 보장이 아니다 — 검증·자동화의 시작 도구.

## 라이선스

[MIT](LICENSE)
