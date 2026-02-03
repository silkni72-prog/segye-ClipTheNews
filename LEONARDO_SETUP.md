# Leonardo.ai API 설정 가이드

AI 이미지 생성 기능을 사용하려면 Leonardo.ai API 키가 필요합니다.

## 🎯 Leonardo.ai란?

Leonardo.ai는 AI 이미지 생성 서비스로, 텍스트 프롬프트를 입력하면 고품질 이미지를 생성합니다.

**무료 플랜:**
- 하루 150 토큰
- 약 30-40개 이미지 생성 가능
- **하루 7-10개 영상 무료 생성**

---

## 📋 API 키 발급 방법

### 1단계: 회원가입

1. https://leonardo.ai 접속
2. **Sign Up** 클릭
3. 이메일 또는 Google 계정으로 가입

### 2단계: API 키 생성

1. 로그인 후 우측 상단 프로필 아이콘 클릭
2. **Settings** (설정) 선택
3. 좌측 메뉴에서 **API Access** 클릭
4. **Generate API Key** 버튼 클릭
5. API 키 복사 (한 번만 표시되므로 반드시 복사!)

### 3단계: .env 파일 설정

1. `backend/.env` 파일 열기 (없으면 생성)
2. 다음 라인 추가:

```env
# Leonardo.ai API Key
LEONARDO_API_KEY=your_leonardo_api_key_here
```

3. `your_leonardo_api_key_here` 부분을 복사한 API 키로 교체

**예시:**
```env
LEONARDO_API_KEY=sk-1234567890abcdef1234567890abcdef
```

---

## ✅ 설정 확인

### 방법 1: 백엔드 로그 확인

영상 생성 시 백엔드 로그에서 확인:

```
[Step 2/3] Trying Leonardo AI for 2 more images...
[INFO] Requesting AI image generation...
[INFO] Prompt: business meeting in modern office...
[OK] AI image generated and saved: ai_image_2_abc123.jpg
```

### 방법 2: 에러 메시지 확인

API 키가 없거나 잘못된 경우:

```
[WARN] LEONARDO_API_KEY not found. Skipping AI image generation.
[INFO] To use AI image generation, set LEONARDO_API_KEY in .env file
```

---

## 🎬 이미지 수집 우선순위

ClipTheNews는 하이브리드 방식으로 이미지를 수집합니다:

```
1순위: 뉴스 기사 이미지 (무료)
    ↓ (부족하면)
2순위: Unsplash 스톡 이미지 (무료, 최대 2개)
    ↓ (여전히 부족하면)
3순위: Leonardo AI 생성 이미지 (토큰 소비)
```

**목표:** 4개 이미지 (20초 영상용)

---

## 💰 비용 및 사용량

### 무료 플랜
- **하루 150 토큰**
- 이미지당 약 4-5 토큰 소비
- **하루 30-40개 이미지 생성 가능**

### 영상 생성 시나리오

#### 시나리오 1: 뉴스 이미지 풍부
- 뉴스 이미지: 4개
- AI 생성: 0개
- **비용: 무료**

#### 시나리오 2: 뉴스 이미지 부족
- 뉴스 이미지: 2개
- Unsplash: 2개 (무료)
- AI 생성: 0개
- **비용: 무료**

#### 시나리오 3: 뉴스 이미지 없음
- 뉴스 이미지: 0개
- Unsplash: 2개 (무료)
- AI 생성: 2개
- **비용: 약 10 토큰**
- **하루 15개 영상까지 무료**

### 유료 플랜 (선택사항)
- **Apprentice Standard**: $10/월 (8,500 토큰)
- **Artisan Unlimited**: $24/월 (25,000 토큰)

---

## 🔧 트러블슈팅

### Q: API 키를 입력했는데 작동하지 않아요

**확인사항:**
1. `.env` 파일이 `backend/` 폴더에 있는지 확인
2. `LEONARDO_API_KEY=` 앞에 공백이 없는지 확인
3. API 키 양 끝에 따옴표가 없는지 확인
4. **백엔드 서버 재시작** (중요!)

```bash
# PowerShell
cd backend
..\backend\venv\Scripts\python.exe -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Q: "Invalid Leonardo API key" 오류가 나요

**해결방법:**
1. Leonardo.ai 웹사이트에서 API 키 재확인
2. 새 API 키 생성
3. `.env` 파일 업데이트
4. 백엔드 재시작

### Q: "Rate limit exceeded" 오류가 나요

**해결방법:**
- 무료 토큰을 모두 소진한 경우
- 내일까지 기다리거나 유료 플랜 업그레이드

### Q: 이미지 생성이 너무 느려요

**정상 속도:**
- 이미지당 약 5-20초 소요
- 2개 이미지 생성 시 총 10-40초

**개선 방법:**
- Unsplash API 키도 함께 설정 (Leonardo 사용 줄임)
- 뉴스 이미지가 많은 기사 선택

---

## 📊 사용량 모니터링

### Leonardo.ai 대시보드에서 확인

1. https://leonardo.ai 로그인
2. 우측 상단 프로필 → **API Access**
3. **Usage** 탭에서 확인:
   - 오늘 사용한 토큰
   - 남은 토큰
   - 생성된 이미지 수

### 백엔드 로그에서 확인

영상 생성 완료 시 메시지:
```
영상이 성공적으로 생성되었습니다. (뉴스: 2개, 스톡: 1개, AI생성: 1개)
```

---

## 🎨 프롬프트 커스터마이징 (고급)

AI 생성 이미지 스타일을 변경하고 싶다면:

`backend/services/ai_image_prompt_generator.py` 수정

```python
# 경제 뉴스용 프롬프트 예시
if '경제' in title:
    prompts = [
        f"business meeting, office, {base_style}",
        f"stock chart, financial data, {base_style}",
        # 여기에 원하는 프롬프트 추가
    ]
```

---

## 📚 추가 리소스

- [Leonardo.ai 공식 문서](https://docs.leonardo.ai/)
- [API 레퍼런스](https://docs.leonardo.ai/reference/introduction)
- [커뮤니티 디스코드](https://discord.gg/leonardo-ai)

---

## ❓ 자주 묻는 질문

### Leonardo AI 없이도 사용 가능한가요?

**네!** Leonardo API 키가 없어도 서비스는 정상 작동합니다:
- 뉴스 이미지 + Unsplash 이미지로 영상 생성
- 단, 이미지가 부족한 경우 영상 생성 실패 가능

### 다른 AI 이미지 서비스도 추가할 수 있나요?

**가능합니다!** 비슷한 방식으로:
- DALL-E 3 (OpenAI)
- Stable Diffusion (Stability AI)
- Midjourney (API 없음)

구현이 필요하면 요청하세요!

---

## 📞 지원

문제가 해결되지 않으면:
1. GitHub Issues에 문의
2. 백엔드 로그 전체를 첨부
3. `.env` 파일 내용 (API 키는 가림)
