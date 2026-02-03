# ClipTheNews 사용 가이드

## 서버 실행 방법

### 0. Unsplash API 키 설정 (선택사항)

더 다양한 이미지를 사용하려면 Unsplash API 키를 설정하세요:

```bash
cd backend
# .env 파일에 API 키 추가
echo UNSPLASH_ACCESS_KEY=your_key_here > .env
```

**API 키 발급**: https://unsplash.com/developers

> 💡 API 키 없이도 사용 가능합니다 (뉴스 이미지만 사용)

### 1. 백엔드 서버 시작

```bash
cd backend
.\venv\Scripts\activate  # 가상환경 활성화
python -m uvicorn main:app --reload --port 8000
```

백엔드 서버: http://localhost:8000

### 2. 프론트엔드 서버 시작

새 터미널에서:

```bash
cd frontend
npm run dev
```

프론트엔드 서버: http://localhost:3000

## 사용 방법

### 1단계: 랜딩 페이지 접속
- 브라우저에서 http://localhost:3000 접속
- "지금 시작하기" 버튼 클릭

### 2단계: 영상 생성
- **뉴스 URL** 입력
  - 예: https://news.naver.com 등의 뉴스 기사 URL
  - 네이버뉴스, 조선일보, 중앙일보 등 주요 언론사 지원
  
- **시나리오** 입력
  - 영상 하단에 표시될 자막 텍스트
  - 최대 300자
  - 예: "오늘의 주요 뉴스를 소개합니다"

### 3단계: 영상 다운로드
- "영상 생성하기" 버튼 클릭
- 약 20-40초 대기 (뉴스 스크래핑 + 영상 생성)
- 완료 후 "영상 다운로드" 버튼 클릭

## 성능 최적화

현재 설정:
- **이미지 수**: 최대 2개 (뉴스 이미지 + Unsplash 스톡 이미지)
- **이미지 소스**: 
  1. 뉴스 기사 스크래핑 (우선)
  2. Unsplash API 자동 보충 (부족 시)
- **영상 길이**: 10초
- **해상도**: 1080x1920 (9:16 세로형)
- **인코딩**: ultrafast preset (빠른 생성)
- **애니메이션**: 줌인/줌아웃 효과

## 문제 해결

### 백엔드 서버가 시작되지 않을 때
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### 영상 생성이 실패할 때
- 뉴스 URL이 올바른지 확인
- 해당 뉴스에 이미지가 있는지 확인
- 백엔드 터미널 로그 확인

### 무한 로딩 발생 시
- 백엔드 서버(port 8000)가 실행 중인지 확인
- 브라우저 콘솔에서 에러 메시지 확인

## 기술 스택

- **Frontend**: Next.js 14, Tailwind CSS, TypeScript
- **Backend**: FastAPI, MoviePy, BeautifulSoup4, Pillow
- **Video**: 1080x1920 (9:16), 10초, 24fps, H.264

## API 엔드포인트

### POST /generate
영상 생성 요청

**Request Body:**
```json
{
  "news_url": "https://example.com/news",
  "scenario": "오늘의 뉴스입니다"
}
```

**Response:**
```json
{
  "video_url": "/download/video_20260202_123456_abc123.mp4",
  "message": "영상이 성공적으로 생성되었습니다."
}
```

### GET /download/{filename}
생성된 영상 다운로드
