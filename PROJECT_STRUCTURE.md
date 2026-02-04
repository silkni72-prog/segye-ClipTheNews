# ClipTheNews - 프로젝트 구조

## 📁 전체 디렉토리 구조

```
segye ClipTheNews/
│
├── 📄 docker-compose.yml           # Docker Compose 설정
├── 📄 test_api.py                  # API 테스트 스크립트
├── 📄 .gitignore                   # Git 제외 파일
│
├── 📖 QUICKSTART.md                # 빠른 시작 가이드 ⭐
├── 📖 BACKEND_README.md            # 백엔드 상세 문서
├── 📖 ARCHITECTURE.md              # 시스템 아키텍처
├── 📖 DEPLOYMENT.md                # 배포 가이드
├── 📖 README.md                    # 프로젝트 소개
│
├── 🔧 backend/                     # FastAPI 백엔드
│   ├── main.py                     # FastAPI 메인 앱 ⭐
│   ├── worker.py                   # RQ Worker ⭐
│   ├── config.py                   # 설정 파일
│   ├── requirements.txt            # Python 의존성
│   ├── Dockerfile                  # Docker 이미지
│   ├── .dockerignore               # Docker 제외 파일
│   ├── .env.example                # 환경 변수 예제
│   │
│   ├── run_local.ps1               # Windows 실행 스크립트
│   ├── run_local.sh                # Linux/Mac 실행 스크립트
│   │
│   ├── 📦 models/                  # 데이터 모델
│   │   ├── __init__.py
│   │   └── schemas.py              # Pydantic 스키마
│   │
│   ├── 🛠️ services/                # 비즈니스 로직
│   │   ├── __init__.py
│   │   ├── scraper.py              # 기사 파싱 ⭐
│   │   ├── script_generator.py     # 스크립트 생성 ⭐
│   │   ├── tts_service.py          # 음성 합성 ⭐
│   │   └── video_service.py        # 영상 생성 ⭐
│   │
│   ├── ⚙️ tasks/                   # 백그라운드 작업
│   │   ├── __init__.py
│   │   └── render_task.py          # 영상 렌더링 작업 ⭐
│   │
│   ├── 📂 output/                  # 생성된 영상
│   │   └── .gitkeep
│   │
│   └── 📂 temp/                    # 임시 파일
│       └── .gitkeep
│
└── 🎨 frontend/                    # Next.js 프론트엔드
    ├── package.json
    ├── next.config.ts
    ├── tsconfig.json
    │
    ├── app/                        # Next.js App Router
    │   ├── page.tsx                # 홈페이지
    │   ├── layout.tsx              # 레이아웃
    │   ├── globals.css             # 전역 스타일
    │   │
    │   ├── generate/               # 영상 생성 페이지
    │   │   └── page.tsx
    │   │
    │   └── api/                    # API Routes
    │       └── generate/
    │           └── route.ts
    │
    ├── components/                 # React 컴포넌트
    │   ├── Hero.tsx
    │   ├── Features.tsx
    │   ├── VideoForm.tsx
    │   ├── LoadingSpinner.tsx
    │   └── PricingComparison.tsx
    │
    └── public/                     # 정적 파일
        └── *.svg
```

## 🎯 핵심 파일 설명

### 백엔드 (Backend)

| 파일 | 역할 | 중요도 |
|------|------|--------|
| `main.py` | FastAPI 앱, REST API 엔드포인트 | ⭐⭐⭐ |
| `worker.py` | RQ Worker, 백그라운드 작업 처리 | ⭐⭐⭐ |
| `config.py` | 전역 설정 (Redis, 영상 설정 등) | ⭐⭐ |
| `models/schemas.py` | API 요청/응답 스키마 | ⭐⭐ |
| `services/scraper.py` | 뉴스 기사 스크래핑 | ⭐⭐⭐ |
| `services/script_generator.py` | 20초 스크립트 생성 | ⭐⭐⭐ |
| `services/tts_service.py` | edge-tts 음성 합성 | ⭐⭐⭐ |
| `services/video_service.py` | ffmpeg 영상 생성 | ⭐⭐⭐ |
| `tasks/render_task.py` | 전체 렌더링 파이프라인 | ⭐⭐⭐ |

### 프론트엔드 (Frontend)

| 파일 | 역할 |
|------|------|
| `app/page.tsx` | 메인 페이지 |
| `app/generate/page.tsx` | 영상 생성 페이지 |
| `components/VideoForm.tsx` | 영상 생성 폼 |
| `components/LoadingSpinner.tsx` | 로딩 UI |

### 설정 및 문서

| 파일 | 역할 |
|------|------|
| `docker-compose.yml` | Docker 컨테이너 설정 |
| `backend/Dockerfile` | 백엔드 Docker 이미지 |
| `backend/.env.example` | 환경 변수 템플릿 |
| `QUICKSTART.md` | 빠른 시작 가이드 ⭐ |
| `BACKEND_README.md` | 백엔드 상세 문서 |
| `ARCHITECTURE.md` | 시스템 아키텍처 |

## 🔄 데이터 플로우

```
1. 사용자 요청
   ↓
2. Frontend (VideoForm)
   ↓ POST /jobs
3. FastAPI (main.py)
   ↓ enqueue
4. Redis Queue
   ↓ dequeue
5. RQ Worker (worker.py)
   ↓ execute
6. Render Task (render_task.py)
   ├─ scraper.py (기사 파싱)
   ├─ script_generator.py (스크립트)
   ├─ tts_service.py (음성)
   └─ video_service.py (영상)
   ↓
7. output/{job_id}.mp4
   ↓ GET /result/{job_id}
8. Frontend (다운로드)
```

## 📦 주요 의존성

### Backend
- **FastAPI**: 웹 프레임워크
- **Redis + RQ**: 작업 큐
- **BeautifulSoup**: 웹 스크래핑
- **edge-tts**: 음성 합성
- **OpenAI**: AI 스크립트 생성 (선택)
- **ffmpeg**: 영상 처리 (시스템)

### Frontend
- **Next.js 15**: React 프레임워크
- **TypeScript**: 타입 안전성
- **Tailwind CSS**: 스타일링

## 🚀 실행 방법

### 1. Docker (권장)
```bash
docker-compose up -d
```

### 2. 로컬 실행

**Windows:**
```powershell
cd backend
.\run_local.ps1
# 새 터미널
python worker.py
```

**Linux/Mac:**
```bash
cd backend
./run_local.sh
# 새 터미널
python worker.py
```

## 📊 API 엔드포인트

| Method | Endpoint | 설명 |
|--------|----------|------|
| GET | `/` | API 정보 |
| POST | `/jobs` | 영상 생성 작업 생성 |
| GET | `/status/{job_id}` | 작업 상태 조회 |
| GET | `/result/{job_id}` | 작업 결과 조회 |
| GET | `/download/{filename}` | 영상 다운로드 |
| GET | `/health` | 헬스 체크 |

## 🔧 설정 파일

### backend/.env
```env
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
OPENAI_API_KEY=sk-...  # 선택사항
```

### backend/config.py
- 영상 설정 (해상도, FPS, 길이)
- 자막 설정 (위치, 크기, 색상)
- Redis 설정
- TTS 설정

## 📝 로그 위치

### Docker
```bash
docker-compose logs backend
docker-compose logs worker
```

### 로컬
- Backend: 터미널 출력
- Worker: 터미널 출력

## 🧪 테스트

```bash
# API 테스트
python test_api.py

# 헬스 체크
curl http://localhost:8000/health

# API 문서
http://localhost:8000/docs
```

## 📚 문서 인덱스

- **시작하기**: [QUICKSTART.md](QUICKSTART.md) ⭐
- **백엔드**: [BACKEND_README.md](BACKEND_README.md)
- **아키텍처**: [ARCHITECTURE.md](ARCHITECTURE.md)
- **배포**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **프로젝트 구조**: [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) (이 문서)

## 🔐 보안 고려사항

- `.env` 파일은 Git에 커밋하지 않음
- API 키는 환경 변수로 관리
- CORS 설정으로 프론트엔드만 접근 허용
- 파일 경로 검증으로 경로 탐색 방지

## 🎬 영상 스펙

- **해상도**: 1080x1920 (세로 9:16)
- **길이**: 20초 고정
- **FPS**: 30
- **코덱**: H.264 (libx264)
- **오디오**: AAC, 음성 TTS
- **자막**: SRT, 하단 25%, 1줄

## 🛠️ 개발 팁

### 1. 디버깅
```bash
# Worker 로그 실시간 확인
python worker.py

# Backend 로그
uvicorn main:app --reload --log-level debug
```

### 2. 새 서비스 추가
1. `backend/services/` 에 파일 생성
2. `services/__init__.py` 에 import 추가
3. `tasks/render_task.py` 에서 사용

### 3. 환경 변수 추가
1. `backend/config.py` 에 변수 추가
2. `backend/.env.example` 업데이트
3. `docker-compose.yml` 에 환경 변수 추가

---

**Version**: 2.0.0  
**Last Updated**: 2026-02-04
