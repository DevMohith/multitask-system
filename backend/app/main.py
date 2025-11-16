from fastapi import FastAPI
from app.api.tasks import router as tasks_router, redis_listener
import threading

app = FastAPI()

# Start Redis pub/sub listener in background
threading.Thread(target=redis_listener, daemon=True).start()

app.include_router(tasks_router, prefix="/task")
