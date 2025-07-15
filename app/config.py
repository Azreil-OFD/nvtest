import configparser
from pathlib import Path
from typing import Dict, List

CONFIG_PATH = Path('clients.conf')

def load_config() -> Dict[str, Dict[str, str]]:
    parser = configparser.ConfigParser()
    if CONFIG_PATH.exists():
        parser.read(CONFIG_PATH)
    return {section: dict(parser[section]) for section in parser.sections()}

def save_config(data: Dict[str, Dict[str, str]]):
    parser = configparser.ConfigParser()
    for section, values in data.items():
        parser[section] = values
    with CONFIG_PATH.open('w') as f:
        parser.write(f)
