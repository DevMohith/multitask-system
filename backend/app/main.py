from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.tasks import router as tasks_router, redis_listener
import threading

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def start_redis_listener():
    t = threading.Thread(target=redis_listener, daemon=True)
    t.start()
    print("✔ Redis listener started")

# Register routes
app.include_router(tasks_router, prefix="/task")
