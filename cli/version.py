import typer

from repository_infrastructure_example import __appname__, __version__

version_app = typer.Typer()


@version_app.command()
def version():
    print(f"{__appname__}: Version {__version__}")
