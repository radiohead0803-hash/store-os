# Mini Store MVP - 10분 만에 실행하는 주문 시스템

## 빠른 시작

```bash
# 1. 패키지 설치
pip install fastapi uvicorn

# 2. 서버 실행
python app.py

# 3. 브라우저 열기
# → http://localhost:8000
```

## 기능

- ✅ 주문 접수 (상품, 고객 정보, 수량)
- ✅ 주문 관리 페이지 (운영자용)
- ✅ SQLite 자동 저장 (orders.db)
- ✅ 실시간 통계 API
- ✅ 모바일 반응형 디자인

## 파일 구조

```
mini-mvp/
├── app.py        # 메인 애플리케이션 (250줄)
├── orders.db     # SQLite 데이터베이스 (자동 생성)
└── README.md     # 이 파일
```

## 실행 로그 예시

```
$ python app.py

============================================================
🚀 Mini Store MVP 시작
============================================================

📱 접속 주소:
   주문 페이지: http://localhost:8000
   주문 관리: http://localhost:8000/orders
   통계 API: http://localhost:8000/stats

종료: Ctrl+C

============================================================

INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

## API 엔드포인트

### 1. 주문 접수
```bash
curl -X POST http://localhost:8000/order \
  -H "Content-Type: application/json" \
  -d '{
    "product": "칭찬스티커 기본 세트",
    "customer_name": "김엄마",
    "customer_phone": "010-1234-5678",
    "quantity": 2,
    "price": 9900
  }'

# 응답:
{
  "order_id": 1,
  "status": "접수완료",
  "total": 19800,
  "message": "주문이 성공적으로 접수되었습니다."
}
```

### 2. 주문 목록 조회 (JSON)
```bash
curl http://localhost:8000/api/orders

# 응답:
{
  "orders": [
    {
      "id": 1,
      "product": "칭찬스티커 기본 세트",
      "customer_name": "김엄마",
      "customer_phone": "010-1234-5678",
      "quantity": 2,
      "price": 9900,
      "total": 19800,
      "status": "pending",
      "created_at": "2026-05-22T10:30:00"
    }
  ],
  "total": 1
}
```

### 3. 통계 조회
```bash
curl http://localhost:8000/stats

# 응답:
{
  "total_orders": 15,
  "total_revenue": 148500,
  "today_orders": 3
}
```

## 다음 단계

### 1단계: 디자인 추가 (Canva)
- 상품 이미지 제작
- 썸네일 + 상세 이미지

### 2단계: 상품 설명 생성 (Claude)
```bash
cd ../..
python scripts/auto_claude.py \
  --product "칭찬스티커 기본 세트" \
  --save listings/
```

### 3단계: 법률 체크
```bash
python scripts/legal_check.py listings/listing_*.md
```

### 4단계: 배포 (Vercel)
```bash
# 무료 배포
vercel deploy

# 또는 Railway
railway up
```

## 비용

- ✅ FastAPI + SQLite: **무료**
- ✅ 로컬 개발: **무료**
- ✅ Vercel Hobby 배포: **무료** (100GB bandwidth)

## 실전 팁

### 1. 데이터베이스 백업
```bash
cp orders.db orders_backup_$(date +%Y%m%d).db
```

### 2. 주문 데이터 CSV 내보내기
```python
import sqlite3
import csv

conn = sqlite3.connect('orders.db')
cursor = conn.execute('SELECT * FROM orders')

with open('orders.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow([d[0] for d in cursor.description])
    writer.writerows(cursor.fetchall())

print("✅ orders.csv 생성 완료")
```

### 3. 주문 상태 업데이트
```python
import sqlite3

conn = sqlite3.connect('orders.db')
conn.execute('UPDATE orders SET status = ? WHERE id = ?', ('completed', 1))
conn.commit()
print("✅ 주문 #1 처리 완료")
```

## 제한사항 (MVP)

- ❌ 결제 연동 없음 (주문 접수만)
- ❌ 회원 가입/로그인 없음
- ❌ 이메일/SMS 알림 없음
- ❌ 재고 관리 없음

→ **Standard 단계**로 업그레이드 시 추가

## 문제 해결

### 포트 8000이 사용 중일 때
```python
# app.py 마지막 줄 수정
uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")
```

### SQLite 파일 손상 시
```bash
rm orders.db
python app.py  # 자동 재생성
```

## 라이선스

MIT License - 자유롭게 수정 및 배포 가능
