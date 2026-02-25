FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    g++ \
    make \
    sqlite3 \
    libsqlite3-dev \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app