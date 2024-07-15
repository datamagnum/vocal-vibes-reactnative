#!/usr/bin/env bash
HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-8000}"


gunicorn -k uvicorn.workers.UvicornWorker -c app/core/gunicorn_conf.py app.main:app
