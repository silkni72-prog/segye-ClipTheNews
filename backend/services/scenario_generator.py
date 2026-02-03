"""
자동 시나리오 생성 서비스
제목 기반 템플릿을 사용하여 자연스러운 시나리오 생성
4개 이미지에 맞춰 4개 문장으로 구성
"""

def generate_scenario_from_title(title: str) -> str:
    """
    뉴스 제목을 기반으로 자연스러운 4문장 시나리오 생성
    각 문장은 마침표로 구분되어 영상의 각 장면에 표시됨
    
    Args:
        title: 뉴스 제목
        
    Returns:
        str: 4개 문장으로 구성된 시나리오 (마침표로 구분)
    """
    if not title or len(title.strip()) == 0:
        return "오늘의 주요 뉴스. 핵심 내용 정리. 자세한 분석. 계속 주목하세요"
    
    title = title.strip()
    
    # 제목 길이 조절
    short_title = title if len(title) <= 25 else title[:22] + "..."
    
    # 키워드 기반 맞춤 4문장 시나리오
    
    # 경제 관련
    if any(word in title for word in ['경제', '금융', '주식', '증시', '환율', '부동산']):
        return f"{short_title}. 전문가 분석 나와. 시장 반응 주목. 향후 전망 살펴봅니다"
    
    # 정치 관련
    elif any(word in title for word in ['대통령', '정치', '국회', '의원', '선거', '정부']):
        return f"{short_title}. 정치권 반응 엇갈려. 주요 쟁점 정리. 향후 전개 주목"
    
    # 사건사고
    elif any(word in title for word in ['사고', '화재', '사망', '체포', '검거', '피해']):
        return f"속보입니다. {short_title}. 현장 상황 전해드려. 자세한 내용 확인"
    
    # 스포츠
    elif any(word in title for word in ['축구', '야구', '농구', '올림픽', '월드컵', '우승']):
        return f"{short_title}. 경기 결과 나와. 선수들 반응 화제. 다음 일정 체크"
    
    # 날씨
    elif any(word in title for word in ['날씨', '기상', '태풍', '폭염', '한파', '비', '눈']):
        return f"{short_title}. 기상청 예보 나와. 주의사항 체크. 대비 필요합니다"
    
    # IT/기술
    elif any(word in title for word in ['IT', '기술', '스마트폰', 'AI', '인공지능', '삼성', '애플', '앱', '소프트웨어']):
        return f"{short_title}. 기술 업계 주목. 시장 영향 분석. 향후 동향 살펴봐"
    
    # 연예/문화
    elif any(word in title for word in ['드라마', '영화', '배우', '가수', '앨범', '공연', 'K팝']):
        return f"{short_title}. 화제의 중심에. 팬들 반응 뜨거워. 계속 주목하세요"
    
    # 사회 일반
    elif any(word in title for word in ['시민', '주민', '지역', '교통', '환경', '교육']):
        return f"{short_title}. 시민들 관심 집중. 주요 내용 정리. 영향 살펴봅니다"
    
    # 국제
    elif any(word in title for word in ['미국', '중국', '일본', '북한', '국제', '해외']):
        return f"{short_title}. 국제 사회 반응. 우리 영향은. 향후 전개 주목"
    
    # 기본 템플릿 (제목 길이별)
    if len(title) <= 20:
        return f"{short_title}. 핵심 내용 정리. 상세 분석 나와. 계속 확인하세요"
    else:
        return f"{short_title}. 주요 내용 살펴봐. 전문가 의견은. 자세히 알아봅니다"


def generate_scenario_with_summary(title: str, content: str = None) -> str:
    """
    제목과 본문을 함께 사용하여 시나리오 생성 (미래 확장용)
    
    Args:
        title: 뉴스 제목
        content: 뉴스 본문 (선택)
        
    Returns:
        str: 생성된 시나리오
    """
    # 현재는 제목만 사용, 나중에 본문 요약 기능 추가 가능
    if content and len(content) > 50:
        # 본문 첫 문장 추출
        first_sentence = content.split('.')[0].strip()
        if len(first_sentence) < 50:
            return f"{title}. {first_sentence}"
    
    return generate_scenario_from_title(title)
