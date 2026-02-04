"""
FastAPI 메인 애플리케이션
Redis + RQ 기반 백그라운드 영상 생성
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from redis import Redis
from rq import Queue
from rq.job import Job
import uuid
from pathlib import Path

from models.schemas import (
    JobRequest, JobResponse, JobStatus, JobResult
)
from config import (
    REDIS_URL, REDIS_HOST, REDIS_PORT, REDIS_DB,
    OUTPUT_DIR, JOB_RESULT_TTL, JOB_TIMEOUT
)
from tasks.render_task import render_job

# FastAPI 앱
app = FastAPI(
    title="ClipTheNews API",
    description="뉴스 기사를 20초 세로 숏폼으로 자동 생성하는 API",
    version="2.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://*.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redis 연결
try:
    redis_conn = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)
    queue = Queue(connection=redis_conn)
    print(f"[OK] Redis 연결 성공: {REDIS_HOST}:{REDIS_PORT}")
except Exception as e:
    print(f"[ERROR] Redis 연결 실패: {e}")
    redis_conn = None
    queue = None


@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "service": "ClipTheNews API",
        "version": "2.0.0",
        "description": "뉴스 기사를 20초 세로 숏폼으로 자동 생성",
        "endpoints": {
            "POST /jobs": "영상 생성 작업 요청",
            "GET /status/{job_id}": "작업 상태 조회",
            "GET /result/{job_id}": "작업 결과 조회",
            "GET /download/{filename}": "영상 다운로드"
        },
        "redis_connected": redis_conn is not None
    }


@app.post("/jobs", response_model=JobResponse)
async def create_job(request: JobRequest):
    """
    영상 생성 작업 생성
    
    Args:
        request: {article_url: str, mode: 'nyt_question' | 'guardian_observe'}
        
    Returns:
        {job_id: str, status: str, message: str}
    """
    if not redis_conn or not queue:
        raise HTTPException(
            status_code=503,
            detail="Redis 연결 실패. 서버 관리자에게 문의하세요."
        )
    
    # URL 검증
    if not request.article_url.startswith(('http://', 'https://')):
        raise HTTPException(
            status_code=400,
            detail="유효한 URL을 입력해주세요."
        )
    
    try:
        # Job ID 생성
        job_id = str(uuid.uuid4())
        
        # RQ 작업 등록
        job = queue.enqueue(
            render_job,
            job_id,  # render_job의 첫 번째 인자
            request.article_url,  # render_job의 두 번째 인자
            request.mode.value,  # render_job의 세 번째 인자
            job_id=job_id,  # RQ Job ID 설정
            job_timeout=JOB_TIMEOUT,
            result_ttl=JOB_RESULT_TTL
        )
        
        print(f"[{job_id}] 작업 생성: {request.article_url} (mode: {request.mode})")
        
        return JobResponse(
            job_id=job_id,
            status="queued",
            message="작업이 대기열에 추가되었습니다."
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"작업 생성 실패: {str(e)}"
        )


@app.get("/status/{job_id}", response_model=JobStatus)
async def get_job_status(job_id: str):
    """
    작업 상태 조회
    
    Args:
        job_id: 작업 ID
        
    Returns:
        {job_id: str, status: str, progress: int, message: str}
    """
    if not redis_conn:
        raise HTTPException(
            status_code=503,
            detail="Redis 연결 실패"
        )
    
    try:
        job = Job.fetch(job_id, connection=redis_conn)
        
        # RQ 상태 매핑
        status_map = {
            'queued': 'queued',
            'started': 'started',
            'finished': 'finished',
            'failed': 'failed',
            'deferred': 'queued',
            'scheduled': 'queued'
        }
        
        status = status_map.get(job.get_status(), 'unknown')
        
        # 진행률 추정
        progress = 0
        message = ""
        
        if status == 'queued':
            progress = 0
            message = "대기 중..."
        elif status == 'started':
            progress = 50
            message = "영상 생성 중..."
        elif status == 'finished':
            progress = 100
            message = "완료"
        elif status == 'failed':
            progress = 0
            message = "실패"
        
        error = None
        if status == 'failed' and job.exc_info:
            error = str(job.exc_info)
        
        return JobStatus(
            job_id=job_id,
            status=status,
            progress=progress,
            message=message,
            error=error
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"작업을 찾을 수 없습니다: {str(e)}"
        )


@app.get("/result/{job_id}", response_model=JobResult)
async def get_job_result(job_id: str):
    """
    작업 결과 조회
    
    Args:
        job_id: 작업 ID
        
    Returns:
        {job_id: str, status: str, video_url: str, duration: float}
    """
    if not redis_conn:
        raise HTTPException(
            status_code=503,
            detail="Redis 연결 실패"
        )
    
    try:
        job = Job.fetch(job_id, connection=redis_conn)
        status = job.get_status()
        
        if status == 'finished':
            result = job.result
            
            if result and result.get('status') == 'success':
                video_filename = result.get('video_path')
                
                return JobResult(
                    job_id=job_id,
                    status='finished',
                    video_url=f"/download/{video_filename}",
                    duration=result.get('duration')
                )
            else:
                # 작업은 완료되었지만 실패
                return JobResult(
                    job_id=job_id,
                    status='failed',
                    error=result.get('error', '알 수 없는 오류')
                )
        
        elif status == 'failed':
            error = str(job.exc_info) if job.exc_info else "작업 실패"
            return JobResult(
                job_id=job_id,
                status='failed',
                error=error
            )
        
        else:
            # 아직 진행 중
            return JobResult(
                job_id=job_id,
                status=status,
                error=None
            )
        
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"작업을 찾을 수 없습니다: {str(e)}"
        )


@app.get("/download/{filename}")
async def download_video(filename: str):
    """
    생성된 영상 다운로드
    
    Args:
        filename: 파일명
        
    Returns:
        FileResponse
    """
    file_path = OUTPUT_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="파일을 찾을 수 없습니다."
        )
    
    return FileResponse(
        path=file_path,
        media_type="video/mp4",
        filename=filename
    )


@app.get("/health")
async def health_check():
    """헬스 체크"""
    redis_status = "connected" if redis_conn else "disconnected"
    
    return {
        "status": "healthy",
        "redis": redis_status,
        "queue_size": len(queue) if queue else 0
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
