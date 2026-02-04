# ClipTheNews - 시스템 아키텍처

## 전체 구조

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Frontend  │────▶│   FastAPI    │────▶│    Redis    │
│  (Next.js)  │     │   Backend    │     │   (Queue)   │
└─────────────┘     └──────────────┘     └─────────────┘
                           │                      │
                           │                      │
                           ▼                      ▼
                    ┌──────────────┐     ┌─────────────┐
                    │  File System │     │  RQ Worker  │
                    │   (output/)  │◀────│ (Background)│
                    └──────────────┘     └─────────────┘
```

## 컴포넌트 설명

### 1. FastAPI Backend (main.py)

**역할**: REST API 서버

**엔드포인트**:
- `POST /jobs`: 영상 생성 작업 요청
- `GET /status/{job_id}`: 작업 상태 조회
- `GET /result/{job_id}`: 작업 결과 조회
- `GET /download/{filename}`: 영상 다운로드
- `GET /health`: 헬스 체크

**기술**:
- FastAPI (비동기 웹 프레임워크)
- Redis 연결 (작업 큐)
- CORS 미들웨어

### 2. Redis Queue

**역할**: 작업 큐 및 상태 관리

**사용**:
- RQ (Redis Queue) 라이브러리
- 작업 대기열 관리
- 작업 상태 추적
- 결과 캐싱 (1시간 TTL)

### 3. RQ Worker (worker.py)

**역할**: 백그라운드 작업 처리

**프로세스**:
1. Redis에서 작업 가져오기
2. `render_job()` 함수 실행
3. 결과를 Redis에 저장
4. 다음 작업 대기

**특징**:
- 비동기 처리
- 타임아웃 관리 (10분)
- 오류 핸들링 및 폴백

### 4. Render Task (tasks/render_task.py)

**역할**: 실제 영상 생성 로직

**단계**:
```
1. 기사 파싱 (scraper.py)
   ↓
2. 스크립트 생성 (script_generator.py)
   ↓
3. 음성 합성 (tts_service.py)
   ↓
4. 영상 렌더링 (video_service.py)
   ↓
5. 결과 반환
```

## 서비스 모듈

### scraper.py
- 뉴스 사이트별 파싱 로직
- NYTimes, Guardian 특화 파서
- Generic 파서 (범용)

### script_generator.py
- OpenAI GPT 기반 스크립트 생성
- 템플릿 기반 폴백 (API 없을 때)
- 모드별 스타일 (question/observe)
- 20초 분량, 3구간 구성

### tts_service.py
- edge-tts 사용
- 한국어 음성 (ko-KR-SunHiNeural)
- 비동기 처리
- MP3 출력

### video_service.py
- ffmpeg 기반 영상 생성
- 1080x1920 세로 영상
- 3개 클립 연결
- SRT 자막 오버레이
- 단색 배경 폴백

## 데이터 플로우

### 1. 작업 생성
```
Client → POST /jobs → FastAPI
                       ↓
                   RQ enqueue
                       ↓
                   Redis Queue
```

### 2. 작업 처리
```
Worker → Redis Queue (dequeue)
  ↓
render_job()
  ├─ scraper → 기사 데이터
  ├─ script_generator → 스크립트
  ├─ tts_service → audio.mp3
  └─ video_service → video.mp4
       ↓
  Redis (결과 저장)
```

### 3. 결과 조회
```
Client → GET /result/{job_id} → FastAPI
                                  ↓
                              Redis (조회)
                                  ↓
                            video_url 반환
```

### 4. 다운로드
```
Client → GET /download/{filename} → FastAPI
                                     ↓
                                 FileResponse
                                     ↓
                               output/{file}
```

## 파일 시스템

```
backend/
├── output/              # 생성된 영상 저장
│   └── {job_id}.mp4
├── temp/                # 임시 파일 (자동 삭제)
│   ├── {job_id}_audio.mp3
│   ├── solid_bg_*.png
│   └── clip_*.mp4
```

## 에러 처리

### 1. 작업 레벨
- 각 단계마다 try-catch
- 실패 시 폴백 시도
- 최종 실패 시 에러 메시지 반환

### 2. 폴백 전략
```
기사 파싱 실패 → 에러 반환 (필수)
스크립트 생성 실패 → 템플릿 사용
음성 합성 실패 → 에러 반환 (필수)
영상 렌더링 실패 → 단색 배경 사용
```

### 3. Redis 장애
- 연결 실패 시 503 에러
- 재연결 시도 없음 (외부 관리)

## 성능 최적화

### 1. 비동기 처리
- FastAPI 비동기 엔드포인트
- RQ 백그라운드 작업
- 클라이언트 즉시 응답

### 2. 리소스 관리
- 임시 파일 자동 삭제
- Redis TTL (1시간)
- 작업 타임아웃 (10분)

### 3. 확장성
- Worker 수평 확장 가능
- Redis 클러스터 지원
- 여러 Worker 동시 실행

## 보안

### 1. 입력 검증
- URL 형식 검증
- Pydantic 스키마 검증
- 파일명 새니타이징

### 2. CORS
- 허용 도메인 제한
- 프론트엔드만 접근 가능

### 3. 파일 시스템
- 출력 디렉토리 제한
- 경로 탐색 방지

## 모니터링

### 헬스 체크
```
GET /health
{
  "status": "healthy",
  "redis": "connected",
  "queue_size": 3
}
```

### 로그
- Worker 표준 출력
- 각 작업 단계별 로그
- 에러 스택 트레이스

## 배포 옵션

### 1. Docker Compose
- Redis, Backend, Worker 통합
- 로컬 개발 및 테스트용
- 간편한 설정

### 2. 로컬 실행
- Python venv
- Redis 별도 실행
- 개발 및 디버깅용

### 3. 프로덕션 배포
- Redis 별도 호스팅
- Backend: Render/Railway/Fly.io
- Worker: 백그라운드 서비스
- 파일 저장: S3/Cloud Storage

## 확장 계획

### 1. 성능 개선
- [ ] 병렬 처리 (스크립트 + 음성)
- [ ] 캐싱 (동일 기사)
- [ ] CDN 연동

### 2. 기능 추가
- [ ] 실제 스톡 영상 통합
- [ ] 다양한 음성 선택
- [ ] 자막 스타일 커스터마이징
- [ ] 썸네일 자동 생성

### 3. 모니터링
- [ ] Prometheus 메트릭
- [ ] Sentry 에러 추적
- [ ] 작업 성공률 대시보드

## 기술 스택 요약

| 레이어 | 기술 |
|--------|------|
| API | FastAPI, Pydantic |
| Queue | Redis, RQ |
| Scraping | BeautifulSoup, Requests |
| AI | OpenAI GPT-3.5 |
| TTS | edge-tts |
| Video | ffmpeg, Pillow |
| Container | Docker, Docker Compose |

---

**Last Updated**: 2026-02-04
