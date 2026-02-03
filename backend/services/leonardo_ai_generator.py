"""
Leonardo.ai API 연동 서비스
AI 이미지 생성 기능
"""

import requests
import os
import time
from typing import Optional
import urllib3

# SSL 경고 메시지 비활성화 (개발 환경용)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LEONARDO_API_URL = "https://cloud.leonardo.ai/api/rest/v1"

def generate_ai_image(prompt: str, output_path: str) -> Optional[str]:
    """
    Leonardo.ai API로 이미지 생성
    
    Args:
        prompt: 영어 프롬프트
        output_path: 저장 경로
        
    Returns:
        생성된 이미지 경로 또는 None (실패 시)
    """
    api_key = os.getenv('LEONARDO_API_KEY')
    if not api_key:
        print("[WARN] LEONARDO_API_KEY not found. Skipping AI image generation.")
        print("[INFO] To use AI image generation, set LEONARDO_API_KEY in .env file")
        return None
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # 1. 이미지 생성 요청
    payload = {
        "prompt": prompt,
        "width": 768,
        "height": 1360,  # 9:16 비율 (세로형)
        "num_images": 1,
        "modelId": "6bef9f1b-29cb-40c7-b9df-32b51c1f67d3",  # Leonardo Diffusion XL
        "presetStyle": "CINEMATIC",
        "public": False,
        "guidance_scale": 7,
        "sd_version": "SDXL_0_9",
        "num_inference_steps": 30
    }
    
    try:
        print(f"[INFO] Requesting AI image generation...")
        print(f"[INFO] Prompt: {prompt[:100]}...")
        
        response = requests.post(
            f"{LEONARDO_API_URL}/generations",
            headers=headers,
            json=payload,
            timeout=30,
            verify=False  # SSL 검증 우회 (개발 환경)
        )
        response.raise_for_status()
        
        response_data = response.json()
        generation_id = response_data["sdGenerationJob"]["generationId"]
        print(f"[INFO] Generation ID: {generation_id}")
        
        # 2. 생성 완료 대기 (폴링)
        max_attempts = 60  # 최대 2분 (60 × 2초)
        for attempt in range(max_attempts):
            time.sleep(2)  # 2초 대기
            
            print(f"[INFO] Checking status... (attempt {attempt + 1}/{max_attempts})")
            
            status_response = requests.get(
                f"{LEONARDO_API_URL}/generations/{generation_id}",
                headers=headers,
                timeout=10,
                verify=False
            )
            status_response.raise_for_status()
            
            status_data = status_response.json()
            generation_status = status_data.get("generations_by_pk", {}).get("status")
            
            print(f"[INFO] Status: {generation_status}")
            
            if generation_status == "COMPLETE":
                generated_images = status_data["generations_by_pk"].get("generated_images", [])
                
                if not generated_images:
                    print("[ERROR] No images generated")
                    return None
                
                image_url = generated_images[0]["url"]
                print(f"[INFO] Image URL obtained, downloading...")
                
                # 3. 이미지 다운로드
                img_response = requests.get(image_url, timeout=30, verify=False)
                img_response.raise_for_status()
                
                # 디렉토리 생성
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                with open(output_path, 'wb') as f:
                    f.write(img_response.content)
                
                print(f"[OK] AI image generated and saved: {os.path.basename(output_path)}")
                return output_path
            
            elif generation_status == "FAILED":
                print(f"[ERROR] AI image generation failed")
                return None
        
        print("[WARN] AI image generation timeout (exceeded 2 minutes)")
        return None
        
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            print(f"[ERROR] Invalid Leonardo API key. Please check LEONARDO_API_KEY in .env")
        elif e.response.status_code == 429:
            print(f"[ERROR] Leonardo API rate limit exceeded. Please wait or upgrade plan.")
        else:
            print(f"[ERROR] HTTP error during AI image generation: {e}")
            print(f"[ERROR] Response: {e.response.text if hasattr(e, 'response') else 'N/A'}")
        return None
        
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Network error during AI image generation: {e}")
        return None
        
    except KeyError as e:
        print(f"[ERROR] Unexpected API response format: missing key {e}")
        return None
        
    except Exception as e:
        print(f"[ERROR] Unexpected error during AI image generation: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_leonardo_connection() -> bool:
    """
    Leonardo.ai API 연결 테스트
    
    Returns:
        연결 성공 여부
    """
    api_key = os.getenv('LEONARDO_API_KEY')
    if not api_key:
        print("[ERROR] LEONARDO_API_KEY not found in environment")
        return False
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        # API 키 유효성 확인 (user info endpoint)
        response = requests.get(
            f"{LEONARDO_API_URL}/me",
            headers=headers,
            timeout=10,
            verify=False
        )
        response.raise_for_status()
        
        user_data = response.json()
        username = user_data.get("user_details", [{}])[0].get("user", {}).get("username", "Unknown")
        
        print(f"[OK] Leonardo API connection successful!")
        print(f"[INFO] User: {username}")
        return True
        
    except Exception as e:
        print(f"[ERROR] Leonardo API connection failed: {e}")
        return False
