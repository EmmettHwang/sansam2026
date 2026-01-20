# 🚀 GitHub에 업로드하는 방법

## 📋 준비된 파일 목록

모든 파일이 준비되었습니다! 이제 GitHub에 올리기만 하면 됩니다.

```
✅ .gitignore               # Git 제외 파일
✅ README.md                # GitHub 메인 문서
✅ requirements.txt         # Python 패키지 목록
✅ main.py                  # FastAPI 백엔드
✅ admin.html               # 관리자 페이지
✅ index.html               # 메인 페이지
✅ test_connection.py       # 연결 테스트
✅ 서버실행_FastAPI.bat     # Windows 실행 파일
✅ 연결테스트.bat           # 연결 테스트 파일
✅ 모든 문서 파일
✅ css/, js/, database/, images/ 폴더
```

---

## 🎯 GitHub에 업로드하는 방법

### 방법 1: GitHub Desktop 사용 (초보자 추천)

1. **GitHub Desktop 다운로드**
   - https://desktop.github.com/

2. **GitHub에 로그인**
   - GitHub Desktop 실행
   - File → Options → Accounts → Sign in

3. **저장소 추가**
   - File → Add Local Repository
   - Choose... → `sansam2026` 폴더 선택

4. **커밋 및 푸시**
   - 왼쪽 하단에 모든 변경사항 표시됨
   - Summary: "Initial commit - 팜랜드 산양산삼 랜딩 페이지"
   - Description: "FastAPI + MySQL + FTP 기반 갤러리 시스템"
   - Commit to main 버튼 클릭
   - Push origin 버튼 클릭

---

### 방법 2: Git 명령어 사용 (개발자)

#### 1️⃣ 로컬에서 Git 초기화 (프로젝트 폴더에서)

```bash
cd sansam2026
git init
```

#### 2️⃣ 원격 저장소 연결

```bash
git remote add origin https://github.com/EmmettHwang/sansam2026.git
```

#### 3️⃣ 모든 파일 추가

```bash
git add .
```

#### 4️⃣ 커밋

```bash
git commit -m "Initial commit - 팜랜드 산양산삼 랜딩 페이지

- FastAPI 백엔드 서버
- 갤러리 시스템 (5개 카테고리)
- 간단구매 시스템
- 드래그앤드롭 이미지 업로드
- FTP 무제한 저장
- MySQL 데이터베이스
- 모바일 반응형 디자인"
```

#### 5️⃣ 푸시

```bash
# 기존 저장소가 있는 경우
git push -u origin main --force

# 또는 (저장소가 비어있는 경우)
git branch -M main
git push -u origin main
```

---

### 방법 3: GitHub 웹에서 직접 업로드 (파일 수가 적을 때)

1. https://github.com/EmmettHwang/sansam2026 접속
2. **Add file** → **Upload files** 클릭
3. 모든 파일/폴더를 드래그앤드롭
4. Commit message 입력
5. **Commit changes** 클릭

⚠️ **주의**: 파일이 많으면 시간이 오래 걸립니다. 방법 1 또는 2 추천!

---

## 🧪 업로드 확인

업로드가 완료되면:

1. https://github.com/EmmettHwang/sansam2026 접속
2. 파일 목록 확인
3. README.md가 자동으로 표시됨

---

## 🎯 다른 컴퓨터에서 클론하기

업로드가 완료되면 다른 컴퓨터에서 다음 명령어로 클론할 수 있습니다:

```bash
git clone https://github.com/EmmettHwang/sansam2026.git
cd sansam2026
```

---

## 📋 전체 Git 명령어 (처음부터 끝까지)

```bash
# 1. 프로젝트 폴더로 이동
cd sansam2026

# 2. Git 초기화
git init

# 3. 원격 저장소 연결
git remote add origin https://github.com/EmmettHwang/sansam2026.git

# 4. 모든 파일 추가
git add .

# 5. 커밋
git commit -m "Initial commit - 팜랜드 산양산삼 랜딩 페이지"

# 6. 브랜치 이름 변경 (main으로)
git branch -M main

# 7. 푸시
git push -u origin main

# 또는 (기존 저장소가 있는 경우)
git push -u origin main --force
```

---

## 🐛 문제 해결

### ❌ "remote origin already exists"

**해결**:
```bash
git remote remove origin
git remote add origin https://github.com/EmmettHwang/sansam2026.git
```

### ❌ "fatal: refusing to merge unrelated histories"

**해결**:
```bash
git pull origin main --allow-unrelated-histories
git push -u origin main
```

### ❌ "Permission denied (publickey)"

**해결**: HTTPS 사용
```bash
git remote set-url origin https://github.com/EmmettHwang/sansam2026.git
```

### ❌ "Updates were rejected"

**해결**: 강제 푸시 (주의!)
```bash
git push -u origin main --force
```

---

## 🎉 완료!

업로드가 완료되면:

1. ✅ GitHub에서 저장소 확인
2. ✅ README.md 자동 표시 확인
3. ✅ 파일 목록 확인

**이제 다른 컴퓨터에서:**
```bash
git clone https://github.com/EmmettHwang/sansam2026.git
cd sansam2026
서버실행_FastAPI.bat
```

🎊 **성공!**
