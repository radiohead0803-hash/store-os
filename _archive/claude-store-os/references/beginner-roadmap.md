# Beginner Roadmap

## Goal
Build a Claude-operated self-owned store MVP that can sell the first reward-sticker product with minimum operator involvement and explicit approval gates.

## 0. 준비물

| 준비물 | 초보자 행동 | 완료 증거 |
|---|---|---|
| GitHub 계정 | repo 생성 가능 확인 | 로그인 캡처 또는 repo URL |
| Railway 계정 | 새 프로젝트 생성 가능 확인 | Railway dashboard 접근 |
| Claude/Claude Code | 개발 프롬프트 실행 가능 확인 | Claude Code 실행 화면 |
| 도메인 또는 임시 URL | MVP는 Railway URL로 시작 | URL 기록 |
| 사업자/PG 여부 | MVP에서는 주문접수만 먼저 가능 | 결제 연동 보류/진행 결정 |

## 1. 1주차 - 개발 패키지 생성

1. Skill의 `init_store_project.py`로 프로젝트 패키지를 만든다.
2. 생성된 `Docs/BEGINNER_START_HERE.md`를 먼저 읽는다.
3. Claude Code에 `Docs/CLAUDE_CODE_PROMPTS.md`의 Slice 1 프롬프트부터 순서대로 넣는다.
4. 매 slice 후 `validate_store_os.py` 기준 누락 항목을 확인한다.

## 2. 2주차 - 관리자와 상품 워크플로우

| Slice | 결과 |
|---|---|
| Admin settings | 자동화 한도, 운영자 승인 정책 입력 화면 |
| Product idea board | AI 상품 후보와 점수표 |
| Design tracker | Claude Design 결과물 상태관리 |
| Proof checklist | 출시 전 증거 체크 |

## 3. 3주차 - 고객용 판매 흐름

| Slice | 결과 |
|---|---|
| Public product page | 첫 스티커 상품 페이지 |
| Order capture | 주문 정보 접수 |
| Inventory | 재고 차감과 부족 알림 |
| CS draft | 낮은 위험 문의 초안 생성 |

## 4. 4주차 - 검증과 운영 준비

| Gate | 초보자 확인 |
|---|---|
| Unit/API tests | 명령 실행 후 pass 확인 |
| UI smoke | 브라우저에서 클릭 경로 확인 |
| Security/privacy | secret, PII, 권한 확인 |
| Railway deploy | health endpoint 확인 |
| Release gate | Final Proof Dossier 작성 |

## 최소 운영 가능 기준

- 운영자 로그인 가능.
- 상품 후보 생성/점수화 가능.
- 첫 스티커 상품을 proof checklist로 검증 가능.
- 상품을 승인 후 공개 가능.
- 고객이 상품 페이지에서 주문 접수 가능.
- 재고가 차감되고 발주 추천이 뜸.
- CS 초안과 판매 리포트가 생성됨.
- 자동화 액션이 audit log에 남음.
