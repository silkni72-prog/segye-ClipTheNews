# 하이브리드 이미지 시스템 가이드

## 🎨 개요

ClipTheNews는 **하이브리드 이미지 수집 시스템**을 사용합니다:

1. **우선**: 뉴스 기사에서 이미지 스크래핑
2. **보충**: 부족하면 Unsplash API로 관련 스톡 이미지 자동 추가

이를 통해 항상 충분한 이미지로 영상을 생성할 수 있습니다!

---

## ⚙️ Unsplash API 설정

### 1단계: API 키 발급

1. **Unsplash Developers 접속**  
   https://unsplash.com/developers

2. **회원가입/로그인**  
   GitHub 계정으로 간편 로그인 가능

3. **새 앱 만들기**
   - "Your apps" → "New Application" 클릭
   - 이용 약관 동의
   - 앱 이름 입력 (예: "ClipTheNews")
   - 설명 입력 (예: "News video generator")

4. **Access Key 복사**
   - 생성된 앱 페이지에서 "Access Key" 확인
   - 긴 문자열을 복사

### 2단계: 환경변수 설정

#### Windows (PowerShell)
```bash
cd backend
echo UNSPLASH_ACCESS_KEY=여기에_복사한_키_붙여넣기 > .env
```

#### 수동으로 만들기
1. `backend` 폴더에 `.env` 파일 생성
2. 다음 내용 입력:
```
UNSPLASH_ACCESS_KEY=여기에_복사한_키_붙여넣기
```

### 3단계: 서버 재시작

```bash
# 백엔드 서버 재시작 (uvicorn --reload면 자동)
# 또는 Ctrl+C로 종료 후 다시 실행
python -m uvicorn main:app --reload --port 8000
```

---

## 🔍 작동 방식

### 시나리오 1: 뉴스에 충분한 이미지가 있을 때

```
[뉴스 URL 입력]
    ↓
[Step 1] 뉴스 스크래핑 → 2개 이미지 발견
    ↓
[Step 2] Unsplash 건너뛰기 (이미 충분함)
    ↓
[Step 3] 영상 생성 (뉴스 이미지 2개 사용)
```

### 시나리오 2: 뉴스에 이미지가 부족할 때

```
[뉴스 URL 입력]
    ↓
[Step 1] 뉴스 스크래핑 → 1개만 발견
    ↓
[Step 2] Unsplash API 호출
    - 제목에서 키워드 추출 ("경제" → "economy business")
    - Unsplash 검색 → 1개 추가 다운로드
    ↓
[Step 3] 영상 생성 (뉴스 1개 + Unsplash 1개)
```

### 시나리오 3: 뉴스에 이미지가 전혀 없을 때

```
[뉴스 URL 입력]
    ↓
[Step 1] 뉴스 스크래핑 → 0개 발견
    ↓
[Step 2] Unsplash API 호출
    - 제목에서 키워드 추출
    - Unsplash 검색 → 2개 다운로드
    ↓
[Step 3] 영상 생성 (Unsplash 2개 사용)
```

---

## 🎯 키워드 매핑

제목에서 자동으로 키워드를 추출하여 관련 이미지를 검색합니다:

| 한국어 제목 키워드 | Unsplash 검색 키워드 |
|-------------------|---------------------|
| 경제, 금융 | economy business |
| 정치, 대통령 | politics government |
| 기술, IT | technology innovation |
| 스포츠, 축구 | sports, soccer |
| 환경, 날씨 | environment nature |
| 건강, 의료 | health medical |
| 문화, 영화 | culture, movie |
| 부동산 | real estate |
| 주식, 증시 | stock market |

*더 많은 키워드는 `backend/services/stock_image.py` 참조*

---

## 📊 로그 확인

백엔드 터미널에서 다음과 같은 로그를 확인할 수 있습니다:

```
[Step 1/3] Scraping news from: https://example.com/news
✓ Scraped 1 images from news
✓ Title: 경제 성장률 3% 돌파

[Step 2/3] Need 1 more images. Fetching from Unsplash...
Keyword matched: 경제 → economy business
Searching Unsplash for: economy business
Downloaded Unsplash image: unsplash_abc123_0.jpg
✓ Added 1 stock images from Unsplash

✓ Total images for video: 2

[Step 3/3] Generating video...
✓ Video generated: video_20260202_140512_xyz789.mp4
```

---

## ❓ 문제 해결

### Q: "UNSPLASH_ACCESS_KEY not found" 경고가 뜹니다

**A**: `.env` 파일을 확인하세요:
- 파일 위치: `backend/.env`
- 파일명이 정확한지 확인 (`.env`가 맞음, `.env.txt` 아님)
- API 키가 올바르게 입력되었는지 확인

### Q: Unsplash에서 이미지를 못 가져옵니다

**A**: 다음을 확인하세요:
1. API 키가 유효한지 확인
2. 인터넷 연결 확인
3. Unsplash API 사용량 제한 확인 (무료 플랜: 50 requests/hour)

### Q: API 키 없이도 작동하나요?

**A**: 네! API 키가 없으면 뉴스 이미지만 사용합니다.
- 뉴스에 이미지가 있으면 → 정상 작동
- 뉴스에 이미지가 없으면 → 에러 (이 경우 API 키 필요)

---

## 💰 Unsplash API 제한

### 무료 플랜 (Demo)
- **요청 제한**: 50 requests/hour
- **상업적 사용**: 불가
- **개인 프로젝트용**: 충분함

### Production 플랜 (승인 필요)
- **요청 제한**: 5,000 requests/hour
- **상업적 사용**: 가능
- **신청**: https://unsplash.com/api

---

## 🎬 테스트 방법

1. `.env` 파일에 API 키 설정
2. 백엔드 서버 재시작
3. 이미지가 없는 뉴스 URL 입력 (예: 텍스트만 있는 기사)
4. 로그 확인:
   ```
   [Step 2/3] Fetching from Unsplash...
   ✓ Added X stock images from Unsplash
   ```
5. 생성된 영상 확인 → Unsplash 이미지 포함됨

---

## 📝 추가 개선 아이디어

현재는 Unsplash만 지원하지만, 향후 확장 가능:

- **Pexels API**: 또 다른 무료 스톡 이미지 소스
- **OpenAI DALL-E**: AI 생성 이미지 (유료)
- **Stable Diffusion**: 로컬 AI 이미지 생성
- **Google Images**: 웹 크롤링 (저작권 주의)

관심 있으시면 말씀해주세요!
