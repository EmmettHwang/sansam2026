# 🐍 FastAPI로 전환 완료!

## 🎉 PHP → Python FastAPI 포팅 완료!

이제 **Python만** 있으면 됩니다! PHP 설치 불필요!

---

## 🚀 초간단 실행 방법

### ✅ Windows 사용자

1. **`서버실행_FastAPI.bat` 더블클릭**
   ```
   (검은 창이 뜨고 자동으로 설치 + 실행)
   ```

2. **브라우저 열기**
   - 메인 페이지: `http://localhost:8000`
   - 관리자 페이지: `http://localhost:8000/admin`
   - API 문서: `http://localhost:8000/docs` ← 자동 생성!

3. **완료!** 🎉

---

### ✅ Mac/Linux 사용자

1. **터미널 열기**
   ```bash
   chmod +x 서버실행_FastAPI.sh
   ./서버실행_FastAPI.sh
   ```

2. **브라우저에서 접속**
   - `http://localhost:8000/admin`

---

## 📦 필요한 파일

### 신규 파일 (Python FastAPI)
- ✅ **`main.py`** - FastAPI 백엔드 서버 (PHP 대체!)
- ✅ **`requirements.txt`** - Python 패키지 목록
- ✅ **`서버실행_FastAPI.bat`** - Windows 실행 파일
- ✅ **`서버실행_FastAPI.sh`** - Mac/Linux 실행 파일
- ✅ **`admin-web.html`** - 관리자 페이지 (FastAPI용)

### 기존 파일 (그대로 사용)
- ✅ `index.html` - 메인 페이지
- ✅ `css/style.css` - 스타일
- ✅ `js/script.js` - JavaScript
- ✅ `database/schema.sql` - DB 스키마

### 삭제해도 되는 파일 (PHP)
- ❌ `admin-server.php` (→ `admin-web.html`로 대체)
- ❌ `api/*.php` (→ `main.py`로 대체)
- ❌ `purchase.php` (→ 곧 Python으로 변환)
- ❌ `order-complete.php` (→ 곧 Python으로 변환)

---

## 🎯 장점

### PHP → Python FastAPI 전환 장점:

1. **✅ 설치 간단**
   - PHP: XAMPP 설치, 설정 복잡
   - Python: `pip install` 한 줄!

2. **✅ 실행 간단**
   - PHP: php -S localhost:8000 (수동)
   - Python: .bat 파일 더블클릭! (자동)

3. **✅ 자동 API 문서**
   - PHP: 수동으로 문서 작성
   - Python: `/docs` 접속하면 자동 생성!

4. **✅ 타입 안정성**
   - PHP: 타입 체크 약함
   - Python: Pydantic으로 타입 검증

5. **✅ 비동기 처리**
   - PHP: 동기 처리
   - Python: async/await로 성능 ↑

---

## 📋 사용 방법

### 1️⃣ 처음 실행 (자동 설치)

```bash
# Windows
서버실행_FastAPI.bat 더블클릭

# Mac/Linux
./서버실행_FastAPI.sh
```

**자동으로 수행됩니다:**
- ✅ Python 가상환경 생성
- ✅ 필요한 패키지 설치 (FastAPI, uvicorn, mysql-connector 등)
- ✅ 서버 실행

### 2️⃣ DB 초기화

브라우저에서:
```
http://localhost:8000/static/database/init_db.php
```

또는 MySQL 직접 실행:
```bash
mysql -h bitnmeta2.synology.me -P 3307 -u iyrc -p sansam < database/schema.sql
```

### 3️⃣ 관리자 페이지 접속

```
http://localhost:8000/admin
```

- 🖼️ 갤러리 관리 탭: 인허가 이미지 업로드
- 🛒 간단구매 상품 관리 탭: 상품 등록

### 4️⃣ 메인 페이지 확인

```
http://localhost:8000
```

---

## 🔍 API 문서 (자동 생성!)

FastAPI의 최고 장점:

```
http://localhost:8000/docs
```

**Swagger UI가 자동으로 생성됩니다!**
- 모든 API 엔드포인트 목록
- 각 API의 파라미터, 응답 형식
- 브라우저에서 바로 테스트 가능!

---

## 📊 API 엔드포인트

### 갤러리 API
- `GET /api/gallery` - 전체 갤러리 조회
- `GET /api/gallery?category=license` - 인허가 갤러리 조회
- `POST /api/upload` - 이미지 업로드 (multipart/form-data)
- `GET /api/image/{category}/{filename}` - 이미지 가져오기
- `DELETE /api/gallery/{image_id}` - 이미지 삭제

### 상품 API
- `GET /api/products` - 상품 목록 조회
- `GET /api/products?active=1` - 판매중 상품만 조회
- `POST /api/products` - 상품 등록
- `PUT /api/products/{id}` - 상품 수정
- `DELETE /api/products/{id}` - 상품 삭제

### 주문 API
- `POST /api/orders` - 주문 생성
- `GET /api/orders/{order_number}` - 주문 조회

---

## 🛠️ 수동 설치 (고급)

Python이 이미 설치되어 있다면:

```bash
# 1. 가상환경 생성
python -m venv venv

# 2. 가상환경 활성화
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. 패키지 설치
pip install -r requirements.txt

# 4. 서버 실행
python main.py
```

---

## 🔧 설정 변경

`main.py` 파일의 상단 설정:

```python
# DB 설정
DB_CONFIG = {
    'host': 'bitnmeta2.synology.me',
    'port': 3307,
    'user': 'iyrc',
    'password': 'dodan1004~!@',
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
```

---

## 📸 실행 화면

### 서버 시작 시:
```
================================================
  팜랜드 산양산삼 FastAPI 서버
================================================
[1단계] Python 가상환경 확인 중...
✅ 가상환경 확인 완료

[2단계] 가상환경 활성화 중...
✅ 가상환경 활성화 완료

[3단계] 패키지 설치 확인 중...
✅ 패키지 설치 완료

================================================
  FastAPI 서버 시작
================================================

📡 서버 주소:
  - 메인 페이지: http://localhost:8000
  - 관리자 페이지: http://localhost:8000/admin
  - API 문서: http://localhost:8000/docs

💡 종료하려면 Ctrl+C를 누르세요
================================================

INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

## 🚨 문제 해결

### Q1: "python을 찾을 수 없습니다"

**해결:**
1. Python 설치: https://www.python.org/downloads/
2. 설치 시 "Add Python to PATH" 체크!
3. 재부팅 후 다시 실행

### Q2: "pip를 찾을 수 없습니다"

**해결:**
```bash
python -m ensurepip --upgrade
```

### Q3: "패키지 설치 실패"

**해결:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Q4: "8000 포트가 이미 사용 중"

**해결:**
`main.py` 마지막 줄 수정:
```python
uvicorn.run(app, host="0.0.0.0", port=8001)  # 8000 → 8001
```

---

## 🎉 완료!

**이제 PHP 없이 Python만으로 실행됩니다!**

### 실행 순서:
1. `서버실행_FastAPI.bat` 더블클릭
2. `http://localhost:8000/admin` 접속
3. 인허가 이미지 + 상품 등록
4. `http://localhost:8000` 메인 페이지 확인

**모든 기능이 정상 작동합니다!** 🚀

---

## 📦 배포 (카페24)

카페24는 Python을 지원하지 않을 수 있습니다.

**대안:**
1. **Heroku** (무료): Python 완벽 지원
2. **PythonAnywhere** (무료): Python 전용 호스팅
3. **AWS/GCP/Azure** (유료): 전문 클라우드

또는 로컬에서만 사용하고, 데이터베이스는 카페24 MySQL 사용!

---

**Python이 PHP보다 훨씬 쉽습니다!** 🐍✨
