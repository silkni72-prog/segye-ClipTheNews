"""
ClipTheNews API 테스트 스크립트
"""
import requests
import time
import sys

# API 설정
BASE_URL = "http://localhost:8000"

# 테스트 뉴스 URL
TEST_URLS = {
    "nyt": "https://www.nytimes.com/2024/01/01/world/asia/japan-earthquake.html",
    "guardian": "https://www.theguardian.com/world/2024/jan/01/new-year-celebrations"
}


def test_health_check():
    """헬스 체크 테스트"""
    print("\n[1/5] 헬스 체크...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        response.raise_for_status()
        data = response.json()
        print(f"✓ 서버 상태: {data['status']}")
        print(f"✓ Redis: {data['redis']}")
        return True
    except Exception as e:
        print(f"✗ 헬스 체크 실패: {e}")
        return False


def create_job(article_url: str, mode: str = "nyt_question"):
    """작업 생성"""
    print(f"\n[2/5] 작업 생성 중... (mode: {mode})")
    print(f"URL: {article_url}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/jobs",
            json={
                "article_url": article_url,
                "mode": mode
            }
        )
        response.raise_for_status()
        data = response.json()
        
        job_id = data['job_id']
        print(f"✓ 작업 생성 완료")
        print(f"  Job ID: {job_id}")
        print(f"  Status: {data['status']}")
        
        return job_id
    except Exception as e:
        print(f"✗ 작업 생성 실패: {e}")
        return None


def check_status(job_id: str, max_wait: int = 120):
    """작업 상태 확인 (폴링)"""
    print(f"\n[3/5] 작업 상태 확인 중...")
    
    start_time = time.time()
    
    while True:
        try:
            response = requests.get(f"{BASE_URL}/status/{job_id}")
            response.raise_for_status()
            data = response.json()
            
            status = data['status']
            progress = data.get('progress', 0)
            message = data.get('message', '')
            
            elapsed = int(time.time() - start_time)
            print(f"  [{elapsed}s] Status: {status} | Progress: {progress}% | {message}")
            
            if status == 'finished':
                print("✓ 작업 완료!")
                return True
            elif status == 'failed':
                error = data.get('error', 'Unknown error')
                print(f"✗ 작업 실패: {error}")
                return False
            
            # 타임아웃 체크
            if elapsed > max_wait:
                print(f"✗ 타임아웃 ({max_wait}초)")
                return False
            
            # 5초 대기
            time.sleep(5)
            
        except Exception as e:
            print(f"✗ 상태 확인 실패: {e}")
            return False


def get_result(job_id: str):
    """작업 결과 조회"""
    print(f"\n[4/5] 작업 결과 조회 중...")
    
    try:
        response = requests.get(f"{BASE_URL}/result/{job_id}")
        response.raise_for_status()
        data = response.json()
        
        if data['status'] == 'finished':
            video_url = data.get('video_url')
            duration = data.get('duration')
            
            print("✓ 결과 조회 완료")
            print(f"  Video URL: {BASE_URL}{video_url}")
            print(f"  처리 시간: {duration}초")
            
            return f"{BASE_URL}{video_url}"
        else:
            print(f"✗ 작업 미완료: {data['status']}")
            return None
            
    except Exception as e:
        print(f"✗ 결과 조회 실패: {e}")
        return None


def download_video(video_url: str, output_path: str = "test_output.mp4"):
    """영상 다운로드"""
    print(f"\n[5/5] 영상 다운로드 중...")
    
    try:
        response = requests.get(video_url, stream=True)
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"✓ 다운로드 완료: {output_path}")
        return True
        
    except Exception as e:
        print(f"✗ 다운로드 실패: {e}")
        return False


def main():
    """메인 테스트 실행"""
    print("=" * 60)
    print("ClipTheNews API 테스트")
    print("=" * 60)
    
    # 1. 헬스 체크
    if not test_health_check():
        print("\n서버가 실행되지 않았거나 Redis 연결 실패")
        print("실행 방법:")
        print("  Docker: docker-compose up -d")
        print("  로컬: backend/run_local.ps1 (또는 run_local.sh)")
        sys.exit(1)
    
    # 2. 작업 생성
    # 테스트용 URL (실제 뉴스 URL로 변경 가능)
    test_url = input("\n뉴스 URL 입력 (Enter = 기본 URL 사용): ").strip()
    if not test_url:
        test_url = "https://www.nytimes.com/2024/01/01/world/example.html"
        print(f"기본 URL 사용: {test_url}")
    
    mode = input("모드 선택 (1=nyt_question, 2=guardian_observe, Enter=1): ").strip()
    mode = "guardian_observe" if mode == "2" else "nyt_question"
    
    job_id = create_job(test_url, mode)
    if not job_id:
        print("\n작업 생성 실패")
        sys.exit(1)
    
    # 3. 상태 확인
    success = check_status(job_id, max_wait=180)
    if not success:
        print("\n작업 처리 실패 또는 타임아웃")
        sys.exit(1)
    
    # 4. 결과 조회
    video_url = get_result(job_id)
    if not video_url:
        print("\n결과 조회 실패")
        sys.exit(1)
    
    # 5. 다운로드
    download = input("\n영상을 다운로드하시겠습니까? (y/n): ").strip().lower()
    if download == 'y':
        download_video(video_url, f"test_output_{job_id[:8]}.mp4")
    
    print("\n" + "=" * 60)
    print("테스트 완료!")
    print("=" * 60)


if __name__ == "__main__":
    main()
