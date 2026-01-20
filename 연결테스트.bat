@echo off
chcp 65001 > nul
title 연결 테스트 - 팜랜드 산양산삼

echo.
echo =====================================
echo 🧪 DB/FTP 연결 테스트
echo =====================================
echo.

REM Python 설치 확인
python --version > nul 2>&1
if errorlevel 1 (
    echo ❌ Python이 설치되어 있지 않습니다
    echo.
    echo 👉 https://www.python.org/downloads/ 에서 Python을 설치하세요
    echo.
    pause
    exit /b 1
)

echo ✅ Python 설치 확인 완료
echo.

REM 필요한 패키지 설치
echo 📦 필요한 패키지 설치 중...
python -m pip install --quiet mysql-connector-python

echo.
echo =====================================
echo 🚀 연결 테스트 시작
echo =====================================
echo.

REM 테스트 실행
python test_connection.py

echo.
echo =====================================
echo 테스트 완료!
echo =====================================
echo.
pause
