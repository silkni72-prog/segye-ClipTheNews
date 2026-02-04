# ClipTheNews Backend

뉴스 기사 URL을 20초 세로 숏폼 영상(1080x1920 mp4)으로 자동 변환하는 FastAPI 백엔드입니다.

## 주요 기능

- ✅ **백그라운드 작업 처리**: Redis + RQ로 비동기 영상 생성
- ✅ **뉴스 파싱**: NYTimes, Guardian 등 주요 뉴스 사이트 지원
- ✅ **AI 스크립트 생성**: 20초 분량 숏폼 스크립트 자동 생성
- ✅ **음성 합성**: edge-tts를 사용한 한국어 TTS
- ✅ **영상 렌더링**: ffmpeg 기반 1080x1920 세로 영상 생성
- ✅ **자막**: 하단 25% 위치에 1줄 자막 자동 삽입
- ✅ **폴백 처리**: 실패 시 단색 배경으로 자동 폴백

## 기술 스택

- **FastAPI**: REST API 서버
- **Redis + RQ**: 작업 큐 및 백그라운드 처리
- **edge-tts**: 음성 합성
- **ffmpeg**: 영상 생성 및 편집
- **BeautifulSoup**: 웹 스크래핑
- **OpenAI** (선택): AI 스크립트 생성

## 시스템 요구사항

### 필수
- Python 3.11+
- Redis 7+
- ffmpeg

### 선택
- OpenAI API Key (스크립트 자동 생성용)

## 설치 및 실행

### 방법 1: Docker Compose (권장)

```bash
# 1. 환경 변수 설정 (선택사항)
cp backend/.env.example backend/.env
# .env 파일에서 OPENAI_API_KEY 설정 (선택)

# 2. Docker Compose 실행
docker-compose up -d

# 3. 로그 확인
docker-compose logs -f

# 4. 종료
docker-compose down
```

서비스가 시작되면:
- **Backend API**: http://localhost:8000
- **API 문서**: http://localhost:8000/docs
- **Redis**: localhost:6379

### 방법 2: 로컬 실행

#### Windows (PowerShell)

```powershell
# 1. Redis 시작
docker run -d -p 6379:6379 redis:7-alpine

# 2. 백엔드 폴더로 이동
cd backend

# 3. 환경 변수 설정 (선택)
copy .env.example .env
# .env 파일 편집

# 4. 백엔드 서버 시작
.\run_local.ps1

# 5. 새 터미널에서 Worker 시작
.\venv\Scripts\Activate.ps1
python worker.py
```

#### Linux/Mac (Bash)

```bash
# 1. Redis 시작
docker run -d -p 6379:6379 redis:7-alpine
# 또는: brew services start redis (Mac)
# 또는: sudo service redis-server start (Linux)

# 2. 백엔드 폴더로 이동
cd backend

# 3. 환경 변수 설정 (선택)
cp .env.example .env
# .env 파일 편집

# 4. 실행 권한 부여
chmod +x run_local.sh

# 5. 백엔드 서버 시작
./run_local.sh

# 6. 새 터미널에서 Worker 시작
source venv/bin/activate
python worker.py
```

## API 사용법

### 1. 영상 생성 요청

```bash
POST /jobs
Content-Type: application/json

{
  "article_url": "https://www.nytimes.com/2024/01/01/world/example.html",
  "mode": "nyt_question"
}
```

**모드**:
- `nyt_question`: 질문형 스타일 (호기심 유발)
- `guardian_observe`: 관찰형 스타일 (분석적)

**응답**:
```json
{
  "job_id": "abc123xyz",
  "status": "queued",
  "message": "작업이 대기열에 추가되었습니다."
}
```

### 2. 작업 상태 조회

```bash
GET /status/{job_id}
```

**응답**:
```json
{
  "job_id": "abc123xyz",
  "status": "started",
  "progress": 60,
  "message": "영상 생성 중..."
}
```

**상태 값**:
- `queued`: 대기 중
- `started`: 진행 중
- `finished`: 완료
- `failed`: 실패

### 3. 작업 결과 조회

```bash
GET /result/{job_id}
```

**응답 (성공)**:
```json
{
  "job_id": "abc123xyz",
  "status": "finished",
  "video_url": "/download/abc123xyz.mp4",
  "duration": 45.2
}
```

### 4. 영상 다운로드

```bash
GET /download/{filename}
```

브라우저에서 직접 접근 가능:
```
http://localhost:8000/download/abc123xyz.mp4
```

## 프로젝트 구조

```
backend/
├── main.py                  # FastAPI 앱
├── worker.py                # RQ Worker
├── config.py                # 설정
├── requirements.txt         # 의존성
├── Dockerfile               # Docker 이미지
├── .env.example             # 환경 변수 예제
├── models/
│   └── schemas.py           # Pydantic 스키마
├── services/
│   ├── scraper.py           # 기사 파싱
│   ├── script_generator.py  # 스크립트 생성
│   ├── tts_service.py       # 음성 합성
│   └── video_service.py     # 영상 생성
├── tasks/
│   └── render_task.py       # RQ 백그라운드 작업
├── output/                  # 생성된 영상
└── temp/                    # 임시 파일
```

## 환경 변수

```env
# Redis 설정
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# OpenAI API (선택사항 - 스크립트 자동 생성)
OPENAI_API_KEY=your_openai_api_key_here
```

## 문제 해결

### Redis 연결 실패

```bash
# Docker로 Redis 시작
docker run -d -p 6379:6379 redis:7-alpine

# 연결 테스트
redis-cli ping
# 응답: PONG
```

### ffmpeg 설치 확인

```bash
# 설치 확인
ffmpeg -version

# Windows (Chocolatey)
choco install ffmpeg

# Mac (Homebrew)
brew install ffmpeg

# Linux (Ubuntu/Debian)
sudo apt-get install ffmpeg
```

### Worker가 작업을 처리하지 않음

1. Worker가 실행 중인지 확인
2. Redis 연결 확인
3. Worker 로그 확인

```bash
# Worker 재시작
python worker.py
```

### 영상 생성 실패

- **기사 파싱 실패**: 다른 뉴스 URL 시도
- **음성 생성 실패**: edge-tts 설치 확인
- **영상 렌더링 실패**: ffmpeg 설치 확인

### OpenAI API 없이 사용

OpenAI API 키가 없어도 기본 템플릿으로 스크립트가 생성됩니다.
더 나은 품질을 원하면 `OPENAI_API_KEY`를 설정하세요.

## 성능 및 제한

- **처리 시간**: 평균 30-60초 (기사 파싱 + 스크립트 + 음성 + 영상)
- **영상 길이**: 20초 고정
- **해상도**: 1080x1920 (세로 9:16)
- **작업 타임아웃**: 10분
- **결과 보관**: 1시간 (이후 자동 삭제)

## API 문서

서버 실행 후 다음 주소에서 Swagger UI 확인:

```
http://localhost:8000/docs
```

ReDoc 문서:

```
http://localhost:8000/redoc
```

## 테스트

```bash
# Python 테스트 스크립트 실행
python ../test_api.py
```

또는 curl:

```bash
# 1. 작업 생성
curl -X POST http://localhost:8000/jobs \
  -H "Content-Type: application/json" \
  -d '{"article_url": "https://www.nytimes.com/...", "mode": "nyt_question"}'

# 2. 상태 확인
curl http://localhost:8000/status/{job_id}

# 3. 결과 조회
curl http://localhost:8000/result/{job_id}
```

## 라이선스

MIT License

## 지원

문제가 발생하면 GitHub Issues에 등록해주세요.
