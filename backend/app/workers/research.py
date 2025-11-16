import time
import redis
import json

redis_pub = redis.Redis(host="localhost", port=6379, db=0)

def run_research_task(task_id: str, query: str):
    time.sleep(2)

    result = {
        "task_id": task_id,
        "type": "research",
        "result": f"Research result for: {query}"
    }

    # Publish to Redis channel for FastAPI WebSocket relay
    redis_pub.publish("task_updates", json.dumps(result))

    return result

    
# rqworker default
