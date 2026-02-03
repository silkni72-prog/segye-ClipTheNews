# ClipTheNews 🎬

뉴스 URL과 시나리오를 입력하면 자동으로 세로형 뉴스 영상(mp4)을 생성하는 SaaS 웹앱

## 기술 스택

- **Frontend**: Next.js 14 (App Router) + Tailwind CSS + TypeScript
- **Backend**: FastAPI + MoviePy + BeautifulSoup4
- **영상 포맷**: 1080x1920 (9:16 세로형), 20초

## 프로젝트 구조

```
segye-ClipTheNews/
├── frontend/          # Next.js 프론트엔드
│   ├── app/
│   │   ├── page.tsx              # 랜딩 페이지
│   │   ├── generate/             # 영상 생성 페이지
│   │   └── api/generate/         # FastAPI 프록시
│   └── components/               # React 컴포넌트
├── backend/           # FastAPI 백엔드
│   ├── main.py                   # FastAPI 엔트리포인트
│   ├── services/                 # 비즈니스 로직
│   └── models/                   # 데이터 모델
└── README.md
```

## 로컬 개발 환경 설정

### 1. Backend 설정

#### 환경변수 설정 (선택)

`backend/.env` 파일을 생성하여 API 키를 설정하세요:

```env
# Unsplash API (스톡 이미지)
UNSPLASH_ACCESS_KEY=your_unsplash_access_key_here

# Leonardo.ai API (AI 이미지 생성)
LEONARDO_API_KEY=your_leonardo_api_key_here
```

**API 키 발급 방법:**

1. **Unsplash API** (선택):
   - https://unsplash.com/developers 접속
   - "Register as a developer" 클릭
   - 새 앱 생성 → Access Key 복사

2. **Leonardo.ai API** (선택, 무료 플랜 하루 30-40 이미지):
   - https://leonardo.ai 회원가입
   - Settings → API Access → Generate API Key
   - 📖 **상세 가이드**: `LEONARDO_SETUP.md` 참고

> 💡 **참고**: API 키가 없어도 작동합니다. 뉴스 이미지만 사용됩니다.

#### Backend 실행

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Backend: http://localhost:8000

### 2. Frontend 실행

```bash
cd frontend
npm install
npm run dev
```

Frontend: http://localhost:3000

## 기능

1. **랜딩 페이지**: 서비스 소개 및 주요 기능 안내
2. **영상 생성**: 
   - 뉴스 URL 입력
   - 시나리오 자동 생성 (4문장) 또는 수동 입력
   - 20초 세로형 영상 자동 생성
   - **3단계 하이브리드 이미지 수집**:
     1. 뉴스 기사 이미지 스크래핑 (우선)
     2. 부족 시 Unsplash 스톡 이미지 (최대 2개)
     3. 여전히 부족 시 Leonardo AI 이미지 생성
     - 최대 4개 이미지 사용
   - **동적 자막 시스템**:
     - 제목: 상단, 첫 3초만 표시
     - 시나리오: 하단, 각 장면마다 다른 자막
   - 페이드인/페이드아웃 전환 효과

## 사용 방법

1. 랜딩 페이지에서 "지금 시작하기" 클릭
2. 뉴스 URL 입력 (예: 네이버뉴스, 조선일보 등)
3. 시나리오 텍스트 입력
4. "영상 생성" 버튼 클릭
5. 로딩 완료 후 영상 다운로드
