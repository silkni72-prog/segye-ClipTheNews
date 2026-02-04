# ClipTheNews - 빠른 시작 가이드

뉴스 기사를 20초 세로 숏폼 영상으로 자동 변환하는 시스템입니다.

## 🚀 가장 빠른 시작 (Docker)

### 1. 사전 준비

- Docker Desktop 설치 및 실행
- (선택) OpenAI API 키 준비

### 2. 실행

```bash
# 프로젝트 루트에서
docker-compose up -d
```

### 3. 확인

- **API 서버**: http://localhost:8000
- **API 문서**: http://localhost:8000/docs

### 4. 테스트

```bash
# Python 테스트 스크립트
python test_api.py

# 또는 curl
curl -X POST http://localhost:8000/jobs \
  -H "Content-Type: application/json" \
  -d '{"article_url": "https://www.nytimes.com/...", "mode": "nyt_question"}'
```

---

## 📦 로컬 실행 (Windows)

### 1. Redis 시작

```powershell
docker run -d -p 6379:6379 redis:7-alpine
```

### 2. 백엔드 실행

```powershell
cd backend
.\run_local.ps1
```

### 3. Worker 시작 (새 터미널)

```powershell
cd backend
.\venv\Scripts\Activate.ps1
python worker.py
```

---

## 🍎 로컬 실행 (Mac/Linux)

### 1. Redis 시작

```bash
# Docker
docker run -d -p 6379:6379 redis:7-alpine

# 또는 Mac
brew services start redis

# 또는 Linux
sudo service redis-server start
```

### 2. 백엔드 실행

```bash
cd backend
chmod +x run_local.sh
./run_local.sh
```

### 3. Worker 시작 (새 터미널)

```bash
cd backend
source venv/bin/activate
python worker.py
```

---

## 🎯 API 사용법

### 1. 작업 생성

```bash
POST http://localhost:8000/jobs
Content-Type: application/json

{
  "article_url": "https://www.nytimes.com/...",
  "mode": "nyt_question"
}
```

**응답**:
```json
{
  "job_id": "abc123",
  "status": "queued",
  "message": "작업이 대기열에 추가되었습니다."
}
```

### 2. 상태 확인

```bash
GET http://localhost:8000/status/{job_id}
```

### 3. 결과 조회

```bash
GET http://localhost:8000/result/{job_id}
```

### 4. 영상 다운로드

```bash
GET http://localhost:8000/download/{filename}
```

또는 브라우저에서:
```
http://localhost:8000/download/abc123.mp4
```

---

## 📝 모드 설명

### `nyt_question` (질문형)
- 호기심을 자극하는 질문으로 시작
- NYT 스타일의 인게이지먼트 중심
- 예: "이 뉴스 들어보셨나요?"

### `guardian_observe` (관찰형)
- 현상 묘사 및 분석적 접근
- Guardian 스타일의 심층 분석
- 예: "최근 이런 현상이 관찰되고 있습니다."

---

## 🛠️ 문제 해결

### Redis 연결 실패
```bash
# Redis 시작 확인
redis-cli ping
# 응답: PONG

# Docker로 Redis 시작
docker run -d -p 6379:6379 redis:7-alpine
```

### ffmpeg 없음
```bash
# Windows
choco install ffmpeg

# Mac
brew install ffmpeg

# Linux
sudo apt-get install ffmpeg
```

### Worker가 작업을 안 함
1. Worker가 실행 중인지 확인
2. Redis 연결 확인
3. 로그 확인

---

## 📚 상세 문서

- **백엔드 상세**: [BACKEND_README.md](BACKEND_README.md)
- **배포 가이드**: [DEPLOYMENT.md](DEPLOYMENT.md)

---

## 🎬 처리 시간

- **평균**: 30-60초
- **단계**:
  1. 기사 파싱 (5-10초)
  2. 스크립트 생성 (3-5초)
  3. 음성 합성 (5-10초)
  4. 영상 렌더링 (15-35초)

---

## ⚙️ 시스템 요구사항

### 필수
- Python 3.11+
- Redis 7+
- ffmpeg

### 권장
- 4GB RAM
- 2 CPU cores
- 10GB 디스크 (임시 파일용)

---

## 🔑 환경 변수 (선택)

```bash
# backend/.env
OPENAI_API_KEY=sk-...          # AI 스크립트 생성 (선택)
REDIS_HOST=localhost
REDIS_PORT=6379
```

---

## 📞 지원

문제가 발생하면:
1. 로그 확인
2. [BACKEND_README.md](BACKEND_README.md)의 문제 해결 섹션 참고
3. GitHub Issues 등록

---

**Enjoy creating shorts! 🎥**
