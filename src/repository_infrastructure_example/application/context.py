"""
Application context for this example project.

Provides a central place for dependency injection and access to all
services, use-cases, and infrastructure needed by the app. Framework-agnostic
and intended as the single entry point for obtaining application-level objects.
"""

from functools import cached_property

from pydantic import BaseModel

from repository_infrastructure_example.application.settings import ApplicationSettings
from repository_infrastructure_example.containers.clients import Clients
from repository_infrastructure_example.containers.repositories import Repositories
from repository_infrastructure_example.containers.services import Services
from repository_infrastructure_example.infrastructure.postgres import PostgresClient
from repository_infrastructure_example.infrastructure.redis import get_redis_client
from repository_infrastructure_example.utilities.logging import (
    log_settings,
    set_up_loguru,
)


class ApplicationContext:
    _clients: Clients

    def __init__(self) -> None:
        set_up_loguru(self.settings.logging.level)
        self._set_up_clients()

    def _set_up_clients(self) -> None:
        self._clients = Clients(
            postgres_client=PostgresClient(
                connection_string=self.settings.postgres.get_connection_uri()
            ),
            redis_client=get_redis_client(self.settings.redis),
        )

    @cached_property
    def settings(self) -> ApplicationSettings:
        return ApplicationSettings()

    @property
    def clients(self) -> Clients:
        return self._clients

    @cached_property
    def repositories(self) -> Repositories:
        return Repositories(
            backend=self.settings.repository.backend,
            postgres_client=self.clients.postgres,
        )

    @cached_property
    def services(self) -> Services:
        return Services(
            repositories=self.repositories,
            redis_client=self.clients.redis,
            cache_settings=self.settings.cache,
            redis_cache_settings=self.settings.redis,
        )

    def log_settings(self) -> None:
        # Gather all settings, then log them
        settings_to_log: list[BaseModel] = [setting for _, setting in self.settings]
        log_settings(*settings_to_log)
