"""
Configuration settings for the backend application
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).parent

# Output directories
OUTPUT_DIR = BASE_DIR / "output"
TEMP_DIR = BASE_DIR / "temp"

# 디렉토리 생성
OUTPUT_DIR.mkdir(exist_ok=True)
TEMP_DIR.mkdir(exist_ok=True)

# Redis configuration
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))
REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

# API Keys (optional for enhanced features)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Video settings
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
VIDEO_DURATION = 20  # seconds
VIDEO_FPS = 30

# Subtitle settings
SUBTITLE_FONT_SIZE = 48
SUBTITLE_POSITION = 0.75  # 75% from top (하단 25%)
SUBTITLE_BG_COLOR = "black"
SUBTITLE_TEXT_COLOR = "white"

# Stock video placeholder (solid colors)
FALLBACK_COLORS = [
    "#1e3a8a",  # Navy blue
    "#1e40af",  # Blue
    "#1e293b",  # Slate
]

# TTS settings
TTS_VOICE = "ko-KR-SunHiNeural"  # edge-tts 한국어 음성
TTS_RATE = "+0%"  # 속도 조절

# Job expiry time (seconds)
JOB_RESULT_TTL = 3600  # 1 hour
JOB_TIMEOUT = 600  # 10 minutes
