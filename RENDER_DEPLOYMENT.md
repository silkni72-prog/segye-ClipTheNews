# Render 배포 가이드 (클릭으로 완료!)

## 🎯 배포 순서 (중요!)

1. **Redis 생성** (먼저!)
2. **Backend Web Service 생성**
3. **Worker Background Service 생성**
4. **Frontend 환경 변수 업데이트**

---

## Step 1: Redis 생성

### 1-1. Render 접속
```
https://dashboard.render.com
```

### 1-2. Redis 생성
1. **"New +"** 클릭
2. **"Redis"** 선택
3. 설정:
   ```
   Name: clipthenews-redis
   Region: Oregon (US West)
   Plan: Free
   ```
4. **"Create Redis"** 클릭

### 1-3. Redis URL 복사
생성 후 **"Internal Redis URL"** 복사:
```
redis://red-xxxxx.render.com:6379
```

⚠️ **이 URL을 메모장에 저장하세요!** 다음 단계에서 사용합니다.

---

## Step 2: Backend API 서버 생성

### 2-1. 새 Web Service 생성
1. **"New +"** → **"Web Service"**
2. GitHub 저장소 연결:
   - Repository: `silkni72-prog/segye-ClipTheNews`
   - **"Connect"** 클릭

### 2-2. 설정 입력

#### Name
```
clipthenews-backend
```

#### Region
```
Oregon (US West)
```

#### Branch
```
main
```

#### Root Directory
```
backend
```

#### Runtime
```
Python 3
```

#### Build Command
```
pip install -r requirements.txt
```

#### Start Command
```
uvicorn main:app --host 0.0.0.0 --port $PORT
```

#### Instance Type
```
Free
```

### 2-3. 환경 변수 설정

**"Advanced"** → **"Add Environment Variable"**

#### 필수 환경 변수
```bash
# Redis (필수!)
REDIS_URL=redis://red-xxxxx.render.com:6379  # Step 1에서 복사한 URL

# 서버 설정
REDIS_HOST=red-xxxxx.render.com              # Redis 호스트만
REDIS_PORT=6379
REDIS_DB=0
```

#### 선택 환경 변수 (기능 강화)
```bash
# AI 이미지 생성
LEONARDO_API_KEY=your_leonardo_key_here

# 스톡 이미지
UNSPLASH_ACCESS_KEY=your_unsplash_key_here

# AI 스크립트 생성 (고급)
OPENAI_API_KEY=sk-your-openai-key-here

# TTS (고급)
# GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
# ELEVENLABS_API_KEY=your_elevenlabs_key
```

### 2-4. 배포 시작
**"Create Web Service"** 클릭!

배포 진행 상황:
```
Installing dependencies...
✓ Build successful
✓ Deploy live
```

### 2-5. URL 확인
배포 완료 후:
```
https://clipthenews-backend.onrender.com
```

이 URL을 복사하세요!

---

## Step 3: Worker 생성 (백그라운드 작업)

영상 생성은 오래 걸리므로 별도 Worker가 필요합니다.

### 3-1. Background Worker 생성
1. **"New +"** → **"Background Worker"**
2. 같은 저장소 선택 (`segye-ClipTheNews`)

### 3-2. 설정 입력

#### Name
```
clipthenews-worker
```

#### Root Directory
```
backend
```

#### Build Command
```
pip install -r requirements.txt
```

#### Start Command
```
python worker.py
```

### 3-3. 환경 변수
**Backend와 동일한 환경 변수 입력** (특히 `REDIS_URL`!)

```bash
REDIS_URL=redis://red-xxxxx.render.com:6379
REDIS_HOST=red-xxxxx.render.com
REDIS_PORT=6379
REDIS_DB=0

# 선택사항 (Backend와 동일하게)
LEONARDO_API_KEY=...
UNSPLASH_ACCESS_KEY=...
OPENAI_API_KEY=...
```

### 3-4. 생성
**"Create Background Worker"** 클릭!

---

## Step 4: Frontend 환경 변수 업데이트

### 4-1. Vercel 대시보드 접속
```
https://vercel.com/dashboard
```

### 4-2. 프로젝트 선택
- Project: `frontend`

### 4-3. 환경 변수 추가
1. **Settings** → **Environment Variables**
2. **"Add"** 클릭
3. 입력:

```bash
# Key
NEXT_PUBLIC_API_URL

# Value (Step 2에서 복사한 Backend URL)
https://clipthenews-backend.onrender.com

# Environment
Production, Preview, Development (모두 선택)
```

4. **"Save"** 클릭

### 4-4. 재배포
1. **Deployments** 탭
2. 최신 배포의 **"..."** 클릭
3. **"Redeploy"** 선택
4. **"Redeploy"** 확인

---

## ✅ 배포 완료 확인

### Backend 테스트
```bash
# 브라우저에서 접속
https://clipthenews-backend.onrender.com

# 응답 확인
{
  "service": "ClipTheNews API",
  "version": "2.0.0",
  "redis_connected": true  # ← 이게 true여야 함!
}
```

### Worker 로그 확인
Render Dashboard → `clipthenews-worker` → **Logs**

```
[OK] Redis 연결 성공
Listening for jobs on default queue...
```

### Frontend 테스트
```
https://frontend-beta-jet-95.vercel.app
```

1. 뉴스 URL 입력
2. 모드 선택
3. **"영상 생성하기"** 클릭
4. Job ID 받음 → 처리 대기

---

## 🐛 문제 해결

### "Redis 연결 실패"
- **원인**: `REDIS_URL` 환경 변수 누락
- **해결**: Backend와 Worker 모두에 `REDIS_URL` 추가

### "Worker가 작업을 안 함"
- **확인 1**: Worker 로그에서 "Listening for jobs" 메시지 확인
- **확인 2**: Redis URL이 정확한지 확인
- **해결**: Worker 재시작 (Render Dashboard → Manual Deploy)

### "첫 요청이 느림 (30초+)"
- **원인**: Render 무료 플랜은 15분 비활동 시 슬립
- **정상**: 첫 요청에 30초 웨이크업 시간 필요
- **해결**: Keep-alive 설정 (별도 문서 참고)

### "영상 생성 실패"
- **로그 확인**: Render Dashboard → Worker → Logs
- **일반적 원인**:
  - ffmpeg 누락 (Dockerfile 사용 시 해결)
  - 메모리 부족 (무료 플랜 512MB 제한)
  - 타임아웃 (긴 영상)

---

## 💰 비용 (무료!)

### Render 무료 플랜
- **Web Service**: 750시간/월
- **Background Worker**: 750시간/월
- **Redis**: 25MB 스토리지

### 제한 사항
- 15분 비활동 시 슬립 모드
- 첫 요청 시 30초 웨이크업
- 월 750시간 (31일 = 744시간, 거의 무제한)

---

## 🚀 업그레이드 옵션

무료 플랜이 부족하면:

### Render Starter ($7/월)
- ✅ 항상 켜짐 (슬립 없음)
- ✅ 512MB → 1GB RAM
- ✅ 더 빠른 응답

### Railway ($5 크레딧)
- ✅ 항상 켜짐
- ✅ 자동 스케일링
- ✅ 더 나은 성능

---

## 📊 배포 구조

```
GitHub Repository (segye-ClipTheNews)
    ↓ (자동 배포)
┌───────────────────────────────────┐
│  Render                           │
│                                   │
│  ┌─────────────┐                 │
│  │   Redis     │ (무료)          │
│  │  (메모리DB)  │                 │
│  └─────────────┘                 │
│         ↕                         │
│  ┌─────────────┐  ┌────────────┐ │
│  │  Backend    │  │   Worker   │ │
│  │   (API)     │←→│  (영상생성) │ │
│  └─────────────┘  └────────────┘ │
│         ↓                         │
└───────────────────────────────────┘
         ↓ API 호출
┌───────────────────────────────────┐
│  Vercel                           │
│  ┌─────────────┐                 │
│  │  Frontend   │ (Next.js)       │
│  │  (UI)       │                 │
│  └─────────────┘                 │
└───────────────────────────────────┘
```

---

## 🎉 완료!

이제 다음 기능이 작동합니다:

- ✅ 뉴스 URL 입력
- ✅ AI 스크립트 생성 (20초)
- ✅ AI 음성 합성 (edge-tts)
- ✅ 영상 자동 생성 (ffmpeg)
- ✅ 백그라운드 작업 (서버 안 멈춤)
- ✅ 결과 다운로드

**전 세계 어디서나 접속 가능한 SaaS가 완성되었습니다!** 🚀

---

**마지막 업데이트**: 2026-02-04
