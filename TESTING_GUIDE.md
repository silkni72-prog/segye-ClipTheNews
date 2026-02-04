# 테스트 가이드 - 프론트엔드-백엔드 연동

## ✅ 구현 완료 사항

다음 파일들이 수정되었습니다:

1. `.env.local` - 백엔드 URL 설정
2. `app/api/generate/route.ts` - 백엔드 API 연동 및 폴링 로직
3. `components/VideoForm.tsx` - 영상 플레이어 및 상태 표시 UI

## 🚀 백엔드 실행 방법

### 1단계: Redis 시작

새 터미널을 열고:

```powershell
# Docker로 Redis 실행
docker run -d -p 6379:6379 redis:7-alpine
```

**확인**: Redis가 실행 중인지 확인
```powershell
docker ps
```

### 2단계: Python 백엔드 실행

새 터미널을 열고:

```powershell
cd backend
python main.py
```

백엔드가 http://localhost:8000 에서 실행됩니다.

**확인**: 브라우저에서 http://localhost:8000 접속
- "ClipTheNews API" 메시지가 보이면 성공!

### 3단계: Worker 실행

또 다른 새 터미널을 열고:

```powershell
cd backend
python worker.py
```

Worker가 작업 큐를 모니터링합니다.

## 🧪 테스트 방법

### 프론트엔드에서 테스트

1. 브라우저에서 http://localhost:3000/generate 접속
2. 뉴스 URL 입력 (예: https://www.segye.com/newsView/20260202515616)
3. 영상 스타일 선택 (질문형 또는 관찰형)
4. "영상 생성하기" 버튼 클릭

**예상 동작**:
- 로딩 스피너와 진행 단계 표시
- 30~60초 후 영상 생성 완료
- 영상 플레이어에서 재생 가능
- 다운로드 버튼으로 저장 가능

### 백엔드 직접 테스트 (선택사항)

```powershell
# 테스트 스크립트 실행
python test_api.py
```

## 🔍 실행 상태 확인

### 필수 프로세스 체크리스트

- [ ] Redis 실행 중 (포트 6379)
- [ ] Python 백엔드 실행 중 (포트 8000)
- [ ] Python Worker 실행 중
- [ ] Next.js 프론트엔드 실행 중 (포트 3000)

### 터미널 구성

총 3개의 터미널이 필요합니다:

```
터미널 1: Redis (Docker)
터미널 2: Python 백엔드 (backend/main.py)
터미널 3: Python Worker (backend/worker.py)

기존 터미널: Next.js 프론트엔드 (이미 실행 중)
```

## 🐛 문제 해결

### 1. "백엔드 서버에 연결할 수 없습니다" 오류

**원인**: 백엔드가 실행되지 않았거나 포트가 다름

**해결**:
1. 백엔드가 실행 중인지 확인: http://localhost:8000
2. `.env.local` 파일의 `NEXT_PUBLIC_BACKEND_URL` 확인
3. 백엔드 터미널 로그 확인

### 2. "Redis 연결 실패" 오류

**원인**: Redis가 실행되지 않음

**해결**:
```powershell
# Redis 상태 확인
docker ps | findstr redis

# Redis 재시작
docker run -d -p 6379:6379 redis:7-alpine
```

### 3. 영상이 생성되지 않음

**원인**: Worker가 실행되지 않음

**해결**:
1. Worker 터미널 확인
2. Worker 로그에서 에러 확인
3. Worker 재시작

### 4. FFmpeg 관련 오류

**원인**: FFmpeg가 설치되지 않음

**해결**:
```powershell
# Windows (Chocolatey)
choco install ffmpeg

# 또는 수동 설치: https://ffmpeg.org/download.html
```

## 📊 백엔드 API 엔드포인트

- `GET /` - 서버 상태 확인
- `POST /jobs` - 영상 생성 작업 생성
- `GET /status/{job_id}` - 작업 상태 조회
- `GET /result/{job_id}` - 작업 결과 조회
- `GET /download/{filename}` - 영상 다운로드
- `GET /health` - 헬스 체크

## 🎯 예상 처리 시간

| 단계 | 소요 시간 |
|------|-----------|
| 기사 파싱 | 5-10초 |
| 스크립트 생성 | 3-5초 |
| 음성 합성 (TTS) | 5-10초 |
| 영상 렌더링 | 15-35초 |
| **총 예상 시간** | **30-60초** |

## 📝 로그 확인

### 프론트엔드 로그
- 브라우저 개발자 도구 → Console 탭
- Next.js 터미널

### 백엔드 로그
- Python 백엔드 터미널
- Worker 터미널

### 유용한 로그 메시지
```
[job_id] 작업 시작
[job_id] [1/4] 기사 파싱 중...
[job_id] [2/4] 스크립트 생성 중...
[job_id] [3/4] 음성 생성 중...
[job_id] [4/4] 영상 렌더링 중...
[job_id] ✓ 영상 렌더링 완료
```

## 🎉 성공 확인

영상이 생성되고 다음 항목이 모두 표시되면 성공입니다:

- ✅ "영상이 생성되었습니다!" 메시지
- ✅ 비디오 플레이어에 영상 표시
- ✅ 재생 가능
- ✅ 다운로드 버튼 작동

## 📚 추가 문서

- [QUICKSTART.md](QUICKSTART.md) - 빠른 시작 가이드
- [BACKEND_README.md](BACKEND_README.md) - 백엔드 상세 문서
- [DEPLOYMENT.md](DEPLOYMENT.md) - 배포 가이드

---

**문제가 계속 발생하면 GitHub Issues에 다음 정보와 함께 등록해주세요:**
1. 오류 메시지
2. 터미널 로그
3. 브라우저 콘솔 로그
