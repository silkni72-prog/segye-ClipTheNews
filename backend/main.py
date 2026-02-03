from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from models.schemas import VideoRequest, VideoResponse
from services.scraper import scrape_news
from services.video_generator import generate_video
from services.stock_image import get_stock_images, extract_keyword_from_title
from services.scenario_generator import generate_scenario_from_title
from services.ai_image_prompt_generator import generate_image_prompt
from services.leonardo_ai_generator import generate_ai_image
import os
import uuid
from pathlib import Path
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

app = FastAPI(
    title="ClipTheNews API",
    description="뉴스 URL을 10초 세로형 영상으로 변환하는 API",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://frontend-beta-jet-95.vercel.app",
        "https://*.vercel.app",  # 모든 Vercel 도메인 허용
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 출력 디렉토리 확인 및 생성
output_dir = Path(__file__).parent / "output"
output_dir.mkdir(exist_ok=True)

@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "message": "ClipTheNews API",
        "version": "1.0.0",
        "endpoints": {
            "POST /generate": "영상 생성",
            "GET /download/{filename}": "영상 다운로드"
        }
    }

@app.post("/generate", response_model=VideoResponse)
async def create_video(request: VideoRequest):
    """
    뉴스 URL과 시나리오를 받아 10초 세로형 영상 생성
    
    Args:
        request: VideoRequest {news_url: str, scenario: str}
        
    Returns:
        VideoResponse: {video_url: str, message: str}
    """
    try:
        # 입력 검증
        if not request.news_url or not request.news_url.startswith(('http://', 'https://')):
            raise HTTPException(status_code=400, detail="유효한 URL을 입력해주세요.")
        
        # 시나리오 검증 (선택사항으로 변경)
        if request.scenario and len(request.scenario) > 500:
            raise HTTPException(status_code=400, detail="시나리오는 500자 이하로 입력해주세요.")
        
        # 1. 뉴스 스크래핑
        print(f"[Step 1/3] Scraping news from: {request.news_url}")
        try:
            news_data = scrape_news(request.news_url)
        except Exception as e:
            raise HTTPException(
                status_code=400, 
                detail=f"뉴스 스크래핑에 실패했습니다: {str(e)}"
            )
        
        print(f"[OK] Scraped {len(news_data.get('images', []))} images from news")
        print(f"[OK] Title: {news_data['title']}")
        
        # 2. 하이브리드 이미지 수집: 뉴스 → Unsplash → Leonardo AI
        target_image_count = 4  # 목표 이미지 수 (20초 영상용)
        images = news_data.get('images', [])
        scraped_count = len(images)
        
        print(f"[Step 2/3] Image collection: {len(images)}/{target_image_count} from news")
        
        # 2-1. Unsplash로 보충 (최대 2개까지만)
        if len(images) < target_image_count:
            unsplash_needed = min(2, target_image_count - len(images))
            print(f"[Step 2/3] Trying Unsplash for {unsplash_needed} more images...")
            
            keyword = extract_keyword_from_title(news_data['title'])
            stock_images = get_stock_images(
                keyword=keyword, 
                count=unsplash_needed
            )
            
            if stock_images:
                images.extend(stock_images)
                print(f"[OK] Added {len(stock_images)} stock images from Unsplash")
            else:
                print("[WARN] Unsplash fetch failed or no API key")
        
        # 2-2. Leonardo AI로 나머지 보충
        if len(images) < target_image_count:
            ai_needed = target_image_count - len(images)
            print(f"[Step 2/3] Trying Leonardo AI for {ai_needed} more images...")
            
            # 임시 디렉토리 생성
            temp_dir = os.path.join(os.path.dirname(__file__), 'temp')
            os.makedirs(temp_dir, exist_ok=True)
            
            ai_count = 0
            for i in range(len(images), target_image_count):
                prompt = generate_image_prompt(news_data['title'], i, target_image_count)
                temp_path = os.path.join(temp_dir, f'ai_image_{i}_{uuid.uuid4().hex[:8]}.jpg')
                
                ai_image_path = generate_ai_image(prompt, temp_path)
                if ai_image_path:
                    images.append(ai_image_path)
                    ai_count += 1
                else:
                    print(f"[WARN] Failed to generate AI image {i+1}")
            
            if ai_count > 0:
                print(f"[OK] Added {ai_count} AI-generated images from Leonardo")
            else:
                print("[WARN] Leonardo AI generation failed or no API key")
        
        # 최종 이미지 확인
        if not images or len(images) == 0:
            hints = []
            if not os.getenv('UNSPLASH_ACCESS_KEY'):
                hints.append("Unsplash API 키")
            if not os.getenv('LEONARDO_API_KEY'):
                hints.append("Leonardo API 키")
            
            hint_text = ""
            if hints:
                hint_text = f" {' 또는 '.join(hints)}를 설정하면 자동으로 이미지를 보충합니다."
            
            raise HTTPException(
                status_code=400,
                detail=f"이미지를 찾을 수 없습니다. 다른 뉴스 URL을 시도해주세요.{hint_text}"
            )
        
        print(f"[OK] Total images collected: {len(images)}/{target_image_count}")
        
        # 2-1. 시나리오 자동 생성 (입력되지 않은 경우)
        scenario = request.scenario
        if not scenario or len(scenario.strip()) == 0:
            print("[INFO] No scenario provided. Auto-generating...")
            scenario = generate_scenario_from_title(news_data['title'])
            print(f"[OK] Auto-generated scenario: {scenario}")
        else:
            print(f"[INFO] Using user-provided scenario: {scenario}")
        
        # 3. 영상 생성
        print("[Step 3/3] Generating video...")
        try:
            filename = generate_video(
                images=images,
                scenario=scenario,
                title=news_data['title']
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"영상 생성에 실패했습니다: {str(e)}"
            )
        
        print(f"[OK] Video generated: {filename}")
        
        # 4. 응답 반환
        video_url = f"/download/{filename}"
        
        # 사용된 이미지 소스 정보 계산
        stock_count = len([img for img in images if 'unsplash' in img.lower() or 'stock' in img.lower()])
        ai_count = len([img for img in images if 'ai_image' in img.lower()])
        news_count = len(images) - stock_count - ai_count
        
        # 메시지 생성
        message_parts = [f"영상이 성공적으로 생성되었습니다. (뉴스: {news_count}개"]
        if stock_count > 0:
            message_parts.append(f"스톡: {stock_count}개")
        if ai_count > 0:
            message_parts.append(f"AI생성: {ai_count}개")
        
        message = ", ".join(message_parts) + ")"
        
        return VideoResponse(
            video_url=video_url,
            message=message
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"영상 생성 중 오류가 발생했습니다: {str(e)}"
        )

@app.get("/download/{filename}")
async def download_video(filename: str):
    """
    생성된 영상 파일 다운로드
    
    Args:
        filename: 영상 파일명
        
    Returns:
        FileResponse: 영상 파일
    """
    file_path = output_dir / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="파일을 찾을 수 없습니다.")
    
    return FileResponse(
        path=file_path,
        media_type="video/mp4",
        filename=filename
    )

@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
