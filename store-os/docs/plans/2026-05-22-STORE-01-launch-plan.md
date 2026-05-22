# [STORE-01] 초등 칭찬스티커 보드판 출시 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Mini 단계 졸업 조건(실 판매 10건 + 긍정 리뷰 3건 + 순이익 > 0)을 14일 안에 확보한다.

**Architecture:** 14일을 12개 task로 분할. 각 task는 Day 단위 또는 더 작게. 산출물은 모두 `store-os/docs/evidence/store-01/`에 누적되며 git commit으로 audit log를 형성. AI는 L1 초안만(상품 설명·콘텐츠 카피), L0 작업(법률 승인·인쇄 발주·결제·환불)은 운영자 직접.

**Tech Stack:** Canva (디자인) · 외부 인쇄소 (50건 발주) · 네이버 스마트스토어 (1채널 입점) · `store-os/scripts/` (legal_check·auto_claude·cost_calculator) · `store-os/docs/evidence/store-01/` (증거 누적) · 한국어 운영.

**Spec ref:** [2026-05-22-STORE-01-design.md](../specs/2026-05-22-STORE-01-design.md)
**GOAL ref:** [STORE-01-praise-sticker-board.md](../goals/STORE-01-praise-sticker-board.md)

---

## File Structure (이 plan이 만들어내는 산출물)

```
store-os/docs/evidence/store-01/
├── README.md                          # 증거 누적 인덱스
├── day-01-design-v1/
│   ├── board-a4.canva-export.pdf
│   ├── stickers-30-set.canva-export.pdf
│   └── design-notes.md
├── day-02-self-print-check/
│   ├── self-print-photo-board.jpg
│   ├── self-print-photo-stickers.jpg
│   ├── board-print-ready.pdf            # CMYK 변환본
│   ├── stickers-print-ready.pdf
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
│   ├── listing-draft-v1.md              # auto_claude.py 출력
│   ├── legal-check-output.txt           # legal_check.py 출력
│   ├── listing-final.md                 # 운영자 편집 후 등록 본
│   └── listing-screenshots/
├── day-07-marketing-seed/
│   ├── blog-post-01.md
│   └── instagram-post-01.md
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
│   ├── kpi.xlsx                          # 일 단위 KPI + 운영 로그
│   ├── cs-tickets/
│   └── orders-log.md
└── graduation-evaluation/
    ├── final-kpi-summary.md
    └── proof-decision.md                 # Final Proof Agent 결정 기록
```

---

## Critical Path

```
Task 1 (Day 1)  ──→ Task 2 (Day 2)  ──→ Task 3 (Day 3)  ──→ Task 4 (Day 4)
디자인 v1            자가 출력 검수      인쇄소 견적·프루프    50건 발주
                                                                ↓ 납기 3–5일
Task 5 (Day 5–6)   Task 6 (Day 7)         Task 7 (Day 8)  ←─────┘
상품 페이지         마케팅 시드            입고 자가 검수
                                                ↓
Task 8 (Day 9)   ──→ Task 9 (Day 10) ──→ Task 10 (Day 11)
공개 전환            베타 발송               마케팅 본격
                                                ↓
                                          Task 11 (Day 12–14)
                                          일일 운영
                                                ↓
                                          Task 12
                                          졸업 평가
```

Task 1–4가 critical path. Task 5–6은 인쇄 진행 중 병렬 가능.

---

## Task 1: Canva 보드판·스티커 v1 디자인 (Day 1)

**Files:**
- Create: `store-os/docs/evidence/store-01/day-01-design-v1/board-a4.canva-export.pdf`
- Create: `store-os/docs/evidence/store-01/day-01-design-v1/stickers-30-set.canva-export.pdf`
- Create: `store-os/docs/evidence/store-01/day-01-design-v1/design-notes.md`

- [ ] **Step 1: Canva 새 프로젝트 생성 — 보드판 A4 (210×297mm)**

Canva → "맞춤 크기" → 210mm × 297mm → 새 프로젝트.

- [ ] **Step 2: 보드판 레이아웃 작성**

스펙: 5열 × 6행 = 30칸. 각 칸 30×30mm. 칸 사이 간격 2–3mm.
상단: "이름: __________" 영역 (CUSTOM SKU에서 이 영역에 자녀 이름 인쇄, STD는 공란).
하단: "이번 달 목표: __________" 칸 (보호자 수기 작성용 공란).
색감: 파스텔 1–2색 포인트만. 배경은 흰색.

- [ ] **Step 3: 스티커 시트 새 프로젝트 — A4**

210×297mm. 6열 × 5행 = 30매. 각 30×30mm 정사각.

- [ ] **Step 4: 스티커 메시지 30매 입력**

- 행동 기반 10매: "스스로 정리했어요", "약속 지켰어요", "양보했어요", "도와줬어요", "참았어요", "감사 표현했어요", "스스로 일어났어요", "숙제 끝냈어요", "정리정돈했어요", "차분히 기다렸어요"
- 일반 칭찬 10매: "잘했어요", "최고예요", "고마워요", "사랑해요", "자랑스러워요", "멋져요", "굿!", "OK!", "Yay!", "★"
- 자유 10매: 이모지·도형 (예: 🌟⭐❤️🎉👍😊🏆🌈🎈🍀) — 부모가 의미 부여

법률 점검: "성적 향상", "100% 효과", "공부 잘함" 같은 단정 표현 금지. 위 30매에는 없음 ✓.

- [ ] **Step 5: 두 디자인 모두 PDF로 export**

Canva → 공유 → 다운로드 → PDF (인쇄용) → 저장:
- `board-a4.canva-export.pdf`
- `stickers-30-set.canva-export.pdf`

- [ ] **Step 6: design-notes.md 작성**

```markdown
# Day 1 디자인 v1 노트

- 보드판: A4, 30칸(5×6), 30×30mm 칸. 자녀 이름 영역(상단) + 월 목표 영역(하단).
- 스티커: A4 시트, 30매(6×5), 30×30mm 정사각.
- 색감: 파스텔 [실제 사용한 색 코드 #XXXXXX].
- 금지어 점검: 단정·과대광고 표현 없음 ✓
- 다음 단계: Day 2 자가 출력 검수.
```

- [ ] **Step 7: Commit**

```bash
git add store-os/docs/evidence/store-01/day-01-design-v1/
git commit -m "store-01(day-1): Canva 보드판·스티커 v1 디자인 완료"
```

---

## Task 2: 자가 출력 검수 + PDF/CMYK 변환 (Day 2)

**Files:**
- Create: `store-os/docs/evidence/store-01/day-02-self-print-check/self-print-photo-board.jpg`
- Create: `store-os/docs/evidence/store-01/day-02-self-print-check/self-print-photo-stickers.jpg`
- Create: `store-os/docs/evidence/store-01/day-02-self-print-check/board-print-ready.pdf`
- Create: `store-os/docs/evidence/store-01/day-02-self-print-check/stickers-print-ready.pdf`
- Create: `store-os/docs/evidence/store-01/day-02-self-print-check/inspection-notes.md`

- [ ] **Step 1: 가정 프린터로 v1 PDF 출력 1장씩**

`day-01-design-v1/`의 두 PDF를 A4 용지에 출력. (가능하면 두꺼운 250g 용지가 있다면 사용, 없으면 일반 A4)

- [ ] **Step 2: 출력물 사진 촬영**

자연광에서 보드판 1장, 스티커 1장 촬영. 색감·여백·텍스트 가독성 확인용.
- `self-print-photo-board.jpg` 저장
- `self-print-photo-stickers.jpg` 저장

- [ ] **Step 3: 검수 — 4개 체크포인트**

다음 4가지를 육안 점검:
1. 글자 크기·가독성 OK?
2. 칸 격자 비뚤어지지 않음?
3. 색감 화면 대비 변색 심각?
4. 여백·marginal 균형 OK?

문제 있으면 Canva로 돌아가서 v2 수정 후 재출력. 통과까지 반복.

- [ ] **Step 4: PDF → CMYK 변환**

인쇄소 제출용 CMYK 변환. Canva 직접 export는 sRGB. 변환 방법 (택 1):
- (a) Adobe Acrobat Pro 사용: 파일 → 인쇄 작업 → PDF/X-1a 저장
- (b) 무료: Canva PDF를 [iLovePDF CMYK 변환](https://www.ilovepdf.com/) 또는 [PDF24](https://tools.pdf24.org/)에 업로드
- (c) 인쇄소가 sRGB 받아주면 변환 생략 가능 (Task 3에서 확인)

저장:
- `board-print-ready.pdf`
- `stickers-print-ready.pdf`

- [ ] **Step 5: inspection-notes.md 작성**

```markdown
# Day 2 자가 출력 검수 + CMYK 변환

## 검수 결과
- [✓ or 수정사항] 글자 가독성
- [✓ or 수정사항] 칸 격자 정렬
- [✓ or 수정사항] 색감
- [✓ or 수정사항] 여백·균형

## CMYK 변환
- 방법: [(a) Adobe / (b) iLovePDF / (c) 생략]
- 변환 후 색감 변화: [관찰]
- 인쇄소 제출 준비 완료 ✓
```

- [ ] **Step 6: Commit**

```bash
git add store-os/docs/evidence/store-01/day-02-self-print-check/
git commit -m "store-01(day-2): 자가 출력 검수 + CMYK 변환 완료"
```

---

## Task 3: 인쇄소 견적·컬러프루프 (Day 3)

**Files:**
- Create: `store-os/docs/evidence/store-01/day-03-print-quotes/quote-shop-a.txt`
- Create: `store-os/docs/evidence/store-01/day-03-print-quotes/quote-shop-b.txt`
- Create: `store-os/docs/evidence/store-01/day-03-print-quotes/quote-shop-c.txt`
- Create: `store-os/docs/evidence/store-01/day-03-print-quotes/selection-decision.md`

- [ ] **Step 1: 인쇄소 3곳 후보 선정**

추천: 성원애드피아·레드프린팅·디비프린팅 등. 조건:
- A4 매트 코팅지 250–300g 인쇄 가능
- 50건 소량 인쇄 가능
- 컬러프루프 (1장) 별도 요청 가능
- 납기 3–5일

- [ ] **Step 2: 각 인쇄소 견적 요청**

요청 내용 (3곳 동일):
- 보드판: A4, 250g 매트 코팅지, 양면 컬러, 50매
- 스티커 시트: A4 다이컷(또는 키스컷), 50시트
- 컬러프루프 1장 (보드판) 우선 발송 → 색감 확인 후 50건 발주

견적서·납기·총비용을 메모 또는 PDF로 받아 저장:
- `quote-shop-a.txt`
- `quote-shop-b.txt`
- `quote-shop-c.txt`

각 파일 형식:
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

기준: 총비용 + 납기 + 컬러프루프 지원 여부 + 후기·신뢰도. `selection-decision.md` 작성:

```markdown
# Day 3 인쇄소 선정

| 항목 | A | B | C |
|---|---|---|---|
| 총비용 | | | |
| 납기 | | | |
| 컬러프루프 | | | |
| 후기 |  | | |

## 선정: [상호]
이유: [핵심 근거 1–2문장]
```

- [ ] **Step 4: 선정 인쇄소에 컬러프루프 1장 발주**

이메일 또는 인쇄소 사이트에서 발주. 보드판 1장만. 비용 5,000–10,000원 예상. 납기 2일.

- [ ] **Step 5: Commit**

```bash
git add store-os/docs/evidence/store-01/day-03-print-quotes/
git commit -m "store-01(day-3): 인쇄소 3곳 견적 + 선정 + 컬러프루프 발주"
```

---

## Task 4: 인쇄소 50건 발주 (Day 4)

**Files:**
- Create: `store-os/docs/evidence/store-01/day-04-print-order/order-confirmation.pdf` (인쇄소가 발급)
- Create: `store-os/docs/evidence/store-01/day-04-print-order/color-proof-request.md`

**Prerequisite:** Task 3의 컬러프루프 수령 후에만 진행.

- [ ] **Step 1: 컬러프루프 도착 → 색감 검수**

배송 받은 컬러프루프 1장 자연광 검수. PDF 화면과 비교.
- 색 변색 심각? → 인쇄소에 색감 조정 요청 (CMYK 값 수정 필요할 수 있음)
- OK → Step 2 진행
- 거절 수준 → 다른 인쇄소로 재시도 (Task 3로 회귀)

검수 결과를 `color-proof-request.md`에 기록:
```markdown
# Day 4 컬러프루프 검수

- 수령 일자: 2026-05-XX
- 색감 변화: [관찰]
- 결정: [발주 진행 / 색 조정 요청 / 인쇄소 변경]
```

- [ ] **Step 2: 50건 발주**

선정된 인쇄소에 발주:
- 보드판 A4 250g 매트 코팅지 50매
- 스티커 A4 다이컷 시트 50매
- 납기 3–5일

발주 confirmation PDF/이메일 저장:
- `order-confirmation.pdf`

- [ ] **Step 3: 카드 결제 + 영수증 확보**

L0 결정 (운영자 직접). 결제 후 영수증·세금계산서를 비용 추적용으로 보관.

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
- Create: `store-os/docs/evidence/store-01/day-05-06-listing/listing-screenshots/` (등록 페이지 캡처)

**Prerequisite:** Task 4 발주 완료 후. 인쇄 진행 중 병렬.

- [ ] **Step 1: Claude API 키 설정 (1회)**

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

(미사용 가능하면 Claude 웹 인터페이스로 대체. 본 plan은 CLI 흐름 가정.)

- [ ] **Step 2: 상품 설명 초안 자동 생성**

```bash
cd store-os
python scripts/auto_claude.py \
  --product "초등 저학년 칭찬스티커 보드판 + 스티커 세트" \
  --target "초등 1-3학년 자녀를 둔 학부모" \
  --count 1 \
  --save docs/evidence/store-01/day-05-06-listing/
```

생성된 파일을 `listing-draft-v1.md`로 rename.

- [ ] **Step 3: 운영자 편집 — 4가지 필수 추가**

`listing-draft-v1.md` 열어 다음을 확인·추가하여 `listing-final.md` 작성:

1. **사업자 정보**: 상호·대표자명·사업자등록번호·통신판매업 신고번호·주소·연락처
2. **가격 구조**: STD 9,900원 / CUSTOM 11,900원 (옵션 +2,000원)
3. **배송 안내**: 결제 후 1–2 영업일 발송, 택배사 [지정], 배송비 [정책]
4. **환불 정책**: "7일 미개봉 반품 가능 / CUSTOM은 자녀 이름 인쇄 후 환불 불가" 명시

- [ ] **Step 4: 법률 자동 점검**

```bash
cd store-os
python scripts/legal_check.py docs/evidence/store-01/day-05-06-listing/listing-final.md \
  > docs/evidence/store-01/day-05-06-listing/legal-check-output.txt 2>&1
```

출력 확인. **필수 조치 사항이 1개라도 있으면 Step 3로 회귀 후 수정.**
필수 조치 0건 시에만 다음 단계 진행.

- [ ] **Step 5: 스마트스토어 상품 등록 (unpublished 상태)**

네이버 스마트스토어 셀러센터 → 상품 등록:
- 카테고리: 문구·오피스 > 학용품 > 칭찬스티커
- 상품명: "초등 저학년 칭찬스티커 보드판 세트 [자녀 이름 무료 인쇄]"
- 가격: 9,900원 (기본) + 옵션 "자녀 이름 커스터마이즈 (+2,000원)"
- 재고: 50개 (Task 4 발주분)
- 상세페이지: `listing-final.md` 내용을 HTML/리치 에디터로 입력
- 사업자 정보 푸터 자동 포함되어 있는지 확인
- 상품 상태: **판매중 X (보류)** ← 중요

- [ ] **Step 6: 상품 사진 5장 업로드 (Day 8 입고 후로 미루기)**

Day 8에 입고된 실제 인쇄물로 촬영. Day 5–6 시점에는 v1 자가 출력본 사진 임시 사용 가능, 단 Day 8에 교체 필수.

- [ ] **Step 7: 등록 페이지 스크린샷 저장**

상품 등록 페이지 캡처 → `listing-screenshots/draft-page.png`.

- [ ] **Step 8: Commit**

```bash
git add store-os/docs/evidence/store-01/day-05-06-listing/
git commit -m "store-01(day-5-6): 상품 페이지 작성 + legal_check 통과 + unpublished 등록"
```

---

## Task 6: 마케팅 콘텐츠 시드 (Day 7)

**Files:**
- Create: `store-os/docs/evidence/store-01/day-07-marketing-seed/blog-post-01.md`
- Create: `store-os/docs/evidence/store-01/day-07-marketing-seed/instagram-post-01.md`

- [ ] **Step 1: 블로그 글 #1 작성**

제목: "초등 1학년 아이와 약속 지키기 — 우리 집 시행착오"
형식: 800–1,200자 정보성 글. 운영자 개인 경험 톤. 끝에 보드판 자연스럽게 등장.

`blog-post-01.md` 저장.

- [ ] **Step 2: legal_check.py 통과 확인**

```bash
cd store-os
python scripts/legal_check.py docs/evidence/store-01/day-07-marketing-seed/blog-post-01.md
```

필수 조치 0건일 때만 발행 준비. 1개라도 있으면 수정 후 재검사.

- [ ] **Step 3: 인스타 포스트 #1 작성**

제목: "엄마가 직접 만든 칭찬스티커 — 자녀 이름 들어간 보드"
형식: 인스타용 짧은 카피 + 사진 1–3장 계획. 사진은 Day 8 입고 후 촬영.

`instagram-post-01.md` 저장 (사진 placeholder 명시).

- [ ] **Step 4: 발행 보류 (Day 11까지)**

콘텐츠 본격 발행은 Day 11. Day 7은 작성·검수만. 발행 일정 표기.

- [ ] **Step 5: Commit**

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

**Prerequisite:** Task 4 발주의 인쇄물 입고.

- [ ] **Step 1: 박스 개봉 + 수량·외관 확인**

50건 모두 있는지 확인. 외관 손상·이물 점검. 사진 촬영:
- `unboxing-photos/box-opened.jpg`
- `unboxing-photos/all-50-spread.jpg`

- [ ] **Step 2: 무작위 1건 운영자 본인 사용 5분간 관찰**

운영자가 (또는 운영자의 자녀/조카) 보드판 + 스티커 1세트를 실제로 5분간 사용:
- 칸에 스티커 붙이기 → 잘 붙는가?
- 떼었다 다시 붙이기 가능한가?
- 글자 가독성 어린이 눈높이에서 OK?

사진 4–6장 촬영:
- `usage-test-5min-photos/sticker-attach.jpg`
- `usage-test-5min-photos/sticker-reattach.jpg`
- `usage-test-5min-photos/readability.jpg`
- `usage-test-5min-photos/full-board-with-stickers.jpg`

- [ ] **Step 3: 검수 결정 작성**

```markdown
# Day 8 자가 품질 검수 결정

## 입고
- 수량: 50건 ✓ / [부족 N건]
- 외관 손상: [없음 / N건]

## 사용 테스트
- 스티커 접착: [OK / 약함]
- 재부착: [OK / 불가]
- 글자 가독성: [OK / 작음]
- 종이 두께·코팅: [OK / 약함]

## 결정
- [✓ 통과 — Day 9 공개 전환 진행]
- [⚠️ 조건부 통과 — N개 사항 후속 보강]
- [❌ 차단 — 인쇄소에 클레임]
```

- [ ] **Step 4: 검수 통과 시 상품 사진 5장 촬영 + Task 5 listing에 업로드**

스마트스토어 상품 페이지에서 사진 교체. 임시 사진 → 실제 입고 인쇄물 사진.

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

**Prerequisite:** Task 7 검수 통과 + Task 5 사진 교체 완료.

- [ ] **Step 1: 최종 페이지 운영자 점검 (5분)**

스마트스토어 상품 페이지를 운영자가 고객 입장에서 한 번 더 처음부터 끝까지 읽기. 4가지 확인:
1. 가격·옵션 표시 정확?
2. 사업자 정보 표시?
3. 환불 정책 명확?
4. 사진 5장 모두 실 인쇄물?

문제 있으면 즉시 수정.

- [ ] **Step 2: unpublished → 판매중 전환**

셀러센터 → 상품 → 판매 상태 "판매중" 토글.

- [ ] **Step 3: 공개 페이지 스크린샷**

브라우저에서 일반 고객 시점으로 상품 페이지 캡처:
- `public-listing-screenshot.png`

- [ ] **Step 4: audit 로그 작성**

```markdown
# Day 9 공개 전환 audit

- 전환 일시: 2026-05-XX HH:MM (UTC+09:00)
- 운영자: [본인]
- 사전 점검 4개 항목 모두 ✓
- 공개 페이지 URL: https://smartstore.naver.com/[shop]/products/[id]
- proof 결정: builder가 자가 Pass 금지 — 별도 Final Proof Agent의 졸업 평가에서 결정
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

**중요:** 베타 1–2명 매출은 졸업 카운트 **제외**. 단, 후기·사진 자산은 마케팅 콘텐츠로 사용 가능.

- [ ] **Step 1: 베타 대상자 1–2명 섭외**

지인 학부모 중 초등 1–3학년 자녀를 둔 1–2명. 무료 또는 원가($제공 + 솔직 후기 + 사진 사용 동의 조건.

- [ ] **Step 2: 발송**

운영자 직접 포장·발송 (L0). 송장 번호 별도 기록 (스토어 통계와 분리 — 졸업 카운트 제외 표시).

- [ ] **Step 3: D+2~3 후기·사진 수령**

베타 사용자에게 톡톡·메시지로 부탁:
- 5–10문장 후기
- 자녀 사용 사진 2–3장 (자녀 얼굴 노출 동의 필요 — 모자이크 또는 뒷모습)

`beta-feedback-01.md`에 후기 텍스트 + `beta-photos/`에 사진 저장.

- [ ] **Step 4: 동의서 확인**

베타 사용자가 마케팅 자료(블로그·인스타)에 후기·사진 사용해도 OK라는 명시적 동의를 받아 기록:
- `beta-feedback-01.md` 끝에 "사진·후기 마케팅 사용 동의: ✓ ([날짜])" 추가.

- [ ] **Step 5: Commit**

```bash
git add store-os/docs/evidence/store-01/day-10-beta-delivery/
git commit -m "store-01(day-10): 베타 1-2명 발송 + 후기 자산 확보 (졸업 카운트 제외)"
```

---

## Task 10: 마케팅 본격 발행 (Day 11)

**Files:**
- Modify: `store-os/docs/evidence/store-01/day-07-marketing-seed/blog-post-01.md` (베타 사진 포함)
- Modify: `store-os/docs/evidence/store-01/day-07-marketing-seed/instagram-post-01.md` (베타 사진 포함)
- Create: `store-os/docs/evidence/store-01/day-11-marketing-publish/publish-log.md`
- Create: `store-os/docs/evidence/store-01/day-11-marketing-publish/content-published/` (발행 후 URL 캡처)

- [ ] **Step 1: 베타 자산을 콘텐츠에 통합**

Task 9의 사진·후기를 Task 6 블로그·인스타 초안에 자연스럽게 삽입. 베타 사용자 익명 처리 또는 동의 받은 명의.

- [ ] **Step 2: legal_check.py 재실행 (수정 후)**

```bash
cd store-os
python scripts/legal_check.py docs/evidence/store-01/day-07-marketing-seed/blog-post-01.md
python scripts/legal_check.py docs/evidence/store-01/day-07-marketing-seed/instagram-post-01.md
```

둘 다 필수 조치 0건 확인. 1개라도 있으면 수정 후 재검사.

- [ ] **Step 3: 블로그 발행**

네이버 블로그 또는 티스토리에 글 발행. URL 기록.

- [ ] **Step 4: 인스타 발행**

인스타 포스트 발행. URL 기록.

- [ ] **Step 5: 맘 카페 정보성 답변 1건**

직접 홍보 ❌. 다른 학부모 질문에 답변하면서 자연스럽게 운영자 프로필(스토어 링크)로 유도. 카페별 규정 사전 확인.

- [ ] **Step 6: publish-log.md 작성**

```markdown
# Day 11 마케팅 발행 로그

| 콘텐츠 | 플랫폼 | URL | 발행 시각 |
|---|---|---|---|
| 블로그 #1 | 네이버 블로그 | [URL] | 2026-05-XX HH:MM |
| 인스타 #1 | Instagram | [URL] | 2026-05-XX HH:MM |
| 맘 카페 답변 | [카페명] | [URL] | 2026-05-XX HH:MM |

## 첫 24시간 모니터링 (Day 12 작성)
- 블로그 방문: [숫자]
- 인스타 도달: [숫자]
- 스토어 유입 (출처별): [숫자]
```

- [ ] **Step 7: Commit**

```bash
git add store-os/docs/evidence/store-01/
git commit -m "store-01(day-11): 마케팅 블로그·인스타·맘 카페 발행"
```

---

## Task 11: 일일 운영 + 모니터링 (Day 12–14)

**Files:**
- Create: `store-os/docs/evidence/store-01/day-12-14-ops/kpi.xlsx` (또는 .csv)
- Create: `store-os/docs/evidence/store-01/day-12-14-ops/cs-tickets/`
- Create: `store-os/docs/evidence/store-01/day-12-14-ops/orders-log.md`

**반복 일일 체크리스트** (Day 12, Day 13, Day 14 각각):

- [ ] **Step 1: 오전 체크 (08:00–10:00)**

1. 스마트스토어 셀러센터 → 신규 주문 확인
2. STD 주문 → 재고 픽업 → 송장 출력 → 포장 → 발송
3. CUSTOM 주문 → 자녀 이름 톡톡 confirmation → 자가 인쇄 → 포장 → 발송
4. 톡톡 메시지 확인 → 24h SLA 내 응답

- [ ] **Step 2: 저녁 체크 (19:00–21:00)**

1. 신규 주문 확인 (오후 도착분)
2. 발송 완료 건 배송 추적 번호 입력
3. D+3 도래 주문에 톡톡 후기 요청 1회
4. 톡톡 메시지 확인 → 24h SLA

- [ ] **Step 3: KPI 1줄 기록 (매일 21:00 이후)**

`kpi.xlsx` 또는 `kpi.csv` 에 한 줄:

```csv
date,orders,sales_kw,reviews_4plus,inquiries,refunds,cancellations,beta_excluded,notes
2026-05-XX,2,19800,0,1,0,0,0,"첫날 — 블로그 유입 1건, 직접검색 1건"
```

- [ ] **Step 4: Auto-pause 트리거 점검**

다음 1개라도 발생 시 즉시 상품 일시정지 + 운영자 알림:
- 환불·교환 1건 → 일단 처리 + 원인 분석 (5건+ 시 일시정지)
- 리뷰 평점 < 3.5 (3건 이상)
- CS 시간당 > 5건
- 법률·분쟁 문의 1건+

발생 시 `cs-tickets/<ticket-id>.md` 생성:
```markdown
# CS Ticket [id]
- 발생: 2026-05-XX HH:MM
- 카테고리: [refund / quality / legal / other]
- 처리: [운영자 직접 응대 — L0]
- 결과: [결과 1줄]
```

- [ ] **Step 5: 일일 commit (밤)**

```bash
git add store-os/docs/evidence/store-01/day-12-14-ops/
git commit -m "store-01(day-XX): 일일 운영 — 주문 N건, 응답 N건, KPI 갱신"
```

---

## Task 12: Mini 졸업 평가 (Day 14 또는 50건 소진)

**Files:**
- Create: `store-os/docs/evidence/store-01/graduation-evaluation/final-kpi-summary.md`
- Create: `store-os/docs/evidence/store-01/graduation-evaluation/proof-decision.md`

**평가 시점:** Day 14 도래 또는 50건 재고 소진, 둘 중 먼저 도달한 시점.

- [ ] **Step 1: 7개 졸업 조건 자동 점수표 작성**

`kpi.xlsx`의 누적 합계로 다음 표를 `final-kpi-summary.md`에 채움:

```markdown
# STORE-01 Mini 졸업 평가

| # | 항목 | 목표 | 실측 | 통과 |
|---|---|---|---|---|
| 1 | 실 판매 (지인 베타 제외) | 10건+ | [N] | [✓/✗] |
| 2 | 긍정 리뷰 (4점+) | 3건+ | [N] | [✓/✗] |
| 3 | 재구매 또는 문의 | 1건+ | [N] | [✓/✗] |
| 4 | 순이익 | > 0 | [매출] − [비용] = [N]원 | [✓/✗] |
| 5 | 법률 점검 | 필수 조치 0 | [N] | [✓/✗] |
| 6 | 자가 품질 검수 | 통과 | Day 8 통과 ✓ | ✓ |
| 7 | audit log | 누락 0 | [확인] | [✓/✗] |

## 7개 모두 통과? [YES / NO]
```

- [ ] **Step 2: Final Proof Agent 호출 (별도 subagent)**

이 plan을 실행 중이라면 메인 세션이 `general-purpose` 또는 `superpowers:code-reviewer` subagent를 별도 dispatch. Subagent 프롬프트:

```
Final Proof Agent — STORE-01 Mini 졸업 결정

다음 증거를 검토하여 Pass / Conditional Pass / Fail 결정:
- final-kpi-summary.md (7개 조건 점수표)
- kpi.xlsx (일별 데이터)
- 모든 cs-tickets/
- listing-final.md + legal-check-output.txt
- day-08-quality-check/ (자가 검수)

규칙:
- 7개 모두 통과 → Pass
- 1–2개 미달 + 보완 계획 있음 → Conditional Pass (보완 항목·만료일 명시)
- 3개 이상 미달 또는 법률·자가검수 실패 → Fail

Evidence Card 형식으로 결정 + 근거 반환. proof-decision.md에 저장 가능한 형식.
```

- [ ] **Step 3: proof-decision.md 저장**

Final Proof Agent의 출력을 `proof-decision.md`로 저장. 형식:

```markdown
# STORE-01 Mini Proof Decision

- Decision: [Pass / Conditional Pass / Fail]
- Date: 2026-05-XX
- Proof Agent: [agent type]
- Evidence reviewed: [파일 목록]
- 근거:
  [Final Proof Agent의 reasoning 1–3 문단]
- Conditions (Conditional Pass인 경우만):
  - [조건 1 + 만료일]
  - [조건 2 + 만료일]
- 다음 GOAL:
  - Pass → [STORE-04] Mini → Standard 졸업 GOAL 신규 작성
  - Conditional Pass → 보완 후 재평가 (만료일 도달 시)
  - Fail → 재고 처리 + 학습 회고 + 다음 슬라이스 결정
```

- [ ] **Step 4: 최종 Commit**

```bash
git add store-os/docs/evidence/store-01/graduation-evaluation/
git commit -m "store-01(graduation): Mini 졸업 평가 — [Pass/Conditional/Fail]"
```

---

## Self-Review

이 plan을 spec과 대조하여 점검:

**1. Spec 커버리지 — spec 10개 섹션 모두 task로 매핑되었는가?**
- §1 SKU 구조 → Task 1 (디자인) + Task 5 (옵션 등록) ✓
- §2 14일 일정 → Task 1–12 매핑 ✓
- §3 마케팅 콘텐츠 → Task 6 (시드) + Task 10 (발행) ✓
- §4 운영 워크플로 → Task 11 (일일 운영) ✓
- §5 검증·졸업 → Task 12 (평가) ✓
- §6 리스크 12가지 → 각 task의 검수·법률체크·자동 일시정지로 반영 ✓
- §7 자동화 경계 → 모든 task의 L0·L1 표시 ✓
- §8 다음 단계 → Task 12 이후 [STORE-04] 진입 명시 ✓

**2. Placeholder 점검** — "TBD", "TODO" 없음. 모든 step에 실 명령·실 코드 (Canva 메뉴, bash 명령, 산출물 경로) ✓

**3. 타입·시그니처 일관성** — 모든 task에서 `store-os/docs/evidence/store-01/day-XX-…/` 경로 통일 ✓. KPI 컬럼명 일관 (`orders, sales_kw, reviews_4plus, ...`) ✓.

**4. 누락 — `kpi.xlsx` 스키마 명시** (Step 11-3 CSV 형식으로 표현). audit log 형식 (`day-09 audit log`) 명시. CS 티켓 형식 명시. ✓

Self-review 통과.

---

## Execution Handoff

이 plan은 **운영자 직접 실행이 본질**입니다. 코드 task가 거의 없고 (`auto_claude.py`·`legal_check.py` 호출만), 대부분이 Canva·인쇄소·스마트스토어·물리 검수·마케팅 발행 작업입니다. 따라서:

**Subagent-Driven Development는 부적합** — subagent가 Canva·인쇄소·스마트스토어를 조작할 수 없음.

**대신 권장 실행 방식**:

### Inline Execution + 운영자 협업 (Recommended)

- 메인 세션이 `superpowers:executing-plans`로 plan을 로드하고 task별 진행
- 각 task는 운영자가 **직접 실행** (Canva 작업, 발주, 사진 촬영)
- 메인 세션은 검증·증거 점검·다음 task 안내·`legal_check.py` 실행 등 보조
- task 완료 시 운영자가 결과 보고 → 메인 세션이 evidence 정리 + commit
- 매일 끝에 메인 세션이 KPI 1줄 기록 도움

### 또는 운영자 단독 실행

- 운영자가 이 plan을 책처럼 따라가며 직접 실행
- 보조 없음. 가장 자율적이지만 가장 느림

---

**상태**: Draft — 사용자 검토 대기
**작성**: 2026-05-22 writing-plans 세션
**다음 행동**: 사용자 plan 승인 → 실행 방식 결정 (Inline + 협업 권장)
