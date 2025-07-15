import threading
import time
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import configparser
import sounddevice as sd

CONFIG_FILE = 'clients.conf'

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

class VoiceProgram:
    def __init__(self):
        self.running = False
        self.thread = None

    def load_config(self):
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)
        return {s: dict(config.items(s)) for s in config.sections()}

    def listen_loop(self):
        while self.running:
            time.sleep(1)
            print('listening...')

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.listen_loop, daemon=True)
            self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=1)
            self.thread = None

voice_program = VoiceProgram()

@app.get('/', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})

@app.get('/api/get_sound_device')
async def get_sound_device():
    devices = sd.query_devices()
    return JSONResponse(devices)

@app.post('/api/save_config')
async def save_config(data: dict):
    config = configparser.ConfigParser()
    for name, vals in data.items():
        config[name] = vals
    with open(CONFIG_FILE, 'w') as f:
        config.write(f)
    if voice_program.running:
        voice_program.stop()
        voice_program.start()
    return {'status': 'saved'}

@app.get('/api/get_config')
async def get_config():
    return voice_program.load_config()

@app.post('/api/start')
async def start_program():
    voice_program.start()
    return {'running': True}

@app.post('/api/stop')
async def stop_program():
    voice_program.stop()
    return {'running': False}

@app.get('/api/status')
async def status():
    return {'running': voice_program.running}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=30001)
