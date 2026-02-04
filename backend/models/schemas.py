"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, Literal
from enum import Enum


class VideoMode(str, Enum):
    """영상 생성 모드"""
    NYT_QUESTION = "nyt_question"
    GUARDIAN_OBSERVE = "guardian_observe"


class JobRequest(BaseModel):
    """영상 생성 요청"""
    article_url: str = Field(..., description="뉴스 기사 URL")
    mode: VideoMode = Field(..., description="영상 생성 모드")
    
    class Config:
        json_schema_extra = {
            "example": {
                "article_url": "https://www.nytimes.com/2024/01/01/world/example.html",
                "mode": "nyt_question"
            }
        }


class JobResponse(BaseModel):
    """작업 생성 응답"""
    job_id: str = Field(..., description="작업 ID")
    status: str = Field(..., description="작업 상태")
    message: str = Field(..., description="메시지")
    
    class Config:
        json_schema_extra = {
            "example": {
                "job_id": "abc123xyz",
                "status": "queued",
                "message": "작업이 대기열에 추가되었습니다."
            }
        }


class JobStatus(BaseModel):
    """작업 상태 조회"""
    job_id: str = Field(..., description="작업 ID")
    status: str = Field(..., description="작업 상태: queued, started, finished, failed")
    progress: Optional[int] = Field(None, description="진행률 (0-100)")
    message: Optional[str] = Field(None, description="상태 메시지")
    error: Optional[str] = Field(None, description="에러 메시지 (실패 시)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "job_id": "abc123xyz",
                "status": "started",
                "progress": 60,
                "message": "영상 렌더링 중..."
            }
        }


class JobResult(BaseModel):
    """작업 결과"""
    job_id: str = Field(..., description="작업 ID")
    status: str = Field(..., description="작업 상태")
    video_url: Optional[str] = Field(None, description="영상 다운로드 URL")
    thumbnail_url: Optional[str] = Field(None, description="썸네일 URL (추후 지원)")
    duration: Optional[float] = Field(None, description="처리 시간 (초)")
    error: Optional[str] = Field(None, description="에러 메시지")
    
    class Config:
        json_schema_extra = {
            "example": {
                "job_id": "abc123xyz",
                "status": "finished",
                "video_url": "/download/abc123xyz.mp4",
                "duration": 45.2
            }
        }
