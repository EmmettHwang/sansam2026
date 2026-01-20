# 🌿 팜랜드 산양산삼 랜딩 페이지

치악산에서 정성으로 키운 산양산삼 판매 랜딩 사이트

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Version](https://img.shields.io/badge/Version-1.0.20260120--1530-brightgreen.svg)]()
[![License](https://img.shields.io/badge/License-Private-red.svg)]()

---

## 📌 버전 정보

**현재 버전**: `1.0.20260120-1530`

### 버전 형식
- **메이저**: 주요 기능 변경
- **마이너**: 기능 추가/수정
- **날짜시간**: YYYYMMDD-HHMM

### 버전 히스토리

#### v1.0.20260120-1530 (2026-01-20)
- ✅ FastAPI 백엔드 서버
- ✅ 갤러리 시스템 (5개 카테고리)
- ✅ 간단구매 시스템
- ✅ 드래그앤드롭 이미지 업로드
- ✅ FTP 무제한 저장
- ✅ MySQL 데이터베이스
- ✅ 모바일 반응형 디자인
- ✅ 자동 API 문서

---

## 🚀 빠른 시작

### 1️⃣ 프로젝트 클론

```bash
git clone https://github.com/EmmettHwang/sansam2026.git
cd sansam2026
```

### 2️⃣ 가상환경 생성 및 패키지 설치

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**Mac / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3️⃣ 백엔드 서버 실행

**Windows (간편):**
```bash
서버실행_FastAPI.bat (더블클릭)
```

**수동 실행:**
```bash
uvicorn main:app --reload
```

### 4️⃣ 브라우저에서 접속

- 🌐 **메인 페이지**: http://localhost:8000
- 🔧 **관리자 페이지**: http://localhost:8000/admin
- 📚 **API 문서**: http://localhost:8000/docs

---

## 🎯 핵심 기능

- ✅ **갤러리 시스템**: 재배지, 산양산삼, 선별과정, 포장, 인허가 이미지 관리
- ✅ **간단구매 시스템**: 상품 등록 → 주문 → 무통장입금
- ✅ **드래그앤드롭 업로드**: 쉬운 이미지 업로드
- ✅ **FTP 무제한 저장**: 실제 이미지는 FTP, 경로만 DB 저장
- ✅ **모바일 최적화**: 반응형 디자인
- ✅ **자동 API 문서**: FastAPI 자동 생성

---

## 📁 프로젝트 구조

```
sansam2026/
├── 🚀 서버실행_FastAPI.bat    # Windows 자동 실행
├── 🚀 서버실행_FastAPI.sh     # Mac/Linux 자동 실행
├── 🔧 main.py                 # FastAPI 백엔드
├── 📦 requirements.txt        # Python 패키지
├── 🧪 test_connection.py      # DB/FTP 연결 테스트
├── 🧪 연결테스트.bat          # 연결 테스트 실행
├── 🌐 index.html              # 메인 랜딩 페이지
├── 🔐 admin.html              # 관리자 페이지
├── 📄 privacy.html            # 개인정보처리방침
├── 📚 GitHub_실행가이드.md    # 상세 실행 가이드 ⭐
├── 📚 시작하기.md             # 빠른 시작 가이드
├── 📚 FastAPI_사용법.md       # FastAPI 상세 가이드
├── 📚 INSTALL.md              # 설치 가이드
├── css/
│   └── style.css              # 메인 스타일시트
├── js/
│   └── script.js              # 메인 JavaScript
├── database/
│   └── schema.sql             # MySQL 스키마
├── images/                    # 정적 이미지
└── .gitignore
```

---

## 🛠️ 시스템 요구사항

- **Python**: 3.8 이상
- **MySQL**: 5.7 이상
- **FTP 서버**: 접근 가능

---

## 🧪 연결 테스트 (선택사항)

백엔드 서버 실행 전에 DB와 FTP 연결을 테스트할 수 있습니다.

```bash
python test_connection.py
```

**또는 (Windows):**
```bash
연결테스트.bat (더블클릭)
```

---

## 📊 기술 스택

### 백엔드
- **FastAPI** - 고성능 Python 웹 프레임워크
- **Uvicorn** - ASGI 서버
- **MySQL** - 데이터베이스
- **FTP** - 파일 저장

### 프론트엔드
- **HTML5** - 구조
- **CSS3** - 스타일링
- **JavaScript (ES6+)** - 인터랙션

---

## 🎨 주요 기능 사용법

### 1️⃣ 인허가 갤러리 업로드

1. http://localhost:8000/admin 접속
2. **갤러리 관리** 탭 클릭
3. **인허가** 카드 선택 (5번째 카드)
4. 사업자등록증.jpg 드래그앤드롭
5. 자동 업로드 완료

### 2️⃣ 간단구매 상품 등록

1. http://localhost:8000/admin 접속
2. **간단구매 상품 관리** 탭 클릭
3. 상품 정보 입력 (상품명, 가격, 설명)
4. 상품 이미지 드래그앤드롭
5. **💾 저장** 버튼 클릭

---

## 🐛 문제 해결

### "이미지 업로드 실패" 또는 "갤러리 로드 실패"

**원인**: 백엔드 서버가 실행되지 않음

**해결**:
```bash
# Windows
서버실행_FastAPI.bat

# 수동 실행
uvicorn main:app --reload
```

### "DB 연결 실패"

**해결**: `main.py`의 DB 설정 확인
```python
DB_CONFIG = {
    'host': 'bitnmeta2.synology.me',
    'port': 3307,
    'user': 'iyrc',
    'password': 'dodan1004~!@',
    'database': 'sansam'
}
```

### "FTP 연결 실패"

**해결**: `main.py`의 FTP 설정 확인
```python
FTP_CONFIG = {
    'host': 'bitnmeta2.synology.me',
    'port': 2121,
    'user': 'ha',
    'password': 'dodan1004~',
    'base_path': '/sansam/'
}
```

---

## 📚 문서

- **[GitHub_실행가이드.md](GitHub_실행가이드.md)** - 상세 실행 가이드 ⭐ **필독!**
- **[시작하기.md](시작하기.md)** - 빠른 시작 가이드
- **[FastAPI_사용법.md](FastAPI_사용법.md)** - FastAPI 상세 가이드
- **[백엔드_테스트_가이드.md](백엔드_테스트_가이드.md)** - 테스트 가이드
- **[INSTALL.md](INSTALL.md)** - 설치 가이드

---

## 📞 연락처

- **상호**: 팜랜드
- **대표**: 신성식
- **사업자등록번호**: 621-78-00335
- **주소**: 강원도 원주시 소초면 학곡리 산88
- **전화**: 010-2512-6818
- **상담시간**: 08:00 ~ 20:00 (연중무휴)

---

## 📄 라이선스

이 프로젝트는 팜랜드 산양산삼 전용 랜딩 페이지입니다.

---

## 🤝 기여

이 프로젝트는 팜랜드 내부용입니다.

---

## ⭐ 시작하기

```bash
git clone https://github.com/EmmettHwang/sansam2026.git
cd sansam2026
서버실행_FastAPI.bat
```

**브라우저 접속:**
```
http://localhost:8000/admin
```

🎊 **완성!**
