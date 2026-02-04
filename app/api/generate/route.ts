import { NextResponse } from 'next/server';
import OpenAI from 'openai';

// OpenAI 클라이언트 (선택사항)
const openai = process.env.OPENAI_API_KEY 
  ? new OpenAI({ apiKey: process.env.OPENAI_API_KEY })
  : null;

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { news_url, mode } = body;
    
    console.log('📰 뉴스 URL:', news_url);
    console.log('🎬 모드:', mode);
    
    if (!news_url || !news_url.startsWith('http')) {
      return NextResponse.json(
        { message: '유효한 뉴스 URL을 입력해주세요.' },
        { status: 400 }
      );
    }

    // 1단계: 기사 파싱
    console.log('🔍 기사 파싱 중...');
    const articleData = await scrapeArticle(news_url);
    
    if (!articleData.title) {
      return NextResponse.json(
        { message: '기사를 파싱할 수 없습니다. 다른 URL을 시도해주세요.' },
        { status: 400 }
      );
    }
    
    console.log('✅ 제목:', articleData.title.slice(0, 50) + '...');

    // 2단계: 스크립트 생성
    console.log('📝 스크립트 생성 중...');
    const script = await generateScript(articleData, mode);
    
    console.log('✅ 스크립트:', script.slice(0, 100) + '...');

    // 3단계: 결과 반환
    return NextResponse.json({
      video_url: '/api/dummy-video',  // 더미 URL (나중에 실제 영상 생성 추가)
      message: '스크립트가 생성되었습니다!',
      script: script,
      title: articleData.title,
      summary: articleData.summary
    });

  } catch (error) {
    console.error('❌ API 오류:', error);
    return NextResponse.json(
      { 
        message: error instanceof Error ? error.message : '알 수 없는 오류가 발생했습니다.' 
      },
      { status: 500 }
    );
  }
}

// 기사 스크래핑 함수
async function scrapeArticle(url: string) {
  try {
    const response = await fetch(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
      }
    });
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    
    const html = await response.text();
    
    // 간단한 HTML 파싱
    const titleMatch = html.match(/<title[^>]*>([^<]+)<\/title>/i);
    const title = titleMatch ? titleMatch[1].trim() : '';
    
    // 메타 description 추출
    const descMatch = html.match(/<meta[^>]*name=["']description["'][^>]*content=["']([^"']+)["']/i);
    const summary = descMatch ? descMatch[1] : '';
    
    // p 태그에서 본문 추출
    const paragraphs = html.match(/<p[^>]*>([^<]+)<\/p>/gi) || [];
    const content = paragraphs
      .slice(0, 5)
      .map(p => p.replace(/<[^>]+>/g, ''))
      .join(' ')
      .slice(0, 500);
    
    return {
      title: title || '제목 없음',
      summary: summary || content || '내용 없음',
      content: content
    };
    
  } catch (error) {
    console.error('스크래핑 오류:', error);
    throw new Error('기사를 불러올 수 없습니다.');
  }
}

// 스크립트 생성 함수
async function generateScript(articleData: { title: string; summary: string }, mode: string) {
  // OpenAI 사용 가능한 경우
  if (openai) {
    try {
      const prompt = mode === 'nyt_question'
        ? `다음 뉴스를 20초 숏폼 영상용 스크립트로 작성하세요. 질문형으로 시작하세요.

제목: ${articleData.title}
요약: ${articleData.summary}

요구사항:
- 60-80단어 (20초 분량)
- 호기심을 자극하는 질문으로 시작
- 핵심 내용 2-3문장
- 생각해볼 점으로 마무리

스크립트만 출력하세요:`
        : `다음 뉴스를 20초 숏폼 영상용 스크립트로 작성하세요. 관찰형 스타일로 작성하세요.

제목: ${articleData.title}
요약: ${articleData.summary}

요구사항:
- 60-80단어 (20초 분량)
- 현상 묘사로 시작
- 배경 설명
- 의미 있는 통찰로 마무리

스크립트만 출력하세요:`;

      const completion = await openai.chat.completions.create({
        model: 'gpt-3.5-turbo',
        messages: [
          { role: 'system', content: '당신은 숏폼 영상 스크립트 작가입니다.' },
          { role: 'user', content: prompt }
        ],
        temperature: 0.7,
        max_tokens: 200
      });

      return completion.choices[0]?.message?.content || generateTemplateScript(articleData, mode);
      
    } catch (error) {
      console.error('OpenAI 오류:', error);
      // 폴백: 템플릿 사용
      return generateTemplateScript(articleData, mode);
    }
  }
  
  // OpenAI 없으면 템플릿 사용
  return generateTemplateScript(articleData, mode);
}

// 템플릿 기반 스크립트 생성
function generateTemplateScript(articleData: { title: string; summary: string }, mode: string) {
  const title = articleData.title;
  const summary = articleData.summary.slice(0, 150);
  
  if (mode === 'nyt_question') {
    return `이 뉴스 들어보셨나요? ${title}. 최근 이 이슈가 화제입니다. ${summary}. 여러분은 어떻게 생각하시나요?`;
  } else {
    return `${title}. 이 사건의 배경을 살펴보면, ${summary}. 이것이 의미하는 바는 무엇일까요.`;
  }
}
