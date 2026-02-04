"""
ffmpeg를 사용한 영상 생성 서비스
1080x1920 세로 영상, 3개 클립, 자막 포함
"""
import subprocess
import os
from pathlib import Path
from typing import List, Dict, Optional
from PIL import Image, ImageDraw, ImageFont
import json


class VideoService:
    """영상 생성 서비스"""
    
    def __init__(self, width: int = 1080, height: int = 1920, fps: int = 30):
        self.width = width
        self.height = height
        self.fps = fps
    
    def create_video(
        self,
        video_clips: List[str],
        audio_path: str,
        subtitles: List[Dict],
        output_path: str,
        duration: float = 20.0
    ) -> str:
        """
        영상 생성
        
        Args:
            video_clips: 영상 클립 파일 경로 리스트 (3개, placeholder 가능)
            audio_path: 음성 파일 경로
            subtitles: 자막 데이터 [{'text': str, 'start': float, 'duration': float}]
            output_path: 출력 파일 경로
            duration: 영상 길이 (초)
            
        Returns:
            생성된 파일 경로
        """
        try:
            # 1. 영상 클립 준비 (3개 구간)
            clip_duration = duration / 3
            prepared_clips = []
            
            for i in range(3):
                if i < len(video_clips) and os.path.exists(video_clips[i]):
                    # 실제 영상 파일 사용
                    clip_path = self._prepare_video_clip(video_clips[i], clip_duration)
                else:
                    # Placeholder: 단색 배경 생성
                    clip_path = self._create_solid_background(i, clip_duration)
                
                prepared_clips.append(clip_path)
            
            # 2. 클립 연결
            concat_path = self._concatenate_clips(prepared_clips, duration)
            
            # 3. 자막 오버레이
            subtitle_path = self._create_subtitle_file(subtitles)
            
            # 4. 최종 영상 생성 (영상 + 음성 + 자막)
            self._merge_audio_and_subtitles(concat_path, audio_path, subtitle_path, output_path)
            
            # 임시 파일 정리
            for clip in prepared_clips:
                if os.path.exists(clip):
                    os.remove(clip)
            if os.path.exists(concat_path):
                os.remove(concat_path)
            if os.path.exists(subtitle_path):
                os.remove(subtitle_path)
            
            return output_path
            
        except Exception as e:
            raise Exception(f"영상 생성 실패: {str(e)}")
    
    def _prepare_video_clip(self, input_path: str, duration: float) -> str:
        """영상 클립을 1080x1920으로 리사이즈 및 트림"""
        temp_dir = Path(input_path).parent / "temp"
        temp_dir.mkdir(exist_ok=True)
        output_path = str(temp_dir / f"clip_{Path(input_path).stem}_resized.mp4")
        
        cmd = [
            "ffmpeg", "-y",
            "-i", input_path,
            "-vf", f"scale={self.width}:{self.height}:force_original_aspect_ratio=increase,crop={self.width}:{self.height}",
            "-t", str(duration),
            "-r", str(self.fps),
            "-an",  # 오디오 제거
            output_path
        ]
        
        subprocess.run(cmd, check=True, capture_output=True)
        return output_path
    
    def _create_solid_background(self, index: int, duration: float) -> str:
        """단색 배경 영상 생성 (placeholder)"""
        from config import FALLBACK_COLORS, TEMP_DIR
        
        # 색상 선택
        color = FALLBACK_COLORS[index % len(FALLBACK_COLORS)]
        
        # 이미지 생성
        img = Image.new('RGB', (self.width, self.height), color)
        img_path = str(TEMP_DIR / f"solid_bg_{index}.png")
        img.save(img_path)
        
        # ffmpeg로 영상 생성
        output_path = str(TEMP_DIR / f"solid_clip_{index}.mp4")
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1",
            "-i", img_path,
            "-t", str(duration),
            "-r", str(self.fps),
            "-vf", f"scale={self.width}:{self.height}",
            "-pix_fmt", "yuv420p",
            output_path
        ]
        
        subprocess.run(cmd, check=True, capture_output=True)
        
        # 임시 이미지 삭제
        if os.path.exists(img_path):
            os.remove(img_path)
        
        return output_path
    
    def _concatenate_clips(self, clips: List[str], total_duration: float) -> str:
        """여러 클립을 하나로 연결"""
        from config import TEMP_DIR
        
        # concat 파일 생성
        concat_file = str(TEMP_DIR / "concat_list.txt")
        with open(concat_file, 'w') as f:
            for clip in clips:
                f.write(f"file '{clip}'\n")
        
        output_path = str(TEMP_DIR / "concatenated.mp4")
        cmd = [
            "ffmpeg", "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", concat_file,
            "-c", "copy",
            output_path
        ]
        
        subprocess.run(cmd, check=True, capture_output=True)
        
        if os.path.exists(concat_file):
            os.remove(concat_file)
        
        return output_path
    
    def _create_subtitle_file(self, subtitles: List[Dict]) -> str:
        """SRT 자막 파일 생성"""
        from config import TEMP_DIR
        
        srt_path = str(TEMP_DIR / "subtitles.srt")
        
        with open(srt_path, 'w', encoding='utf-8') as f:
            for i, sub in enumerate(subtitles, 1):
                start_time = sub['start_time']
                duration = sub['duration']
                end_time = start_time + duration
                
                # SRT 시간 형식: 00:00:00,000
                start_str = self._format_srt_time(start_time)
                end_str = self._format_srt_time(end_time)
                
                f.write(f"{i}\n")
                f.write(f"{start_str} --> {end_str}\n")
                f.write(f"{sub['text']}\n\n")
        
        return srt_path
    
    def _format_srt_time(self, seconds: float) -> str:
        """초를 SRT 시간 형식으로 변환"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
    
    def _merge_audio_and_subtitles(
        self,
        video_path: str,
        audio_path: str,
        subtitle_path: str,
        output_path: str
    ):
        """영상에 음성과 자막 추가"""
        # 자막 스타일: 하단 25% 위치, 검은 배경, 흰색 텍스트
        subtitle_filter = (
            f"subtitles={subtitle_path}:force_style='"
            f"Alignment=2,"  # 하단 중앙
            f"MarginV=50,"  # 하단 여백
            f"FontSize=32,"
            f"PrimaryColour=&H00FFFFFF,"  # 흰색
            f"OutlineColour=&H00000000,"  # 검은 테두리
            f"Outline=2,"
            f"BackColour=&H80000000,"  # 반투명 검은 배경
            f"BorderStyle=4'"  # 박스 스타일
        )
        
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-i", audio_path,
            "-vf", subtitle_filter,
            "-c:v", "libx264",
            "-c:a", "aac",
            "-shortest",
            "-pix_fmt", "yuv420p",
            output_path
        ]
        
        subprocess.run(cmd, check=True, capture_output=True)


def create_video(
    video_clips: List[str],
    audio_path: str,
    subtitles: List[Dict],
    output_path: str,
    duration: float = 20.0
) -> str:
    """
    편의 함수: 영상 생성
    """
    service = VideoService()
    return service.create_video(video_clips, audio_path, subtitles, output_path, duration)
