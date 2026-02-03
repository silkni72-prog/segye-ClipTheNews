import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import uuid
from typing import List, Dict
import urllib3

# SSL 경고 메시지 비활성화 (개발 환경용)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def scrape_news(url: str) -> Dict:
    """
    뉴스 URL에서 제목, OG 이미지, 본문 이미지 추출
    
    Args:
        url: 뉴스 기사 URL
        
    Returns:
        dict: {
            'title': 기사 제목,
            'images': 다운로드된 이미지 경로 리스트
        }
    """
    try:
        # User-Agent 헤더를 추가하여 차단 방지
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        # SSL 인증서 검증 우회 (개발 환경용)
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 1. OG 이미지 추출 (우선순위 1)
        og_image = soup.find('meta', property='og:image')
        og_image_url = og_image.get('content') if og_image else None
        
        # 2. 본문 이미지들 추가 추출
        article_images = []
        
        # 다양한 선택자로 이미지 찾기
        image_selectors = [
            'article img',
            '.article-body img',
            '.news-content img',
            '.article_body img',
            '.article-content img',
            'img[data-src]',
            'img[src]'
        ]
        
        for selector in image_selectors:
            for img in soup.select(selector):
                src = img.get('src') or img.get('data-src') or img.get('data-lazy-src')
                if src and src not in article_images:
                    # 상대 경로를 절대 경로로 변환
                    full_url = urljoin(url, src)
                    # 작은 아이콘/로고 제외 (너비/높이가 작은 이미지)
                    if not any(x in full_url.lower() for x in ['logo', 'icon', 'banner', 'ad']):
                        article_images.append(full_url)
        
        # 3. 제목 추출
        title = None
        title_meta = soup.find('meta', property='og:title')
        if title_meta:
            title = title_meta.get('content')
        else:
            h1_tag = soup.find('h1')
            if h1_tag:
                title = h1_tag.get_text(strip=True)
        
        if not title:
            title = "뉴스 제목"
        
        # 4. 이미지 다운로드
        # OG 이미지를 최우선으로, 본문 이미지 최대 3개 추가
        image_urls = []
        if og_image_url:
            image_urls.append(og_image_url)
        
        # 중복 제거 후 추가
        for img_url in article_images:
            if img_url not in image_urls:
                image_urls.append(img_url)
            if len(image_urls) >= 4:  # 최대 4개까지 (20초 영상용)
                break
        
        # 이미지가 없으면 기본 이미지 경로 반환
        if not image_urls:
            return {
                'title': title,
                'images': []
            }
        
        downloaded_images = download_images(image_urls)
        
        return {
            'title': title,
            'images': downloaded_images
        }
    
    except Exception as e:
        print(f"Error scraping news: {str(e)}")
        raise Exception(f"뉴스 스크래핑 실패: {str(e)}")


def download_images(urls: List[str]) -> List[str]:
    """
    이미지 URL 리스트를 다운로드하여 로컬 경로 반환
    
    Args:
        urls: 이미지 URL 리스트
        
    Returns:
        List[str]: 다운로드된 이미지 파일 경로 리스트
    """
    downloaded_paths = []
    
    # temp 디렉토리 생성
    temp_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'temp')
    os.makedirs(temp_dir, exist_ok=True)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    for idx, url in enumerate(urls):
        try:
            # SSL 인증서 검증 우회 (개발 환경용)
            response = requests.get(url, headers=headers, timeout=10, stream=True, verify=False)
            response.raise_for_status()
            
            # 파일 확장자 추출
            content_type = response.headers.get('content-type', '')
            if 'image/jpeg' in content_type or 'image/jpg' in content_type:
                ext = '.jpg'
            elif 'image/png' in content_type:
                ext = '.png'
            elif 'image/webp' in content_type:
                ext = '.webp'
            else:
                ext = '.jpg'  # 기본값
            
            # 고유한 파일명 생성
            filename = f"img_{uuid.uuid4().hex[:8]}_{idx}{ext}"
            filepath = os.path.join(temp_dir, filename)
            
            # 이미지 저장
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            downloaded_paths.append(filepath)
            
        except Exception as e:
            print(f"Failed to download image {url}: {str(e)}")
            continue
    
    return downloaded_paths
