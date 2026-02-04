# 🚀 단일화 완료! - 초간단 실행 가이드

## ✅ 백엔드 제거 완료!

Redis, Docker, Python, FastAPI **모두 제거**하고 **Next.js만**으로 작동합니다!

---

## 🎯 실행 방법 (2단계만!)

### 1️⃣ OpenAI API 키 설정 (선택사항)

`.env.local` 파일을 열고:

```env
OPENAI_API_KEY=sk-your-key-here
```

> 💡 **없어도 작동합니다!** 템플릿 기반으로 스크립트가 생성됩니다.

### 2️⃣ 서버 시작

```bash
npm run dev
```

끝! 🎉

---

## 📍 접속

```
http://localhost:3000
```

---

## 🎬 사용 방법

1. **뉴스 URL 입력**
   - NYTimes, Guardian, 한국 뉴스 등 아무 URL

2. **영상 스타일 선택**
   - 질문형 (NYT 스타일)
   - 관찰형 (Guardian 스타일)

3. **"영상 생성하기" 클릭**

4. **결과 확인**
   - 📰 기사 제목
   - 📝 생성된 스크립트 (20초 분량)
   - 📋 요약

---

## 🔧 기능

### ✅ 작동하는 기능
- ✅ 뉴스 URL 파싱
- ✅ 기사 제목/요약 추출
- ✅ 20초 숏폼 스크립트 자동 생성
- ✅ 2가지 스타일 (질문형/관찰형)
- ✅ OpenAI 연동 (선택)
- ✅ 템플릿 폴백

### 🚧 나중에 추가 가능
- 🚧 실제 영상 생성 (ffmpeg)
- 🚧 음성 합성 (TTS)
- 🚧 스톡 이미지 추가
- 🚧 자막 오버레이

---

## 📦 설치된 패키지

```json
{
  "next": "16.1.6",
  "openai": "^4.20.1",
  "react": "19.2.3",
  "react-dom": "19.2.3"
}
```

---

## 🛠️ 파일 구조

```
프로젝트 루트/
├── app/
│   ├── api/
│   │   └── generate/
│   │       └── route.ts        ⭐ 백엔드 로직 (기사 파싱 + 스크립트 생성)
│   ├── page.tsx
│   └── layout.tsx
├── components/
│   └── VideoForm.tsx           ⭐ UI 컴포넌트
├── .env.local                  ⭐ OpenAI API 키 (선택)
├── package.json
└── SIMPLE_START.md             ⭐ 이 파일
```

---

## 💡 OpenAI API 키 받는 방법

1. https://platform.openai.com/ 접속
2. API Keys → Create new secret key
3. `.env.local`에 붙여넣기
4. 서버 재시작 (`npm run dev`)

---

## 🐛 문제 해결

### "npm run dev" 오류

```bash
# node_modules 삭제 후 재설치
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### 포트 3000이 이미 사용 중

```bash
# 포트 변경
npm run dev -- -p 3001
```

---

## 📊 성능

- **시작 시간**: < 5초
- **기사 파싱**: 1-3초
- **스크립트 생성**: 
  - OpenAI 사용: 2-5초
  - 템플릿: 즉시

---

## 🎯 장점

✅ **설치 간단**: Node.js만 있으면 OK
✅ **의존성 최소**: Redis, Docker, Python 불필요
✅ **빠른 시작**: `npm run dev` 한 줄
✅ **유지보수 쉬움**: 모든 코드가 한 곳에
✅ **배포 간편**: Vercel에 바로 배포 가능

---

## 🚀 Vercel 배포

```bash
# Vercel CLI 설치
npm i -g vercel

# 배포
vercel

# 환경 변수 설정
vercel env add OPENAI_API_KEY
```

---

## 📚 API 엔드포인트

### POST /api/generate

**요청:**
```json
{
  "news_url": "https://...",
  "mode": "nyt_question"
}
```

**응답:**
```json
{
  "message": "스크립트가 생성되었습니다!",
  "title": "기사 제목",
  "summary": "기사 요약",
  "script": "생성된 20초 스크립트",
  "video_url": "/api/dummy-video"
}
```

---

## 🎉 결과

**이전 (복잡):**
- Backend (Python + FastAPI)
- Redis
- RQ Worker
- Docker
- ffmpeg
- 총 5개 서비스

**지금 (단순):**
- Next.js
- 총 1개 서비스

**80% 단순화 완료!** 🎊

---

**마지막 업데이트**: 2026-02-04
