from typing import Annotated
from uuid import UUID

import typer
from _context import get_context
from rich.console import Console
from rich.table import Table

from repository_infrastructure_example.services.organisation import (
    OrganisationServiceError,
)
from repository_infrastructure_example.services.user import UserServiceError

console = Console()
user_app = typer.Typer(help="User management commands", no_args_is_help=True)


@user_app.command("list", help="List all users")
def list_users(
    organisation_id: Annotated[
        UUID,
        typer.Argument(help="The ID of the organisation to list users for."),
    ],
    limit: Annotated[
        int,
        typer.Option(
            help="Limit the number of users returned. If 0, return all users."
        ),
    ] = 0,
) -> None:
    # Prepare table
    table = Table(show_header=True, header_style="bold")
    table.add_column("ID", no_wrap=True)
    table.add_column("First Name")
    table.add_column("Last Name")
    table.add_column("Email")
    table.add_column("Active", justify="center")
    table.add_column("Created")
    table.add_column("Updated")

    ctx = get_context()

    try:
        users = ctx.services.user.get_users(organisation_id=organisation_id)
    except (OrganisationServiceError, UserServiceError) as error:
        console.print(f"[red]Error:[/red] {error}")
        raise typer.Exit(code=1)

    if limit > 0:
        users = users[:limit]

    for user in users:
        table.add_row(
            str(user.id),
            user.first_name,
            user.last_name,
            user.email,
            str(user.is_active),
            user.created_at.isoformat(),
            user.updated_at.isoformat(),
        )
    console.print(table)


@user_app.command("add", help="Add a new user")
def add_user(
    organisation_id: Annotated[
        UUID,
        typer.Argument(help="The ID of the organisation to add the user to."),
    ],
    first_name: Annotated[str, typer.Argument(help="The first name of the user.")],
    last_name: Annotated[str, typer.Argument(help="The last name of the user.")],
    email: Annotated[str, typer.Argument(help="The email of the user.")],
    is_active: Annotated[
        bool,
        typer.Option(
            "--active/--inactive",
            help="Whether the user is active.",
        ),
    ] = True,
) -> None:
    ctx = get_context()

    try:
        user_id = ctx.services.user.add_user(
            organisation_id=organisation_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_active=is_active,
        )
    except (OrganisationServiceError, UserServiceError) as error:
        console.print(f"[red]Error:[/red] {error}")
        raise typer.Exit(code=1)

    console.print(f"[green]Successfully added user:[/green] {user_id}")


@user_app.command("update", help="Update an existing user")
def update_user(
    organisation_id: Annotated[
        UUID,
        typer.Argument(help="The ID of the organisation the user belongs to."),
    ],
    user_id: Annotated[UUID, typer.Argument(help="ID of the user to update.")],
    first_name: Annotated[
        str | None,
        typer.Option(
            help="New first name of the user. If not provided, retains existing."
        ),
    ] = None,
    last_name: Annotated[
        str | None,
        typer.Option(
            help="New last name of the user. If not provided, retains existing."
        ),
    ] = None,
    email: Annotated[
        str | None,
        typer.Option(help="New email of the user. If not provided, retains existing."),
    ] = None,
    is_active: Annotated[
        bool | None,
        typer.Option(
            "--active/--inactive",
            help="Set user active or inactive. If not provided, retains existing.",
        ),
    ] = None,
) -> None:
    ctx = get_context()

    if first_name is None and last_name is None and email is None and is_active is None:
        raise typer.BadParameter(
            "At least one of --first-name, --last-name, --email, or --active/--inactive must be provided."
        )

    try:
        ctx.services.user.update_user(
            organisation_id=organisation_id,
            user_id=user_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_active=is_active,
        )
    except (OrganisationServiceError, UserServiceError) as error:
        console.print(f"[red]Error:[/red] {error}")
        raise typer.Exit(code=1)

    console.print(f"[green]Successfully updated user:[/green] {user_id}")


@user_app.command("delete", help="Delete an existing user")
def delete_user(
    organisation_id: Annotated[
        UUID,
        typer.Argument(help="The ID of the organisation the user belongs to."),
    ],
    user_id: Annotated[UUID, typer.Argument(help="ID of the user to delete.")],
) -> None:
    ctx = get_context()

    try:
        ctx.services.user.delete_user(
            organisation_id=organisation_id,
            user_id=user_id,
        )
    except (OrganisationServiceError, UserServiceError) as error:
        console.print(f"[red]Error:[/red] {error}")
        raise typer.Exit(code=1)

    console.print(f"[green]Successfully deleted user:[/green] {user_id}")
