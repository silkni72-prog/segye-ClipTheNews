"""
뉴스 기사 스크래핑 서비스
NYT와 Guardian 등 다양한 뉴스 사이트 지원
"""
import requests
from bs4 import BeautifulSoup
from typing import Dict, Optional
import re


class ArticleScraper:
    """뉴스 기사 스크래퍼"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def scrape(self, url: str) -> Dict[str, str]:
        """
        기사 URL에서 제목과 본문 추출
        
        Args:
            url: 기사 URL
            
        Returns:
            Dict with 'title', 'content', 'summary'
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # URL 기반 사이트 감지
            if 'nytimes.com' in url:
                return self._scrape_nytimes(soup)
            elif 'theguardian.com' in url:
                return self._scrape_guardian(soup)
            else:
                # Generic scraper
                return self._scrape_generic(soup)
                
        except Exception as e:
            raise Exception(f"기사 스크래핑 실패: {str(e)}")
    
    def _scrape_nytimes(self, soup: BeautifulSoup) -> Dict[str, str]:
        """NYTimes 기사 파싱"""
        title = ""
        content = ""
        
        # Title
        title_tag = soup.find('h1')
        if title_tag:
            title = title_tag.get_text(strip=True)
        
        # Content - NYT specific selectors
        content_tags = soup.find_all('p', class_=re.compile('css-.*'))
        if not content_tags:
            content_tags = soup.find_all('p')
        
        paragraphs = []
        for p in content_tags[:10]:  # 처음 10개 문단만
            text = p.get_text(strip=True)
            if len(text) > 50:  # 의미있는 문단만
                paragraphs.append(text)
        
        content = ' '.join(paragraphs)
        
        return {
            'title': title,
            'content': content,
            'summary': content[:500] if content else ''
        }
    
    def _scrape_guardian(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Guardian 기사 파싱"""
        title = ""
        content = ""
        
        # Title
        title_tag = soup.find('h1')
        if title_tag:
            title = title_tag.get_text(strip=True)
        
        # Content - Guardian specific
        article_body = soup.find('div', {'id': 'maincontent'})
        if not article_body:
            article_body = soup.find('article')
        
        if article_body:
            paragraphs = []
            for p in article_body.find_all('p')[:10]:
                text = p.get_text(strip=True)
                if len(text) > 50:
                    paragraphs.append(text)
            content = ' '.join(paragraphs)
        
        return {
            'title': title,
            'content': content,
            'summary': content[:500] if content else ''
        }
    
    def _scrape_generic(self, soup: BeautifulSoup) -> Dict[str, str]:
        """일반 웹사이트 파싱"""
        title = ""
        content = ""
        
        # Title
        title_tag = soup.find('h1')
        if not title_tag:
            title_tag = soup.find('title')
        if title_tag:
            title = title_tag.get_text(strip=True)
        
        # Content
        # Try common article containers
        article = soup.find('article')
        if not article:
            article = soup.find('div', class_=re.compile('article|content|post'))
        if not article:
            article = soup
        
        paragraphs = []
        for p in article.find_all('p')[:15]:
            text = p.get_text(strip=True)
            if len(text) > 50:
                paragraphs.append(text)
        
        content = ' '.join(paragraphs)
        
        return {
            'title': title,
            'content': content,
            'summary': content[:500] if content else ''
        }


def scrape_article(url: str) -> Dict[str, str]:
    """
    편의 함수: 기사 스크래핑
    """
    scraper = ArticleScraper()
    return scraper.scrape(url)
