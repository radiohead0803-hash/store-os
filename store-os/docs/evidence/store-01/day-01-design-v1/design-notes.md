# Day 1 Claude Design 자산 v1 노트

**날짜**: 2026-05-22
**Task**: plan.md Task 1 (Claude Design 자산 생성)
**브랜치**: `feature/store-01-day-01-design`

## 자산 생성 요약

### 보드판 (board-v1.svg)

- **사이즈**: A4 210×297mm
- **레이아웃**: 5열 × 6행 = 30칸 그리드, 각 30×30mm, 칸 간 2mm
- **영역**:
  - 상단: 제목 "칭찬 스티커 보드" + 이름 영역 ("이름: ___")
  - 중앙: 30칸 그리드 (좌상단에 1–30 칸 번호)
  - 하단: "이번 달 목표" 영역 (수기 2줄)
- **색감**: 민트 #A8DADC (메인), 소프트 핑크 #FFD6E0 (보조), 다크 슬레이트 #264653 (텍스트)
- **폰트**: Pretendard·SD 산돌고딕 라이트 fallback
- **이터레이션**: v1 1회 (수정 없음)

### 스티커 시트 (stickers-v1.svg)

- **사이즈**: A4 210×297mm, 30매 (6열 × 5행), 각 30×30mm, 칸 간 2mm
- **메시지 분포**:
  - 행동 기반 10매 (민트 배경): 스스로 정리·약속 지켰·양보·도와줬·참았·감사 표현·스스로 일어났·숙제 끝냈·정리정돈·차분히 기다렸
  - 일반 칭찬 10매 (핑크 배경): 잘했어요·최고예요·고마워요·사랑해요·자랑스러워요·멋져요·굿!·OK!·Yay!·★
  - 자유 10매 (노랑 #FFF3B0 배경): 🌟⭐❤️🎉👍😊🏆🌈🎈🍀
- **다이컷·키스컷 가이드**: v1에는 미포함. vendor 템플릿이 결정되면 v2에 추가.
- **이터레이션**: v1 1회

## DesignAsset 레코드

`design-assets.csv` 에 2건 등록:

| product_id | type | version | proof_status | operator_approval |
|---|---|---|---|---|
| STORE-01-STD | board_pdf | v1 | **pending** | **pending** |
| STORE-01-STD | sticker_sheet | v1 | **pending** | **pending** |

> 본 환경 출력 형식은 SVG. plan에는 `*.pdf`로 명시되어 있으나 Claude는 PDF 바이너리 직접 생성 불가. Day 2 (Task 2 Step 3 CMYK 변환 단계)에서 운영자가 SVG → PDF/CMYK 변환 (Inkscape 또는 온라인 도구).

## 법률·IP 사전 점검 (자가)

- ✅ 캐릭터·연예인·로고·디즈니·산리오 0
- ✅ 일러스트 없음 (모두 텍스트 + 도형 + Unicode 표준 이모지)
- ✅ 폰트: Pretendard (Open Font License) 또는 시스템 폰트 fallback
- ✅ 단정 표현·과대광고 0 (`legal_check.py` 별도 Task 2에서 점검)
- ✅ 디자인 스타일이 특정 제품 명백한 복제 아님 (일반적 칭찬 보드 패턴)

전면 통과 — Day 2 IP precheck에서 재확인.

## 다음 단계 (Task 2)

1. 자가 출력 검수 (가정 프린터 1장씩)
2. 4개 체크포인트 검증 (가독성·격자 정렬·색감·여백)
3. IP precheck `ip-precheck-output.md` 작성
4. CMYK 변환 → `board-print-ready.pdf` + `stickers-print-ready.pdf`
5. 운영자 최종 승인 → DesignAsset `proof_status=pass`, `operator_approval=approved` 업데이트
