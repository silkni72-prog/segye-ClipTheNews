from pydantic import BaseModel, HttpUrl
from typing import Optional

class VideoRequest(BaseModel):
    news_url: str
    scenario: Optional[str] = ""  # 선택사항, 기본값은 빈 문자열

class VideoResponse(BaseModel):
    video_url: str
    message: str
