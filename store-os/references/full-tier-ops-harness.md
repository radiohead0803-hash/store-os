# Full 단계 운영 하네스 — store_ops.py 사용 가이드

**Full 단계 전용**. Mini/Standard 사용자에겐 권하지 않는다 — 단계 졸업 조건 미충족 상태에서 이 하네스를 도입하면 운영 복잡도만 증가하고 매출 데이터는 늘지 않는다.

## 입력 조건 체크

다음을 모두 만족할 때만 이 하네스를 활성화한다:
- ✅ Standard 졸업 (월 100만원 × 3개월)
- ✅ 다채널 의향 (네이버 + 쿠팡 또는 Shopify)
- ✅ 시장 데이터 CSV 보유 (검색량·경쟁·키워드)
- ✅ 운영자 승인 워크플로 합의

미충족 시: Standard 단계 도구로 회귀 권고.

## 명령어 카탈로그

### 시장 분석 → 상품 점수

```bash
python scripts/store_ops.py sample-data --output ./out/sample_market.csv
python scripts/store_ops.py analyze-market ./market.csv --output ./out/store-ops
# → product_scores.csv, market_summary.json
```

받는 CSV 컬럼: 키워드, 월검색량, 경쟁상품수, 평균가, 트렌드. 별칭은 `market-data-schema.md` 참조.

### 리스팅 초안 생성

```bash
python scripts/store_ops.py generate-listings ./out/store-ops/product_scores.csv \
  --output ./out/store-ops/listings
# → 점수 상위 N개에 대해 unpublished 리스팅 초안 생성
```

생성된 리스팅은 `status=unpublished`. 법률 체크·운영자 승인 통과 전 공개 불가.

### 콘텐츠 캘린더

```bash
python scripts/store_ops.py content-calendar ./out/store-ops/product_scores.csv \
  --output ./out/store-ops/content_calendar.csv --days 30
```

### 리스크 스캔

```bash
python scripts/store_ops.py scan-risks ./out/store-ops/listings \
  --output ./out/store-ops/risk_scan.csv
```

점검 항목: 과대광고, 아동 관련 표현, 환불·배송 보장 문구, 저작권·상표권 가능성, 근거 없는 최상급 표현.

### 플랫폼 import 파일

```bash
python scripts/store_ops.py export-store-import \
  ./out/store-ops/product_scores.csv \
  ./out/store-ops/listings \
  --output ./out/store-ops/store_import.csv \
  --platform naver
```

`naver`, `coupang`, `shopify` 지원. 생성된 CSV는 수동 업로드 또는 API staging용. `live_publish_allowed=false` 기본.

### 프린터블 산출물

```bash
python scripts/store_ops.py generate-printables "초등 칭찬스티커 세트" \
  --output ./out/store-ops/printables
# → 보드판, 스티커 시트, 학습 체크리스트 TXT/HTML/PDF 초안
```

### KPI 평가

```bash
python scripts/store_ops.py evaluate-kpi ./out/store-ops/kpi_tracker.csv \
  --output ./out/store-ops/kpi_decisions.csv
```

scale / improve / pause 추천. 운영자가 최종 결정.

### 운영자 리뷰 큐

```bash
python scripts/store_ops.py review-queue ./out/store-ops \
  --output ./out/store-ops/operator_review_queue.csv
```

공개 리스팅·세일·import·유료광고·프로덕션 배포 전에 운영자가 확인해야 하는 항목 모음.

### Connector / Order State / Auto-pause / Audit (live 영역)

```bash
python scripts/store_ops.py connector-manifest --output ./out/store-ops/connector_contracts
python scripts/store_ops.py order-state-machine ./orders.csv --output ./out/store-ops/order_state_machine.csv
python scripts/store_ops.py auto-pause \
  ./out/store-ops/kpi_tracker.csv \
  --cs-csv ./out/store-ops/order_ops/cs_triage.csv \
  --risk-csv ./out/store-ops/risk_scan.csv \
  --output ./out/store-ops/auto_pause_decisions.csv
python scripts/store_ops.py audit-log ./out/store-ops --output ./out/store-ops/audit_log.csv
```

이 4개는 라이브 API 운영을 위한 사전 자산이지 실제 API 호출 자체는 별도 운영자 승인이 필요하다.

### 대시보드

```bash
python scripts/store_ops.py render-dashboard ./out/store-ops \
  --output ./out/store-ops/dashboard.html
# → 로컬 HTML. 운영자가 브라우저로 검토.
```

### 한 방 파이프라인

```bash
python scripts/store_ops.py run-pipeline ./market.csv --output ./out/store-ops
# → 위 명령들을 순차 실행
```

## 출력물의 위상

이 하네스가 만드는 모든 출력은 **운영자가 검토할 초안 또는 staging 파일**이다. AI가 직접 라이브 게시하지 않는다.

라이브 전환을 위해 필요한 것:
- 실제 플랫폼 API 자격증명 (시크릿 매니저 사용)
- 결제·배송·환불 운영 합의
- 운영자 일일 SLA 확보
- 광고·CS 자동 일시정지 룰 활성화 + 알림 채널 합의
- `proof-and-audit.md`의 모든 게이트 통과

## 100점 운영 기준

- Market CSV → product_scores.csv + market_summary.json 생성 ✓
- 리스팅 draft는 unpublished 상태로만 존재 ✓
- store_import.csv 수동 업로드 또는 API staging 가능 ✓
- risk_scan.csv 자동 생성 + 운영자 검토 ✓
- printable 초안 (TXT/HTML/PDF) 생성 ✓
- KPI 자동 평가 + scale/improve/pause 권고 ✓
- 운영자 리뷰 큐 생성 (공개/세일/import/광고/배포 전) ✓
- 운영 SOP 일/주/월 문서화 ✓
- 운영 하네스에 25+ unittest ✓
- 플랫폼 API staging, 주문·CS·배송 큐, 이미지 생성 계획, IP precheck 출력 모두 proof 증거에 포함 ✓

이 모두를 만족하지 않으면 "100점 운영"이라고 부르지 않는다. 부분 충족은 부분 충족이다.
