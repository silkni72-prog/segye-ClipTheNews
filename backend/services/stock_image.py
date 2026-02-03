import requests
import os
import uuid
from typing import List
import urllib3

# SSL 경고 메시지 비활성화 (개발 환경용)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_stock_images(keyword: str, count: int = 2, api_key: str = None) -> List[str]:
    """
    Unsplash에서 키워드 관련 스톡 이미지 검색 및 다운로드
    
    Args:
        keyword: 검색 키워드
        count: 가져올 이미지 수
        api_key: Unsplash Access Key
        
    Returns:
        List[str]: 다운로드된 이미지 경로 리스트
    """
    if not api_key:
        api_key = os.getenv('UNSPLASH_ACCESS_KEY')
    
    if not api_key:
        print("Warning: UNSPLASH_ACCESS_KEY not found. Skipping stock images.")
        return []
    
    try:
        url = "https://api.unsplash.com/search/photos"
        params = {
            "query": keyword,
            "per_page": count,
            "orientation": "portrait",  # 세로형 이미지
            "client_id": api_key
        }
        
        print(f"Searching Unsplash for: {keyword}")
        response = requests.get(url, params=params, timeout=10, verify=False)
        response.raise_for_status()
        data = response.json()
        
        if not data.get('results'):
            print(f"No images found for keyword: {keyword}")
            return []
        
        # 이미지 다운로드
        downloaded_images = []
        temp_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'temp')
        os.makedirs(temp_dir, exist_ok=True)
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        for idx, photo in enumerate(data['results'][:count]):
            try:
                # 고화질 이미지 URL
                image_url = photo['urls']['regular']
                
                # 이미지 다운로드 (SSL 검증 우회)
                img_response = requests.get(image_url, headers=headers, timeout=10, stream=True, verify=False)
                img_response.raise_for_status()
                
                # 파일 저장
                filename = f"unsplash_{uuid.uuid4().hex[:8]}_{idx}.jpg"
                filepath = os.path.join(temp_dir, filename)
                
                with open(filepath, 'wb') as f:
                    for chunk in img_response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                downloaded_images.append(filepath)
                print(f"Downloaded Unsplash image: {filename}")
                
            except Exception as e:
                print(f"Failed to download Unsplash image {idx}: {str(e)}")
                continue
        
        return downloaded_images
        
    except Exception as e:
        print(f"Error fetching from Unsplash: {str(e)}")
        return []


def extract_keyword_from_title(title: str) -> str:
    """
    뉴스 제목에서 핵심 키워드 추출
    
    Args:
        title: 뉴스 제목
        
    Returns:
        str: 영어 검색 키워드
    """
    # 간단한 키워드 매핑 (한국어 → 영어)
    keyword_map = {
        '경제': 'economy business',
        '정치': 'politics government',
        '사회': 'society community',
        '문화': 'culture art',
        '스포츠': 'sports',
        '기술': 'technology innovation',
        'IT': 'technology computer',
        '과학': 'science research',
        '환경': 'environment nature',
        '교육': 'education school',
        '건강': 'health medical',
        '의료': 'medical healthcare',
        '부동산': 'real estate building',
        '금융': 'finance money',
        '증시': 'stock market',
        '국제': 'international world',
        '북한': 'korea news',
        '대통령': 'president government',
        '선거': 'election voting',
        '법원': 'court justice',
        '경찰': 'police law',
        '사고': 'accident emergency',
        '날씨': 'weather climate',
        '축구': 'soccer football',
        '야구': 'baseball',
        '영화': 'movie cinema',
        '음악': 'music concert',
        '여행': 'travel tourism',
        '음식': 'food cuisine',
        '패션': 'fashion style',
        '게임': 'gaming esports',
        '자동차': 'car automobile',
        '주식': 'stock market',
        '암호화폐': 'cryptocurrency bitcoin',
        '비트코인': 'bitcoin cryptocurrency',
    }
    
    # 제목에서 키워드 찾기
    title_lower = title.lower()
    for korean, english in keyword_map.items():
        if korean in title:
            print(f"Keyword matched: {korean} → {english}")
            return english
    
    # 매칭되는 키워드가 없으면 일반적인 뉴스 이미지
    print("No specific keyword matched, using generic 'news'")
    return "news breaking korea"
