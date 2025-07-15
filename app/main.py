from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .config import load_config, save_config
from .program import Program

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

program = Program()

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "status": program.is_running})

@app.get("/api/get_sound_device")
def get_sound_device():
    try:
        import sounddevice as sd
        devices = sd.query_devices()
        result = []
        for idx, dev in enumerate(devices):
            result.append({"id": idx, "name": dev['name']})
        return result
    except Exception:
        # Fallback when sounddevice or PortAudio is unavailable
        return []

@app.get("/api/get_config")
def get_config():
    return load_config()

@app.post("/api/save_config")
def save_cfg(data: dict):
    save_config(data)
    if program.is_running:
        program.stop()
        program.start()
    return {"status": "ok"}

@app.post("/api/start")
def start():
    program.start()
    return {"running": True}

@app.post("/api/stop")
def stop():
    program.stop()
    return {"running": False}

@app.get("/api/status")
def status():
    return {"running": program.is_running}
