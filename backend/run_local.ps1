# PowerShell script to run the backend locally
# Windows용 로컬 실행 스크립트

Write-Host "================================" -ForegroundColor Green
Write-Host "ClipTheNews Backend - Local Run" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host ""

# 1. Redis 확인
Write-Host "[1/3] Redis 확인 중..." -ForegroundColor Yellow
$redisRunning = $false

try {
    $redisTest = redis-cli ping 2>$null
    if ($redisTest -eq "PONG") {
        Write-Host "✓ Redis가 실행 중입니다." -ForegroundColor Green
        $redisRunning = $true
    }
} catch {
    Write-Host "✗ Redis가 실행되지 않았습니다." -ForegroundColor Red
}

if (-not $redisRunning) {
    Write-Host ""
    Write-Host "Redis를 시작하는 방법:" -ForegroundColor Cyan
    Write-Host "  1. Docker: docker run -d -p 6379:6379 redis:7-alpine" -ForegroundColor White
    Write-Host "  2. WSL: sudo service redis-server start" -ForegroundColor White
    Write-Host "  3. Windows: Redis 설치 후 redis-server 실행" -ForegroundColor White
    Write-Host ""
    exit 1
}

# 2. 가상환경 및 의존성 설치
Write-Host ""
Write-Host "[2/3] Python 환경 설정 중..." -ForegroundColor Yellow

if (-not (Test-Path "venv")) {
    Write-Host "가상환경 생성 중..." -ForegroundColor Cyan
    python -m venv venv
}

Write-Host "가상환경 활성화 중..." -ForegroundColor Cyan
.\venv\Scripts\Activate.ps1

Write-Host "의존성 설치 중..." -ForegroundColor Cyan
pip install -q -r requirements.txt

# 3. 서버 실행
Write-Host ""
Write-Host "[3/3] 서버 시작" -ForegroundColor Yellow
Write-Host ""
Write-Host "================================" -ForegroundColor Green
Write-Host "백엔드 서버: http://localhost:8000" -ForegroundColor Cyan
Write-Host "API 문서: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Worker 시작 방법 (새 터미널):" -ForegroundColor Yellow
Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "  python worker.py" -ForegroundColor White
Write-Host "================================" -ForegroundColor Green
Write-Host ""

# 서버 실행
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
