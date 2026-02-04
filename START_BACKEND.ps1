# ClipTheNews 백엔드 빠른 시작 스크립트
# PowerShell 관리자 권한으로 실행하세요

Write-Host "================================" -ForegroundColor Cyan
Write-Host "ClipTheNews 백엔드 시작" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# 1. Redis 확인 (Docker)
Write-Host "[1/4] Redis 확인 중..." -ForegroundColor Yellow
$redisRunning = docker ps --filter "name=redis" --filter "status=running" -q 2>$null

if (-not $redisRunning) {
    Write-Host "Redis 컨테이너를 시작합니다..." -ForegroundColor Cyan
    
    # 기존 컨테이너 제거
    docker rm -f redis 2>$null | Out-Null
    
    # Redis 시작
    docker run -d -p 6379:6379 --name redis redis:7-alpine
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Redis 시작 완료" -ForegroundColor Green
        Start-Sleep -Seconds 2
    } else {
        Write-Host "✗ Redis 시작 실패" -ForegroundColor Red
        Write-Host ""
        Write-Host "해결 방법:" -ForegroundColor Yellow
        Write-Host "1. Docker Desktop 설치: https://www.docker.com/products/docker-desktop/" -ForegroundColor White
        Write-Host "2. Docker Desktop 실행" -ForegroundColor White
        Write-Host "3. 이 스크립트 다시 실행" -ForegroundColor White
        Write-Host ""
        Read-Host "계속하려면 Enter를 누르세요"
        exit 1
    }
} else {
    Write-Host "✓ Redis가 이미 실행 중입니다" -ForegroundColor Green
}

# 2. ffmpeg 확인
Write-Host ""
Write-Host "[2/4] ffmpeg 확인 중..." -ForegroundColor Yellow
$ffmpegInstalled = Get-Command ffmpeg -ErrorAction SilentlyContinue

if ($ffmpegInstalled) {
    Write-Host "✓ ffmpeg 설치됨" -ForegroundColor Green
} else {
    Write-Host "✗ ffmpeg가 설치되지 않았습니다" -ForegroundColor Red
    Write-Host ""
    Write-Host "설치 방법 (관리자 권한 PowerShell):" -ForegroundColor Yellow
    Write-Host "  choco install ffmpeg" -ForegroundColor White
    Write-Host ""
    Write-Host "또는 수동 다운로드:" -ForegroundColor Yellow
    Write-Host "  https://github.com/BtbN/FFmpeg-Builds/releases" -ForegroundColor White
    Write-Host ""
    $continue = Read-Host "계속하시겠습니까? (y/n)"
    if ($continue -ne 'y') {
        exit 1
    }
}

# 3. Python 의존성 설치
Write-Host ""
Write-Host "[3/4] Python 환경 설정 중..." -ForegroundColor Yellow
cd backend

if (-not (Test-Path "venv")) {
    Write-Host "가상환경 생성 중..." -ForegroundColor Cyan
    python -m venv venv
}

Write-Host "가상환경 활성화 중..." -ForegroundColor Cyan
.\venv\Scripts\Activate.ps1

Write-Host "의존성 설치 중..." -ForegroundColor Cyan
pip install -q -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ 의존성 설치 실패" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Python 환경 준비 완료" -ForegroundColor Green

# 4. 백엔드 서버 시작
Write-Host ""
Write-Host "[4/4] 백엔드 서버 시작" -ForegroundColor Yellow
Write-Host ""
Write-Host "================================" -ForegroundColor Green
Write-Host "백엔드 API: http://localhost:8000" -ForegroundColor Cyan
Write-Host "API 문서: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Worker 시작 방법 (새 PowerShell 창):" -ForegroundColor Yellow
Write-Host "  cd backend" -ForegroundColor White
Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "  python worker.py" -ForegroundColor White
Write-Host "================================" -ForegroundColor Green
Write-Host ""
Write-Host "Ctrl+C로 종료" -ForegroundColor Gray
Write-Host ""

# 서버 시작
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
