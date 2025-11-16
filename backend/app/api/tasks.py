from fastapi import APIRouter, WebSocket
from rq import Queue
from uuid import uuid4
from app.queue.redis_conn import redis_conn
from app.workers.research import run_research_task
from app.workers.python_exec import run_python_task
from app.events.manager import manager
import asyncio
import threading
import redis
import json


router = APIRouter()
task_queue = Queue("default", connection=redis_conn)

redis_client = redis.Redis(host="localhost", port=6379, db=0)

def redis_listener():
    pubsub = redis_client.pubsub()
    pubsub.subscribe("task_updates")

    for message in pubsub.listen():
        if message["type"] == "message":
            data = json.loads(message["data"])
            asyncio.run(manager.broadcast(data))

@router.post("/create")
def create_task(type: str, payload: str):
    task_id = str(uuid4())

    if type == "research":
        job = task_queue.enqueue(run_research_task, task_id, payload)

    elif type == "python":
        job = task_queue.enqueue(run_python_task, task_id, payload)

    else:
        return {"error": "Unknown task type"}

    return {"task_id": task_id, "status": "queued"}


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # keep alive
    except:
        manager.disconnect(websocket)
