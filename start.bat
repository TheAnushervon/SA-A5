@echo off
echo Starting FastAPI apps...

start uvicorn user.auth:app --reload --host 0.0.0.0 --port 8000
start uvicorn message.message:app --reload --host 0.0.0.0 --port 8001
start uvicorn feed.feed:app --reload --host 0.0.0.0 --port 8002

echo All apps started.
pause
