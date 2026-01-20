# FastAPI 백엔드 설정
import os
import io
from datetime import datetime
from typing import Optional, List
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import mysql.connector
from mysql.connector import Error
import ftplib
import uuid

# ============================================
# 버전 정보
# ============================================
VERSION = "1.0.20260120-1530"
VERSION_DATE = "2026-01-20 15:30"
VERSION_DESCRIPTION = "팜랜드 산양산삼 랜딩 페이지 v1.0"

# FastAPI 앱 생성
app = FastAPI(
    title="팜랜드 산양산삼 API",
    description=VERSION_DESCRIPTION,
    version=VERSION
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 정적 파일 서빙
app.mount("/static", StaticFiles(directory="."), name="static")

# ============================================
# 데이터베이스 설정
# ============================================
DB_CONFIG = {
    'host': 'bitnmeta2.synology.me',
    'port': 3307,
    'user': 'iyrc',
    'password': 'Dodan1004!',
    'database': 'sansam'
}

# FTP 설정
FTP_CONFIG = {
    'host': 'bitnmeta2.synology.me',
    'port': 2121,
    'user': 'ha',
    'password': 'dodan1004~',
    'base_path': '/sansam/'
}

# 카테고리 정보
CATEGORIES = {
    'farm': {'name': '재배지', 'icon': '🏞️'},
    'ginseng': {'name': '산양산삼', 'icon': '🌿'},
    'process': {'name': '선별과정', 'icon': '⚙️'},
    'package': {'name': '포장', 'icon': '📦'},
    'license': {'name': '인허가', 'icon': '📄'}
}

# ============================================
# 데이터베이스 연결
# ============================================
def get_db_connection():
    """MySQL 데이터베이스 연결"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"DB Connection Error: {e}")
        return None

# ============================================
# FTP 연결
# ============================================
def get_ftp_connection():
    """FTP 서버 연결"""
    try:
        ftp = ftplib.FTP()
        ftp.connect(FTP_CONFIG['host'], FTP_CONFIG['port'])
        ftp.login(FTP_CONFIG['user'], FTP_CONFIG['password'])
        ftp.set_pasv(True)
        return ftp
    except Exception as e:
        print(f"FTP Connection Error: {e}")
        return None

# ============================================
# Pydantic 모델
# ============================================
class Product(BaseModel):
    name: str
    description: Optional[str] = ""
    price: int
    image_path: str
    stock: int = 999
    display_order: int = 0
    is_active: int = 1

class Order(BaseModel):
    product_id: int
    quantity: int
    customer_name: str
    customer_phone: str
    customer_email: Optional[str] = ""
    delivery_address: str
    delivery_message: Optional[str] = ""

# ============================================
# API 엔드포인트
# ============================================

@app.get("/")
async def root():
    """루트 페이지 - index.html 반환"""
    return FileResponse("index.html")

@app.get("/admin")
async def admin():
    """관리자 페이지"""
    return FileResponse("admin.html")

@app.get("/api/version")
async def get_version():
    """버전 정보 반환"""
    return {
        "success": True,
        "version": VERSION,
        "version_date": VERSION_DATE,
        "description": VERSION_DESCRIPTION
    }

# ============================================
# 갤러리 API
# ============================================

@app.get("/api/gallery")
async def get_gallery(category: Optional[str] = None):
    """갤러리 이미지 조회"""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="DB 연결 실패")
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        if category:
            # 특정 카테고리 조회
            cursor.execute(
                "SELECT * FROM gallery_images WHERE category = %s ORDER BY display_order ASC, created_at ASC",
                (category,)
            )
            images = cursor.fetchall()
            
            # URL 생성
            for img in images:
                img['url'] = f"/api/image/{img['category']}/{img['filename']}"
            
            return {
                "success": True,
                "data": {
                    "category": category,
                    "images": images,
                    "count": len(images)
                }
            }
        else:
            # 모든 카테고리 조회
            result = {}
            
            for cat_code, cat_info in CATEGORIES.items():
                cursor.execute(
                    "SELECT * FROM gallery_images WHERE category = %s ORDER BY display_order ASC, created_at ASC",
                    (cat_code,)
                )
                images = cursor.fetchall()
                
                # URL 생성
                for img in images:
                    img['url'] = f"/api/image/{img['category']}/{img['filename']}"
                
                # 대표 이미지 찾기
                rep_image = next((img for img in images if img['is_representative'] == 1), images[0] if images else None)
                
                result[cat_code] = {
                    'name': cat_info['name'],
                    'icon': cat_info['icon'],
                    'count': len(images),
                    'representative': rep_image,
                    'images': images
                }
            
            return {
                "success": True,
                "data": result
            }
    
    except Error as e:
        raise HTTPException(status_code=500, detail=f"DB 오류: {str(e)}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

@app.post("/api/upload")
async def upload_image(
    category: str = Form(...),
    images: List[UploadFile] = File(...)
):
    """이미지 업로드 (여러 개 지원)"""
    
    uploaded = []
    errors = []
    
    for image in images:
        try:
            # 파일 확장자 확인
            allowed_extensions = ['jpg', 'jpeg', 'png', 'gif', 'webp']
            file_ext = image.filename.split('.')[-1].lower()
            if file_ext not in allowed_extensions:
                errors.append(f"{image.filename}: 지원하지 않는 파일 형식")
                continue
            
            # 파일명 생성
            timestamp = int(datetime.now().timestamp())
            unique_id = str(uuid.uuid4())[:8]
            filename = f"image_{timestamp}_{unique_id}.{file_ext}"
            
            # FTP 업로드
            ftp = get_ftp_connection()
            if not ftp:
                errors.append(f"{image.filename}: FTP 연결 실패")
                continue
            
            # FTP 폴더 생성 (없으면)
            ftp_path = f"{FTP_CONFIG['base_path']}{category}/"
            try:
                ftp.cwd(ftp_path)
            except:
                # 폴더 생성
                dirs = ftp_path.strip('/').split('/')
                current = ''
                for d in dirs:
                    current += f'/{d}'
                    try:
                        ftp.mkd(current)
                    except:
                        pass
                ftp.cwd(ftp_path)
            
            # 파일 업로드
            file_content = await image.read()
            ftp.storbinary(f'STOR {filename}', io.BytesIO(file_content))
            ftp.quit()
            
            # DB에 메타데이터 저장
            conn = get_db_connection()
            if not conn:
                errors.append(f"{image.filename}: DB 연결 실패")
                continue
            
            cursor = conn.cursor()
            file_path = f"{ftp_path}{filename}"
            file_size = len(file_content)
            
            # 이미지가 첫 번째인 경우 대표 이미지로 설정
            cursor.execute("SELECT COUNT(*) FROM gallery_images WHERE category = %s", (category,))
            count = cursor.fetchone()[0]
            is_representative = 1 if count == 0 else 0
            
            cursor.execute("""
                INSERT INTO gallery_images 
                (category, filename, original_name, file_path, file_size, is_representative, display_order)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (category, filename, image.filename, file_path, file_size, is_representative, count))
            
            conn.commit()
            image_id = cursor.lastrowid
            
            cursor.close()
            conn.close()
            
            uploaded.append({
                "filename": filename,
                "original_name": image.filename,
                "file_path": f"/api/image/{category}/{filename}",
                "image_id": image_id
            })
        
        except Exception as e:
            errors.append(f"{image.filename}: {str(e)}")
    
    return {
        "success": len(uploaded) > 0,
        "message": f"{len(uploaded)}장 업로드 성공, {len(errors)}장 실패",
        "data": {
            "uploaded": uploaded,
            "errors": errors
        }
    }

@app.get("/api/image/{category}/{filename}")
async def serve_image(category: str, filename: str):
    """FTP에서 이미지 가져오기"""
    ftp = get_ftp_connection()
    if not ftp:
        raise HTTPException(status_code=500, detail="FTP 연결 실패")
    
    try:
        ftp_path = f"{FTP_CONFIG['base_path']}{category}/{filename}"
        
        # 메모리에 파일 다운로드
        file_data = io.BytesIO()
        ftp.retrbinary(f'RETR {ftp_path}', file_data.write)
        ftp.quit()
        
        file_data.seek(0)
        
        # MIME 타입 결정
        ext = filename.split('.')[-1].lower()
        mime_types = {
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'png': 'image/png',
            'gif': 'image/gif',
            'webp': 'image/webp'
        }
        media_type = mime_types.get(ext, 'image/jpeg')
        
        from fastapi.responses import StreamingResponse
        return StreamingResponse(file_data, media_type=media_type)
    
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"이미지를 찾을 수 없습니다: {str(e)}")

@app.delete("/api/gallery/{image_id}")
async def delete_image(image_id: int):
    """이미지 삭제"""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="DB 연결 실패")
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        # 이미지 정보 조회
        cursor.execute("SELECT * FROM gallery_images WHERE id = %s", (image_id,))
        image = cursor.fetchone()
        
        if not image:
            raise HTTPException(status_code=404, detail="이미지를 찾을 수 없습니다")
        
        # FTP에서 삭제
        ftp = get_ftp_connection()
        if ftp:
            try:
                ftp.delete(image['file_path'])
                ftp.quit()
            except:
                pass
        
        # DB에서 삭제
        cursor.execute("DELETE FROM gallery_images WHERE id = %s", (image_id,))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return {"success": True, "message": "이미지가 삭제되었습니다"}
    
    except Error as e:
        raise HTTPException(status_code=500, detail=f"DB 오류: {str(e)}")

# ============================================
# 상품 API
# ============================================

@app.get("/api/products")
async def get_products(active: Optional[int] = None):
    """상품 목록 조회"""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="DB 연결 실패")
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        if active is not None:
            cursor.execute(
                "SELECT * FROM products WHERE is_active = %s ORDER BY display_order ASC, id DESC",
                (active,)
            )
        else:
            cursor.execute("SELECT * FROM products ORDER BY display_order ASC, id DESC")
        
        products = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return {
            "success": True,
            "data": products,
            "count": len(products)
        }
    
    except Error as e:
        raise HTTPException(status_code=500, detail=f"DB 오류: {str(e)}")

@app.post("/api/products")
async def create_product(product: Product):
    """상품 등록"""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="DB 연결 실패")
    
    try:
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO products (name, description, price, image_path, stock, display_order, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (product.name, product.description, product.price, product.image_path, 
              product.stock, product.display_order, product.is_active))
        
        conn.commit()
        product_id = cursor.lastrowid
        
        cursor.close()
        conn.close()
        
        return {
            "success": True,
            "message": "상품이 등록되었습니다",
            "product_id": product_id
        }
    
    except Error as e:
        raise HTTPException(status_code=500, detail=f"DB 오류: {str(e)}")

@app.put("/api/products/{product_id}")
async def update_product(product_id: int, product: Product):
    """상품 수정"""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="DB 연결 실패")
    
    try:
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE products 
            SET name = %s, description = %s, price = %s, image_path = %s, 
                stock = %s, display_order = %s, is_active = %s
            WHERE id = %s
        """, (product.name, product.description, product.price, product.image_path,
              product.stock, product.display_order, product.is_active, product_id))
        
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return {"success": True, "message": "상품이 수정되었습니다"}
    
    except Error as e:
        raise HTTPException(status_code=500, detail=f"DB 오류: {str(e)}")

@app.delete("/api/products/{product_id}")
async def delete_product(product_id: int):
    """상품 삭제"""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="DB 연결 실패")
    
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return {"success": True, "message": "상품이 삭제되었습니다"}
    
    except Error as e:
        raise HTTPException(status_code=500, detail=f"DB 오류: {str(e)}")

# ============================================
# 주문 API
# ============================================

@app.post("/api/orders")
async def create_order(order: Order):
    """주문 생성"""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="DB 연결 실패")
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        # 상품 정보 조회
        cursor.execute("SELECT * FROM products WHERE id = %s AND is_active = 1", (order.product_id,))
        product = cursor.fetchone()
        
        if not product:
            raise HTTPException(status_code=404, detail="상품을 찾을 수 없습니다")
        
        # 주문번호 생성
        order_number = datetime.now().strftime("%Y%m%d") + "-" + str(uuid.uuid4())[:8].upper()
        
        # 총 금액 계산
        total_price = product['price'] * order.quantity
        
        # 주문 저장
        cursor.execute("""
            INSERT INTO orders 
            (order_number, product_id, product_name, product_price, quantity, total_price,
             customer_name, customer_phone, customer_email, delivery_address, delivery_message,
             payment_status, order_status, ip_address)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (order_number, product['id'], product['name'], product['price'], order.quantity, total_price,
              order.customer_name, order.customer_phone, order.customer_email, 
              order.delivery_address, order.delivery_message, 'pending', 'ordered', '127.0.0.1'))
        
        conn.commit()
        order_id = cursor.lastrowid
        
        cursor.close()
        conn.close()
        
        return {
            "success": True,
            "message": "주문이 접수되었습니다",
            "order": {
                "id": order_id,
                "order_number": order_number,
                "product_name": product['name'],
                "quantity": order.quantity,
                "total_price": total_price,
                "customer_name": order.customer_name
            }
        }
    
    except Error as e:
        raise HTTPException(status_code=500, detail=f"DB 오류: {str(e)}")

@app.get("/api/orders/{order_number}")
async def get_order(order_number: str):
    """주문 조회"""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="DB 연결 실패")
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM orders WHERE order_number = %s", (order_number,))
        order = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if not order:
            raise HTTPException(status_code=404, detail="주문을 찾을 수 없습니다")
        
        return {"success": True, "data": order}
    
    except Error as e:
        raise HTTPException(status_code=500, detail=f"DB 오류: {str(e)}")

# ============================================
# 서버 실행
# ============================================
if __name__ == "__main__":
    import uvicorn
    import io
    
    print("=" * 50)
    print("  팜랜드 산양산삼 FastAPI 서버")
    print("=" * 50)
    print(f"  서버 주소: http://localhost:8000")
    print(f"  관리자: http://localhost:8000/admin")
    print(f"  API 문서: http://localhost:8000/docs")
    print("=" * 50)
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
