---
title: Minecraft Experiment
emoji: 🧪
colorFrom: green
colorTo: blue
sdk: docker
app_port: 7860
startup_duration_timeout: 1h
---

# Minecraft Docker Space Experiment

A minimal Minecraft server control panel running on Hugging Face Docker Spaces.

## Features

- HTTP control panel for starting/stopping the server
- Real-time log streaming
- Lightweight Paper server configuration
- Single-click deployment to HF Spaces

## API Endpoints

- `GET /` - Status overview
- `GET /status` - Server status and recent logs
- `POST /start` - Start the Minecraft server
- `POST /stop` - Gracefully stop the server

## Local Testing

```bash
pip install -r requirements.txt
python -m uvicorn app:app --reload --port 7860
```

Then visit `http://localhost:7860/docs` for interactive API docs.
