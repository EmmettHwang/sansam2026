# FastAPI 백엔드 설정
import os
import io
from datetime import datetime
from typing import Optional, List
from fastapi import FastAPI, File, UploadFile, HTTPException, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
import mysql.connector
from mysql.connector import Error
import ftplib
import uuid
import subprocess
from PIL import Image

# ============================================
# 버전 정보
# ============================================
VERSION = "1.4.20260129-0050"
VERSION_DATE = "2026-01-29 00:50"
VERSION_DESCRIPTION = "팜랜드 산양산삼 랜딩 페이지 v1.4 - 상담신청 이메일 알림, 서버 자동화"

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

# 422 에러 핸들러
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print("\n" + "="*60)
    print("❌ 422 VALIDATION ERROR")
    print("="*60)
    print(f"URL: {request.url}")
    print(f"Method: {request.method}")
    print(f"Headers: {dict(request.headers)}")
    print(f"\nValidation Errors:")
    for error in exc.errors():
        print(f"  - {error}")
    print(f"\nBody: {exc.body}")
    print("="*60 + "\n")
    
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "입력 데이터 검증 실패",
            "errors": exc.errors(),
            "detail": str(exc.errors())
        }
    )

# 정적 파일 서빙
app.mount("/css", StaticFiles(directory="css"), name="css")
app.mount("/js", StaticFiles(directory="js"), name="js")
app.mount("/images", StaticFiles(directory="images"), name="images")
app.mount("/static", StaticFiles(directory="."), name="static")

# ============================================
# 데이터베이스 설정
# ============================================
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'iyrc',
    'password': 'dodan1004',
    'database': 'sansam'
}

# FTP 설정
FTP_CONFIG = {
    'host': 'bitnmeta2.synology.me',
    'port': 2121,
    'user': 'ha',
    'password': 'dodan1004~',
    'base_path': '/homes/ha/sansam/'
}

# 카테고리 정보
CATEGORIES = {
    'farm': {'name': '재배지', 'icon': '🏞️'},
    'ginseng': {'name': '산양산삼', 'icon': '🌿'},
    'process': {'name': '선별과정', 'icon': '⚙️'},
    'package': {'name': '포장', 'icon': '📦'},
    'license': {'name': '인허가', 'icon': '📄'},
    'live': {'name': 'Live', 'icon': '📹'}
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
        
        # 현재 디렉토리 확인
        current_dir = ftp.pwd()
        print(f"🔗 FTP 연결 성공 - 현재 디렉토리: {current_dir}")
        
        return ftp
    except Exception as e:
        print(f"❌ FTP Connection Error: {e}")
        return None

# ============================================
# Pydantic 모델
# ============================================
class Product(BaseModel):
    name: str
    description: Optional[str] = ""
    price: int
    image_path: Optional[str] = ""  # Optional로 변경
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
    """루트 페이지 - index.html 반환 (캐시 무시)"""
    return FileResponse(
        "index.html",
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        }
    )

@app.get("/admin")
async def admin():
    """관리자 페이지 (캐시 무시)"""
    return FileResponse(
        "admin.html",
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        }
    )

@app.get("/favicon.ico")
async def favicon():
    """파비콘"""
    return FileResponse("favicon.svg", media_type="image/svg+xml")

@app.get("/api/version")
async def get_version():
    """버전 정보 반환"""
    return {
        "success": True,
        "version": VERSION,
        "version_date": VERSION_DATE,
        "description": VERSION_DESCRIPTION
    }

@app.get("/api/test")
async def test():
    """테스트 엔드포인트"""
    return {"success": True, "message": "API 정상 작동"}

@app.post("/api/og-image")
async def upload_og_image(file: UploadFile = File(...)):
    """OG 이미지 (미리보기 이미지) 업로드"""
    try:
        # 파일 확장자 확인
        allowed_extensions = ['jpg', 'jpeg', 'png', 'webp']
        file_ext = file.filename.split('.')[-1].lower()
        if file_ext not in allowed_extensions:
            return {"success": False, "message": "지원하지 않는 파일 형식입니다."}

        # 파일 저장
        content = await file.read()
        save_path = "images/og-preview.jpg"

        # images 폴더 생성
        os.makedirs("images", exist_ok=True)

        # 이미지 리사이즈 (1200x630 권장)
        try:
            img = Image.open(io.BytesIO(content))
            # 비율 유지하며 리사이즈
            target_width = 1200
            target_height = 630
            img = img.resize((target_width, target_height), Image.LANCZOS)

            # RGB 모드로 변환 (PNG의 경우 RGBA일 수 있음)
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')

            img.save(save_path, 'JPEG', quality=90, optimize=True)
        except Exception as e:
            # 리사이즈 실패 시 원본 저장
            with open(save_path, 'wb') as f:
                f.write(content)

        return {"success": True, "message": "미리보기 이미지가 업로드되었습니다."}

    except Exception as e:
        return {"success": False, "message": str(e)}

# ============================================
# 갤러리 API
# ============================================

@app.get("/api/gallery")
async def get_gallery(category: Optional[str] = None):
    """갤러리 이미지 조회"""
    # 로그 최소화
    # print(f"🖼️ Gallery GET: category={category}")
    
    conn = get_db_connection()
    if not conn:
        print("❌ Gallery API: DB 연결 실패")
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
            
            # 로그 제거 - 성능 향상
            # print(f"   카테고리 '{category}': {len(images)}개 이미지")
            
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
                
                # 로그 제거 - 성능 향상
                # print(f"   카테고리 '{cat_code}': {len(images)}개 이미지")
                
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
    
    print("\n" + "="*60)
    print("📥 UPLOAD REQUEST RECEIVED")
    print("="*60)
    
    try:
        print(f"Category: {category}")
        print(f"Images count: {len(images)}")
        for i, img in enumerate(images, 1):
            print(f"  {i}. {img.filename} ({img.content_type})")
    except Exception as log_error:
        print(f"❌ 로깅 에러: {log_error}")
    
    print("="*60 + "\n")
    
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
            
            # 폴더가 없으면 생성
            try:
                ftp.cwd(ftp_path)
                print(f"  ✅ FTP 폴더 존재: {ftp_path}")
            except Exception as e:
                print(f"  📁 FTP 폴더 생성 중: {ftp_path}")
                # 각 레벨의 폴더를 순차적으로 생성
                path_parts = ftp_path.strip('/').split('/')
                current_path = '/'
                
                for part in path_parts:
                    current_path = current_path.rstrip('/') + '/' + part
                    try:
                        ftp.cwd(current_path)
                        print(f"    ✅ {current_path} 존재")
                    except:
                        try:
                            ftp.mkd(current_path)
                            ftp.cwd(current_path)
                            print(f"    ✅ {current_path} 생성 완료")
                        except Exception as mkd_error:
                            print(f"    ❌ {current_path} 생성 실패: {mkd_error}")
                            errors.append(f"{image.filename}: FTP 폴더 생성 실패 ({current_path})")
                            ftp.quit()
                
                # 폴더 생성 실패 시 다음 파일로
                if f"{image.filename}: FTP 폴더 생성 실패" in str(errors):
                    continue
            
            # 파일 업로드
            try:
                file_content = await image.read()
                ftp.storbinary(f'STOR {filename}', io.BytesIO(file_content))
                print(f"  ✅ FTP 업로드 성공: {filename}")
            except Exception as upload_error:
                print(f"  ❌ FTP 업로드 실패: {upload_error}")
                errors.append(f"{image.filename}: {str(upload_error)}")
                ftp.quit()
                continue
            
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
async def serve_image(category: str, filename: str, size: int = None):
    """이미지 제공 (로컬 캐시 우선, 없으면 FTP에서 다운로드)

    Args:
        size: 리사이즈 너비 (기본값은 카테고리별 최적화)
    """

    # 카테고리별 기본 리사이즈 크기 설정 (성능 최적화)
    DEFAULT_SIZES = {
        'live': 1280,      # 타임랩스
        'products': 600,   # 상품 이미지 (작게)
        'farm': 1000,      # 갤러리
        'ginseng': 1000,
        'process': 1000,
        'package': 1000,
        'license': 1000,
    }

    if size is None:
        size = DEFAULT_SIZES.get(category, 1000)

    # 로컬 캐시 경로 (리사이즈된 이미지는 별도 폴더)
    if size:
        cache_dir = f"images/cache/{category}/resized_{size}"
    else:
        cache_dir = f"images/cache/{category}"
    os.makedirs(cache_dir, exist_ok=True)
    cache_path = f"{cache_dir}/{filename}"

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

    # 로컬 캐시 확인
    if os.path.exists(cache_path):
        return FileResponse(cache_path, media_type=media_type)

    # FTP에서 다운로드
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

        # 리사이즈 처리
        if size:
            try:
                img = Image.open(file_data)

                # 이미지가 목표 크기보다 크면 리사이즈
                if img.width > size:
                    ratio = size / img.width
                    new_height = int(img.height * ratio)
                    img = img.resize((size, new_height), Image.LANCZOS)

                # RGB 변환 (PNG RGBA 처리)
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')

                # 저장 (JPEG 압축)
                output = io.BytesIO()
                img.save(output, format='JPEG', quality=85, optimize=True)
                output.seek(0)

                with open(cache_path, 'wb') as f:
                    f.write(output.getvalue())
            except Exception as resize_error:
                print(f"  ⚠️ 리사이즈 실패, 원본 사용: {resize_error}")
                file_data.seek(0)
                with open(cache_path, 'wb') as f:
                    f.write(file_data.getvalue())
        else:
            # 원본 저장
            with open(cache_path, 'wb') as f:
                f.write(file_data.getvalue())

        return FileResponse(cache_path, media_type=media_type)

    except Exception as e:
        print(f"  ❌ 이미지 로드 실패: {str(e)}")
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
# Live 타임랩스 API (FTP 직접 읽기, DB 사용 안 함)
# ============================================

@app.get("/api/live/images")
async def get_live_images(limit: int = 100, offset: int = 0):
    """
    Live 타임랩스 이미지 목록 조회 (FTP에서 직접)
    - DB에 저장하지 않고 FTP에서 직접 이미지 목록 가져오기
    - 최신 이미지부터 정렬
    """
    # 로그 최소화 - 필요시에만 출력
    # print(f"📹 Live Timelapse: limit={limit}, offset={offset}")
    
    ftp = get_ftp_connection()
    if not ftp:
        raise HTTPException(status_code=500, detail="FTP 연결 실패")
    
    try:
        live_path = f"{FTP_CONFIG['base_path']}live/"
        
        # live 폴더로 이동
        try:
            ftp.cwd(live_path)
        except:
            # live 폴더가 없으면 생성
            print(f"  📁 Live 폴더 생성: {live_path}")
            try:
                ftp.mkd(live_path)
                ftp.cwd(live_path)
            except Exception as e:
                print(f"  ❌ Live 폴더 생성 실패: {e}")
                ftp.quit()
                return {
                    "success": True,
                    "data": {
                        "images": [],
                        "total": 0,
                        "limit": limit,
                        "offset": offset
                    }
                }
        
        # 이미지 파일 목록 가져오기
        files = []
        ftp.dir(files.append)
        
        # 이미지 파일만 필터링 (jpg, jpeg, png, gif, webp)
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
        image_files = []
        
        for file_info in files:
            parts = file_info.split()
            if len(parts) < 9:
                continue
            
            filename = ' '.join(parts[8:])
            file_ext = filename.lower().split('.')[-1]
            
            if f'.{file_ext}' in image_extensions:
                # 파일 수정 시간 파싱 (예: -rw-r--r-- 1 user group 12345 Jan 20 15:30 image.jpg)
                try:
                    month = parts[5]
                    day = parts[6]
                    time_or_year = parts[7]
                    
                    # 파일 크기
                    file_size = int(parts[4])
                    
                    image_files.append({
                        'filename': filename,
                        'url': f'/api/image/live/{filename}',
                        'size': file_size,
                        'modified': f"{month} {day} {time_or_year}"
                    })
        # 파일 정보 파싱 실패 시 로그 제거 (성능 향상)
                except Exception as e:
                    # print(f"  ⚠️ 파일 정보 파싱 실패: {filename} - {e}")
                    continue
        
        ftp.quit()
        
        # 최신 파일부터 정렬 (파일명으로 정렬 - 타임랩스는 보통 타임스탬프 기반)
        image_files.sort(key=lambda x: x['filename'], reverse=True)
        
        # 페이지네이션
        total = len(image_files)
        paginated = image_files[offset:offset + limit]
        
        # 로그 최소화 - 성능 향상
        # print(f"  ✅ 총 {total}개 이미지 발견")
        # print(f"  📄 반환: {len(paginated)}개 (offset: {offset}, limit: {limit})")
        
        return {
            "success": True,
            "data": {
                "images": paginated,
                "total": total,
                "limit": limit,
                "offset": offset
            }
        }
    
    except Exception as e:
        # 에러만 로그 출력
        print(f"  ❌ Live 이미지 조회 실패: {e}")
        raise HTTPException(status_code=500, detail=f"Live 이미지 조회 실패: {str(e)}")

# ============================================
# 상품 API
# ============================================

@app.get("/api/products")
async def get_products(active: Optional[int] = None):
    """상품 목록 조회"""
    # 로그 최소화
    # print(f"🔍 Products GET: active={active}")
    
    conn = get_db_connection()
    if not conn:
        print("❌ Products API: DB 연결 실패")
        raise HTTPException(status_code=500, detail="DB 연결 실패")
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        if active is not None:
            query = "SELECT * FROM products WHERE is_active = %s ORDER BY display_order ASC, id DESC"
            cursor.execute(query, (active,))
            print(f"   SQL: {query} (is_active={active})")
        else:
            query = "SELECT * FROM products ORDER BY display_order ASC, id DESC"
            cursor.execute(query)
            print(f"   SQL: {query}")
        
        products = cursor.fetchall()
        print(f"   결과: {len(products)}개 상품")
        
        if len(products) > 0:
            for p in products:
                print(f"   - ID {p['id']}: {p['name']} (is_active={p['is_active']})")
        
        cursor.close()
        conn.close()
        
        return {
            "success": True,
            "data": products,
            "count": len(products)
        }
    
    except Error as e:
        print(f"❌ Products API Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"DB 오류: {str(e)}")

@app.post("/api/products")
async def create_product(product: Product):
    """상품 등록"""
    print(f"📦 상품 등록: {product.name} (₩{product.price:,})")
    
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
        
        print(f"✅ 상품 등록 성공: ID {product_id}")
        
        return {
            "success": True,
            "message": "상품이 등록되었습니다",
            "product_id": product_id
        }
    
    except Error as e:
        print(f"❌ 상품 등록 실패: {str(e)}")
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
# 상담 신청 API
# ============================================
class ConsultationRequest(BaseModel):
    name: Optional[str] = ""
    phone: str
    purpose: str
    budget: Optional[str] = "미정"
    delivery: Optional[str] = "미정"
    message: Optional[str] = ""
    form_type: str = "quick"  # "quick" or "detail"

@app.post("/api/consultation")
async def submit_consultation(request: ConsultationRequest):
    """상담 신청을 이메일로 전송"""
    try:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if request.form_type == "quick":
            subject = f"[1분 상담 신청] {request.phone}"
            body = f"""안녕하세요, 새로운 상담 신청이 접수되었습니다.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 1분 상담 신청
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📞 연락처: {request.phone}
📝 문의 내용: {request.purpose}

⏰ 접수 시간: {now}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
팜랜드 산양산삼 자동 알림
"""
        else:
            subject = f"[상세 상담 신청] {request.name} / {request.phone}"
            body = f"""안녕하세요, 새로운 상세 상담 신청이 접수되었습니다.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 상세 상담 신청
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👤 이름: {request.name}
📞 연락처: {request.phone}
🎯 목적: {request.purpose}
💰 예산: {request.budget}
📅 수령 희망일: {request.delivery}
💬 추가 요청: {request.message or "없음"}

⏰ 접수 시간: {now}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
팜랜드 산양산삼 자동 알림
"""

        # 이메일 전송 (msmtp 사용)
        email_content = f"Subject: {subject}\nContent-Type: text/plain; charset=utf-8\n\n{body}"

        process = subprocess.Popen(
            ['msmtp', 'hdh6401@gmail.com'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate(email_content.encode('utf-8'))

        if process.returncode != 0:
            print(f"Email send error: {stderr.decode()}")
            # 이메일 실패해도 성공 응답 (사용자 경험을 위해)

        return {"success": True, "message": "상담 신청이 접수되었습니다."}

    except Exception as e:
        print(f"Consultation error: {str(e)}")
        return {"success": False, "message": "상담 신청 처리 중 오류가 발생했습니다."}

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
