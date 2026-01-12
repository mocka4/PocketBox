# pocketbox/supervisor.py
import subprocess
import time
from pathlib import Path

def supervise_container(name: str, cmd: str, log_path: Path, restart: bool = True):
    """
    Run a container command with supervision:
    - Captures logs
    - Restarts if the process dies (if restart=True)
    - Detached from terminal
    """
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.touch(exist_ok=True)

    while True:
        with log_path.open("ab") as f:
            f.write(f"\n=== Starting container '{name}' ===\n".encode())
            f.flush()
            # Start CMD detached
            proc = subprocess.Popen(
                cmd.split(),
                stdout=f,
                stderr=f,
                start_new_session=True
            )
            proc.wait()
            f.write(f"\n=== Container '{name}' exited with code {proc.returncode} ===\n".encode())
            f.flush()
        
        if not restart:
            break
        time.sleep(1)  # small delay before restarting