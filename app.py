Root=1-69d2811a-4ac137fa05258d9f71073322Root=1-69d2811a-4ac137fa05258d9f71073322import os
import subprocess
import threading
from collections import deque
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

MC_DIR = "/app/mc"
MC_JAR = os.path.join(MC_DIR, "server.jar")
JAVA_CMD = ["java", "-Xms512M", "-Xmx1024M", "-jar", MC_JAR, "nogui"]

process = None
logs = deque(maxlen=200)

def stream_logs(proc):
    for line in proc.stdout:
        logs.append(line.rstrip())

@app.get("/")
def home():
    return {
        "message": "Minecraft experiment controller",
        "running": process is not None and process.poll() is None
    }

@app.get("/status")
def status():
    running = process is not None and process.poll() is None
    return {
        "running": running,
        "logs": list(logs)[-50:]
    }

@app.post("/start")
def start():
    global process
    if process is not None and process.poll() is None:
        return JSONResponse({"ok": False, "message": "already running"}, status_code=400)

    process = subprocess.Popen(
        JAVA_CMD,
        cwd=MC_DIR,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    threading.Thread(target=stream_logs, args=(process,), daemon=True).start()
    return {"ok": True, "message": "server starting"}

@app.post("/stop")
def stop():
    global process
    if process is None or process.poll() is not None:
        return JSONResponse({"ok": False, "message": "not running"}, status_code=400)

    process.stdin.write("stop\n")
    process.stdin.flush()
    return {"ok": True, "message": "stop sent"}
