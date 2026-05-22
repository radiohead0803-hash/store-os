# 네이버 스마트스토어 API 연동 가이드

## 목차
1. [준비물](#준비물)
2. [OAuth 인증](#oauth-인증)
3. [상품 등록](#상품-등록)
4. [주문 조회](#주문-조회)
5. [재고 관리](#재고-관리)
6. [자주 묻는 질문](#faq)

---

## 준비물

### 1. 스마트스토어 개설
- 네이버 커머스 (https://sell.smartstore.naver.com) 가입
- 사업자 또는 개인 판매자 인증
- 정산 계좌 등록

### 2. API 신청
1. 스마트스토어 센터 → 설정 → 개발자 도구
2. "API 이용 신청" 클릭
3. 승인 대기 (1-2영업일)
4. **Client ID** 및 **Client Secret** 발급

### 3. 필수 정보
```python
NAVER_CLIENT_ID = "your_client_id"
NAVER_CLIENT_SECRET = "your_client_secret"
NAVER_STORE_ID = "your_store_id"
```

---

## OAuth 인증

### 1단계: 인증 URL 생성

```python
import urllib.parse

def get_auth_url():
    base_url = "https://commerce.naver.com/oauth2/authorize"
    params = {
        "client_id": NAVER_CLIENT_ID,
        "redirect_uri": "http://localhost:8000/callback",
        "response_type": "code",
        "scope": "product_read,product_write,order_read"
    }
    return f"{base_url}?{urllib.parse.urlencode(params)}"

# 실행
print(get_auth_url())
# → 브라우저에서 이 URL로 접속하여 승인
```

### 2단계: Access Token 발급

```python
import requests

def get_access_token(auth_code):
    url = "https://commerce.naver.com/oauth2/token"
    data = {
        "client_id": NAVER_CLIENT_ID,
        "client_secret": NAVER_CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": "http://localhost:8000/callback"
    }
    
    response = requests.post(url, data=data)
    token_data = response.json()
    
    # 토큰 저장
    with open("naver_token.json", "w") as f:
        json.dump(token_data, f)
    
    return token_data["access_token"]
```

### 3단계: Token Refresh (30일 후)

```python
def refresh_token(refresh_token):
    url = "https://commerce.naver.com/oauth2/token"
    data = {
        "client_id": NAVER_CLIENT_ID,
        "client_secret": NAVER_CLIENT_SECRET,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }
    
    response = requests.post(url, data=data)
    return response.json()["access_token"]
```

---

## 상품 등록

### API 엔드포인트
```
POST https://api.commerce.naver.com/external/v1/products
```

### 최소 필수 필드

```python
def create_product(access_token, product_data):
    url = "https://api.commerce.naver.com/external/v1/products"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # 최소 상품 데이터
    payload = {
        "originProduct": {
            "statusType": "SALE",  # SALE: 판매중, SOLD_OUT: 품절
            "saleType": "NEW",
            "name": product_data["name"],  # 상품명 (필수)
            "images": [
                {
                    "url": product_data["image_url"],
                    "imageType": "REPRESENTATIVE"  # 대표 이미지
                }
            ],
            "salePrice": product_data["price"],  # 판매가 (필수)
            "stockQuantity": product_data["stock"],  # 재고 (필수)
            "deliveryInfo": {
                "deliveryType": "DELIVERY",
                "deliveryFee": {
                    "feeType": "FREE"  # 무료 배송
                }
            },
            "detailContent": product_data["description"],  # 상세 설명
            "categoryId": product_data["category_id"]  # 카테고리 ID
        }
    }
    
    response = requests.post(url, headers=headers, json=payload)
    return response.json()
```

### 카테고리 ID 조회

```python
def get_categories(access_token):
    url = "https://api.commerce.naver.com/external/v1/categories"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(url, headers=headers)
    categories = response.json()
    
    # 예시: 문구/오피스 > 학용품 > 칭찬스티커
    # 카테고리 검색
    for cat in categories["data"]:
        if "학용품" in cat["name"]:
            print(f"{cat['id']}: {cat['name']}")
```

### 상품 이미지 업로드

```python
def upload_image(access_token, image_path):
    url = "https://api.commerce.naver.com/external/v1/product-images/upload"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    with open(image_path, "rb") as f:
        files = {"imageFile": f}
        response = requests.post(url, headers=headers, files=files)
    
    return response.json()["imageUrl"]

# 사용 예
image_url = upload_image(access_token, "sticker_thumbnail.jpg")
```

---

## 주문 조회

### 전체 주문 조회

```python
def get_orders(access_token, start_date, end_date):
    url = "https://api.commerce.naver.com/external/v1/pay-order/seller/orders"
    
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {
        "lastChangedFrom": start_date,  # 2026-05-01
        "lastChangedTo": end_date,      # 2026-05-31
        "lastChangedType": "PAY_WAITING"  # 결제 대기
    }
    
    response = requests.get(url, headers=headers, params=params)
    return response.json()["data"]
```

### 주문 상태 변경 (배송 처리)

```python
def ship_order(access_token, order_id, tracking_number):
    url = f"https://api.commerce.naver.com/external/v1/pay-order/seller/product-orders/{order_id}/dispatch"
    
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {
        "dispatchDate": "2026-05-22",
        "deliveryMethod": "DELIVERY",
        "deliveryCompany": "CJ대한통운",
        "trackingNumber": tracking_number
    }
    
    response = requests.post(url, headers=headers, json=payload)
    return response.json()
```

---

## 재고 관리

### 재고 조회

```python
def get_stock(access_token, product_id):
    url = f"https://api.commerce.naver.com/external/v1/products/{product_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(url, headers=headers)
    product = response.json()["originProduct"]
    return product["stockQuantity"]
```

### 재고 업데이트

```python
def update_stock(access_token, product_id, new_stock):
    url = f"https://api.commerce.naver.com/external/v1/products/{product_id}/stock"
    
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {"stockQuantity": new_stock}
    
    response = requests.patch(url, headers=headers, json=payload)
    return response.json()
```

---

## 통합 스크립트 (scripts/naver_integration.py)

```python
#!/usr/bin/env python3
"""네이버 스마트스토어 API 연동"""
import argparse
import json
import requests
from pathlib import Path

class NaverStoreAPI:
    def __init__(self, client_id, client_secret, access_token=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self.base_url = "https://api.commerce.naver.com/external/v1"
    
    def get_auth_url(self, redirect_uri="http://localhost:8000/callback"):
        params = {
            "client_id": self.client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": "product_read,product_write,order_read"
        }
        return f"https://commerce.naver.com/oauth2/authorize?{urllib.parse.urlencode(params)}"
    
    def upload_product(self, product_data, dry_run=True):
        if dry_run:
            print("\n📤 네이버 스마트스토어 등록 미리보기")
            print(f"상품명: {product_data['name']}")
            print(f"가격: {product_data['price']:,}원")
            print(f"재고: {product_data['stock']}개")
            print("\n⚠️ --dry-run 모드: 실제 등록하려면 --confirm 추가")
            return None
        
        # 실제 API 호출
        url = f"{self.base_url}/products"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "originProduct": {
                "statusType": "SALE",
                "name": product_data["name"],
                "salePrice": product_data["price"],
                "stockQuantity": product_data["stock"],
                # ... (전체 필드)
            }
        }
        
        response = requests.post(url, headers=headers, json=payload)
        return response.json()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--init-auth", action="store_true")
    parser.add_argument("--upload", help="상품 파일 경로")
    parser.add_argument("--dry-run", action="store_true")
    
    args = parser.parse_args()
    
    # 환경변수 또는 설정 파일에서 로드
    api = NaverStoreAPI(
        client_id=os.getenv("NAVER_CLIENT_ID"),
        client_secret=os.getenv("NAVER_CLIENT_SECRET")
    )
    
    if args.init_auth:
        print("🔐 OAuth 인증 시작")
        print(f"브라우저에서 열기: {api.get_auth_url()}")
    
    if args.upload:
        # 상품 파일 파싱 및 업로드
        pass

if __name__ == "__main__":
    main()
```

---

## FAQ

### Q1: API 호출 한도는?
**A**: 일반적으로 분당 100회, 일일 10,000회 제한. 대량 처리 시 배치 API 사용.

### Q2: 테스트 환경은 없나요?
**A**: 네이버는 별도 샌드박스 없음. 실제 스토어에서 "숨김" 상품으로 테스트 권장.

### Q3: 이미지 용량 제한은?
**A**: 단일 이미지 최대 10MB, 권장 해상도 1000x1000px.

### Q4: 수수료는?
**A**: 일반 상품 2.5%, 디지털/컨텐츠 12%. API 사용료 없음.

### Q5: 결제 연동은?
**A**: 네이버페이가 자동 연동됨. 별도 PG사 계약 불필요.

---

## 참고 자료

- 네이버 커머스 API 문서: https://developers.naver.com/docs/commerce/api/
- 스마트스토어 센터: https://sell.smartstore.naver.com
- API 지원 문의: commerce-api@navercorp.com

---

## 다음 단계

1. ✅ API 인증 완료
2. ✅ 첫 상품 등록
3. → 주문 자동 처리 (scripts/order_automation.py)
4. → 재고 자동 알림 (scripts/inventory_monitor.py)
