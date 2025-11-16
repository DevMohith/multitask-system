from pydantic import BaseModel

class TaskStatus(BaseModel):
    id: str
    status: str
    result: dict | None = None
