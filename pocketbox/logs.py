from pathlib import Path

BASE = Path.home() / ".pocketbox"


def show_logs(name: str):
    cdir = BASE / "containers" / f"{name}-1"
    logf = cdir / "logs.txt"

    if not logf.exists():
        print("📭 No logs found")
        return

    print(f"📜 Logs for {name}:\n")
    print(logf.read_text())