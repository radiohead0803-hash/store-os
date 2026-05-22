# Troubleshooting

## Beginner Failure Map

| 증상 | 가능 원인 | 조치 |
|---|---|---|
| Claude Code가 너무 큰 범위를 만들려 함 | 프롬프트가 slice 단위가 아님 | `CLAUDE_CODE_PROMPTS.md`의 Slice 1부터 하나씩 실행 |
| 배포는 됐지만 화면이 안 뜸 | env 또는 build 실패 | Railway logs, health endpoint, env 예시 확인 |
| 상품이 공개되지 않음 | proof/legal 승인 미완료 | ProofChecklist와 Product flags 확인 |
| AI 자동답변이 안 나감 | 정책 템플릿 미승인 | AutomationPolicy에서 low-risk FAQ 허용 확인 |
| 재고 발주가 자동 실행되지 않음 | 한도 초과 또는 L2/L3 정책 미설정 | operator approval required로 처리 |
| 주문 데이터에 개인정보가 과다 저장됨 | PII 최소화 미적용 | schema와 CS prompt redaction 규칙 수정 |
| 스티커 인쇄 품질 불명확 | proof evidence 부족 | 실물 사진, DPI, 칼선, 샘플 검수 증거 업로드 |

## Hard Stop Conditions

즉시 중단하고 운영자 승인 필요:

- DB migration이 운영 데이터 삭제 가능.
- secret이 코드/로그에 노출.
- AI가 환불 거절 문구를 자동 전송하려 함.
- 상품 상세페이지에 교육 효과 보장 표현이 있음.
- 고액 발주가 자동 실행되려 함.
