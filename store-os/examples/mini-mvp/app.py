#!/usr/bin/env python3
"""
최소 주문 접수 시스템 (10줄)
실행: pip install fastapi uvicorn && python app.py
접속: http://localhost:8000
"""
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import sqlite3
from datetime import datetime
from pathlib import Path

app = FastAPI(title="Mini Store MVP")

# SQLite 초기화
DB_PATH = Path(__file__).parent / "orders.db"
def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product TEXT NOT NULL,
            customer_name TEXT NOT NULL,
            customer_phone TEXT NOT NULL,
            quantity INTEGER DEFAULT 1,
            price INTEGER NOT NULL,
            total INTEGER NOT NULL,
            status TEXT DEFAULT 'pending',
            created_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

class Order(BaseModel):
    product: str
    customer_name: str
    customer_phone: str
    quantity: int = 1
    price: int

@app.get("/", response_class=HTMLResponse)
def home():
    """메인 페이지 - 주문 폼"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>칭찬스티커 스토어</title>
        <style>
            body { font-family: sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }
            h1 { color: #2c3e50; }
            .form-group { margin: 15px 0; }
            label { display: block; margin-bottom: 5px; font-weight: bold; }
            input, select { width: 100%; padding: 10px; box-sizing: border-box; }
            button { background: #3498db; color: white; padding: 12px 30px; border: none; cursor: pointer; font-size: 16px; }
            button:hover { background: #2980b9; }
            .success { background: #2ecc71; color: white; padding: 15px; margin: 20px 0; border-radius: 5px; }
        </style>
    </head>
    <body>
        <h1>🌟 칭찬스티커 스토어</h1>
        <p>초등학생 자녀를 위한 칭찬 보드판 + 스티커 세트</p>
        
        <form id="orderForm">
            <div class="form-group">
                <label>상품 선택:</label>
                <select id="product" required>
                    <option value="칭찬스티커 기본 세트" data-price="9900">칭찬스티커 기본 세트 - 9,900원</option>
                    <option value="칭찬스티커 프리미엄 세트" data-price="14900">칭찬스티커 프리미엄 세트 - 14,900원</option>
                </select>
            </div>
            
            <div class="form-group">
                <label>수량:</label>
                <input type="number" id="quantity" value="1" min="1" required>
            </div>
            
            <div class="form-group">
                <label>주문자 성함:</label>
                <input type="text" id="customer_name" placeholder="홍길동" required>
            </div>
            
            <div class="form-group">
                <label>연락처:</label>
                <input type="tel" id="customer_phone" placeholder="010-1234-5678" required>
            </div>
            
            <button type="submit">주문하기</button>
        </form>
        
        <div id="result"></div>
        
        <hr style="margin: 40px 0;">
        <p><a href="/orders">📋 주문 목록 보기</a></p>
        
        <script>
            document.getElementById('orderForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const product = document.getElementById('product');
                const selectedOption = product.options[product.selectedIndex];
                
                const orderData = {
                    product: selectedOption.value,
                    customer_name: document.getElementById('customer_name').value,
                    customer_phone: document.getElementById('customer_phone').value,
                    quantity: parseInt(document.getElementById('quantity').value),
                    price: parseInt(selectedOption.dataset.price)
                };
                
                try {
                    const response = await fetch('/order', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(orderData)
                    });
                    
                    const result = await response.json();
                    
                    if (response.ok) {
                        document.getElementById('result').innerHTML = 
                            `<div class="success">
                                ✅ 주문이 접수되었습니다!<br>
                                주문번호: #${result.order_id}<br>
                                총 금액: ${result.total.toLocaleString()}원
                            </div>`;
                        document.getElementById('orderForm').reset();
                    } else {
                        alert('주문 실패: ' + result.detail);
                    }
                } catch (error) {
                    alert('오류 발생: ' + error.message);
                }
            });
        </script>
    </body>
    </html>
    """

@app.post("/order")
def create_order(order: Order):
    """주문 접수"""
    total = order.price * order.quantity
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute(
        'INSERT INTO orders (product, customer_name, customer_phone, quantity, price, total, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)',
        (order.product, order.customer_name, order.customer_phone, order.quantity, order.price, total, datetime.now().isoformat())
    )
    conn.commit()
    order_id = cursor.lastrowid
    conn.close()
    
    return {
        "order_id": order_id,
        "status": "접수완료",
        "total": total,
        "message": "주문이 성공적으로 접수되었습니다."
    }

@app.get("/orders", response_class=HTMLResponse)
def list_orders():
    """주문 목록 (운영자용)"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute('SELECT * FROM orders ORDER BY created_at DESC')
    orders = cursor.fetchall()
    conn.close()
    
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>주문 관리</title>
        <style>
            body { font-family: sans-serif; margin: 20px; }
            h1 { color: #2c3e50; }
            table { width: 100%; border-collapse: collapse; margin: 20px 0; }
            th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
            th { background: #3498db; color: white; }
            tr:hover { background: #f5f5f5; }
            .pending { color: #f39c12; font-weight: bold; }
            .completed { color: #2ecc71; font-weight: bold; }
            a { color: #3498db; text-decoration: none; }
        </style>
    </head>
    <body>
        <h1>📋 주문 관리</h1>
        <p><a href="/">← 주문 페이지로 돌아가기</a></p>
        <table>
            <tr>
                <th>주문번호</th>
                <th>상품</th>
                <th>고객명</th>
                <th>연락처</th>
                <th>수량</th>
                <th>금액</th>
                <th>상태</th>
                <th>주문일시</th>
            </tr>
    """
    
    for order in orders:
        order_id, product, name, phone, qty, price, total, status, created = order
        status_class = "pending" if status == "pending" else "completed"
        status_text = "접수완료" if status == "pending" else "처리완료"
        
        html += f"""
            <tr>
                <td>#{order_id}</td>
                <td>{product}</td>
                <td>{name}</td>
                <td>{phone}</td>
                <td>{qty}개</td>
                <td>{total:,}원</td>
                <td class="{status_class}">{status_text}</td>
                <td>{created[:16]}</td>
            </tr>
        """
    
    html += """
        </table>
        <p>총 주문: """ + str(len(orders)) + """개</p>
    </body>
    </html>
    """
    
    return html

@app.get("/api/orders")
def get_orders_json():
    """주문 목록 (JSON API)"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute('SELECT * FROM orders ORDER BY created_at DESC')
    columns = [description[0] for description in cursor.description]
    orders = [dict(zip(columns, row)) for row in cursor.fetchall()]
    conn.close()
    
    return {"orders": orders, "total": len(orders)}

@app.get("/stats")
def get_stats():
    """통계 (대시보드용)"""
    conn = sqlite3.connect(DB_PATH)
    
    # 총 주문 수
    total_orders = conn.execute('SELECT COUNT(*) FROM orders').fetchone()[0]
    
    # 총 매출
    total_revenue = conn.execute('SELECT SUM(total) FROM orders').fetchone()[0] or 0
    
    # 오늘 주문 수
    today = datetime.now().date().isoformat()
    today_orders = conn.execute('SELECT COUNT(*) FROM orders WHERE created_at LIKE ?', (f'{today}%',)).fetchone()[0]
    
    conn.close()
    
    return {
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "today_orders": today_orders
    }

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("🚀 Mini Store MVP 시작")
    print("="*60)
    print("\n📱 접속 주소:")
    print("   주문 페이지: http://localhost:8000")
    print("   주문 관리: http://localhost:8000/orders")
    print("   통계 API: http://localhost:8000/stats")
    print("\n종료: Ctrl+C\n")
    print("="*60 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
