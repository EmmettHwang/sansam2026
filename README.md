# 🏔️ 팜랜드 산양산삼 랜딩 페이지

![Version](https://img.shields.io/badge/version-1.2.20260121--0615-green)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688)
![License](https://img.shields.io/badge/license-Proprietary-red)

강원도 원주에서 자연 그대로 키운 산양산삼을 소개하는 랜딩 페이지입니다.

---

## 📋 목차

- [버전 관리](#-버전-관리)
- [주요 기능](#-주요-기능)
- [기술 스택](#-기술-스택)
- [빠른 시작](#-빠른-시작)
- [서버 설정](#-서버-설정)
- [프로젝트 구조](#-프로젝트-구조)
- [API 문서](#-api-문서)
- [배포](#-배포)

---

## 📌 버전 관리

### 현재 버전: `v1.2.20260121-0615`

**⚠️ 중요: 파일 수정 시 반드시 마이너 버전(가운데 숫자)을 증가시키세요!**

### 📝 버전 포맷 및 규칙

**형식**: `메이저.마이너.날짜시간`
- **메이저** (Major): 1
- **마이너** (Minor): 0, 1, 2, 3... ✅ **수정할 때마다 증가!**
- **날짜시간**: YYYYMMDD-HHMM

**예시**:
```
v1.0.20260121-0541  (현재)
    ↓ 첫 번째 수정
v1.1.20260121-0545  (마이너 버전 0 → 1)
    ↓ 두 번째 수정
v1.2.20260121-0550  (마이너 버전 1 → 2)
    ↓ 세 번째 수정
v1.3.20260121-0555  (마이너 버전 2 → 3)
```

**규칙**:
- ✅ **코드 수정할 때마다 마이너 버전을 1 증가** (0→1→2→3...)
- ✅ 날짜시간은 실제 수정 시간으로 업데이트
- ✅ 메이저 버전(1)은 대규모 업데이트 시에만 변경

### 📝 버전 업데이트 대상 파일

**매 수정마다 아래 4개 파일을 함께 업데이트:**

1. **README.md** (3번째 줄 + 27번째 줄)
   ```markdown
   ![Version](https://img.shields.io/badge/version-1.X.YYYYMMDD--HHMM-green)
   ### 현재 버전: `v1.X.YYYYMMDD-HHMM`
   ```

2. **main.py** (15-16번째 줄)
   ```python
   VERSION = "1.X.YYYYMMDD-HHMM"  # X는 마이너 버전 (0, 1, 2, 3...)
   VERSION_DATE = "YYYY-MM-DD HH:MM"  # 실제 수정 시간
   ```

3. **index.html** (Footer 부분 + CSS/JS 쿼리)
   ```html
   <span id="versionInfo">v1.X.YYYYMMDD-HHMM</span>
   <link rel="stylesheet" href="css/style.css?v=YYYYMMDD-HHMM">
   <script src="js/script.js?v=YYYYMMDD-HHMM"></script>
   ```

4. **admin.html** (Footer 부분)
   ```html
   <span>v1.X.YYYYMMDD-HHMM</span>
   ```

### 🔄 버전 업데이트 예시

```bash
# 현재 시간 확인
date  # 2026-01-21 05:45

# 현재 버전: v1.0.20260121-0541
# 첫 수정 후: v1.1.20260121-0545  ← 마이너 버전 0→1
# 두 번째 수정: v1.2.20260121-0550  ← 마이너 버전 1→2
# 세 번째 수정: v1.3.20260121-0555  ← 마이너 버전 2→3
```

### 🎯 빠른 체크리스트

수정 완료 후:
- [ ] 마이너 버전 증가 확인 (예: 0→1, 1→2, 2→3)
- [ ] 날짜시간 업데이트 확인
- [ ] 4개 파일 모두 업데이트 확인
  - [ ] README.md
  - [ ] main.py
  - [ ] index.html
  - [ ] admin.html
# → v1.0.20260121-0300
```

**매 수정마다 버전을 올려야 추적이 쉽습니다!**
- [문의](#-문의)

---

## ✨ 주요 기능

### 🖼️ 갤러리 관리
- **드래그 앤 드롭** 이미지 업로드
- **FTP 자동 저장** (무제한 용량)
- **로컬 캐시 시스템** (첫 로드 후 빠른 표시)
- **5개 카테고리**: 재배지, 산양산삼, 선별과정, 포장, 인허가
- **대표 이미지** 자동 설정
- **실시간 썸네일** 미리보기

### 🛒 간단구매
- 상품 등록/수정/삭제
- 이미지 업로드
- 재고 관리 (기본 999개)
- 주문 시스템
- **무통장 입금** 안내

### 📄 인허가 관리
- 사업자등록증 업로드
- 인증서 관리
- 메인 페이지 자동 표시

### 📱 반응형 디자인
- 모바일 최적화
- 터치 제스처 지원
- 플로팅 전화 버튼

---

## 🛠️ 기술 스택

### 백엔드
- **FastAPI** 0.104.1 - 고성능 Python 웹 프레임워크
- **MySQL** 8.2.0 - 데이터베이스
- **FTP** - 이미지 파일 저장
- **Uvicorn** - ASGI 서버

### 프론트엔드
- **HTML5** / **CSS3** / **JavaScript**
- Vanilla JS (프레임워크 없음)
- 반응형 디자인

### 인프라
- **MySQL**: bitnmeta2.synology.me:3307
- **FTP**: bitnmeta2.synology.me:2121
- **저장 경로**: /homes/ha/sansam/

---

## 🚀 빠른 시작

### 1️⃣ 프로젝트 클론

```bash
git clone https://github.com/EmmettHwang/sansam2026.git
cd sansam2026
```

### 2️⃣ Conda 가상환경 활성화

**이 프로젝트는 Conda 가상환경을 사용합니다.**

```bash
# Conda 환경 활성화
conda activate sansam2026

# 패키지 설치
pip install -r requirements.txt
```

**환경이 없는 경우 생성:**
```bash
conda create -n sansam2026 python=3.8
conda activate sansam2026
pip install -r requirements.txt
```

### 3️⃣ 서버 설정 (초기 1회만)

**Windows:**
```cmd
서버설정.bat
```

**메뉴 선택**: `1` (전체 초기 설정)

→ FTP 폴더 생성 + DB 테이블 생성 자동 완료!

### 4️⃣ 백엔드 서버 실행

**⚠️ 중요: 반드시 conda 환경을 활성화한 후 실행하세요!**

```bash
# 1. Conda 환경 활성화
conda activate sansam2026

# 2. 서버 실행
uvicorn main:app --reload
```

**Windows 배치 파일:**
```cmd
서버실행_FastAPI.bat
```

**Mac/Linux:**
```bash
chmod +x 서버실행_FastAPI.sh
./서버실행_FastAPI.sh
```

### 5️⃣ 브라우저 접속

- **메인 페이지**: http://localhost:8000
- **관리자 페이지**: http://localhost:8000/admin
- **API 문서**: http://localhost:8000/docs

---

## ⚙️ 서버 설정

### 📦 server_setup.py (올인원 통합 스크립트)

**실행:**
```cmd
서버설정.bat
```

**메뉴:**
```
1. 🚀 전체 초기 설정 (FTP + DB 테이블 생성)
2. 📁 FTP 폴더 생성
3. 📂 FTP 파일 목록 확인
4. 💾 DB 테이블 생성
5. 📊 DB 이미지 목록 확인
6. 🧹 DB 이미지 데이터 삭제
7. 🔍 전체 상태 확인 (FTP + DB)
0. 🚪 종료
```

### 🔧 설정 정보

**FTP 설정 (main.py):**
```python
FTP_CONFIG = {
    'host': 'bitnmeta2.synology.me',
    'port': 2121,
    'user': 'ha',
    'password': 'dodan1004~',
    'base_path': '/homes/ha/sansam/'
}
```

**DB 설정 (main.py):**
```python
DB_CONFIG = {
    'host': 'bitnmeta2.synology.me',
    'port': 3307,
    'user': 'iyrc',
    'password': 'Dodan1004!',
    'database': 'sansam'
}
```

---

## 📁 프로젝트 구조

```
sansam2026/
├── css/
│   └── style.css              # 메인 스타일
├── database/
│   └── schema.sql             # DB 스키마
├── images/                    # 로컬 이미지 (placeholder)
├── js/
│   └── script.js              # 메인 JavaScript
├── index.html                 # 메인 페이지
├── admin.html                 # 관리자 페이지
├── privacy.html               # 개인정보처리방침
├── main.py                    # FastAPI 백엔드
├── server_setup.py            # 서버 설정 통합 스크립트
├── requirements.txt           # Python 패키지
├── 서버설정.bat               # 서버 설정 실행 (Windows)
├── 서버실행_FastAPI.bat       # 백엔드 실행 (Windows)
├── 서버실행_FastAPI.sh        # 백엔드 실행 (Mac/Linux)
├── favicon.svg                # 파비콘 (山 한자)
├── .gitignore                 # Git 제외 파일
└── README.md                  # 이 파일
```

---

## 📡 API 문서

### 갤러리 API

#### GET /api/gallery
갤러리 이미지 목록 조회

**Query Parameters:**
- `category` (optional): farm, ginseng, process, package, license

**Response:**
```json
{
  "success": true,
  "categories": [
    {
      "category": "farm",
      "name": "재배지",
      "icon": "🏞️",
      "count": 2,
      "representative": "/api/image/farm/image_xxx.jpg",
      "images": [...]
    }
  ]
}
```

#### POST /api/upload
이미지 업로드 (다중 파일 지원)

**Form Data:**
- `category`: 카테고리 (farm, ginseng, process, package, license)
- `images`: 이미지 파일들 (jpg, jpeg, png, gif, webp)

**Response:**
```json
{
  "success": true,
  "message": "2장 업로드 성공, 0장 실패",
  "data": {
    "uploaded": [...],
    "errors": []
  }
}
```

#### DELETE /api/gallery/{image_id}
이미지 삭제

**Response:**
```json
{
  "success": true,
  "message": "이미지가 삭제되었습니다"
}
```

#### GET /api/image/{category}/{filename}
이미지 파일 가져오기 (FTP에서)

### 상품 API

#### GET /api/products
상품 목록 조회

**Query Parameters:**
- `active` (optional): 0 (전체), 1 (활성화만)

#### POST /api/products
상품 등록

**Body:**
```json
{
  "name": "치악산 산양산삼 10년근",
  "description": "설명",
  "price": 150000,
  "image_path": "/homes/ha/sansam/...",
  "stock": 999,
  "display_order": 0,
  "is_active": 1
}
```

#### PUT /api/products/{product_id}
상품 수정

#### DELETE /api/products/{product_id}
상품 삭제

### 버전 API

#### GET /api/version
버전 정보 조회

**Response:**
```json
{
  "success": true,
  "version": "1.0.20260121-0220",
  "version_date": "2026-01-21 02:20",
  "description": "팜랜드 산양산삼 랜딩 페이지 v1.0"
}
```

---

## 🚀 배포

### GitHub에 푸시

```bash
git add .
git commit -m "Update: 설명"
git push origin main
```

### 프로덕션 배포

**Publish 탭**에서 배포하거나, 별도 호스팅 서버에 배포하세요.

---

## 📊 데이터베이스 스키마

### gallery_images
```sql
CREATE TABLE gallery_images (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category VARCHAR(50) NOT NULL,
    filename VARCHAR(255) NOT NULL,
    original_name VARCHAR(255),
    file_path VARCHAR(500) NOT NULL,
    file_size INT,
    is_representative TINYINT(1) DEFAULT 0,
    display_order INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### products
```sql
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price INT NOT NULL,
    image_path VARCHAR(500) NOT NULL,
    stock INT DEFAULT 999,
    display_order INT DEFAULT 0,
    is_active TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### orders
```sql
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_number VARCHAR(50) UNIQUE NOT NULL,
    product_id INT NOT NULL,
    product_name VARCHAR(200) NOT NULL,
    product_price INT NOT NULL,
    quantity INT NOT NULL,
    total_price INT NOT NULL,
    customer_name VARCHAR(100) NOT NULL,
    customer_phone VARCHAR(20) NOT NULL,
    customer_email VARCHAR(255),
    delivery_address TEXT NOT NULL,
    delivery_message TEXT,
    payment_status VARCHAR(20) DEFAULT 'pending',
    order_status VARCHAR(20) DEFAULT 'ordered',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);
```

---

## 🔧 문제 해결

### 1. 이미지 업로드 실패
```cmd
서버설정.bat
메뉴 선택: 7 (전체 상태 확인)
```

### 2. DB 연결 실패
`main.py`의 DB_CONFIG 확인

### 3. FTP 연결 실패
`main.py`의 FTP_CONFIG 확인

### 4. 서버가 시작되지 않음
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

---

## 📞 문의

**팜랜드 산양산삼**

- 📞 **전화**: 010-2512-6818
- 📍 **주소**: 강원도 원주시 소초면 학곡리 산88
- 🕐 **상담시간**: 08:00 ~ 20:00 (연중무휴)
- 👤 **대표**: 신성식
- 🏢 **사업자등록번호**: 621-78-00335

---

## 📝 라이선스

이 프로젝트는 팜랜드 산양산삼 전용 랜딩 페이지입니다.

---

## 🎉 버전 정보

**현재 버전**: v1.0.20260121-0510

### ✅ 완료된 기능
- FastAPI 백엔드 구현
- FTP 이미지 저장 (`/homes/ha/sansam/`)
- 로컬 이미지 캐시 시스템
- 갤러리 관리 (5개 카테고리: 재배지, 산양산삼, 선별과정, 포장, 인허가)
- 간단구매 시스템 (상품 등록/조회/수정/삭제)
- 무통장 입금 안내
- Trust Grid 동적 로드
- 모바일 최적화
- 관리자 페이지 (드래그 앤 드롭 업로드)
- 서버 설정 통합 스크립트
- 파비콘 (山 한자)
- 사업자 정보 추가

### 🎯 다음 단계
- 갤러리 이미지 업로드 (재배지, 산양산삼, 선별과정, 포장, 인허가)
- 메인 페이지 최종 점검
- Live 카메라 추가 (IP카메라 주소 확보 후)
- GitHub 배포

---

**Made with ❤️ by 팜랜드 산양산삼**
