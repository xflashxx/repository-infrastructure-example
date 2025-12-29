"""
Repository Infrastructure Example CLI

This CLI provides a set of commands for interacting with the repository example.
"""

import typer
from organisations import organisation_app
from seed import seed_app
from users import user_app
from version import version_app

app = typer.Typer(help="Repository Example CLI", no_args_is_help=True)

app.add_typer(version_app)
app.add_typer(seed_app)
app.add_typer(organisation_app, name="organisations")
app.add_typer(user_app, name="users")


if __name__ == "__main__":
    app()
