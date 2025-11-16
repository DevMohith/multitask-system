import redis
import os
from dotenv import load_dotenv

load_dotenv

redis_conn = redis.Redis(
    host=os.getenv("REDIS_HOST", "LOCALHOST"),
    port=int(os.getenv("REDIS_PORT","6379")),
    db=0
)