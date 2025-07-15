import threading
import time
from typing import Dict

from .config import load_config

class Program:
    def __init__(self):
        self._thread = None
        self._stop_event = threading.Event()

    def _run(self):
        while not self._stop_event.is_set():
            config = load_config()
            for name, client in config.items():
                print(f"Simulating processing for {name}: {client}")
            time.sleep(1)

    def start(self):
        if self.is_running:
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self):
        if not self.is_running:
            return
        self._stop_event.set()
        self._thread.join()
        self._thread = None

    @property
    def is_running(self) -> bool:
        return self._thread is not None and self._thread.is_alive()
