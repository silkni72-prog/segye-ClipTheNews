# Keep-Alive 설정 가이드

Render 무료 플랜의 슬립 모드를 방지하기 위한 Keep-Alive 서비스 설정 방법입니다.

## 🎯 목적

- Render 무료 플랜은 15분간 요청이 없으면 슬립 모드로 전환
- Keep-Alive 서비스로 주기적으로 백엔드를 핑해서 슬립 방지
- 콜드 스타트로 인한 502/503 에러 해결

---

## 방법 1: UptimeRobot (추천) ⭐

### 장점:
- 완전 무료
- 설정 간단
- 모니터링 기능 포함

### 설정 방법:

1. **가입**
   - https://uptimerobot.com 접속
   - 무료 계정 생성

2. **모니터 추가**
   - Dashboard → **Add New Monitor** 클릭
   - 다음 정보 입력:
     ```
     Monitor Type: HTTP(s)
     Friendly Name: ClipTheNews Backend
     URL: https://segye-clipthenews.onrender.com
     Monitoring Interval: 5 minutes
     ```
   - **Create Monitor** 클릭

3. **완료!**
   - 5분마다 자동으로 백엔드를 핑
   - 백엔드가 슬립 모드로 들어가지 않음

---

## 방법 2: Cron-job.org

### 설정 방법:

1. **가입**
   - https://cron-job.org 접속
   - 무료 계정 생성

2. **Cron Job 추가**
   - **Create cronjob** 클릭
   - 다음 정보 입력:
     ```
     Title: Keep ClipTheNews Alive
     URL: https://segye-clipthenews.onrender.com
     Schedule: */5 * * * * (Every 5 minutes)
     ```
   - **Create cronjob** 클릭

---

## 방법 3: GitHub Actions (코드 기반)

`.github/workflows/keep-alive.yml` 파일 생성:

```yaml
name: Keep Backend Alive

on:
  schedule:
    # 5분마다 실행
    - cron: '*/5 * * * *'
  workflow_dispatch:

jobs:
  ping:
    runs-on: ubuntu-latest
    steps:
      - name: Ping backend
        run: |
          curl https://segye-clipthenews.onrender.com
```

**주의**: GitHub Actions는 워크플로우가 60일간 실행되지 않으면 자동 비활성화됩니다.

---

## ⚠️ 주의사항

### Render 무료 플랜 제한:
- 월 750시간 무료 (한 서비스 기준 충분)
- Keep-Alive로 계속 실행 시 월 750시간 소진
- 여러 서비스 운영 시 주의

### 권장 설정:
- **Ping 간격**: 5분 (너무 자주 하면 불필요한 리소스 사용)
- **Timeout**: 30초
- **Retry**: 비활성화 (불필요)

---

## 📊 효과

### Before (Keep-Alive 없음):
```
첫 요청 → 콜드 스타트 (30초~1분) → 502/503 에러 가능
```

### After (Keep-Alive 설정):
```
모든 요청 → 즉시 응답 (백엔드 항상 깨어있음)
```

---

## 🧪 테스트

Keep-Alive 설정 후:
1. UptimeRobot 대시보드에서 로그 확인
2. 5분 간격으로 핑이 성공하는지 확인
3. 프론트엔드에서 영상 생성 테스트
4. 502/503 에러 없이 작동하는지 확인

---

## 💰 비용

- **UptimeRobot 무료**: 50개 모니터까지
- **Cron-job.org 무료**: 무제한
- **GitHub Actions 무료**: 월 2000분 (충분)

**모두 완전 무료로 사용 가능!**

---

## 🎊 최종 구성

Keep-Alive 설정 완료 후:

```
UptimeRobot (5분마다)
    ↓
https://segye-clipthenews.onrender.com (항상 Live)
    ↑
https://frontend-beta-jet-95.vercel.app (즉시 응답)
```

콜드 스타트 문제 완전 해결! 🚀
