#!/bin/bash
# Bash script to run the backend locally
# Linux/Mac용 로컬 실행 스크립트

echo "================================"
echo "ClipTheNews Backend - Local Run"
echo "================================"
echo ""

# 1. Redis 확인
echo "[1/3] Redis 확인 중..."
if redis-cli ping > /dev/null 2>&1; then
    echo "✓ Redis가 실행 중입니다."
else
    echo "✗ Redis가 실행되지 않았습니다."
    echo ""
    echo "Redis를 시작하는 방법:"
    echo "  1. Docker: docker run -d -p 6379:6379 redis:7-alpine"
    echo "  2. Linux: sudo service redis-server start"
    echo "  3. Mac: brew services start redis"
    echo ""
    exit 1
fi

# 2. 가상환경 및 의존성 설치
echo ""
echo "[2/3] Python 환경 설정 중..."

if [ ! -d "venv" ]; then
    echo "가상환경 생성 중..."
    python3 -m venv venv
fi

echo "가상환경 활성화 중..."
source venv/bin/activate

echo "의존성 설치 중..."
pip install -q -r requirements.txt

# 3. 서버 실행
echo ""
echo "[3/3] 서버 시작"
echo ""
echo "================================"
echo "백엔드 서버: http://localhost:8000"
echo "API 문서: http://localhost:8000/docs"
echo ""
echo "Worker 시작 방법 (새 터미널):"
echo "  source venv/bin/activate"
echo "  python worker.py"
echo "================================"
echo ""

# 서버 실행
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
