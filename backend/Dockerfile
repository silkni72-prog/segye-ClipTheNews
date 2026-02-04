# Python 3.11 base image
FROM python:3.11-slim

# ffmpeg 설치 (영상 처리 필수)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리
WORKDIR /app

# 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# 출력 디렉토리 생성
RUN mkdir -p output temp

# 포트 노출 (Render는 동적 포트 사용)
EXPOSE 8000

# 시작 명령어 (Render 호환)
# Render는 $PORT 환경 변수를 제공
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
