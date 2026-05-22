# CLAUDE.md — Claude Store OS 프로젝트 운영 규칙

이 파일은 Claude Code가 이 디렉토리에서 작업할 때 자동 로드되는 운영 규칙이다.
스킬 본체는 `store-os/SKILL.md`. 이 파일은 **그 위에서 어떻게 일할지** + **언제 어떤 도구를 자동 호출할지**를 정한다.

---

## A. 절대 원칙 (5가지)

1. **Builder ≠ Proof** — Builder는 자기 작업을 자기가 승인할 수 없다. Pass/Conditional Pass/Fail은 별도 proof 에이전트만 찍는다.
2. **병렬 가능 작업은 무조건 병렬** — 의존성 없는 여러 작업은 같은 메시지의 다중 Agent 블록으로 보낸다.
3. **스킬 자동 호출이 기본** — 작업에 매칭되는 스킬이 1%라도 있으면 Skill 도구로 invoke 후 진행한다. 매핑 테이블은 §C, §D.
4. **brainstorming → writing-plans → subagent-driven-development 흐름이 표준** — 새 기능·신규 시스템 개발은 이 3개 스킬 체인을 통과한다. brainstorming의 HARD-GATE: 디자인 승인 전에는 코드 한 줄도 쓰지 않는다.
5. **GOAL 카드로 모든 복잡 시스템 작업을 정의** — Store OS에서도 PLM/QMS 스타일 GOAL 템플릿을 사용. 발동 조건은 §H.

---

## B. 작업 페이즈 흐름 — 표준 스킬 체인 (HARD-GATE 포함)

```
                ╔══════════════════ HARD-GATE ══════════════════╗
                ║ brainstorming이 디자인 승인을 받기 전에는       ║
                ║ 코드·스캐폴딩·구현 스킬 일체 호출 금지.         ║
                ╚════════════════════════════════════════════════╝

[Intake]   →   [Brainstorm]   →   [Plan]   →   [Build]   →   [Verify]   →   [Ship]   →   [Operate]
   ↓               ↓                ↓            ↓             ↓             ↓             ↓
office-       brainstorming     writing-      TDD +         verification   ship +      canary +
hours          (HARD-GATE +     plans         subagent-     -before-       land-and-   retro +
+ GOAL         spec self-       (saves to     driven-       completion     deploy      document-
정의           review +         docs/super-   development   (Iron Law)                 release +
(§H)           user spec        powers/       (병렬          + qa /                     consolidate-
               review)          plans/        subagent      design-                    memory
                                YYYY-MM-DD)   per task)     review
                                ↓             ↓             ↓
                                terminal:     2-stage       gate:
                                writing-      review per    Pass/Cond/
                                plans 호출    task          Fail (별도
                                                            proof agent)
```

**체인 규칙**:
- brainstorming이 끝나면 **자동으로** writing-plans 호출. 다른 구현 스킬 호출 금지.
- writing-plans가 끝나면 **자동으로** subagent-driven-development 호출 (subagent 가용) 또는 executing-plans (불가용).
- 모든 task 완료 후 자동으로 finishing-a-development-branch 호출.
- 완료 보고 직전 verification-before-completion 의무 (Iron Law: 이 메시지에서 다시 검증 안 돌리면 "완료"라 말하지 못함).

각 페이즈가 끝나면 **다음 페이즈를 사용자에게 명시적으로 제안**한다 ("다음은 X 페이즈입니다. Y 스킬 호출하겠습니다"). 사용자가 페이즈를 건너뛰자고 해도 §F 자동 호출 의무는 유지된다.

---

## C. 스킬 자동 호출 매핑 — 사용자 발화/의도별

### C-1. 기획·아이디어 페이즈

| 사용자 발화·의도 | 자동 호출 스킬 | 비고 |
|---|---|---|
| "이 아이디어 괜찮을까?", "만들어볼만 할까?" | `office-hours` | YC 6가지 forcing question + 디자인 씽킹 |
| "어떻게 만들지?", "기능 추가하고 싶다" | **`superpowers:brainstorming` (HARD-GATE)** | 디자인 승인 전 구현 스킬 호출 금지. terminal: `writing-plans`. §G-1 |
| §H-3 GOAL 카탈로그 트리거 키워드 매칭 | **GOAL 카드 작성 → brainstorming** | 12개 GOAL ID 중 매칭 |
| "PLM 개발", "QMS 구축", "토탈 시스템", "BOM·ECO·PPAP·APQP" | **`anthropic-skills:plm-qms-goals`** | `/goal [PLM-XX]` 또는 `/goal [QMS-XX]` |
| "스코프 더 크게", "10x 비전" | `plan-ceo-review` | 4가지 모드 (확장·선택확장·유지·축소) |
| "아키텍처 검토", "이대로 만들면 되나" | `plan-eng-review` | 데이터 흐름·엣지케이스·테스트 커버리지 |
| "디자인 사전 검토", "구현 전에 봐줘" | `plan-design-review` | 차원별 0–10 점수 + 10점으로 가는 길 |
| "DX 검토", "API 디자인", "개발자 경험" | `plan-devex-review` | 경쟁사 벤치마크 + magical moment |
| "계획 자동 검토 / 풀 리뷰 / 모든 리뷰" | `autoplan` | CEO+Eng+Design+DX 자동 통합 + 6원칙 자동 결정 |
| "다음 단계 계획 짜줘 / 구현 플랜" | `superpowers:writing-plans` | brainstorming 직후 자동 chain |

### C-2. 설계·아키텍처 페이즈

| 사용자 발화·의도 | 자동 호출 스킬 | 비고 |
|---|---|---|
| "시스템 설계", "아키텍처 그려줘", "서비스 경계" | `engineering:system-design` · `engineering:architecture` | API·데이터 모델·서비스 boundary |
| "기술 부채 평가" | `engineering:tech-debt` | |
| "테스트 전략" | `engineering:testing-strategy` | 단위·통합·E2E 균형 |
| "디자인 시스템 / 브랜드 / 컬러 팔레트" | `design-consultation` · `anthropic-skills:brand-guidelines` · `design:design-system` | DESIGN.md 산출 |
| "시안 더 보여줘", "디자인 변형 / shotgun" | `design-shotgun` | 다중 AI 변형 + 비교 보드 |
| "최종 HTML 디자인" | `design-html` | Pretext-native, 30KB |
| "접근성 검토" | `design:accessibility-review` | WCAG · screen reader |
| "UX 카피·문구" | `design:ux-copy` · `customer-support:draft-response` | |
| "유저 리서치 / 인터뷰 정리" | `design:user-research` · `design:research-synthesis` | |

### C-3. 구현 페이즈

| 사용자 발화·의도 | 자동 호출 스킬 | 비고 |
|---|---|---|
| "기능 구현", "스크립트 작성" | `superpowers:test-driven-development` | 테스트 먼저 |
| "계획대로 실행" | `superpowers:executing-plans` · `superpowers:subagent-driven-development` | 독립 작업은 subagent 분기 |
| "병렬로 N개 처리" | `superpowers:dispatching-parallel-agents` | 다중 Agent 블록 가이드 |
| "기존 코드 정리 / 단순화" | `simplify` | 재사용·품질·효율 통과 |
| "Claude API 통합 / SDK 사용" | `claude-api` | 프롬프트 캐싱·thinking·tool use 베스트프랙티스 |
| "MCP 만들고 싶다" | `anthropic-skills:mcp-builder` | MCP 서버 신규 작성 |
| "스킬 만들고 싶다 / 스킬 개선" | `anthropic-skills:skill-creator` · `superpowers:writing-skills` | description optimizer 포함 |
| "Cowork 플러그인" | `cowork-plugin-management:create-cowork-plugin` | |

### C-4. 검증 페이즈

| 사용자 발화·의도 | 자동 호출 스킬 | 비고 |
|---|---|---|
| "버그 났다", "에러", "안 된다", "왜 안 돼" | `superpowers:systematic-debugging` · `engineering:debug` · `investigate` | 근본 원인 강제 4-phase |
| "QA / 테스트해줘 / 버그 찾아 (수정 포함)" | `qa` | test + fix + 재검증 loop |
| "리포트만 / 수정은 하지 마" | `qa-only` | 리포트만 |
| "디자인 점검 / 시각 QA" | `design-review` | 시각·간격·hierarchy·AI slop |
| "DX 실측", "온보딩 시간 측정" | `devex-review` | |
| "벤치마크 / 성능", "느려" | `benchmark` · `benchmark-models` (모델 비교) | |
| "코드 리뷰 / 머지 전 검토" | `superpowers:requesting-code-review` → `superpowers:code-reviewer` (별도 agent) → `superpowers:receiving-code-review` | proof 분리 |
| "보안 / pentest / OWASP" | `security-review` · `cso` | daily + comprehensive |
| "건강도 점수" | `health` | 종합 0–10 |
| "완료 직전 / ready 인지 확인" | `superpowers:verification-before-completion` | "AI가 만들었으니 됐다" 회로 차단 |
| "두 번째 의견 / 다른 AI" | `codex` | OpenAI Codex review·challenge·consult |

### C-5. 출시·운영 페이즈

| 사용자 발화·의도 | 자동 호출 스킬 | 비고 |
|---|---|---|
| "배포 / 출시 / PR 만들어 / push" | `ship` → `superpowers:finishing-a-development-branch` | VERSION·CHANGELOG·PR |
| "머지 + 배포" | `land-and-deploy` | merge → CI → deploy → canary |
| "배포 후 / 프로덕션 감시" | `canary` | console·perf 감시 |
| "배포 설정" | `setup-deploy` | Fly/Render/Vercel/Netlify/Heroku |
| "incident / 장애 대응" | `engineering:incident-response` | |
| "체크리스트 / 배포 전 점검" | `engineering:deploy-checklist` | |
| "릴리즈 노트 / 문서 갱신" | `document-release` · `engineering:documentation` | |
| "회고 / 주간 정리 / 리트로" | `retro` · `engineering:standup` | gstack은 commit 기반 |
| "고객 문제 / 에스컬레이션" | `customer-support:customer-escalation` · `customer-support:ticket-triage` | |
| "KB 글 / 헬프 아티클" | `customer-support:kb-article` | |
| "고객 리서치" | `customer-support:customer-research` | |
| "출시 보고 / 임원 메모" | `anthropic-skills:internal-comms` · `anthropic-skills:doc-coauthoring` | |

### C-6. 산출물·자료 페이즈

| 사용자 발화·의도 | 자동 호출 스킬 |
|---|---|
| "엑셀 / .xlsx / 스프레드시트" | `anthropic-skills:xlsx` |
| "워드 / .docx / 문서" | `anthropic-skills:docx` |
| "PPT / .pptx / 슬라이드" | `anthropic-skills:pptx` |
| "PDF (장문)" | `anthropic-skills:pdf` · `make-pdf` |
| "PDF (마크다운 → 출판물)" | `make-pdf` |
| "이미지 보정 / 리사이즈 / 사회미디어 변형" | `adobe-for-creativity:adobe-*` |
| "캔버스 / 캔버스 디자인" | `anthropic-skills:canvas-design` |
| "Slack GIF" | `anthropic-skills:slack-gif-creator` |
| "웹 아티팩트" | `anthropic-skills:web-artifacts-builder` |
| "테마 (코드 에디터)" | `anthropic-skills:theme-factory` |
| "알고리즘 아트 / 생성 미술" | `anthropic-skills:algorithmic-art` |

### C-7. 메모리·세션 관리

| 사용자 발화·의도 | 자동 호출 스킬 |
|---|---|
| "어디까지 했지 / 컨텍스트 저장" | `context-save` |
| "이어서 / 복원" | `context-restore` |
| "메모리 합치기 / 정리" | `anthropic-skills:consolidate-memory` |
| "학습 누적 / 패턴" | `learn` |
| "이전 세션 검색" | `ccd_session_mgmt` MCP |

### C-8. 안전·접근 통제

| 사용자 발화·의도 | 자동 호출 스킬 |
|---|---|
| "주의 모드 / careful / prod" | `careful` |
| "이 폴더만 / freeze" | `freeze` (해제 `unfreeze`) |
| "최대 안전 모드" | `guard` (careful + freeze 결합) |

### C-9. 환경·설정

| 사용자 발화·의도 | 자동 호출 스킬 |
|---|---|
| "permission 추가 / 자동 승인" | `update-config` · `fewer-permission-prompts` |
| "키바인딩" | `keybindings-help` |
| "스케줄 작업 / cron / 주기 작업" | `schedule` · `loop` (인터벌) |

---

## D. MCP·플러그인 커넥터 자동 호출 매핑

### D-1. 사용 가능한 MCP — 한눈 요약

| MCP | 기능 영역 | 자주 쓰는 도구 |
|---|---|---|
| **Notion** (`mcp__9cd8e8ad-…`) | 운영 SOP·KPI·리뷰 큐 | `notion-search`, `notion-create-pages`, `notion-update-page`, `notion-fetch` |
| **Google Calendar** (`mcp__9f82eb2d-…`) | 배포 윈도우·on-call·proof 마감 | `create_event`, `list_events`, `suggest_time` |
| **Claude in Chrome** (`mcp__Claude_in_Chrome__*`) | 실제 사이트 자동화 (네이버/쿠팡 셀러 UI) | `navigate`, `find`, `form_input`, `read_page`, `gif_creator` |
| **Claude Preview** (`mcp__Claude_Preview__*`) | dev 서버 UI 검증 (FastAPI / Next.js) | `preview_start`, `preview_screenshot`, `preview_console_logs`, `preview_eval` |
| **Figma** (`mcp__db1e6d74-…`) | 디자인 자산·컨텍스트 | `get_design_context`, `get_screenshot`, `upload_assets`, `generate_diagram` |
| **Desktop Commander** (`mcp__Desktop_Commander__*`) | 로컬 프로세스·파일 | `start_process`, `interact_with_process`, `read_process_output`, `start_search` |
| **PDF Viewer** (`mcp__pdf-viewer__*`) | PDF 표시·상호작용 | `display_pdf`, `interact`, `list_pdfs` |
| **MCP Registry** (`mcp__mcp-registry__*`) | 신규 MCP 발견 | `search_mcp_registry`, `suggest_connectors` |
| **Scheduled Tasks** (`mcp__scheduled-tasks__*`) | OS 레벨 예약 | `create_scheduled_task`, `list_scheduled_tasks` |
| **CCD Session** (`mcp__ccd_session_mgmt__*`) | 이전 세션 검색·아카이브 | `search_session_transcripts`, `list_sessions` |
| **CCD Directory** (`mcp__ccd_directory__*`) | 디렉토리 메타 요청 | `request_directory` |

### D-2. 작업 의도별 MCP 자동 호출

| 작업 의도 | MCP 자동 호출 | 함께 호출할 스킬 |
|---|---|---|
| 운영 SOP · 운영자 리뷰 큐 발행 | Notion `create-pages`/`update-page` | `engineering:documentation` |
| KPI tracker 갱신 (Notion 미러) | Notion `update-page` + xlsx 스킬로 로컬 | `anthropic-skills:xlsx` |
| 배포 윈도우 잡기 | Calendar `create_event` + `suggest_time` | `engineering:deploy-checklist` |
| 운영자 on-call 확인 | Calendar `list_events` | `engineering:incident-response` |
| 실제 네이버 셀러 UI 절차 녹화 | Chrome `navigate`/`find`/`gif_creator` → SOP에 첨부 | `engineering:documentation` |
| 쿠팡 PDS 입점 폼 자동 채움 (운영자 동석) | Chrome `form_input` (L0 자동 제출 금지) | — |
| Mini MVP UI 검증 | Preview `preview_start` + `screenshot` + `console_logs` | `qa`, `superpowers:verification-before-completion` |
| Figma → 상세 이미지 컨텍스트 추출 | Figma `get_design_context`, `get_screenshot` | `design-review` |
| 운영 플로우 다이어그램 자동 생성 | Figma `generate_diagram` | `engineering:architecture` |
| dev 서버 백그라운드 띄우기 + 로그 추적 | Desktop Commander `start_process`/`read_process_output` | — |
| PDF 운영 문서 시각 확인 | PDF Viewer `display_pdf` | — |
| 신규 MCP 후보 탐색 | MCP Registry `search_mcp_registry` (자동 설치 금지) | `cso`, `anthropic-skills:mcp-builder` |
| 예약 작업 등록 (일일 KPI 집계 등) | Scheduled Tasks `create_scheduled_task` | `schedule`, `loop` |
| 이전 세션 컨텍스트 복원 | CCD Session `search_session_transcripts` | `context-restore` |

### D-3. 스마트스토어 / 쿠팡 / Shopify — 공식 MCP 부재 시 폴백

공식 커머스 플랫폼 MCP는 현재 없음. 따라서:

| 작업 | 1차 (선호) | 2차 (폴백) |
|---|---|---|
| 상품 등록 | `store_ops.py platform-payloads` + 운영자 manual upload | Chrome MCP로 셀러 UI 자동화 (L0 제출은 운영자 클릭) |
| OAuth 인증 | `scripts/naver_integration.py --init-auth` (`references/naver-api-guide.md`) | Chrome MCP `navigate` + `form_input` |
| 주문 동기화 | CSV ingest (`store_ops.py ingest-orders`) | REST API (운영자 승인 후) |

비공식 third-party 커머스 MCP 사용은 supply chain·시크릿 리스크로 **금지**. 사용하려면 `cso` 통과 + 운영자 승인.

---

## E. 서브 에이전트 병렬 운영 패턴 — Store OS 특화

### E-1. 빈출 병렬 패턴

| 패턴 | 병렬 단위 | 통합 시점 | 통합 책임자 |
|---|---|---|---|
| 다채널 staging | Naver / Coupang / Shopify 각 1 agent | review-queue 단계 | 메인 세션 |
| 다영역 proof | Legal / Design / Security / QA 각 1 agent (subagent_type=code-reviewer 또는 general-purpose) | Final Proof Agent에서 종합 | Final Proof Agent (별도) |
| 리스팅 대량 생성 | 상품 5–10개당 1 agent | risk_scan 통합 단계 | 메인 세션 |
| 시장 데이터 분석 | 키워드 군집별 1 agent | product_scores.csv 머지 | 메인 세션 |
| 운영 보고서 작성 | 단계별 (KPI / 광고 / CS / 재고) 각 1 agent | 임원 보고서 머지 | `internal-comms` 호출 후 머지 |
| 디자인 변형 탐색 | 스타일별 1 agent | 비교 보드 | `design-shotgun` 가이드 |

### E-2. Subagent 프롬프트 표준

각 subagent 프롬프트는:

1. **목표** — 무엇을 산출할지 (파일·형식·위치)
2. **컨텍스트** — 이 세션의 히스토리를 못 보므로 충분히 설명 (제품·단계·이미 결정된 사항)
3. **제약** — L0 자동화 금지·승인 게이트·산출물 길이 등
4. **반환 형식** — Evidence Card 포함 + Proof decision 비워둠 (proof는 별도 agent)

`superpowers:dispatching-parallel-agents` 스킬을 패턴 가이드로 반드시 참조.

### E-3. Proof 페이즈 분리 강제

```
[Builder subagents — 병렬]
    ↓ (각자 Evidence Card 반환, Proof decision: BLANK)
[Final Proof Agent — 별도 subagent (general-purpose 또는 superpowers:code-reviewer)]
    ↓
Pass / Conditional Pass / Fail
    ↓
[운영자 알림 — Conditional Pass인 경우 추적 조건 + 만료일]
```

이 분리를 어기면 `references/proof-and-audit.md`의 audit log에 위반 기록 + 다음 게이트 자동 Fail.

---

## F. 자동 호출 의무 — 우회 금지 규칙

다음 조건이 충족되면 **사용자가 요청하지 않아도** 해당 스킬·MCP를 자동 호출한다:

| 트리거 | 의무 호출 | 비고 |
|---|---|---|
| 새 기능·신규 스크립트·신규 시스템 설계 시작 | `superpowers:brainstorming` | HARD-GATE: 디자인 승인 전 구현 스킬 금지 |
| Store OS 작업 발화 매칭 (§H-3 GOAL 카탈로그) | 해당 GOAL 카드 작성 → brainstorming | 12개 GOAL ID 자동 매칭 |
| PLM/QMS·엔터프라이즈 시스템 발화 | `anthropic-skills:plm-qms-goals` | §H-1 |
| brainstorming 완료 직후 | `superpowers:writing-plans` | terminal state — 다른 스킬 금지 |
| writing-plans 완료 직후 | `superpowers:subagent-driven-development` (subagent 가용) 또는 `superpowers:executing-plans` | required sub-skill |
| 멀티스텝 작업 (3 step+) 계획 시작 | `superpowers:writing-plans` | docs/superpowers/plans/ 저장 |
| 새 코드·스크립트 작성 시작 | `superpowers:test-driven-development` | Iron Law: 테스트 먼저 |
| 독립 작업 2개 이상 동시 가능 | `superpowers:dispatching-parallel-agents` | §E 패턴 |
| 작업 완료 보고 직전 | `superpowers:verification-before-completion` | Iron Law: fresh 검증 이 메시지에서 |
| 모든 task 완료 시 | `superpowers:finishing-a-development-branch` | 자동 chain |
| 라이브 API·시크릿·결제 코드 작성 | `security-review` (간단) 또는 `cso` (큰 변경) | |
| Claude API 호출 코드 작성·수정 | `claude-api` | 프롬프트 캐싱 적용 의무 |
| SKILL.md 수정 | `anthropic-skills:skill-creator` | description optimizer 포함 |
| MCP 추가·신규 작성 | `cso` → `anthropic-skills:mcp-builder` | supply chain 검토 선행 |
| UI 변경 후 검증 | `qa` + Preview MCP | gstack family |
| 사용자가 "배포·push·PR" 언급 | `ship` → `land-and-deploy` → `canary` | gstack chain |
| "전체 자동 리뷰", "모든 리뷰 돌려" | `autoplan` | CEO+design+eng+DX 통합 |
| "리뷰 평가만" (단일 영역) | `plan-ceo-review` / `plan-eng-review` / `plan-design-review` / `plan-devex-review` | 영역 매칭 |
| "디버그·에러·왜 안 돼" | `investigate` 또는 `superpowers:systematic-debugging` | 4-phase 근본 원인 |
| "코덱스 의견 / 다른 AI" | `codex` | 2nd opinion |
| 회고·주간 정리 | `retro` | 커밋·KPI 기반 |
| 위험 작업 (rm·force-push·prod) | `careful` | 또는 `guard` (careful+freeze) |

이 의무는 **사용자의 명시 거부**가 없는 한 유지. 사용자가 "skip"이라 해도 invoke 후 결과를 짧게 표시하고 진행 여부를 확인.

### F-1. HARD-GATE / Iron Law 위반 시

- brainstorming HARD-GATE 위반 (디자인 승인 전 구현) → 즉시 중단, 처음부터 brainstorming 재시작.
- TDD Iron Law 위반 (테스트 없이 쓴 코드) → 해당 코드 **삭제** 후 테스트부터.
- verification-before-completion Iron Law 위반 ("통과" 주장에 fresh 검증 없음) → 주장 철회, fresh 명령 실행 후 재보고.

---

## G. 스킬 디시플린 카드 — 본문에서 추출한 발동 조건·HARD-GATE·Iron Law

각 카드는 해당 스킬을 호출할 때 **이 세션이 어떤 룰을 받아들이는지**를 명시한다.

### G-1. `superpowers:brainstorming` (HARD-GATE)

| 항목 | 내용 |
|---|---|
| **HARD-GATE** | 디자인을 사용자가 승인하기 전에는 구현 스킬 일체 호출 금지. "이건 너무 단순해" 사고 자체가 안티패턴. |
| **9-step 체크리스트** | 1) project context 탐색 2) visual companion 제안 (해당 시) 3) 한 번에 하나씩 명료화 질문 4) 2–3개 접근법 제시 5) 디자인 섹션별 승인 6) `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md` 저장+commit 7) spec self-review 8) 사용자 spec 검토 게이트 9) writing-plans로 자동 전환 |
| **terminal state** | 오직 `superpowers:writing-plans` 호출만 허용. frontend-design·mcp-builder 등 다른 구현 스킬 금지. |
| **YAGNI** | 모든 디자인에서 불필요 기능 제거. 다른 접근법 2–3개 항상 제시. |
| **Store OS 발동** | 새 상품·새 채널·새 자동화·새 게이트 도입 시 무조건. "근데 이건 작은 변경이라…" → 발동. |

### G-2. `superpowers:writing-plans`

| 항목 | 내용 |
|---|---|
| **announce** | 시작 시 "I'm using the writing-plans skill to create the implementation plan." 출력 의무. |
| **저장 경로** | `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md` (Store OS는 `store-os/plans/`로 매핑) |
| **task granularity** | 2–5분짜리 step 단위 — "Write failing test" / "Run it to fail" / "Implement minimal" / "Run tests" / "Commit" |
| **plan header 필수** | "REQUIRED SUB-SKILL: superpowers:subagent-driven-development (recommended) or superpowers:executing-plans" 라인 포함 |
| **다음 스킬** | subagent 가용 → `subagent-driven-development`. 불가용 → `executing-plans`. |

### G-3. `superpowers:subagent-driven-development`

| 항목 | 내용 |
|---|---|
| **패턴** | task당 fresh subagent — **2-stage review**: spec compliance 먼저, 그 다음 code quality. 둘 다 별도 subagent. |
| **세션 보존** | 같은 세션 안에서 subagent 분기. 메인 세션은 코디네이션에만 집중 → 컨텍스트 보호. |
| **task 완료 후** | TodoWrite 완료. 모든 task 끝나면 final code reviewer subagent → `finishing-a-development-branch`. |
| **Store OS 매핑** | 리스팅 다채널 staging·proof 4영역 분기·시장 데이터 군집별 분석 — 모두 이 패턴. §E 표 참조. |

### G-4. `superpowers:dispatching-parallel-agents`

| 항목 | 내용 |
|---|---|
| **발동 조건** | 2개 이상 독립 문제 도메인. 셋 다 충족 — 공유 상태 없음 · 서로 영향 없음 · 컨텍스트 독립적. |
| **금지 조건** | 실패들이 서로 연관 (하나 고치면 다른 것도 해결될 수도) · 전체 시스템 상태 이해 필요 · agent 간 간섭 가능. |
| **agent prompt 표준** | 1) focused (도메인 1개) 2) self-contained (필요 컨텍스트 전부) 3) specific output (반환 형식 명시) |
| **Store OS 발동** | "Naver·Coupang·Shopify 동시 staging" "Legal+Design+Security+QA proof 동시" — 무조건 병렬. |

### G-5. `superpowers:test-driven-development` (Iron Law)

| 항목 | 내용 |
|---|---|
| **Iron Law** | NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST. 테스트 없이 쓴 코드는 **삭제 후 처음부터**. "참조용으로 두기" 금지. |
| **사이클** | RED (실패 테스트) → 잘못된 실패 검증 → GREEN (최소 구현) → all green 검증 → REFACTOR → green 유지 검증 → 다음. |
| **예외** (사용자 합의 필요) | throwaway prototype · 자동 생성 코드 · 설정 파일. "이번만 skip" 사고 자체가 안티패턴. |
| **Store OS 매핑** | store_ops.py의 45 unittest 가 본 룰을 따른 결과. 신규 스크립트는 동일 기준. |

### G-6. `superpowers:verification-before-completion` (Iron Law)

| 항목 | 내용 |
|---|---|
| **Iron Law** | NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE. **이 메시지에서** 검증 명령을 안 돌렸으면 "통과" "완료" 단어 사용 금지. |
| **gate function** | 1) 이 주장을 입증할 명령은? 2) FULL command 실행 (fresh) 3) 출력 전체 읽고 exit code 확인 4) 출력이 주장 뒷받침? → 5) 그제서야 주장. 한 단계 skip = 거짓말. |
| **금지 표현** | "should" "probably" "seems to" — 검증 없는 만족 표현 ("Great!", "Perfect!", "Done!") |
| **Store OS 매핑** | "테스트 통과", "스크립트 동작" 등 모든 완료 주장 전에 `cd store-os && python -m unittest tests.test_store_ops` 등 fresh run. |

### G-7. `superpowers:executing-plans`

| 항목 | 내용 |
|---|---|
| **언제** | subagent 미가용 환경. 또는 사용자가 별도 세션에서 실행 원할 때. |
| **순서** | 1) 플랜 로드 + 비판적 검토 (의문 있으면 사용자에게 raise) 2) TodoWrite 생성 3) task별 in_progress → 단계 그대로 → 검증 → completed 4) 모두 끝나면 `finishing-a-development-branch` 호출 |
| **stop 조건** | blocker · 플랜 결함 · 지시 불분명 · 검증 반복 실패 → 추측 말고 사용자에게 질문. |

### G-8. `engineering:code-review` 또는 `superpowers:code-reviewer`

| 항목 | 내용 |
|---|---|
| **호출 위치** | builder가 끝낸 후, 별도 subagent로. 같은 세션의 builder가 자기 결과를 리뷰하지 않는다. |
| **Store OS 매핑** | Final Proof Agent의 일부. §E-3 Proof 페이즈 분리 도식 참조. |

### G-9. `claude-api`

| 항목 | 내용 |
|---|---|
| **발동 조건** | Anthropic SDK import 또는 Claude API 호출 코드 작성·수정 시. |
| **의무** | 프롬프트 캐싱 적용. thinking·tool use·batch 기능 도입 시 본 스킬 가이드 의무 참조. |
| **Store OS 매핑** | `auto_claude.py` 개선 · 향후 CS·이미지 brief 자동화 모두 본 스킬 통과. |

### G-10. `anthropic-skills:skill-creator`

| 항목 | 내용 |
|---|---|
| **발동 조건** | 새 스킬 작성 · 기존 스킬 수정 · description 최적화. |
| **eval 의무** | 변경 후 trigger eval 실행 권장 (Windows에서는 `PYTHONUTF8=1` + `shutil.which("claude")` 패치 필요 — §G 참조). |

### G-11. `gstack` 패밀리 라우팅

| 발화·작업 | gstack 스킬 |
|---|---|
| "사이트 열어줘" "스크린샷" "QA 해줘" | `browse`, `qa`, `qa-only` |
| "디자인 평가" | `design-review`, `design-shotgun`, `design-consultation`, `design-html` |
| "퍼포먼스 측정" | `benchmark`, `benchmark-models` |
| "보안 감사" | `cso` |
| "배포 / 머지 / PR" | `ship` → `land-and-deploy` → `canary` |
| "회고 / 위클리" | `retro`, `landing-report` |
| "전체 자동 리뷰" | `autoplan` (CEO + design + eng + DX 통합 — 6원칙 자동 결정 + 최종 게이트) |
| "주의 모드" | `careful`, `freeze`, `guard` |
| "코덱스 의견" | `codex` |
| "디버그" | `investigate` |
| "건강도" | `health` |

`autoplan`은 "review" 키워드 다발 시 우선 후보. 단, 사용자가 단일 리뷰만 원하면 개별 `plan-*-review` 사용.

---

## H. GOAL 카드 — 복잡 시스템 작업의 표준 정의 도구

`anthropic-skills:plm-qms-goals`는 자동차 PLM/QMS 도메인용이지만 **GOAL 카드 패턴 자체는 Store OS의 복잡 작업에도 그대로 쓴다**.

### H-1. plm-qms-goals 자동 호출 조건

| 발화·맥락 | 호출 |
|---|---|
| "PLM 개발", "QMS 구축", "토탈 시스템" | plm-qms-goals |
| "BOM 관리", "ECN/ECO 워크플로우", "PPAP/APQP" | plm-qms-goals |
| "협력사 포털", "감사 추적", "규제 준수 시스템" | plm-qms-goals |
| "엔터프라이즈 시스템 개발 목표 설정" | plm-qms-goals |
| Store OS 작업이지만 사용자가 "GOAL 템플릿으로 정의해줘"라고 명시 | plm-qms-goals (템플릿 형식 차용) |

### H-2. Store OS용 GOAL 카드 표준

모든 복잡 작업·기능 도입 시 다음 GOAL 카드를 먼저 작성한다 (brainstorming 1단계와 결합):

```markdown
# GOAL Card — [STORE-XX] <작업명>

**목표**: <한 줄로 무엇을 만들 것인가>

**범위**:
- 포함:
- 제외:
- 단계: Mini / Standard / Full

**Observations** (현재 상태·근거 데이터):

**Alternatives** (검토한 대안 2–3개):

**Logic** (선택 이유):

**Risks** (식별된 리스크 + 완화):
- L0 자동화 영향 여부:
- 법률·과대광고·아동대상 영향 여부:
- 시크릿·PII 영향 여부:

**Decision Needed** (사용자가 결정해야 할 사항):

**Evidence Required** (이 작업이 Pass 받기 위해 필요한 증거):
- 테스트:
- 스크린샷·로그:
- 운영자 승인:
- proof agent 결정:

**Trigger Keywords** (이 GOAL이 발동되는 사용자 발화):
```

### H-3. Store OS GOAL 카드 카탈로그 (자동 매칭)

사용자 발화에서 다음 키워드가 감지되면 해당 GOAL 카드부터 작성한다:

| GOAL ID | 작업 | 트리거 키워드 |
|---|---|---|
| **[STORE-01]** | 신규 상품 라인 출시 | "새 상품", "라인업 추가", "다른 카테고리", "[제품명] 팔고 싶다" |
| **[STORE-02]** | 신규 채널 입점 | "쿠팡 입점", "Shopify 추가", "다채널", "스마트스토어 자동화" |
| **[STORE-03]** | Claude API 자동화 도입 | "AI로 상품 설명", "CS 자동", "이미지 brief 자동", "Claude API" |
| **[STORE-04]** | 단계 졸업 (Mini→Standard→Full) | "Standard로 가도 되나", "Full 단계 준비", "월 매출 100만원 달성" |
| **[STORE-05]** | OAuth·API 연동 | "네이버 API", "쿠팡 API", "OAuth", "refresh token" |
| **[STORE-06]** | 법률·과대광고·아동대상 점검 | "전자상거래법", "100% 효과", "초등학생 대상", "과대광고" |
| **[STORE-07]** | proof / audit / kill-switch 설계 | "승인 게이트", "audit log", "자동 일시정지", "환불 자동" |
| **[STORE-08]** | 이미지·디자인 자동 생성 | "썸네일", "상세 이미지", "프린터블 PDF", "디자인 brief" |
| **[STORE-09]** | KPI 추적·운영 보고 | "KPI tracker", "운영 대시보드", "주간 보고", "ROAS" |
| **[STORE-10]** | IP / 저작권 / 상표 precheck | "캐릭터 라이선스", "디즈니", "산리오", "상표권" |
| **[STORE-11]** | 배포·릴리즈·인프라 | "Railway 배포", "Vercel 배포", "PostgreSQL 마이그레이션" |
| **[STORE-12]** | MCP·플러그인 연결 | "Notion 연동", "Figma 자산", "새 MCP 추가" |

각 GOAL 발동 후 자동 체인:
```
[GOAL Card 작성]
   ↓
brainstorming (HARD-GATE — 사용자 디자인 승인)
   ↓
writing-plans
   ↓
subagent-driven-development (또는 executing-plans)
   ↓
verification-before-completion
   ↓
Final Proof Agent (별도 subagent — Pass/Cond/Fail)
   ↓
Evidence Card 마무리 + audit log 기록
```

### H-4. plm-qms-goals 활용 시나리오 (Store OS 외 작업)

사용자가 Store OS 외에 PLM/QMS 시스템 개발을 요청하면 plm-qms-goals 스킬을 invoke하여:
- `/goal [PLM-XX]` 또는 `/goal [QMS-XX]` 형식으로 작업 정의
- 자동차 부품 도메인 컨텍스트 (BOM·ECO·PPAP·APQP) 자동 반영
- 협력사 포털·CAD 통합·감사 추적 등 엔터프라이즈 기능 GOAL 템플릿 사용

---

## I. 환경·도구 사용 규칙 (이 머신 한정)

- **OS**: Windows 11 Pro, PowerShell 기본. Bash 도구 가용 — POSIX 도구가 깔끔할 때 Bash.
- **Python 인코딩**: cp949 default. 신규 스크립트는 `sys.stdout.reconfigure(encoding='utf-8')` 또는 `PYTHONUTF8=1`.
- **subprocess + claude CLI**: Windows에선 `claude` → `claude.cmd`. 항상 `shutil.which("claude")`로 해석.
- **테스트 회귀 게이트**: `cd store-os && python -m unittest tests.test_store_ops` 통과 의무 (현재 45/45).
- **아카이브 폴더**: `_archive/claude-store-os`, `_archive/store-os-v2` 는 참조 전용. 수정 금지.

---

## J. 응답·산출물 규칙

- 한국어 우선. 명령어·파일 경로·코드 블록은 영어 원문.
- 시간·비용·법률 리스크는 항상 명시. "약간 / 곧 / 빠르게" 같은 모호어 금지.
- 완료 보고 전 verification 단계 의무.
- audit·proof·승인 게이트 작업은 Evidence Card 끝맺음 필수.
- 작업 후 변경 사항·다음 행동만 1–2문장 요약. 자랑·반복 금지.

---

## K. 위반 시 처리

| 위반 | 처리 |
|---|---|
| Builder가 자기 Pass 찍은 흔적 | 즉시 Fail + audit 추가 |
| 병렬 가능 작업을 순차로 돌림 | 다음 작업에서 병렬로 재시도 |
| 필수 스킬 invoke 없이 완료 | 다시 스킬로 invoke해 검증 후 완료 보고 |
| L0 자동화 실행 시도 | 즉시 중단 + 운영자 보고 |
| 시크릿을 코드·프롬프트·문서에 저장 | 즉시 회수 + git history 정리 + audit |
| 비공식 third-party MCP 임의 설치 | 즉시 비활성화 + `cso` 의뢰 |

---

## L. 자주 참조하는 파일 위치

### L-1. Store OS 스킬 자산
| 파일 | 용도 |
|---|---|
| `store-os/SKILL.md` | 스킬 본체 (3단계·proof·자동화 경계) |
| `store-os/references/three-tier-rationale.md` | 단계 건너뛰기 차단 근거 |
| `store-os/references/proof-and-audit.md` | proof decision·audit 스키마·게이트 |
| `store-os/references/full-tier-ops-harness.md` | store_ops.py 명령 카탈로그 |
| `store-os/references/cost-breakdown.md` | 단계별 비용·손익분기 |
| `store-os/references/naver-api-guide.md` | 네이버 OAuth·상품 등록 |
| `store-os/references/legal-checklist.md` | 전자상거래법 체크 |
| `store-os/scripts/store_ops.py` | Full 단계 운영 하네스 (45 unittest) |
| `store-os/scripts/validate_idea.py` | Mini 단계 아이디어 검증 |
| `store-os/scripts/legal_check.py` | 법률·과대광고 자동 점검 |
| `store-os/scripts/cost_calculator.py` | 단계별 월 비용 시뮬레이터 |
| `store-os/examples/mini-mvp/app.py` | 10분 작동 주문 시스템 (FastAPI+SQLite) |
| `store-os/evals/trigger-eval.json` | 스킬 트리거 평가 데이터셋 |
| `_archive/` | v1·v2 (참조 전용) |

### L-2. superpowers 표준 산출물 경로 (Store OS에서도 동일 적용)
| 산출물 | 경로 | 생성 스킬 |
|---|---|---|
| 디자인 spec | `store-os/docs/specs/YYYY-MM-DD-<topic>-design.md` | `superpowers:brainstorming` |
| 구현 플랜 | `store-os/docs/plans/YYYY-MM-DD-<feature-name>.md` | `superpowers:writing-plans` |
| GOAL 카드 | `store-os/docs/goals/STORE-XX-<작업명>.md` | §H-2 GOAL 표준 |
| Evidence Card | 작업 응답 끝부분 + audit_log.csv | Builder/Proof 에이전트 |

### L-3. 스킬 디렉토리 위치 (참조용)
| 패밀리 | 위치 |
|---|---|
| superpowers | `~/.claude/plugins/cache/claude-plugins-official/superpowers/5.0.7/skills/` |
| gstack | `~/.claude/skills/gstack/` (autoplan·browse·qa 등) |
| anthropic-skills | `~/AppData/Roaming/Claude/.../skills/` (plm-qms-goals·skill-creator·xlsx 등) |
| engineering | `~/AppData/Roaming/Claude/.../plugin_01FTLa86.../skills/` |
| design | `~/AppData/Roaming/Claude/.../plugin_01XXJmxL.../skills/` |
| customer-support | `~/AppData/Roaming/Claude/.../plugin_016kCmK4.../skills/` |
| adobe-for-creativity | `~/AppData/Roaming/Claude/.../plugin_017FSfZw.../skills/` |

---

## M. 운영자에게 전달할 한 줄

"규칙을 우회하면 단기 효율은 오르지만 사고 비용이 매출보다 빨리 늘어난다. 그게 가게가 망하는 순서다."
