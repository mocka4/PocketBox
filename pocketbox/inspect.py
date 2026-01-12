import time
from pathlib import Path

BASE = Path.home() / ".pocketbox"


def inspect_container(name: str):
    cdir = BASE / "containers" / f"{name}-1"
    meta = cdir / "meta"
    pidf = cdir / "pid"
    logf = cdir / "logs.txt"

    if not meta.exists():
        print("❌ Container not found")
        return

    data = {}
    for line in meta.read_text().splitlines():
        k, v = line.split("=", 1)
        data[k] = v

    status = "running" if pidf.exists() else "stopped"
    uptime = ""
    if "started" in data:
        uptime = f"{int(time.time()) - int(data['started'])}s"

    print(f"Name: {name}-1")
    print(f"Image: {data.get('image')}")
    print(f"Status: {status}")
    if pidf.exists():
        print(f"PID: {pidf.read_text()}")
    print(f"CMD: {data.get('cmd')}")
    print(f"Uptime: {uptime}")
    print(f"Ports: {data.get('ports') or 'none'}")
    print(f"Logs: {logf}")