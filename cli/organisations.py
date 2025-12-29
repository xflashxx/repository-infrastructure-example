"""
CLI for managing organisations.
"""

from typing import Annotated
from uuid import UUID

import typer
from _context import get_context
from rich.console import Console
from rich.table import Table

from repository_infrastructure_example.services.organisation import (
    OrganisationServiceError,
)

console = Console()
organisation_app = typer.Typer(
    help="Organisation management commands", no_args_is_help=True
)


@organisation_app.command("list", help="List all organisations")
def list_organisations(
    limit: Annotated[
        int,
        typer.Option(
            help="Limit the number of organisations returned. If 0, return all organisations."
        ),
    ] = 0,
) -> None:
    # Prepare table
    table = Table(show_header=True, header_style="bold")
    table.add_column("ID", no_wrap=True)
    table.add_column("Name")
    table.add_column("Slug")
    table.add_column("Email")
    table.add_column("Active", justify="center")
    table.add_column("Created")
    table.add_column("Updated")

    ctx = get_context()

    try:
        organisations = ctx.services.organisation.get_organisations()
    except OrganisationServiceError as error:
        console.print(f"[red]Error:[/red] {error}")
        raise typer.Exit(code=1)

    if limit > 0:
        organisations = organisations[:limit]

    for org in organisations:
        table.add_row(
            str(org.id),
            org.name,
            org.slug,
            org.email,
            str(org.is_active),
            org.created_at.isoformat(timespec="seconds"),
            org.updated_at.isoformat(timespec="seconds"),
        )
    console.print(table)


@organisation_app.command("add", help="Add a new organisation")
def add_organisation(
    name: Annotated[str, typer.Argument(help="The name of the organisation to add.")],
    email: Annotated[str, typer.Argument(help="The email of the organisation to add.")],
    is_active: Annotated[
        bool,
        typer.Option(
            "--active/--inactive",
            help="Whether the organisation is active.",
        ),
    ] = True,
) -> None:
    ctx = get_context()

    try:
        organisation_id = ctx.services.organisation.add_organisation(
            name=name, email=email, is_active=is_active
        )
    except OrganisationServiceError as error:
        console.print(f"[red]Error:[/red] {error}")
        raise typer.Exit(code=1)

    console.print(f"[green]Successfully added organisation:[/green] {organisation_id}")


@organisation_app.command("update", help="Update an existing organisation")
def update_organisation(
    organisation_id: Annotated[
        UUID,
        typer.Argument(help="ID of the organisation to update."),
    ],
    name: Annotated[
        str | None,
        typer.Option(
            help="New name of the organisation.",
        ),
    ] = None,
    email: Annotated[
        str | None,
        typer.Option(
            help="New contact email.",
        ),
    ] = None,
    is_active: Annotated[
        bool | None,
        typer.Option(
            "--active/--inactive",
            help="Set organisation active or inactive.",
        ),
    ] = None,
) -> None:
    ctx = get_context()

    if name is None and email is None and is_active is None:
        raise typer.BadParameter(
            "At least one of --name, --email, or --active/--inactive must be provided."
        )
    try:
        ctx.services.organisation.update_organisation(
            organisation_id=organisation_id,
            name=name,
            email=email,
            is_active=is_active,
        )
    except OrganisationServiceError as error:
        console.print(f"[red]Error:[/red] {error}")
        raise typer.Exit(code=1)

    console.print(
        f"[green]Successfully updated organisation:[/green] {organisation_id}"
    )


@organisation_app.command("delete", help="Delete an organisation")
def delete_organisation(
    organisation_id: Annotated[
        UUID,
        typer.Argument(help="ID of the organisation to delete."),
    ],
) -> None:
    ctx = get_context()

    try:
        ctx.services.organisation.delete_organisation(
            organisation_id=organisation_id,
        )
    except OrganisationServiceError as error:
        console.print(f"[red]Error:[/red] {error}")
        raise typer.Exit(code=1)

    console.print(
        f"[green]Successfully deleted organisation:[/green] {organisation_id}"
    )
