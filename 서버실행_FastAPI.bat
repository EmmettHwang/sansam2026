@echo off
chcp 65001 > nul
echo ================================================
echo   팜랜드 산양산삼 FastAPI 서버
echo ================================================
echo.
echo [1단계] Python 가상환경 확인 중...

REM 가상환경이 있는지 확인
if not exist "venv\" (
    echo.
    echo 가상환경이 없습니다. 생성 중...
    python -m venv venv
    if errorlevel 1 (
        echo.
        echo ❌ 가상환경 생성 실패
        echo Python이 설치되어 있는지 확인하세요
        echo https://www.python.org/downloads/
        pause
        exit /b 1
    )
    echo ✅ 가상환경 생성 완료
)

echo ✅ 가상환경 확인 완료
echo.
echo [2단계] 가상환경 활성화 중...
call venv\Scripts\activate.bat

echo ✅ 가상환경 활성화 완료
echo.
echo [3단계] 패키지 설치 확인 중...

REM requirements.txt가 있으면 설치
if exist "requirements.txt" (
    echo 필요한 패키지를 설치합니다...
    pip install -q -r requirements.txt
    if errorlevel 1 (
        echo.
        echo ❌ 패키지 설치 실패
        pause
        exit /b 1
    )
    echo ✅ 패키지 설치 완료
) else (
    echo ⚠️  requirements.txt 파일이 없습니다
    echo 수동으로 패키지를 설치하세요:
    echo   pip install fastapi uvicorn python-multipart mysql-connector-python
    pause
)

echo.
echo ================================================
echo   FastAPI 서버 시작
echo ================================================
echo.
echo 📡 서버 주소:
echo   - 메인 페이지: http://localhost:8000
echo   - 관리자 페이지: http://localhost:8000/admin
echo   - API 문서: http://localhost:8000/docs
echo.
echo 💡 종료하려면 Ctrl+C를 누르세요
echo ================================================
echo.

python main.py

pause
