# Created by Jan Rummens at 8/01/2021
from nemonet.runner.vision_runner import Runner
import typer

app = typer.Typer()

@app.command()
def scenario(name: str, useconfig: bool = False):
    try:
        if useconfig:
            runner = Runner(runner_config="runner_config.json")
        else:
            runner = Runner()
        runner.execute_scenario(name)
    except ValueError:
        typer.echo(f"invalid commandline")
        raise typer.Exit(code=1)


def main():
    app()

