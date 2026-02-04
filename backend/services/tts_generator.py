"""
TTS (Text-to-Speech) 음성 생성 서비스
하이브리드 접근: gTTS (무료) → Google Cloud TTS → ElevenLabs (업그레이드)
"""

import os
from typing import Optional, Dict
from pathlib import Path


def generate_voice_gtts(text: str, output_path: str, lang: str = 'ko') -> Optional[Dict]:
    """
    gTTS (Google Translate TTS)로 음성 생성 - 무료, API 키 불필요
    
    Args:
        text: 음성으로 변환할 텍스트
        output_path: 저장 경로 (.mp3)
        lang: 언어 코드 (기본: 'ko')
        
    Returns:
        {
            'audio_path': str,
            'duration': float,  # 초
            'method': str  # 'gtts'
        }
    """
    try:
        from gtts import gTTS
        from pydub import AudioSegment
        
        print(f"[INFO] Generating voice with gTTS...")
        print(f"[INFO] Text length: {len(text)} characters")
        
        # TTS 생성
        tts = gTTS(text=text, lang=lang, slow=False)
        
        # 디렉토리 생성
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # 저장
        tts.save(output_path)
        
        # 음성 길이 계산
        audio = AudioSegment.from_mp3(output_path)
        duration = len(audio) / 1000.0  # 밀리초 → 초
        
        print(f"[OK] Voice generated: {os.path.basename(output_path)}")
        print(f"[INFO] Duration: {duration:.1f} seconds")
        
        return {
            'audio_path': output_path,
            'duration': duration,
            'method': 'gtts'
        }
        
    except ImportError:
        print("[ERROR] gTTS not installed. Run: pip install gtts pydub")
        return None
    except Exception as e:
        print(f"[ERROR] gTTS generation failed: {e}")
        return None


def generate_voice_google_cloud(text: str, output_path: str) -> Optional[Dict]:
    """
    Google Cloud TTS로 음성 생성 - 고품질, 월 100만자 무료
    
    Args:
        text: 음성으로 변환할 텍스트
        output_path: 저장 경로 (.mp3)
        
    Returns:
        음성 정보 딕셔너리
    """
    # Google Cloud 인증 확인
    credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if not credentials_path:
        print("[WARN] GOOGLE_APPLICATION_CREDENTIALS not set. Using gTTS instead.")
        return generate_voice_gtts(text, output_path)
    
    try:
        from google.cloud import texttospeech
        from pydub import AudioSegment
        import io
        
        print(f"[INFO] Generating voice with Google Cloud TTS...")
        
        client = texttospeech.TextToSpeechClient()
        
        synthesis_input = texttospeech.SynthesisInput(text=text)
        
        # 한국어 WaveNet 음성 (자연스러운 뉴스 앵커 스타일)
        voice = texttospeech.VoiceSelectionParams(
            language_code="ko-KR",
            name="ko-KR-Wavenet-A",  # 여성 뉴스 앵커 스타일
            ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
        )
        
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=1.0,  # 정상 속도
            pitch=0.0
        )
        
        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )
        
        # 저장
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'wb') as out:
            out.write(response.audio_content)
        
        # 길이 계산
        audio = AudioSegment.from_mp3(output_path)
        duration = len(audio) / 1000.0
        
        print(f"[OK] Google Cloud TTS generated: {os.path.basename(output_path)}")
        print(f"[INFO] Duration: {duration:.1f} seconds")
        
        return {
            'audio_path': output_path,
            'duration': duration,
            'method': 'google_cloud'
        }
        
    except ImportError:
        print("[WARN] google-cloud-texttospeech not installed. Using gTTS.")
        return generate_voice_gtts(text, output_path)
    except Exception as e:
        print(f"[WARN] Google Cloud TTS failed: {e}. Using gTTS.")
        return generate_voice_gtts(text, output_path)


def generate_voice_elevenlabs(text: str, output_path: str) -> Optional[Dict]:
    """
    ElevenLabs TTS로 음성 생성 - 최고 품질 (향후 업그레이드용)
    
    Args:
        text: 음성으로 변환할 텍스트
        output_path: 저장 경로 (.mp3)
        
    Returns:
        음성 정보 딕셔너리
    """
    api_key = os.getenv('ELEVENLABS_API_KEY')
    if not api_key:
        print("[WARN] ELEVENLABS_API_KEY not set. Using gTTS instead.")
        return generate_voice_gtts(text, output_path)
    
    try:
        import requests
        from pydub import AudioSegment
        
        print(f"[INFO] Generating voice with ElevenLabs...")
        
        # 한국어 뉴스 앵커 목소리 ID (ElevenLabs에서 제공)
        # 실제로는 ElevenLabs 대시보드에서 목소리를 선택해야 함
        VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Rachel (영어 기본값)
        
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
        
        headers = {
            "xi-api-key": api_key,
            "Content-Type": "application/json"
        }
        
        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75,
                "style": 0.0,
                "use_speaker_boost": True
            }
        }
        
        response = requests.post(url, json=data, headers=headers, timeout=60)
        response.raise_for_status()
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        # 길이 계산
        audio = AudioSegment.from_mp3(output_path)
        duration = len(audio) / 1000.0
        
        print(f"[OK] ElevenLabs TTS generated: {os.path.basename(output_path)}")
        print(f"[INFO] Duration: {duration:.1f} seconds")
        
        return {
            'audio_path': output_path,
            'duration': duration,
            'method': 'elevenlabs'
        }
        
    except Exception as e:
        print(f"[WARN] ElevenLabs TTS failed: {e}. Using gTTS.")
        return generate_voice_gtts(text, output_path)


def generate_voice(text: str, output_path: str) -> Optional[Dict]:
    """
    하이브리드 TTS: 사용 가능한 최고 품질 서비스 자동 선택
    
    우선순위:
    1. ElevenLabs (최고 품질, 유료)
    2. Google Cloud TTS (고품질, 무료)
    3. gTTS (기본 품질, 무료, API 키 불필요)
    
    Args:
        text: 음성으로 변환할 텍스트
        output_path: 저장 경로 (.mp3)
        
    Returns:
        {
            'audio_path': str,
            'duration': float,
            'method': str
        }
    """
    # 1순위: ElevenLabs (API 키 있으면)
    if os.getenv('ELEVENLABS_API_KEY'):
        result = generate_voice_elevenlabs(text, output_path)
        if result:
            return result
    
    # 2순위: Google Cloud TTS (인증 파일 있으면)
    if os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
        result = generate_voice_google_cloud(text, output_path)
        if result:
            return result
    
    # 3순위: gTTS (항상 사용 가능)
    print("[INFO] Using gTTS (free, no API key required)")
    return generate_voice_gtts(text, output_path)
