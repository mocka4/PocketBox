import os
import json
import signal
import shutil
from pathlib import Path

BASE = Path.home() / ".pocketbox"
PORTS_LOCK = BASE / "ports.lock"

def stop_container(name):
    cdir = BASE / "containers" / f"{name}-1"
    pid_file = cdir / "pid"

    if not pid_file.exists():
        print("❌ container not found")
        return

    pid = int(pid_file.read_text())

    try:
        os.kill(pid, signal.SIGTERM)
        print(f"⏹ stopped {name}")
    except ProcessLookupError:
        print("⚠️ process already stopped")

def rm_container(name):
    cdir = BASE / "containers" / f"{name}-1"

    if not cdir.exists():
        print("❌ container not found")
        return

    # stop if running
    pidf = cdir / "pid"
    if pidf.exists():
        try:
            os.kill(int(pidf.read_text()), signal.SIGTERM)
        except ProcessLookupError:
            pass

    # free ports
    if PORTS_LOCK.exists():
        ports = json.loads(PORTS_LOCK.read_text())
        ports = {k: v for k, v in ports.items() if not k.startswith(f"{name}-1:")}
        PORTS_LOCK.write_text(json.dumps(ports, indent=2))

    shutil.rmtree(cdir)
    print(f"🗑 removed {name}")