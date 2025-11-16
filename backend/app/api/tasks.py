from fastapi import APIRouter, WebSocket
from uuid import uuid4
from app.events.manager import manager
from worker import research_task, python_task
import asyncio
import threading
import redis
import json
import time

router = APIRouter()

redis_client = redis.Redis(host="localhost", port=6379, db=0)

def redis_listener():
    import asyncio
    import time

    print("🚀 Redis listener started")

    pubsub = redis_client.pubsub()
    pubsub.subscribe("task_updates")

    # IMPORTANT: create new loop for this thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    while True:
        message = pubsub.get_message()

        if message and message["type"] == "message":
            data = json.loads(message["data"])
            print("📡 Redis received:", data)

            # Schedule WS broadcast on THIS thread's loop
            loop.call_soon_threadsafe(
                asyncio.create_task,
                manager.broadcast(data)
            )

        time.sleep(0.05)

@router.post("/create")
def create_task(type: str, payload: str):
    task_id = str(uuid4())

    if type == "research":
        research_task.send(task_id, payload)   # Dramatiq
    elif type == "python":
        python_task.send(task_id, payload)     # Dramatiq

    return {"task_id": task_id, "status": "queued"}

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await asyncio.sleep(0.1)  # prevent blocking
    except:
        manager.disconnect(websocket)
