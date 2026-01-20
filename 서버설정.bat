@echo off
chcp 65001 > nul
cls

echo.
echo ============================================================
echo  🏔️  팜랜드 산양산삼 서버 설정
echo ============================================================
echo.

REM Conda 환경 활성화
echo 🔧 Conda 환경 활성화 중...
call conda activate sansam2026
if errorlevel 1 (
    echo ❌ Conda 환경 'sansam2026'를 찾을 수 없습니다!
    echo.
    echo 환경을 생성하려면 아래 명령을 실행하세요:
    echo   conda create -n sansam2026 python=3.8
    echo   conda activate sansam2026
    echo   pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo ✅ Conda 환경 'sansam2026' 활성화 완료
echo.

REM 필요한 패키지 확인
echo 📦 필요한 패키지 확인 중...
python -c "import mysql.connector" 2>nul
if errorlevel 1 (
    echo 📦 mysql-connector-python 설치 중...
    pip install mysql-connector-python
)
echo ✅ 패키지 확인 완료
echo.

REM 서버 설정 실행
python server_setup.py

pause
