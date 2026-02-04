from __future__ import annotations

import os
import uuid
from typing import List, Optional
from PIL import Image as PILImage, ImageDraw, ImageFont
from moviepy.editor import (
    ImageClip,
    CompositeVideoClip,
    concatenate_videoclips,
)
from datetime import datetime

W, H = 1080, 1920
DURATION = 20  # 20초
FPS = 24

def _fit_and_crop_image(img_path: str) -> str:
    """
    이미지를 9:16 비율로 크롭하고 리사이즈
    """
    img = PILImage.open(img_path).convert('RGB')
    
    target_ratio = W / H  # 9:16
    img_ratio = img.width / img.height
    
    if img_ratio > target_ratio:
        # 이미지가 더 넓음 - 좌우를 자름
        new_width = int(img.height * target_ratio)
        left = (img.width - new_width) // 2
        img = img.crop((left, 0, left + new_width, img.height))
    else:
        # 이미지가 더 높음 - 위아래를 자름
        new_height = int(img.width / target_ratio)
        top = (img.height - new_height) // 2
        img = img.crop((0, top, img.width, top + new_height))
    
    # 리사이즈
    img = img.resize((W, H), PILImage.Resampling.LANCZOS)
    
    # 임시 파일로 저장
    temp_path = img_path.replace('.', '_cropped.')
    img.save(temp_path, quality=95)
    return temp_path


def _create_text_overlay(text: str, y_position: int, fontsize: int, bg_color=(0, 0, 0, 180), text_color='#FFFFFF') -> str:
    """
    텍스트 오버레이 이미지 생성
    """
    img = PILImage.new('RGBA', (W, 600), (0, 0, 0, 0))
    
    # 배경 박스
    if bg_color:
        bg = PILImage.new('RGBA', (W - 128, 400), bg_color)
        img.paste(bg, (64, 100), bg)
    
    draw = ImageDraw.Draw(img)
    
    # 폰트 로드
    try:
        font = ImageFont.truetype("malgunbd.ttf", fontsize)
    except:
        try:
            font = ImageFont.truetype("malgun.ttf", fontsize)
        except:
            try:
                font = ImageFont.truetype("arial.ttf", fontsize)
            except:
                font = ImageFont.load_default()
    
    # 텍스트를 여러 줄로 나누기
    words = text.split()
    lines = []
    current_line = ""
    max_chars = 15
    
    for word in words:
        test_line = current_line + word + " "
        if len(test_line) <= max_chars:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line.strip())
            current_line = word + " "
    
    if current_line:
        lines.append(current_line.strip())
    
    # 각 줄 그리기
    y_offset = 150
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x = (W - text_width) // 2
        
        # 테두리 (검은색)
        for adj in range(-4, 5):
            for adj2 in range(-4, 5):
                draw.text((x+adj, y_offset+adj2), line, font=font, fill='black')
        
        # 텍스트
        draw.text((x, y_offset), line, font=font, fill=text_color)
        y_offset += fontsize + 20
    
    # 임시 파일로 저장
    temp_dir = os.path.dirname(os.path.dirname(__file__))
    temp_path = os.path.join(temp_dir, 'output', f'text_{uuid.uuid4().hex[:8]}.png')
    os.makedirs(os.path.dirname(temp_path), exist_ok=True)
    img.save(temp_path)
    return temp_path


def build_short_video(
    image_paths: List[str],
    title: Optional[str],
    captions: List[str],
    output_dir: str,
    total_seconds: float = 20.0,
) -> str:
    """
    간단하고 안정적인 뉴스 영상 생성
    """
    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}.mp4")
    
    if not image_paths:
        raise ValueError("이미지가 없습니다.")
    
    # 최대 4개 이미지
    image_paths = image_paths[:4]
    n = len(image_paths)
    duration_per_image = total_seconds / n
    
    print(f"[INFO] Creating video with {n} images, {duration_per_image:.1f}s each")
    
    # 자막 준비
    if not captions:
        captions = ["오늘의 주요 뉴스"]
    
    # 자막 정규화
    normalized_captions = []
    for cap in captions:
        cap = (cap or "").strip()
        if cap:
            cap = cap.replace("습니다.", "다").replace("다.", "다")
            normalized_captions.append(cap)
    
    if not normalized_captions:
        normalized_captions = ["오늘의 주요 뉴스"]
    
    # 이미지 클립 생성
    clips = []
    for idx, img_path in enumerate(image_paths):
        try:
            # 이미지 크롭 및 리사이즈
            cropped_path = _fit_and_crop_image(img_path)
            
            # 기본 클립 생성
            clip = ImageClip(cropped_path).set_duration(duration_per_image)
            clip = clip.fadein(0.5).fadeout(0.5)
            
            clips.append(clip)
            print(f"[OK] Processed image {idx+1}/{n}")
            
        except Exception as e:
            print(f"[WARN] Failed to process image {idx+1}: {e}")
            continue
    
    if not clips:
        raise ValueError("처리 가능한 이미지가 없습니다.")
    
    # 이미지 연결
    video = concatenate_videoclips(clips, method="compose")
    
    # 오버레이 추가
    overlays = []
    
    # 제목 (첫 3초만 표시)
    if title:
        try:
            title_path = _create_text_overlay(title[:50], 100, 55, bg_color=(0, 0, 0, 200), text_color='#FFFFFF')
            title_clip = ImageClip(title_path).set_duration(3.0)  # 5초에서 3초로 단축
            title_clip = title_clip.set_position(('center', 50))
            overlays.append(title_clip)
            print(f"[OK] Added title overlay (3 seconds)")
        except Exception as e:
            print(f"[WARN] Failed to add title: {e}")
    
    # 자막 (각 장면마다)
    for idx in range(n):
        try:
            caption_text = normalized_captions[min(idx, len(normalized_captions) - 1)]
            caption_path = _create_text_overlay(caption_text, 1200, 65, bg_color=(0, 0, 0, 180), text_color='#FFD700')
            
            start_time = idx * duration_per_image
            
            # 첫 번째 자막은 제목이 끝난 후(3초)부터 표시
            if idx == 0 and title:
                caption_clip = ImageClip(caption_path).set_duration(duration_per_image - 3.0)
                caption_clip = caption_clip.set_start(3.0).set_position(('center', H - 600))
                print(f"[OK] Added caption {idx+1} (starts at 3s): {caption_text[:30]}...")
            else:
                caption_clip = ImageClip(caption_path).set_duration(duration_per_image)
                caption_clip = caption_clip.set_start(start_time).set_position(('center', H - 600))
                print(f"[OK] Added caption {idx+1} (starts at {start_time}s): {caption_text[:30]}...")
            
            overlays.append(caption_clip)
            
        except Exception as e:
            print(f"[WARN] Failed to add caption {idx+1}: {e}")
            continue
    
    # 최종 합성
    if overlays:
        final = CompositeVideoClip([video] + overlays)
    else:
        final = video
    
    # 영상 저장
    print(f"[INFO] Writing video file...")
    final.write_videofile(
        out_path,
        fps=FPS,
        codec='libx264',
        audio=False,
        preset='ultrafast',
        threads=4,
        logger=None
    )
    
    # 정리
    final.close()
    for clip in clips:
        clip.close()
    
    print(f"[OK] Video saved: {os.path.basename(out_path)}")
    return out_path


# Legacy wrapper
def generate_video(images: List[str], scenario: str, title: str) -> str:
    """
    기존 API 호환 래퍼
    """
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output')
    
    # 시나리오를 자막으로 변환
    if scenario and len(scenario.strip()) > 0:
        # 마침표로 분할
        captions = [s.strip() for s in scenario.replace('. ', '.').split('.') if s.strip()]
        
        # 자막이 너무 적으면 단어로 분할
        if len(captions) < 2:
            words = scenario.split()
            mid = len(words) // 2
            captions = [' '.join(words[:mid]), ' '.join(words[mid:])]
    else:
        captions = ["오늘의 주요 뉴스", "자세한 내용을 확인하세요"]
    
    # 자막이 이미지 개수보다 적으면 확장
    print(f"[DEBUG] Scenario: {scenario[:100]}...")
    print(f"[DEBUG] Split into {len(captions)} captions: {captions}")
    print(f"[DEBUG] Need {len(images)} captions for {len(images)} images")
    
    while len(captions) < len(images):
        if captions:
            # 기존 자막을 순환 반복
            captions.append(captions[len(captions) % (len(captions))])
        else:
            captions.append(f"주요 내용 {len(captions) + 1}")
    
    # 자막이 너무 많으면 이미지 개수만큼 자름
    if len(captions) > len(images):
        captions = captions[:len(images)]
    
    print(f"[INFO] Generating video: {len(images)} images, {len(captions)} captions")
    print(f"[INFO] Final captions: {captions}")
    print(f"[INFO] Title: {title[:50]}...")
    
    try:
        full_path = build_short_video(
            image_paths=images,
            title=title,
            captions=captions,
            output_dir=output_dir,
            total_seconds=20.0,
        )
        
        filename = os.path.basename(full_path)
        print(f"[OK] Video generated successfully: {filename}")
        return filename
        
    except Exception as e:
        print(f"[ERROR] Video generation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        raise Exception(f"영상 생성 실패: {str(e)}")


def generate_video_with_voice(
    images: List[str], 
    audio_path: str,
    subtitles: List[Dict],
    title: str
) -> str:
    """
    이미지 + 음성 + 동기화된 자막으로 영상 생성
    
    Args:
        images: 이미지 파일 경로 리스트
        audio_path: 음성 파일 경로 (.mp3)
        subtitles: 타이밍 정보가 포함된 자막 리스트
            [{'text': str, 'start': float, 'end': float, 'duration': float}, ...]
        title: 영상 제목
        
    Returns:
        생성된 영상 파일 이름
    """
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # 1. 오디오 로드
        audio = AudioFileClip(audio_path)
        duration = audio.duration
        
        print(f"[INFO] Audio duration: {duration:.1f} seconds")
        print(f"[INFO] Creating video with {len(images)} images and {len(subtitles)} subtitles")
        
        # 2. 이미지 클립 생성 (오디오 길이에 맞춤)
        if not images:
            raise ValueError("이미지가 없습니다.")
        
        # 이미지를 최대 4개로 제한
        if len(images) > 4:
            images = images[:4]
        
        duration_per_image = duration / len(images)
        clips = []
        
        for idx, img_path in enumerate(images):
            try:
                cropped_path = _fit_and_crop_image(img_path)
                clip = ImageClip(cropped_path).set_duration(duration_per_image)
                clip = clip.fadein(0.5).fadeout(0.5)
                clips.append(clip)
                print(f"[OK] Processed image {idx+1}/{len(images)}")
            except Exception as e:
                print(f"[WARN] Failed to process image {idx+1}: {e}")
                continue
        
        if not clips:
            raise ValueError("처리 가능한 이미지가 없습니다.")
        
        # 3. 이미지 연결
        video = concatenate_videoclips(clips, method="compose")
        
        # 4. 자막 추가 (타이밍에 맞춰)
        overlays = []
        
        # 제목 (첫 3초)
        if title:
            try:
                title_path = _create_text_overlay(title[:50], 100, 55, bg_color=(0, 0, 0, 200), text_color='#FFFFFF')
                title_clip = ImageClip(title_path).set_duration(3.0)
                title_clip = title_clip.set_position(('center', 50))
                overlays.append(title_clip)
                print(f"[OK] Added title overlay")
            except Exception as e:
                print(f"[WARN] Failed to add title: {e}")
        
        # 동기화된 자막 추가
        for idx, sub in enumerate(subtitles):
            try:
                caption_text = sub['text']
                start_time = sub['start']
                sub_duration = sub['duration']
                
                caption_path = _create_text_overlay(
                    caption_text, 
                    1200, 
                    65, 
                    bg_color=(0, 0, 0, 180), 
                    text_color='#FFD700'
                )
                
                caption_clip = ImageClip(caption_path).set_duration(sub_duration)
                caption_clip = caption_clip.set_start(start_time).set_position(('center', H - 600))
                
                overlays.append(caption_clip)
                print(f"[OK] Added synced subtitle {idx+1}: {start_time:.1f}s-{sub['end']:.1f}s")
                
            except Exception as e:
                print(f"[WARN] Failed to add subtitle {idx+1}: {e}")
                continue
        
        # 5. 최종 합성
        if overlays:
            final = CompositeVideoClip([video] + overlays)
        else:
            final = video
        
        # 6. 오디오 추가 (핵심!)
        final = final.set_audio(audio)
        
        # 7. 파일명 생성
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"voice_video_{timestamp}_{uuid.uuid4().hex[:8]}.mp4"
        output_path = os.path.join(output_dir, filename)
        
        # 8. 영상 저장
        print(f"[INFO] Writing video file with audio...")
        final.write_videofile(
            output_path,
            fps=24,
            codec='libx264',
            audio_codec='aac',  # 오디오 코덱 지정
            preset='ultrafast',
            threads=4,
            logger=None
        )
        
        # 9. 정리
        final.close()
        audio.close()
        for clip in clips:
            clip.close()
        
        print(f"[OK] Voice video saved: {filename}")
        return filename
        
    except Exception as e:
        print(f"[ERROR] Voice video generation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        raise Exception(f"음성 영상 생성 실패: {str(e)}")
