from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from app.api.tasks import router as tasks_router, redis_listener
import threading
import asyncio
from app.events.manager import manager

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/task/ws")
async def ws_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await asyncio.sleep(0.1)  # keep alive
    finally:
        manager.disconnect(websocket)

# include REST routes
app.include_router(tasks_router, prefix="/task")

# start Redis listener
threading.Thread(target=redis_listener, daemon=True).start()
