import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_status():
    r = client.get('/api/status')
    assert r.status_code == 200
    assert 'running' in r.json()

def test_get_sound_device():
    r = client.get('/api/get_sound_device')
    assert r.status_code == 200
    assert isinstance(r.json(), list)
