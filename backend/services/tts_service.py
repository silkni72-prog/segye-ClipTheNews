"""
edge-tts를 사용한 음성 생성 서비스
"""
import edge_tts
import asyncio
from pathlib import Path
from typing import Optional
import os


class TTSService:
    """Text-to-Speech 서비스"""
    
    def __init__(self, voice: str = "ko-KR-SunHiNeural"):
        """
        Args:
            voice: edge-tts 음성 이름
                   한국어: ko-KR-SunHiNeural (여성), ko-KR-InJoonNeural (남성)
        """
        self.voice = voice
    
    async def generate_async(self, text: str, output_path: str) -> str:
        """
        텍스트를 음성으로 변환 (비동기)
        
        Args:
            text: 변환할 텍스트
            output_path: 출력 파일 경로 (.mp3)
            
        Returns:
            생성된 파일 경로
        """
        try:
            communicate = edge_tts.Communicate(text, self.voice)
            await communicate.save(output_path)
            return output_path
        except Exception as e:
            raise Exception(f"TTS 생성 실패: {str(e)}")
    
    def generate(self, text: str, output_path: str) -> str:
        """
        텍스트를 음성으로 변환 (동기 래퍼)
        
        Args:
            text: 변환할 텍스트
            output_path: 출력 파일 경로 (.mp3)
            
        Returns:
            생성된 파일 경로
        """
        return asyncio.run(self.generate_async(text, output_path))
    
    async def get_audio_duration_async(self, audio_path: str) -> float:
        """
        음성 파일 길이 확인 (비동기)
        
        Args:
            audio_path: 음성 파일 경로
            
        Returns:
            길이 (초)
        """
        try:
            # ffprobe 또는 librosa 사용 가능하지만, 간단히 추정
            # 평균적으로 한국어는 분당 약 200자
            # 20초 = 약 67자
            file_size = os.path.getsize(audio_path)
            # 대략적인 추정 (mp3 기준)
            estimated_duration = file_size / 4000  # 4KB per second (approximate)
            return min(estimated_duration, 25.0)  # 최대 25초로 제한
        except:
            return 20.0  # 기본값


def generate_speech(text: str, output_path: str, voice: str = "ko-KR-SunHiNeural") -> str:
    """
    편의 함수: 음성 생성
    
    Args:
        text: 변환할 텍스트
        output_path: 출력 파일 경로
        voice: 음성 이름
        
    Returns:
        생성된 파일 경로
    """
    tts = TTSService(voice=voice)
    return tts.generate(text, output_path)
