import time

def run_research_task(task_id: str, query: str):
    time.sleep(3)

    return {
        "task_id": task_id,
        "type": "research",
        "result": f"Simulated research result for: {query}"
    }