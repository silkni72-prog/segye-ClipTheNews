# 배포 가이드

## 🚀 배포 완료 상태

### 프론트엔드 (Vercel) ✅
- **Production URL**: https://frontend-beta-jet-95.vercel.app
- **상태**: 배포 완료
- **플랫폼**: Vercel (무료)

### 백엔드 (배포 필요)
- **플랫폼 옵션**: Railway, Render, AWS, DigitalOcean
- **Dockerfile**: ✅ 준비됨

---

## 📋 백엔드 배포 옵션

### Option 1: Railway (추천, 무료 $5 크레딧)

#### 1-1. Railway 계정 생성
1. https://railway.app 접속
2. GitHub 계정으로 로그인
3. New Project 클릭

#### 1-2. GitHub 저장소 연결
1. "Deploy from GitHub repo" 선택
2. `segye-ClipTheNews` 저장소 선택
3. Root directory: `/backend` 설정

#### 1-3. 환경 변수 설정
```
UNSPLASH_ACCESS_KEY=your_key
LEONARDO_API_KEY=your_key
```

#### 1-4. 자동 배포
- GitHub push 시 자동 배포
- URL: `https://your-app.up.railway.app`

---

### Option 2: Render (무료 플랜)

#### 2-1. Render 계정 생성
1. https://render.com 접속
2. GitHub 계정으로 로그인

#### 2-2. 새 Web Service 생성
1. New → Web Service
2. GitHub 저장소 선택
3. Settings:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

#### 2-3. 환경 변수 설정
```
UNSPLASH_ACCESS_KEY=your_key
LEONARDO_API_KEY=your_key
PORT=8000
```

#### 2-4. 무료 플랜 제한
- 15분 비활동 시 슬립 모드
- 첫 요청 시 30초 웨이크업 시간
- 월 750시간 무료

---

### Option 3: DigitalOcean App Platform

#### 3-1. DigitalOcean 계정
1. https://cloud.digitalocean.com 가입
2. $200 무료 크레딧 (60일)

#### 3-2. App 생성
1. Create → Apps
2. GitHub 저장소 연결
3. Dockerfile 자동 감지

#### 3-3. 환경 변수
```
UNSPLASH_ACCESS_KEY=your_key
LEONARDO_API_KEY=your_key
```

---

## 🔗 프론트엔드-백엔드 연결

### Vercel 환경 변수 설정

프론트엔드가 백엔드 API를 호출하도록 설정:

1. Vercel Dashboard 접속
2. 프로젝트 선택 → Settings → Environment Variables
3. 추가:

```
BACKEND_URL=https://your-backend-url.railway.app
# 또는
BACKEND_URL=https://your-app.onrender.com
```

4. Redeploy 클릭

---

## 🧪 배포 후 테스트

### 1. 프론트엔드 접속
```
https://frontend-beta-jet-95.vercel.app
```

### 2. 영상 생성 테스트
1. Generate 페이지 이동
2. 뉴스 URL 입력
3. 영상 생성 클릭
4. 백엔드 응답 확인

### 3. 에러 발생 시
- Vercel Logs 확인: `vercel logs`
- Railway/Render Logs 확인: 대시보드에서 확인

---

## 💡 현재 상태

### ✅ 완료
- GitHub 푸시 완료
- 프론트엔드 Vercel 배포 완료
- .gitignore 설정 (임시 파일 제외)

### ⏳ 남은 작업
- 백엔드 배포 (Railway/Render 선택 필요)
- 환경 변수 설정
- 프론트엔드-백엔드 연결
- 최종 테스트

---

## 🎯 빠른 배포 (Railway 추천)

```bash
# Railway CLI 설치 (선택)
npm install -g @railway/cli

# 로그인
railway login

# 프로젝트 초기화
cd backend
railway init

# 배포
railway up

# 환경 변수 설정
railway variables set UNSPLASH_ACCESS_KEY=xxx
railway variables set LEONARDO_API_KEY=xxx

# 도메인 확인
railway domain
```

**또는 웹 대시보드**에서 클릭만으로 배포 가능!

---

## 📞 다음 단계

어떤 플랫폼을 사용하시겠어요?
1. **Railway** (추천, 간단)
2. **Render** (무료, 슬립 모드 있음)
3. **DigitalOcean** ($200 크레딧)

선택하시면 해당 플랫폼으로 바로 배포해드리겠습니다! 🚀
