from pathlib import Path
import json
import time

BASE = Path.home() / ".pocketbox"
CONTAINERS_DIR = BASE / "containers"

def list_containers():
    if not CONTAINERS_DIR.exists():
        print("No containers found")
        return

    for c in CONTAINERS_DIR.iterdir():
        if c.is_dir():
            pid_file = c / "pid"
            image_file = c / "image"
            started_file = c / "started_at"
            ports_file = c / "ports.json"

            pid = pid_file.read_text() if pid_file.exists() else "stopped"
            image = image_file.read_text() if image_file.exists() else "unknown"
            started = int(started_file.read_text()) if started_file.exists() else 0
            uptime = int(time.time()) - started if started else 0
            ports = json.loads(ports_file.read_text()) if ports_file.exists() else {}

            status = "running" if pid != "stopped" else "stopped"
            ports_str = ", ".join([f"{k}->{v}" for k, v in ports.items()]) if ports else "none"

            print(f"{c.name}: {status}, image={image}, pid={pid}, uptime={uptime}s, ports={ports_str}")