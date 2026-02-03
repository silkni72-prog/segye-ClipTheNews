# 배포 가이드 (Deployment Guide)

이 가이드는 ClipTheNews 애플리케이션을 프론트엔드(Vercel)와 백엔드(Render)에 배포하는 방법을 설명합니다.

## 1. 백엔드 배포 (Render)

### 1.1. Render 계정 생성
1. [Render.com](https://render.com) 방문
2. GitHub 계정으로 로그인

### 1.2. Web Service 생성
1. Dashboard에서 "New +" → "Web Service" 클릭
2. GitHub 리포지토리 연결: `silkni72-prog/segye-ClipTheNews`
3. 다음 설정 입력:
   - **Name**: `clipthenews-backend`
   - **Region**: Singapore (또는 가장 가까운 지역)
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: `Free`

### 1.3. 환경 변수 설정
Render Dashboard에서 Environment Variables 추가:
- `OPENAI_API_KEY`: OpenAI API 키
- `LEONARDO_API_KEY`: Leonardo AI API 키
- `PEXELS_API_KEY`: Pexels API 키 (optional)
- `UNSPLASH_ACCESS_KEY`: Unsplash API 키 (optional)

### 1.4. 배포
"Create Web Service" 클릭하면 자동으로 배포가 시작됩니다.
배포 완료 후 URL을 복사하세요 (예: `https://clipthenews-backend.onrender.com`)

---

## 2. 프론트엔드 배포 (Vercel)

### 2.1. Vercel 계정 생성
1. [Vercel.com](https://vercel.com) 방문
2. GitHub 계정으로 로그인

### 2.2. 프로젝트 Import
1. "Add New..." → "Project" 클릭
2. GitHub 리포지토리 선택: `silkni72-prog/segye-ClipTheNews`
3. "Import" 클릭

### 2.3. 프로젝트 설정
- **Framework Preset**: Next.js (자동 감지됨)
- **Root Directory**: `frontend` (중요!)
- **Build Command**: `npm run build`
- **Output Directory**: `.next`
- **Install Command**: `npm install`

### 2.4. 환경 변수 설정
Environment Variables 추가:
- `NEXT_PUBLIC_API_URL`: Render에서 받은 백엔드 URL (예: `https://clipthenews-backend.onrender.com`)

### 2.5. 배포
"Deploy" 클릭하면 자동으로 배포가 시작됩니다.
배포 완료 후 프론트엔드 URL을 받게 됩니다 (예: `https://segye-clip-the-news.vercel.app`)

---

## 3. CLI로 배포 (선택사항)

### 3.1. Vercel CLI로 프론트엔드 배포
```bash
# frontend 폴더로 이동
cd frontend

# Vercel 로그인
vercel login

# 프로덕션 배포
vercel --prod
```

### 3.2. 환경 변수 설정
```bash
vercel env add NEXT_PUBLIC_API_URL
```

---

## 4. 배포 확인

### 백엔드 확인
백엔드 URL에 접속해서 API 문서 확인:
```
https://clipthenews-backend.onrender.com/docs
```

### 프론트엔드 확인
프론트엔드 URL에 접속:
```
https://segye-clip-the-news.vercel.app
```

---

## 5. 문제 해결

### 백엔드가 시작되지 않는 경우
- Render 로그 확인
- requirements.txt의 모든 패키지가 설치되었는지 확인
- 환경 변수가 올바르게 설정되었는지 확인

### 프론트엔드에서 백엔드 연결 실패
- `NEXT_PUBLIC_API_URL`이 올바르게 설정되었는지 확인
- CORS 설정 확인 (backend/main.py)
- 백엔드가 정상적으로 실행 중인지 확인

### Render 무료 플랜 제한
- 15분 동안 요청이 없으면 슬립 모드로 전환
- 첫 요청 시 시작 시간이 소요될 수 있음 (30초~1분)

---

## 6. 자동 배포 설정

GitHub에 push하면 자동으로 배포됩니다:
- **Vercel**: main 브랜치 push 시 자동 배포
- **Render**: main 브랜치 push 시 자동 배포

---

## 참고 사항

### API 키 관리
- `.env.local` 파일은 절대 git에 커밋하지 마세요
- 모든 API 키는 배포 플랫폼의 환경 변수로 관리하세요

### 비용
- **Vercel**: Free tier (Hobby) - 충분함
- **Render**: Free tier - 월 750시간 무료 (한 서비스면 충분)

### 성능 최적화
- Render 무료 플랜은 슬립 모드가 있으므로, 프로덕션에서는 유료 플랜 고려
- Vercel은 CDN을 통해 전 세계적으로 빠른 응답 제공
