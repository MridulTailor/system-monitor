import sqlite3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

app = FastAPI(title="System Monitor API")

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
