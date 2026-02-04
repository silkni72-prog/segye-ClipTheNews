# 프론트엔드-백엔드 통합 가이드

## ✅ 완료된 변경사항

새로운 Redis + RQ 백엔드와 프론트엔드가 성공적으로 통합되었습니다!

### 수정된 파일

1. **`frontend/app/api/generate/route.ts`**
   - ❌ 기존: `POST /generate` (동기 API)
   - ✅ 변경: `POST /jobs` → 폴링 → `GET /result` (비동기 작업 큐)
   - 5초마다 상태 확인, 최대 3분 대기

2. **`frontend/components/VideoForm.tsx`**
   - ❌ 제거: `scenario` 입력 필드
   - ✅ 추가: `mode` 선택 (질문형/관찰형)
   - ✅ 수정: 환경 변수 사용 (`NEXT_PUBLIC_API_URL`)

3. **`frontend/.env.local`** (새로 생성)
   - 백엔드 URL 설정
   - 로컬/프로덕션 환경 분리

---

## 🚀 실행 방법

### 1단계: 백엔드 실행

**Docker Compose (권장):**
```bash
# 프로젝트 루트에서
docker-compose up -d

# 로그 확인
docker-compose logs -f backend worker
```

**로컬 실행 (Windows):**
```powershell
cd backend
.\run_local.ps1

# 새 터미널
.\venv\Scripts\Activate.ps1
python worker.py
```

**로컬 실행 (Mac/Linux):**
```bash
cd backend
./run_local.sh

# 새 터미널
source venv/bin/activate
python worker.py
```

### 2단계: 백엔드 확인

```bash
# 헬스 체크
curl http://localhost:8000/health

# API 문서
http://localhost:8000/docs
```

### 3단계: 프론트엔드 실행

```bash
cd frontend

# 의존성 설치 (처음 한 번만)
npm install

# 개발 서버 시작
npm run dev
```

### 4단계: 접속

```
http://localhost:3000
```

---

## 🎯 사용 방법

1. **뉴스 URL 입력**
   - NYTimes, Guardian 등 아무 뉴스 URL

2. **영상 스타일 선택**
   - **질문형 (NYT)**: 호기심을 자극하는 질문으로 시작
   - **관찰형 (Guardian)**: 분석적이고 차분한 톤

3. **영상 생성하기 클릭**
   - 백그라운드에서 처리 (평균 30-60초)
   - 5초마다 자동으로 상태 확인

4. **완료 후 다운로드**
   - 1080x1920 세로 영상 (mp4)
   - 20초 길이, 한국어 음성, 자막 포함

---

## 🔄 데이터 플로우

```
사용자 입력 (URL + 모드)
    ↓
Frontend (VideoForm)
    ↓
Next.js API Route (/api/generate)
    ↓
POST /jobs → Redis Queue
    ↓
RQ Worker (백그라운드)
    ├─ 기사 파싱
    ├─ 스크립트 생성
    ├─ 음성 합성
    └─ 영상 렌더링
    ↓
GET /status (폴링 5초마다)
    ↓
GET /result → video_url
    ↓
영상 다운로드
```

---

## ⚙️ 환경 변수

### 프론트엔드 (`frontend/.env.local`)

```env
# 백엔드 API URL (Next.js 서버에서 사용)
BACKEND_URL=http://localhost:8000

# 클라이언트에서 접근 가능한 API URL
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 백엔드 (`backend/.env`)

```env
# Redis 설정
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# OpenAI API (선택사항 - 더 나은 스크립트 생성)
OPENAI_API_KEY=sk-...
```

---

## 🆚 기존 vs 새로운 API

### 기존 API (동기)
```typescript
POST /generate
Body: { news_url, scenario }
Response: { video_url, message }
```
- 장점: 간단함
- 단점: 요청 타임아웃, 여러 작업 동시 처리 불가

### 새로운 API (비동기)
```typescript
1. POST /jobs
   Body: { article_url, mode }
   Response: { job_id, status: "queued" }

2. GET /status/{job_id}
   Response: { status: "started", progress: 50 }

3. GET /result/{job_id}
   Response: { video_url, duration }

4. GET /download/{filename}
   Response: video file
```
- 장점: 여러 작업 동시 처리, 타임아웃 없음, 진행 상황 확인
- 단점: 복잡함 (프론트엔드에서 자동 처리)

---

## 🎨 UI 변경사항

### Before (기존)
- ✏️ 시나리오 입력 (textarea)
- 수동 입력 필요

### After (새로운)
- 🎭 영상 스타일 선택 (dropdown)
  - 질문형 (NYT 스타일)
  - 관찰형 (Guardian 스타일)
- 자동 스크립트 생성

---

## 📊 성능

### 처리 시간
- **평균**: 30-60초
- **단계별**:
  1. 기사 파싱: 5-10초
  2. 스크립트 생성: 3-5초
  3. 음성 합성: 5-10초
  4. 영상 렌더링: 15-35초

### 동시 처리
- Worker 수 = 동시 처리 작업 수
- Docker Compose: 1개 Worker
- 로컬: Worker 추가 실행 가능

```bash
# Worker 추가 (새 터미널)
cd backend
source venv/bin/activate
python worker.py
```

---

## 🐛 문제 해결

### 1. "서버 연결 실패"

**원인**: 백엔드가 실행되지 않음

**해결**:
```bash
# 백엔드 상태 확인
curl http://localhost:8000/health

# 백엔드 시작
docker-compose up -d
# 또는
cd backend && .\run_local.ps1
```

### 2. "작업 처리 시간 초과"

**원인**: Worker가 실행되지 않음

**해결**:
```bash
# Worker 확인
docker-compose logs worker
# 또는
cd backend && python worker.py
```

### 3. Redis 연결 실패

**해결**:
```bash
# Redis 시작
docker run -d -p 6379:6379 redis:7-alpine

# 연결 확인
redis-cli ping
# 응답: PONG
```

### 4. 영상 다운로드 404

**원인**: 파일이 생성되지 않았거나 경로 오류

**해결**:
- `backend/output/` 폴더 확인
- Worker 로그 확인
- 작업 상태가 'finished'인지 확인

---

## 🚢 프로덕션 배포

### 환경 변수 변경

**프론트엔드 (Vercel):**
```env
BACKEND_URL=https://your-backend.onrender.com
NEXT_PUBLIC_API_URL=https://your-backend.onrender.com
```

**백엔드 (Render/Railway):**
```env
REDIS_HOST=your-redis-host
REDIS_PORT=6379
OPENAI_API_KEY=sk-...
```

### Docker Compose (프로덕션)

```yaml
# docker-compose.prod.yml
services:
  redis:
    image: redis:7-alpine
    
  backend:
    build: ./backend
    environment:
      - REDIS_HOST=redis
      
  worker:
    build: ./backend
    command: python worker.py
    
  frontend:
    build: ./frontend
    environment:
      - BACKEND_URL=http://backend:8000
```

---

## 📚 관련 문서

- [백엔드 상세 문서](BACKEND_README.md)
- [빠른 시작 가이드](QUICKSTART.md)
- [시스템 아키텍처](ARCHITECTURE.md)
- [프로젝트 구조](PROJECT_STRUCTURE.md)

---

## ✅ 체크리스트

통합 전 확인:
- [ ] Redis 실행 중
- [ ] 백엔드 서버 실행 (`http://localhost:8000/health`)
- [ ] Worker 실행 중
- [ ] ffmpeg 설치됨
- [ ] 프론트엔드 `.env.local` 생성

테스트:
- [ ] 프론트엔드 접속 (`http://localhost:3000`)
- [ ] 뉴스 URL 입력
- [ ] 스타일 선택
- [ ] 영상 생성 확인
- [ ] 다운로드 성공

---

**버전**: 2.0.0 (통합 완료)  
**마지막 업데이트**: 2026-02-04
