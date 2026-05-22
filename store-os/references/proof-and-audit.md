# Proof & Audit — 승인 게이트와 감사 로그 설계

## 핵심 원리

**Builder는 자기 일을 자기가 승인할 수 없다.** Proof agent만 Pass를 찍는다. 이걸 어기면 단순히 "AI가 만들었으니 통과" 회로가 만들어진다.

## Proof Decision 3종

| 결정 | 의미 | 다음 행동 |
|---|---|---|
| **Pass** | 증거가 충분하고 리스크가 수용 가능 | 다음 게이트로 진행 |
| **Conditional Pass** | 통과하되 명시된 보정/추적 조건 부착 | 조건 미이행 시 자동 차단 |
| **Fail** | 미통과. 증거 부족 또는 리스크 미해결 | builder에게 반려 + 차단 사유 기록 |

## Evidence Card 필수 필드

```markdown
# Evidence Card
- Changed files:        # 절대 경로 + git diff 요약
- Commands run:         # 복붙 가능한 명령어 (출력 일부 포함)
- Screenshots/logs:     # 파일 경로 또는 인라인
- Risks remaining:      # 알려진 리스크와 완화 계획
- Proof decision:       # Pass / Conditional Pass / Fail (proof agent만)
- Conditions:           # Conditional Pass인 경우, 추적 항목 + 만료일
```

## Audit Log 스키마

모든 자동 행동·승인 행동은 다음 필드로 한 줄 audit event를 남긴다:

| 필드 | 예시 | 비고 |
|---|---|---|
| `ts` | 2026-05-22T10:30:00Z | UTC ISO 8601 |
| `actor` | agent:listing-agent / human:operator@example.com | builder/proof/human 구분 |
| `action` | listing.draft.create / order.refund.approve | dot.notation |
| `target` | product:sku-001 / order:ord-2026-0123 | 영향받은 리소스 |
| `payload_hash` | sha256:abc... | 페이로드 원본 해시 (PII 마스킹 후) |
| `approval_id` | approval:2026-05-22-0007 | 연결된 승인 레코드 |
| `risk_level` | L0 / L1 / L2 / L3 | 자동화 경계 레벨 |
| `rollback_note` | "DB row id 42 — restore via backup 2026-05-22" | 되돌리기 절차 |
| `decision` | Pass / ConditionalPass / Fail / Executed | proof decision 또는 실행 결과 |

audit log는 append-only. 수정·삭제 시도 자체가 audit event다.

## 게이트별 통과 기준 표

| 게이트 | 통과 기준 | 차단 조건 | 필요한 증거 |
|---|---|---|---|
| **Listing Draft → Public** | 법률 체크 통과 + 디자인 proof + 이미지 readability proof + 운영자 승인 | 법률 필수 조치 1개+ 미해결, IP precheck 고위험, 아동 효과 과대광고 표현 | legal_check 출력, design_proof 스크린샷, 운영자 승인 ID |
| **Order Capture → Fulfillment** | 결제 확인, 재고 차감, 주소 검증 통과 | 결제 미확인, 재고 부족, 주소 의심 (해외/PO box 등) | payment_event_id, inventory_event_id |
| **Refund Auto → Refund Execute** | 정책 내 금액·기간, 분쟁 이력 없음, 운영자 승인 (금액 기준 초과 시) | 정책 외, 분쟁/법적 위험, 운영자 한도 초과 | policy_match_log, dispute_history_query |
| **AI 자동 CS 응답** | FAQ 매칭 점수 > threshold, 환불·법률·앵그리 카테고리 아님 | 카테고리 misroute, 점수 미달, 고객 반복 문의 | classifier_output, faq_template_id |
| **Production Deploy** | 테스트 통과, DB 마이그레이션 dry-run 성공, 롤백 경로 확인, 운영자 승인 | 마이그레이션 미검증, 시크릿 변경, 의존성 메이저 변경 | ci_run_id, migration_dry_run_log, rollback_plan |
| **신규 광고 활성화** | ROAS 시뮬, 예산 한도, 카피 법률 체크, 운영자 승인 | 예산 한도 초과, 카피 법률 risk, 신규 제품 (졸업 조건 미충족) | budget_envelope, copy_check_log |

## Kill-switch — 자동 일시정지 룰

다음 조건 충족 시 광고/리스팅/자동 CS를 자동으로 일시정지하고 운영자 알림:

- 광고 ROAS < threshold (24시간)
- 반품률 > threshold (7일)
- CS 티켓 급증 (시간당 normal × 3)
- 동일 상품에 IP/claims 고위험 발견
- CTR 급락 (벤치마크 0.3배 이하)
- 결제 실패율 > threshold

일시정지 자체도 audit event. 운영자 재개도 audit event.

## L0 절대 자동화 금지 목록

- PG/정산/계좌 변경
- 법률·환불·개인정보 문구 최종 승인
- 공개 출시
- 고비용 인쇄 발주 (한도 초과)
- 벤더 계약 체결
- 환불 거부·분쟁 결정
- 프로덕션 배포
- DB 마이그레이션
- 시크릿 변경
- 아동 대상 효과 보증
- 학습 효과 단정
- 의료/금융/법률 자문성 문구

이 목록은 추가만 가능. 제거하려면 별도 정책 변경 + 운영자 승인 필요.

## Conditional Pass 운영 룰

조건은 반드시:
1. **추적 가능** — 자동 모니터로 측정 가능한 지표
2. **만료일 있음** — 무기한 조건 금지
3. **자동 차단** — 조건 미이행 시 다음 게이트 자동 Fail

예: "리스팅 공개는 7일간만 — D+7에 매출 데이터 검토하여 갱신 결정. 매출 0건이면 자동 비공개."

## 운영자에게 전달할 한 문장

"빨간불을 무시한 모든 사고는 빨간불을 무시한 결정이 audit log에 남았다. 그게 다음에 안 무시할 이유다."
