@echo off
chcp 65001 > nul
echo ================================================
echo   팜랜드 산양산삼 FastAPI 서버
echo ================================================
echo.
echo [1단계] Conda 환경 확인 중...

REM Conda 환경 활성화
call conda activate sansam2026
if errorlevel 1 (
    echo.
    echo ❌ Conda 환경 'sansam2026'를 찾을 수 없습니다
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
echo [2단계] 패키지 설치 확인 중...

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
echo.
echo ⚠️  현재 Conda 환경: sansam2026
echo ================================================
echo.

uvicorn main:app --reload

pause
