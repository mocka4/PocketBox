import json
import random
from pathlib import Path

BASE = Path.home() / ".pocketbox"
LOCK = BASE / "ports.lock"

BASE.mkdir(exist_ok=True)

def load():
    if LOCK.exists():
        return json.loads(LOCK.read_text())
    return {}

def save(data):
    LOCK.write_text(json.dumps(data, indent=2))

def allocate(container, internal):
    ports = load()

    while True:
        host = random.randint(5000, 9000)
        if host not in ports.values():
            break

    ports[f"{container}:{internal}"] = host
    save(ports)
    return host