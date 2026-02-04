"""
텍스트 요약 서비스
뉴스 기사를 1분 분량의 음성 대본으로 요약
"""

def summarize_for_voice(article_text: str, target_duration: int = 60) -> str:
    """
    기사 본문을 1분 분량 (약 250-300자)으로 요약
    
    하이브리드 접근:
    - 기본: 간단한 규칙 기반 요약 (무료)
    - 고급: GPT-4 API 요약 (향후 업그레이드용)
    
    Args:
        article_text: 뉴스 기사 본문
        target_duration: 목표 음성 길이 (초, 기본 60초)
        
    Returns:
        요약된 텍스트 (약 250-300자, 1분 분량)
    """
    if not article_text or len(article_text.strip()) == 0:
        return "뉴스 내용을 확인할 수 없습니다."
    
    # 목표 글자 수 계산 (한국어 TTS: 1초당 약 4-5자)
    target_chars = target_duration * 4.5  # 60초 → 약 270자
    
    # 간단한 규칙 기반 요약
    article_text = article_text.strip()
    
    # 1. 문장 단위로 분할
    sentences = []
    for s in article_text.replace('. ', '.').split('.'):
        s = s.strip()
        if s and len(s) > 10:  # 너무 짧은 문장 제외
            sentences.append(s + '.')
    
    if not sentences:
        return article_text[:int(target_chars)]
    
    # 2. 핵심 문장 선택
    # - 첫 문장 (리드 문장, 보통 가장 중요)
    # - 중간 문장들 (본론)
    # - 마지막 문장 (결론)
    
    summary_parts = []
    total_chars = 0
    
    # 첫 문장 (필수)
    if sentences:
        summary_parts.append(sentences[0])
        total_chars += len(sentences[0])
    
    # 중간 문장들 추가 (목표 글자수까지)
    for i in range(1, len(sentences)):
        if total_chars + len(sentences[i]) <= target_chars:
            summary_parts.append(sentences[i])
            total_chars += len(sentences[i])
        else:
            break
    
    # 3. 결과 생성
    summary = ' '.join(summary_parts)
    
    # 4. 길이 조정
    if len(summary) > target_chars * 1.2:  # 너무 길면 자르기
        summary = summary[:int(target_chars)] + '...'
    
    print(f"[INFO] Summarized: {len(article_text)} chars → {len(summary)} chars")
    
    return summary


def summarize_with_gpt(article_text: str, target_duration: int = 60) -> str:
    """
    GPT-4를 사용한 고급 요약 (향후 업그레이드용)
    
    Args:
        article_text: 뉴스 기사 본문
        target_duration: 목표 음성 길이 (초)
        
    Returns:
        GPT가 요약한 텍스트
    """
    import os
    
    # OpenAI API 키 확인
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("[WARN] OPENAI_API_KEY not found. Using simple summarization.")
        return summarize_for_voice(article_text, target_duration)
    
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        
        target_chars = int(target_duration * 4.5)
        
        prompt = f"""다음 뉴스 기사를 {target_duration}초 분량의 음성 대본으로 요약해주세요.
        
요구사항:
- 약 {target_chars}자 내외
- 뉴스 앵커가 읽는 톤
- 핵심 내용만 간결하게
- 자연스러운 문장 구성

기사:
{article_text}

요약:"""

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=500
        )
        
        summary = response.choices[0].message.content.strip()
        print(f"[OK] GPT summary: {len(article_text)} chars → {len(summary)} chars")
        
        return summary
        
    except Exception as e:
        print(f"[WARN] GPT summarization failed: {e}. Using simple method.")
        return summarize_for_voice(article_text, target_duration)


def extract_article_content(news_data: dict) -> str:
    """
    스크래핑된 뉴스 데이터에서 본문 추출
    
    Args:
        news_data: scraper.py에서 반환한 뉴스 데이터
        
    Returns:
        기사 본문 텍스트
    """
    # 뉴스 데이터에 content 필드가 있으면 사용
    if 'content' in news_data and news_data['content']:
        return news_data['content']
    
    # 없으면 제목만 사용
    return news_data.get('title', '뉴스 내용을 확인할 수 없습니다.')
