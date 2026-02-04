"""
자막-음성 동기화 서비스
텍스트를 문장으로 분할하고 음성 길이에 맞춰 타이밍 계산
"""

from typing import List, Dict


def create_timed_subtitles(text: str, audio_duration: float) -> List[Dict]:
    """
    텍스트를 문장으로 나누고 음성 길이에 맞춰 타이밍 계산
    
    Args:
        text: 전체 대본 텍스트
        audio_duration: 음성 길이 (초)
        
    Returns:
        [
            {'text': '첫 번째 문장', 'start': 0.0, 'end': 5.2, 'duration': 5.2},
            {'text': '두 번째 문장', 'start': 5.2, 'end': 10.8, 'duration': 5.6},
            ...
        ]
    """
    if not text or len(text.strip()) == 0:
        return []
    
    # 1. 문장 단위로 분할
    sentences = []
    for s in text.replace('. ', '.').replace('! ', '!').replace('? ', '?').split('.'):
        s = s.strip()
        if s:
            # 느낌표나 물음표로도 분할
            for sub in s.split('!'):
                sub = sub.strip()
                if sub:
                    for subsub in sub.split('?'):
                        subsub = subsub.strip()
                        if subsub and len(subsub) > 3:
                            sentences.append(subsub + '.')
    
    if not sentences:
        sentences = [text]
    
    print(f"[INFO] Split into {len(sentences)} subtitle segments")
    
    # 2. 각 문장 길이 비율로 시간 분배
    total_chars = sum(len(s) for s in sentences)
    
    if total_chars == 0:
        # 모든 문장이 동일 길이로 처리
        duration_per_sentence = audio_duration / len(sentences)
        subtitles = []
        for i, sentence in enumerate(sentences):
            start = i * duration_per_sentence
            end = start + duration_per_sentence
            subtitles.append({
                'text': sentence,
                'start': start,
                'end': end,
                'duration': duration_per_sentence
            })
        return subtitles
    
    # 3. 각 문장에 시간 할당
    subtitles = []
    current_time = 0.0
    
    for sentence in sentences:
        # 글자 수 비율로 시간 계산
        char_ratio = len(sentence) / total_chars
        duration = audio_duration * char_ratio
        
        subtitles.append({
            'text': sentence,
            'start': current_time,
            'end': current_time + duration,
            'duration': duration
        })
        
        current_time += duration
    
    # 4. 마지막 자막의 end를 정확히 audio_duration으로 조정
    if subtitles:
        subtitles[-1]['end'] = audio_duration
        subtitles[-1]['duration'] = audio_duration - subtitles[-1]['start']
    
    print(f"[INFO] Created {len(subtitles)} timed subtitles")
    for idx, sub in enumerate(subtitles):
        print(f"[DEBUG] Subtitle {idx+1}: {sub['start']:.1f}s - {sub['end']:.1f}s ({len(sub['text'])} chars)")
    
    return subtitles


def create_simple_subtitles(text: str, num_segments: int = 4) -> List[str]:
    """
    텍스트를 N개의 자막으로 균등 분할 (간단한 버전)
    
    Args:
        text: 전체 텍스트
        num_segments: 분할할 개수
        
    Returns:
        자막 텍스트 리스트
    """
    sentences = []
    for s in text.replace('. ', '.').split('.'):
        s = s.strip()
        if s and len(s) > 3:
            sentences.append(s + '.')
    
    if not sentences:
        return [text]
    
    # 문장이 충분하면 그대로 사용
    if len(sentences) >= num_segments:
        return sentences[:num_segments]
    
    # 문장이 부족하면 단어로 분할
    words = text.split()
    words_per_segment = max(2, len(words) // num_segments)
    
    segments = []
    for i in range(num_segments):
        start_idx = i * words_per_segment
        end_idx = start_idx + words_per_segment
        if i == num_segments - 1:
            end_idx = len(words)
        
        segment = ' '.join(words[start_idx:end_idx])
        if segment:
            segments.append(segment)
    
    return segments


def adjust_subtitle_timing_for_images(
    subtitles: List[Dict], 
    num_images: int
) -> List[Dict]:
    """
    자막 타이밍을 이미지 개수에 맞춰 조정
    
    이미지가 변경되는 시점에서 자막도 함께 변경되도록
    
    Args:
        subtitles: create_timed_subtitles 결과
        num_images: 영상에 사용할 이미지 개수
        
    Returns:
        조정된 자막 리스트
    """
    if not subtitles or num_images <= 0:
        return subtitles
    
    total_duration = subtitles[-1]['end'] if subtitles else 60.0
    duration_per_image = total_duration / num_images
    
    # 각 이미지 구간에 하나씩 자막 배정
    adjusted = []
    
    for img_idx in range(num_images):
        start_time = img_idx * duration_per_image
        end_time = (img_idx + 1) * duration_per_image
        
        # 해당 구간에 해당하는 자막들 찾기
        segment_subs = []
        for sub in subtitles:
            # 자막이 이 구간과 겹치는지 확인
            if sub['start'] < end_time and sub['end'] > start_time:
                segment_subs.append(sub)
        
        # 가장 적합한 자막 선택 (가장 많이 겹치는 것)
        if segment_subs:
            # 간단하게: 첫 번째 자막 사용
            chosen = segment_subs[0]
            adjusted.append({
                'text': chosen['text'],
                'start': start_time,
                'end': end_time,
                'duration': duration_per_image
            })
        else:
            # 자막이 없으면 가장 가까운 것 사용
            if subtitles:
                idx = min(img_idx, len(subtitles) - 1)
                adjusted.append({
                    'text': subtitles[idx]['text'],
                    'start': start_time,
                    'end': end_time,
                    'duration': duration_per_image
                })
    
    return adjusted
