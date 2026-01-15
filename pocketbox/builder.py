from pathlib import Path
import shutil
import subprocess
import json

BASE = Path.home() / ".pocketbox"

def build_image(name):
    img = BASE / "images" / name
    rootfs = img / "rootfs"

    shutil.rmtree(img, ignore_errors=True)
    rootfs.mkdir(parents=True)

    pocketfile = Path("Pocketfile")
    if not pocketfile.exists():
        raise RuntimeError("Pocketfile not found in current directory")

    instructions = []
    for line in pocketfile.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        k, v = line.split(" ", 1)
        instructions.append((k.upper(), v.strip()))

    for key, val in instructions:
        if key == "RUN":
            print(f"🔧 Running: {val}")
            subprocess.check_call(val, shell=True, cwd=rootfs)

        elif key == "COPY":
            src, dst = val.split()
            shutil.copy(src, rootfs / dst)

        elif key == "CMD":
            (img / "cmd").write_text(val)

        elif key == "EXPOSE":
            ports = {}
            pfile = img / "ports.json"
            if pfile.exists():
                ports = json.loads(pfile.read_text())
            ports[val] = None
            pfile.write_text(json.dumps(ports, indent=2))

        else:
            print(f"⚠ Unknown instruction: {key}")