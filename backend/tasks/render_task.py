"""
RQ 백그라운드 작업: 영상 렌더링
"""
import os
import uuid
from pathlib import Path
import traceback
from typing import Dict
import time

from services.scraper import scrape_article
from services.script_generator import generate_script
from services.tts_service import generate_speech
from services.video_service import create_video
from config import OUTPUT_DIR, TEMP_DIR, TTS_VOICE


def render_job(job_id: str, article_url: str, mode: str) -> Dict:
    """
    영상 렌더링 작업 (RQ 워커에서 실행)
    
    Args:
        job_id: 작업 ID
        article_url: 기사 URL
        mode: 'nyt_question' or 'guardian_observe'
        
    Returns:
        {
            'status': 'success' or 'failed',
            'video_path': str (성공 시),
            'error': str (실패 시),
            'duration': float (처리 시간)
        }
    """
    start_time = time.time()
    temp_files = []
    
    try:
        print(f"[{job_id}] 작업 시작: {article_url} (mode: {mode})")
        
        # 1. 기사 파싱
        print(f"[{job_id}] [1/4] 기사 파싱 중...")
        article_data = scrape_article(article_url)
        
        if not article_data.get('title'):
            raise Exception("기사 제목을 찾을 수 없습니다.")
        
        print(f"[{job_id}] ✓ 제목: {article_data['title'][:50]}...")
        
        # 2. 스크립트 생성 (20초)
        print(f"[{job_id}] [2/4] 스크립트 생성 중...")
        script_data = generate_script(article_data, mode)
        
        print(f"[{job_id}] ✓ 스크립트: {script_data['script'][:50]}...")
        print(f"[{job_id}] ✓ 구간 수: {len(script_data['segments'])}")
        
        # 3. 음성 생성 (edge-tts)
        print(f"[{job_id}] [3/4] 음성 생성 중...")
        audio_filename = f"{job_id}_audio.mp3"
        audio_path = str(TEMP_DIR / audio_filename)
        temp_files.append(audio_path)
        
        generate_speech(
            text=script_data['script'],
            output_path=audio_path,
            voice=TTS_VOICE
        )
        
        if not os.path.exists(audio_path):
            raise Exception("음성 파일 생성 실패")
        
        print(f"[{job_id}] ✓ 음성 생성 완료")
        
        # 4. 영상 생성 (ffmpeg)
        print(f"[{job_id}] [4/4] 영상 렌더링 중...")
        
        # 영상 클립: 여기서는 placeholder (단색 배경) 사용
        # 실제 스톡 영상을 사용하려면 video_clips 리스트에 경로 추가
        video_clips = []  # 빈 리스트 = 단색 배경 사용
        
        # 자막 데이터 준비
        subtitles = []
        for seg in script_data['segments']:
            subtitles.append({
                'text': seg['text'],
                'start_time': seg['start_time'],
                'duration': seg['duration']
            })
        
        # 출력 파일
        output_filename = f"{job_id}.mp4"
        output_path = str(OUTPUT_DIR / output_filename)
        
        create_video(
            video_clips=video_clips,
            audio_path=audio_path,
            subtitles=subtitles,
            output_path=output_path,
            duration=script_data['duration']
        )
        
        if not os.path.exists(output_path):
            raise Exception("영상 파일 생성 실패")
        
        print(f"[{job_id}] ✓ 영상 렌더링 완료: {output_filename}")
        
        # 처리 시간 계산
        duration = time.time() - start_time
        
        # 임시 파일 정리
        _cleanup_temp_files(temp_files)
        
        return {
            'status': 'success',
            'video_path': output_filename,
            'duration': round(duration, 2)
        }
        
    except Exception as e:
        error_msg = str(e)
        print(f"[{job_id}] ✗ 오류 발생: {error_msg}")
        traceback.print_exc()
        
        # 임시 파일 정리
        _cleanup_temp_files(temp_files)
        
        # 실패 시 폴백: 단색 배경 + TTS만으로 간단한 영상 생성
        try:
            print(f"[{job_id}] 폴백 모드로 재시도...")
            fallback_result = _create_fallback_video(job_id, article_url)
            if fallback_result:
                duration = time.time() - start_time
                return {
                    'status': 'success',
                    'video_path': fallback_result,
                    'duration': round(duration, 2),
                    'warning': '일부 기능이 제한된 폴백 모드로 생성되었습니다.'
                }
        except:
            pass
        
        return {
            'status': 'failed',
            'error': error_msg,
            'duration': round(time.time() - start_time, 2)
        }


def _cleanup_temp_files(file_paths: list):
    """임시 파일 정리"""
    for path in file_paths:
        try:
            if os.path.exists(path):
                os.remove(path)
        except:
            pass


def _create_fallback_video(job_id: str, article_url: str) -> str:
    """
    폴백: 최소한의 영상 생성
    단색 배경 + 기본 텍스트 음성
    """
    try:
        # 간단한 메시지
        fallback_text = f"뉴스 영상을 생성하는 중 문제가 발생했습니다. URL: {article_url}"
        
        audio_path = str(TEMP_DIR / f"{job_id}_fallback.mp3")
        generate_speech(fallback_text[:100], audio_path)
        
        output_filename = f"{job_id}.mp4"
        output_path = str(OUTPUT_DIR / output_filename)
        
        create_video(
            video_clips=[],
            audio_path=audio_path,
            subtitles=[{
                'text': fallback_text[:50],
                'start_time': 0,
                'duration': 10
            }],
            output_path=output_path,
            duration=10.0
        )
        
        if os.path.exists(audio_path):
            os.remove(audio_path)
        
        if os.path.exists(output_path):
            return output_filename
        
        return None
        
    except:
        return None
