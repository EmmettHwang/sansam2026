# 팜랜드 산양산삼 랜딩 페이지

![Version](https://img.shields.io/badge/version-1.3.20260128--2354-green)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688)
![License](https://img.shields.io/badge/license-Proprietary-red)

강원도 원주에서 자연 그대로 키운 산양산삼을 소개하는 랜딩 페이지입니다.

**도메인**: https://wonjusansam.co.kr

---

## 버전 히스토리

### v1.3.20260128-2354 (현재)

#### 새로운 기능
- **PC 전화/문자 모달**: PC에서 전화/문자 버튼 클릭 시 예쁜 모달로 안내
  - 전화번호 복사 버튼
  - 상담시간 안내
  - 배경 블러 효과
  - ESC 키/배경 클릭으로 닫기

#### 개선사항
- **간단구매 UI**: admin "등록된 상품"과 동일한 스타일로 통일
  - 그리드 레이아웃 (minmax 250px)
  - 카드 스타일 (흰 배경, 테두리, 둥근 모서리)
  - 버튼 스타일 개선
- **갤러리 슬라이더**: 자동 재생 제거, 수동 조작만 가능
  - 터치 스와이프 지원
  - 마우스 드래그 지원
- **타임랩스 플레이어**: 크기 축소 (50%), 프레임리스 디자인

#### 인프라
- **이미지 캐싱**: 모든 카테고리 이미지 로컬 캐시
  - products: 600px
  - gallery: 1000px
  - live: 1280px
- **OG 이미지**: URL 미리보기 이미지 관리 기능 (admin)

### v1.2.20260121-0615
- 초기 FastAPI 백엔드 구현
- 갤러리 관리 시스템
- 간단구매 시스템
- FTP 이미지 저장

---

## 주요 기능

### 갤러리 관리
- **드래그 앤 드롭** 이미지 업로드
- **FTP 자동 저장** (외부 NAS)
- **로컬 캐시 시스템** (빠른 로딩)
- **5개 카테고리**: 재배지, 산양산삼, 선별과정, 포장, 인허가
- **대표 이미지** 자동 설정

### 간단구매
- 상품 등록/수정/삭제
- admin 스타일 카드 레이아웃
- 구매하기/문의하기 버튼

### Live 타임랩스
- FTP에서 이미지 자동 로드
- 재생/일시정지/속도 조절
- 프레임 단위 이동

### 반응형 디자인
- 모바일 최적화
- 터치 제스처 지원
- PC 전화/문자 모달

---

## 기술 스택

### 백엔드
- **FastAPI** - Python 웹 프레임워크
- **MariaDB** - 데이터베이스 (localhost:3306)
- **FTP** - 이미지 저장 (bitnmeta2.synology.me:2121)
- **Uvicorn** - ASGI 서버

### 프론트엔드
- **HTML5 / CSS3 / Vanilla JavaScript**
- 반응형 디자인
- CSS 애니메이션

### 인프라
- **Nginx** - 리버스 프록시 + SSL
- **Let's Encrypt** - SSL 인증서
- **Certbot** - 인증서 자동 갱신

---

## 서버 설정

### 데이터베이스 (MariaDB)
```
Host: localhost
Port: 3306
User: iyrc
Database: sansam
```

### FTP (외부 NAS)
```
Host: bitnmeta2.synology.me
Port: 2121
User: ha
Base Path: /homes/ha/sansam/
```

### Nginx
```
/etc/nginx/sites-available/sansam
→ wonjusansam.co.kr → localhost:8001
```

---

## 실행 방법

```bash
# 서버 실행
cd /usr/sansam
uvicorn main:app --host 0.0.0.0 --port 8001 --reload

# 또는 nohup으로 백그라운드 실행
nohup uvicorn main:app --host 0.0.0.0 --port 8001 --reload > /var/log/sansam.log 2>&1 &
```

---

## 프로젝트 구조

```
/usr/sansam/
├── main.py              # FastAPI 백엔드
├── index.html           # 메인 페이지
├── admin.html           # 관리자 페이지
├── privacy.html         # 개인정보처리방침
├── css/
│   ├── style.css        # 메인 스타일
│   └── live-player.css  # 타임랩스 플레이어 스타일
├── js/
│   └── script.js        # 메인 JavaScript
├── images/
│   ├── cache/           # 리사이즈된 이미지 캐시
│   └── og-preview.jpg   # OG 미리보기 이미지
└── favicon.svg          # 파비콘
```

---

## API 엔드포인트

| Method | Endpoint | 설명 |
|--------|----------|------|
| GET | /api/version | 버전 정보 |
| GET | /api/gallery | 갤러리 목록 |
| POST | /api/upload | 이미지 업로드 |
| DELETE | /api/gallery/{id} | 이미지 삭제 |
| GET | /api/products | 상품 목록 |
| POST | /api/products | 상품 등록 |
| PUT | /api/products/{id} | 상품 수정 |
| DELETE | /api/products/{id} | 상품 삭제 |
| GET | /api/live/images | 타임랩스 이미지 |
| POST | /api/og-image | OG 이미지 업로드 |

---

## 문의

**팜랜드 산양산삼**
- 전화: 010-2512-6818
- 주소: 강원도 원주시 소초면 학곡리 산88
- 상담시간: 08:00 ~ 20:00 (연중무휴)
- 대표: 신성식
- 사업자등록번호: 621-78-00335

---

**Made with love by 팜랜드 산양산삼**
