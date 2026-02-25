import sqlite3
import threading
import time
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI(title="System Monitor API")

# Stress test state
stress_lock = threading.Lock()
stress_state = {
    "active": False,
    "threads": [],
    "stop_flag": False,
    "num_workers": 2
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "/app/metrics.db"

def get_db(path=DB_PATH):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/")
def dashboard():
    return FileResponse("/app/api/dashboard.html")

@app.get("/metrics")
def get_all_metrics(limit: int = 50):
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM metrics ORDER BY timestamp DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.get("/metrics/latest")
def get_latest_stats():
    conn = get_db(DB_PATH)
    row = conn.execute(
        "SELECT * FROM metrics ORDER BY timestamp DESC LIMIT 1"
    ).fetchone()
    conn.close()
    return dict(row) if row else {}

@app.get("/metrics/cpu")
def get_cpu_stats(limit: int = 50):
    conn = get_db(DB_PATH)
    rows = conn.execute(
        "SELECT timestamp, cpu_pct FROM metrics ORDER BY timestamp DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.get("/metrics/memory")
def get_memory_stats(limit: int = 50):
    conn = get_db(DB_PATH)
    rows = conn.execute(
        "SELECT timestamp, mem_used_mb, mem_total_mb FROM metrics ORDER BY timestamp DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.get("/metrics/network")
def get_network_stats(limit: int = 50):
    conn = get_db(DB_PATH)
    rows = conn.execute(
        "SELECT timestamp, rx_kb, tx_kb FROM metrics ORDER BY timestamp DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]

# CPU Stress Generator for Demo
def cpu_stress_worker():
    """Perform CPU-intensive work until stop_flag is set."""
    while not stress_state["stop_flag"]:
        # Recompute continuously to maintain CPU load
        for n in range(2, 50000):
            if stress_state["stop_flag"]:
                break
            # Check if n is prime (CPU-intensive)
            all(n % i != 0 for i in range(2, int(n ** 0.5) + 1))
class StressRequest(BaseModel):
    enabled: bool
    workers: int = 2

@app.post("/demo/stress")
def toggle_stress(request: StressRequest):
    """Toggle CPU stress testing for demo purposes."""
    
    with stress_lock:
        if request.enabled and not stress_state["active"]:
            # Start stress test
            stress_state["active"] = True  # Set immediately to prevent race condition
            stress_state["stop_flag"] = False
            stress_state["num_workers"] = min(max(request.workers, 1), 8)  # Limit 1-8 workers
            stress_state["threads"] = []
            
            for i in range(stress_state["num_workers"]):
                t = threading.Thread(target=cpu_stress_worker, daemon=True, name=f"StressWorker-{i}")
                t.start()
                stress_state["threads"].append(t)
            
            return {
                "status": "started",
                "workers": stress_state["num_workers"],
                "message": f"CPU stress test started with {stress_state['num_workers']} worker(s)"
            }
        
        elif not request.enabled and stress_state["active"]:
            # Stop stress test
            stress_state["stop_flag"] = True
            stress_state["active"] = False
            threads_to_join = stress_state["threads"][:]
            stress_state["threads"] = []
    
    # Join threads outside the lock to avoid blocking other requests
    if not request.enabled and threads_to_join:
        for t in threads_to_join:
            t.join(timeout=2.0)
        
        return {
            "status": "stopped",
            "message": "CPU stress test stopped"
        }
    
    with stress_lock:
        return {
            "status": "active" if stress_state["active"] else "inactive",
            "workers": stress_state["num_workers"] if stress_state["active"] else 0,
            "message": f"Stress test already {'active' if stress_state['active'] else 'inactive'}"
        }

@app.get("/demo/stress/status")
def stress_status():
    """Get current stress test status."""
    with stress_lock:
        return {
            "active": stress_state["active"],
            "workers": stress_state["num_workers"] if stress_state["active"] else 0,
            "threads_alive": sum(1 for t in stress_state["threads"] if t.is_alive())
        }

