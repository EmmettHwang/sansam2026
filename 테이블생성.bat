@echo off
chcp 65001 > nul
title 테이블 생성 - 팜랜드 산양산삼

echo.
echo =====================================
echo 🔧 데이터베이스 테이블 생성
echo =====================================
echo.

REM Python 설치 확인
python --version > nul 2>&1
if errorlevel 1 (
    echo ❌ Python이 설치되어 있지 않습니다
    echo.
    pause
    exit /b 1
)

echo ✅ Python 설치 확인 완료
echo.

REM 필요한 패키지 설치
echo 📦 필요한 패키지 확인 중...
python -m pip install --quiet mysql-connector-python

echo.
echo =====================================
echo 🚀 테이블 생성 시작
echo =====================================
echo.

REM 테이블 생성 실행
python create_tables.py

echo.
pause
