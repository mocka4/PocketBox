import typer
from pocketbox import runtime

app = typer.Typer()


@app.command()
def build(path: str = typer.Argument(None)):
    image = runtime.build_image(path)
    print(f"✅ Image '{image}' built!")


@app.command()
def run(supervised: bool = typer.Option(False)):
    image = runtime.build_image(None)
    name = runtime.run_container(image, supervised)
    print(f"▶ {name} running")


@app.command()
def ps():
    for name, pid, running in runtime.list_containers():
        print(f"{name}: {'running' if running else 'stopped'} (PID {pid})")


@app.command()
def inspect(name: str):
    info = runtime.inspect_container(name)
    for k, v in info.items():
        print(f"{k.capitalize()}: {v}")


@app.command()
def stop(name: str):
    runtime.stop_container(name)
    print(f"Container '{name}' stopped.")


@app.command()
def rm(name: str):
    runtime.remove_container(name)
    print(f"Container '{name}' removed.")


@app.command()
def exec(name: str, cmd: str):
    runtime.exec_container(name, cmd)


@app.command()
def logs(name: str):
    runtime.show_logs(name)


if __name__ == "__main__":
    app()