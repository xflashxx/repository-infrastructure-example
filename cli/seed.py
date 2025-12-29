from typing import Annotated, Final

import typer
from _context import get_context
from loguru import logger
from typer.main import Typer

from repository_infrastructure_example.dev.factories.organisation import (
    generate_organisations,
)
from repository_infrastructure_example.dev.factories.user import (
    generate_users,
)

_DEFAULT_ORGANISATION_COUNT: Final[int] = 5
_DEFAULT_USER_COUNT_PER_ORGANISATION: Final[int] = 10

seed_app: Typer = typer.Typer(help="Development database seeding")


@seed_app.command()
def seed(
    *,
    n_organisations: Annotated[
        int, typer.Option(help="Number of organisations to create.")
    ] = _DEFAULT_ORGANISATION_COUNT,
    n_users_per_organisation: Annotated[
        int, typer.Option(help="Number of users per organisation.")
    ] = _DEFAULT_USER_COUNT_PER_ORGANISATION,
) -> None:
    """Seeds the development database with synthetic data."""
    ctx = get_context()
    # Run database migrations
    ctx.postgres_client.run_migrations()

    logger.info("Seeding fake data...")

    for organisation in generate_organisations(
        n=n_organisations,
    ):
        # Add the organisation
        organisation_id = ctx.services.organisation.add_organisation(
            name=organisation.name,
            email=organisation.email,
            is_active=organisation.is_active,
        )

        # Add users for the organisation
        for user in generate_users(n=n_users_per_organisation):
            _ = ctx.services.user.add_user(
                organisation_id=organisation_id,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                is_active=user.is_active,
            )
