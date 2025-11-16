import dramatiq
from dramatiq.brokers.redis import RedisBroker
import requests
import time
import json
import redis
import os

redis_broker = RedisBroker(host="localhost", port=6379)
dramatiq.set_broker(redis_broker)

redis_pub = redis.Redis(host="localhost", port=6379, db=0)

@dramatiq.actor
def research_task(task_id, query):
    print("🔥 WORKER RECEIVED TASK:", task_id, query)

    # TRY WORLD BANK POPULATION DATA
    population = None
    if "india" in query.lower() and "population" in query.lower():
        try:
            wb_url = "https://api.worldbank.org/v2/country/IND/indicator/SP.POP.TOTL"
            wb_params = {"format": "json", "per_page": 1}
            wb_res = requests.get(wb_url, params=wb_params, timeout=10)
            wb_json = wb_res.json()

            # Extract most recent year's population
            population_data = wb_json[1][0]
            population = population_data.get("value")
        except Exception as e:
            print("⚠️ World Bank fetch failed:", e)

    # GET WIKIPEDIA SUMMARY
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "prop": "extracts",
        "exintro": True,
        "explaintext": True,
        "format": "json",
        "titles": query
    }

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
        )
    }

    summary = None
    link = None

    try:
        r = requests.get(url, params=params, headers=headers, timeout=10)
        print("📥 WIKI RAW STATUS:", r.status_code)
        print("📥 WIKI RAW TEXT SAMPLE:", r.text[:200])

        data = r.json()
        pages = data.get("query", {}).get("pages", {})
        page = next(iter(pages.values()))

        summary = page.get("extract", "No summary available.")
        pageid = page.get("pageid")
        link = f"https://en.wikipedia.org/?curid={pageid}" if pageid else None

    except Exception as e:
        print("❌ Wiki error:", e)

    # 3️⃣ FINAL RESPONSE
    final_summary = summary

    # If summary empty but population exists → create own summary
    if (not summary or summary.strip() == "") and population:
        final_summary = f"The current estimated population of India is {population:,} people."

    result = {
        "task_id": task_id,
        "type": "research",
        "query": query,
        "summary": final_summary,
        "population": population,
        "links": [{"title": "Wikipedia Page", "url": link}] if link else [],
        "images": []
    }

    print("🔥 WORKER PUBLISHING TO REDIS:", result)
    redis_pub.publish("task_updates", json.dumps(result))
    print("🔥 WORKER FINISHED PROCESSING:", task_id)

    
@dramatiq.actor
def python_task(task_id, code):
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
