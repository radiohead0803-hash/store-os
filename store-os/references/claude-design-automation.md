# Claude Design Automation

> Store OS 디자인 자산은 **Claude Design 워크플로**로 생성한다. 운영자가 외부 디자인 도구(Canva 등)를 직접 다루지 않고, AI 생성 → 운영자 승인 → DesignAsset 레코드 워크플로를 따른다.

## "Claude Design" 정체 명시

**"Claude Design"은 Anthropic의 별도 제품이 아닙니다.** 본 프로젝트 내부에서 사용하는 워크플로 명칭이며, 실체는 **Claude(LLM)와 주변 도구를 묶은 AI 디자인 파이프라인**입니다.

`anthropic-skills:canvas-design`(HTML canvas 그래픽 스킬)과도 다릅니다 — 두 명칭이 비슷해서 혼동하기 쉽지만 별개.

### 5가지 실제 구현 경로

| 경로 | 출력물 | 비용 | 본 환경 가용 | 적합 작업 |
|---|---|---|---|---|
| **A. Claude가 SVG/HTML 직접 작성** | 벡터 그래픽·UI 레이아웃·인쇄용 도형 | 무료 (Claude 사용권) | ✅ | 보드판·스티커·인포그래픽·인쇄용 PDF 소스·간단 썸네일 |
| **B. claude.ai Artifacts** | SVG·HTML·React 컴포넌트 인터랙티브 미리보기 | 무료 (Pro·Free) | ⚠️ 사용자가 claude.ai 웹에서 실행 | UI 시안 비교·인터랙티브 mockup·운영자 시연 |
| **C. Claude API + 이미지 생성 API 연동** | 사진풍 비트맵 (DALL-E 3·Stable Diffusion·Midjourney·Replicate 등) | 약 $0.04–0.08/장 | ⚠️ 별도 API 키 필요 | 상품 사진·라이프스타일 컷·고품질 마케팅 이미지 |
| **D. Figma MCP 연동** | 실제 Figma 파일 (Auto Layout·컴포넌트·디자인 시스템) | Figma 계정 | ✅ `mcp__db1e6d74-…__use_figma` | 디자인 시스템·재사용 컴포넌트·Standard 단계 브랜드 통일 |
| **E. Adobe 스킬 연동** | 사진 리터칭·리사이즈·소셜 변형·템플릿 디자인 | Adobe Creative Cloud | ✅ `adobe-for-creativity:adobe-*` | 입고 사진 가공·소셜 미디어 변형·배치 편집 |

### Store OS 작업별 권장 경로

```
[보드판·스티커 베이스 (Mini 단계)]    → A (Claude SVG 직접)
[인쇄용 다이컷·키스컷 가이드 추가]    → A + 수동 vendor 템플릿 입력
[베타 후기 사진·상품 입고 사진 가공]  → E (Adobe 스킬)
[마케팅 라이프스타일 컷 (Standard+)]  → C (이미지 생성 API)
[디자인 시스템·브랜드 통일 (Full)]    → D (Figma MCP)
[운영자 시연용 인터랙티브 mockup]     → B (Artifacts)
```

## Core Rule

워크플로(경로 A–E 무관)는 디자인 자산을 생성·수정할 수 있지만, **인쇄 proof + 저작권 점검 + 운영자 승인이 기록되기 전에는 상품을 출시할 수 없다.**

## 워크플로 (필수 단계 순서)

```
product idea
   ↓
design brief (Claude Design 프롬프트 작성)
   ↓
Claude Design 자산 생성 (v1)
   ↓
DesignAsset 레코드 저장 (prompt + file + version + proof_status=pending)
   ↓
인쇄 proof / readability proof (실제 출력 또는 vendor 미리보기 검증)
   ↓
저작권·상표·과대광고 점검 (legal_check.py + 수동)
   ↓
운영자 검토 + 승인 (operator_approval=approved)
   ↓
listing 자산으로 등록 (상품 페이지·인쇄소 발주에 사용)
```

**Builder ≠ Proof**: Claude Design이 자산을 만들고 proof status를 "pass"로 자기 채점할 수 없다. 별도 proof agent 또는 운영자가 판정.

## 필수 디자인 자산 (Store OS 기본)

| Asset | 용도 | 필요한 proof |
|---|---|---|
| A4 reward board PDF | 칭찬스티커 보드판 본체 | A4 출력 가독성 사진 또는 화면 캡처 |
| sticker sheet | 물리 스티커 시트 (다이컷/키스컷) | 크기·cutline·bleed·safe area 확인 |
| 썸네일 | 상품 페이지 클릭 자산 | 모바일 가독성 확인 |
| 상세 이미지 | 리스팅 설명 자산 | 구성·크기·사용법 명료성 |
| 사용 안내 카드 | 고객 사용 가이드 | 오해 소지 표현 없음 |
| 패키지 라벨 | 배송 패키지 브랜딩 | 주소·개인정보 안전 레이아웃 |

## Claude Design 프롬프트 구조 (필수 10요소)

모든 프롬프트는 다음 10요소를 포함:

1. **제품명**과 타겟 고객
2. **자산 종류** (보드 / 스티커 / 썸네일 등) **+ 크기**
3. **사용 장면** (가정 / 학교 / 등)
4. **스타일 제약** (파스텔·미니멀·일러스트 등)
5. **포함할 텍스트** (한국어 원본 그대로)
6. **인쇄 제약** (CMYK·해상도·bleed 등)
7. **접근성·가독성 제약** (어린이 + 학부모 둘 다 읽힘)
8. **회피할 것** (저작권 캐릭터·과대광고·미세 글씨)
9. **필수 export** (PDF/PNG·해상도·sRGB·CMYK)
10. **proof 체크리스트** (출력 후 확인할 항목)

## 인쇄 제약 기본값 (스티커·보드)

| 항목 | 기본값 |
|---|---|
| 보드판 | A4 세로 PDF |
| 스티커 시트 | 정사각 30매, vendor 템플릿 우선 |
| Bleed | vendor 템플릿 따름. 없으면 3mm bleed 표기 요청 |
| Safe area | 텍스트·아이콘은 cutline에서 충분히 안쪽 |
| Color | 파스텔, 인쇄에서 충분한 대비 |
| Text | 한국어, 초등학생·학부모 모두 가독 크기 |
| 금지 | 저작권 캐릭터, 단정적 학습 효과, 미세 글씨 |

## DesignAsset 레코드 (모든 자산 필수)

각 생성된 자산을 다음 스키마로 기록:

| Field | 값 |
|---|---|
| `product_id` | 연결된 상품 (예: `STORE-01-STD`) |
| `type` | `board_pdf` / `sticker_sheet` / `thumbnail` / `detail_image` / `instruction_card` / `package_label` |
| `prompt` | Claude Design에 보낸 원본 프롬프트 |
| `file_path` | 저장 경로 (예: `store-os/docs/evidence/store-01/day-01-design-v1/board-a4-v1.pdf`) |
| `version` | `v1` / `v2` / `v3` ... |
| `proof_status` | `pending` / `pass` / `conditional` / `fail` |
| `operator_approval` | `pending` / `approved` / `rejected` |
| `generated_at` | ISO 8601 |
| `approved_at` | ISO 8601 또는 빈 값 |

저장 위치: `store-os/docs/evidence/<store-id>/design-assets.csv` 누적.

## 디자인 실패 처리

| 실패 양상 | 대응 |
|---|---|
| 텍스트 너무 작음 | 글자 크기 ↑·섹션 수 ↓로 재생성 |
| Cutline 불안전 | vendor 템플릿 적용 후 재생성 |
| 저작권 리스크 | 자산 폐기 + 일반 도형·아이콘으로 재생성 + IP precheck |
| 인쇄 색감 약함 | 고대비 + 흑백 버전 동시 생성 |
| AI 출력 일관성 부족 | 승인된 레이아웃 lock + 카피·색만 변경 요청 |
| Claude Design 미가용 | fallback to upload 템플릿 또는 수동 디자인 도구, 예외 기록 |

## Proof 체크리스트

자산 1건당 다음 모두 통과해야 listing publish 가능:

- [ ] A4 출력이 데스크탑·모바일 미리보기 둘 다 가독
- [ ] 실제 크기 출력·미리보기에서 텍스트 읽힘
- [ ] 스티커 cutline + safe area 통과
- [ ] 저작권 캐릭터·상표·복제 디자인 없음 (IP precheck)
- [ ] 단정적 학습·성과 보장 표현 없음 (`legal_check.py` 통과)
- [ ] 썸네일이 모바일 크기에서 가독
- [ ] **운영자 승인 기록 (operator_approval=approved)**

## 자동화 경계

| 작업 | 레벨 | 비고 |
|---|---|---|
| Claude Design 프롬프트 작성 | L1 | 운영자 작성 또는 AI 초안 + 편집 |
| Claude Design 자산 생성 | L1 (자산이 unpublished 상태로만) | AI 실행 |
| DesignAsset 레코드 저장 | L2 (승인 자동화) | 생성 직후 자동 기록 |
| 인쇄 proof 통과 판정 | L0–L1 | 운영자 또는 proof agent (별도) |
| 저작권 점검 | L1 | 운영자 + IP precheck 자동화 |
| listing publish 승인 | **L0** | 운영자 직접 |
| 인쇄소 발주 | **L0** | 운영자 직접 |

**L0 절대 자동화 금지**: 디자인 자산을 운영자 승인 없이 public listing에 노출하거나 인쇄 발주에 사용.

## 예시 프롬프트 (STORE-01 보드판)

```
[제품] 초등 저학년 칭찬스티커 보드판
[타겟] 초등 1–3학년 자녀를 둔 학부모
[자산] A4 세로 PDF, 210×297mm, CMYK
[사용 장면] 가정 냉장고 또는 아이 방 벽에 부착
[스타일] 파스텔 색감 (민트·핑크·연노랑 중 1–2색), 미니멀, 어린이 친화
[텍스트]
  상단 좌측: "이름: __________" (한국어, 손글씨 영역)
  중앙 그리드: 5열 × 6행 = 30칸 (각 30×30mm, 칸 간 2mm 간격)
  하단: "이번 달 목표: __________"
[인쇄 제약] CMYK, 300dpi, bleed 3mm, safe area 5mm
[가독성] 초등학생 키 110cm 기준 1m 거리에서 텍스트 읽힘
[회피] 캐릭터·로고·저작권 일러스트·"학습 효과 보장" 같은 단정 표현
[필수 export] PDF (CMYK 인쇄용) + PNG (썸네일·웹용)
[proof 체크리스트]
  - A4 출력 시 글자 가독성
  - 칸 격자 정렬
  - 색감 sRGB↔CMYK 변환 안정성
  - 저작권·상표 점검
```

## 참고

- 저작권·상표 사전 점검: `_archive/claude-store-os/references/ip-copyright-precheck.md` (필요 시 `store-os/references/`로 입양)
- 법률 자동 점검: [legal-checklist.md](legal-checklist.md) + `scripts/legal_check.py`
- proof·audit 게이트: [proof-and-audit.md](proof-and-audit.md)
- 자동화 경계 일반 원칙: SKILL.md §자동화 경계
