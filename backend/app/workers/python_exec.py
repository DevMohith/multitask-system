import time
import redis
import json

redis_pub = redis.Redis(host="localhost", port=6379, db=0)

def run_python_task(task_id: str, code: str):
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
    return result
