"""
AI 이미지 프롬프트 생성 서비스
뉴스 제목을 기반으로 Leonardo.ai용 영어 프롬프트 생성
"""

def generate_image_prompt(title: str, index: int, total: int) -> str:
    """
    뉴스 제목을 기반으로 AI 이미지 생성 프롬프트 생성
    
    Args:
        title: 뉴스 제목
        index: 이미지 인덱스 (0~3)
        total: 전체 이미지 개수
        
    Returns:
        영어 프롬프트 (Leonardo.ai용)
    """
    # 기본 스타일
    base_style = "professional news photography, clean and modern, high quality, 9:16 vertical format, photorealistic"
    
    # 카테고리별 프롬프트
    if any(word in title for word in ['경제', '금융', '주식', '증시', '환율', '부동산', '시장', '투자']):
        prompts = [
            f"business meeting in modern office, {base_style}",
            f"stock market chart on screens, financial data visualization, {base_style}",
            f"corporate building exterior, business district skyline, {base_style}",
            f"businessman working with laptop and documents, {base_style}"
        ]
    
    elif any(word in title for word in ['정치', '대통령', '국회', '의원', '선거', '정부', '법안']):
        prompts = [
            f"government building architecture, parliament exterior, {base_style}",
            f"political meeting room, serious atmosphere, {base_style}",
            f"national flag waving, official government setting, {base_style}",
            f"press conference setup with microphones, {base_style}"
        ]
    
    elif any(word in title for word in ['사고', '화재', '사망', '체포', '검거', '피해', '사건', '범죄']):
        prompts = [
            f"emergency services, police or fire department, {base_style}",
            f"crime scene investigation, serious atmosphere, {base_style}",
            f"courthouse or police station exterior, {base_style}",
            f"news reporter at scene, breaking news coverage, {base_style}"
        ]
    
    elif any(word in title for word in ['스포츠', '축구', '야구', '농구', '올림픽', '월드컵', '우승', '경기']):
        prompts = [
            f"sports stadium packed with crowd, {base_style}",
            f"athlete in action, dynamic sports photography, {base_style}",
            f"sports equipment and field, professional setup, {base_style}",
            f"victory celebration, championship moment, {base_style}"
        ]
    
    elif any(word in title for word in ['날씨', '기상', '태풍', '폭염', '한파', '비', '눈', '기온']):
        prompts = [
            f"weather forecast map, meteorological visualization, {base_style}",
            f"dramatic sky and clouds, weather phenomenon, {base_style}",
            f"city skyline with weather conditions, {base_style}",
            f"weather station equipment, meteorological instruments, {base_style}"
        ]
    
    elif any(word in title for word in ['IT', '기술', '스마트폰', 'AI', '인공지능', '삼성', '애플', '소프트웨어', '앱']):
        prompts = [
            f"modern technology devices, smartphone and laptop, {base_style}",
            f"AI technology concept, digital interface, {base_style}",
            f"tech company office, innovation workspace, {base_style}",
            f"software development, coding on screen, {base_style}"
        ]
    
    elif any(word in title for word in ['드라마', '영화', '배우', '가수', '앨범', '공연', 'K팝', '연예']):
        prompts = [
            f"entertainment industry, concert stage lights, {base_style}",
            f"movie theater or cinema interior, {base_style}",
            f"recording studio, music production setup, {base_style}",
            f"red carpet event, celebrity premiere, {base_style}"
        ]
    
    elif any(word in title for word in ['교육', '학교', '대학', '학생', '교사', '시험', '입시']):
        prompts = [
            f"modern classroom with students, educational setting, {base_style}",
            f"university campus architecture, academic buildings, {base_style}",
            f"library interior with books and study area, {base_style}",
            f"graduation ceremony, academic achievement, {base_style}"
        ]
    
    elif any(word in title for word in ['건강', '의료', '병원', '의사', '환자', '질병', '치료']):
        prompts = [
            f"modern hospital interior, medical facility, {base_style}",
            f"doctor examining patient, medical consultation, {base_style}",
            f"medical equipment and technology, {base_style}",
            f"healthcare workers in hospital, {base_style}"
        ]
    
    elif any(word in title for word in ['환경', '기후', '에너지', '재생', '친환경', '탄소', '온실가스']):
        prompts = [
            f"renewable energy, solar panels and wind turbines, {base_style}",
            f"green nature and environment, sustainability concept, {base_style}",
            f"climate change visualization, environmental impact, {base_style}",
            f"eco-friendly city, sustainable urban planning, {base_style}"
        ]
    
    elif any(word in title for word in ['미국', '중국', '일본', '북한', '국제', '해외', '외교']):
        prompts = [
            f"international flags at UN building, global diplomacy, {base_style}",
            f"world map with highlighted regions, geopolitical concept, {base_style}",
            f"international airport terminal, global travel, {base_style}",
            f"foreign embassy or consulate building, {base_style}"
        ]
    
    elif any(word in title for word in ['커피', '음식', '맛집', '요리', '레스토랑', '카페']):
        prompts = [
            f"gourmet food photography, restaurant dish presentation, {base_style}",
            f"modern cafe interior, coffee shop atmosphere, {base_style}",
            f"chef preparing food in kitchen, culinary art, {base_style}",
            f"elegant dining table setting, fine dining, {base_style}"
        ]
    
    # 기본 뉴스 프롬프트
    else:
        prompts = [
            f"breaking news concept, modern news studio background, {base_style}",
            f"news broadcast setting, professional journalism, {base_style}",
            f"newspaper and media concept, journalism industry, {base_style}",
            f"reporter with microphone, live news coverage, {base_style}"
        ]
    
    # 인덱스에 맞는 프롬프트 선택 (순환)
    selected_prompt = prompts[index % len(prompts)]
    
    # 네거티브 프롬프트 힌트 추가 (Leonardo.ai가 피해야 할 것들)
    negative_hints = "low quality, blurry, distorted, cartoon, anime, text, watermark"
    
    return f"{selected_prompt}, avoid: {negative_hints}"


def get_keyword_for_prompt(title: str) -> str:
    """
    뉴스 제목에서 핵심 키워드 추출 (간단한 버전)
    
    Args:
        title: 뉴스 제목
        
    Returns:
        핵심 키워드 (영어)
    """
    # 카테고리별 매핑
    keyword_map = {
        '경제': 'economy business',
        '금융': 'finance banking',
        '정치': 'politics government',
        '스포츠': 'sports',
        '날씨': 'weather',
        'IT': 'technology',
        '의료': 'healthcare medical',
        '교육': 'education',
        '환경': 'environment',
        '문화': 'culture entertainment',
    }
    
    for korean_word, english_keyword in keyword_map.items():
        if korean_word in title:
            return english_keyword
    
    return 'news breaking story'
