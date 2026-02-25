# System Monitor

A lightweight, real-time system monitoring tool built with C++ for data collection and Python for API and visualization. Continuously tracks CPU usage, memory consumption, and network statistics, storing metrics in SQLite and serving them via a REST API with a live web dashboard.

## Features

- Real-time system metrics collection (CPU, memory, network)
- Container-aware CPU monitoring via cgroup v2 (`/sys/fs/cgroup/cpu.stat`)
- SQLite database for persistent metric storage
- RESTful API for data access
- Web-based dashboard with live charts
- Docker support for containerized deployment
- Graceful shutdown via signal handling (SIGINT, SIGTERM)
- Built-in CPU stress test endpoint for demo and testing purposes
- Low resource footprint (~1% CPU overhead)

## Technology Stack

**Core Monitoring**
- C++17 — system metrics collection via cgroup v2 and Linux `/proc` filesystem
- SQLite3 — persistent metric storage

**API & Dashboard**
- FastAPI (Python) — REST endpoints
- Chart.js — live data visualization
- Uvicorn — ASGI server

**Build & Deployment**
- Docker + Docker Compose
- Make-based build system

## Architecture

The C++ monitor and Python API run concurrently in a single container:

- **C++ Monitor** — reads cgroup v2 for CPU, `/proc/meminfo` for memory, and `/proc/net/dev` for network I/O every 2 seconds, writing metrics to `metrics.db`
- **Python API Server** — exposes REST endpoints querying `metrics.db` and serves the live web dashboard

CPU usage is measured using cgroup v2 (`/sys/fs/cgroup/cpu.stat`) rather than `/proc/stat`, which gives accurate per-container CPU utilization instead of host-level stats.

## Prerequisites

- Docker Engine
- Docker Compose

For local development without Docker:
- GCC/G++ with C++17 support
- Make
- SQLite3 development libraries (`libsqlite3-dev`)
- Python 3.8+
- Linux with cgroup v2 support (kernel 5.8+)

## Installation & Usage

### Docker Compose (Recommended)

```bash
git clone https://github.com/MridulTailor/system-monitor.git
cd system-monitor

# Build and start
docker compose up --build

# Run in background
docker compose up --build -d

# View logs
docker compose logs -f

# Stop
docker compose down
```

Access the dashboard at `http://localhost:8000`

### Local Development

```bash
# Install dependencies (Ubuntu/Debian)
sudo apt-get install g++ make sqlite3 libsqlite3-dev python3 python3-pip

# Build the C++ monitor
make

# Install Python dependencies
pip3 install -r api/requirements.txt

# Terminal 1 — start the monitor
./monitor

# Terminal 2 — start the API server
uvicorn api.api:app --host 0.0.0.0 --port 8000 --reload
```

## API Endpoints

### `GET /`
Returns the live web dashboard.

### `GET /metrics`
Returns all stored metrics, newest first.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `limit` | integer | 50 | Max records to return |

**Response:**
```json
[
  {
    "timestamp": 1708876543,
    "cpu_pct": 23.5,
    "mem_used_mb": 608,
    "mem_total_mb": 7836,
    "rx_kb": 1024,
    "tx_kb": 512
  }
]
```

### `GET /metrics/latest`
Returns the most recent metric snapshot.

### `GET /metrics/cpu`
Returns CPU usage history. Accepts `limit` parameter.

### `GET /metrics/memory`
Returns memory usage history. Accepts `limit` parameter.

### `GET /metrics/network`
Returns network I/O history. Accepts `limit` parameter.

### `POST /demo/stress`
Starts or stops a CPU stress test for demo purposes. Spawns configurable worker threads performing CPU-intensive computation.

**Request:**
```json
{
  "enabled": true,
  "workers": 2
}
```

**Response:**
```json
{
  "status": "started",
  "workers": 2,
  "message": "CPU stress test started with 2 worker(s)"
}
```

### `GET /demo/stress/status`
Returns the current stress test state.

```json
{
  "active": true,
  "workers": 2,
  "threads_alive": 2
}
```

Interactive API docs available at `http://localhost:8000/docs`

## Project Structure

```
system-monitor/
├── src/
│   ├── main.cpp                    # Main monitoring loop + signal handling
│   └── collectors/
│       ├── cpu_collector.cpp       # CPU usage via cgroup v2
│       ├── cpu_collector.h
│       ├── mem_collector.cpp       # Memory stats via /proc/meminfo
│       ├── mem_collector.h
│       ├── net_collector.cpp       # Network I/O via /proc/net/dev
│       ├── net_collector.h
│       ├── db_logger.cpp           # SQLite persistence layer
│       └── db_logger.h
├── api/
│   ├── api.py                      # FastAPI server + stress test endpoints
│   ├── dashboard.html              # Live Chart.js dashboard
│   └── requirements.txt
├── tests/                          # Unit tests
├── Makefile
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .gitignore
└── README.md
```

## Database Schema

```sql
CREATE TABLE IF NOT EXISTS metrics (
    timestamp    INTEGER NOT NULL,
    cpu_pct      REAL,
    mem_used_mb  INTEGER,
    mem_total_mb INTEGER,
    rx_kb        INTEGER,
    tx_kb        INTEGER
);
```

## Development

```bash
# Build with debug symbols
make CXXFLAGS="-std=c++17 -g -Wall -Wextra"

# Run tests
pytest tests/

# Clean build artifacts
make clean
```

## Platform Support

Linux only (Ubuntu 20.04+, Debian 11+) with cgroup v2 support (kernel 5.8+). Use Docker for development on macOS or Windows — the Docker VM provides the required Linux kernel environment.

## License

MIT License