import typer
from pocketbox import runtime

app = typer.Typer(help="Pocketbox – lightweight container runtime")


def msg(symbol: str, text: str):
    print(f"[{symbol}] {text}")


@app.command()
def build(path: str = typer.Argument(None)):
    """Build an image from a Pocketfile"""
    image = runtime.build_image(path)
    msg("✅", f" Image '{image}' Built Successfully")


@app.command()
def run(supervised: bool = typer.Option(False)):
    """Run a new container from the current image"""
    image = runtime.build_image(None)
    name = runtime.run_container(image, supervised)
    msg("▶️",  f"Container '{name}' running")


@app.command()
def ps():
    """List running and stopped containers"""
    print("NAME\t\tSTATUS\t\tPID")
    print("-" * 40)
    for name, pid, running in runtime.list_containers():
        status = "running" if running else "stopped"
        print(f"{name}\t{status}\t{pid}")


@app.command()
def inspect(name: str):
    """Inspect a container"""
    info = runtime.inspect_container(name)
    for k, v in info.items():
        print(f"{k.capitalize()}: {v}")


@app.command()
def stop(name: str):
    """Stop a running container"""
    runtime.stop_container(name)
    msg("⏹ ", f"Container '{name}' Stopped")


@app.command()
def rm(name: str):
    """Remove a container"""
    runtime.remove_container(name)
    msg("🗑",  f"Image '{name}' Removed")


@app.command()
def exec(name: str, cmd: str):
    """Execute a command inside the container image"""
    runtime.exec_container(name, cmd)


@app.command()
def logs(name: str):
    """Show container logs"""
    runtime.show_logs(name)



if __name__ == "__main__":
    app()