# Store OS — Claude 기반 커머스 운영체계

> v1·v2 자산을 통합한 단일 최적 스킬. 3단계 모델(Mini → Standard → Full)로 복잡도를 분리하고 단계마다 실행 가능한 스크립트·proof 디시플린·승인 게이트를 제공한다.

## 핵심 철학

1. **검증 우선** — 코드보다 매출이 먼저.
2. **승인 게이트** — L0(돈·법·고객신뢰)는 AI가 초안까지, 운영자가 승인·실행.
3. **증거 기반 완료** — proof agent의 Pass 없이는 ready 아님.

## 1분 빠른 시작

```bash
# 1. 아이디어 검증
python scripts/validate_idea.py "초등 칭찬스티커 세트"

# 2. Claude API로 상품 설명 1개 (실제 비용 출력)
export ANTHROPIC_API_KEY="sk-ant-..."
python scripts/auto_claude.py --product "칭찬스티커" --count 1 --save listings/

# 3. 법률 체크
python scripts/legal_check.py listings/*.md

# 4. 비용 계산
python scripts/cost_calculator.py --monthly-orders 100

# 5. Mini MVP 실행 (10분 안에 작동)
cd examples/mini-mvp && python app.py
```

## 디렉토리

```
store-os/
├── SKILL.md                # 스킬 정의 (트리거·룰·답변 패턴)
├── README.md
├── scripts/
│   ├── validate_idea.py        # Mini 단계 — 아이디어 검증
│   ├── auto_claude.py          # Standard — Claude API 자동 호출
│   ├── cost_calculator.py      # 비용 시뮬레이션
│   ├── legal_check.py          # 전자상거래법 자동 점검
│   ├── store_ops.py            # Full 단계 — 운영 하네스
│   └── init_store_project.py   # Standard/Full — 스캐폴딩
├── references/
│   ├── three-tier-rationale.md     # 단계 모델 근거 + 건너뛰기 응대
│   ├── proof-and-audit.md          # proof decision·audit 스키마·게이트
│   ├── full-tier-ops-harness.md    # store_ops.py 명령 카탈로그
│   ├── cost-breakdown.md           # 단계별 비용·손익분기
│   ├── naver-api-guide.md          # 네이버 OAuth·상품 등록
│   ├── legal-checklist.md          # 전자상거래법 체크리스트
│   ├── store-architecture.md       # 스키마·모듈 경계
│   ├── claude-agent-prompts.md     # Builder/Proof 에이전트 프롬프트
│   ├── operations-sop.md           # 출시 후 일/주/월 SOP
│   └── troubleshooting.md          # 초보자 트러블슈팅
├── examples/
│   └── mini-mvp/                   # 10분 작동 주문 시스템 (FastAPI + SQLite)
└── templates/
    └── prisma-schema.prisma        # Standard/Full DB 스키마 시드
```

## 3단계 요약

| 단계 | 기간 | 비용 | 졸업 조건 |
|---|---|---|---|
| **Mini** | 1–2주 | $0 | 실 판매 10건 + 리뷰 3건 + 순이익 > 0 |
| **Standard** | 1–2개월 | $25–50 | 월 매출 100만원 × 3개월 |
| **Full** | 3–6개월 | $200–400 | 다채널 + AI 운영 70% |

상위 단계 건너뛰기는 권하지 않는다 — 시스템 비용이 매출보다 빨리 늘면 가게가 망한다. 근거: `references/three-tier-rationale.md`.

## v1·v2와의 관계

| 항목 | v1 (claude-store-os) | v2 (store-os-v2) | store-os (이번 통합) |
|---|---|---|---|
| 3단계 모델 | ❌ (8 agent · 4 자동화) | ✅ | ✅ |
| 실행 가능 코드 | ❌ (prompt 위주) | ✅ | ✅ |
| 비용 투명성 | ❌ | ✅ | ✅ (확장) |
| 법률 자동 점검 | 부분 | ✅ | ✅ |
| Proof / Audit | ✅ | ❌ | ✅ |
| Connector / Kill-switch | ✅ | ❌ | ✅ (Full만) |
| SKILL.md 길이 | 280줄 | 280줄 | ~180줄 |
| References | 20개 | 2개 | 10개 (단계 분리) |

요약: **v2의 3단계 골격 + v1의 proof/audit/connector 디시플린**.

## 면책

도구일 뿐 법률 자문 아님. 구체 법률 이슈는 변호사 상담. API 비용은 실제 사용량 변동. 수익 보장 아님.
