# 🚀 GitHub에서 클론하여 로컬에서 실행하기

## 📌 GitHub 저장소

```
https://github.com/EmmettHwang/sansam2026
```

---

## 🎯 1단계: Git Clone

### Windows (Git Bash 또는 명령 프롬프트)

```bash
# 프로젝트 클론
git clone https://github.com/EmmettHwang/sansam2026.git

# 프로젝트 폴더로 이동
cd sansam2026
```

### Mac / Linux (터미널)

```bash
# 프로젝트 클론
git clone https://github.com/EmmettHwang/sansam2026.git

# 프로젝트 폴더로 이동
cd sansam2026
```

---

## 🎯 2단계: Python 가상환경 생성 및 패키지 설치

### Windows

```bash
# Python 가상환경 생성
python -m venv venv

# 가상환경 활성화
venv\Scripts\activate

# 필요한 패키지 설치
pip install -r requirements.txt
```

### Mac / Linux

```bash
# Python 가상환경 생성
python3 -m venv venv

# 가상환경 활성화
source venv/bin/activate

# 필요한 패키지 설치
pip install -r requirements.txt
```

---

## 🎯 3단계: DB/FTP 연결 테스트 (선택사항)

백엔드 서버 실행 전에 DB와 FTP 연결을 테스트할 수 있습니다.

```bash
python test_connection.py
```

**또는 배치 파일 사용 (Windows):**
```bash
연결테스트.bat
```

---

## 🎯 4단계: 백엔드 서버 실행

### 방법 1: 배치 파일 사용 (Windows - 추천!)

```bash
서버실행_FastAPI.bat (더블클릭)
```

### 방법 2: 수동 실행 (Windows)

```bash
# 가상환경 활성화 (아직 안했으면)
venv\Scripts\activate

# FastAPI 서버 실행
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 방법 3: 수동 실행 (Mac / Linux)

```bash
# 가상환경 활성화 (아직 안했으면)
source venv/bin/activate

# FastAPI 서버 실행
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### ✅ 정상 실행 확인

터미널에 다음 메시지가 표시되면 성공:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using WatchFiles
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

---

## 🎯 5단계: 브라우저에서 접속

서버가 실행되면 다음 주소로 접속하세요:

### 메인 페이지
```
http://localhost:8000
```

### 관리자 페이지
```
http://localhost:8000/admin
```

### API 문서 (자동 생성)
```
http://localhost:8000/docs
```

---

## 🎨 6단계: 이미지 업로드 테스트

### 갤러리 이미지 업로드

1. http://localhost:8000/admin 접속
2. **갤러리 관리** 탭 클릭
3. 5개 카드 확인:
   - 🏞️ 재배지
   - 🌿 산양산삼
   - ⚙️ 선별과정
   - 📦 포장
   - 📄 인허가
4. 원하는 카드 선택
5. 이미지 드래그앤드롭
6. "이미지가 업로드되었습니다" 메시지 확인

### 상품 등록

1. **간단구매 상품 관리** 탭 클릭
2. 상품 정보 입력:
   - 상품명: `치악산 산양산삼 10년근`
   - 가격: `150000`
   - 설명: `치악산에서 10년간 자란 프리미엄 산양산삼`
3. 상품 이미지 드래그앤드롭
4. **💾 저장** 버튼 클릭
5. 상품 목록에서 확인

---

## 🐛 문제 해결

### ❌ "python 명령을 찾을 수 없습니다"

**원인**: Python이 설치되지 않음

**해결**:
1. https://www.python.org/downloads/ 에서 Python 3.8 이상 설치
2. 설치 시 "Add Python to PATH" 체크!

### ❌ "pip install 실패"

**원인**: pip 업그레이드 필요

**해결**:
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### ❌ "이미지 업로드 실패"

**원인**: 백엔드 서버가 실행되지 않음

**해결**:
1. 터미널에서 서버 실행 상태 확인
2. `uvicorn main:app --reload` 다시 실행

### ❌ "갤러리 로드 실패"

**원인**: 백엔드 서버가 실행되지 않음

**해결**:
1. 터미널에서 서버 실행 상태 확인
2. F12 (개발자 도구) → Console 탭에서 에러 확인

### ❌ "DB 연결 실패"

**원인**: MySQL 서버 접속 불가

**해결**:
1. MySQL 서버 실행 확인
2. `main.py`의 DB 설정 확인:
   ```python
   DB_CONFIG = {
       'host': 'bitnmeta2.synology.me',
       'port': 3307,
       'user': 'iyrc',
       'password': 'dodan1004~!@',
       'database': 'sansam'
   }
   ```
3. 방화벽에서 포트 3307 허용 확인

### ❌ "FTP 연결 실패"

**원인**: FTP 서버 접속 불가

**해결**:
1. FTP 서버 실행 확인
2. `main.py`의 FTP 설정 확인:
   ```python
   FTP_CONFIG = {
       'host': 'bitnmeta2.synology.me',
       'port': 2121,
       'user': 'ha',
       'password': 'dodan1004~',
       'base_path': '/sansam/'
   }
   ```
3. 방화벽에서 포트 2121 허용 확인

---

## 📋 전체 명령어 요약 (빠른 실행)

### Windows

```bash
# 1. 프로젝트 클론
git clone https://github.com/EmmettHwang/sansam2026.git
cd sansam2026

# 2. 가상환경 생성 및 패키지 설치
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# 3. 연결 테스트 (선택)
python test_connection.py

# 4. 서버 실행
uvicorn main:app --reload

# 또는 배치 파일 사용
서버실행_FastAPI.bat
```

### Mac / Linux

```bash
# 1. 프로젝트 클론
git clone https://github.com/EmmettHwang/sansam2026.git
cd sansam2026

# 2. 가상환경 생성 및 패키지 설치
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. 연결 테스트 (선택)
python test_connection.py

# 4. 서버 실행
uvicorn main:app --reload

# 또는 실행 스크립트 사용
chmod +x 서버실행_FastAPI.sh
./서버실행_FastAPI.sh
```

---

## 🎉 완성!

**브라우저에서 접속:**
- 메인 페이지: http://localhost:8000
- 관리자 페이지: http://localhost:8000/admin
- API 문서: http://localhost:8000/docs

**문제가 발생하면:**
1. 터미널에 표시된 에러 메시지 확인
2. 브라우저 F12 → Console 탭에서 에러 확인
3. 에러 메시지를 복사해서 질문하세요!

🎊 **성공!**
