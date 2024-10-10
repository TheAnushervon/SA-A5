#!/bin/bash

echo "Starting FastAPI apps..."

uvicorn user.auth:app --reload --host 0.0.0.0 --port 8000 &
uvicorn message.message:app --reload --host 0.0.0.0 --port 8001 &
uvicorn feed.feed:app --reload --host 0.0.0.0 --port 8002 &

echo "All apps started."
