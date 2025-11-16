import dramatiq
from dramatiq.brokers.redis import RedisBroker

import time
import json
import redis

redis_broker = RedisBroker(host="localhost", port=6379)
dramatiq.set_broker(redis_broker)

redis_pub = redis.Redis(host="localhost", port=6379, db=0)

@dramatiq.actor
def research_task(task_id, query):
    time.sleep(2)
    result = {
        "task_id": task_id,
        "type": "research",
        "result": f"Research result for: {query}"
    }
    redis_pub.publish("task_updates", json.dumps(result))

@dramatiq.actor
def python_task(task_id, code):
    try:
        local = {}
        exec(code, {}, local)
        output = local
    except Exception as e:
        output = {"error": str(e)}

    result = {
        "task_id": task_id,
        "type": "python",
        "result": output
    }
    redis_pub.publish("task_updates", json.dumps(result))
