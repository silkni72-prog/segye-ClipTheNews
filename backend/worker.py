"""
RQ Worker 실행 스크립트
백그라운드 작업 처리
"""
import sys
from redis import Redis
from rq import Worker, Queue, Connection
from config import REDIS_HOST, REDIS_PORT, REDIS_DB

# Redis 연결
redis_conn = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

if __name__ == '__main__':
    print("=" * 50)
    print("RQ Worker 시작")
    print(f"Redis: {REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}")
    print("=" * 50)
    
    with Connection(redis_conn):
        worker = Worker(['default'], connection=redis_conn)
        worker.work()
