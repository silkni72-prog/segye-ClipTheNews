# ClipTheNews Worker 시작 스크립트

Write-Host "================================" -ForegroundColor Cyan
Write-Host "ClipTheNews Worker 시작" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

cd backend

# 가상환경 활성화
if (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "가상환경 활성화 중..." -ForegroundColor Yellow
    .\venv\Scripts\Activate.ps1
} else {
    Write-Host "✗ 가상환경을 찾을 수 없습니다" -ForegroundColor Red
    Write-Host "먼저 START_BACKEND.ps1을 실행하세요" -ForegroundColor Yellow
    Read-Host "계속하려면 Enter를 누르세요"
    exit 1
}

Write-Host ""
Write-Host "Worker 시작 중..." -ForegroundColor Yellow
Write-Host "Ctrl+C로 종료" -ForegroundColor Gray
Write-Host ""

# Worker 실행
python worker.py
