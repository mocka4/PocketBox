import os
import shutil
import subprocess
import time
from pathlib import Path
from datetime import datetime
import urllib.request
import zipfile
import tempfile


BASE_DIR = Path.home() / ".pocketbox"
IMAGES_DIR = BASE_DIR / "images"
CONTAINERS_DIR = BASE_DIR / "containers"

IMAGES_DIR.mkdir(parents=True, exist_ok=True)
CONTAINERS_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------
# Helpers
# -------------------------

def next_container_name(image: str, custom: str | None = None) -> str:
    """Generate a unique container name"""
    if custom:
        return custom

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{image}-{timestamp}"


BASE_IMAGE_REPO = "https://github.com/mocka4/pocketbox-base-images/archive/refs/heads/main.zip"

def pull_image(image: str):
    """
    Pull a base image from the Pocketbox base image repository
    """
    target = IMAGES_DIR / image

    if target.exists():
        raise RuntimeError(f"Image '{image}' already exists locally")

    with tempfile.TemporaryDirectory() as tmp:
        zip_path = Path(tmp) / "images.zip"

        # Download repo
        urllib.request.urlretrieve(BASE_IMAGE_REPO, zip_path)

        # Extract
        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(tmp)

        extracted = Path(tmp) / "pocketbox-base-images-main" / image

        if not extracted.exists():
            raise RuntimeError(f"Base image '{image}' not found in registry")

        shutil.copytree(extracted, target)

    return image


# -------------------------
# Image build
# -------------------------

def build_image(source: str | None = None) -> str:
    src = Path(source) if source else Path.cwd()
    pocketfile = src / "Pocketfile"

    if not pocketfile.exists():
        raise RuntimeError("Pocketfile not found")

    image_name = src.name
    image_dir = IMAGES_DIR / image_name

    if image_dir.exists():
        shutil.rmtree(image_dir)

    image_dir.mkdir(parents=True)

    for item in src.iterdir():
        if item.name == "__pycache__":
            continue
        if item.is_file():
            shutil.copy(item, image_dir / item.name)
        elif item.is_dir():
            shutil.copytree(item, image_dir / item.name)

    cmd_file = image_dir / "cmd"
    if not cmd_file.exists():
        raise RuntimeError("Missing cmd file in image")

    return image_name


# -------------------------
# Container lifecycle
# -------------------------

def run_container(image: str, supervised: bool = False, name: str | None = None) -> str:
    image_dir = IMAGES_DIR / image
    if not image_dir.exists():
        raise RuntimeError(f"Image '{image}' does not exist")

    cmd_file = image_dir / "cmd"
    cmd = cmd_file.read_text().strip().split()

    name = next_container_name(image, name)
    cdir = CONTAINERS_DIR / name
    cdir.mkdir(parents=True, exist_ok=True)

    log = cdir / "logs.txt"
    pidf = cdir / "pid"
    meta = cdir / "meta"

    with open(log, "a") as logs:
        proc = subprocess.Popen(
            cmd,
            cwd=image_dir,
            stdout=logs,
            stderr=logs,
            env=os.environ.copy()
        )

    pidf.write_text(str(proc.pid))
    meta.write_text(
        f"image={image}\n"
        f"cmd={' '.join(cmd)}\n"
        f"start={int(time.time())}\n"
        f"supervised={supervised}\n"
    )

    return name


def list_containers():
    for c in CONTAINERS_DIR.iterdir():
        pidf = c / "pid"
        pid = pidf.read_text() if pidf.exists() else "?"
        running = pid.isdigit() and os.path.exists(f"/proc/{pid}")
        yield c.name, pid, running


def inspect_container(name: str) -> dict:
    cdir = CONTAINERS_DIR / name
    if not cdir.exists():
        raise RuntimeError("Container not found")

    meta = {}
    m = cdir / "meta"
    if m.exists():
        for line in m.read_text().splitlines():
            k, v = line.split("=", 1)
            meta[k] = v

    pidf = cdir / "pid"
    pid = pidf.read_text() if pidf.exists() else "Unknown"
    running = pid.isdigit() and os.path.exists(f"/proc/{pid}")

    return {
        "name": name,
        "image": meta.get("image", "unknown"),
        "cmd": meta.get("cmd", "unknown"),
        "pid": pid,
        "status": "running" if running else "stopped",
        "logs": str(cdir / "logs.txt"),
    }


def stop_container(name: str):
    cdir = CONTAINERS_DIR / name
    pidf = cdir / "pid"

    if not pidf.exists():
        raise RuntimeError("Container not running")

    pid = pidf.read_text()
    if pid.isdigit() and os.path.exists(f"/proc/{pid}"):
        os.kill(int(pid), 9)

    pidf.unlink(missing_ok=True)


def remove_container(name: str):
    try:
        stop_container(name)
    except RuntimeError:
        pass

    shutil.rmtree(CONTAINERS_DIR / name, ignore_errors=True)


def exec_container(name: str, command: str):
    info = inspect_container(name)
    img = IMAGES_DIR / info["image"]
    subprocess.run(command, shell=True, cwd=img)


def show_logs(name: str):
    log = CONTAINERS_DIR / name / "logs.txt"
    if log.exists():
        print(log.read_text())