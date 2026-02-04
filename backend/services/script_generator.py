"""
20초 숏폼 스크립트 생성 서비스
모드별로 다른 스타일의 스크립트 생성
"""
import os
from typing import Dict, List
import re


class ScriptGenerator:
    """스크립트 생성기"""
    
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        self.has_openai = bool(self.openai_api_key)
    
    def generate(self, article_data: Dict[str, str], mode: str) -> Dict[str, any]:
        """
        기사 데이터로부터 20초 스크립트 생성
        
        Args:
            article_data: {'title', 'content', 'summary'}
            mode: 'nyt_question' or 'guardian_observe'
            
        Returns:
            {
                'script': str,  # 전체 스크립트
                'segments': List[Dict],  # 구간별 스크립트 (자막용)
                'duration': float  # 예상 길이
            }
        """
        if self.has_openai:
            return self._generate_with_ai(article_data, mode)
        else:
            return self._generate_template(article_data, mode)
    
    def _generate_with_ai(self, article_data: Dict[str, str], mode: str) -> Dict:
        """OpenAI API를 사용한 스크립트 생성"""
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.openai_api_key)
            
            if mode == "nyt_question":
                prompt = f"""다음 뉴스 기사를 읽고, 20초짜리 숏폼 영상을 위한 스크립트를 작성하세요.
스타일: 질문형 (NYT 스타일)
- 시작: 호기심을 자극하는 질문으로 시작
- 중간: 핵심 내용 2-3문장
- 끝: 생각해볼 점으로 마무리

제목: {article_data['title']}
내용: {article_data['summary'][:500]}

요구사항:
- 총 60-80단어 (한국어 기준 20초 분량)
- 3개 구간으로 나누기 (각 구간 7초 정도)
- 구간 구분은 [SEGMENT] 로 표시
- 자연스러운 구어체

출력 형식:
첫번째 구간 내용[SEGMENT]두번째 구간 내용[SEGMENT]세번째 구간 내용"""
            
            else:  # guardian_observe
                prompt = f"""다음 뉴스 기사를 읽고, 20초짜리 숏폼 영상을 위한 스크립트를 작성하세요.
스타일: 관찰형 (Guardian 스타일)
- 시작: 현상 묘사
- 중간: 배경 설명
- 끝: 의미 있는 통찰

제목: {article_data['title']}
내용: {article_data['summary'][:500]}

요구사항:
- 총 60-80단어 (한국어 기준 20초 분량)
- 3개 구간으로 나누기 (각 구간 7초 정도)
- 구간 구분은 [SEGMENT] 로 표시
- 차분하고 분석적인 톤

출력 형식:
첫번째 구간 내용[SEGMENT]두번째 구간 내용[SEGMENT]세번째 구간 내용"""
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "당신은 숏폼 영상 스크립트 작가입니다."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300
            )
            
            script_text = response.choices[0].message.content.strip()
            return self._parse_script(script_text)
            
        except Exception as e:
            print(f"OpenAI API 오류: {e}. 템플릿 사용.")
            return self._generate_template(article_data, mode)
    
    def _generate_template(self, article_data: Dict[str, str], mode: str) -> Dict:
        """템플릿 기반 스크립트 생성 (OpenAI 없을 때)"""
        title = article_data['title']
        summary = article_data['summary'][:300]
        
        if mode == "nyt_question":
            # 질문형 스타일
            script_text = f"""이 뉴스 들어보셨나요? {title}[SEGMENT]최근 이 이슈가 화제입니다. {summary[:100]}[SEGMENT]여러분은 어떻게 생각하시나요?"""
        else:
            # 관찰형 스타일
            script_text = f"""{title}[SEGMENT]이 사건의 배경을 살펴보면, {summary[:100]}[SEGMENT]이것이 의미하는 바는 무엇일까요."""
        
        return self._parse_script(script_text)
    
    def _parse_script(self, script_text: str) -> Dict:
        """스크립트 텍스트를 구간별로 파싱"""
        # [SEGMENT]로 분리
        segments = script_text.split('[SEGMENT]')
        segments = [s.strip() for s in segments if s.strip()]
        
        # 최소 3개 구간 보장
        while len(segments) < 3:
            segments.append("")
        
        # 전체 스크립트
        full_script = ' '.join(segments)
        
        # 각 구간에 타이밍 할당 (20초 / 3 = 약 6.67초)
        segment_duration = 20.0 / len(segments)
        
        parsed_segments = []
        for i, text in enumerate(segments):
            parsed_segments.append({
                'index': i,
                'text': text,
                'start_time': i * segment_duration,
                'duration': segment_duration
            })
        
        return {
            'script': full_script,
            'segments': parsed_segments,
            'duration': 20.0
        }


def generate_script(article_data: Dict[str, str], mode: str) -> Dict:
    """
    편의 함수: 스크립트 생성
    """
    generator = ScriptGenerator()
    return generator.generate(article_data, mode)
