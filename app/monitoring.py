#monitoring.py
#here in future will be something like this:
"""
import schedule
import time
import httpx

def check_endpoints():
    try:
        live = httpx.get("http://localhost:8000/health/live", timeout=2.0)
        ready = httpx.get("http://localhost:8000/health/ready", timeout=2.0)
        
        print(f"[Liveness] {live.status_code} | [Readiness] {ready.status_code}")
    except Exception as e:
        print(f"Health check check failed: {e}")

# Run health check every 10 seconds
schedule.every(10).seconds.do(check_endpoints)

while True:
    schedule.run_pending()
    time.sleep(1)

"""