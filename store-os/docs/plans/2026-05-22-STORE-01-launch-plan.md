# [STORE-01] 초등 칭찬스티커 보드판 출시 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended for code-heavy tasks) or `superpowers:executing-plans` (recommended for this operational plan). Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Mini 단계 졸업 조건(실 판매 10건 + 긍정 리뷰 3건 + 순이익 > 0)을 14일 안에 확보한다.

**Architecture:** 14일을 12개 task로 분할. **Claude Design**으로 디자인 자산 생성 → 운영자 승인 → 인쇄소 발주 → 스마트스토어 입점 → 마케팅 → 일일 운영 → Mini 졸업 평가. 모든 디자인 자산은 DesignAsset 레코드로 버전 관리되며 proof_status·operator_approval이 통과한 자산만 인쇄·listing에 사용된다. AI는 L1 자산 생성·카피 초안, L0 작업(법률 승인·인쇄 발주·결제·환불)은 운영자 직접.

**Tech Stack:** **Claude Design** (디자인 자산 생성) · 외부 인쇄소 (50건 발주) · 네이버 스마트스토어 (1채널) · `store-os/scripts/` (legal_check·auto_claude·cost_calculator) · `store-os/docs/evidence/store-01/` (증거 누적) · DesignAsset 레코드 CSV · 한국어 운영.

**Spec ref:** [2026-05-22-STORE-01-design.md](../specs/2026-05-22-STORE-01-design.md)
**GOAL ref:** [STORE-01-praise-sticker-board.md](../goals/STORE-01-praise-sticker-board.md)
**Design automation ref:** [claude-design-automation.md](../../references/claude-design-automation.md)

---

## File Structure

```
store-os/docs/evidence/store-01/
├── README.md
├── design-assets.csv                       # DesignAsset 레코드 누적
├── day-01-design-v1/
│   ├── prompt-board.md                     # Claude Design 보드판 프롬프트
│   ├── prompt-stickers.md                  # 스티커 시트 프롬프트
│   ├── board-v1.pdf                        # AI 생성 보드판 v1
│   ├── stickers-v1.pdf                     # AI 생성 스티커 v1
│   ├── iteration-notes.md                  # v1→v2→… 변경 사유
│   └── design-notes.md
├── day-02-design-approval/
│   ├── self-print-photo-board.jpg
│   ├── self-print-photo-stickers.jpg
│   ├── board-print-ready.pdf               # CMYK 변환 + 승인본
│   ├── stickers-print-ready.pdf
│   ├── ip-precheck-output.md               # 저작권·상표 점검
│   ├── operator-approval.md                # operator_approval=approved 기록
│   └── inspection-notes.md
├── day-03-print-quotes/
│   ├── quote-shop-a.txt
│   ├── quote-shop-b.txt
│   ├── quote-shop-c.txt
│   └── selection-decision.md
├── day-04-print-order/
│   ├── order-confirmation.pdf
│   └── color-proof-request.md
├── day-05-06-listing/
│   ├── listing-draft-v1.md
│   ├── legal-check-output.txt
│   ├── listing-final.md
│   └── listing-screenshots/
├── day-07-marketing-seed/
│   ├── prompt-blog.md                      # Claude Design + 카피 프롬프트
│   ├── blog-post-01.md
│   ├── instagram-post-01.md
│   └── legal-check-content.txt
├── day-08-quality-check/
│   ├── unboxing-photos/
│   ├── usage-test-5min-photos/
│   └── inspection-decision.md
├── day-09-public-launch/
│   ├── public-listing-screenshot.png
│   └── publish-audit-log.md
├── day-10-beta-delivery/
│   ├── beta-feedback-01.md
│   ├── beta-feedback-02.md (if any)
│   └── beta-photos/
├── day-11-marketing-publish/
│   ├── publish-log.md
│   └── content-published/
├── day-12-14-ops/
│   ├── kpi.csv
│   ├── cs-tickets/
│   └── orders-log.md
└── graduation-evaluation/
    ├── final-kpi-summary.md
    └── proof-decision.md
```

---

## Critical Path

```
Task 1 (Day 1)         Task 2 (Day 2)         Task 3 (Day 3)         Task 4 (Day 4)
Claude Design 생성  →  IP precheck +       →  인쇄소 견적·프루프  →  50건 발주
+ DesignAsset 기록     운영자 승인                                     ↓
                                                                       (납기 3–5일)
Task 5 (Day 5–6)       Task 6 (Day 7)         Task 7 (Day 8)  ←────────┘
상품 페이지            마케팅 시드            입고 검수
                                                ↓
Task 8 (Day 9)     →   Task 9 (Day 10)    →   Task 10 (Day 11)
공개 전환              베타 발송              마케팅 본격
                                                ↓
                                          Task 11 (Day 12–14)
                                          일일 운영
                                                ↓
                                          Task 12
                                          졸업 평가
```

---

## Task 1: Claude Design 자산 생성 (Day 1)

**Files:**
- Create: `store-os/docs/evidence/store-01/design-assets.csv` (초기 헤더 + 2 row)
- Create: `store-os/docs/evidence/store-01/day-01-design-v1/prompt-board.md`
- Create: `store-os/docs/evidence/store-01/day-01-design-v1/prompt-stickers.md`
- Create: `store-os/docs/evidence/store-01/day-01-design-v1/board-v1.pdf`
- Create: `store-os/docs/evidence/store-01/day-01-design-v1/stickers-v1.pdf`
- Create: `store-os/docs/evidence/store-01/day-01-design-v1/iteration-notes.md`
- Create: `store-os/docs/evidence/store-01/day-01-design-v1/design-notes.md`

**Reference:** `store-os/references/claude-design-automation.md` 의 프롬프트 10요소 + 인쇄 제약 기본값 따름.

- [ ] **Step 1: design-assets.csv 초기화**

```bash
cd "C:/Users/admin/Documents/Claude/Projects/Claude Store OS"
cat > store-os/docs/evidence/store-01/design-assets.csv <<'EOF'
product_id,type,prompt_file,file_path,version,proof_status,operator_approval,generated_at,approved_at
EOF
```

- [ ] **Step 2: 보드판 Claude Design 프롬프트 작성**

`store-os/docs/evidence/store-01/day-01-design-v1/prompt-board.md` 에 [claude-design-automation.md](../../references/claude-design-automation.md) §예시 프롬프트(STORE-01 보드판)의 10요소를 적용:

```markdown
[제품] 초등 저학년 칭찬스티커 보드판
[타겟] 초등 1–3학년 자녀를 둔 학부모
[자산] A4 세로 PDF, 210×297mm, CMYK 인쇄용
[사용 장면] 가정 냉장고 또는 아이 방 벽에 부착
[스타일] 파스텔 색감(민트·핑크·연노랑 중 1–2색), 미니멀, 어린이 친화
[텍스트]
  - 상단 좌측: "이름: __________" (한국어, 손글씨 영역)
  - 중앙 그리드: 5열 × 6행 = 30칸 (각 30×30mm, 칸 간 2mm 간격)
  - 하단: "이번 달 목표: __________"
[인쇄 제약] CMYK, 300dpi, bleed 3mm, safe area 5mm
[가독성] 초등학생 키 110cm 기준 1m 거리에서 텍스트 가독
[회피] 캐릭터·로고·저작권 일러스트, "학습 효과 보장" 같은 단정 표현
[필수 export] PDF (CMYK 인쇄용) + PNG (썸네일·웹용)
[proof 체크리스트]
  - A4 출력 가독성
  - 칸 격자 정렬
  - 색감 sRGB↔CMYK 변환 안정성
  - 저작권·상표 점검
```

- [ ] **Step 3: 보드판 Claude Design 자산 생성**

Claude Design에서 위 프롬프트로 자산 생성. 결과 PDF를 다운로드:
- `store-os/docs/evidence/store-01/day-01-design-v1/board-v1.pdf`

생성 결과 만족스럽지 않으면 `iteration-notes.md` 에 v1 → v2 변경 사유 기록 후 재생성. 통과까지 반복.

- [ ] **Step 4: 스티커 시트 Claude Design 프롬프트 작성**

`store-os/docs/evidence/store-01/day-01-design-v1/prompt-stickers.md`:

```markdown
[제품] 칭찬스티커 시트 (보드판 매칭)
[타겟] 동일
[자산] A4 다이컷 스티커 시트 PDF, 6열 × 5행 = 30매, 각 30×30mm 정사각
[사용 장면] 보드판에 부착하여 행동·칭찬 표시
[스타일] 보드판과 동일 파스텔 톤
[텍스트] 30매 메시지 분포:
  행동 기반 10매: "스스로 정리했어요", "약속 지켰어요", "양보했어요", "도와줬어요", "참았어요", "감사 표현했어요", "스스로 일어났어요", "숙제 끝냈어요", "정리정돈했어요", "차분히 기다렸어요"
  일반 칭찬 10매: "잘했어요", "최고예요", "고마워요", "사랑해요", "자랑스러워요", "멋져요", "굿!", "OK!", "Yay!", "★"
  자유 10매: 이모지·도형 (🌟⭐❤️🎉👍😊🏆🌈🎈🍀)
[인쇄 제약] CMYK, 300dpi, vendor 다이컷 또는 키스컷 템플릿, safe area 텍스트가 cutline에서 3mm 이상 안쪽
[회피] 저작권 캐릭터, 단정 표현, 미세 글씨
[필수 export] PDF (다이컷 가이드 라인 포함)
[proof 체크리스트]
  - 텍스트 30×30mm 안에서 가독
  - cutline + safe area 통과
  - 저작권 안전
```

- [ ] **Step 5: 스티커 시트 자산 생성**

Claude Design 실행 → `stickers-v1.pdf` 저장. 만족 시까지 반복, iteration-notes에 기록.

- [ ] **Step 6: DesignAsset 2개 row 추가**

```bash
TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
cat >> store-os/docs/evidence/store-01/design-assets.csv <<EOF
STORE-01-STD,board_pdf,day-01-design-v1/prompt-board.md,day-01-design-v1/board-v1.pdf,v1,pending,pending,$TS,
STORE-01-STD,sticker_sheet,day-01-design-v1/prompt-stickers.md,day-01-design-v1/stickers-v1.pdf,v1,pending,pending,$TS,
EOF
```

- [ ] **Step 7: design-notes.md 작성**

```markdown
# Day 1 Claude Design 자산 v1 노트

- 보드판 v1: prompt-board.md 기반, A4 세로, 30칸 그리드, 파스텔 [실제 색감].
- 스티커 v1: prompt-stickers.md 기반, 30매 다이컷, 메시지 분포 [실제 분포].
- iteration 횟수: [N회]
- DesignAsset 레코드: 2건 추가 (proof_status=pending, operator_approval=pending)
- 다음 단계: Day 2 IP precheck + 운영자 승인
```

- [ ] **Step 8: Commit**

```bash
git add store-os/docs/evidence/store-01/
git commit -m "store-01(day-1): Claude Design 보드판·스티커 v1 생성 + DesignAsset 등록"
```

---

## Task 2: IP precheck + 운영자 승인 (Day 2)

**Files:**
- Create: `store-os/docs/evidence/store-01/day-02-design-approval/ip-precheck-output.md`
- Create: `store-os/docs/evidence/store-01/day-02-design-approval/self-print-photo-board.jpg`
- Create: `store-os/docs/evidence/store-01/day-02-design-approval/self-print-photo-stickers.jpg`
- Create: `store-os/docs/evidence/store-01/day-02-design-approval/board-print-ready.pdf`
- Create: `store-os/docs/evidence/store-01/day-02-design-approval/stickers-print-ready.pdf`
- Create: `store-os/docs/evidence/store-01/day-02-design-approval/operator-approval.md`
- Create: `store-os/docs/evidence/store-01/day-02-design-approval/inspection-notes.md`
- Modify: `store-os/docs/evidence/store-01/design-assets.csv` (proof_status·operator_approval 업데이트)

- [ ] **Step 1: 자가 출력 검수**

`day-01-design-v1/board-v1.pdf` 및 `stickers-v1.pdf` 를 가정 프린터로 A4 출력. 자연광에서 사진 촬영:
- `self-print-photo-board.jpg`
- `self-print-photo-stickers.jpg`

4개 체크포인트 (claude-design-automation.md proof 체크리스트):
1. 글자 크기·가독성 OK?
2. 칸 격자 비뚤어지지 않음?
3. 색감 화면 대비 변색 심각?
4. 여백·marginal 균형 OK?

문제 있으면 Task 1로 회귀 → Claude Design 재생성 → 재출력. 통과까지.

- [ ] **Step 2: IP precheck (저작권·상표 점검)**

`ip-precheck-output.md` 에 다음 항목 자가 점검:

```markdown
# Day 2 IP Precheck (보드판 v1 + 스티커 v1)

## 점검 항목
- [ ] 캐릭터·연예인·로고 사용 0
- [ ] 디즈니·산리오·기타 라이선스 캐릭터 0
- [ ] 폰트 라이선스 OK (한국어 무료 상업용 또는 구매한 폰트)
- [ ] 일러스트·아이콘 무료 상업 이용 가능 자산만 (Iconify·Lucide 등) 또는 직접 그림
- [ ] 디자인 스타일이 특정 제품의 명백한 복제가 아님 (네이버 쇼핑 1페이지 시각 비교)

## 결과
- [✓ 통과] / [⚠️ 수정 필요: …] / [❌ 차단]

## 근거 자료
- 폰트: [폰트명] (라이선스 [Open/구매])
- 아이콘·일러스트: [출처]
- 디자인 스타일 비교: 네이버 쇼핑 검색 결과 1페이지 캡처 첨부 (별도 파일)
```

차단 발생 시 Task 1로 회귀.

- [ ] **Step 3: PDF → CMYK 변환**

CMYK 변환 (택 1):
- (a) Adobe Acrobat Pro → PDF/X-1a 저장
- (b) iLovePDF / PDF24 무료 도구
- (c) 인쇄소가 sRGB 받아주면 변환 생략

저장: `board-print-ready.pdf`, `stickers-print-ready.pdf`.

- [ ] **Step 4: 운영자 최종 승인**

`operator-approval.md`:

```markdown
# Day 2 운영자 승인

- 일시: 2026-05-XX HH:MM (UTC+09:00)
- 운영자: [본인]
- 자산:
  - board_pdf v1 → board-print-ready.pdf (CMYK 변환 후)
  - sticker_sheet v1 → stickers-print-ready.pdf (CMYK 변환 후)
- 검수 결과:
  - 자가 출력 4개 체크포인트 통과 ✓
  - IP precheck 통과 ✓
- 결정: **approved** — Task 3 인쇄소 견적 진행
```

- [ ] **Step 5: DesignAsset 레코드 업데이트**

design-assets.csv 의 2개 row를 `proof_status=pass`, `operator_approval=approved`, `approved_at` 채움:

```bash
# 간단한 sed 또는 수동 편집. CSV 직접 수정 권장 (LibreOffice/엑셀).
# 또는 Python 1줄:
python -c "
import csv
from datetime import datetime, timezone
p = 'store-os/docs/evidence/store-01/design-assets.csv'
ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
rows = list(csv.DictReader(open(p, encoding='utf-8')))
for r in rows:
    r['proof_status'] = 'pass'
    r['operator_approval'] = 'approved'
    r['approved_at'] = ts
with open(p, 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader()
    w.writerows(rows)
"
```

- [ ] **Step 6: inspection-notes.md 작성**

```markdown
# Day 2 검수·CMYK 변환·승인 종합

- 자가 출력 검수: [통과/수정 후 재출력 N회]
- IP precheck: [통과]
- CMYK 변환 방법: [(a)/(b)/(c)]
- 운영자 승인: approved
- 다음 단계: Day 3 인쇄소 견적
```

- [ ] **Step 7: Commit**

```bash
git add store-os/docs/evidence/store-01/
git commit -m "store-01(day-2): IP precheck + 자가 검수 + 운영자 승인 — DesignAsset proof_status=pass"
```

---

## Task 3: 인쇄소 견적·컬러프루프 (Day 3)

**Files:**
- Create: `store-os/docs/evidence/store-01/day-03-print-quotes/quote-shop-a.txt`
- Create: `store-os/docs/evidence/store-01/day-03-print-quotes/quote-shop-b.txt`
- Create: `store-os/docs/evidence/store-01/day-03-print-quotes/quote-shop-c.txt`
- Create: `store-os/docs/evidence/store-01/day-03-print-quotes/selection-decision.md`

**Prerequisite:** Task 2의 `operator_approval=approved` 통과.

- [ ] **Step 1: 인쇄소 3곳 후보 선정**

성원애드피아·레드프린팅·디비프린팅 등. 조건: A4 매트 코팅지 250–300g + 50건 소량 + 컬러프루프 1장 별도 가능 + 납기 3–5일.

- [ ] **Step 2: 각 인쇄소 견적 요청**

요청 내용 동일 (3곳):
- 보드판: A4, 250g 매트 코팅지, 양면 컬러, 50매
- 스티커 시트: A4 다이컷, 50시트
- 컬러프루프 1장 (보드판) 별도 발주 가능 여부

각 견적을 `quote-shop-X.txt` 형식으로 저장:

```
인쇄소: [상호]
보드판 50건: [가격] 원
스티커 50시트: [가격] 원
컬러프루프 1장: [가격] 원
배송비: [가격] 원
총비용: [가격] 원
납기: [영업일]
연락처: [전화·이메일]
견적일: 2026-05-XX
```

- [ ] **Step 3: 선정 의사결정**

`selection-decision.md`:

```markdown
# Day 3 인쇄소 선정

| 항목 | A | B | C |
|---|---|---|---|
| 총비용 | | | |
| 납기 | | | |
| 컬러프루프 | | | |
| 후기 | | | |

## 선정: [상호]
이유: [핵심 근거 1–2문장]
```

- [ ] **Step 4: 선정 인쇄소에 컬러프루프 1장 발주**

이메일 또는 인쇄소 사이트로 발주. 보드판 1장 5,000–10,000원 예상. 납기 2일.

- [ ] **Step 5: Commit**

```bash
git add store-os/docs/evidence/store-01/day-03-print-quotes/
git commit -m "store-01(day-3): 인쇄소 3곳 견적 + 선정 + 컬러프루프 발주"
```

---

## Task 4: 인쇄소 50건 발주 (Day 4)

**Files:**
- Create: `store-os/docs/evidence/store-01/day-04-print-order/order-confirmation.pdf`
- Create: `store-os/docs/evidence/store-01/day-04-print-order/color-proof-request.md`

**Prerequisite:** Task 3의 컬러프루프 수령.

- [ ] **Step 1: 컬러프루프 도착 → 색감 검수**

자연광 검수. PDF 화면과 비교.
- 색 변색 심각 → 인쇄소에 CMYK 조정 요청 (재생성·재출력 가능성)
- OK → Step 2
- 거절 수준 → Task 3로 회귀 (다른 인쇄소)

`color-proof-request.md`:

```markdown
# Day 4 컬러프루프 검수

- 수령: 2026-05-XX
- 색감 변화: [관찰]
- 결정: [발주 진행 / 색 조정 / 인쇄소 변경]
```

- [ ] **Step 2: 50건 발주**

선정 인쇄소에 발주:
- 보드판 A4 250g 매트 코팅지 50매
- 스티커 A4 다이컷 시트 50매
- 납기 3–5일

발주 confirmation 저장: `order-confirmation.pdf`.

- [ ] **Step 3: 카드 결제 + 영수증 보관**

L0 결정. 결제 후 영수증·세금계산서를 비용 추적용으로 보관.

- [ ] **Step 4: Commit**

```bash
git add store-os/docs/evidence/store-01/day-04-print-order/
git commit -m "store-01(day-4): 인쇄소 50건 발주 완료 — 납기 Day 8"
```

---

## Task 5: 스마트스토어 상품 페이지 (Day 5–6)

**Files:**
- Create: `store-os/docs/evidence/store-01/day-05-06-listing/listing-draft-v1.md`
- Create: `store-os/docs/evidence/store-01/day-05-06-listing/legal-check-output.txt`
- Create: `store-os/docs/evidence/store-01/day-05-06-listing/listing-final.md`
- Create: `store-os/docs/evidence/store-01/day-05-06-listing/listing-screenshots/`

**Prerequisite:** Task 4 발주 완료. Task 5–7은 인쇄 진행 중 병렬.

- [ ] **Step 1: Claude API 키 설정 (1회)**

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

(웹 인터페이스 사용 시 생략 가능.)

- [ ] **Step 2: 상품 설명 초안 자동 생성**

```bash
cd store-os
python scripts/auto_claude.py \
  --product "초등 저학년 칭찬스티커 보드판 + 스티커 세트" \
  --target "초등 1-3학년 자녀를 둔 학부모" \
  --count 1 \
  --save docs/evidence/store-01/day-05-06-listing/
```

생성 파일을 `listing-draft-v1.md`로 rename.

- [ ] **Step 3: 운영자 편집 — 4가지 필수 추가**

`listing-final.md`에 다음 추가:
1. **사업자 정보**: 상호·대표자명·사업자등록번호·통신판매업 신고번호·주소·연락처
2. **가격 구조**: STD 9,900원 / CUSTOM 11,900원 (옵션 +2,000원)
3. **배송 안내**: 결제 후 1–2 영업일 발송, 택배사 [지정], 배송비 [정책]
4. **환불 정책**: "7일 미개봉 반품 가능 / CUSTOM은 자녀 이름 인쇄 후 환불 불가"

- [ ] **Step 4: 법률 자동 점검**

```bash
cd store-os
python scripts/legal_check.py docs/evidence/store-01/day-05-06-listing/listing-final.md \
  > docs/evidence/store-01/day-05-06-listing/legal-check-output.txt 2>&1
```

필수 조치 0건 확인. 1개라도 있으면 Step 3 회귀.

- [ ] **Step 5: 스마트스토어 상품 등록 (unpublished)**

네이버 스마트스토어 셀러센터:
- 카테고리: 문구·오피스 > 학용품 > 칭찬스티커
- 상품명: "초등 저학년 칭찬스티커 보드판 세트 [자녀 이름 무료 인쇄]"
- 가격: 9,900원 (기본) + 옵션 "자녀 이름 커스터마이즈 (+2,000원)"
- 재고: 50개
- 상세페이지: `listing-final.md` 내용
- 사업자 정보 푸터 확인
- 상품 상태: **판매 X (보류)**

- [ ] **Step 6: 상품 사진 5장 업로드 (Day 8 입고 후)**

Day 8에 실 인쇄물로 촬영·교체. Day 5–6 시점에는 v1 자가 출력본 사진 임시 가능.

- [ ] **Step 7: 등록 페이지 스크린샷**

`listing-screenshots/draft-page.png`.

- [ ] **Step 8: Commit**

```bash
git add store-os/docs/evidence/store-01/day-05-06-listing/
git commit -m "store-01(day-5-6): 상품 페이지 작성 + legal_check 통과 + unpublished 등록"
```

---

## Task 6: 마케팅 콘텐츠 시드 (Day 7)

**Files:**
- Create: `store-os/docs/evidence/store-01/day-07-marketing-seed/prompt-blog.md`
- Create: `store-os/docs/evidence/store-01/day-07-marketing-seed/blog-post-01.md`
- Create: `store-os/docs/evidence/store-01/day-07-marketing-seed/instagram-post-01.md`
- Create: `store-os/docs/evidence/store-01/day-07-marketing-seed/legal-check-content.txt`

- [ ] **Step 1: Claude Design + 카피 프롬프트 작성**

`prompt-blog.md` 에 콘텐츠 톤·형식·법률 제약을 명시:

```markdown
[목적] 학부모 공감 정보성 블로그 글 1편 (800–1200자)
[톤] 운영자 개인 경험 톤, 잔소리 안 통한 시행착오 솔직 인정
[제목] "초등 1학년 아이와 약속 지키기 — 우리 집 시행착오"
[구조] 도입(공감) → 시도해본 방법 3가지 → 행동 기반 칭찬으로 전환 → 보드판 자연스레 등장 → 마무리
[회피] "학습 효과 보장", "성적 향상", "100% 효과" 같은 단정. 광고성 어휘.
[결말 링크] 1회만 자연스럽게
```

- [ ] **Step 2: Claude로 블로그 글 작성**

웹 인터페이스 또는 API. 프롬프트 결과를 `blog-post-01.md` 저장.

- [ ] **Step 3: 인스타 포스트 카피 작성**

`instagram-post-01.md`:

```markdown
[제목] 엄마가 직접 만든 칭찬스티커 — 자녀 이름 들어간 보드
[톤] 짧고 따뜻한 1인칭
[형식] 카피 100–200자 + 사진 placeholder (Day 8 입고 후 촬영분 또는 Day 10 베타 자산)
[해시태그] #초등엄마 #칭찬스티커 #자녀이름인쇄 #육아템
[CTA] 프로필 링크 → 스토어
```

- [ ] **Step 4: 법률 자동 점검**

```bash
cd store-os
python scripts/legal_check.py docs/evidence/store-01/day-07-marketing-seed/blog-post-01.md \
  > docs/evidence/store-01/day-07-marketing-seed/legal-check-content.txt 2>&1
python scripts/legal_check.py docs/evidence/store-01/day-07-marketing-seed/instagram-post-01.md \
  >> docs/evidence/store-01/day-07-marketing-seed/legal-check-content.txt 2>&1
```

둘 다 필수 조치 0건 확인.

- [ ] **Step 5: 발행 보류 (Day 11까지)**

작성·검수만. 발행은 Day 11에 베타 자산 통합 후.

- [ ] **Step 6: Commit**

```bash
git add store-os/docs/evidence/store-01/day-07-marketing-seed/
git commit -m "store-01(day-7): 마케팅 콘텐츠 시드 2편 작성 + 법률 통과"
```

---

## Task 7: 입고 자가 품질 검수 (Day 8)

**Files:**
- Create: `store-os/docs/evidence/store-01/day-08-quality-check/unboxing-photos/`
- Create: `store-os/docs/evidence/store-01/day-08-quality-check/usage-test-5min-photos/`
- Create: `store-os/docs/evidence/store-01/day-08-quality-check/inspection-decision.md`

**Prerequisite:** Task 4 발주 인쇄물 입고.

- [ ] **Step 1: 박스 개봉 + 수량·외관 확인**

50건 모두 확인. 외관 손상·이물 점검. 사진:
- `unboxing-photos/box-opened.jpg`
- `unboxing-photos/all-50-spread.jpg`

- [ ] **Step 2: 무작위 1건 운영자 5분 사용 관찰**

운영자(또는 자녀·조카)가 5분간 사용. 사진 4–6장:
- `usage-test-5min-photos/sticker-attach.jpg`
- `usage-test-5min-photos/sticker-reattach.jpg`
- `usage-test-5min-photos/readability.jpg`
- `usage-test-5min-photos/full-board-with-stickers.jpg`

- [ ] **Step 3: 검수 결정**

```markdown
# Day 8 자가 품질 검수

## 입고
- 수량: [N건] ✓ / [부족 N건]
- 외관 손상: [없음 / N건]

## 사용 테스트
- 스티커 접착: [OK / 약함]
- 재부착: [OK / 불가]
- 글자 가독성: [OK / 작음]
- 종이 두께·코팅: [OK / 약함]

## 결정
- [✓ 통과 — Day 9 공개]
- [⚠️ 조건부 — N개 후속 보강]
- [❌ 차단 — 인쇄소 클레임]
```

- [ ] **Step 4: 검수 통과 시 상품 사진 5장 촬영·Task 5 listing 업로드**

스마트스토어에서 사진 교체 (임시 → 실 인쇄물).

- [ ] **Step 5: Commit**

```bash
git add store-os/docs/evidence/store-01/day-08-quality-check/
git commit -m "store-01(day-8): 입고 자가 품질 검수 [통과/조건부/차단]"
```

---

## Task 8: 공개 전환 (Day 9)

**Files:**
- Create: `store-os/docs/evidence/store-01/day-09-public-launch/public-listing-screenshot.png`
- Create: `store-os/docs/evidence/store-01/day-09-public-launch/publish-audit-log.md`

**Prerequisite:** Task 7 통과 + Task 5 사진 교체.

- [ ] **Step 1: 최종 페이지 운영자 점검 (5분)**

고객 입장에서 처음~끝 읽기. 4가지 확인:
1. 가격·옵션 표시 정확
2. 사업자 정보 표시
3. 환불 정책 명확
4. 사진 5장 모두 실 인쇄물

- [ ] **Step 2: unpublished → 판매중 전환**

셀러센터 → 판매 상태 토글.

- [ ] **Step 3: 공개 페이지 스크린샷**

`public-listing-screenshot.png`.

- [ ] **Step 4: audit 로그 작성**

```markdown
# Day 9 공개 전환 audit

- 전환 일시: 2026-05-XX HH:MM (UTC+09:00)
- 운영자: [본인]
- 사전 점검 4개 항목 ✓
- 공개 URL: https://smartstore.naver.com/[shop]/products/[id]
- proof 결정: Final Proof Agent에서 졸업 평가 시점에 결정 (이 task는 builder)
```

- [ ] **Step 5: Commit**

```bash
git add store-os/docs/evidence/store-01/day-09-public-launch/
git commit -m "store-01(day-9): 상품 페이지 공개 전환 — Mini 판매 카운트 시작"
```

---

## Task 9: 베타 발송 + 후기 자산 (Day 10)

**Files:**
- Create: `store-os/docs/evidence/store-01/day-10-beta-delivery/beta-feedback-01.md`
- Create: `store-os/docs/evidence/store-01/day-10-beta-delivery/beta-photos/`
- (Optional) `store-os/docs/evidence/store-01/day-10-beta-delivery/beta-feedback-02.md`

**중요**: 베타 매출은 졸업 카운트 **제외**. 후기·사진은 마케팅 자산.

- [ ] **Step 1: 베타 1–2명 섭외**

지인 학부모 중 초등 1–3학년 자녀. 무료/원가 제공 + 솔직 후기 + 사진 사용 동의.

- [ ] **Step 2: 발송**

운영자 직접 포장·발송 (L0). 송장 번호 분리 기록.

- [ ] **Step 3: D+2~3 후기·사진 수령**

5–10문장 후기 + 사진 2–3장 (자녀 얼굴 모자이크·뒷모습). `beta-feedback-01.md` + `beta-photos/`.

- [ ] **Step 4: 마케팅 사용 동의 명시**

`beta-feedback-01.md` 끝에 "사진·후기 마케팅 사용 동의: ✓ ([날짜])".

- [ ] **Step 5: Commit**

```bash
git add store-os/docs/evidence/store-01/day-10-beta-delivery/
git commit -m "store-01(day-10): 베타 1-2명 발송 + 후기 자산 (졸업 카운트 제외)"
```

---

## Task 10: 마케팅 본격 발행 (Day 11)

**Files:**
- Modify: `day-07-marketing-seed/blog-post-01.md` (베타 자산 통합)
- Modify: `day-07-marketing-seed/instagram-post-01.md` (베타 사진 통합)
- Create: `store-os/docs/evidence/store-01/day-11-marketing-publish/publish-log.md`
- Create: `store-os/docs/evidence/store-01/day-11-marketing-publish/content-published/`

- [ ] **Step 1: 베타 자산을 콘텐츠에 통합**

Task 9 사진·후기를 Task 6 초안에 자연스럽게 삽입. 베타 사용자 익명 또는 동의 명의.

- [ ] **Step 2: legal_check.py 재실행**

```bash
cd store-os
python scripts/legal_check.py docs/evidence/store-01/day-07-marketing-seed/blog-post-01.md
python scripts/legal_check.py docs/evidence/store-01/day-07-marketing-seed/instagram-post-01.md
```

둘 다 필수 조치 0건 확인.

- [ ] **Step 3: 블로그 발행**

네이버 블로그 또는 티스토리. URL 기록.

- [ ] **Step 4: 인스타 발행**

포스트 발행. URL 기록.

- [ ] **Step 5: 맘 카페 정보성 답변 1건**

직접 홍보 ❌. 다른 학부모 질문 답변. 프로필 → 스토어 유도. 카페별 규정 사전 확인.

- [ ] **Step 6: publish-log.md 작성**

```markdown
# Day 11 발행 로그

| 콘텐츠 | 플랫폼 | URL | 발행 시각 |
|---|---|---|---|
| 블로그 #1 | 네이버 블로그 | [URL] | 2026-05-XX HH:MM |
| 인스타 #1 | Instagram | [URL] | 2026-05-XX HH:MM |
| 맘 카페 답변 | [카페] | [URL] | 2026-05-XX HH:MM |

## 첫 24h 모니터링 (Day 12 작성)
- 블로그 방문: [N]
- 인스타 도달: [N]
- 스토어 유입 (출처별): [N]
```

- [ ] **Step 7: Commit**

```bash
git add store-os/docs/evidence/store-01/
git commit -m "store-01(day-11): 마케팅 블로그·인스타·맘 카페 발행"
```

---

## Task 11: 일일 운영 + 모니터링 (Day 12–14)

**Files:**
- Create: `store-os/docs/evidence/store-01/day-12-14-ops/kpi.csv`
- Create: `store-os/docs/evidence/store-01/day-12-14-ops/cs-tickets/`
- Create: `store-os/docs/evidence/store-01/day-12-14-ops/orders-log.md`

**반복** (Day 12·13·14):

- [ ] **Step 1: 오전 체크 (08:00–10:00)**

1. 셀러센터 신규 주문 확인
2. STD → 재고 픽업·송장·포장·발송
3. CUSTOM → 자녀 이름 톡톡 confirmation → 자가 인쇄 → 발송
4. 톡톡 24h SLA

- [ ] **Step 2: 저녁 체크 (19:00–21:00)**

1. 오후 도착분 주문 확인
2. 배송 추적 번호 입력
3. D+3 후기 요청 톡톡 1회
4. 톡톡 24h SLA

- [ ] **Step 3: KPI 1줄 (매일 21:00 이후)**

`kpi.csv`:

```csv
date,orders,sales_kw,reviews_4plus,inquiries,refunds,cancellations,beta_excluded,notes
2026-05-XX,2,19800,0,1,0,0,0,"첫날 — 블로그 유입 1건, 직접검색 1건"
```

- [ ] **Step 4: Auto-pause 트리거 점검**

다음 1개라도 → 즉시 상품 일시정지 + 운영자 알림:
- 환불·교환 1건 → 처리 + 원인 분석 (5건+ 시 일시정지)
- 리뷰 평점 < 3.5 (3건 이상)
- CS 시간당 > 5건
- 법률·분쟁 문의 1건+

발생 시 `cs-tickets/<id>.md`:

```markdown
# CS Ticket [id]
- 발생: 2026-05-XX HH:MM
- 카테고리: [refund / quality / legal / other]
- 처리: 운영자 직접 (L0)
- 결과: [결과 1줄]
```

- [ ] **Step 5: 일일 commit**

```bash
git add store-os/docs/evidence/store-01/day-12-14-ops/
git commit -m "store-01(day-XX): 일일 운영 — 주문 N건, 응답 N건, KPI 갱신"
```

---

## Task 12: Mini 졸업 평가 (Day 14 또는 50건 소진)

**Files:**
- Create: `store-os/docs/evidence/store-01/graduation-evaluation/final-kpi-summary.md`
- Create: `store-os/docs/evidence/store-01/graduation-evaluation/proof-decision.md`

**평가 시점:** Day 14 또는 50건 재고 소진, 먼저 도달.

- [ ] **Step 1: 7개 졸업 조건 점수표**

`kpi.csv` 누적 합계로:

```markdown
# STORE-01 Mini 졸업 평가

| # | 항목 | 목표 | 실측 | 통과 |
|---|---|---|---|---|
| 1 | 실 판매 (베타 제외) | 10건+ | [N] | [✓/✗] |
| 2 | 긍정 리뷰 (4점+) | 3건+ | [N] | [✓/✗] |
| 3 | 재구매/문의 | 1건+ | [N] | [✓/✗] |
| 4 | 순이익 | > 0 | [매출] − [비용] = [N]원 | [✓/✗] |
| 5 | 법률 점검 | 필수 조치 0 | [N] | [✓/✗] |
| 6 | 자가 품질 검수 | 통과 | Day 8 ✓ | ✓ |
| 7 | audit log | 누락 0 | [확인] | [✓/✗] |

## 7개 모두 통과? [YES/NO]
```

- [ ] **Step 2: Final Proof Agent 호출 (별도 subagent)**

메인 세션이 `general-purpose` 또는 `superpowers:code-reviewer` subagent dispatch. 프롬프트:

```
Final Proof Agent — STORE-01 Mini 졸업 결정

다음 증거 검토 → Pass / Conditional Pass / Fail:
- final-kpi-summary.md
- kpi.csv
- 모든 cs-tickets/
- design-assets.csv (proof_status·operator_approval 모두 통과 확인)
- listing-final.md + legal-check-output.txt
- day-08-quality-check/

규칙:
- 7개 모두 통과 → Pass
- 1–2개 미달 + 보완 계획 있음 → Conditional Pass
- 3개 이상 미달 또는 법률·자가검수 실패 → Fail

Evidence Card 형식 + 근거 반환.
```

- [ ] **Step 3: proof-decision.md 저장**

```markdown
# STORE-01 Mini Proof Decision

- Decision: [Pass / Conditional Pass / Fail]
- Date: 2026-05-XX
- Proof Agent: [agent type]
- Evidence reviewed: [파일 목록]
- 근거: [reasoning 1–3 문단]
- Conditions (Conditional Pass): [조건 + 만료일]
- 다음 GOAL:
  - Pass → [STORE-04] Mini → Standard 졸업 GOAL 신규 작성
  - Conditional Pass → 보완 후 재평가
  - Fail → 재고 처리 + 학습 회고 + 다음 슬라이스 결정
```

- [ ] **Step 4: 최종 Commit**

```bash
git add store-os/docs/evidence/store-01/graduation-evaluation/
git commit -m "store-01(graduation): Mini 졸업 평가 — [Pass/Conditional/Fail]"
```

---

## Self-Review

**1. Spec 커버리지** — spec 10개 섹션 모두 task 매핑:
- §1 SKU → T1(Design) + T5(Listing) ✓
- §2 14일 일정 → T1–12 ✓
- §3 마케팅 → T6(시드) + T10(발행) ✓
- §4 운영 → T11 ✓
- §5 검증·졸업 → T12 ✓
- §6 리스크 12 → 각 task의 검수·법률체크·auto-pause로 반영 ✓
- §7 자동화 경계 → 모든 task L0/L1 표시 ✓
- §8 다음 단계 → T12 이후 [STORE-04] ✓

**2. Claude Design 통합 확인**:
- claude-design-automation.md 워크플로 (design brief → 생성 → DesignAsset 레코드 → proof → 승인) Task 1·2에 반영 ✓
- DesignAsset.csv 스키마 일치 ✓
- proof_status·operator_approval 게이트 Task 2에 명시 ✓
- IP precheck Task 2 Step 2 ✓
- 운영자 승인 없이는 인쇄·listing 불가 (Task 2 → Task 3 prerequisite) ✓

**3. Placeholder 점검** — fill-in 템플릿(`[N]`·`[shop]` 등)만, 진짜 TBD 없음 ✓

**4. 타입·시그니처 일관성** — 경로(`day-XX-…/`), DesignAsset 컬럼명, KPI 컬럼명 모두 통일 ✓

Self-review 통과.

---

## Execution Handoff

**Subagent-Driven Development는 부적합** — subagent가 Claude Design·인쇄소·스마트스토어를 직접 조작 불가.

**Recommended: Inline Execution + 운영자 협업**

- 메인 세션이 `superpowers:executing-plans`로 plan을 로드하고 task별 진행
- Claude Design·물리 작업은 운영자가 직접 실행
- 메인 세션은 검증·증거 정리·`legal_check.py` 실행·KPI 기록·DesignAsset.csv 자동 업데이트 보조
- task 완료 시 운영자 보고 → 메인 세션이 evidence 정리 + commit

또는 **운영자 단독 실행** — 보조 없이 plan을 책처럼 따라가며 직접 실행.

---

**상태**: Draft — 사용자 검토 대기
**작성**: 2026-05-22 writing-plans 세션 (Claude Design 도입 반영)
**다음 행동**: plan 승인 → 실행 방식 결정 (Inline 협업 권장)
