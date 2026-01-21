import typer
from rich.console import Console
from rich.table import Table
from rich import box
from pocketbox import runtime
import time
from pathlib import Path

console = Console()
app = typer.Typer(help="Pocketbox – lightweight container runtime")


# -------------------------
# Helper for messages
# -------------------------
def msg(symbol: str, text: str):
    console.print(f"[bold green]{symbol}[/bold green] {text}")


# -------------------------
# CLI Commands
# -------------------------

@app.command()
def build(path: str = typer.Argument(None)):
    """Build an image from a Pocketfile"""
    image = runtime.build_image(path)
    msg("✅", f"Image '{image}' built successfully!")

@app.command()
def pull(image: str):
    """Pull a base image from the Pocketbox registry"""
    pulled = runtime.pull_image(image)
    msg("⬇️", f"Base image '{pulled}' pulled successfully")


@app.command()
def run(supervised: bool = typer.Option(False), name: str = typer.Option(None)):
    """Run a new container from the current image"""
    image = runtime.build_image(None)
    cname = runtime.run_container(image, supervised, name)
    msg("▶️", f"Container '{cname}' running")


@app.command()
def ps():
    """List running and stopped containers"""
    table = Table(title="Pocketbox Containers", box=box.ROUNDED)
    table.add_column("NAME", style="cyan")
    table.add_column("STATUS", style="magenta")
    table.add_column("PID", justify="right")

    for name, pid, running in runtime.list_containers():
        status = "[green]running[/green]" if running else "[red]stopped[/red]"
        table.add_row(name, status, str(pid))

    console.print(table)


@app.command()
def inspect(name: str):
    """Inspect a container"""
    info = runtime.inspect_container(name)
    for k, v in info.items():
        console.print(f"[bold]{k.capitalize()}:[/bold] {v}")


@app.command()
def stop(name: str):
    """Stop a running container"""
    runtime.stop_container(name)
    msg("⏹", f"Container '{name}' stopped")


@app.command()
def rm(name: str):
    """Remove a container"""
    runtime.remove_container(name)
    msg("🗑", f"Container '{name}' removed")


@app.command()
def exec(name: str, cmd: str):
    """Execute a command inside the container image"""
    runtime.exec_container(name, cmd)
    msg("💻", f"Executed command in container '{name}'")


@app.command()
def logs(name: str, follow: bool = typer.Option(False, "--follow", "-f", help="Follow logs in real-time")):
    """Show container logs"""
    log_file = Path(runtime.CONTAINERS_DIR) / name / "logs.txt"

    if not log_file.exists():
        console.print(f"[red]Logs not found for container '{name}'[/red]")
        return

    if not follow:
        console.print(log_file.read_text())
        return

    # Real-time follow
    console.print(f"[bold yellow]Following logs for container '{name}'... (CTRL+C to stop)[/bold yellow]\n")
    with log_file.open() as f:
        f.seek(0, 2)  # Go to end of file
        try:
            while True:
                line = f.readline()
                if not line:
                    time.sleep(0.2)
                    continue
                print(line, end="")
        except KeyboardInterrupt:
            console.print("\n[bold red]Stopped following logs[/bold red]")


# -------------------------
# Entry point for pip-installed CLI
# -------------------------
def main():
    app()


if __name__ == "__main__":
    main()