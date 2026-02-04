import { NextResponse } from 'next/server';

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';
const MAX_POLLING_TIME = 600000; // 10 minutes
const POLLING_INTERVAL = 2000; // 2 seconds

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

    // 1단계: 백엔드에 작업 생성
    console.log('🔄 백엔드에 작업 요청 중...');
    
    let jobResponse;
    try {
      jobResponse = await fetch(`${BACKEND_URL}/jobs`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          article_url: news_url,
          mode: mode,
        }),
      });

      if (!jobResponse.ok) {
        const errorData = await jobResponse.json();
        throw new Error(errorData.detail || '백엔드 서버 오류');
      }
    } catch (error) {
      console.error('❌ 백엔드 연결 실패:', error);
      return NextResponse.json(
        { 
          message: '백엔드 서버에 연결할 수 없습니다. 백엔드가 실행 중인지 확인해주세요 (http://localhost:8000)' 
        },
        { status: 503 }
      );
    }

    const jobData = await jobResponse.json();
    const jobId = jobData.job_id;
    
    console.log('✅ 작업 생성:', jobId);

    // 2단계: 작업 상태 폴링
    console.log('⏳ 영상 생성 대기 중...');
    
    const result = await pollJobStatus(jobId);
    
    if (result.status === 'finished' && result.video_url) {
      console.log('✅ 영상 생성 완료:', result.video_url);
      
      return NextResponse.json({
        video_url: `${BACKEND_URL}${result.video_url}`,
        message: '영상이 생성되었습니다!',
        job_id: jobId,
        status: 'finished',
      });
    } else {
      throw new Error(result.error || '영상 생성에 실패했습니다.');
    }

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

// 작업 상태 폴링 함수
async function pollJobStatus(jobId: string): Promise<{
  status: string;
  video_url?: string;
  error?: string;
}> {
  const startTime = Date.now();
  
  while (Date.now() - startTime < MAX_POLLING_TIME) {
    try {
      // 상태 확인
      const statusResponse = await fetch(`${BACKEND_URL}/status/${jobId}`);
      
      if (!statusResponse.ok) {
        throw new Error('작업 상태를 확인할 수 없습니다.');
      }
      
      const statusData = await statusResponse.json();
      console.log(`[${jobId}] 상태: ${statusData.status}, 진행률: ${statusData.progress}%`);
      
      // 완료된 경우
      if (statusData.status === 'finished') {
        // 결과 조회
        const resultResponse = await fetch(`${BACKEND_URL}/result/${jobId}`);
        
        if (!resultResponse.ok) {
          throw new Error('작업 결과를 가져올 수 없습니다.');
        }
        
        const resultData = await resultResponse.json();
        
        if (resultData.status === 'finished' && resultData.video_url) {
          return {
            status: 'finished',
            video_url: resultData.video_url,
          };
        } else {
          return {
            status: 'failed',
            error: resultData.error || '영상 생성에 실패했습니다.',
          };
        }
      }
      
      // 실패한 경우
      if (statusData.status === 'failed') {
        return {
          status: 'failed',
          error: statusData.error || '영상 생성에 실패했습니다.',
        };
      }
      
      // 진행 중인 경우 - 대기 후 재시도
      await new Promise(resolve => setTimeout(resolve, POLLING_INTERVAL));
      
    } catch (error) {
      console.error('폴링 오류:', error);
      throw error;
    }
  }
  
  // 타임아웃
  throw new Error('영상 생성 시간이 초과되었습니다. 다시 시도해주세요.');
}
