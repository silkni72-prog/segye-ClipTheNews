import { NextResponse } from 'next/server';

const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8000';

export async function POST(request: Request) {
  try {
    const body = await request.json();
    
    console.log('Sending request to backend:', body);
    
    const response = await fetch(`${BACKEND_URL}/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
      // 타임아웃 방지 - 영상 생성은 시간이 걸릴 수 있음
      // Render 무료 플랜 콜드 스타트를 위해 긴 타임아웃 설정
      signal: AbortSignal.timeout(120000), // 120초 (2분)
    });

    console.log('Backend response status:', response.status);
    
    const data = await response.json();
    console.log('Backend response data:', data);

    if (!response.ok) {
      // FastAPI 에러 형식: {detail: string} 또는 {detail: {message: string}}
      const errorMessage = typeof data.detail === 'string' 
        ? data.detail 
        : data.detail?.message || data.message || '영상 생성에 실패했습니다.';
      
      return NextResponse.json(
        { message: errorMessage },
        { status: response.status }
      );
    }

    return NextResponse.json(data);
  } catch (error) {
    console.error('API error:', error);
    console.error('BACKEND_URL:', BACKEND_URL);
    return NextResponse.json(
      { message: `서버 연결에 실패했습니다. 백엔드 서버(${BACKEND_URL})가 실행 중인지 확인해주세요.` },
      { status: 500 }
    );
  }
}
