import sys
from functools import cached_property

from loguru import logger
from rich.console import Console
from rich.table import Table

from repository_infrastructure_example import __appname__, __version__
from repository_infrastructure_example.application.settings import ApplicationSettings
from repository_infrastructure_example.containers.repositories import Repositories
from repository_infrastructure_example.containers.services import Services
from repository_infrastructure_example.infrastructure.postgres import PostgresClient


class ApplicationContext:
    _postgres_client: PostgresClient

    def __init__(self) -> None:
        self._set_up_loguru()
        self._set_up_postgres_client()

    @cached_property
    def settings(self) -> ApplicationSettings:
        return ApplicationSettings()

    def _set_up_loguru(self) -> None:
        logger.remove()
        logger.add(sys.stderr, level=self.settings.logging.log_level)

    def _set_up_postgres_client(self) -> None:
        self._postgres_client = PostgresClient(
            connection_string=self.settings.database.get_connection_uri()
        )

    @property
    def postgres_client(self) -> PostgresClient:
        return self._postgres_client

    @cached_property
    def repositories(self) -> Repositories:
        return Repositories(
            backend=self.settings.repository.backend,
            postgres_client=self.postgres_client,
        )

    @cached_property
    def services(self) -> Services:
        return Services(repositories=self.repositories)

    def log_settings(self) -> None:
        console = Console()
        table = Table(
            title=f"{__appname__} {__version__}",
            show_header=True,
            header_style="bold magenta",
        )
        table.add_column("Setting")
        table.add_column("Value")

        for settings in (
            self.settings.database,
            self.settings.repository,
            self.settings.logging,
        ):
            # Section header
            table.add_row(
                f"[bold yellow]{settings.__class__.__name__}[/bold yellow]", ""
            )

            items = list(settings.model_dump().items())
            for i, (env_var_name, value) in enumerate(items, start=1):
                table.add_row(str(env_var_name).upper(), str(value))

                # After the last row of this setting, insert a divider
                if i == len(items):
                    table.add_row("─" * 20, "")

        console.print(table)
