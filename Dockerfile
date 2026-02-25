FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    g++ \
    make \
    cmake \
    sqlite3 \
    libsqlite3-dev \
    python3 \
    python3-pip \
    vim \
    gdb \
    valgrind \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
