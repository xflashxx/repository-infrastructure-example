from typing_extensions import assert_never

from repository_infrastructure_example.infrastructure.postgres import PostgresClient
from repository_infrastructure_example.repositories.backend import RepositoryBackend
from repository_infrastructure_example.repositories.organisation import (
    OrganisationRepository,
)
from repository_infrastructure_example.repositories.postgresql.organisation.repository import (
    PostgresOrganisationRepository,
)
from repository_infrastructure_example.repositories.postgresql.user.repository import (
    PostgresUserRepository,
)
from repository_infrastructure_example.repositories.user import UserRepository


class Repositories:
    _backend: RepositoryBackend
    _postgres_client: PostgresClient

    def __init__(
        self, *, backend: RepositoryBackend, postgres_client: PostgresClient
    ) -> None:
        self._backend = backend
        self._postgres_client = postgres_client

    @property
    def organisation(self) -> OrganisationRepository:
        if self._backend == RepositoryBackend.POSTGRESQL:
            return PostgresOrganisationRepository(
                session_factory=self._postgres_client.session
            )

        assert_never(self._backend)

    @property
    def user(self) -> UserRepository:
        if self._backend == RepositoryBackend.POSTGRESQL:
            return PostgresUserRepository(session_factory=self._postgres_client.session)

        assert_never(self._backend)
