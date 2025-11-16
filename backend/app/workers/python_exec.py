import time

def run_python_task(task_id: str, code: str):
    # WARNING: sandboxing must be added for real production
    try:
        output = {}
        exec(code, {}, output)
        result = output
    except Exception as e:
        result = {"error": str(e)}

    time.sleep(1)
    return {
        "task_id": task_id,
        "type": "python",
        "result": result
    }
