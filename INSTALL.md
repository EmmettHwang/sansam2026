# 팜랜드 산양산삼 - 통합 시스템 설치 가이드

## 🎯 시스템 개요

**갤러리 + 간단구매 + 주문 관리 통합 시스템!**

### 주요 기능
- ✅ **갤러리 시스템** - 드래그앤드롭 업로드, 무제한 용량
- ✅ **인허가 갤러리** - 사업자등록증, 인증서 관리
- ✅ **간단구매** - 상품 등록 + 주문 시스템
- ✅ **무통장입금** - 계좌 안내 + 주문번호 발급
- ✅ **FTP 저장** - 실제 파일은 FTP, DB는 경로만
- ✅ **모바일 최적화** - 반응형 디자인

---

## 📋 시스템 요구사항

### 서버
- **PHP 7.4 이상**
- **MySQL 5.7 이상**
- **FTP 서버** (이미 있음: bitnmeta2.synology.me)
- **카페24 호스팅** 또는 **자체 서버**

### 제공된 정보
```
DB_HOST=bitnmeta2.synology.me
DB_PORT=3307
DB_USER=iyrc
DB_PASSWORD=dodan1004~!@
DB_NAME=sansam

FTP_HOST=bitnmeta2.synology.me
FTP_PORT=2121
FTP_USER=ha
FTP_PASSWORD=dodan1004~
FTP_PATH=/sansam/
```

---

## 🚀 설치 단계

### 1단계: 자동 데이터베이스 설정 (3분)

#### 방법 A: 브라우저 자동 설치 (권장)
```
https://도메인/database/init_db.php
```
접속하면:
1. ✅ DB 연결 테스트
2. ✅ 테이블 자동 생성 (gallery_images, products, orders)
3. ✅ 기본 카테고리 설정 (재배지/산양산삼/선별과정/포장/인허가)
4. ✅ 초기화 완료 메시지

**⚠️ 완료 후 반드시 `init_db.php` 파일을 삭제하세요!**

#### 방법 B: 수동 설치
```bash
mysql -h bitnmeta2.synology.me -P 3307 -u iyrc -p
# 비밀번호 입력: dodan1004~!@
```

#### 1-2. 데이터베이스 생성 (이미 있다면 건너뛰기)
```sql
CREATE DATABASE IF NOT EXISTS sansam CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE sansam;
```

#### 1-3. 테이블 생성
`database/schema.sql` 파일의 내용을 실행:
```bash
mysql -h bitnmeta2.synology.me -P 3307 -u iyrc -p sansam < database/schema.sql
```

또는 MySQL 클라이언트에서 직접 실행:
```sql
-- gallery_images 테이블 생성
CREATE TABLE IF NOT EXISTS `gallery_images` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `category` VARCHAR(50) NOT NULL,
    `filename` VARCHAR(255) NOT NULL,
    `original_name` VARCHAR(255) NOT NULL,
    `file_path` VARCHAR(500) NOT NULL,
    `file_size` INT NOT NULL,
    `width` INT DEFAULT NULL,
    `height` INT DEFAULT NULL,
    `is_representative` TINYINT(1) DEFAULT 0,
    `display_order` INT DEFAULT 0,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX `idx_category` (`category`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- gallery_categories 테이블 생성
CREATE TABLE IF NOT EXISTS `gallery_categories` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `code` VARCHAR(50) NOT NULL UNIQUE,
    `name` VARCHAR(100) NOT NULL,
    `icon` VARCHAR(50) DEFAULT NULL,
    `display_order` INT DEFAULT 0,
    `is_active` TINYINT(1) DEFAULT 1,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX `idx_code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 기본 카테고리 데이터
INSERT INTO `gallery_categories` (`code`, `name`, `icon`, `display_order`) VALUES
('farm', '재배지', '🏞️', 1),
('ginseng', '산양산삼', '🌿', 2),
('process', '선별과정', '⚙️', 3),
('package', '포장', '📦', 4);
```

---

### 2단계: FTP 폴더 생성 (2분)

FTP 클라이언트(FileZilla 등)로 접속:
- Host: bitnmeta2.synology.me
- Port: 2121
- Username: ha
- Password: dodan1004~

폴더 구조 생성:
```
/sansam/
  ├── farm/       (재배지)
  ├── ginseng/    (산양산삼)
  ├── process/    (선별과정)
  └── package/    (포장)
```

---

### 3단계: 파일 업로드 (10분)

#### 카페24에 업로드할 파일들:
```
farmland-server/
├── api/
│   ├── config.php        # 설정 파일
│   ├── upload.php        # 업로드 API
│   ├── gallery.php       # 조회 API
│   └── delete.php        # 삭제 API
├── admin-server.php      # 관리자 페이지 (NEW!)
├── index.html            # 메인 페이지
├── privacy.html          # 개인정보처리방침
├── css/
│   └── style.css
└── js/
    └── script.js
```

#### 업로드 방법:
1. FTP로 카페24 서버 접속
2. 위 파일들을 루트 또는 `/farmland/` 폴더에 업로드
3. `api/` 폴더 권한 확인: 755

---

### 4단계: 설정 확인 (3분)

#### 4-1. config.php 확인
`api/config.php` 파일을 열고 설정이 맞는지 확인:
```php
define('DB_HOST', 'bitnmeta2.synology.me');
define('DB_PORT', '3307');
define('DB_USER', 'iyrc');
define('DB_PASSWORD', 'dodan1004~!@');
define('DB_NAME', 'sansam');

define('FTP_HOST', 'bitnmeta2.synology.me');
define('FTP_PORT', 2121);
define('FTP_USER', 'ha');
define('FTP_PASSWORD', 'dodan1004~');
define('FTP_BASE_PATH', '/sansam/');
```

#### 4-2. PHP 확장 모듈 확인
카페24 관리자 > PHP 설정에서 다음 확인:
- ✅ `pdo_mysql` - 활성화
- ✅ `ftp` - 활성화
- ✅ `gd` - 활성화

---

### 5단계: 테스트 (5분)

#### 5-1. 관리자 페이지 접속
```
https://your-domain.com/admin-server.php
```

시스템 정보가 표시되는지 확인:
- ✅ DB: bitnmeta2.synology.me:3307
- ✅ FTP: bitnmeta2.synology.me:2121

#### 5-2. 이미지 업로드 테스트
1. 재배지 카테고리에 이미지 1장 드래그
2. "업로드 중..." 로딩 표시 확인
3. 업로드 완료 메시지 확인
4. FTP에서 `/sansam/farm/` 폴더 확인

#### 5-3. 메인 페이지 확인
```
https://your-domain.com/index.html
```
- 갤러리에 업로드한 이미지가 표시되는지 확인
- 클릭 시 Lightbox 슬라이드쇼 확인

---

## 🔧 문제 해결 (Troubleshooting)

### 문제 1: "DB 연결에 실패했습니다"
**원인:** MySQL 연결 실패

**해결:**
1. MySQL 서버 실행 여부 확인
```bash
mysql -h bitnmeta2.synology.me -P 3307 -u iyrc -p
```
2. 방화벽 확인 (3307 포트)
3. `api/config.php`의 DB 정보 재확인

---

### 문제 2: "FTP 연결에 실패했습니다"
**원인:** FTP 연결 실패

**해결:**
1. FTP 서버 실행 여부 확인
2. FileZilla로 수동 접속 테스트
3. 포트 2121 방화벽 확인
4. `api/config.php`의 FTP 정보 재확인

---

### 문제 3: "업로드된 파일이 없습니다"
**원인:** 파일 업로드 실패

**해결:**
1. PHP `upload_max_filesize` 확인 (최소 10MB)
```php
// php.ini
upload_max_filesize = 10M
post_max_size = 10M
```
2. FTP 폴더 권한 확인 (쓰기 가능)
3. 이미지 파일 형식 확인 (JPG, PNG, GIF만 허용)

---

### 문제 4: "갤러리 로드 실패"
**원인:** API 접근 불가

**해결:**
1. `api/gallery.php` 파일 존재 여부 확인
2. 브라우저 개발자 도구 > 네트워크 탭 확인
3. CORS 오류 시 `.htaccess` 추가:
```apache
<IfModule mod_headers.c>
    Header set Access-Control-Allow-Origin "*"
</IfModule>
```

---

## 📊 데이터 구조

### gallery_images 테이블
| 필드 | 타입 | 설명 |
|------|------|------|
| id | INT | 고유 ID (자동 증가) |
| category | VARCHAR(50) | 카테고리 코드 |
| filename | VARCHAR(255) | 저장된 파일명 |
| original_name | VARCHAR(255) | 원본 파일명 |
| file_path | VARCHAR(500) | FTP 전체 경로 |
| file_size | INT | 파일 크기 (bytes) |
| width | INT | 이미지 너비 |
| height | INT | 이미지 높이 |
| is_representative | TINYINT(1) | 대표 이미지 여부 |
| display_order | INT | 표시 순서 |
| created_at | TIMESTAMP | 생성 시간 |

---

## 🎯 사용 방법

### 이미지 업로드
1. `admin-server.php` 접속
2. 카테고리별로 이미지 드래그앤드롭
3. 자동으로 FTP + DB에 저장
4. 메인 페이지에서 즉시 확인

### 이미지 삭제
1. 관리자 페이지에서 이미지 위에 마우스 오버
2. ✕ 버튼 클릭
3. FTP + DB에서 자동 삭제

### 대표 이미지 변경
- 첫 번째 이미지가 자동으로 대표 이미지
- 순서 변경 원하면 DB에서 `display_order` 수정

---

## 🔐 보안 권장사항

### 1. 관리자 페이지 보호
`admin-server.php`를 `/admin/` 폴더로 이동:
```
/admin/
  └── index.php (admin-server.php 이름 변경)
```

`.htaccess`로 비밀번호 보호:
```apache
AuthType Basic
AuthName "Admin Area"
AuthUserFile /path/to/.htpasswd
Require valid-user
```

### 2. DB 비밀번호 별도 관리
`api/config.php`를 웹 루트 밖으로 이동:
```
/home/your-account/
  ├── config.php  (웹 루트 밖)
  └── public_html/
      └── api/
```

### 3. FTP 비밀번호 암호화
환경 변수 또는 별도 설정 파일 사용

---

## 📞 지원

문제가 계속되면:
1. `api/config.php` 파일 재확인
2. DB 테이블 생성 확인
3. FTP 폴더 생성 확인
4. PHP 에러 로그 확인

---

**✅ 설치 완료!**

이제 어디서나 접근 가능한 서버 기반 갤러리 시스템을 사용할 수 있습니다! 🎉
