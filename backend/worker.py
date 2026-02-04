"""
RQ Worker 실행 스크립트
백그라운드 작업 처리
Windows 호환 모드
"""
import sys
import platform
from redis import Redis
from rq import Worker, Queue, Connection, SimpleWorker
from config import REDIS_HOST, REDIS_PORT, REDIS_DB

# Redis 연결
redis_conn = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

if __name__ == '__main__':
    print("=" * 50)
    print("RQ Worker 시작 (Windows 호환 모드)")
    print(f"Redis: {REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}")
    print(f"Platform: {platform.system()}")
    print("=" * 50)
    
    with Connection(redis_conn):
        # Windows에서는 SimpleWorker 사용 (fork() 및 SIGALRM 미지원)
        if platform.system() == 'Windows':
            print("Windows 감지 - SimpleWorker 사용")
            worker = SimpleWorker(['default'], connection=redis_conn)
        else:
            worker = Worker(['default'], connection=redis_conn)
        
        print(f"Worker 타입: {type(worker).__name__}")
        print("작업 대기 중...")
        worker.work(with_scheduler=False)
